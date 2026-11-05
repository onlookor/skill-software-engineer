#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project.py —— 方法注册表自检 + 同源投影（registry/scripts/）

性质：工具，不含规范命题（README §1）。所有判据的权威出处：
  · 条目 schema 与闭集值       母本 0.17.2（@322-381）
  · kind 封闭枚举              母本 0.17.3
  · M 系列检查式               母本 0.17.8；M10–M15 见 0.18.6
  · 检查矩阵与 seed 资格公式   registry/README.md §5
  · 字段剖面物化公式           registry/profiles.yaml 头注 2（required = common − optional − N/A + extra）
  · 谓词词汇封闭               registry/predicate_vocabulary.yaml（数据侧投影，非权威）
  · 事实占位符 / 勘察义务      README §3.3；母本 0.18.6 M15
  · Waiver 五要素              母本 9.2.2

用法（README §6）：
  cd registry
  python3 scripts/project.py --check      # 仅自检，写 projections/自检报告.md
  python3 scripts/project.py --project    # 自检 + 生成人类层投影（projections/）

退出码：0 = 无硬检查失败；1 = 存在硬检查失败（含指针反查失败）。
依赖：标准库 + pyyaml。生成物禁手改（README §1）。
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write('缺少 pyyaml：python3 -m pip install pyyaml\n')
    raise

# ═══════════════════════════════ 1. 路径与常量 ═══════════════════════════════

SCRIPT_DIR = Path(__file__).resolve().parent
REG_DIR = SCRIPT_DIR.parent
SE_DIR = REG_DIR.parent

LAW_PATH = SE_DIR / '软件工程元框架成文法.md'
COMPILE_PATH = SE_DIR / '编译规范.md'
REG_PATH = REG_DIR / 'method_registry.yaml'
PROFILES_PATH = REG_DIR / 'profiles.yaml'
VOCAB_PATH = REG_DIR / 'predicate_vocabulary.yaml'
PROJ_DIR = REG_DIR / 'projections'

# ── 0.17.2 闭集值（逐字采用；不重定义、不扩展、不裁剪）──
ENUM_STATUS = {'draft', 'seed', 'active', 'deprecated', 'retired'}
ENUM_REVERSIBILITY = {'free', 'bounded', 'costly', 'irreversible'}
ENUM_ORIGIN = {'manual', 'compiled', 'hybrid'}
ENUM_RELATION = {'hard_conflict', 'tension', 'composable', 'requires'}
ENUM_LEVEL = {'hard', 'soft', 'conditional'}
ENUM_SIGNAL = {'P0', 'P1', 'P2'}
ENUM_ROLE = {'implements', 'consumed_by', 'triggers'}
ENUM_COMPILE_USAGE = {'metadata_extraction', 'case_study', 'parameter_source', 'narrative_only'}
ENUM_AGG = {'itemwise', 'additive', 'grouped_max', 'weighted_avg'}
ENUM_SOURCE_TYPE = {'clause_id', 'bib_id', 'row_id'}
ANCHOR_SERIES = tuple('VWXYZQR TGEM'.replace(' ', ''))  # V/W/X/Y/Z/Q/R/T/G/E/M

# ── 0.17.2 字段集（README §2：条目内不得出现 0.17.2 之外的字段）──
ENTRY_FIELDS = {
    'entry_id', 'kind', 'name', 'version', 'status', 'provenance', 'typical_reversibility',
    'applicability', 'envelope', 'cost_profile', 'compatibility', 'constraints_imposed',
    'anti_patterns', 'formal_anchor', 'references', 'narrative',
}
APPLICABILITY_FIELDS = {'problem_space', 'current_space', 'delivery_space'}
SOURCE_REF_FIELDS = {'source_type', 'value', 'verified'}
PROVENANCE_FIELDS = {'origin', 'source_pointers'}
VERSION_FIELDS = {'major', 'minor', 'patch'}
ENVELOPE_ITEM_FIELDS = {'metric', 'bound_expr', 'source'}
COST_PROFILE_FIELDS = {
    'latency_budget_delta', 'failure_modes', 'consistency_impact', 'observability_requires',
    'ops_cost', 'skill_prerequisites', 'aggregation_semantics',
}
COMPAT_ITEM_FIELDS = {'peer_entry', 'relation', 'evidence'}
CONSTRAINT_ITEM_FIELDS = {'target_aspect', 'constraint', 'level'}
ANTI_PATTERN_ITEM_FIELDS = {'pattern_id', 'description', 'detection_predicate', 'signal_level'}
ANCHOR_ITEM_FIELDS = {'property_id', 'role'}
REFERENCE_ITEM_FIELDS = {'bib_id', 'support_claim', 'compile_usage', 'trust_grade'}
NARRATIVE_FIELDS = {'benefit_cost_analysis', 'typical_scenarios', 'common_misuse'}

# ── M3 参数化判据（关系算子字符集 + 词形表；MJ-2 转写规则的机器可判定面）──
REL_OPS = set('≤≥<>=↑↓→ΣΠ∈∧∨¬±×÷')
REL_WORDS = ('max', 'min', '单调', '上界', '下界', '不减', '不增')
# 0.17.7 门槛 2（无出处的具体数值 = 假精确）：带时间/比例单位的裸数值
CONCRETE_NUM_RE = re.compile(r'\d+(?:\.\d+)?\s*(?:ms|毫秒|秒|s\b|分钟|小时|%|％)')

# ── 四层数据源标签（0.17.6(1)；行内注释约定，见 method_registry.yaml 头注）──
LAYER_LABELS = ('骨架源', '交叉表源', '参考资料源', '人工判断')

# ── 子维度显示名（README §4 裁决表；条目归属由 row_id 前缀数据驱动推得）──
SUBDIM_NAME = {
    '1.2.1': '子维度一：抽象/代码结构风格',
    '1.2.2': '子维度二：部署/运行单元风格',
    '1.2.3': '子维度三：通信/协调风格',
    '1.2.4': '子维度四：风格选择元方法',
}

# 条目级检查（渲染逐条矩阵用）
ENTRY_CHECKS = ['C-ID', 'M2', 'M3', 'M4', 'M6', 'M9', 'C-ENV', 'C-ST']
# seed 资格公式（README §5）：M2 ∧ M3 ∧ M4 ∧ M6 ∧ M9 ∧ C-ENV ∧ C-ST（M5 软，记警告不阻断）
SEED_CHECKS = ['M2', 'M3', 'M4', 'M6', 'M9', 'C-ENV', 'C-ST', 'C-ID']


# ═══════════════════════════════ 2. 通用工具 ═══════════════════════════════

class Row:
    """一条检查结果。level ∈ hard|soft|info；ok ∈ True|False|None（None = 不适用/跳过）。"""

    __slots__ = ('check', 'scope', 'level', 'ok', 'reason')

    def __init__(self, check: str, scope: str, level: str, ok, reason: str = ''):
        self.check = check
        self.scope = scope
        self.level = level
        self.ok = ok
        self.reason = reason


class Report:
    def __init__(self):
        self.rows: list[Row] = []

    def add(self, check, scope, level, ok, reason=''):
        self.rows.append(Row(check, scope, level, ok, reason))

    def ok(self, check, scope, level='hard', reason=''):
        self.add(check, scope, level, True, reason)

    def fail(self, check, scope, reason, level='hard'):
        self.add(check, scope, level, False, reason)

    def skip(self, check, scope, reason, level='hard'):
        self.add(check, scope, level, None, reason)

    def of(self, check):
        return [r for r in self.rows if r.check == check]

    def failures(self, level='hard'):
        return [r for r in self.rows if r.level == level and r.ok is False]

    def status_of(self, entry_id: str, check: str) -> str:
        """逐条矩阵用：'✓' / '✗' / '–'（无记录 = 不适用）。多项取最差。"""
        marks = {'✓': 0, '–': 1, '✗': 2}
        best = None
        for r in self.rows:
            if r.check != check or r.scope.split(' ')[0] != entry_id:
                continue
            m = '✓' if r.ok is True else ('✗' if r.ok is False else '–')
            if best is None or marks[m] > marks[best]:
                best = m
        return best or '·'


def load_yaml(path: Path):
    with path.open(encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def read_text(path: Path) -> str:
    return path.open(encoding='utf-8').read()


def has_path(obj, dotted: str) -> bool:
    """点路径 presence 判定：键在案且值非 None（空列表 = 在案，空值语义由 C-ENV 等另行判定）。"""
    cur = obj
    for part in dotted.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return cur is not None


def get_path(obj, dotted: str, default=None):
    cur = obj
    for part in dotted.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def bracket_spans(s: str) -> list[str]:
    """深度计数括号匹配器：提取顶层 […] 片段（嵌套安全）。"""
    out, depth, start = [], 0, -1
    for i, ch in enumerate(s):
        if ch == '[':
            if depth == 0:
                start = i
            depth += 1
        elif ch == ']':
            if depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    out.append(s[start:i + 1])
    return out


TRUST_PREFIX_RE = re.compile(r'^\[(已核验|存疑|未核验|待核验)')


def outside_brackets(s: str) -> str:
    """剔除方括号内文本（占位符内容不参与谓词名提取）。"""
    depth, res = 0, []
    for ch in s:
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth = max(0, depth - 1)
        elif depth == 0:
            res.append(ch)
    return ''.join(res)


PRED_CALL_RE = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*\(')


def predicate_names(s: str) -> list[str]:
    return PRED_CALL_RE.findall(outside_brackets(s))


def walk_strings(obj, path: str, out: list):
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk_strings(v, f'{path}.{k}' if path else str(k), out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_strings(v, f'{path}[{i}]', out)
    elif isinstance(obj, str):
        out.append((path, obj))


def walk_pointers(obj, path: str, out: list):
    """递归收集机器可读源指针。兼容两种书写形态：
    (a) source_ref = {source_type, value, verified}；(b) references[] 的裸 bib_id。"""
    if isinstance(obj, dict):
        st, val = obj.get('source_type'), obj.get('value')
        if isinstance(st, str) and st in ENUM_SOURCE_TYPE and val is not None:
            out.append((st, val, path))
        elif 'bib_id' in obj and 'source_type' not in obj:
            out.append(('bib_id', obj['bib_id'], path + '.bib_id'))
        for k, v in obj.items():
            walk_pointers(v, f'{path}.{k}' if path else str(k), out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_pointers(v, f'{path}[{i}]', out)


def md_cell(s) -> str:
    return str(s).replace('|', '\\|').replace('\n', ' ').strip()


def scope_covers(scope: str, entry_id: str) -> bool:
    """profiles.yaml entry_level_exemptions.scope 覆盖判定。
    scope 形态如 "STY-020…STY-024（1.2.4 风格选择元方法）"：取全部 {KIND}-{三位} token，
    ≥2 个 → 区间覆盖；1 个 → 等值。"""
    toks = re.findall(r'([A-Z]{3})-(\d{3})', scope or '')
    if not toks:
        return False
    m = re.fullmatch(r'([A-Z]{3})-(\d{3})', entry_id)
    if not m:
        return False
    kind, num = m.group(1), int(m.group(2))
    same = [int(n) for k, n in toks if k == kind]
    if not same:
        return False
    return min(same) <= num <= max(same)


# ═══════════════════════════ 3. 权威源索引（防幻觉反查） ═══════════════════════════

LAW_HEAD_RE = re.compile(r'^#{2,6}\s+((?:\d+\.)+\d*|\d+)\s')
COMPILE_HEAD_RE = re.compile(r'^#{1,6}\s+((?:\d+\.)+\d*|\d+)[\s、.]')
ANY_HEAD_RE = re.compile(r'^(#{1,6})\s+(.*)$')
BIB_LINE_RE = re.compile(r'^(\d{1,3})\.\s')
KIND_ROW_RE = re.compile(r'^\|\s*([A-Z]{3})\s*\|')
PUBLISHED_REF_RE = re.compile(r'(?<![A-Za-z0-9\-])([A-Z]{3})-(\d{1,3})(?![0-9\-])')


class Index:
    """母本 / 编译规范的标题索引、书目索引、kind 枚举、已发布引用。"""

    def __init__(self, law_text: str, compile_text: str):
        self.law_text = law_text
        self.compile_text = compile_text
        self.law_lines = law_text.splitlines()
        self.compile_lines = compile_text.splitlines()
        self.law_headings = self._headings(self.law_lines, LAW_HEAD_RE)
        self.compile_headings = self._headings(self.compile_lines, COMPILE_HEAD_RE)
        self.bib, self.bib_dups, self.bib_sections = self._bib_index(self.law_lines)
        self.kinds = self._kind_enum(self.law_lines)
        self.published = self._published_refs(self.law_lines)

    @staticmethod
    def _headings(lines, regex) -> dict:
        idx = {}
        for i, ln in enumerate(lines, 1):
            m = regex.match(ln)
            if m:
                idx.setdefault(m.group(1).rstrip('.'), (i, ln.strip()))
        return idx

    @staticmethod
    def _bib_index(lines):
        """母本参考文献分节分布（每方面一节 + 总纲节）→ 聚合成全局书目索引。
        节定位：标题含「参考文献」且不含「治理条款」（0.12 是治理条款，非文献表）。
        节终止：遇到同级或更高级标题。行形态：^{1..3 位数字}. """
        secs = []
        for i, ln in enumerate(lines):
            m = ANY_HEAD_RE.match(ln)
            if m and '参考文献' in m.group(2) and '治理条款' not in m.group(2):
                secs.append((i, len(m.group(1)), m.group(2).strip()))
        idx, dups = {}, []
        for start, lvl, title in secs:
            j = start + 1
            while j < len(lines):
                m2 = ANY_HEAD_RE.match(lines[j])
                if m2 and len(m2.group(1)) <= lvl:
                    break
                m3 = BIB_LINE_RE.match(lines[j])
                if m3:
                    n = int(m3.group(1))
                    if n in idx:
                        dups.append(n)
                    else:
                        idx[n] = (j + 1, title, lines[j].strip())
                j += 1
        return idx, dups, secs

    @staticmethod
    def _kind_enum(lines) -> dict:
        """0.17.3 kind 封闭枚举表：^| {三位大写前缀} |

        节域限定（仅扫 0.17.3 标题至下一同级/更高级标题之间）：母本各方面表格首列
        同为三位大写缩写（ESB/SOA/BFF/ADR…），全域扫描会把架构风格名误采为 kind。"""
        out, start, lvl = {}, None, 0
        for i, ln in enumerate(lines):
            m = ANY_HEAD_RE.match(ln)
            if m:
                if start is not None and len(m.group(1)) <= lvl:
                    break
                if start is None and m.group(2).strip().startswith('0.17.3'):
                    start, lvl = i, len(m.group(1))
                continue
            if start is None:
                continue
            km = KIND_ROW_RE.match(ln)
            if km:
                out.setdefault(km.group(1), (i + 1, ln.strip()))
        return out

    @staticmethod
    def _published_refs(lines) -> dict:
        """母本正文已发布的 entry_id 形态引用（0.22 承诺一：编号永不复用/重排）。"""
        out = {}
        for i, ln in enumerate(lines, 1):
            for m in PUBLISHED_REF_RE.finditer(ln):
                key = f'{m.group(1)}-{int(m.group(2)):03d}'
                out.setdefault(key, []).append((i, ln.strip()))
        return out


def resolve_pointer(st: str, val, idx: Index):
    """指针反查。返回 (ok, 描述, 细节)。"""
    s = str(val).strip()
    if st == 'clause_id':
        if s.startswith('编译规范'):
            num = s.replace('编译规范', '').strip(' 、.')
            hit = idx.compile_headings.get(num)
            return (hit is not None, f'编译规范 {num}',
                    f'编译规范.md @{hit[0]}' if hit else '编译规范.md 无该标题')
        hit = idx.law_headings.get(s)
        return (hit is not None, s, f'母本 @{hit[0]}' if hit else '母本无该条款标题')
    if st == 'bib_id':
        try:
            n = int(s)
        except ValueError:
            return (False, f'书目 {s}', 'bib_id 非整数')
        hit = idx.bib.get(n)
        return (hit is not None, f'书目 {n}', f'母本 @{hit[0]}（{hit[1]}）' if hit else '母本参考文献表无该编号')
    if st == 'row_id':
        clause, _, row = s.partition('-')
        row = row.strip()
        ok_clause = clause in idx.law_headings
        ok_row = bool(row) and row in idx.law_text
        detail = []
        if not ok_clause:
            detail.append(f'母本无条款 {clause}')
        if not row:
            detail.append('缺行名（形态应为 "{表号}-{行名}"）')
        elif not ok_row:
            detail.append(f'母本正文查无行名「{row}」')
        return (ok_clause and ok_row, s, '；'.join(detail) or f'母本 @{idx.law_headings[clause][0]} 表内')
    return (False, f'{st}:{s}', '未知 source_type')


# ═══════════════════════════ 4. 剖面物化（C-KP / M2） ═══════════════════════════

def materialize_profile(common_required: dict, prof: dict) -> dict:
    """物化公式（profiles.yaml 头注 2）：
       required_fields = common_required − optional − not_applicable + required_extra"""
    base = []
    for grp_name, grp in common_required.items():
        for f in grp.get('fields') or []:
            if f not in base:
                base.append(f)
    opt = [o['field'] for o in (prof.get('optional') or [])]
    na = [o['field'] for o in (prof.get('not_applicable') or [])]
    extra = list(prof.get('required_extra') or [])
    required = [f for f in base if f not in opt and f not in na]
    for e in extra:
        if e not in required:
            required.append(e)
    return {
        'required': required,
        'optional': opt,
        'not_applicable': na,
        # C-KP 的「两列表」契约：optional_fields = 选填 ∪ 不适用（不适用单列以保留 0.17.6 第四层区分）
        'optional_fields': opt + [f for f in na if f not in opt],
        'undecided': list(prof.get('undecided_fields') or []),
        'exemptions': list(prof.get('entry_level_exemptions') or []),
        'base': base,
    }


# ═══════════════════════════════ 5. 检查器 ═══════════════════════════════

def check_pointers(rep: Report, idx: Index, docs: dict):
    """PTR：三文件全部机器可读源指针反查权威源（防幻觉）。"""
    total = miss = 0
    per_file = {}
    for name, doc in docs.items():
        ptrs = []
        walk_pointers(doc, '', ptrs)
        # profiles.yaml 的 seed_source.clause_id 为裸字符串形态（可含 "/" 复合）
        if name == 'profiles.yaml':
            for p in doc.get('profiles') or []:
                cid = (p.get('seed_source') or {}).get('clause_id')
                if isinstance(cid, str):
                    for part in cid.split('/'):
                        ptrs.append(('clause_id', part.strip(), f"{p.get('entry_id')}.seed_source.clause_id"))
        ok_n = 0
        misses = []
        for st, val, path in ptrs:
            total += 1
            good, desc, detail = resolve_pointer(st, val, idx)
            if good:
                ok_n += 1
            else:
                miss += 1
                misses.append(f'{path} → {st}:{val}（{detail}）')
        per_file[name] = (len(ptrs), ok_n, misses)
        for m in misses:
            rep.fail('PTR', name, m)
    if miss == 0:
        rep.ok('PTR', '三文件全部指针', 'hard',
               f'{total} 个源指针全部反查命中（母本标题 {len(idx.law_headings)} 个／'
               f'编译规范标题 {len(idx.compile_headings)} 个／书目 {len(idx.bib)} 条）')
    return per_file, total, miss


def check_bib_sanity(rep: Report, idx: Index):
    """书目索引自检：编号连续、无重复、分节可定位（信息性；失败即索引构建缺陷）。"""
    if idx.bib_dups:
        rep.fail('PTR', '书目索引', f'参考文献编号重复：{sorted(set(idx.bib_dups))}', level='hard')
    nums = sorted(idx.bib)
    gaps = [n for n in range(1, (nums[-1] + 1) if nums else 1) if n not in idx.bib]
    if gaps:
        rep.fail('PTR', '书目索引', f'参考文献编号不连续，缺：{gaps}', level='hard')
    if nums:
        rep.ok('PTR', '书目索引', 'hard',
               f'聚合 {len(idx.bib_sections)} 个参考文献节，编号 1..{nums[-1]} 连续无重复')


def check_kind_enum(rep: Report, idx: Index, profiles_doc: dict):
    """C-KP（元注册面）：17 kind 剖面齐备、id 形态、describes_kind ∈ 封闭枚举、物化两列表在案。"""
    profs = profiles_doc.get('profiles') or []
    kinds_in_law = set(idx.kinds)
    if not kinds_in_law:
        rep.fail('C-KP', 'profiles.yaml', '母本 0.17.3 kind 封闭枚举解析为空（索引构建失败）')
        return {}
    rep.ok('C-KP', '0.17.3 枚举', 'hard', f'kind 封闭枚举解析得 {len(kinds_in_law)} 个：{"、".join(sorted(kinds_in_law))}')

    mat = {}
    seen_ids, seen_kinds = set(), set()
    for p in profs:
        pid = p.get('entry_id')
        kind = p.get('describes_kind')
        if pid in seen_ids:
            rep.fail('C-KP', str(pid), '元条目 entry_id 重复')
        seen_ids.add(pid)
        if not re.fullmatch(r'kind_profile_[A-Z]{3}', str(pid)):
            rep.fail('C-KP', str(pid), 'id 形态应为 kind_profile_{KIND}（README §5 C-ID 元条目例外）')
        if kind not in kinds_in_law:
            rep.fail('C-KP', str(pid), f'describes_kind={kind} ∉ 0.17.3 封闭枚举')
        if kind in seen_kinds:
            rep.fail('C-KP', str(pid), f'kind {kind} 剖面重复登记')
        seen_kinds.add(kind)
        m = materialize_profile(profiles_doc.get('common_required') or {}, p)
        mat[kind] = m
        # C-KP 判据：物化后的 required_fields / optional_fields 两列表在案（避自指，KP-G2）
        if not m['required']:
            rep.fail('C-KP', str(pid), '物化后 required_fields 为空')
        if not isinstance(p.get('optional'), list) or not isinstance(p.get('not_applicable'), list):
            rep.fail('C-KP', str(pid), 'optional / not_applicable 须为列表（物化输入）')
        for item in (p.get('optional') or []) + (p.get('not_applicable') or []):
            if not item.get('reason') or not item.get('provenance'):
                rep.fail('C-KP', str(pid),
                         f"降级项 {item.get('field')} 缺 reason/provenance（0.17.6 第四层：禁默认值假充）")
        for ex in m['exemptions']:
            for k in ('scope', 'field', 'check', 'reason', 'provenance'):
                if not ex.get(k):
                    rep.fail('C-KP', str(pid), f'entry_level_exemptions 项缺 {k}')
        rep.ok('C-KP', str(pid), 'hard',
               f"required {len(m['required'])} 项／optional {len(m['optional'])} 项／"
               f"N-A {len(m['not_applicable'])} 项／status={p.get('status')}")
    missing = kinds_in_law - seen_kinds
    if missing:
        rep.fail('C-KP', 'profiles.yaml', f'0.17.3 枚举中无剖面的 kind：{sorted(missing)}')
    extra = seen_kinds - kinds_in_law
    if extra:
        rep.fail('C-KP', 'profiles.yaml', f'剖面存在但 ∉ 0.17.3 枚举：{sorted(extra)}')
    if not missing and not extra:
        rep.ok('C-KP', '剖面覆盖', 'hard', f'{len(seen_kinds)} 个 kind 剖面与 0.17.3 枚举一一对应')
    return mat


def _source_ref_ok(sr, rep: Report, where: str) -> bool:
    ok = True
    if not isinstance(sr, dict):
        rep.fail('M2', where, f'源指针应为 source_ref 对象，实为 {type(sr).__name__}（README §2）')
        return False
    extra = set(sr) - SOURCE_REF_FIELDS
    if extra:
        rep.fail('M2', where, f'source_ref 含 0.17.2 之外字段：{sorted(extra)}（README §2）')
        ok = False
    if sr.get('source_type') not in ENUM_SOURCE_TYPE:
        rep.fail('M2', where, f"source_type={sr.get('source_type')} ∉ {sorted(ENUM_SOURCE_TYPE)}（0.17.2）")
        ok = False
    if sr.get('value') in (None, ''):
        rep.fail('M2', where, 'source_ref.value 缺失')
        ok = False
    if not isinstance(sr.get('verified'), bool):
        rep.fail('M2', where, f"verified 应为布尔（README §2 键名映射「核验状态」→ verified），实为 {sr.get('verified')!r}")
        ok = False
    return ok


def check_schema(rep: Report, e: dict, eid: str):
    """M2 的 schema 面：字段集封闭 + 闭集值 + 结构形态（0.17.2 逐字采用，README §2）。"""
    where = f'{eid} schema'
    extra = set(e) - ENTRY_FIELDS
    if extra:
        rep.fail('M2', where, f'条目含 0.17.2 之外字段：{sorted(extra)}（README §2 禁令）')
    if e.get('status') not in ENUM_STATUS:
        rep.fail('M2', where, f"status={e.get('status')!r} ∉ 0.17.5 枚举 {sorted(ENUM_STATUS)}")
    if e.get('typical_reversibility') not in ENUM_REVERSIBILITY:
        rep.fail('M2', where, f"typical_reversibility={e.get('typical_reversibility')!r} ∉ {sorted(ENUM_REVERSIBILITY)}")
    v = e.get('version')
    if not isinstance(v, dict) or set(v) != VERSION_FIELDS:
        rep.fail('M2', where, f'version 应为 {{major, minor, patch}}（README §2），实为 {v!r}')
    prov = e.get('provenance')
    if not isinstance(prov, dict):
        rep.fail('M2', where, f'provenance 应为对象，实为 {type(prov).__name__}')
    else:
        if set(prov) - PROVENANCE_FIELDS:
            rep.fail('M2', where, f'provenance 含 0.17.2 之外字段：{sorted(set(prov) - PROVENANCE_FIELDS)}')
        if prov.get('origin') not in ENUM_ORIGIN:
            rep.fail('M2', where, f"provenance.origin={prov.get('origin')!r} ∉ {sorted(ENUM_ORIGIN)}（0.17.6 四层）")
        sps = prov.get('source_pointers')
        if not isinstance(sps, list) or not sps:
            rep.fail('M2', where, 'provenance.source_pointers 应为非空列表（0.4 出处门槛）')
        else:
            for i, sr in enumerate(sps):
                _source_ref_ok(sr, rep, f'{where}.source_pointers[{i}]')

    app = e.get('applicability')
    if isinstance(app, dict):
        if set(app) - APPLICABILITY_FIELDS:
            rep.fail('M2', where, f'applicability 含 0.17.2 之外字段：{sorted(set(app) - APPLICABILITY_FIELDS)}')
        for k, v2 in app.items():
            if not isinstance(v2, list):
                rep.fail('M2', where, f'applicability.{k} 应为谓词列表，实为 {type(v2).__name__}')
    for i, it in enumerate(e.get('envelope') or []):
        w = f'{where}.envelope[{i}]'
        if not isinstance(it, dict):
            rep.fail('M2', w, 'envelope 项应为对象')
            continue
        if set(it) - ENVELOPE_ITEM_FIELDS:
            rep.fail('M2', w, f'含 0.17.2 之外字段：{sorted(set(it) - ENVELOPE_ITEM_FIELDS)}')
        for k in ENVELOPE_ITEM_FIELDS - {'source'}:
            if not str(it.get(k) or '').strip():
                rep.fail('M2', w, f'{k} 缺失')
        if 'source' in it:
            _source_ref_ok(it['source'], rep, w + '.source')
    cp = e.get('cost_profile')
    if isinstance(cp, dict):
        if set(cp) - COST_PROFILE_FIELDS:
            rep.fail('M2', where, f'cost_profile 含 0.17.2 之外字段：{sorted(set(cp) - COST_PROFILE_FIELDS)}')
        agg = cp.get('aggregation_semantics')
        if agg not in ENUM_AGG:
            rep.fail('M2', where, f'aggregation_semantics={agg!r} ∉ {sorted(ENUM_AGG)}（0.17.2）')
        if agg == 'weighted_avg':
            rep.fail('M2', where, 'aggregation_semantics=weighted_avg 须附权重出处（0.17.2）；本批未登记权重源')
        for k in ('failure_modes', 'observability_requires', 'skill_prerequisites'):
            if k in cp and not isinstance(cp[k], list):
                rep.fail('M2', where, f'cost_profile.{k} 应为列表（0.17.2），实为 {type(cp[k]).__name__}')
    for i, it in enumerate(e.get('compatibility') or []):
        w = f'{where}.compatibility[{i}]'
        if not isinstance(it, dict):
            rep.fail('M2', w, 'compatibility 项应为对象')
            continue
        if set(it) - COMPAT_ITEM_FIELDS:
            rep.fail('M2', w, f'含 0.17.2 之外字段：{sorted(set(it) - COMPAT_ITEM_FIELDS)}')
        if it.get('relation') not in ENUM_RELATION:
            rep.fail('M2', w, f"relation={it.get('relation')!r} ∉ {sorted(ENUM_RELATION)}")
        if not it.get('peer_entry'):
            rep.fail('M2', w, 'peer_entry 缺失')
        if not it.get('evidence'):
            rep.fail('M2', w, 'evidence 缺失（0.4：关系须带出处或显式人工判断）')
        elif isinstance(it['evidence'], dict):
            _source_ref_ok(it['evidence'], rep, w + '.evidence')
    for i, it in enumerate(e.get('constraints_imposed') or []):
        w = f'{where}.constraints_imposed[{i}]'
        if not isinstance(it, dict):
            rep.fail('M2', w, '项应为对象')
            continue
        if set(it) - CONSTRAINT_ITEM_FIELDS:
            rep.fail('M2', w, f'含 0.17.2 之外字段：{sorted(set(it) - CONSTRAINT_ITEM_FIELDS)}')
        if it.get('level') not in ENUM_LEVEL:
            rep.fail('M2', w, f"level={it.get('level')!r} ∉ {sorted(ENUM_LEVEL)}")
        if not isinstance(it.get('target_aspect'), int):
            rep.fail('M2', w, f"target_aspect 应为方面序号整数，实为 {it.get('target_aspect')!r}")
    for i, it in enumerate(e.get('anti_patterns') or []):
        w = f'{where}.anti_patterns[{i}]'
        if not isinstance(it, dict):
            rep.fail('M2', w, '项应为对象')
            continue
        if set(it) - ANTI_PATTERN_ITEM_FIELDS:
            rep.fail('M2', w, f'含 0.17.2 之外字段：{sorted(set(it) - ANTI_PATTERN_ITEM_FIELDS)}')
        if it.get('signal_level') not in ENUM_SIGNAL:
            rep.fail('M2', w, f"signal_level={it.get('signal_level')!r} ∉ {sorted(ENUM_SIGNAL)}（0.14）")
        if str(it.get('pattern_id') or '') != f"{eid}-AP{i + 1}":
            rep.fail('M2', w, f"pattern_id={it.get('pattern_id')!r} 与条目序不符（应为 {eid}-AP{i + 1}）")
    for i, it in enumerate(e.get('formal_anchor') or []):
        w = f'{where}.formal_anchor[{i}]'
        if not isinstance(it, dict):
            rep.fail('M2', w, '项应为对象')
            continue
        if set(it) - ANCHOR_ITEM_FIELDS:
            rep.fail('M2', w, f'含 0.17.2 之外字段：{sorted(set(it) - ANCHOR_ITEM_FIELDS)}')
        pid = str(it.get('property_id') or '')
        if not re.fullmatch(rf'[{"".join(ANCHOR_SERIES)}]\d{{1,2}}', pid):
            rep.fail('M2', w, f'property_id={pid!r} 不属 V/W/X/Y/Z/Q/R/T/G/E/M 系列（0.17.2）')
        if it.get('role') not in ENUM_ROLE:
            rep.fail('M2', w, f"role={it.get('role')!r} ∉ {sorted(ENUM_ROLE)}")
    for i, it in enumerate(e.get('references') or []):
        w = f'{where}.references[{i}]'
        if not isinstance(it, dict):
            rep.fail('M2', w, '项应为对象')
            continue
        if set(it) - REFERENCE_ITEM_FIELDS:
            rep.fail('M2', w, f'含 0.17.2 之外字段：{sorted(set(it) - REFERENCE_ITEM_FIELDS)}')
    nar = e.get('narrative')
    if isinstance(nar, dict) and set(nar) - NARRATIVE_FIELDS:
        rep.fail('M2', where, f'narrative 含 0.17.2 之外字段：{sorted(set(nar) - NARRATIVE_FIELDS)}')


def check_m2(rep: Report, e: dict, eid: str, mat: dict, prof_status: dict):
    """M2 = ∀E(status ≠ draft): fields_complete(E, kind_profile(E.kind))（0.17.8）。"""
    check_schema(rep, e, eid)
    kind = e.get('kind')
    if e.get('status') == 'draft':
        rep.skip('M2', eid, 'status=draft，M2 量词 ∀E(status≠draft) 不适用（仍执行 schema 面校验）')
        return
    m = mat.get(kind)
    if not m:
        rep.fail('M2', eid, f'kind={kind} 无物化剖面 → 完备性不可判定')
        return
    missing = [f for f in m['required'] if not has_path(e, f)]
    if missing:
        rep.fail('M2', eid, f"按 kind_profile_{kind} 剖面缺必填字段：{missing}")
    else:
        rep.ok('M2', eid, 'hard',
               f"剖面 required {len(m['required'])} 项全部在案（optional {len(m['optional'])}／N-A {len(m['not_applicable'])}）")
    if prof_status.get(kind) == 'draft':
        rep.skip('M2', eid, f'kind_profile_{kind} 为 draft（KP-G3 适用性无据）→ 必填面含 undecided_fields，判定不完整')


def check_m3(rep: Report, e: dict, eid: str, idx: Index):
    """M3 = ∀ item ∈ E.envelope: parameterized(bound_expr) ∧ sourced(item.source)（0.17.8）。"""
    env = e.get('envelope')
    if env is None:
        rep.skip('M3', eid, 'envelope 字段缺失（由 M2 记失败）')
        return
    if not env:
        rep.skip('M3', eid, 'envelope: []（空集上 ∀ 平凡为真；非空义务由 C-ENV 判定）')
        return
    bad = []
    for i, it in enumerate(env):
        expr = str(it.get('bound_expr') or '')
        if not (any(ch in REL_OPS for ch in expr) or any(w in expr for w in REL_WORDS)):
            bad.append(f'[{i}] bound_expr 未参数化（无关系算子/界词形）：{_trunc(expr, 48)}')
        m = CONCRETE_NUM_RE.search(expr)
        if m:
            bad.append(f'[{i}] bound_expr 含无出处具体数值 {m.group(0)!r}（0.17.7 门槛 2 假精确）')
        sr = it.get('source')
        if not isinstance(sr, dict):
            bad.append(f'[{i}] source 非 source_ref')
        else:
            good, desc, detail = resolve_pointer(sr.get('source_type'), sr.get('value'), idx)
            if not good:
                bad.append(f'[{i}] source 未过 0.4 出处门槛：{desc}（{detail}）')
    if bad:
        rep.fail('M3', eid, '；'.join(bad))
    else:
        rep.ok('M3', eid, 'hard', f'{len(env)} 项 bound_expr 全部参数化且 source 反查命中')


def check_m4(rep: Report, e: dict, eid: str, vocab: set):
    """M4 = ∀ p ∈ E.anti_patterns: executable(p.detection_predicate)（0.17.8）；
    可执行性的数据侧判据 = 词汇封闭（README §3.1 / 编译规范 2.3 谓词名注册）。
    同时校验 applicability 三空间谓词（README §3.1）。"""
    unknown = []
    scanned = 0
    for i, it in enumerate(e.get('anti_patterns') or []):
        dp = str(it.get('detection_predicate') or '')
        if not dp.strip():
            rep.fail('M4', eid, f'anti_patterns[{i}].detection_predicate 为空（0.17.2 精化 4：必须带检测谓词）')
            continue
        scanned += 1
        for name in predicate_names(dp):
            if name not in vocab:
                unknown.append(f'AP{i + 1}: {name}')
    for sp in ('problem_space', 'current_space', 'delivery_space'):
        for j, cond in enumerate((e.get('applicability') or {}).get(sp) or []):
            scanned += 1
            for name in predicate_names(str(cond)):
                if name not in vocab:
                    unknown.append(f'applicability.{sp}[{j}]: {name}')
    if unknown:
        rep.fail('M4', eid, '未登记谓词（本地造词，禁）：' + '、'.join(sorted(set(unknown)))
                        + ' → 走 R2 提议并登记 vocabulary_gaps')
    else:
        rep.ok('M4', eid, 'hard', f'{scanned} 处谓词表达式全部落在登记词汇内（词汇量 {len(vocab)}）')


def check_m5(rep: Report, e: dict, eid: str):
    """M5 = narrative_sync（软，P2 抽查）：决策性叙事须已形式化或带 clue 标记（0.17.8）。
    数据侧抽查判据：narrative 中的规范措辞句，须在机器层有承载者
    （constraints_imposed / anti_patterns / formal_anchor 之一非空）或句内带 clue: 标记。"""
    nar = e.get('narrative') or {}
    missing_fields = [f for f in sorted(NARRATIVE_FIELDS) if not str(nar.get(f) or '').strip()]
    if missing_fields:
        rep.fail('M5', eid, f'narrative 缺 {missing_fields}（0.17.2 人类解释层三字段）', level='soft')
    carriers = bool(e.get('constraints_imposed')) or bool(e.get('anti_patterns')) or bool(e.get('formal_anchor'))
    warns = []
    for f in sorted(NARRATIVE_FIELDS):
        text = str(nar.get(f) or '')
        for sent in re.split(r'[；。]', text):
            if any(k in sent for k in ('必须', '不得', '禁止', '只能', '应当')):
                if 'clue:' in sent or carriers:
                    continue
                warns.append(f'{f}: {_trunc(sent.strip(), 40)}')
    if warns:
        rep.add('M5', eid, 'soft', False, '决策性叙事无机器层承载者且无 clue 标记：' + '；'.join(warns[:4]))
    else:
        rep.ok('M5', eid, 'soft', 'narrative 三字段在案；规范措辞句均有机器层承载者或 clue 标记')


def check_m6(rep: Report, e: dict, eid: str):
    """M6 = ∀ reference ∈ E: declared(compile_usage) ∧ graded(trust)
             ∧ (grade = 存疑 → ¬sole_source(envelope ∨ detection))（0.17.8）。"""
    refs = e.get('references')
    if refs is None:
        rep.skip('M6', eid, 'references 字段缺失（由 M2 记失败）')
        return
    bad = []
    doubt = set()
    for i, r in enumerate(refs):
        if r.get('compile_usage') not in ENUM_COMPILE_USAGE:
            bad.append(f'[{i}] compile_usage={r.get("compile_usage")!r} ∉ 0.17.2 枚举')
        tg = str(r.get('trust_grade') or '').strip()
        if not tg:
            bad.append(f'[{i}] trust_grade 缺失（0.12 分级）')
        elif not TRUST_PREFIX_RE.match(tg):
            bad.append(f'[{i}] trust_grade={tg!r} 非 0.12 分级标注形态（[…已核验/存疑/未核验/待核验]）')
        if '存疑' in tg:
            try:
                doubt.add(int(r.get('bib_id')))
            except (TypeError, ValueError):
                pass
        if not str(r.get('support_claim') or '').strip():
            bad.append(f'[{i}] support_claim 缺失（0.17.7 门槛 6：文献须载明所支撑主张）')
    if doubt:
        env = e.get('envelope') or []
        if env and all(isinstance(it.get('source'), dict)
                       and it['source'].get('source_type') == 'bib_id'
                       and _as_int(it['source'].get('value')) in doubt for it in env):
            bad.append(f'envelope 的唯一出处为存疑级书目 {sorted(doubt)}（M6 后件违例）')
        sps = (e.get('provenance') or {}).get('source_pointers') or []
        if sps and all(sp.get('source_type') == 'bib_id' and _as_int(sp.get('value')) in doubt for sp in sps):
            bad.append(f'detection 面唯一出处为存疑级书目 {sorted(doubt)}（M6 后件违例）')
    if bad:
        rep.fail('M6', eid, '；'.join(bad))
    elif not refs:
        rep.ok('M6', eid, 'hard', 'references: []（空集上 ∀ 平凡为真；文献缺口已登记 gaps，禁以不承载主张的文献充当出处）')
    else:
        rep.ok('M6', eid, 'hard', f'{len(refs)} 条 reference 均声明 compile_usage + trust_grade；存疑级 {len(doubt)} 条未构成唯一出处')


def _as_int(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def check_m9(rep: Report, e: dict, eid: str, all_ids: set):
    """M9 = ∀ c ∈ E.compatibility: registered(c.peer_entry)（0.17.8）——peer 须存在于本注册表。"""
    comp = e.get('compatibility')
    if comp is None:
        rep.skip('M9', eid, 'compatibility 字段缺失（由 M2 记失败）')
        return
    missing = [c.get('peer_entry') for c in comp if c.get('peer_entry') not in all_ids]
    if missing:
        rep.fail('M9', eid, f'peer_entry 不存在于注册表：{missing}（未建批次 → 登记 pending_conflict_rows，不得写入 compatibility）')
    else:
        rep.ok('M9', eid, 'hard',
               f'{len(comp)} 条 compatibility 的 peer_entry 全部在案' + ('（[]：镜像登记/互斥不枚举，见 MJ-5/MJ-9）' if not comp else ''))


def check_cenv(rep: Report, e: dict, eid: str, mat: dict):
    """C-ENV（0.8：每种方法条目必须声明包络）：源行属 1.2.1/1.2.2/1.2.3 的条目 envelope 非空；
    子维度四元方法条目按剖面 entry_level_exemptions 豁免。"""
    m = mat.get(e.get('kind')) or {}
    row_clauses = set()
    for sp in (e.get('provenance') or {}).get('source_pointers') or []:
        if sp.get('source_type') == 'row_id':
            row_clauses.add(str(sp.get('value')).partition('-')[0])
    exempt = [ex for ex in m.get('exemptions', [])
              if ex.get('field') == 'envelope' and ex.get('check') == 'C-ENV' and scope_covers(ex.get('scope', ''), eid)]
    if exempt:
        rep.skip('C-ENV', eid, f"剖面豁免（scope「{exempt[0].get('scope')}」）：{_trunc(exempt[0].get('reason', ''), 60)}")
        return
    env = e.get('envelope') or []
    if row_clauses & {'1.2.1', '1.2.2', '1.2.3'}:
        if env:
            rep.ok('C-ENV', eid, 'hard', f'源行 {sorted(row_clauses)}，envelope {len(env)} 项非空（0.8）')
        else:
            rep.fail('C-ENV', eid, f'源行属 {sorted(row_clauses & {"1.2.1", "1.2.2", "1.2.3"})} 但 envelope 为空（0.8 包络声明义务）')
    elif env:
        rep.ok('C-ENV', eid, 'hard', f'envelope {len(env)} 项非空（源行 {sorted(row_clauses) or "无 row_id"}）')
    else:
        rep.skip('C-ENV', eid, f'源行不属 1.2.1/1.2.2/1.2.3（实为 {sorted(row_clauses) or "无 row_id"}）且无豁免登记 → 需剖面明示')
        rep.fail('C-ENV', eid, 'envelope 为空但无 entry_level_exemptions 覆盖（豁免须显式登记，禁默认放行）')


def check_cid(rep: Report, entries: list, idx: Index):
    """C-ID：entry_id 唯一、格式 {kind前缀}-{三位序号}、kind ∈ 0.17.3 封闭枚举、
    与母本既有已发布引用无冲突（0.22 承诺一）。"""
    seen = {}
    for e in entries:
        eid = str(e.get('entry_id'))
        kind = e.get('kind')
        if eid in seen:
            rep.fail('C-ID', eid, f'entry_id 重复（另见 {seen[eid]}）')
        seen[eid] = kind
        if not re.fullmatch(r'[A-Z]{3}-\d{3}', eid):
            rep.fail('C-ID', eid, '格式应为 {kind前缀}-{三位序号}（0.17.2 / README §5 C-ID）')
        if kind not in idx.kinds:
            rep.fail('C-ID', eid, f'kind={kind} ∉ 0.17.3 封闭枚举')
        if eid.split('-')[0] != kind:
            rep.fail('C-ID', eid, f'entry_id 前缀 {eid.split("-")[0]} 与 kind={kind} 不一致')
    if len(seen) == len(entries):
        rep.ok('C-ID', '全体条目', 'hard', f'{len(entries)} 个 entry_id 唯一、格式合规、kind 全部落在 0.17.3 枚举内')

    # 母本已发布引用比对（编号永不复用/重排）
    covered = {k for k in {e.get('kind') for e in entries}}
    unresolved_covered, pending = [], []
    for ref, ctxs in sorted(idx.published.items()):
        rk = ref.split('-')[0]
        if ref in seen:
            rep.add('C-ID', ref, 'info', True,
                    f'母本已发布引用 → 命中本注册表条目「{next(e["name"] for e in entries if e["entry_id"] == ref)}」；'
                    f'母本出处 {[c[0] for c in ctxs]}（书写形态等价关系见 README §4 / MJ-1）')
        elif rk in covered:
            unresolved_covered.append((ref, [c[0] for c in ctxs]))
        else:
            pending.append((ref, [c[0] for c in ctxs]))
    if unresolved_covered:
        for ref, lns in unresolved_covered:
            rep.fail('C-ID', ref, f'母本已发布引用（@{lns}）所属 kind 已在本批覆盖，但注册表无该 entry_id → 编号断裂（0.22 承诺一）')
    else:
        rep.ok('C-ID', '已发布引用', 'hard',
               f'母本已发布引用 {len(idx.published)} 个；本批覆盖 kind 的引用全部命中，无编号断裂')
    if pending:
        rep.add('C-ID', '待后续批次', 'info', None,
                '母本已发布引用属未建批次（须先解既有引用，README §4）：'
                + '、'.join(f'{r}(@{",".join(map(str, l))})' for r, l in pending))
    return seen


def check_meta(rep: Report, reg_doc: dict, entries: list, idx: Index, mat: dict, prof_status: dict):
    """META：meta 一致性（entry_count、kind 覆盖宣称）+ 与 0.17.3 枚举的对齐。"""
    meta = reg_doc.get('meta') or {}
    n = meta.get('entry_count')
    if n != len(entries):
        rep.fail('META', 'meta.entry_count', f'声明 {n}，实为 {len(entries)}')
    else:
        rep.ok('META', 'meta.entry_count', 'hard', f'{n} = 实际条目数')
    counts = {}
    for e in entries:
        counts[e.get('kind')] = counts.get(e.get('kind'), 0) + 1
    cov = str(meta.get('kind_coverage') or '')
    for k in counts:
        if k not in cov:
            rep.fail('META', 'meta.kind_coverage', f'宣称未提及已入库 kind={k}')
    rep.add('META', '按 kind 计数', 'info', True, '、'.join(f'{k}={v}' for k, v in sorted(counts.items())))

    # 覆盖宣称的机器可判定面：seed_source.table_rows 的逐表行数 vs 实际 row_id 分布
    for p in (load_yaml(PROFILES_PATH).get('profiles') or []):
        if p.get('describes_kind') not in counts:
            continue
        rows_decl = str((p.get('seed_source') or {}).get('table_rows') or '')
        decl = {t: int(n2) for t, n2 in re.findall(r'(\d+\.\d+\.\d+)（(\d+)\s*行）', rows_decl)}
        if not decl:
            rep.add('META', p['entry_id'], 'info', None, f'table_rows 未给逐表行数（{_trunc(rows_decl, 40)}）→ 覆盖宣称不可机器判定')
            continue
        actual = {}
        rownames = {}
        for e in entries:
            if e.get('kind') != p.get('describes_kind'):
                continue
            for sp in (e.get('provenance') or {}).get('source_pointers') or []:
                if sp.get('source_type') == 'row_id':
                    clause, _, rn = str(sp.get('value')).partition('-')
                    actual[clause] = actual.get(clause, 0) + 1
                    rownames.setdefault(clause, set()).add(rn)
        dup_rows = {c: len(v) for c, v in rownames.items() if len(v) != actual.get(c)}
        bad = [f'{c}：宣称 {decl[c]} 行，实得 {actual.get(c, 0)} 条' for c in decl if decl[c] != actual.get(c, 0)]
        extra_tbl = sorted(set(actual) - set(decl))
        if extra_tbl:
            bad.append(f'条目引用了宣称外的表：{extra_tbl}')
        if bad:
            rep.fail('META', p['entry_id'], '；'.join(bad))
        else:
            rep.ok('META', p['entry_id'], 'hard',
                   f"覆盖宣称核验通过：{'、'.join(f'{c} {decl[c]} 行' for c in sorted(decl))}，"
                   f'逐行一一对应（去重后行名数 = 条目数）')

    # 剖面 draft 的 kind 不得有 seed 条目（C-ST 附加面，此处先记录事实）
    for k, st in prof_status.items():
        if st == 'draft' and counts.get(k):
            rep.fail('META', f'kind={k}', f'剖面为 draft（KP-G3）但已有 {counts[k]} 条条目入库')


def check_cst(rep: Report, entries: list, mat: dict, prof_status: dict):
    """C-ST：声明状态与自检资格一致。
       (i) status=seed → 该条 SEED_CHECKS 全部硬检查通过；
       (ii) 任一硬检查未过 → 必须为 draft；
       (iii) 所属 kind 剖面为 draft → 不得声明 seed（KP-G3）。"""
    for e in entries:
        eid = str(e.get('entry_id'))
        st = e.get('status')
        kind = e.get('kind')
        failed = []
        for c in SEED_CHECKS:
            if c == 'C-ST':
                continue
            if rep.status_of(eid, c) == '✗':
                failed.append(c)
        if st == 'seed':
            if failed:
                rep.fail('C-ST', eid, f'声明 seed 但硬检查未过：{failed} → 按 C-ST 回落 status: draft')
            elif prof_status.get(kind) == 'draft':
                rep.fail('C-ST', eid, f'kind_profile_{kind} 为 draft（适用性无据，KP-G3）→ 该条目不得声明 seed')
            else:
                rep.ok('C-ST', eid, 'hard', f'seed 资格成立（{"∧".join(SEED_CHECKS)} 全过；剖面 status={prof_status.get(kind)}）')
        elif st == 'draft':
            rep.skip('C-ST', eid, 'status=draft（bootstrap 前状态；不受 seed 资格约束）'
                                  + (f'；未过检查：{failed}' if failed else ''))
        else:
            if failed:
                rep.fail('C-ST', eid, f'声明 {st} 但硬检查未过：{failed}')
            else:
                rep.add('C-ST', eid, 'info', True,
                        f'status={st}（active/deprecated/retired 的资格判据见 0.17.5，非本工具静态自检面）')


def check_ledgers(rep: Report, reg_doc: dict, vocab_doc: dict, profiles_doc: dict):
    """台账完整性（信息性）：gaps / status_transitions / waivers / manual_judgments /
    pending_conflict_rows / survey_obligations 的要素齐备。"""
    GAP_KEYS = ('gap_id', 'type', 'statement', 'impact', 'route', 'status')
    for g in reg_doc.get('gaps') or []:
        miss = [k for k in GAP_KEYS if not g.get(k)]
        if miss:
            rep.fail('LEDGER', str(g.get('gap_id')), f'缺口台账缺要素 {miss}', level='info')
    n_gaps = len(reg_doc.get('gaps') or [])

    MJ_KEYS = ('id', 'subject', 'judgment', 'basis', 'affected', 'provenance')
    for m in reg_doc.get('manual_judgments') or []:
        miss = [k for k in MJ_KEYS if not m.get(k)]
        if miss:
            rep.fail('LEDGER', str(m.get('id')), f'人工判断登记缺要素 {miss}', level='info')
    n_mj = len(reg_doc.get('manual_judgments') or [])

    # 9.2.2 Waiver 五要素 + 批准状态
    WV_KEYS = ('waiver_id', 'rule', 'violation_fact', 'scope', 'deadline', 'remediation_plan', 'risk_quantification')
    for w in reg_doc.get('waivers') or []:
        miss = [k for k in WV_KEYS if not w.get(k)]
        if miss:
            rep.fail('LEDGER', str(w.get('waiver_id')), f'Waiver 缺 9.2.2 要素 {miss}', level='hard')
        ap = w.get('approval') or {}
        if not ap.get('category') or ap.get('status') not in {'pending', 'approved', 'rejected'}:
            rep.fail('LEDGER', str(w.get('waiver_id')), 'Waiver 缺批准类目/状态（登记即申请，Agent 不自行批准）', level='hard')
        elif ap.get('status') == 'pending':
            rep.add('LEDGER', str(w.get('waiver_id')), 'info', None,
                    'Waiver 五要素齐备，批准状态 pending（待人工裁决；0.10 第一条 / 1.1 纪律二）')
    n_wv = len(reg_doc.get('waivers') or [])

    ST_KEYS = ('transition_id', 'from', 'to', 'scope', 'date', 'condition', 'evidence', 'impact_level', 'provenance')
    for s in reg_doc.get('status_transitions') or []:
        miss = [k for k in ST_KEYS if not s.get(k)]
        if miss:
            rep.fail('LEDGER', str(s.get('transition_id')), f'状态迁移简记缺要素 {miss}', level='hard')
        else:
            # 简记 scope 与实际条目状态一致性
            declared = set(s.get('scope') or [])
            actual = {str(e['entry_id']) for e in (reg_doc.get('entries') or [])
                      if e.get('status') == s.get('to')}
            if declared - actual:
                rep.fail('LEDGER', str(s.get('transition_id')),
                         f'简记声明迁移至 {s.get("to")} 的条目实际状态不符：{sorted(declared - actual)}', level='hard')
            elif actual - declared:
                rep.fail('LEDGER', str(s.get('transition_id')),
                         f'实际为 {s.get("to")} 但未在简记 scope 内：{sorted(actual - declared)}', level='hard')
            else:
                rep.ok('LEDGER', str(s.get('transition_id')), 'hard',
                       f'简记 scope {len(declared)} 条与实际 status={s.get("to")} 条目集一致')
    n_st = len(reg_doc.get('status_transitions') or [])

    SO_KEYS = ('obligation_id', 'kind', 'obligation', 'gap_ref', 'consumer', 'trigger_rule', 'status')
    for s in reg_doc.get('survey_obligations') or []:
        miss = [k for k in SO_KEYS if not s.get(k)]
        if miss:
            rep.fail('LEDGER', str(s.get('obligation_id')), f'勘察义务缺要素 {miss}', level='info')
    n_so = len(reg_doc.get('survey_obligations') or [])

    pcr = reg_doc.get('pending_conflict_rows') or {}
    n_pcr = len(pcr.get('open_rows') or [])
    for r in pcr.get('open_rows') or []:
        miss = [k for k in ('row_id', 'matrix_row', 'peer_status', 'disposition', 'source') if not r.get(k)]
        if miss:
            rep.fail('LEDGER', str(r.get('row_id')), f'未闭合冲突行缺要素 {miss}', level='info')
    n_closed = len(pcr.get('closed_in_entries') or [])

    vg = len(vocab_doc.get('vocabulary_gaps') or [])
    for g in vocab_doc.get('vocabulary_gaps') or []:
        miss = [k for k in ('id', 'missing_need', 'workaround', 'route') if not g.get(k)]
        if miss:
            rep.fail('LEDGER', str(g.get('id')), f'词汇缺口缺要素 {miss}', level='info')
    kpg = len(profiles_doc.get('gaps') or [])
    for g in profiles_doc.get('gaps') or []:
        miss = [k for k in ('gap_id', 'type', 'statement', 'impact', 'route', 'status') if not g.get(k)]
        if miss:
            rep.fail('LEDGER', str(g.get('gap_id')), f'剖面缺口缺要素 {miss}', level='info')

    if not rep.failures('hard') or True:
        rep.add('LEDGER', '台账全景', 'info', True,
                f'gaps {n_gaps}｜status_transitions {n_st}｜waivers {n_wv}｜manual_judgments {n_mj}｜'
                f'pending_conflict_rows 开放 {n_pcr}/已闭合 {n_closed}｜survey_obligations {n_so}｜'
                f'vocabulary_gaps {vg}｜profiles.gaps {kpg}')


# 有意悬空的 open gap：白名单附理由，不按异常计。G-PRJ-1 由 ADR-PRJ-2-01 §5.2 指定保留为
# 「曾把类型错误误判为数据缺口」的历史记录，不补 SO、不关闭；关闭须新 ADR 授权。
GAP_SO_WHITELIST = {
    'G-PRJ-1': 'ADR-PRJ-2-01 §5.2 指定历史留痕：G-PRJ-1 原文保留、不补 SO、不关闭。',
}


def check_gap_so_integrity(rep, reg_doc):
    """信息级：gap↔SO 双向引用完整性（不参与 seed 资格，不作硬失败）。"""
    gaps = {g['gap_id']: g for g in (reg_doc.get('gaps') or [])}
    sos = reg_doc.get('survey_obligations') or []
    open_gaps = {gid for gid, g in gaps.items() if g.get('status') == 'open'}
    refs, covered = {}, {}
    bad_ref, non_gap = [], 0
    for s in sos:
        oid = s['obligation_id']
        toks = [x.strip() for x in re.split(r'[,，;；]', str(s.get('gap_ref') or '')) if x.strip()]
        # gap_ref 允许混写词汇缺口／README 等交叉引用；仅对 G-<KIND>-<n> 形态校验 gap 存在性。
        gap_toks = [t for t in toks if re.fullmatch(r'G-[A-Z]+-[0-9]+', t)]
        non_gap += len(toks) - len(gap_toks)
        refs[oid] = gap_toks
        for t in gap_toks:
            if t not in gaps:
                bad_ref.append((oid, t))
                continue
            if s.get('status') == 'open' and gaps[t].get('status') == 'closed':
                rep.fail('GAP-SO', oid, f'open SO 指向已 closed gap {t}', level='info')
            if s.get('status') == 'open':
                covered.setdefault(t, []).append(oid)
    for t in sorted({t for _, t in bad_ref}):
        ids = [oid for oid, x in bad_ref if x == t]
        rep.fail('GAP-SO', ','.join(ids), f'gap_ref 指向不存在的 gap {t}', level='info')
    dangling = []
    for gid in sorted(open_gaps):
        if covered.get(gid):
            continue
        if gid in GAP_SO_WHITELIST:
            rep.add('GAP-SO', gid, 'info', True, '有意悬空：' + GAP_SO_WHITELIST[gid])
        else:
            dangling.append(gid)
            rep.fail('GAP-SO', gid, 'open gap 无 open SO 承接', level='info')
    rep.add('GAP-SO', '引用完整性', 'info', not dangling and not bad_ref,
            f'open gaps {len(open_gaps)}｜有 open SO 承接 {len(open_gaps) - len(dangling)}｜'
            f'白名单悬空 {len([g for g in open_gaps if g in GAP_SO_WHITELIST])}｜'
            f'无承接 {len(dangling)}｜SO {len(sos)}｜坏引用 {len(bad_ref)}｜非 gap 交叉引用 {non_gap}')


# ═══════════════════════════ 6. 普查与词汇装配 ═══════════════════════════

# 显式事实标记：以 `待勘察：` 开头（书写约定），或整句以 `待勘察` 结尾（值位未定，如
# DPS-004 bound_expr「到期时刻具体值待勘察」）。中间提及（如叙事里的「待勘察事实」）不计。
FACT_PLACEHOLDER_RE = re.compile(r'^待勘察(?:[：:]|\s|$)|待勘察$')
PLACEHOLDER_FIELD_ORDER = [
    'applicability.problem_space',
    'applicability.current_space',
    'applicability.delivery_space',
    'anti_patterns.detection_predicate',
    'cost_profile',
    'envelope.bound_expr',
    'narrative',
    'other',
]


def placeholder_field(path: str) -> str:
    """把字段路径归入可审计的槽类别（README §3.3 新口径）。"""
    if path.startswith('applicability.'):
        return 'applicability.' + path.split('.')[1].split('[')[0]
    if 'detection_predicate' in path:
        return 'anti_patterns.detection_predicate'
    if path.startswith('cost_profile'):
        return 'cost_profile'
    if path.startswith('envelope') and 'bound_expr' in path:
        return 'envelope.bound_expr'
    if path.startswith('narrative'):
        return 'narrative'
    return 'other'


def census_placeholders(entries: list) -> dict:
    """方括号内容分账（README §3.3 新口径 / 母本 0.18.6 M15）。

    判定式（显式、可审计）：
      · 排除 0.12 可信度标注（[已核验]/[存疑]/[未核验]/[待核验]）——单独由
        census_trust_marks 统计，既不进事实也不进槽；
      · 方括号内容带显式事实标记 → 事实占位（真·待勘察，M15 义务）：
        以 `待勘察：` 开头，或整句以 `待勘察` 结尾（见 FACT_PLACEHOLDER_RE）；
      · 其余 → 未绑定槽（谓词／参数槽，决策期求值，不计事实债）。

    不重复计数：每处方括号只归一类，事实数＋槽数 ≡ 原方括号总数。
    返回：
      {all, facts, slots}  # entry_id → [(字段路径, 文本)]
      total / fact_total / slot_total
      by_field  # 字段类别 → {fact, slot}
      by_kind   # kind → {字段类别: 槽数}
      kind_facts  # kind → 事实数
    """
    all_out, facts, slots = {}, {}, {}
    by_field = {g: {'fact': 0, 'slot': 0} for g in PLACEHOLDER_FIELD_ORDER}
    by_kind: dict = {}
    kind_facts: dict = {}
    total = fact_total = slot_total = 0
    for e in entries:
        eid = str(e.get('entry_id'))
        kind = str(e.get('kind'))
        strs = []
        walk_strings(e, '', strs)
        items = []
        for path, s in strs:
            for span in bracket_spans(s):
                if TRUST_PREFIX_RE.match(span):
                    continue
                items.append((path, span[1:-1].strip()))
        # 同一字段路径内多处方括号（如 detection_predicate 的合取支）加 #n 序号消歧
        seen: dict = {}
        for path, _ in items:
            seen[path] = seen.get(path, 0) + 1
        dup = {p for p, n in seen.items() if n > 1}
        cnt: dict = {}
        numbered = []
        for path, txt in items:
            if path in dup:
                cnt[path] = cnt.get(path, 0) + 1
                path = f'{path}#{cnt[path]}'
            numbered.append((path, txt))
        if not numbered:
            continue
        all_out[eid] = numbered
        for path, txt in numbered:
            group = placeholder_field(path)
            is_fact = bool(FACT_PLACEHOLDER_RE.search(txt))
            total += 1
            if is_fact:
                fact_total += 1
                facts.setdefault(eid, []).append((path, txt))
                by_field[group]['fact'] += 1
                kind_facts[kind] = kind_facts.get(kind, 0) + 1
            else:
                slot_total += 1
                slots.setdefault(eid, []).append((path, txt))
                by_field[group]['slot'] += 1
                by_kind.setdefault(kind, {})
                by_kind[kind][group] = by_kind[kind].get(group, 0) + 1
    return {
        'all': all_out, 'facts': facts, 'slots': slots,
        'total': total, 'fact_total': fact_total, 'slot_total': slot_total,
        'by_field': by_field, 'by_kind': by_kind, 'kind_facts': kind_facts,
    }


def census_trust_marks(entries: list) -> dict:
    """0.12 可信度标注普查（与事实占位符分列：前者是出处分级，后者是待勘察事实）。"""
    out = {}
    for e in entries:
        strs = []
        walk_strings(e, '', strs)
        marks = []
        for path, s in strs:
            for span in bracket_spans(s):
                m = TRUST_PREFIX_RE.match(span)
                if m:
                    marks.append((path, m.group(1)))
        if marks:
            out[str(e.get('entry_id'))] = marks
    return out


def build_vocab(rep: Report, vocab_doc: dict) -> set:
    """装配 M4 封闭词汇 = predicates ∪ formula_words ∪ clause_defined_predicates。
    数据面校验：每项须有 name 与 source（指针的反查由 PTR 统一执行）。"""
    vocab: set[str] = set()
    for grp in ('predicates', 'formula_words', 'clause_defined_predicates'):
        items = vocab_doc.get(grp)
        if not isinstance(items, list) or not items:
            rep.fail('VCB', grp, f'{grp} 缺失或非列表 → M4 词汇封闭的数据源不完整')
            continue
        names = []
        for i, it in enumerate(items):
            if not isinstance(it, dict) or not it.get('name'):
                rep.fail('VCB', f'{grp}[{i}]', '缺 name')
                continue
            names.append(str(it['name']))
            if not isinstance(it.get('source'), dict):
                rep.fail('VCB', f'{grp}[{i}]',
                         f"谓词 {it['name']} 缺 source（本文件非权威，每项须带母本指针）")
        dups = sorted({n for n in names if names.count(n) > 1})
        if dups:
            rep.fail('VCB', grp, f'组内重名：{dups}')
        vocab |= set(names)
        rep.ok('VCB', grp, 'hard', f'{len(names)} 项装配入封闭词汇（累计 {len(vocab)}）')
    vg = vocab_doc.get('vocabulary_gaps') or []
    rep.add('VCB', '词汇缺口', 'info', True,
            f'{len(vg)} 项待 R2 提议：{"、".join(str(g.get("id")) for g in vg)}'
            '（缺口词不得进入封闭词汇，README §3.1）')
    return vocab


# ── 四层数据源标签的行内注释提取（0.17.6(1)）──
ENTRY_START_RE = re.compile(r'^\s*-\s+entry_id:\s*(\S+)')
FIELD_RE = re.compile(r'^ {4}([a-z_]+):')


def extract_layers(text: str) -> dict:
    """从 method_registry.yaml **原文**的行内注释提取四层数据源标签。
    标签写在注释里而非机器字段（README §2：条目内不得出现 0.17.2 之外的字段），
    故本函数是宽松投影层：返回 {entry_id: {顶层字段: [标签…]}}，只用于投影展示，
    不参与任何硬检查判定。"""
    out: dict[str, dict] = {}
    cur, field = None, None
    for ln in text.splitlines():
        m = ENTRY_START_RE.match(ln)
        if m:
            cur = m.group(1).strip('"\'')
            out.setdefault(cur, {})
            field = None
        if cur is None:
            continue
        m2 = FIELD_RE.match(ln)
        if m2:
            field = m2.group(1)
        if '#' not in ln:
            continue
        comment = ln.split('#', 1)[1]
        hits = [lab for lab in LAYER_LABELS if lab in comment]
        if not hits:
            continue
        bucket = out[cur].setdefault(field or '(块头)', [])
        for h in hits:
            if h not in bucket:
                bucket.append(h)
    return out


def entry_subdim(e: dict) -> str:
    """条目所属子维度 = provenance.source_pointers 中首个 row_id 的表号前缀。"""
    for sp in (e.get('provenance') or {}).get('source_pointers') or []:
        if sp.get('source_type') == 'row_id':
            return str(sp.get('value')).partition('-')[0]
    return '?'


def entry_row_names(e: dict) -> list[str]:
    return [str(sp.get('value')) for sp in (e.get('provenance') or {}).get('source_pointers') or []
            if sp.get('source_type') == 'row_id']


def seed_summary(rep: Report, entries: list, prof_status: dict) -> dict:
    """逐条 seed 资格判定（README §5 公式），供报告与索引共用。
    返回 {eid: {'status','failed','verdict','detail'}}。"""
    out = {}
    for e in entries:
        eid = str(e.get('entry_id'))
        st = e.get('status')
        failed = [c for c in SEED_CHECKS if c != 'C-ST' and rep.status_of(eid, c) == '✗']
        prof = prof_status.get(e.get('kind'))
        if st == 'seed' and not failed and prof != 'draft':
            verdict, detail = '成立', f'{"∧".join(SEED_CHECKS)} 全过；剖面 status={prof}'
        elif st == 'seed' and failed:
            verdict, detail = '不成立', f'硬检查未过 {failed} → 按 C-ST 回落 status: draft'
        elif st == 'seed' and prof == 'draft':
            verdict, detail = '不成立', f'kind_profile_{e.get("kind")} 为 draft（KP-G3）→ 不得声明 seed'
        elif st == 'draft':
            verdict, detail = '未声明', 'status=draft' + (f'；未过检查：{failed}' if failed else '')
        else:
            verdict, detail = f'非 seed（{st}）', '资格判据见 0.17.5，非本工具静态自检面'
        out[eid] = {'status': st, 'failed': failed, 'verdict': verdict, 'detail': detail}
    return out


# ═══════════════════════ 7. 渲染（机器层 → 人类层同源投影，0.9/E2） ═══════════════════════

GEN_NOTE = ('> 本文件由 `scripts/project.py` 自动生成（机器层→人类层同源投影，母本 0.9／编译规范 E2），**禁止手改**；'
            '修改 registry/ 任一源后重跑 `python3 scripts/project.py --project`。')

SUBDIM_ORDER = ('1.2.3', '1.2.1', '1.2.2', '1.2.4')  # README §4 分块序裁决（MJ-1）


def src_hashes() -> dict:
    """三个 YAML 源的 sha256 前 12 位（投影脚注 = 手改检测面）。"""
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()[:12]
            for p in (REG_PATH, PROFILES_PATH, VOCAB_PATH)}


def write_text(name: str, text: str) -> Path:
    PROJ_DIR.mkdir(parents=True, exist_ok=True)
    path = PROJ_DIR / name
    hs = '；'.join(f'`{k}`→`{v}`' for k, v in src_hashes().items())
    footer = (f'\n---\n生成于 {datetime.datetime.now().isoformat(timespec="seconds")}｜'
              f'源哈希（sha256 前 12 位）：{hs}\n')
    path.write_text(text.rstrip('\n') + '\n' + footer, encoding='utf-8')
    return path


_ANCHOR_HEAD_RE = re.compile(r'@(?=[0-9mrpvcd!])')


def _cut(text, limit: int) -> tuple:
    """按 limit 截断；切点若落在 @ 锚点 token 内，延到该 token 末尾（不得切断锚点）。"""
    s = str(text or '')
    if len(s) <= limit:
        return s, False
    cut = limit
    for m in _ANCHOR_HEAD_RE.finditer(s):
        end = m.start() + 1
        while end < len(s) and (s[end].isalnum() or s[end] in ':._-#~'):
            end += 1
        if m.start() < cut < end:
            cut = end
    return s[:cut], True


def _trunc(text, limit: int) -> str:
    out, more = _cut(text, limit)
    return out + ('…' if more else '')


def _first_sentence(text, limit: int = 90) -> str:
    s = re.split(r'[。；]', str(text or '').replace('\n', ' ').strip(), maxsplit=1)[0]
    return _trunc(s, limit)


def _clip(text, limit: int = 70) -> str:
    """空白归一后按长度截断（不切句：保留方括号/成对符号的完整性）。"""
    s = ' '.join(str(text or '').split())
    return _trunc(s, limit)


def _flat(v, limit: int = 100) -> str:
    """str 直接截句；非 str（dict/list）按 YAML 流式展平后截句。"""
    s = v if isinstance(v, str) else yaml.safe_dump(v, allow_unicode=True, default_flow_style=True).strip()
    return _first_sentence(s.replace('\n', ' '), limit)


def _kind_census(entries: list) -> list:
    """按入库序（kind 首次出现序）统计 [(kind, count)]。数据全部来自 entries 本身。"""
    order, cnt = [], {}
    for e in entries:
        k = e.get('kind')
        if k not in cnt:
            order.append(k)
        cnt[k] = cnt.get(k, 0) + 1
    return [(k, cnt[k]) for k in order]


def render_survey(ctx: dict) -> str:
    """勘察义务清单.md：Part A 决策期事实占位逐条枚举 + 槽汇总 + Part B 入库期 SO 台账。"""
    reg_doc, ph, tm = ctx['reg_doc'], ctx['placeholders'], ctx['trust_marks']
    facts, slots = ph['facts'], ph['slots']
    n_total, n_fact, n_slot = ph['total'], ph['fact_total'], ph['slot_total']
    ttot = sum(len(v) for v in tm.values())
    doubt = sum(1 for v in tm.values() for _, g in v if g == '存疑')
    L = ['# 勘察义务清单', '', GEN_NOTE, '',
         '双通道义务（README §3.3；母本 0.18.6 M15、0.12、0.20.2 FM-1）：', '',
         '- **决策期**（Part A）：每个事实占位符在选型时逐条求值 真/假/未知，记录入 selection_log；'
         '未知 → 候选保留 ∧ 登记勘察任务（M15），**禁沉默排除**；无出处阈值禁填（0.17.7 门槛 2）。',
         '- **入库期**（Part B）：台账 survey_obligations（SO）是义务本身的登记面。', '',
         '## Part A｜决策期：事实占位逐条枚举（新口径）', '',
         f'- 方括号总数 **{n_total}** ＝ 事实占位 **{n_fact}** ＋ 未绑定槽 **{n_slot}**。',
         '- 判定式：方括号内容以 `待勘察：` 开头，或整句以 `待勘察` 结尾（值位未定）→ 事实占位；'
         '其余 → 谓词／参数槽（决策期求值，**不计事实债**）；0.12 可信度标注单列（见下节）。',
         f'- 本表只列事实占位；槽的字段分布见「未绑定槽汇总」，逐条核对见自检报告「占位符口径」。', '']
    if not facts:
        L += ['（本批无事实占位符）', '']
    for eid in sorted(facts):
        rows = facts[eid]
        L += [f'### {eid}（{len(rows)} 处）', '',
              '| # | 字段路径 | 事实占位（待决策期求值） |', '|---|---|---|']
        for i, (path, txt) in enumerate(rows, 1):
            L.append(f'| {i} | `{path}` | {md_cell(txt)} |')
        L.append('')
    L += ['### 未绑定槽汇总（不计事实债）', '',
          '| 字段类别 | 槽数 |', '|---|---|']
    for group in PLACEHOLDER_FIELD_ORDER:
        n = ph['by_field'][group]['slot']
        if n:
            L.append(f'| `{group}` | {n} |')
    L += [f'| **合计** | **{n_slot}** |', '',
          f'**合计：事实占位 {n_fact} 处（{len(facts)} 个条目）／未绑定槽 {n_slot} 处；'
          f'原方括号总数 {n_total}**。汇总义务见台账 SO-6（Part B）。', '',
          '### 可信度标注盘点（0.12）', '']
    if not tm:
        L += ['（无可信度标注）', '']
    for eid in sorted(tm):
        rows = tm[eid]
        L.append(f'- **{eid}**（{len(rows)} 处）：' + '；'.join(f'`{p}` → [{g}]' for p, g in rows))
    L += ['', f'合计 {ttot} 处标注（存疑 {doubt} 处）。M6 硬面：「存疑」级不得为唯一出处。', '',
          '## Part B｜入库期：勘察义务台账（SO）', '',
          '| obligation_id | kind | 义务（首句） | gap_ref | consumer | trigger_rule | status |',
          '|---|---|---|---|---|---|---|']
    for so in reg_doc.get('survey_obligations') or []:
        L.append('| {oid} | {k} | {ob} | {gr} | {cs} | {tr} | {st} |'.format(
            oid=so.get('obligation_id'), k=md_cell(_flat(so.get('kind'), 30)),
            ob=md_cell(_first_sentence(so.get('obligation'), 110)),
            gr=md_cell(_flat(so.get('gap_ref'), 50)), cs=md_cell(_flat(so.get('consumer'), 50)),
            tr=md_cell(_flat(so.get('trigger_rule'), 40)), st=so.get('status')))
    L.append('')
    return '\n'.join(L)


def render_self_check(ctx: dict) -> str:
    """自检报告.md：汇总条带 + PTR 分文件 + 逐条矩阵 + 硬失败/软警告明细 + 台账核对附录。"""
    rep, entries, seeds, reg_doc = ctx['rep'], ctx['entries'], ctx['seeds'], ctx['reg_doc']
    hard_f, soft_f = rep.failures('hard'), rep.failures('soft')
    n_hard_ok = len([r for r in rep.rows if r.level == 'hard' and r.ok is True])
    ph = ctx['placeholders']
    n_total, n_fact, n_slot = ph['total'], ph['fact_total'], ph['slot_total']
    verdicts: dict = {}
    for s in seeds.values():
        verdicts[s['verdict']] = verdicts.get(s['verdict'], 0) + 1
    wvs = reg_doc.get('waivers') or []
    e3w = [w for w in wvs if 'E3' in str(w.get('rule'))]
    e3txt = ('E3 面见台账 waivers：'
             + '、'.join(f'{w.get("waiver_id")}（{w.get("status")}）' for w in e3w)
             + '——各项独立生效、互不援引，scope 与闭合条件以台账原文为准'
             ) if e3w else 'E3 面台账 waivers 节暂无登记项'
    L = ['# 自检报告（注册表静态自检）', '', GEN_NOTE, '',
         '判据出处：README §5 检查矩阵；条款权威见 project.py 头注。'
         f'本报告是**静态自检**，不是 FVR 运行器（{e3txt}）。', '',
         '## 汇总', '',
         f'- 硬检查：通过 **{n_hard_ok}** 项／失败 **{len(hard_f)}** 项；软警告 {len(soft_f)} 项',
         f'- 条目：{len(entries)} 条；占位符（新口径）：事实占位 **{n_fact}** 处／'
         f'未绑定槽 **{n_slot}** 处（原方括号总数 {n_total}；旧口径亦为 1480，'
         f'见 README §4.16／§4.17，不回改）',
         '- seed 资格：' + ('、'.join(f'{k} {v} 条' for k, v in sorted(verdicts.items())) or '（无）'),
         f'- 指针反查：{ctx["ptr_total"]} 个，miss {ctx["ptr_miss"]} 个', '']
    L += ['### 指针反查（PTR）分文件', '', '| 文件 | 指针数 | 命中 | miss |', '|---|---|---|---|']
    for name, (n, okn, misses) in ctx['per_file'].items():
        L.append(f'| {name} | {n} | {okn} | {len(misses)} |')
    L += ['', '## 占位符口径（新，README §3.3）', '',
          '判定式：方括号 `[...]` 表示谓词／参数槽（决策期求值）；仅内容以 `待勘察：` 开头、'
          '或整句以 `待勘察` 结尾者（值位未定）为**事实占位**；0.12 可信度标注单列，不计入任一类。'
          '**事实占位＋未绑定槽 ≡ 原方括号总数**。', '',
          f'- 原方括号总数：**{n_total}**',
          f'- 事实占位（真·待勘察，M15 义务）：**{n_fact}**',
          f'- 未绑定槽（谓词／参数，不计事实债）：**{n_slot}**', '',
          '### 按字段分解', '',
          '| 字段类别 | 事实 | 槽 | 合计 |', '|---|---|---|---|']
    for group in PLACEHOLDER_FIELD_ORDER:
        cell = ph['by_field'][group]
        if cell['fact'] or cell['slot']:
            L.append(f'| `{group}` | {cell["fact"]} | {cell["slot"]} | {cell["fact"] + cell["slot"]} |')
    L += [f'| **合计** | **{n_fact}** | **{n_slot}** | **{n_total}** |', '',
          '### 按 kind 分解', '',
          '| kind | 事实 | problem | current | delivery | detection | cost | bound | narrative | 槽合计 | 合计 |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    kinds = set(ph['by_kind']) | set(ph['kind_facts'])
    for k in sorted(kinds, key=lambda x: (-(ph['kind_facts'].get(x, 0)
                                            + sum(ph['by_kind'].get(x, {}).values())), x)):
        groups = ph['by_kind'].get(k, {})
        cells = [groups.get(g, 0) for g in (
            'applicability.problem_space', 'applicability.current_space',
            'applicability.delivery_space', 'anti_patterns.detection_predicate',
            'cost_profile', 'envelope.bound_expr', 'narrative')]
        nf = ph['kind_facts'].get(k, 0)
        ns = sum(groups.values())
        L.append(f'| {k} | {nf} | ' + ' | '.join(map(str, cells)) + f' | {ns} | {nf + ns} |')
    L += [f'| **合计** | **{n_fact}** | **{ph["by_field"]["applicability.problem_space"]["slot"]}** | '
          f'**{ph["by_field"]["applicability.current_space"]["slot"]}** | '
          f'**{ph["by_field"]["applicability.delivery_space"]["slot"]}** | '
          f'**{ph["by_field"]["anti_patterns.detection_predicate"]["slot"]}** | '
          f'**{ph["by_field"]["cost_profile"]["slot"]}** | '
          f'**{ph["by_field"]["envelope.bound_expr"]["slot"]}** | '
          f'**{ph["by_field"]["narrative"]["slot"]}** | **{n_slot}** | **{n_total}** |', '',
          '### 事实占位清单（逐条可核）', '',
          '| # | entry_id | 字段路径 | 原文片段 |', '|---|---|---|---|']
    n = 0
    for eid in sorted(ph['facts']):
        for path, txt in ph['facts'][eid]:
            n += 1
            L.append(f'| {n} | {eid} | `{path}` | {md_cell(_flat(txt, 90))} |')
    if n == 0:
        L.append('| — | — | — | （无事实占位） |')
    L += ['', f'**事实占位合计 {n_fact} 处；槽 {n_slot} 处；原方括号总数 {n_total} 处。**', '',
          '## 逐条矩阵', '',
          '图例：✓ 过 ｜ ✗ 败 ｜ – 不适用/跳过 ｜ · 无记录。'
          'seed 资格 = M2∧M3∧M4∧M6∧M9∧C-ENV∧C-ST（README §5；M5 软警告不阻断；C-ID 全局面并入）。', '',
          '| entry_id | status | C-ID | M2 | M3 | M4 | M5 | M6 | M9 | C-ENV | C-ST | seed 资格 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for e in entries:
        eid = str(e.get('entry_id'))
        cells = [rep.status_of(eid, c) for c in ('C-ID', 'M2', 'M3', 'M4', 'M5', 'M6', 'M9', 'C-ENV', 'C-ST')]
        s = seeds[eid]
        note = f'（{_first_sentence(s["detail"], 50)}）' if s['verdict'] == '不成立' else ''
        L.append(f'| {eid} | {e.get("status")} | ' + ' | '.join(cells) + f' | {s["verdict"]}{note} |')
    L += ['', '## 硬失败明细', '']
    if not hard_f:
        L += ['（无——硬检查全过）', '']
    else:
        L += [f'- **[{r.check}] {r.scope}**：{r.reason}' for r in hard_f] + ['']
    L += ['## 软警告（M5 narrative_sync）', '']
    if not soft_f:
        L += ['（无）', '']
    else:
        L += [f'- **[{r.check}] {r.scope}**：{r.reason}' for r in soft_f] + ['']
    # ── 附录：台账核对（ST-STY-01 evidence 约定 / Waiver / MJ / LEDGER）──
    L += ['## 附录：台账核对', '']
    for t in reg_doc.get('status_transitions') or []:
        ev_ok = not hard_f
        L += [f'- **{t.get("transition_id")}**（{t.get("from")}→{t.get("to")}，{t.get("date")}，'
              f'影响级 {t.get("impact_level")}）：条件「{_flat(t.get("condition"), 70)}」——'
              f'本次运行{"满足" if ev_ok else "**不满足**"}其 evidence 约定'
              + ('' if ev_ok else ' → 按 C-ST 回落 status: draft（禁止静默迁移）'),
              f'  - evidence 原文：{_flat(t.get("evidence"), 120)}', '']
    for w in wvs:
        ap = w.get('approval') or {}
        dl = w.get('deadline') or {}
        L += [f'- **{w.get("waiver_id")}**（{w.get("status")}；批准状态 {ap.get("status")}，'
              f'类目「{_flat(ap.get("category"), 40)}」）：规则「{_flat(w.get("rule"), 60)}」。'
              'Waiver 批准是人的裁决（9.2.2），本工具与 Agent 不自行批准。',
              f'  - scope（起首摘录，超长以 … 标记截断）：{_flat(w.get("scope"), 110)}',
              f'  - 时限：type={dl.get("type")}｜lrm={_flat(dl.get("lrm"), 60)}｜'
              f'calendar_date={dl.get("calendar_date") or "（未给日历日期，以事件定 LRM）"}',
              f'  - remediation_plan（起首摘录，超长以 … 标记截断）：{_flat(w.get("remediation_plan"), 110)}', '']
    mjs = reg_doc.get('manual_judgments') or []
    L += [f'- **人工判断台账（MJ）**：{len(mjs)} 项在案（' + '、'.join(str(m.get('id')) for m in mjs) + '）。',
          f'- **缺口台账（gaps）**：{len(reg_doc.get("gaps") or [])} 项；'
          f'**SO 台账**：{len(reg_doc.get('survey_obligations') or [])} 项；'
          f'**PCR**：closed {len((reg_doc.get('pending_conflict_rows') or {}).get('closed_in_entries') or [])}'
          f'／open {len((reg_doc.get('pending_conflict_rows') or {}).get('open_rows') or [])}。', '']
    led = [r for r in rep.of('LEDGER') if r.level == 'info']
    if led:
        L += ['### 台账完整性检查（LEDGER，信息性）', '']
        L += [f'- {r.scope}：{r.reason}' for r in led] + ['']
    return '\n'.join(L)


def _entry_card(e: dict, ctx: dict) -> list:
    """单条目紧凑卡片（kind 无关）：只投影 yaml 既有字段，不新增任何事实。"""
    seeds, layers = ctx['seeds'], ctx['layers']
    eid = str(e.get('entry_id'))
    s = seeds[eid]
    v = e.get('version') or {}
    L = [f'### {eid}｜{e.get("name")}', '',
         f'- **状态** {e.get("status")}（seed 资格：{s["verdict"]}）｜'
         f'**版本** {v.get("major")}.{v.get("minor")}.{v.get("patch")}｜'
         f'**可逆性** {e.get("typical_reversibility")}｜**origin** {(e.get("provenance") or {}).get("origin")}',
         '- **源行**：' + ('、'.join(entry_row_names(e)) or '（无 row_id 源行）')]
    for it in e.get('envelope') or []:
        L.append(f'- **envelope** {it.get("metric")}：`{it.get("bound_expr")}`')
    cp = e.get('cost_profile') or {}
    if cp:
        ops = ' '.join(str(cp.get('ops_cost') or '').split()).strip('[]')
        L.append(f'- **成本**：ops_cost＝{_clip(ops, 70)}｜'
                 f'聚合语义={cp.get("aggregation_semantics")}')
    aps = e.get('anti_patterns') or []
    if aps:
        sig: dict = {}
        for ap in aps:
            sig[ap.get('signal_level')] = sig.get(ap.get('signal_level'), 0) + 1
        L.append(f'- **反模式** {len(aps)} 项（' + '／'.join(f'{k}×{n}' for k, n in sorted(sig.items())) + '）：'
                 + '；'.join(f'{ap.get("pattern_id")} {_first_sentence(ap.get("description"), 36)}' for ap in aps))
    comp = e.get('compatibility') or []
    if comp:
        L.append('- **兼容性**：' + '、'.join(f'{c.get("peer_entry")}({c.get("relation")})' for c in comp))
    cons = e.get('constraints_imposed') or []
    if cons:
        parts = []
        for c in cons[:4]:
            ta = c.get('target_aspect')
            lab = f'方面 {ta}' if isinstance(ta, int) else str(ta)
            parts.append(f'{lab}←{_first_sentence(c.get("constraint"), 36)}')
        L.append(f'- **施加约束** {len(cons)} 项：' + '；'.join(parts)
                 + ('…' if len(cons) > 4 else ''))
    fa = e.get('formal_anchor') or []
    if fa:
        L.append('- **formal_anchor**：' + '、'.join(f'{a.get("property_id")}({a.get("role")})' for a in fa))
    refs = e.get('references') or []
    if refs:
        L.append('- **参考文献**：' + '、'.join(
            f'bib {r.get("bib_id")} {r.get("trust_grade")}·{r.get("compile_usage")}' for r in refs))
    nar = e.get('narrative') or {}
    if nar.get('benefit_cost_analysis'):
        L.append(f'- **叙事（收益-成本）**：{_first_sentence(nar.get("benefit_cost_analysis"), 100)}')
    lay = layers.get(eid) or {}
    if lay:
        L.append('- **数据来源层**（yaml 行内注释）：'
                 + '；'.join(f'{f}: ' + '/'.join(labs) for f, labs in lay.items()))
    L.append('')
    return L


def render_entry_cards(ctx: dict) -> str:
    """STY.md：全部条目的人类层卡片视图，按 kind 入库序分块。
    STY 块内保留四子维度分块（SUBDIM_ORDER，README §4 裁决 MJ-1）；其余 kind 各一块，
    块标题的源表号取自 provenance.source_pointers 的 row_id 前缀（客观事实，非自撰名称）。
    机器层权威 = method_registry.yaml；本投影只作人类阅读面，不新增任何事实。"""
    entries, reg_doc, prof_status = ctx['entries'], ctx['reg_doc'], ctx['prof_status']
    meta = reg_doc.get('meta') or {}
    rv = meta.get('registry_version') or {}
    census = _kind_census(entries)
    L = ['# 方法条目卡片（人类层投影）', '', GEN_NOTE, '',
         f'- 批次：{meta.get("batch")}',
         f'- 版本：registry_version {rv.get("major")}.{rv.get("minor")}.{rv.get("patch")}',
         f'- 条目：合计 {len(entries)} 条＝' + '＋'.join(f'{k} {n} 条' for k, n in census),
         f'- kind 覆盖：{meta.get("kind_coverage")}',
         '- 文件名沿用 README §6 既定产物名 `STY.md`（该产物首块 kind 为 STY 时的历史命名）；'
         '改文件名属规范面变更，须走 ADR＋人工批准，本投影不自行改名。',
         '- 编号：STY 块内分块序为 README §4 裁决，锚定 STY-004（母本反例 18-A 既有引用一致，MJ-1）；母本零改动。',
         '- 卡片仅为紧凑投影；字段全量与逐字措辞以 method_registry.yaml 为准。', '']
    by_kind: dict = {}
    for e in entries:
        by_kind.setdefault(e.get('kind'), []).append(e)
    for k, n in census:
        group = sorted(by_kind[k], key=lambda x: str(x.get('entry_id')))
        subs: dict = {}
        for e in group:
            subs.setdefault(entry_subdim(e), []).append(e)
        pstat = prof_status.get(k)
        order = [s for s in SUBDIM_ORDER if s in subs] + sorted(s for s in subs if s not in SUBDIM_ORDER)
        if k == 'STY':
            for sub in order:
                g2 = subs[sub]
                L += [f'## {SUBDIM_NAME.get(sub, sub)}', '',
                      f'（{g2[0].get("entry_id")}–{g2[-1].get("entry_id")}，共 {len(g2)} 条；'
                      f'kind_profile_STY status={pstat}）', '']
                for e in g2:
                    L += _entry_card(e, ctx)
        else:
            L += [f'## kind {k}（源表 {"、".join(order)}）', '',
                  f'（{group[0].get("entry_id")}–{group[-1].get("entry_id")}，共 {n} 条；'
                  f'kind_profile_{k} status={pstat}；块内按 entry_id 升序）', '']
            for e in group:
                L += _entry_card(e, ctx)
    return '\n'.join(L)


def render_index(ctx: dict) -> str:
    """索引.md：meta、产物互链、17 剖面状态、条目清单、六节台账摘要。"""
    reg_doc, profiles_doc = ctx['reg_doc'], ctx['profiles_doc']
    entries, seeds = ctx['entries'], ctx['seeds']
    meta = reg_doc.get('meta') or {}
    rv = meta.get('registry_version') or {}
    L = ['# 方法注册表索引（投影）', '', GEN_NOTE, '',
         '## 产物（README §6）', '',
         '| 文件 | 内容 |', '|---|---|',
         f'| [STY.md](STY.md) | 方法条目卡片（人类层投影）：{len(entries)} 条＝'
         + '＋'.join(f'{k} {n} 条' for k, n in _kind_census(entries))
         + '；按 kind 入库序分块，STY 块内再分四子维度 |',
         '| [自检报告.md](自检报告.md) | 汇总＋逐条矩阵＋硬失败明细＋台账核对 |',
         '| [勘察义务清单.md](勘察义务清单.md) | 决策期占位符逐条枚举＋入库期 SO 台账 |',
         '| 索引.md（本文件） | meta、剖面状态、条目清单、台账全景 |', '',
         '## meta（method_registry.yaml）', '',
         f'- registry_version：{rv.get("major")}.{rv.get("minor")}.{rv.get("patch")}｜批次：{meta.get("batch")}',
         f'- entry_count：{meta.get("entry_count")}｜kind_coverage：{meta.get("kind_coverage")}']
    for k in ('schema_source', 'kind_enum_source', 'seed_channel_source', 'metric_vocabulary_source', 'signal_level_source'):
        src = meta.get(k) or {}
        L.append(f'- {k}：{src.get("source_type")}→{src.get("value")}（verified={src.get("verified")}）')
    L += ['', '## kind 剖面状态（profiles.yaml，17 个）', '',
          '| entry_id | kind | status | required | optional | N-A | undecided | 条目级豁免 |',
          '|---|---|---|---|---|---|---|---|']
    for p in profiles_doc.get('profiles') or []:
        m = ctx['mat'].get(p.get('describes_kind')) or {}
        L.append('| {pid} | {k} | {st} | {r} | {o} | {n} | {u} | {e} |'.format(
            pid=p.get('entry_id'), k=p.get('describes_kind'), st=p.get('status'),
            r=len(m.get('required') or []), o=len(m.get('optional') or []),
            n=len(m.get('not_applicable') or []), u=len(m.get('undecided') or []),
            e=len(m.get('exemptions') or [])))
    L += ['', f'## 条目清单（全部 {len(entries)} 条）', '',
          '| entry_id | kind | 子维度/源表 | name | status | seed 资格 |',
          '|---|---|---|---|---|---|']
    for e in entries:
        eid = str(e.get('entry_id'))
        L.append(f'| {eid} | {e.get("kind")} | {entry_subdim(e)} | {md_cell(e.get("name"))} '
                 f'| {e.get("status")} | {seeds[eid]["verdict"]} |')
    L += ['', '## 台账全景（method_registry.yaml）', '', '### gaps（缺口）', '',
          '| gap_id | type | status | 陈述（首句） |', '|---|---|---|---|']
    for g in reg_doc.get('gaps') or []:
        L.append(f'| {g.get("gap_id")} | {md_cell(_flat(g.get("type"), 30))} | {g.get("status")} '
                 f'| {md_cell(_first_sentence(g.get("statement"), 80))} |')
    L += ['', '### manual_judgments（MJ，人工判断留痕）', '',
          '| id | subject | affected |', '|---|---|---|']
    for m in reg_doc.get('manual_judgments') or []:
        L.append(f'| {m.get("id")} | {md_cell(_flat(m.get("subject"), 60))} | {md_cell(_flat(m.get("affected"), 60))} |')
    L += ['', '### status_transitions / waivers / PCR / SO', '',
          '| 台账 | 项 | 状态 |', '|---|---|---|']
    for t in reg_doc.get('status_transitions') or []:
        L.append(f'| status_transitions | {t.get("transition_id")}（{_flat(t.get("from"), 20)}→'
                 f'{_flat(t.get("to"), 20)}，{t.get("date")}） | {_flat(t.get("scope"), 40)} |')
    for w in reg_doc.get('waivers') or []:
        L.append(f'| waivers | {w.get("waiver_id")}（{(w.get("approval") or {}).get("category", "")[:24]}…） '
                 f'| {w.get("status")}／批准 {(w.get("approval") or {}).get("status")} |')
    pcr = reg_doc.get('pending_conflict_rows') or {}
    for r in pcr.get('open_rows') or []:
        L.append(f'| PCR open | {r.get("row_id")}（{md_cell(_flat(r.get("matrix_row"), 40))}） '
                 f'| {md_cell(_flat(r.get("disposition"), 50))} |')
    L.append(f'| PCR closed | 已在条目 compatibility 承载 | {len(pcr.get("closed_in_entries") or [])} 行 |')
    for so in reg_doc.get('survey_obligations') or []:
        L.append(f'| survey_obligations | {so.get("obligation_id")}（{_flat(so.get("kind"), 24)}） '
                 f'| {so.get("status")} |')
    L.append('')
    return '\n'.join(L)


# ═══════════════════════════════ 8. 编排与 CLI ═══════════════════════════════

def run_checks():
    """加载全部源 → 依序执行全部检查 → 返回 (rep, ctx)。ctx 供四个渲染器共用。"""
    rep = Report()
    reg_doc = load_yaml(REG_PATH)
    profiles_doc = load_yaml(PROFILES_PATH)
    vocab_doc = load_yaml(VOCAB_PATH)
    law_text, compile_text = read_text(LAW_PATH), read_text(COMPILE_PATH)
    reg_text = read_text(REG_PATH)
    idx = Index(law_text, compile_text)
    # PTR：三文件全部机器可读源指针反查权威源（防幻觉，README §5）
    per_file, ptr_total, ptr_miss = check_pointers(rep, idx, {
        REG_PATH.name: reg_doc, PROFILES_PATH.name: profiles_doc, VOCAB_PATH.name: vocab_doc})
    check_bib_sanity(rep, idx)
    vocab = build_vocab(rep, vocab_doc)
    mat = check_kind_enum(rep, idx, profiles_doc)
    prof_status = {p.get('describes_kind'): p.get('status') for p in profiles_doc.get('profiles') or []}
    entries = reg_doc.get('entries') or []
    all_ids = {str(e.get('entry_id')) for e in entries}
    check_cid(rep, entries, idx)
    for e in entries:
        eid = str(e.get('entry_id'))
        check_schema(rep, e, eid)
        check_m2(rep, e, eid, mat, prof_status)
        check_m3(rep, e, eid, idx)
        check_m4(rep, e, eid, vocab)
        check_m5(rep, e, eid)
        check_m6(rep, e, eid)
        check_m9(rep, e, eid, all_ids)
        check_cenv(rep, e, eid, mat)
    check_meta(rep, reg_doc, entries, idx, mat, prof_status)
    check_cst(rep, entries, mat, prof_status)
    check_ledgers(rep, reg_doc, vocab_doc, profiles_doc)
    check_gap_so_integrity(rep, reg_doc)
    ctx = {
        'rep': rep, 'idx': idx, 'reg_doc': reg_doc, 'profiles_doc': profiles_doc,
        'vocab_doc': vocab_doc, 'entries': entries, 'mat': mat, 'prof_status': prof_status,
        'per_file': per_file, 'ptr_total': ptr_total, 'ptr_miss': ptr_miss,
        'placeholders': census_placeholders(entries), 'trust_marks': census_trust_marks(entries),
        'seeds': seed_summary(rep, entries, prof_status), 'layers': extract_layers(reg_text),
    }
    return rep, ctx


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description='方法注册表自检 + 同源投影（registry/README §5/§6）')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true', help='仅自检（写 projections/自检报告.md）')
    g.add_argument('--project', action='store_true', help='自检 + 生成全部人类层投影')
    args = ap.parse_args(argv)
    for p in (LAW_PATH, COMPILE_PATH, REG_PATH, PROFILES_PATH, VOCAB_PATH):
        if not p.exists():
            sys.stderr.write(f'缺少必需文件：{p}\n')
            return 1
    rep, ctx = run_checks()
    write_text('自检报告.md', render_self_check(ctx))
    if args.project:
        write_text('STY.md', render_entry_cards(ctx))
        write_text('勘察义务清单.md', render_survey(ctx))
        write_text('索引.md', render_index(ctx))
    hard_f, soft_f = rep.failures('hard'), rep.failures('soft')
    ph = ctx['placeholders']
    print(f'自检：{len(rep.rows)} 条记录｜硬失败 {len(hard_f)}｜软警告 {len(soft_f)}｜'
          f'占位符 {ph["total"]} 处＝事实 {ph["fact_total"]}＋槽 {ph["slot_total"]}')
    print(f'产物：{PROJ_DIR}/' + ('（四件）' if args.project else '（自检报告.md）'))
    if hard_f:
        for r in hard_f[:20]:
            print(f'  ✗ [{r.check}] {r.scope}: {r.reason}')
        if len(hard_f) > 20:
            print(f'  …另 {len(hard_f) - 20} 条，详见 projections/自检报告.md')
    return 1 if hard_f else 0


if __name__ == '__main__':
    sys.exit(main())

