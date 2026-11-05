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
    'ADR草案-PRJ交付空间-谓词槽纠正.md',
    'ADR草案-GRD-PRJ-GOV-剖面变更.md',
    'R2提案-KP-G3-包络义务适用范围.md',
    'ADR草案-行内标记方案-五项gap.md',
    'ADR草案-G-OWN-CSL-行内出处.md',
    'ADR草案-G-STY-1-G-ENV-1-接地编译前置.md',
    'ADR草案-G-PRJ-1-悬空保留.md',
]
# 活跃集合（规范 F-1 的适用域）；不存在的文件自动跳过
LIVE = [
    'registry/method_registry.yaml', 'registry/profiles.yaml',
    'registry/predicate_vocabulary.yaml', 'registry/README.md',
    'registry/projections/STY.md', 'registry/projections/索引.md',
    'registry/projections/自检报告.md', 'registry/projections/勘察义务清单.md',
    '悬置未决事项-冻结快照-2026-11-04.md', '参考资料缺口核对报告.md',
]

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
# 规范 §2 新增两式（2026-11-05 裁定）：key- 点路径（下标必须保留）／sec- 逐字标题
SUB_KEY_RE = re.compile(r'#key-(?P<path>[A-Za-z0-9_.\[\]-]+)')
SUB_FN_RE = re.compile(r'#fn-(?P<name>[A-Za-z_][A-Za-z0-9_]*)')
PY_SUFFIXES = ('.py',)


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


def scan(docs: dict, reg, row_ids: set) -> dict:
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
            for m in LINE_RE.finditer(line):
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
                else:
                    # 邻接条款号（≤15 字）与落点条款不符 → 疑似漂移
                    pre = line[max(0, m.start() - 15):m.start()]
                    cm = re.search(r'(\d+(?:\.\d+){1,})(?![\d.])', pre)
                    if cm and clause and cm.group(1) != clause:
                        drift = 'suspect_clause_mismatch'
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


# ── 断言 F-1～F-8 ───────────────────────────────────────────────
def assertions(rows, docs, reg, mode, rowkeys, unresolved_ids) -> list[dict]:
    out = []
    live_rows = [r for r in rows if r['file'] in LIVE and r['form'] in ('legacy', 'prefix')]
    live_all = [r for r in rows if r['file'] in LIVE]
    frozen_rows = [r for r in rows if r['file'] in FROZEN and r['form'] in ('legacy', 'prefix')]
    if mode == 'prefix_id':
        bare = [r for r in live_all if r['form'] == 'key_at' or r['resolvable_to'] in ('line_only', 'none')]
        desc = 'F-1（prefix_id）：活跃锚点必须解析到条款/row_id/字段'
    elif mode == 'prefix':
        bare = [r for r in live_all if r['form'] in ('legacy', 'key_at')]
        desc = 'F-1（prefix）：活跃锚点必须带目标前缀'
    else:
        bare = [r for r in live_rows if r['form'] == 'legacy']
        desc = 'F-1（none，现状度量）：活跃文件内的裸行号数量'
    out.append(dict(id='F-1', desc=desc, status='fail' if bare else 'pass', count=len(bare),
                    examples=' | '.join(f"{r['file']}:{r['line']} {r['token']}" for r in bare[:10])))
    # F-2
    miss = [r for r in live_all if r['form'] in ('prefix_doc', 'prefix_field')
            and r['resolvable_to'] == 'none']
    if mode != 'none':
        miss += [r for r in live_all if r['form'] == 'key_at']
    miss += [r for r in live_all if r['form'] in ('legacy', 'prefix')
             and (r['resolvable_to'] == 'none' or int(r['landing_line'] or 0) < 1
                  or (r['target_kind'] in ('mother', 'registry', 'profiles', 'vocab', 'compile')
                      and int(r['landing_line'] or 0) > len(docs.get(r['target_file'], Doc(r['target_file'])).lines))
                  or (mode == 'prefix_id' and r['target_kind'] in ('mother', 'registry')
                      and r['resolvable_to'] not in ('clause_id', 'row_id')))]
    out.append(dict(id='F-2', desc='每条锚点可解析（文件/条款/子锚）',
                    status='fail' if miss else 'pass', count=len(miss),
                    examples=' | '.join(f"{r['file']}:{r['line']} {r['token']}->{r['target_file']}" for r in miss[:10])))
    # F-3 漂移：hard（超界/目标缺失/反向）+ soft（邻接条款号不一致，启发式）
    drift_hard = [r for r in live_rows if r['drift'] in ('out_of_range', 'target_missing')]
    drift_soft = [r for r in live_rows if r['drift'] == 'suspect_clause_mismatch']
    out.append(dict(id='F-3', desc='漂移例外归零（hard：超界/目标缺失）',
                    status='fail' if drift_hard else 'pass', count=len(drift_hard),
                    examples=' | '.join(f"{r['file']}:{r['line']} {r['token']} {r['drift']}({r['drift_delta']})" for r in drift_hard[:10]) +
                             f' || soft_suspect={len(drift_soft)}'))
    # F-4 跨目标类歧义串（忽略 unknown，unknown 归 F-2/F-3）
    # 口径按规范 §8：冻结文件只做快照复算，不计入 F-1～F-6 的失败计数。
    mixed, frozen_only, frozen_occ = classify_mixed(rows)
    out.append(dict(id='F-4', desc='同一锚点串不跨目标类',
                    status='fail' if mixed else 'pass', count=len(mixed),
                    examples=' | '.join(f'{k}:{"/".join(sorted(v))}' for k, v in list(mixed.items())[:10])))
    # INFO-1：仅因冻结文件才成 mixed 的串，info 级，不计入 F-4 分母、不计失败
    out.append(dict(id='INFO-1', desc='frozen_only_mixed（仅冻结侧致歧义；info，不计入 F-4 分母）',
                    status='info', count=len(frozen_only),
                    examples=f'live_occurrences={frozen_occ} | ' +
                             ' | '.join(f'{k}:{"/".join(sorted(v))}' for k, v in
                                        list(frozen_only.items())[:10])))
    # F-5 行键唯一性：表标识＋（必要时）次级键，同条款内必须唯一（规范 §3.1）
    dup_keys = Counter((r['doc'], r['clause'], r['key']) for r in rowkeys)
    dups = sum(v - 1 for v in dup_keys.values() if v > 1)
    out.append(dict(id='F-5', desc='行键式 row 子锚在同条款内唯一（表标识＋次级键）',
                    status='fail' if (dups or unresolved_ids) else 'pass',
                    count=dups + len(unresolved_ids),
                    examples=' | '.join(f'{c}/{k}×{v}' for (d_, c, k), v in dup_keys.items() if v > 1)[:300] +
                             (f' || unresolved_table_id={unresolved_ids}' if unresolved_ids else '')))
    # F-6 区间反向（短式已按首位补全；仍反向者记失败）
    bad = [f"{r['file']}:{r['line']} {r['token']}" for r in live_rows if r['range_note'] == 'reversed']
    raw_rev = len(bad)
    out.append(dict(id='F-6', desc='区间起止有序，无反向',
                    status='fail' if raw_rev else 'pass', count=raw_rev,
                    examples=' | '.join(bad[:10])))
    # F-7 台账计数守恒（内部一致性）
    entries = reg.get('entries') or []
    meta_n = (reg.get('meta') or {}).get('entry_count')
    seed_n = sum(1 for e in entries if e.get('status') == 'seed')
    ok7 = (len(entries) == meta_n) if meta_n is not None else False
    out.append(dict(id='F-7', desc='台账计数守恒（entries==meta.entry_count，seed 计数可解释）',
                    status='pass' if ok7 else 'fail', count=0 if ok7 else 1,
                    examples=f'entries={len(entries)} meta.entry_count={meta_n} seed={seed_n} '
                             f'gaps={len(reg.get("gaps") or [])} SO={len(reg.get("survey_obligations") or [])}'))
    return out


def fingerprint(line: str) -> str:
    return re.sub(r'\s+', ' ', line.strip())[:60]


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(REG / 'anchor_index'), help='输出目录（默认 registry/anchor_index）')
    ap.add_argument('--target-mode', choices=('none', 'prefix', 'prefix_id'), default='none',
                    help='none=现状; prefix=全部带目标前缀; prefix_id=前缀+ID+子锚')
    args = ap.parse_args(argv)

    rels = target_files()
    docs = {rel: Doc(rel) for rel in rels}          # 一次性快照，F-8 幂等基于同一快照
    for rel in ['软件工程元框架成文法.md', 'registry/method_registry.yaml', 'registry/profiles.yaml',
                'registry/predicate_vocabulary.yaml', '编译规范.md'] + LIVE + FROZEN:
        docs.setdefault(rel, Doc(rel))
    reg, row_ids = load_registry()

    rows, label_rows = split_labels(scan(docs, reg, row_ids))
    rowkey_rows, unresolved_ids, affected = derive_row_keys(docs)
    assert_rows = assertions(rows, docs, reg, args.target_mode, rowkey_rows, unresolved_ids)
    targets_rows = [{k: r[k] for k in ('file', 'line', 'col', 'token', 'form', 'sub_kind', 'sub_value',
                                       'target_file', 'target_kind', 'assign_basis', 'in_yaml_value',
                                       'in_comment', 'in_code_span')} for r in rows]
    resolv_rows = [{k: r[k] for k in ('file', 'line', 'col', 'token', 'landing_form', 'landing_line',
                                      'clause', 'row_key', 'row_registered', 'resolvable_to', 'range')}
                   for r in rows]
    drift_rows = [{k: r[k] for k in ('file', 'line', 'col', 'token', 'target_file', 'target_kind',
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
    rows2, _label2 = split_labels(scan(docs, reg, row_ids))
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
        'live_anchors': sum(1 for r in rows if r['file'] in LIVE and r['form'] in ('legacy', 'prefix')),
        'frozen_anchors': sum(1 for r in rows if r['file'] in FROZEN and r['form'] in ('legacy', 'prefix')),
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
        'failures': [a for a in assert_rows if a['status'] == 'fail'],
    }
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')

    print(json.dumps(summary, ensure_ascii=False, indent=1))
    hard_fail = any(a['status'] == 'fail' for a in assert_rows)
    return 1 if hard_fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
