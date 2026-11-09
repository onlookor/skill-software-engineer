#!/usr/bin/env python3
"""锚点只读检测器与索引生成器（anchor_index）。

唯一职责：扫描全库 `@` 引用，产出三张可机读表与一份汇总，并校验规范 F-1～F-8。
**只读**：不修改母本、registry yaml、README、投影；输出只写到 --out 目录。

用法:
  python3 registry/scripts/anchor_index.py
  python3 registry/scripts/anchor_index.py --out /tmp/anchor_index
  python3 registry/scripts/anchor_index.py --target-mode prefix      # 按"全部带前缀"形态校验
  python3 registry/scripts/anchor_index.py --target-mode prefix_id   # 再校验 ID＋子锚

形态预留: none(现状) / prefix(纯前缀) / prefix_id(前缀＋ID＋子锚)。
退出码: 0=无 hard 失败; 1=存在 hard 失败; 2=环境/参数错误。
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print('需要 PyYAML（registry/scripts/project.py 亦依赖）', file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[2]          # .../software-engineering
REG = ROOT / 'registry'
MOTHER = ROOT / '软件工程元框架成文法.md'
REG_YAML = REG / 'method_registry.yaml'
PROF_YAML = REG / 'profiles.yaml'
VOCAB_YAML = REG / 'predicate_vocabulary.yaml'
COMPILE = ROOT / '编译规范.md'

# 冻结文件（0.22：历史记录不重写），只做快照复算，不计入 F-1～F-6 失败
FROZEN = [
    '软件工程元框架成文法-changlog.md',
    'todo.md',
    'adr/ADR-PRJ-2-01-approved-20261104-PRJ交付空间谓词槽纠正.md',
    'adr/ADR-KP-G3-01-approved-20261103-GRD-PRJ-GOV剖面变更.md',
    'R2提案-KP-G3-包络义务适用范围.md',
    'adr/ADR-INLINE-MARK-01-approved-20261104-五项行内标记方案.md',
    'adr/ADR-G-OWN-CSL-01-approved-20261104-行内出处补写.md',
    'adr/ADR-G-STY-ENV-01-approved-20261104-接地编译前置两闸.md',
    'adr/ADR-G-PRJ-1-01-approved-20261106-有意保留悬空.md',
    # 已批准且已执行（2026-11-07 纳入）：执行后其锚点只做快照复算，不再参与活跃锚点约束（F-1～F-6）
    'adr/ADR-SRC-02-approved-20261106-signals字段方案A.md',      # ADR-SRC-02（approved；SRC-001…008 与 signals 已落地）
    'adr/ADR-VG09-01-approved-20261106-谓词表一次性扩容.md',      # ADR-VG09-01（approved；母本 9.5 与 vocabulary 已落地）
    'adr/ADR-R2-APPL-01-approved-20261106-applicability事实槽.md',  # ADR-R2-APPL-01（approved；applicability 事实槽已落地）
]
# 活跃集合（规范 F-1 的适用域）；不存在的文件自动跳过
LIVE = [
    'registry/method_registry.yaml', 'registry/profiles.yaml',
    'registry/predicate_vocabulary.yaml', 'registry/README.md',
    'registry/projections/STY.md', 'registry/projections/索引.md',
    'registry/projections/自检报告.md', 'registry/projections/勘察义务清单.md',
    '参考资料缺口核对报告.md',
]

# 0.22.2 承诺四：文件三分。LIVE／FROZEN 为显式清单，其余为 sandbox。
def classify(rel: str) -> str:
    in_live, in_frozen = rel in LIVE, rel in FROZEN
    if in_live and in_frozen:
        return 'conflict'
    if in_live:
        return 'live'
    if in_frozen:
        return 'frozen'
    return 'sandbox'

SCOPE_DENOM = ('live',)


TARGETS = {  # prefix -> (相对路径, kind)
    'm': ('软件工程元框架成文法.md', 'mother'),
    'r': ('registry/method_registry.yaml', 'registry'),
    'p': ('registry/profiles.yaml', 'profiles'),
    'v': ('registry/predicate_vocabulary.yaml', 'vocab'),
    'c': ('编译规范.md', 'compile'),
}
KIND_TO_FILE = {k: (p, kk) for k, (p, kk) in TARGETS.items()}

# 上下文线索 → 目标（长词在前，避免前缀误吞）
CLUES = [
    ('registry/README', 'd:registry/README.md', 'doc'),
    ('method_registry', 'r', 'registry'),
    ('predicate_vocabulary', 'v', 'vocab'),
    ('profiles.yaml', 'p', 'profiles'),
    ('project.py', 'd:registry/scripts/project.py', 'doc'),
    ('勘察义务清单', 'd:registry/projections/勘察义务清单.md', 'doc'),
    ('自检报告', 'd:registry/projections/自检报告.md', 'doc'),
    ('STY.md', 'd:registry/projections/STY.md', 'doc'),
    ('changlog', 'd:软件工程元框架成文法-changlog.md', 'doc'),
    ('changelog', 'd:软件工程元框架成文法-changlog.md', 'doc'),
    ('编译规范', 'c', 'compile'),
    ('单行本', 'd:软件工程元框架总纲单行本.md', 'doc'),
    ('母本', 'm', 'mother'),
    ('索引', 'd:registry/projections/索引.md', 'doc'),
    ('todo', 'd:todo.md', 'doc'),
    ('README', 'd:README.md', 'doc'),
    ('R2提案', 'd:R2提案-KP-G3-包络义务适用范围.md', 'doc'),
]

# 行锚：@[prefix:]N[-N][#sub][~end]，其后不接数字/小数点
LINE_RE = re.compile(
    r'@(?:(?P<prefix>[mrpvcd]):)?(?P<a>\d{1,5})(?:-(?P<b>\d{1,5}))?'
    r'(?P<sub>#[A-Za-z0-9_\u4e00-\u9fff.\-]+)?'
    r'(?![\d.])'
)
# 条款式：@[prefix:]1.2.3
CLAUSE_RE = re.compile(r'@(?:(?P<prefix>[mrpvcd]):)?(?P<clause>\d+(?:\.\d+){1,})(?![\d.])')
# 键@行 形态（如 time_semantics@69），不是规范锚点，单列统计
KEY_AT_RE = re.compile(r'(?<![@\w])(?P<key>[A-Za-z_][A-Za-z0-9_.]*)\s*@(?P<a>\d{1,5})(?![\d.])')

HEAD_RE = re.compile(r'^(#{2,6})\s+((?:\d+\.)+\d*|\d+)\s')


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='ignore')


def norm_cell(s: str) -> str:
    return re.sub(r'[*`\s]', '', s)


class Doc:
    def __init__(self, rel: str):
        self.rel = rel
        self.path = ROOT / rel
        self.exists = self.path.is_file()
        self.lines = read(self.path).split('\n') if self.exists else []
        self.headings = []          # (line, level, clause)
        self.all_heads = []         # (line, level, 逐字标题)：含非数字标题（表标识取用）
        self.titles = []            # (line, 逐字标题)：所有 Markdown 标题（`#sec-` 的匹配集）
        self.clause_dups = []
        self.fence_lines = set()    # 代码围栏内行号（规范 R5：围栏内不视为锚点）
        if self.exists:
            seen = defaultdict(list)
            in_fence = False
            for i, ln in enumerate(self.lines, 1):
                if ln.lstrip().startswith('```'):
                    in_fence = not in_fence
                    self.fence_lines.add(i)
                    continue
                if in_fence:
                    self.fence_lines.add(i)
                    continue
                m = HEAD_RE.match(ln)
                if m:
                    num = m.group(2).strip()
                    self.headings.append((i, len(m.group(1)), num))
                    seen[num].append(i)
                tm = re.match(r'^#{1,6}\s+(.*\S)\s*$', ln)
                if tm:
                    self.titles.append((i, tm.group(1)))
                    self.all_heads.append((i, ln.index(' '), tm.group(1)))
            self.clause_dups = {k: v for k, v in seen.items() if len(v) > 1}

    def clause_at(self, line: int):
        best = None
        for (ln, lvl, num) in self.headings:
            if ln <= line:
                best = (ln, lvl, num)
            else:
                break
        return best

    def line_of_clause(self, clause: str):
        hits = [ln for (ln, _lvl, num) in self.headings if num == clause]
        return hits[0] if len(hits) == 1 else (None if not hits else -1)

    # ── 结构地址解析（ADR-ANCHOR-01 §3）──────────────────────────
    def clause_span(self, clause: str):
        """(标题行, 结束行[不含])；条款号不唯一或不存在返回 None。"""
        hits = [(ln, lvl) for (ln, lvl, num) in self.headings if num == clause]
        if len(hits) != 1:
            return None
        ln, lvl = hits[0]
        end = len(self.lines) + 1
        for (l2, lvl2, _n2) in self.headings:
            if l2 > ln and lvl2 <= lvl:
                end = l2
                break
        return ln, end

    def para_lines(self, clause: str):
        """条款内正文段落首行（非标题/表格/列表/围栏/空行），1-based 序位。"""
        span = self.clause_span(clause)
        if not span:
            return []
        start, end = span
        out, fence = [], False
        for i in range(start + 1, end):
            s = self.lines[i - 1].strip()
            if s.startswith('```'):
                fence = not fence
                continue
            if fence or not s or s.startswith('#') or s.startswith('|') or set(s) <= set('-|: '):
                continue
            if re.match(r'^(?:[-*+]|\d+[.)])\s', s):
                continue
            out.append(i)
        return out

    def list_item_paths(self, clause: str):
        """条款内列表项 {路径: 行号}；路径形如 `1`／`2.3`（按缩进层级）。"""
        span = self.clause_span(clause)
        if not span:
            return {}
        start, end = span
        out, counters, fence = {}, [], False
        for i in range(start + 1, end):
            raw = self.lines[i - 1]
            s = raw.strip()
            if s.startswith('```'):
                fence = not fence
                continue
            if fence or not re.match(r'^(?:[-*+]|\d+[.)])\s', s):
                continue
            indent = len(raw) - len(raw.lstrip(' '))
            level = min(indent // 2, 5)
            while len(counters) <= level:
                counters.append(0)
            counters[level] += 1
            del counters[level + 1:]
            out['.'.join(str(c) for c in counters)] = i
        return out

    def heading_line(self, label: str):
        hits = [ln for (ln, _lvl, num) in self.headings if num == label]
        return hits[0] if len(hits) == 1 else (None if not hits else -1)

    # ── 代码块锚（ADR-ANCHOR-01 §3.6 `code-`）────────────────────
    def code_lines(self, clause: str):
        """条款内围栏代码块的正文行（不含 ``` 分隔行），文档序 1-based。"""
        span = self.clause_span(clause)
        if not span:
            return []
        start, end = span
        return [i for i in range(start + 1, end)
                if i in self.fence_lines and not self.lines[i - 1].lstrip().startswith('```')]

    def code_ids(self, clause: str):
        """{标识: [行号]}；标识取代码行首个「大写字母＋至少一位数字」token。"""
        out = defaultdict(list)
        for i in self.code_lines(clause):
            m = CODE_LINE_ID_RE.match(self.lines[i - 1].strip())
            if m:
                out[m.group(1)].append(i)
        return out


# ── 台账装载（只读）─────────────────────────────────────────────
def load_registry():
    if not REG_YAML.is_file():
        return {}, set()
    d = yaml.safe_load(read(REG_YAML)) or {}
    row_ids = set()
    for e in d.get('entries') or []:
        for sp in (e.get('provenance') or {}).get('source_pointers') or []:
            if sp.get('source_type') == 'row_id' and '-' in str(sp.get('value')):
                row_ids.add(norm_cell(str(sp['value']).split('-', 1)[1]))
    return d, row_ids


def entry_by_id(d, eid):
    for e in d.get('entries') or []:
        if e.get('entry_id') == eid:
            return e
    return None


def has_path(obj, dotted: str) -> bool:
    cur = obj
    for part in dotted.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return cur is not None


EXCLUDE_DOCS = {
    '锚点与引用规范.md', '提案-锚点改版-语义锚点.md',          # 语法示例，不计入引用统计
    'registry/anchor_index/插行位移演练报告.md',                # 演练报告含锚点示例（2026-11-05）
}

# `标识@行` 五类分账（2026-11-05 裁定，见规范 §10.1）
DOC_KEYS = {'README', 'README.md', 'profiles.yaml', 'project.py', 'method_registry.yaml',
            'predicate_vocabulary.yaml', 'changlog', 'changelog', 'todo', 'todo.md',
            'R2', 'R2提案', 'STY.md', '索引', '自检报告', '勘察义务清单'}
FORMULA_KEY_RE = re.compile(r'^[A-Z][A-Z0-9]{0,2}\d{0,2}$')
FIELD_KEY_RE = re.compile(r'^[a-z_][a-z0-9_]*$')
DESC_LABELS = {'Read'}          # 动作词+行号，属描述型标签
LABEL_CLASSES = ('formula_label', 'field_label')

# 新式文档/剖面锚：@d:<路径>#<sub>、@p:<KIND>#<sub>
DOC_ANCHOR_RE = re.compile(r'@(?P<prefix>[dp]):(?P<loc>[^\s#，。；|）（：、／]+)')
# 结构地址锚（ADR-ANCHOR-01）：@m:<条款>[#sub]、@r:<entry>[#field-…]、@v:<term>、@c:<节>
STRUCT_RE = re.compile(
    r'@(?P<prefix>[mrv]):(?P<loc>[A-Za-z0-9_.\-]+)(?:#(?P<sub>[^\s，。；|）（：、／]+))?')
# 规范 §2 新增两式（2026-11-05 裁定）：key- 点路径（下标必须保留）／sec- 逐字标题
SUB_KEY_RE = re.compile(r'#key-(?P<path>[A-Za-z0-9_.\[\]-]+)')
SUB_FN_RE = re.compile(r'#fn-(?P<name>[A-Za-z_][A-Za-z0-9_]*)')
PY_SUFFIXES = ('.py',)

# 行键转义（ADR-ANCHOR-01 §3.11）：子锚字符集不含全角括注与顿号，正文一律转义
ESC_MAP = {'（': '~p~', '）': '~q~', '、': '~d~'}
ESC_REV = {v: k for k, v in ESC_MAP.items()}
FORBIDDEN_SUB = '（）：、，；／'


def escape_sub(s: str) -> str:
    for ch, code in ESC_MAP.items():
        s = s.replace(ch, code)
    return s


def unescape_sub(s: str) -> str:
    for code, ch in ESC_REV.items():
        s = s.replace(code, ch)
    return s


# 代码块行首标识：FM-13／GS-03／T1／E3／M34 等（大写字母＋至少一位数字）
# 注意：不得与下方 table_ids 用的 CODE_ID_RE（表标识）重名，否则后者会覆盖前者
CODE_LINE_ID_RE = re.compile(r'^[^\w]*([A-Z]{1,4}-?\d{1,4}[A-Z]?)(?![A-Za-z0-9])')


def build_rowkey_map(rowkey_rows):
    """{(doc, clause, '#row-…'): [行号]}，供结构地址解析。"""
    out = defaultdict(list)
    for r in rowkey_rows:
        out[(r['doc'], r['clause'], r['key'])].append(r['line'])
    return out


def vocab_terms() -> set:
    d = yaml.safe_load(read(VOCAB_YAML)) or {}
    out = set()
    for key in ('vocab', 'terms', 'predicates'):
        val = d.get(key)
        if isinstance(val, list):
            for it in val:
                if isinstance(it, dict):
                    for k in ('name', 'term', 'id'):
                        if it.get(k):
                            out.add(str(it[k]))
                elif isinstance(it, str):
                    out.add(it)
        elif isinstance(val, dict):
            out.update(str(k) for k in val)
    return out


def resolve_struct(prefix: str, loc: str, sub: str, docs: dict,
                   rowkey_map, reg, terms: set) -> dict:
    """解析结构地址；返回落点与候选取数（>1 由 F-9 报冲突）。"""
    empty = dict(landing_line='', landing_form='', clause='', resolvable_to='none',
                 struct_candidates=0, struct_unit='')
    if prefix == 'm':
        doc = docs.get('软件工程元框架成文法.md')
        if not doc or not doc.exists or not re.fullmatch(r'\d+(?:\.\d+)+', loc):
            return empty
        span = doc.clause_span(loc)
        if not span:
            return empty
        if not sub or sub == 'head':
            return dict(landing_line=span[0], landing_form='heading', clause=loc,
                        resolvable_to='clause_head', struct_candidates=1,
                        struct_unit=f'm:{loc}:head')
        if sub.startswith('p-') and sub[2:].isdigit():
            lines = doc.para_lines(loc)
            n = int(sub[2:])
            if 1 <= n <= len(lines):
                return dict(landing_line=lines[n - 1], landing_form='paragraph', clause=loc,
                            resolvable_to='para', struct_candidates=1,
                            struct_unit=f'm:{loc}:{sub}')
            return empty
        if sub.startswith('li-'):
            path = sub[3:]
            if not re.fullmatch(r'\d+(?:\.\d+)*', path):
                return empty
            hit = doc.list_item_paths(loc).get(path)
            if hit:
                return dict(landing_line=hit, landing_form='list_item', clause=loc,
                            resolvable_to='list_item', struct_candidates=1,
                            struct_unit=f'm:{loc}:{sub}')
            return empty
        if sub.startswith('row-'):
            cand = rowkey_map.get(('软件工程元框架成文法.md', loc, '#' + unescape_sub(sub)), [])
            if len(cand) == 1:
                return dict(landing_line=cand[0], landing_form='table_row', clause=loc,
                            resolvable_to='row_id', struct_candidates=1,
                            struct_unit=f'm:{loc}:{sub}')
            return dict(empty, struct_candidates=len(cand), struct_unit=f'm:{loc}:{sub}')
        if sub.startswith('code-'):
            rest = sub[5:]
            if rest.isdigit():
                lines = doc.code_lines(loc)
                n = int(rest)
                if 1 <= n <= len(lines):
                    return dict(landing_line=lines[n - 1], landing_form='code', clause=loc,
                                resolvable_to='code_ordinal', struct_candidates=1,
                                struct_unit=f'm:{loc}:{sub}')
                return empty
            cand = doc.code_ids(loc).get(rest, [])
            if len(cand) == 1:
                return dict(landing_line=cand[0], landing_form='code', clause=loc,
                            resolvable_to='code_id', struct_candidates=1,
                            struct_unit=f'm:{loc}:{sub}')
            return dict(empty, struct_candidates=len(cand), struct_unit=f'm:{loc}:{sub}')
        return empty
    if prefix == 'r':
        if not re.match(r'^[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9]+$', loc):
            return empty
        e = entry_by_id(reg, loc)
        if e is None:
            return empty
        if not sub:
            return dict(landing_line='', landing_form='entry', clause='',
                        resolvable_to='entry', struct_candidates=1, struct_unit=f'r:{loc}')
        if sub.startswith('field-'):
            ok = has_path(e, sub[6:])
            return dict(landing_line='', landing_form='field', clause='',
                        resolvable_to='entry_field' if ok else 'none',
                        struct_candidates=1 if ok else 0, struct_unit=f'r:{loc}:{sub}')
        return empty
    if prefix == 'v':
        ok = loc in terms
        return dict(landing_line='', landing_form='term', clause='',
                    resolvable_to='term' if ok else 'none',
                    struct_candidates=1 if ok else 0, struct_unit=f'v:{loc}')
    return empty


def _split_dotted(path: str):
    """把 `a.b[0].c` 拆为 [('key','a'),('key','b'),('idx',0),('key','c')]。"""
    parts, i = [], 0
    while i < len(path):
        if path[i] == '[':
            j = path.find(']', i)
            if j < 0 or not path[i + 1:j].isdigit():
                return None
            parts.append(('idx', int(path[i + 1:j])))
            i = j + 1
        else:
            j = len(path)
            for ch in '.[':
                k = path.find(ch, i)
                if k >= 0:
                    j = min(j, k)
            key = path[i:j]
            if not key:
                return None
            parts.append(('key', key))
            i = j
        if i < len(path) and path[i] == '.':
            i += 1
    return parts


def _walk(node, parts):
    """在 yaml.compose 节点树上按 parts 走；返回节点或 None。"""
    for kind, val in parts:
        if kind == 'key':
            if not isinstance(node, yaml.MappingNode):
                return None
            hit = None
            for k, v in node.value:
                if str(getattr(k, 'value', k)) == val:
                    hit = v
                    break
            if hit is None:
                return None
            node = hit
        else:
            if not isinstance(node, yaml.SequenceNode) or not (0 <= val < len(node.value)):
                return None
            node = node.value[val]
    return node


def key_path_valid(path: Path, dotted: str) -> bool:
    """结构化文件里 key- 点路径须按原样（含 [n]）解析到恰好一个节点。"""
    parts = _split_dotted(dotted)
    if not parts or not path.is_file():
        return False
    text = read(path)
    if path.suffix in ('.yaml', '.yml'):
        try:
            root = yaml.compose(text)
        except Exception:
            return False
        return root is not None and _walk(root, parts) is not None
    if path.suffix == '.json':
        try:
            cur = json.loads(text)
        except Exception:
            return False
        for kind, val in parts:
            if kind == 'key':
                if not isinstance(cur, dict) or val not in cur:
                    return False
                cur = cur[val]
            else:
                if not isinstance(cur, list) or not (0 <= val < len(cur)):
                    return False
                cur = cur[val]
        return True
    return False


def _py_tree(path: Path):
    if not path.is_file():
        return None
    try:
        return ast.parse(read(path))
    except Exception:
        return None


def fn_symbol_valid(path: Path, name: str) -> bool:
    """脚本锚 `#fn-`：AST 校验该函数在该文件内存在且唯一。"""
    tree = _py_tree(path)
    if tree is None:
        return False
    hits = [n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    return len(hits) == 1


def key_symbol_valid(path: Path, name: str) -> bool:
    """脚本内 `#key-`：AST 校验模块级符号（顶层赋值／常量）存在且唯一。"""
    tree = _py_tree(path)
    if tree is None:
        return False
    hits = 0
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in n.targets):
            hits += 1
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == name:
            hits += 1
    return hits == 1


_PROF_CACHE = None


def profiles_by_id() -> dict:
    global _PROF_CACHE
    if _PROF_CACHE is None:
        d = yaml.safe_load(read(PROF_YAML)) or {}
        _PROF_CACHE = {p.get('entry_id'): p for p in d.get('profiles') or []}
    return _PROF_CACHE


def profile_exists(kind: str) -> bool:
    return f'kind_profile_{kind}' in profiles_by_id()


def profile_field_valid(kind: str, dotted: str) -> bool:
    """`@p:<KIND>#<字段>`：字段路径相对该剖面根，须解析到恰好一个节点。"""
    p = profiles_by_id().get(f'kind_profile_{kind}')
    if p is None:
        return False
    parts = _split_dotted(dotted)
    if not parts:
        return False
    cur = p
    for typ, val in parts:
        if typ == 'key':
            if not isinstance(cur, dict) or val not in cur:
                return False
            cur = cur[val]
        else:
            if not isinstance(cur, list) or not (0 <= val < len(cur)):
                return False
            cur = cur[val]
    return True


def sec_match(doc: 'Doc', rest: str) -> tuple:
    """`#sec-` 按目标文件标题集做最长前缀匹配；命中标题须在文件内唯一。"""
    cands = [t for _ln, t in doc.titles if rest.startswith(t)]
    if not cands:
        return None, 0
    best = max(cands, key=len)
    n = sum(1 for _ln, t in doc.titles if t == best)
    return (best, n) if n == 1 else (None, n)


def key_class(rel: str, token: str) -> str:
    key = token.split('@')[0].strip()
    if rel in FROZEN:
        return 'frozen_key_at'
    if key.startswith('kind_profile'):
        return 'field_path'
    if key in DOC_KEYS:
        return 'doc_ref'
    if FORMULA_KEY_RE.match(key):
        return 'formula_label'
    if FIELD_KEY_RE.match(key) or key in DESC_LABELS:
        return 'field_label'
    return 'other'


def split_labels(rows: list) -> tuple:
    """返回 (锚点行, label_refs 行)；936 处标签引用不计入锚点总量。"""
    labels = [r for r in rows if r.get('label_class') in LABEL_CLASSES]
    anchors = [r for r in rows if r.get('label_class') not in LABEL_CLASSES]
    return anchors, labels


# ── 扫描 ────────────────────────────────────────────────────────
def target_files() -> list[str]:
    self_rel = str(Path(__file__).resolve().relative_to(ROOT))
    out = [p for p in ROOT.rglob('*') if p.is_file() and p.suffix in ('.md', '.yaml', '.py')
           and '.git' not in p.parts and 'archieve' not in p.parts
           and str(p.relative_to(ROOT)) not in EXCLUDE_DOCS
           and str(p.relative_to(ROOT)) != self_rel]   # 不扫描检测器自身（docstring 含语法示例）
    return [str(p.relative_to(ROOT)) for p in sorted(out)]


def esc(s: str) -> str:
    return s.strip().startswith('#')


def in_backticks(line: str, pos: int) -> bool:
    return line.count('`', 0, pos) % 2 == 1


def doc_len(docs, rel) -> int:
    d = docs.get(rel)
    return len(d.lines) if d and d.exists else 0


def assign_target(rel: str, num: int, prefix, ctx: str, docs: dict) -> tuple[str, str, str]:
    """返回 (target_rel, target_kind, basis)。

    basis ∈ explicit / context / context_short_fallback / self_range / range_inference / default / unknown
    """
    mlen = doc_len(docs, '软件工程元框架成文法.md')
    rlen = doc_len(docs, 'registry/method_registry.yaml')
    own_len = doc_len(docs, rel)
    if prefix:
        if prefix == 'd':
            return ('', 'doc', 'explicit')
        p, kind = TARGETS[prefix]
        return (p, kind, 'explicit')
    # 上下文线索（线索目标过短则回落母本/registry，并留痕）
    for clue, tgt, kind in CLUES:
        if clue in ctx:
            cand = tgt[2:] if tgt.startswith('d:') else TARGETS[tgt][0]
            kk = 'doc' if tgt.startswith('d:') else TARGETS[tgt][1]
            if num <= doc_len(docs, cand):
                return (cand, kk, 'context')
            if num <= mlen:
                return ('软件工程元框架成文法.md', 'mother', 'context_short_fallback')
            if num <= rlen:
                return ('registry/method_registry.yaml', 'registry', 'context_short_fallback')
            return ('', 'unknown', 'unknown')
    if num > mlen:
        if rel == 'registry/method_registry.yaml':
            return (rel, 'registry', 'self_range')
        if rel in ('软件工程元框架成文法-changlog.md', 'todo.md') and num <= own_len:
            return (rel, 'doc', 'self_range')
        if num <= rlen:
            return ('registry/method_registry.yaml', 'registry', 'range_inference')
        return ('', 'unknown', 'unknown')
    # 数值同时落在自身文件与母本范围 → 结构性歧义，按母本默认
    return ('软件工程元框架成文法.md', 'mother', 'default')


def scan(docs: dict, reg, row_ids: set, rowkey_map=None, terms=None) -> dict:
    rowkey_map = rowkey_map or {}
    terms = terms or set()
    rows = []
    for rel in sorted(docs):
        doc = docs[rel]
        txt_lines = doc.lines
        for i, line in enumerate(txt_lines, 1):
            claimed = []                   # 已被行锚/条款锚占用的字符区间，防止 key@N 重复计数
            if i in doc.fence_lines:       # 规范 R5：代码围栏内的 @ 不是锚点
                continue
            if doc.path.suffix == '.py' and esc(line):
                continue
            # 结构地址锚优先（@m:条款[#sub]／@r:entry[#field-]／@v:term）
            for m in STRUCT_RE.finditer(line):
                prefix, loc = m.group('prefix'), m.group('loc')
                sub = m.group('sub') or ''
                if re.fullmatch(r'\d{1,5}', loc):      # 纯数字 = 旧式行锚，交给 LINE_RE
                    continue
                res = resolve_struct(prefix, loc, sub, docs, rowkey_map, reg, terms)
                tgt_rel = {'m': '软件工程元框架成文法.md',
                           'r': 'registry/method_registry.yaml',
                           'v': 'registry/predicate_vocabulary.yaml'}[prefix]
                tgt_kind = {'m': 'mother', 'r': 'registry', 'v': 'vocab'}[prefix]
                claimed.append((m.start(), m.end()))
                rows.append(dict(
                    file=rel, line=i, col=m.start() + 1, token=m.group(0), form='struct',
                    in_code_span=in_backticks(line, m.start()), in_comment=esc(line),
                    in_yaml_value=rel.endswith('.yaml') and bool(line.strip()) and not esc(line),
                    target_file=tgt_rel, target_kind=tgt_kind, assign_basis='explicit',
                    landing_form=res['landing_form'], landing_line=res['landing_line'],
                    clause=res['clause'], resolvable_to=res['resolvable_to'],
                    row_key='', row_registered='', range='0', drift='n/a', drift_delta='',
                    sub_kind=(sub.split('-')[0] if sub else 'head'), sub_value=sub,
                    struct_candidates=res['struct_candidates'], struct_unit=res['struct_unit'],
                    label_class='',
                ))
            for m in LINE_RE.finditer(line):
                if any(s <= m.start() < e for s, e in claimed):
                    continue
                a = int(m.group('a')); b = m.group('b')
                range_end = ''
                range_note = ''
                if b:
                    b = int(b)
                    if b < a:
                        # 短式区间：@2505-25 视为 2505–2525
                        cand = int(str(a)[:max(1, len(str(a)) - len(str(b)))] + str(b))
                        if cand >= a:
                            b = cand; range_note = 'short_form'
                        else:
                            range_note = 'reversed'
                    range_end = b
                prefix = m.group('prefix')
                sub = (m.group('sub') or '')[1:]
                ctx = line[max(0, m.start() - 80):m.start()]
                tgt_rel, tgt_kind, basis = assign_target(rel, a, prefix, ctx, docs)
                tdoc = docs.get(tgt_rel) if tgt_rel else None
                tlen = len(tdoc.lines) if tdoc and tdoc.exists else 0
                # 落点
                land = None
                if tdoc and tdoc.exists and 1 <= a <= tlen:
                    land = tdoc.lines[a - 1].strip()
                if land is None:
                    form = 'blank'
                elif land.startswith('|'):
                    form = 'table_row'
                elif land.startswith('#'):
                    form = 'heading'
                elif re.match(r'^(?:-|\*)\s', land) or re.match(r'^\d+[.)]\s', land):
                    form = 'list_item'
                elif not land:
                    form = 'blank'
                else:
                    form = 'paragraph'
                # 可解析性
                clause = None
                if tdoc and tdoc.exists and 1 <= a <= tlen:
                    c = tdoc.clause_at(a)
                    clause = c[2] if c else None
                clause_ok = bool(clause) and not (tdoc and clause in tdoc.clause_dups)
                row_key = None
                row_ok = None
                if form == 'table_row' and land:
                    row_key = land.strip('|').split('|')[0].strip()
                    row_ok = norm_cell(row_key) in row_ids
                # 字段路径（仅 prefix_id 形态）
                field_ok = None
                if tgt_kind == 'registry' and sub.startswith('field-') and basis == 'explicit':
                    e = entry_by_id(reg, m.group(0))  # 占位：locator 解析见下
                    field_ok = None
                resolvable = 'line_only'
                if form == 'heading' and clause_ok:
                    resolvable = 'clause_id'
                elif form == 'table_row' and row_ok:
                    resolvable = 'row_id'
                elif tdoc is None or not tdoc.exists:
                    resolvable = 'none'
                # 漂移
                drift = 'n/a'
                delta = ''
                if tdoc is None or not tdoc.exists:
                    drift = 'target_missing'
                elif a > tlen:
                    drift = 'out_of_range'
                    delta = str(a - tlen)
                # 邻条款号启发式已废弃（ADR-ANCHOR-01 §7.7）：1,041/1,052 是正常交叉引用，
                # 不是漂移。漂移只由 F-3 的落点指纹比对判定。
                rows.append(dict(
                    file=rel, line=i, col=m.start() + 1, token=m.group(0),
                    form='legacy' if not prefix else 'prefix',
                    in_code_span=in_backticks(line, m.start()),
                    in_comment=esc(line),
                    in_yaml_value=rel.endswith('.yaml') and bool(line.strip()) and not esc(line),
                    target_file=tgt_rel or '', target_kind=tgt_kind, assign_basis=basis,
                    landing_form=form, landing_line=a,
                    clause=clause or '', resolvable_to=resolvable,
                    row_key=row_key or '', row_registered=row_ok if row_ok is not None else '',
                    range='1' if b else '0', range_end=range_end, range_note=range_note,
                    drift=drift, drift_delta=delta,
                    sub_kind='', sub_value='',
                ))
                claimed.append((m.start(), m.end()))
            # 条款式（@1.2.3）单列
            for m in CLAUSE_RE.finditer(line):
                if any(s <= m.start() < e for s, e in claimed):
                    continue
                claimed.append((m.start(), m.end()))
                rows.append(dict(
                    file=rel, line=i, col=m.start() + 1, token=m.group(0), form='clause_style',
                    in_code_span=in_backticks(line, m.start()), in_comment=esc(line),
                    in_yaml_value=rel.endswith('.yaml') and bool(line.strip()) and not esc(line),
                    target_file='', target_kind='', assign_basis='explicit_clause',
                    landing_form='', landing_line='', clause=m.group('clause') or '',
                    resolvable_to='clause_id', row_key='', row_registered='',
                    range='0', drift='n/a', drift_delta='',
                    sub_kind='', sub_value='',
                ))
            for m in DOC_ANCHOR_RE.finditer(line):
                if any(s <= m.start() < e for s, e in claimed):
                    continue
                prefix = m.group('prefix'); loc = m.group('loc')
                if prefix == 'p':
                    tgt_rel, tgt_kind = 'registry/profiles.yaml', 'profiles'
                else:
                    tgt_rel, tgt_kind = loc, 'doc'
                tdoc = docs.get(tgt_rel) or Doc(tgt_rel)
                rest = line[m.end():]
                sub_kind = sub_value = ''
                end = m.end()
                resolvable = 'doc_symbol' if tdoc.exists else 'none'
                if rest.startswith('#key-'):
                    km = SUB_KEY_RE.match(rest)
                    sub_kind = 'key'
                    if km:
                        sub_value = km.group('path')
                        end = m.end() + km.end()
                        if prefix == 'p':
                            resolvable = 'key_path' if profile_field_valid(loc, sub_value) else 'none'
                        elif tgt_rel.endswith(PY_SUFFIXES):
                            resolvable = 'key_symbol' if key_symbol_valid(ROOT / tgt_rel, sub_value) else 'none'
                        else:
                            resolvable = 'key_path' if key_path_valid(ROOT / tgt_rel, sub_value) else 'none'
                    else:
                        end = m.end() + 5
                        resolvable = 'none'
                elif rest.startswith('#fn-'):
                    sub_kind = 'fn'
                    fm = SUB_FN_RE.match(rest)
                    if fm and tgt_rel.endswith(PY_SUFFIXES):
                        sub_value = fm.group('name')
                        end = m.end() + fm.end()
                        resolvable = 'fn_symbol' if fn_symbol_valid(ROOT / tgt_rel, sub_value) else 'none'
                    else:
                        end = m.end() + 4
                        resolvable = 'none'
                elif rest.startswith('#sec-'):
                    sub_kind = 'sec'
                    title, n = sec_match(tdoc, rest[5:])
                    if title:
                        sub_value = title
                        end = m.end() + 5 + len(title)
                        resolvable = 'sec_title'
                    else:
                        end = m.end() + 5
                        resolvable = 'none'
                elif prefix == 'p':
                    sm = re.match(r'#(?P<f>[A-Za-z0-9_.\[\]-]+)', rest)
                    if sm:
                        sub_value = sm.group('f')
                        end = m.end() + sm.end()
                        resolvable = 'field_path' if profile_field_valid(loc, sub_value) else 'none'
                    else:
                        resolvable = 'kind_profile' if profile_exists(loc) else 'none'
                claimed.append((m.start(), end))
                rows.append(dict(
                    file=rel, line=i, col=m.start() + 1, token=line[m.start():end],
                    form='prefix_field' if prefix == 'p' else 'prefix_doc',
                    sub_kind=sub_kind, sub_value=sub_value,
                    in_code_span=in_backticks(line, m.start()), in_comment=esc(line),
                    in_yaml_value=rel.endswith('.yaml') and bool(line.strip()) and not esc(line),
                    target_file=tgt_rel, target_kind=tgt_kind, assign_basis='explicit',
                    landing_form='', landing_line='', clause='', resolvable_to=resolvable,
                    row_key='', row_registered='', range='0', drift='n/a', drift_delta='',
                    label_class='',
                ))
            for m in KEY_AT_RE.finditer(line):
                if any(s <= m.start() < e for s, e in claimed):
                    continue
                claimed.append((m.start(), m.end()))
                rows.append(dict(
                    file=rel, line=i, col=m.start() + 1, token=m.group(0), form='key_at',
                    in_code_span=in_backticks(line, m.start()), in_comment=esc(line),
                    in_yaml_value=rel.endswith('.yaml') and bool(line.strip()) and not esc(line),
                    target_file='', target_kind='', assign_basis='key_at',
                    landing_form='', landing_line='', clause='', resolvable_to='none',
                    row_key='', row_registered='', range='0', drift='n/a', drift_delta='',
                    label_class=key_class(rel, m.group(0)),
                    sub_kind='', sub_value='',
                ))
    return rows


# ── 表标识与行键推导（规范 §3.1）────────────────────────────────
CODE_ID_RE = re.compile(r'^([A-Za-z][A-Za-z0-9\-]+)$')
SEC_SPLIT_RE = re.compile(r'[：:，,。；（(→|/]')


def _head_before(heads, line, max_level):
    best = None
    for (ln, lvl, txt) in heads:
        if ln >= line:
            break
        if lvl <= max_level:
            best = (ln, lvl, txt)
    return best


def _head_token(txt):
    return re.split(r'[.．、：:（(\s]', txt)[0].strip()


def table_blocks(doc):
    """返回表块 [{clause,start,header,rows[(line,cells)]}]；表头与分隔行不入 rows（规范 §3.1）。"""
    out, lines = [], doc.lines
    i = 1
    while i <= len(lines):
        s = lines[i - 1]
        if (i not in doc.fence_lines and s.lstrip().startswith('|') and i < len(lines)
                and re.match(r'^\s*\|[ :\-|]+\|\s*$', lines[i])):
            cl = doc.clause_at(i)
            hdr = [c.strip() for c in s.strip().strip('|').split('|')]
            rows, j = [], i + 2
            while j <= len(lines) and lines[j - 1].lstrip().startswith('|'):
                if j not in doc.fence_lines:
                    cells = [c.strip() for c in lines[j - 1].strip().strip('|').split('|')]
                    if any(cells) and not set(''.join(cells)) <= set('-: '):
                        rows.append((j, cells))
                j += 1
            if cl:
                out.append(dict(clause=cl[2], start=i, header=hdr, rows=rows))
            i = j
            continue
        i += 1
    return out


def table_ids(doc, blocks, unresolved):
    """语义表标识：分节码（SM-xx）→ 表头首列 → 同条款冲突时追加前置小节短标签。"""
    ids = []
    for b in blocks:
        h = _head_before(doc.all_heads, b['start'], 5)
        tok = _head_token(h[2]) if h and h[1] >= 4 else ''
        base = tok if CODE_ID_RE.match(tok or '') else ''
        if not base and b['header']:
            first = norm_cell(b['header'][0])
            if re.sub(r'[\W_]', '', first, flags=re.UNICODE):
                base = first
            else:
                h2 = _head_before(doc.all_heads, b['start'], 2)
                base = norm_cell(re.sub(r'^附录[一二三四五六七八九十]+[：:]', '', h2[2])) if h2 else ''
        ids.append(base)
    base_cnt = Counter((b['clause'], ids[i]) for i, b in enumerate(blocks))
    for idx, b in enumerate(blocks):
        if ids[idx] and base_cnt[(b['clause'], ids[idx])] > 1:
            h3 = _head_before(doc.all_heads, b['start'], 3)
            suf = _head_token(h3[2]) if h3 else ''
            ids[idx] = f'{ids[idx]}-{norm_cell(suf)}' if suf else ''
    final_cnt = Counter((b['clause'], ids[i]) for i, b in enumerate(blocks))
    for idx, b in enumerate(blocks):
        if not ids[idx] or final_cnt[(b['clause'], ids[idx])] > 1:
            unresolved.append((b['clause'], b['start'], b['header'][0] if b['header'] else ''))
    return ids


def derive_row_keys(docs):
    """按规范 §3.1 推导 `#row-<表标识>-<行名>[-<次级键>]`；返回 (行键表, 未解表标识, 受影响条款)。"""
    out, unresolved, affected = [], [], set()
    for rel in sorted({p for p, _ in TARGETS.values()}):
        d = docs.get(rel)
        if not d or not d.exists:
            continue
        blocks = table_blocks(d)
        ids = table_ids(d, blocks, unresolved)
        by_clause = defaultdict(Counter)
        for b in blocks:
            for _, r in b['rows']:
                by_clause[b['clause']][norm_cell(r[0])] += 1
        for b, tid in zip(blocks, ids):
            if any(by_clause[b['clause']][norm_cell(r[0])] > 1 for _, r in b['rows']):
                affected.add((rel, b['clause']))
            cnt = Counter(norm_cell(r[0]) for _, r in b['rows'])
            for line, cells in b['rows']:
                name = norm_cell(cells[0])
                sec = ''
                if cnt[name] > 1 and len(cells) > 1:
                    sec = norm_cell(SEC_SPLIT_RE.split(cells[1])[0])[:12]
                key = f'#row-{tid}-{name}' + (f'-{sec}' if sec else '')
                if cnt[name] > 1:
                    conflict = '同表首列重名→次级键'
                elif by_clause[b['clause']][name] > 1:
                    conflict = '跨表重名→表标识消歧'
                else:
                    conflict = ''
                out.append(dict(doc=rel, clause=b['clause'], table_id=tid, table_line=b['start'],
                                header=b['header'][0] if b['header'] else '', line=line,
                                row_name=name, secondary=sec, key=key,
                                conflict=conflict))
    return out, unresolved, affected


def classify_mixed(rows):
    """返回 (活跃侧跨目标串, 仅冻结侧致歧义串, 后者在活跃侧出现次数)。"""
    live_rows = [r for r in rows if r['file'] in LIVE and r['form'] in ('legacy', 'prefix')]
    all_kinds, live_kinds = defaultdict(set), defaultdict(set)
    for r in rows:
        k = r['target_kind']
        if k and k != 'unknown':
            all_kinds[r['token']].add(k)
    for r in live_rows:
        k = r['target_kind']
        if k and k != 'unknown':
            live_kinds[r['token']].add(k)
    mixed_live = {t: v for t, v in live_kinds.items() if len(v) > 1}
    frozen_only = {t: v for t, v in all_kinds.items()
                   if len(v) > 1 and len(live_kinds.get(t, set())) <= 1}
    occ = sum(1 for r in live_rows if r['token'] in frozen_only)
    return mixed_live, frozen_only, occ


# ── 断言 F-1～F-10（ADR-ANCHOR-01 §6）──────────────────────────
def assertions(rows, docs, reg, mode, rowkeys, unresolved_ids, f10=None, f3=None) -> list[dict]:
    out = []
    live_all = [r for r in rows if classify(r['file']) == 'live']
    live_line = [r for r in live_all if r['form'] in ('legacy', 'prefix')]
    frozen_line = [r for r in rows if classify(r['file']) == 'frozen'
                   and r['form'] in ('legacy', 'prefix')]
    conflict = sorted({r['file'] for r in rows if classify(r['file']) == 'conflict'})
    out.append(dict(id='CFG-01', desc='同一文件不得同时命中 LIVE 与 FROZEN',
                    status='fail' if conflict else 'pass', count=len(conflict),
                    examples=' | '.join(conflict[:10])))
    # F-1：LIVE 内非结构地址锚（裸行号＋带前缀行号）
    out.append(dict(id='F-1', desc='F-1：LIVE 内非结构地址锚数（裸行号＋带前缀行号）＝0',
                    status='fail' if live_line else 'pass', count=len(live_line),
                    examples=' | '.join(f"{r['file']}:{r['line']} {r['token']}" for r in live_line[:10])))
    # F-2：结构地址必须解析到恰一结构单元；@!GAP: 不在扫描面内
    miss = [r for r in live_all if r['form'] in ('struct', 'prefix_doc', 'prefix_field')
            and r['resolvable_to'] == 'none']
    out.append(dict(id='F-2', desc='F-2：结构地址解析到恰一结构单元（0 个即失败）',
                    status='fail' if miss else 'pass', count=len(miss),
                    examples=' | '.join(f"{r['file']}:{r['line']} {r['token']}->{r['target_file']}" for r in miss[:10])))
    # F-3：只做落点内容指纹比对（邻条款号启发式已废弃，ADR-ANCHOR-01 §7.7）
    # 基线未冻结时 status=info 且 coverage=0——不得当作通过（ADR §11 挡板）。
    f3 = f3 or dict(status='info', count=0, coverage=0, examples='fingerprint baseline not frozen')
    out.append(dict(id='F-3', desc='F-3：结构锚落点首句/首列指纹与基线一致（按 struct_unit 归并根因）',
                    status=f3['status'], count=f3['count'], coverage=f3['coverage'],
                    roots=f3.get('roots', 0), affected=f3.get('affected', f3['count']),
                    examples=f3['examples']))
    # ESC-01：row-/code- 子锚禁用字符必须转义（ADR-ANCHOR-01 §3.7）
    esc_bad = [(r, esc_errors(r, docs)) for r in live_all if r['form'] == 'struct']
    esc_bad = [(r, e) for r, e in esc_bad if e]
    out.append(dict(id='ESC-01', desc='ESC-01：row-/code- 子锚无未转义禁用字符',
                    status='fail' if esc_bad else 'pass', count=len(esc_bad),
                    coverage=sum(1 for r in live_all if r['form'] == 'struct'
                                 and (r.get('sub_value') or '').startswith(('row-', 'code-'))),
                    examples=' | '.join(f"{r['file']}:{r['line']} {r['token']} {','.join(e)}"
                                        for r, e in esc_bad[:10])))
    # F-4：跨目标类歧义串（冻结侧只做快照，见 INFO-1）
    mixed, frozen_only, frozen_occ = classify_mixed(rows)
    out.append(dict(id='F-4', desc='F-4：同一锚点串不跨目标类',
                    status='fail' if mixed else 'pass', count=len(mixed),
                    examples=' | '.join(f'{k}:{"/".join(sorted(v))}' for k, v in list(mixed.items())[:10])))
    out.append(dict(id='INFO-1', desc='frozen_only_mixed（仅冻结侧致歧义；info，不计入 F-4 分母）',
                    status='info', count=len(frozen_only),
                    examples=f'live_occurrences={frozen_occ} | ' +
                             ' | '.join(f'{k}:{"/".join(sorted(v))}' for k, v in
                                        list(frozen_only.items())[:10])))
    # F-5 行键唯一性
    dup_keys = Counter((r['doc'], r['clause'], r['key']) for r in rowkeys)
    dups = sum(v - 1 for v in dup_keys.values() if v > 1)
    out.append(dict(id='F-5', desc='行键式 row 子锚在同条款内唯一（表标识＋次级键）',
                    status='fail' if (dups or unresolved_ids) else 'pass',
                    count=dups + len(unresolved_ids),
                    examples=' | '.join(f'{c}/{k}×{v}' for (d_, c, k), v in dup_keys.items() if v > 1)[:300] +
                             (f' || unresolved_table_id={unresolved_ids}' if unresolved_ids else '')))
    # F-6 区间反向
    bad = [f"{r['file']}:{r['line']} {r['token']}" for r in live_line if r['range_note'] == 'reversed']
    out.append(dict(id='F-6', desc='F-6：区间起止有序，无反向',
                    status='fail' if bad else 'pass', count=len(bad),
                    examples=' | '.join(bad[:10])))
    # F-7 台账计数守恒
    entries = reg.get('entries') or []
    meta_n = (reg.get('meta') or {}).get('entry_count')
    seed_n = sum(1 for e in entries if e.get('status') == 'seed')
    ok7 = (len(entries) == meta_n) if meta_n is not None else False
    out.append(dict(id='F-7', desc='台账计数守恒（entries==meta.entry_count，seed 计数可解释）',
                    status='pass' if ok7 else 'fail', count=0 if ok7 else 1,
                    examples=f'entries={len(entries)} meta.entry_count={meta_n} seed={seed_n} '
                             f'gaps={len(reg.get("gaps") or [])} SO={len(reg.get("survey_obligations") or [])}'))
    # F-9 地址唯一性：(clause, sub) 解析到 >1 个单元即冲突
    # 覆盖数＝实际参与判定的不同结构地址数（struct_unit 去重）；0 表示空测，不等于通过。
    amb = [r for r in live_all if r['form'] == 'struct' and int(r.get('struct_candidates') or 0) > 1]
    covered = {r['struct_unit'] for r in live_all
               if r['form'] == 'struct' and int(r.get('struct_candidates') or 0) >= 1}
    out.append(dict(id='F-9', desc='F-9：结构地址 (clause, sub) 唯一性冲突＝0',
                    status='fail' if amb else 'pass', count=len(amb),
                    coverage=len(covered),
                    examples=f'checked_pairs={len(covered)} conflicts={len(amb)} | ' +
                             ' | '.join(f"{r['file']}:{r['line']} {r['token']}->{r['struct_unit']}"
                                        for r in amb[:10])))
    # F-10 重排稳定性：与本文件基线比对（B−1 后由 B0 冻结）
    f10 = f10 or dict(status='info', count=0, examples='baseline not frozen', diff={})
    out.append(dict(id='F-10', desc='F-10：重排前后结构地址变化集＝本批声明清单',
                    status=f10['status'], count=f10['count'], examples=f10['examples']))
    # INFO-2 冻结侧行号锚快照（只观测）
    out.append(dict(id='INFO-2', desc='冻结侧行号锚快照（as-of 豁免，只观测）',
                    status='info', count=len(frozen_line),
                    examples=' | '.join(f"{r['file']}:{r['line']} {r['token']}" for r in frozen_line[:5])))
    return out


def fingerprint(line: str) -> str:
    return re.sub(r'\s+', ' ', line.strip())[:60]


def landing_fingerprint(doc, line, form: str) -> str:
    """落点指纹：表行取首列，正文/围栏取首句（≤60 字），其余取整行规范化。"""
    try:
        n = int(line)
    except (TypeError, ValueError):
        return ''
    if doc is None or not getattr(doc, 'exists', False) or not (1 <= n <= len(doc.lines)):
        return ''
    s = doc.lines[n - 1].strip()
    if form == 'table_row':                        # 首列
        return norm_cell(s.strip('|').split('|')[0])[:60]
    t = re.sub(r'\s+', ' ', s)
    if form in ('paragraph', 'code'):              # 首句
        t = re.split(r'[。；]', t)[0]
    return t[:60]


def esc_errors(row, docs) -> list[str]:
    """ESC-01：row-/code- 子锚内出现未转义禁用字符，或 `~` 不是合法转义码。"""
    sub = row.get('sub_value') or ''
    if not (sub.startswith('row-') or sub.startswith('code-')):
        return []
    errs = []
    if any(ch in FORBIDDEN_SUB for ch in sub):
        errs.append('forbidden_in_sub')
    # 正则会在禁用字符处截断：token 后紧跟的字符即被截掉的原文
    doc = docs.get(row['file'])
    if doc and doc.exists:
        ln = doc.lines[int(row['line']) - 1]
        end = int(row['col']) - 1 + len(row['token'])
        if end < len(ln) and ln[end] in FORBIDDEN_SUB:
            errs.append('truncated_at_forbidden')
    i = 0
    while i < len(sub):
        if sub[i] == '~':
            if sub[i:i + 3] not in ESC_REV:
                errs.append('bad_escape')
                break
            i += 3
        else:
            i += 1
    return errs


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    fields = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with path.open('w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields, restval='')
        w.writeheader()
        w.writerows(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(REG / 'anchor_index'), help='输出目录（默认 registry/anchor_index）')
    ap.add_argument('--target-mode', choices=('none', 'prefix', 'prefix_id'), default='none',
                    help='none=现状; prefix=全部带目标前缀; prefix_id=前缀+ID+子锚')
    ap.add_argument('--freeze-baseline', action='store_true',
                    help='把本次结构地址解析结果写为 registry/anchor_baseline.json（供 F-3／F-10）')
    ap.add_argument('--baseline', default='',
                    help='基线文件路径（默认 registry/anchor_baseline.json；自测时可指向 /tmp）')
    ap.add_argument('--expected-changes', default='',
                    help='本批声明的变化清单 JSON（key 数组）；F-10 只允许清单内的变化')
    args = ap.parse_args(argv)

    rels = target_files()
    docs = {rel: Doc(rel) for rel in rels}          # 一次性快照，F-8 幂等基于同一快照
    for rel in ['软件工程元框架成文法.md', 'registry/method_registry.yaml', 'registry/profiles.yaml',
                'registry/predicate_vocabulary.yaml', '编译规范.md'] + LIVE + FROZEN:
        docs.setdefault(rel, Doc(rel))
    reg, row_ids = load_registry()
    rowkey_rows, unresolved_ids, affected = derive_row_keys(docs)
    rowkey_map = build_rowkey_map(rowkey_rows)
    terms = vocab_terms()

    rows, label_rows = split_labels(scan(docs, reg, row_ids, rowkey_map, terms))
    for r in rows:
        r['scope'] = classify(r['file'])

    def struct_snapshot(all_rows):
        """{(file|token|occ): 结构单元} 与 {(file|token|occ): 落点指纹}。"""
        occ, units, fps = Counter(), {}, {}
        for r in all_rows:
            if r['form'] != 'struct' or classify(r['file']) != 'live':
                continue
            k = (r['file'], r['token'], occ[(r['file'], r['token'])])
            occ[(r['file'], r['token'])] += 1
            key = '%s|%s|%d' % k
            tdoc = docs.get(r['target_file']) if r['target_file'] else None
            fp = landing_fingerprint(tdoc, r['landing_line'], r['landing_form'])
            if not fp:
                # 无行落点（如 @r:...#field- 的 YAML 点路径锚）不属 F-3 覆盖面：
                # F-3 是「行落点指纹」比对，字段锚的稳定性由 F-2 解析承担（ADR §7.7）。
                continue
            units[key] = r['struct_unit']
            fps[key] = fp
        return units, fps

    cur_map, cur_fps = struct_snapshot(rows)
    base_path = Path(args.baseline) if args.baseline else (REG / 'anchor_baseline.json')
    if args.freeze_baseline:
        base_path.parent.mkdir(parents=True, exist_ok=True)
        base_path.write_text(json.dumps({'units': cur_map, 'fps': cur_fps},
                                        ensure_ascii=False, indent=1, sort_keys=True),
                             encoding='utf-8')
        f10 = dict(status='info', count=0,
                   examples=f'baseline frozen: {len(cur_map)} structural anchors, {len(cur_fps)} fingerprints')
        f3 = dict(status='info', count=0, coverage=0, examples='baseline just frozen; re-run to compare')
    elif not base_path.exists():
        f10 = dict(status='info', count=0, examples='baseline not frozen', diff={})
        f3 = dict(status='info', count=0, coverage=0, examples='fingerprint baseline not frozen')
    else:
        base = json.loads(base_path.read_text(encoding='utf-8'))
        base_map = base.get('units') if isinstance(base, dict) and 'units' in base else base
        base_fps = base.get('fps') if isinstance(base, dict) else None
        diff = {k: (base_map.get(k), cur_map.get(k)) for k in set(base_map) | set(cur_map)
                if base_map.get(k) != cur_map.get(k)}
        allowed = set()
        if args.expected_changes and Path(args.expected_changes).exists():
            allowed = set(json.loads(Path(args.expected_changes).read_text(encoding='utf-8')))
        unexpected = {k: v for k, v in diff.items() if k not in allowed}
        f10 = dict(status='fail' if unexpected else 'pass', count=len(diff), diff=diff,
                   examples=' | '.join(f'{k}:{v[0]}->{v[1]}' for k, v in list(diff.items())[:10]))
        if not base_fps:
            f3 = dict(status='info', count=0, coverage=0,
                      examples='基线无 fps（旧格式）；F-3 不得计入通过')
        else:
            keys = [k for k in base_fps if k in cur_fps and base_fps[k] and cur_fps[k]]
            mism = [(k, base_fps[k], cur_fps[k]) for k in keys if base_fps[k] != cur_fps[k]]
            gone = [k for k in base_fps if base_fps[k] and k not in cur_fps]
            if not keys and not gone:
                f3 = dict(status='info', count=0, coverage=0, roots=0, affected=0,
                          examples='coverage 0：空测，不计通过')
            else:
                # 按根因归并：同一 struct_unit 下的落点指纹变化/缺失只算一处根因，
                # 影响面另记 affected（一次编辑只报一条根因＋影响面计数；ADR §7.7）。
                groups = defaultdict(list)
                for k, a, b in mism:
                    groups[base_map.get(k) or cur_map.get(k) or k].append((k, a, b))
                for k in gone:
                    groups[base_map.get(k) or k].append((k, base_fps[k], None))
                affected = len(mism) + len(gone)
                roots = len(groups)
                f3 = dict(status='fail' if (mism or gone) else 'pass',
                          count=affected, coverage=len(keys), roots=roots, affected=affected,
                          examples=f'checked={len(keys)} mismatch={len(mism)} missing={len(gone)} '
                                   f'roots={roots} affected={affected} | ' +
                                   ' | '.join(f'{u}×{len(v)}' for u, v in
                                              sorted(groups.items(), key=lambda kv: -len(kv[1]))[:8]))
    assert_rows = assertions(rows, docs, reg, args.target_mode, rowkey_rows, unresolved_ids, f10, f3)
    targets_rows = [{k: r[k] for k in ('file', 'line', 'col', 'token', 'form', 'scope', 'sub_kind', 'sub_value',
                                       'target_file', 'target_kind', 'assign_basis', 'in_yaml_value',
                                       'in_comment', 'in_code_span')} for r in rows]
    resolv_rows = [{k: r[k] for k in ('file', 'line', 'col', 'token', 'scope', 'landing_form', 'landing_line',
                                      'clause', 'row_key', 'row_registered', 'resolvable_to', 'range')}
                   for r in rows]
    drift_rows = [{k: r[k] for k in ('file', 'line', 'col', 'token', 'scope', 'target_file', 'target_kind',
                                     'landing_line', 'drift', 'drift_delta')} for r in rows]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / 'targets.csv', targets_rows)
    write_csv(out / 'resolvability.csv', resolv_rows)
    write_csv(out / 'drift.csv', drift_rows)
    write_csv(out / 'assertions.csv', assert_rows)
    label_out = [{'file': r['file'], 'line': r['line'], 'col': r['col'], 'token': r['token'],
                  'label': r['token'].split('@')[0].strip(), 'label_class': r['label_class'],
                  'exempt_reason': 'code_span' if r['in_code_span'] else 'not_anchor'}
                 for r in label_rows]
    write_csv(out / 'label_refs.csv', label_out)
    if (out / 'label_refs.csv').stat().st_size == 0:
        (out / 'label_refs.csv').write_text(
            'file,line,col,token,label,label_class,exempt_reason\n', encoding='utf-8')

    # 行键映射（仅受影响条款：同条款内出现重名者）
    affected_keys = [r for r in rowkey_rows if (r['doc'], r['clause']) in affected]
    if affected_keys:
        write_csv(out / 'row_keys.csv', affected_keys)
    else:
        (out / 'row_keys.csv').write_text(
            'doc,clause,table_id,table_line,header,line,row_name,secondary,key,conflict\n',
            encoding='utf-8')

    # 索引：语义键 → 现行行 + 指纹
    index = {}
    for r in rows:
        if r['form'] not in ('legacy', 'prefix') or not r['target_file']:
            continue
        doc = docs.get(r['target_file'])
        if doc and doc.exists and 1 <= int(r['landing_line'] or 0) <= len(doc.lines):
            key = f"{r['target_kind']}:{r['clause']}#{r['landing_form']}"
            index.setdefault(key, []).append({
                'file': r['target_file'], 'line': r['landing_line'],
                'fp': fingerprint(doc.lines[int(r['landing_line']) - 1]),
            })
    (out / 'anchor_index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')

    # F-8 幂等：再扫一次比较哈希
    rows2, _label2 = split_labels(scan(docs, reg, row_ids, rowkey_map, terms))
    for r in rows2:
        r['scope'] = classify(r['file'])
    h1 = hashlib.sha256(json.dumps(targets_rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    h2 = hashlib.sha256(json.dumps([{k: r[k] for k in targets_rows[0]} for r in rows2], ensure_ascii=False,
                                   sort_keys=True).encode()).hexdigest()
    assert_rows.append(dict(id='F-8', desc='索引生成幂等（两次扫描输出一致）',
                            status='pass' if h1 == h2 else 'fail', count=0 if h1 == h2 else 1,
                            examples=f'hash={h1[:16]}'))

    mixed_live, frozen_only, frozen_occ = classify_mixed(rows)
    summary = {
        'target_mode': args.target_mode,
        'total_rows': len(rows),
        'f4_mixed_live_tokens': len(mixed_live),
        'frozen_only_mixed_tokens': len(frozen_only),
        'frozen_only_mixed_live_occurrences': frozen_occ,
        'row_keys_affected_total': len(affected_keys),
        'row_keys_unresolved_table_ids': len(unresolved_ids),
        'by_form': dict(Counter(r['form'] for r in rows)),
        'by_file': dict(Counter(r['file'] for r in rows)),
        'by_target_kind': dict(Counter(r['target_kind'] or 'none' for r in rows)),
        'by_assign_basis': dict(Counter(r['assign_basis'] for r in rows)),
        'by_landing_form': dict(Counter(r['landing_form'] or 'none' for r in rows)),
        'by_resolvable': dict(Counter(r['resolvable_to'] for r in rows)),
        'by_drift': dict(Counter(r['drift'] for r in rows)),
        'by_range_note': dict(Counter(r['range_note'] for r in rows if r['range'] == '1')),
        'default_basis_ambiguous': sum(1 for r in rows if r['assign_basis'] == 'default'
                                       and r['target_kind'] == 'mother'
                                       and r['landing_line'] <= doc_len(docs, r['file'])),
        'fenced_skipped': sum(1 for rel, d in docs.items() if d.exists
                              for i, ln in enumerate(d.lines, 1)
                              if i in d.fence_lines and '@' in ln),
        'yaml_value_anchors': sum(1 for r in rows if r['in_yaml_value']),
        'comment_anchors': sum(1 for r in rows if r['in_comment']),
        'code_span_anchors': sum(1 for r in rows if r['in_code_span']),
        'ranges': sum(1 for r in rows if r['range'] == '1'),
        'live_anchors': sum(1 for r in rows if r['scope'] == 'live' and r['form'] in ('legacy', 'prefix')),
        'frozen_anchors': sum(1 for r in rows if r['scope'] == 'frozen' and r['form'] in ('legacy', 'prefix')),
        'struct_anchors': sum(1 for r in rows if r['form'] == 'struct'),
        'by_scope': dict(Counter(r['scope'] for r in rows)),
        'label_refs_total': len(label_rows),
        'label_refs_by_class': dict(Counter(r['label_class'] for r in label_rows)),
        'label_refs_by_file': dict(Counter(r['file'] for r in label_rows)),
        'label_refs_code_span': sum(1 for r in label_rows if r['in_code_span']),
        'key_at_anchors': sum(1 for r in rows if r['form'] == 'key_at'),
        'key_at_by_class': dict(Counter(r['label_class'] for r in rows if r['form'] == 'key_at')),
        'migratable_total': sum(1 for r in rows if r['form'] == 'key_at'
                                and r['label_class'] in ('doc_ref', 'field_path', 'other')
                                and not r['in_code_span']),
        'migratable_by_class': dict(Counter(r['label_class'] for r in rows if r['form'] == 'key_at'
                                            and r['label_class'] in ('doc_ref', 'field_path', 'other')
                                            and not r['in_code_span'])),
        'key_at_exempt_frozen': sum(1 for r in rows if r['form'] == 'key_at' and r['file'] in FROZEN),
        'key_at_exempt_code_span': sum(1 for r in rows if r['form'] == 'key_at' and r['in_code_span']),
        'prefix_doc_total': sum(1 for r in rows if r['form'] == 'prefix_doc'),
        'prefix_field_total': sum(1 for r in rows if r['form'] == 'prefix_field'),
        'prefix_by_sub': dict(Counter(r['sub_kind'] or 'none' for r in rows
                                      if r['form'] in ('prefix_doc', 'prefix_field'))),
        'prefix_unresolved': sum(1 for r in rows if r['form'] in ('prefix_doc', 'prefix_field')
                                 and r['resolvable_to'] == 'none'),
        'key_path_ok': sum(1 for r in rows if r['sub_kind'] == 'key' and r['resolvable_to'] == 'key_path'),
        'sec_title_ok': sum(1 for r in rows if r['sub_kind'] == 'sec' and r['resolvable_to'] == 'sec_title'),
        'assertions': {a['id']: a['status'] for a in assert_rows},
        'f9_checked_pairs': next((a.get('coverage') for a in assert_rows if a['id'] == 'F-9'), None),
        'failures': [a for a in assert_rows if a['status'] == 'fail'],
    }
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')

    print(json.dumps(summary, ensure_ascii=False, indent=1))
    hard_fail = any(a['status'] == 'fail' for a in assert_rows)
    return 1 if hard_fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
