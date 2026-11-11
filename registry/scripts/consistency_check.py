#!/usr/bin/env python3
"""A 类一致性检查（只读）。

检查「母本 ↔ registry 指针」五条判据（A1–A5），产出 kind × 判据清单，
并对每条判据做反向自测（总则第 10 条：空转判据不算数）。

只读：不修改母本、profiles.yaml、ADR 或任何冻结文件；唯一写入是 --out 报告。
用法:
  python3 registry/scripts/consistency_check.py
  python3 registry/scripts/consistency_check.py --out /tmp/a.md
"""
from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
MOTHER = ROOT / '软件工程元框架成文法.md'
PROFILES = ROOT / 'registry' / 'profiles.yaml'
DEFAULT_OUT = ROOT / 'registry' / 'consistency-report-20261111.md'

HEAD_RE = re.compile(r'^(#{2,6})\s+((?:\d+\.)+\d*)\s')

# 0.18.1 的三段登记状态（判据的分档依据；来源见报告 B 类检查点）
PARTICIPATING = {'STY', 'DEC', 'CTR', 'OWN', 'CSL', 'CRD', 'QAT', 'VFM', 'DPS', 'PRJ'}
PENDING = {'STP', 'DFL', 'SCH', 'CFG', 'RLP'}
NONPART = {'GRD', 'SRC', 'GOV'}

PREFIX = '待补登记'

# 0.18.1 段末新增的「10 决策点 → 0.18.4 九行」映射句（A2 的第二命中源）
MAPPING_START = '上述 10 个决策点与 0.18.4 九行的逐项对应为'


def load_clauses() -> dict[str, dict]:
    lines = MOTHER.read_text(encoding='utf-8').splitlines()
    heads = [(i, l) for i, l in enumerate(lines) if HEAD_RE.match(l)]
    clauses: dict[str, dict] = {}
    for idx, (i, line) in enumerate(heads):
        num = HEAD_RE.match(line).group(2)
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        clauses[num] = {
            'line': i + 1,
            'title': line.strip(),
            'text': '\n'.join(lines[i:end]),
        }
    return clauses


def load_profiles() -> dict[str, dict]:
    data = yaml.safe_load(PROFILES.read_text(encoding='utf-8'))
    return {e['describes_kind']: e for e in data['profiles']}


def kind_names(clauses: dict[str, dict]) -> dict[str, str]:
    """从 0.17.3 的 kind 封闭枚举表解析 kind → 正式名称。"""
    names = {}
    for m in re.finditer(r'^\|\s*([A-Z]{2,4})\s*\|\s*([^|]+?)\s*\|', clauses['0.17.3']['text'], re.M):
        names[m.group(1)] = m.group(2).strip()
    return names


def _hit(term: str, text: str) -> int:
    return text.count(term)


def _segment(text: str, start: str, end: str) -> str:
    i = text.find(start)
    j = text.find(end, i) if i >= 0 else -1
    if i < 0 or j < 0:
        return ''
    return text[i:j]


def check_a1(entry: dict, kind: str, clauses: dict) -> dict:
    src = (entry.get('selection_profile') or {}).get('source') or {}
    st, val = src.get('source_type'), src.get('value')
    if st != 'clause_id':
        return {'status': 'skip', 'evidence': f'source_type={st}，A1 不适用'}
    if val in clauses:
        return {'status': 'pass', 'evidence': f'{val} 存在（第 {clauses[val]["line"]} 行）'}
    return {'status': 'fail', 'evidence': f'条款号 {val} 在母本不存在（检索 0 次）'}


def check_a2(entry: dict, kind: str, name: str, clauses: dict) -> dict:
    src = (entry.get('selection_profile') or {}).get('source') or {}
    if src.get('verified') is not True:
        return {'status': 'skip', 'evidence': 'verified 非 true，A2 不适用'}
    terms = [kind, name]
    if kind in PARTICIPATING:
        text = clauses['0.18.4']['text']
        mapseg = _segment(clauses['0.18.1']['text'], MAPPING_START, '。')
        hit = [(t, _hit(t, text)) for t in terms if _hit(t, text)]
        mhit = [(t, _hit(t, mapseg)) for t in terms if _hit(t, mapseg)]
        if hit or mhit:
            parts = []
            if hit:
                parts.append('0.18.4 命中：' + '、'.join(f'{t}×{n}' for t, n in hit))
            if mhit:
                parts.append('0.18.1 映射句命中：' + '、'.join(f'{t}×{n}' for t, n in mhit))
            return {'status': 'pass', 'evidence': '；'.join(parts)}
        rows = [r for r in re.findall(r'^\|\s*([^|]+?)\s*\|', text, re.M) if set(r.strip()) - {'-'}]
        return {'status': 'fail',
                'evidence': f'0.18.4 行名与 0.18.1 映射句检索「{name}」「{kind}」均 0 次；该表行名：'
                            + '；'.join(r.strip() for r in rows)}
    if kind in PENDING:
        text = clauses['0.18.1']['text']
        seg = _segment(text, '存储拓扑、数据流动机制', '；守护规则模板') or text
        hit = [(t, _hit(t, seg)) for t in terms if _hit(t, seg)]
        if hit:
            return {'status': 'pass', 'evidence': '0.18.1 待补枚举命中：' + '、'.join(f'{t}×{n}' for t, n in hit)}
        return {'status': 'fail', 'evidence': f'0.18.1「尚未登记 0.18.4 变体」枚举内检索「{name}」0 次'}
    if kind in NONPART:
        text = clauses['0.18.1']['text']
        seg = _segment(text, '守护规则模板、漂移/腐化信号源', '三类合计') or text
        hit = [(t, _hit(t, seg)) for t in terms if _hit(t, seg)]
        if hit:
            return {'status': 'pass', 'evidence': '0.18.1 不参与枚举命中：' + '、'.join(f'{t}×{n}' for t, n in hit)}
        return {'status': 'fail', 'evidence': f'0.18.1「不参与…不补表」枚举内检索「{name}」0 次'}
    return {'status': 'fail', 'evidence': f'{kind} 不属于 10／5／3 任一分档'}


def check_a3(entry: dict, kind: str, name: str, clauses: dict) -> dict:
    """verified 取甲：只判条款存在；逐字点名降为信息项（unnamed），不参与判定。"""
    pointers = (entry.get('provenance') or {}).get('source_pointers') or []
    missing, unnamed = [], []
    for p in pointers:
        val, ver = p.get('value'), p.get('verified')
        if val not in clauses:
            missing.append(val)
            continue
        if ver is not True:
            continue
        text = clauses[val]['text']
        if not (_hit(kind, text) or _hit(name, text)):
            unnamed.append(f'{val}（检索 {name}／{kind} 0 次；条款首行：{clauses[val]["title"]}）')
    if missing:
        return {'status': 'fail', 'pointers': len(pointers),
                'evidence': '条款不存在：' + '；'.join(f'{v}（检索 0 次）' for v in missing),
                'missing': missing, 'unnamed': unnamed}
    return {'status': 'pass', 'pointers': len(pointers), 'unnamed': unnamed,
            'evidence': f'{len(pointers)} 条指针的条款号均存在；未点名 {len(unnamed)} 条（信息项）'}


def check_a4(entry: dict, kind: str, clauses: dict) -> dict:
    sp = entry.get('selection_profile') or {}
    if 'participates' not in sp:
        return {'status': 'fail', 'evidence': 'selection_profile 缺 participates 键（不得默认按不适用抵扣）'}
    if not isinstance(sp['participates'], bool):
        return {'status': 'fail', 'evidence': f'participates 非布尔：{sp["participates"]!r}'}
    return {'status': 'pass', 'evidence': f'participates={sp["participates"]}'}


def check_a5(entry: dict, kind: str, clauses: dict) -> dict:
    sp = entry.get('selection_profile') or {}
    part, variant = sp.get('participates'), (sp.get('variant') or '')
    has = variant.startswith(PREFIX)
    if part is False and has:
        return {'status': 'fail', 'evidence': 'participates=false 却带「待补登记」前缀'}
    if part is True and kind in PENDING and not has:
        return {'status': 'fail', 'evidence': 'participates=true 且属待补，却无「待补登记」前缀'}
    if part is True and kind not in PENDING and has:
        return {'status': 'fail', 'evidence': 'participates=true 且非待补，却带「待补登记」前缀'}
    return {'status': 'pass', 'evidence': f'participates={part}，前缀={"有" if has else "无"}'}


CHECKS = [('A1', check_a1), ('A2', check_a2), ('A3', check_a3), ('A4', check_a4), ('A5', check_a5)]


def run_all(entries: dict, names: dict, clauses: dict, override_name: dict | None = None) -> list[dict]:
    rows = []
    for kind in sorted(entries):
        name = (override_name or {}).get(kind, names.get(kind, ''))
        for cid, fn in CHECKS:
            if cid == 'A2':
                r = fn(entries[kind], kind, name, clauses)
            elif cid == 'A3':
                r = fn(entries[kind], kind, name, clauses)
            else:
                r = fn(entries[kind], kind, clauses)
            rows.append({'kind': kind, 'criterion': cid, **r})
    return rows


def selftest(entries: dict, names: dict, clauses: dict) -> list[dict]:
    out = []

    def one(cid, what, rows, kind, expected='fail'):
        sub = [r for r in rows if r['criterion'] == cid and r['kind'] == kind]
        got = sub[0]['status'] if sub else 'missing'
        out.append({'criterion': cid, 'mutation': what, 'expected': expected,
                    'actual': got, 'ok': got == expected})

    e = copy.deepcopy(entries)
    e['STY']['selection_profile']['source']['value'] = '9.9.9'
    one('A1', 'STY 的 selection_profile.source 改为不存在的 9.9.9',
        [dict(status=check_a1(e['STY'], 'STY', clauses)['status'], criterion='A1', kind='STY')], 'STY')

    one('A2', 'VFM 的检索名称改为「虚构验证手段X」（条款中不存在）',
        run_all(entries, names, clauses, override_name={'VFM': '虚构验证手段X'}), 'VFM')

    e = copy.deepcopy(entries)
    e['STY']['provenance']['source_pointers'].append({'value': '9.9.9', 'verified': True})
    one('A3', 'STY 追加不存在的指针条款号 9.9.9',
        [dict(status=check_a3(e['STY'], 'STY', names['STY'], clauses)['status'], criterion='A3', kind='STY')], 'STY')

    e = copy.deepcopy(entries)
    e['STY']['provenance']['source_pointers'].append({'value': '0.5', 'verified': True})
    one('A3', '降级对照：STY 追加 0.5（条款存在但未点名 STY）应为 pass（信息项）',
        [dict(status=check_a3(e['STY'], 'STY', names['STY'], clauses)['status'], criterion='A3', kind='STY')],
        'STY', expected='pass')

    e = copy.deepcopy(entries)
    del e['GRD']['selection_profile']['participates']
    one('A4', '删掉 GRD 的 participates 键',
        [dict(status=check_a4(e['GRD'], 'GRD', clauses)['status'], criterion='A4', kind='GRD')], 'GRD')

    e = copy.deepcopy(entries)
    e['GRD']['selection_profile']['variant'] = '待补登记（X）：' + (e['GRD']['selection_profile'].get('variant') or '')
    one('A5', 'GRD（participates=false）variant 加「待补登记」前缀',
        [dict(status=check_a5(e['GRD'], 'GRD', clauses)['status'], criterion='A5', kind='GRD')], 'GRD')

    e = copy.deepcopy(entries)
    v = e['STP']['selection_profile'].get('variant') or ''
    e['STP']['selection_profile']['variant'] = v[len(PREFIX):].lstrip('：:') if v.startswith(PREFIX) else v
    one('A5', 'STP（participates=true 且属待补）去掉「待补登记」前缀',
        [dict(status=check_a5(e['STP'], 'STP', clauses)['status'], criterion='A5', kind='STP')], 'STP')
    return out


def render(rows: list[dict], tests: list[dict], names: dict) -> str:
    kinds = sorted({r['kind'] for r in rows})
    by_crit = {c: [r for r in rows if r['criterion'] == c] for c, _ in CHECKS}
    fails = [r for r in rows if r['status'] == 'fail']

    L = []
    L.append('# A 类一致性清单（母本 ↔ registry 指针）')
    L.append('')
    L.append('> 只读检查产出；未修改任何数据文件。判据 A1–A5 定义见下，分档依据为 0.18.1 的 10／5／3。')
    L.append('')
    L.append('## 0. 判据定义')
    L.append('')
    L.append('- **A1**：`selection_profile.source`（`source_type: clause_id`）的值必须在母本中存在对应条款号。')
    L.append('- **A2**：`verified: true` 时该 kind 须在所指条文命中。参与 10 个 → 0.18.4 的行名或行文，**或** 0.18.1 段末「10 决策点 → 九行」映射句；待补 5 个 → 0.18.1「尚未登记 0.18.4 变体」枚举；不参与 3 个 → 0.18.1「不参与…不补表」枚举。')
    L.append('- **A3**：`provenance.source_pointers` 每个 `clause_id` 必须存在；`verified: true` 时「是否在该条款内逐字点名本 kind」只作**信息项**（裁定取甲：verified 表示条款存在且规范内容适用于本 kind，不要求逐字点名），不参与通过判定。')
    L.append('- **A4**：`participates` 必须显式存在且为布尔；缺键不得默认按不适用抵扣（R-9 候选）。')
    L.append('- **A5**：`variant` 与 `participates` 不得矛盾：`false` 不得带「待补登记」前缀；`true` 且属待补须带；`true` 且非待补不得带。')
    L.append('')
    L.append('**逐字口径**：检索词 = kind 前缀（如 `STY`）或 0.17.3 的正式名称整串（如 `架构风格`），整串包含即命中；不做同义词放宽。')
    L.append('')
    L.append('## 1. 汇总')
    L.append('')
    L.append(f'- 检查项总数：**{len(rows)}**（{len(kinds)} kind × 5 判据）')
    L.append(f'- fail 总数：**{len(fails)}**')
    L.append('')
    L.append('| 判据 | 检查 | pass | fail | skip |')
    L.append('|---|---:|---:|---:|---:|')
    for c, _ in CHECKS:
        rs = by_crit[c]
        L.append(f'| {c} | {len(rs)} | {sum(r["status"]=="pass" for r in rs)} | '
                 f'{sum(r["status"]=="fail" for r in rs)} | {sum(r["status"]=="skip" for r in rs)} |')
    L.append('')
    L.append('| kind | 分档 | A1 | A2 | A3 | A4 | A5 | fail 数 |')
    L.append('|---|---|---|---|---|---|---|---:|')
    for k in kinds:
        tier = '参与' if k in PARTICIPATING else ('待补' if k in PENDING else '不参与')
        cells = []
        for c, _ in CHECKS:
            st = next(r['status'] for r in rows if r['kind'] == k and r['criterion'] == c)
            cells.append({'pass': 'pass', 'fail': '**fail**', 'skip': 'skip'}[st])
        n = sum(1 for r in rows if r['kind'] == k and r['status'] == 'fail')
        L.append(f'| {k} | {tier} | ' + ' | '.join(cells) + f' | {n} |')
    L.append('')
    L.append('## 2. fail 明细（按判据）')
    L.append('')
    if not fails:
        L.append('（无）')
    for c, _ in CHECKS:
        rs = [r for r in fails if r['criterion'] == c]
        if not rs:
            continue
        L.append(f'### {c}（{len(rs)} 条）')
        L.append('')
        for r in rs:
            L.append(f'- **{r["kind"]}**：{r["evidence"]}')
        L.append('')
    L.append('## 2.1 信息项：A3 逐字点名情况（不参与判定）')
    L.append('')
    a3 = [r for r in rows if r['criterion'] == 'A3']
    ptr_total = sum(r.get('pointers', 0) for r in a3)
    un_total = sum(len(r.get('unnamed', [])) for r in a3)
    L.append(f'- 指针总数 **{ptr_total}**，其中 **{un_total}** 条未在所指条款内逐字点名；按裁定取甲，此项只作可读信息，不计 fail。')
    L.append('')
    for r in a3:
        if r.get('unnamed'):
            L.append(f'- **{r["kind"]}**（{len(r["unnamed"])}）：' + '；'.join(r['unnamed']))
    L.append('')
    L.append('## 3. 反向自测（总则第 10 条）')
    L.append('')
    L.append('| 判据 | 造了什么错 | 期望 | 实测 | 结论 |')
    L.append('|---|---|---|---|---|')
    for t in tests:
        L.append(f'| {t["criterion"]} | {t["mutation"]} | {t["expected"]} | {t["actual"]} | '
                 f'{"如期报红" if t["ok"] else "**未报红，判据空转**"} |')
    L.append('')
    L.append('## 4. B 类检查点（只列不判）')
    L.append('')
    L.append('1. 0.17.3 kind 枚举总数（18）vs 0.18.1 的 10＋5＋3（＝18）。')
    L.append('2. 0.18.1「共 10 类」vs 0.18.4 的 9 行；所有权与一致性共用第 4 行。')
    L.append('3. 0.18.4 表前句（「唯一登记处」）与表后句（行名并列、未出现者不登记）是否覆盖 9 行的并列情形。')
    L.append('4. 0.17.2 的 `participates` 条件规则 vs 0.18.1 的三段状态（10 适用／5 待补／3 不参与）与 0.18.4 行覆盖。')
    L.append('5. 5.2 表末注「全注册表通用」vs 0.17.2 的 kind 剖面与 `not_applicable`（R-1 已取丙，检查点保留）。')
    L.append('6. GOV 消费路径三处枚举：0.17.3 种子源（0.5／7.2.3／7.2.4）、0.18.1 末句（0.5 与 7.2.3／7.2.4）、7.2.4 正文。')
    L.append('7. 0.17.3 末句（未登记决策点暂按 S0–S6；participates: true 者按 0.18.8 补登记）vs 0.18.1 的 5 类补登记句。')
    L.append('8. 0.18.4 表前「profiles.yaml 的 variant 是同源投影，不构成独立登记」vs registry 六条 `selection_profile.source` 的指向方向。')
    L.append('9. 0.18.1「上述 10 个决策点登记于 0.18.4 的 9 行」的内部算术（10 决策点／9 行／共用第 4 行）。')
    L.append('')
    L.append('## 5. 判读提示')
    L.append('')
    L.append('`verified` 语义取**甲**（2026-11-11 裁定）：只表示「条款存在且其规范内容适用于本 kind」，不要求逐字点名；故 A3 的未点名条目列为信息项。A2 的参与类命中源有两处：0.18.4 行名／行文，或 0.18.1 段末新增的「10 决策点 → 九行」映射句（含并列关系与方面号）。')
    L.append('')
    return '\n'.join(L) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    args = ap.parse_args()
    clauses = load_clauses()
    entries = load_profiles()
    names = kind_names(clauses)
    missing = sorted(set(entries) - set(names))
    if missing:
        print(f'0.17.3 未解析到名称：{missing}', file=sys.stderr)
        return 2
    rows = run_all(entries, names, clauses)
    tests = selftest(entries, names, clauses)
    Path(args.out).write_text(render(rows, tests, names), encoding='utf-8')
    fails = sum(r['status'] == 'fail' for r in rows)
    bad = [t for t in tests if not t['ok']]
    print(f'checks={len(rows)} fail={fails} selftests={len(tests)} selftest_bad={len(bad)}')
    print(f'report={args.out}')
    return 0 if not bad else 1


if __name__ == '__main__':
    raise SystemExit(main())
