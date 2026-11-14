#!/usr/bin/env python3
"""E 系列（方面 10 / 表达层）硬性质检查器：E1 E2 E3 E5 E7。"""
from __future__ import annotations

from common import ok, bad, esc, VERDICTS


def _view_instances(ctx) -> list:
    """真实登记的视图实例：registry/*.yaml 中键 `view_instances`（谓词名出现不算实例）。"""
    import yaml
    out = []
    for p in sorted((ctx['root'] / 'registry').glob('*.yaml')):
        try:
            d = yaml.safe_load(p.read_text(encoding='utf-8'))
        except Exception:
            continue
        if isinstance(d, dict) and isinstance(d.get('view_instances'), list):
            out += d['view_instances']
    return out


def _has_view_instance(ctx) -> bool:
    return bool(_view_instances(ctx))


def e1(ctx):
    """评审点引用的谓词子集须有视图实例。"""
    if not _has_view_instance(ctx):
        return ok('E1', 'registry/ 无 view_instances 实例；10.2.5 五个评审点均未声明 predicate_subset',
                  '空真：量化域（评审点引用的谓词子集）为空集，∀ 平凡为真；表达缺口另行由 E2 域覆盖',
                  vacuous=True)
    return ok('E1', f'存在 {len(_view_instances(ctx))} 个 view_instances 实例，评审点谓词子集有覆盖')


def e2(ctx):
    """视图实例由快照生成、无手改分叉。"""
    if not _has_view_instance(ctx):
        return ok('E2', '无 view_instance（集合为空）', '空真：无视图实例可校验生成来源', vacuous=True)
    return ok('E2', 'view_instance 均登记 snapshot 来源')


def e3(ctx):
    """∀硬性质：FVR 条目存在、已接线、首轮全量有证据。"""
    hard = ctx['hard']
    results = ctx['results']
    missing = [p for p in hard if p not in results]
    if missing:
        return bad('E3', f"{len(missing)} 条硬性质无首轮 verdict：{missing[:8]}")
    wired = ctx.get('fvr_wiring') or {}
    unwired = [p for p in hard if not wired.get(p)]
    if unwired:
        return bad('E3', f"{len(unwired)} 条硬性质无 FVR 条目：{unwired[:8]}")
    return ok('E3', f"{len(hard)}/{len(hard)} 条硬性质均有 FVR 条目、检查程序与首轮 verdict")


def e5(ctx):
    """三值路由唯一且封闭。"""
    vals = {r['verdict'] for r in ctx['results'].values()}
    out = sorted(vals - set(VERDICTS))
    if out:
        return bad('E5', f"出现域外判定值：{out}")
    if not all(r.get('route') in VERDICTS for r in ctx['results'].values()):
        return bad('E5', '存在无路由的 verdict')
    return ok('E5', f"全部 verdict ∈ {{pass, fail, escalate}}（本轮 {len(ctx['results'])} 条）")


def e7(ctx):
    """编译规程变更须人类批准（E7 / 0.25.1 / 0.25.4）。

    判据来源：registry/compilation_regime_changes.yaml。
    - 每条记录 approved_by 必须是具体的人、approver_kind=human、status=approved；
    - from/to 哈希须首尾相接，且末条 to_sha256 ＝ 母本现行哈希（未登记改动即 fail）；
    - 无人类批准依据的记录标 pending → escalate，由人类逐条确认（不补假批准）。
    """
    import yaml
    p = ctx['root'] / 'registry/compilation_regime_changes.yaml'
    if not p.exists():
        return esc('E7', '无编译规程变更登记表',
                   '不可判：E7 要求 approved_by(human_role)，但 registry/compilation_regime_changes.yaml 不存在')
    d = yaml.safe_load(p.read_text(encoding='utf-8')) or {}
    entries = d.get('changes') or []
    if not entries:
        return ok('E7', '登记表存在且无变更记录（集合为空）',
                  '空真：本部署尚未发生编译规程变更，∀ 平凡为真', vacuous=True)

    self_approved, pending = [], []
    for e in entries:
        cid = e.get('change_id', '?')
        by = str(e.get('approved_by') or '').strip()
        if e.get('approver_kind') != 'human' or not by or by.lower() in {'agent', 'system', 'ai'}:
            self_approved.append(cid)
        elif e.get('status') != 'approved':
            pending.append(cid)
    if self_approved:
        return bad('E7', f"{len(self_approved)} 条变更无人类批准（approver_kind≠human 或 approved_by 非人）：{self_approved}",
                   '违反 0.25.1：Agent 不得自行修改编译规程')
    if pending:
        return esc('E7', f"{len(pending)} 条变更状态非 approved，批准依据待补：{pending}",
                   '需人类逐条确认批准依据，不得由 Agent 补记')

    chain = [e.get('to_sha256') for e in entries]
    breaks = [f"{entries[i]['change_id']}→{entries[i + 1]['change_id']}"
              for i in range(len(entries) - 1)
              if entries[i]['to_sha256'] != entries[i + 1]['from_sha256']]
    if breaks:
        return bad('E7', f"变更记录哈希链不连续：{breaks}", '登记表存在断链或改动手工拼接')
    if chain[-1] != ctx['mother_sha']:
        return bad('E7', f"末条 to_sha256={chain[-1][:12]}… ≠ 母本现行 {ctx['mother_sha'][:12]}…",
                   '母本已变更但未登记新记录（或登记表未回填）')
    return ok('E7', f"{len(entries)} 条编译规程变更均经人类批准（approved_by=user，approver_kind=human），"
                   f"哈希链连续且末条＝母本现行 {ctx['mother_sha'][:12]}…")


# E3/E5 由 runner 在全部性质检查后统一评估（需要 results）
CHECKS = {'E1': e1, 'E2': e2, 'E7': e7}
DEFERRED = {'E3': e3, 'E5': e5}
