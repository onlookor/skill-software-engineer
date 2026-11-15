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
  external 类条目额外核对 bib_id 是否可在母本参考文献中解析，并区分「未核验缺陷」与
  「external 来源清单」（hybrid 条目的出处构成，不等于未核验）。
- C7 判定谓词（编译规范 5.1）：`version_consistent ∧ fidelity_verdict = pass`；
  三清单随产物发布，非空不阻塞（唯一发布阈值＝悬空引用类锚定缺口=0，见 C2）。

用法：python3 pilot/vertical-slice-20261112/c7-coverage.py [--out PATH]
输出：pilot/vertical-slice-20261112/c7-coverage-report.yaml
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
BIB_LINE_RE = re.compile(r'^(\d{1,3})\.\s')
REF_HEAD_RE = re.compile(r'^### \d+\.(?:9|[78]) ')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mother_bib_ids(lines: list[str]) -> set[int]:
    """母本各 x.7/x.8/x.9 节中形如 `N. ` 的参考文献条目号。"""
    ids, in_ref = set(), False
    for line in lines:
        if REF_HEAD_RE.match(line):
            in_ref = True
            continue
        if in_ref and re.match(r'^#{2,4} ', line):
            in_ref = False
        m = BIB_LINE_RE.match(line)
        if in_ref and m:
            ids.add(int(m.group(1)))
    return ids


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


def provenance_rows(entries: list[dict], id_key: str, origin_file: str,
                    bib_ids: set[int]) -> dict:
    """聚合一个注册面的 provenance：缺失 source_status、未核验指针、非母本来源。"""
    missing_status, unverified, non_mother, class_dist = 0, [], [], {}
    pointer_total = pointer_verified = 0
    refs_used: set[str] = set()
    for e in entries:
        eid = e.get(id_key) or e.get('entry_id') or '?'
        prov = e.get('provenance') or {}
        if 'source_status' not in e and 'source_status' not in prov:
            missing_status += 1
        sc = prov.get('source_class')
        class_dist[str(sc)] = class_dist.get(str(sc), 0) + 1
        pointers = prov.get('source_pointers') or []
        pointer_total += len(pointers)
        pointer_verified += sum(p.get('verified') is True for p in pointers)
        bib_refs = sorted({str(p.get('value')) for p in pointers
                           if p.get('source_type') == 'bib_id'})
        refs_used.update(bib_refs)
        unresolved = [r for r in bib_refs if not r.isdigit() or int(r) not in bib_ids]
        if sc in ('external', 'external-bib'):
            non_mother.append({
                'id': eid,
                'source_class': sc,
                'origin': prov.get('origin'),
                'pointer_count': len(pointers),
                'all_pointers_verified': bool(pointers) and
                                         all(p.get('verified') is True for p in pointers),
                'bib_refs': bib_refs,
                'bib_refs_unresolved': unresolved,
            })
        bad = [p for p in pointers if p.get('verified') is not True]
        if bad:
            unverified.append({
                'id': eid,
                'source_class': sc,
                'pointers': [{k: p.get(k) for k in ('source_type', 'value', 'verified')}
                             for p in bad],
            })
    unresolved_all = sorted(r for r in refs_used
                            if not r.isdigit() or int(r) not in bib_ids)
    return {
        'file': origin_file,
        'entry_count': len(entries),
        'source_status_field': 'absent' if missing_status == len(entries) else
                               f'present in {len(entries) - missing_status} entries',
        'entries_without_source_status': missing_status,
        'source_class_distribution': dict(sorted(class_dist.items())),
        'pointer_stats': {
            'total': pointer_total,
            'verified': pointer_verified,
            'unverified': pointer_total - pointer_verified,
        },
        'bib_refs': {
            'distinct': sorted(int(r) for r in refs_used if r.isdigit()),
            'resolved': sorted(int(r) for r in refs_used
                               if r.isdigit() and int(r) in bib_ids),
            'unresolved': unresolved_all,
            'mother_bibliography_range': [min(bib_ids), max(bib_ids)] if bib_ids else [],
        },
        'unverified_pointer_entries': unverified,
        'non_mother_source_entries': non_mother,
        'status': ('无未核验指针且 bib_id 全部可解析；external 类条目为 hybrid 出处构成，'
                   '不是未核验缺陷' if not unverified and not unresolved_all else
                   '存在未核验指针或不可解析的 bib_id，见上两表'),
    }


def c7_predicate(mother_text: str, mr: dict) -> dict:
    """按编译规范 5.1 C7 判定谓词 `version_consistent ∧ fidelity_verdict = pass` 机械核对。"""
    art_path = HERE / 'artifact.yaml'
    ca = (yaml.safe_load(art_path.read_text(encoding='utf-8')) or {}).get(
        'compilation_artifact') or {}
    ver = ca.get('version') or {}
    fw_cur = 'sha256:' + hashlib.sha256(mother_text.encode('utf-8')).hexdigest()
    reg_cur = (mr.get('meta') or {}).get('registry_version')
    fid_path = HERE / 'fidelity-all.json'
    fid = json.loads(fid_path.read_text(encoding='utf-8')) if fid_path.exists() else {}
    f3 = (fid.get('F3') or {}).get('full_verdict')
    fid_pass = fid.get('F1_verdict') == 'pass' and fid.get('F2_verdict') == 'pass' \
        and f3 == 'pass'
    version_consistent = (ver.get('framework_version') == fw_cur
                          and ver.get('registry_version') == reg_cur)
    return {
        'rule': '编译规范 5.1 C7：version_consistent ∧ fidelity_verdict = pass',
        'framework_version': {'current': fw_cur, 'artifact': ver.get('framework_version')},
        'registry_version': {'current': reg_cur, 'artifact': ver.get('registry_version')},
        'version_consistent': version_consistent,
        'fidelity_verdict': {'F1': fid.get('F1_verdict'), 'F2': fid.get('F2_verdict'),
                             'F3_full': f3, 'pass': fid_pass,
                             'source': 'pilot/vertical-slice-20261112/fidelity-all.json'},
        'predicate_satisfied': version_consistent and fid_pass,
        'publish_note': '本报告只核对判定谓词；SM-CA compiling→valid 见白板 state_machines.SM-CA，对外发布动作不在本脚本',
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'c7-coverage-report.yaml'))
    args = ap.parse_args()

    mother_text = MOTHER.read_text(encoding='utf-8')
    mother_lines = mother_text.splitlines()
    soft = soft_denominator(mother_lines)
    bib_ids = mother_bib_ids(mother_lines)
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
        'c7_predicate_check': c7_predicate(mother_text, mr),
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
            'status': ('软性质覆盖为可选（编译规范 3.3 映射表）；未覆盖登记为覆盖率缺口，'
                       '非阻塞发布。是否升为机械检查属待裁项，本脚本不自判'),
        },
        'questionable_source_list': {
            'rule': 'provenance.source_pointers 中 verified != true；source_class ∈ {external, external-bib}；source_status 字段缺失如实记',
            'method_registry': provenance_rows(mr.get('entries') or [], 'entry_id',
                                               'registry/method_registry.yaml', bib_ids),
            'profiles': provenance_rows(profiles, 'entry_id', 'registry/profiles.yaml', bib_ids),
            'status': ('存疑来源按编译规范 4.5 的 `unverified_source` 判定：指针未核验或 bib_id '
                       '不可解析即缺陷；external 类条目另列作出处构成清单，不自动等同缺陷'),
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
