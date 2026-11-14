#!/usr/bin/env python3
"""c7-coverage.py —— C7 覆盖率报告中「软性质未覆盖」「存疑来源」两清单的机械生成器。

这是 pilot 工具（与 check-card.py 同级），不是 registry/scripts 的正式检查器。

口径（人类裁定 2026-11-14，D4）：
- 软性质分母：母本围栏性质块内，性质条款以 `—— 软` 标注者计入分母（来源＝母本条款本身，
  不新建人工清单）。`—— 条件硬`（失败降软）与 `—— 升级型` 不计入：前者是硬性质的条件形态，
  后者按失败升级处理，均非「软性质」条款。
- 软性质覆盖：该性质是否被 FVR 注册面或检查器以 property_id 显式绑定。未绑定 → 未覆盖。
- 存疑来源：从 method_registry 各条与 profiles 各剖面的 `provenance` 自动聚合——
  `source_pointers` 中 `verified != true` 的指针、`source_class` 为 external 的条目；
  注册面若无 `source_status` 字段，如实记 absent（不臆造字段）。

用法：python3 pilot/vertical-slice-20261112/c7-coverage.py [--out PATH]
输出：pilot/vertical-slice-20261112/c7-coverage-report.yaml
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REG = ROOT / 'registry'
MOTHER = ROOT / '软件工程元框架成文法.md'

PROP_RE = re.compile(r'^\s*([A-Z]\d+):')
SOFT_RE = re.compile(r'——\s*软')
SCORE_RE = re.compile(r'——\s*条件硬|——\s*升级型')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def soft_denominator(lines: list[str]) -> list[dict]:
    """围栏块内按性质聚行，取 `—— 软` 标注者为软性质；返回带行号与标注的清单。"""
    in_fence, cur, props = False, None, []
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        m = PROP_RE.match(line)
        if m:
            cur = {'id': m.group(1), 'line': i + 1, 'text': line}
            props.append(cur)
        elif cur is not None:
            cur['text'] += '\n' + line
    out, seen = [], set()
    for p in props:
        if p['id'] in seen or not SOFT_RE.search(p['text']):
            continue
        seen.add(p['id'])
        ann = [x.strip() for x in p['text'].splitlines() if '——' in x]
        out.append({
            'property_id': p['id'],
            'line': p['line'],
            'annotation': ann[-1] if ann else '',
        })
    return out


def bound_property_ids() -> tuple[set, dict]:
    """FVR 注册面 + 检查器函数名中显式绑定的 property_id。"""
    bound, evidence = set(), {}
    fvr = REG / 'fvr_registry.yaml'
    if fvr.exists():
        doc = yaml.safe_load(fvr.read_text(encoding='utf-8')) or {}
        for e in doc.get('entries') or []:
            for pid in e.get('properties') or []:
                bound.add(pid)
                evidence.setdefault(pid, f'fvr_registry:{e.get("fvr_id", "?")}')
    sys.path.insert(0, str(REG / 'checks'))
    for modname in 'm e w x v t g q r'.split():
        mod = __import__(modname)
        for fn in list(getattr(mod, 'CHECKS', {}).values()) + \
                list(getattr(mod, 'DEFERRED', {}).values()):
            pid = fn.__name__.upper()
            bound.add(pid)
            evidence.setdefault(pid, f'registry/checks/{modname}.py::{fn.__name__}')
    return bound, evidence


def provenance_rows(entries: list[dict], id_key: str, origin_file: str) -> dict:
    """聚合一个注册面的 provenance：缺失 source_status、未核验指针、非母本来源。"""
    missing_status, unverified, non_mother, class_dist = 0, [], [], {}
    for e in entries:
        eid = e.get(id_key) or e.get('entry_id') or '?'
        prov = e.get('provenance') or {}
        if 'source_status' not in e and 'source_status' not in prov:
            missing_status += 1
        sc = prov.get('source_class')
        class_dist[str(sc)] = class_dist.get(str(sc), 0) + 1
        if sc in ('external', 'external-bib'):
            non_mother.append({'id': eid, 'source_class': sc, 'origin': prov.get('origin')})
        bad = [p for p in (prov.get('source_pointers') or []) if p.get('verified') is not True]
        if bad:
            unverified.append({
                'id': eid,
                'source_class': sc,
                'pointers': [{k: p.get(k) for k in ('source_type', 'value', 'verified')}
                             for p in bad],
            })
    return {
        'file': origin_file,
        'entry_count': len(entries),
        'source_status_field': 'absent' if missing_status == len(entries) else
                               f'present in {len(entries) - missing_status} entries',
        'entries_without_source_status': missing_status,
        'source_class_distribution': dict(sorted(class_dist.items())),
        'unverified_pointer_entries': unverified,
        'non_mother_source_entries': non_mother,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'c7-coverage-report.yaml'))
    args = ap.parse_args()

    mother_text = MOTHER.read_text(encoding='utf-8')
    soft = soft_denominator(mother_text.splitlines())
    bound, evidence = bound_property_ids()
    covered = [dict(p, checked_by=evidence[p['property_id']])
               for p in soft if p['property_id'] in bound]
    uncovered = [p['property_id'] for p in soft if p['property_id'] not in bound]

    mr_path, pr_path = REG / 'method_registry.yaml', REG / 'profiles.yaml'
    mr = yaml.safe_load(mr_path.read_text(encoding='utf-8')) or {}
    pr = yaml.safe_load(pr_path.read_text(encoding='utf-8')) or {}
    profiles = pr.get('profiles') or []
    if isinstance(profiles, dict):
        profiles = [dict(v, **{'entry_id': k}) for k, v in profiles.items()]

    report = {
        'meta': {
            'kind': 'C7 覆盖率报告（pilot 工具生成，非母本条款）',
            'generated_by': 'pilot/vertical-slice-20261112/c7-coverage.py',
            'mother_sha256': hashlib.sha256(mother_text.encode('utf-8')).hexdigest(),
            'method_registry_sha256': sha(mr_path),
            'profiles_sha256': sha(pr_path),
            'criteria_source': '编译规范 5.1 C7：覆盖率报告含锚定缺口、软性质未覆盖、存疑来源三清单',
        },
        'anchor_gap_list': {
            'source': 'registry/scripts/anchor_index.py（F-1–F-10，输出 registry/anchor_index/summary.json）',
            'status': '由锚索引生成，本脚本不重复计算',
        },
        'soft_property_list': {
            'denominator_rule': '母本围栏性质块内以 `—— 软` 标注的性质条款；`—— 条件硬`／`—— 升级型` 不计入',
            'denominator_count': len(soft),
            'denominator': soft,
            'covered_count': len(covered),
            'covered': covered,
            'uncovered_count': len(uncovered),
            'uncovered': uncovered,
        },
        'questionable_source_list': {
            'rule': 'provenance.source_pointers 中 verified != true；source_class ∈ {external, external-bib}；source_status 字段缺失如实记',
            'method_registry': provenance_rows(mr.get('entries') or [], 'entry_id',
                                               'registry/method_registry.yaml'),
            'profiles': provenance_rows(profiles, 'entry_id', 'registry/profiles.yaml'),
        },
    }
    Path(args.out).write_text(
        yaml.safe_dump(report, allow_unicode=True, sort_keys=False, width=200), encoding='utf-8')
    print(f"soft: {len(soft)} 分母，{len(covered)} 覆盖，{len(uncovered)} 未覆盖")
    print(f"method_registry: unverified={len(report['questionable_source_list']['method_registry']['unverified_pointer_entries'])}"
          f" non_mother={len(report['questionable_source_list']['method_registry']['non_mother_source_entries'])}"
          f" source_status={report['questionable_source_list']['method_registry']['source_status_field']}")
    print(f"profiles: unverified={len(report['questionable_source_list']['profiles']['unverified_pointer_entries'])}"
          f" non_mother={len(report['questionable_source_list']['profiles']['non_mother_source_entries'])}"
          f" source_status={report['questionable_source_list']['profiles']['source_status_field']}")
    print(f'→ {args.out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
