#!/usr/bin/env python3
"""registry/checks/runner.py —— 39 条硬性质首轮全量执行器。

- 顺序：M → E(1/2/7) → W → X → V → T → G → Q → R → E3 → E5（E3/E5 需要全量 results）。
- 断言：硬性质集合与 hard-properties.snapshot.json 一致（不等即点名失败）。
- 接线：每条性质必须在 fvr-G-CAND-*.yaml 中有 property_id 条目，否则 E3 fail。
- 输出：pilot/vertical-slice-20261112/fvr-full-run-1.json（39 行 verdict）。
退出码：0＝39 条全部执行且三值封闭；1＝执行/域/接线问题。
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import yaml  # noqa: E402

import common  # noqa: E402
import m as grp_m  # noqa: E402
import e as grp_e  # noqa: E402
import w as grp_w  # noqa: E402
import x as grp_x  # noqa: E402
import v as grp_v  # noqa: E402
import t as grp_t  # noqa: E402
import g as grp_g  # noqa: E402
import q as grp_q  # noqa: E402
import r as grp_r  # noqa: E402

ORDER = grp_m.CHECKS | grp_e.CHECKS | grp_w.CHECKS | grp_x.CHECKS | grp_v.CHECKS \
    | grp_t.CHECKS | grp_g.CHECKS | grp_q.CHECKS | grp_r.CHECKS


def fvr_wiring(pilot: Path) -> dict[str, dict]:
    out = {}
    for p in sorted(pilot.glob('fvr-G-CAND-*.yaml')):
        d = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
        for ent in d.get('fvr_entries') or []:
            pid = ent.get('property_id')
            if pid:
                out[pid] = {'file': p.name, 'wired': bool(ent.get('wired', bool(ent.get('trigger_wiring'))))}
    return out


def freeze_snapshot(ctx: dict) -> Path:
    """冻结硬性质 ID 集合快照（分母权威来源；母本漂移时集合不等即报）。"""
    tz = timezone(timedelta(hours=8))
    path = common.PILOT / 'hard-properties.snapshot.json'
    out = {
        'frozen_at': datetime.now(tz).isoformat(timespec='seconds'),
        'mother_sha256': ctx['mother_sha'],
        'source': 'regex ^\\s*([A-Z]\\d+):.*(——|—)\\s*硬 over 软件工程元框架成文法.md',
        'count': len(ctx['hard']),
        'ids': ctx['hard'],
        'predicate_blocks': [
            {'section': b['section'], 'line': b['line'], 'predicates': len(b['names'])} for b in ctx['blocks']
        ],
    }
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"snapshot frozen: {len(ctx['hard'])} ids, {len(ctx['blocks'])} blocks → {path}")
    return path


def main() -> int:
    ctx = common.build_context()
    pilot = common.PILOT
    if '--freeze' in sys.argv:
        freeze_snapshot(ctx)
        return 0
    api_json = json.loads((pilot / 'hard-properties.snapshot.json').read_text(encoding='utf-8')) \
        if (pilot / 'hard-properties.snapshot.json').exists() else {}
    snap_ids = api_json.get('ids') or []
    problems = []

    if set(snap_ids) != set(ctx['hard']):
        problems.append(f"快照集合与母本不一致：新增 {sorted(set(ctx['hard']) - set(snap_ids))}，"
                        f"消失 {sorted(set(snap_ids) - set(ctx['hard']))}")

    wiring = fvr_wiring(pilot)
    ctx['fvr_wiring'] = {k: v['wired'] for k, v in wiring.items()}

    for pid in ctx['hard']:
        if pid in grp_e.DEFERRED:
            continue  # E3/E5 需要全量 results，稍后统一评估
        fn = ORDER.get(pid)
        if not fn:
            ctx['results'][pid] = common.bad(pid, '无检查程序', 'ORDER 未登记')
            problems.append(f'{pid} 无检查器')
            continue
        try:
            ctx['results'][pid] = fn(ctx)
        except Exception as exc:  # 检查器自身异常按 escalate 记，不伪装 pass
            ctx['results'][pid] = common.esc(pid, f'检查器异常：{exc}', '需修复检查器')

    # 顺序依赖：E5 先（对已执行结果判三值域），E3 后（需 39 条 verdict 全在）。
    # E3 自身以占位 verdict 进入集合，随后被真实判定覆盖——这是 E3 自指的显式处置。
    ctx['results']['E3'] = common.esc('E3', '占位：等待全量结果', 'E3 自指占位')
    ctx['results']['E5'] = common.esc('E5', '占位：等待全量结果', 'E5 计数含自身')
    ctx['results']['E5'] = grp_e.DEFERRED['E5'](ctx)
    ctx['results']['E3'] = grp_e.DEFERRED['E3'](ctx)

    vals = {r['verdict'] for r in ctx['results'].values()}
    if not vals <= set(common.VERDICTS):
        problems.append(f'域外判定：{sorted(vals - set(common.VERDICTS))}')

    rows = [ctx['results'][p] for p in ctx['hard']]
    tz = timezone(timedelta(hours=8))
    out = {
        'run_id': 'fvr-full-run-1',
        'generated_at': datetime.now(tz).isoformat(timespec='seconds'),
        'mother_sha256': ctx['mother_sha'],
        'predicate_blocks': len(ctx['blocks']),
        'hard_property_source': 'regex ^\\s*([A-Z]\\d+):.*(——|—)\\s*硬 + hard-properties.snapshot.json',
        'snapshot_count': len(snap_ids),
        'executed_count': len(rows),
        'summary': {
            'pass': sum(r['verdict'] == 'pass' for r in rows),
            'fail': sum(r['verdict'] == 'fail' for r in rows),
            'escalate': sum(r['verdict'] == 'escalate' for r in rows),
            'vacuous': sum(bool(r['vacuous']) for r in rows),
        },
        'results': rows,
        'problems': problems,
    }
    path = pilot / 'fvr-full-run-1.json'
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"hard={len(ctx['hard'])}  executed={len(rows)}  blocks={len(ctx['blocks'])}  "
          f"pass={out['summary']['pass']} fail={out['summary']['fail']} "
          f"escalate={out['summary']['escalate']} vacuous={out['summary']['vacuous']}")
    for r in rows:
        print(f"  {r['property']:<4} {r['verdict']:<8} {'vacuous ' if r['vacuous'] else ''}{r['evidence'][:90]}")
    for p in problems:
        print('PROBLEM:', p)
    print('→', path)
    return 0 if not problems else 1


if __name__ == '__main__':
    raise SystemExit(main())
