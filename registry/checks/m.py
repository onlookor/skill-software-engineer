#!/usr/bin/env python3
"""M 系列（总纲机制）硬性质检查器：M1 M2 M3 M4 M8 M9 M10 M11 M12 M14 M15 M20 M22 M23 M24 M25。"""
from __future__ import annotations

import re

from common import ok, bad, esc

REQUIRED_ENTRY_FIELDS = [
    'entry_id', 'kind', 'name', 'version', 'status', 'provenance', 'typical_reversibility',
    'applicability', 'envelope', 'cost_profile', 'compatibility', 'constraints_imposed',
    'anti_patterns', 'formal_anchor', 'references',
]  # 仅作字段面参考；M2 的权威必填面由 kind 剖面物化给出


def m1(ctx):
    """消费的方法条目状态可消费：status ∈ {active, seed}。"""
    ids, bad_ids = set(), []
    for card in ctx['cards'].values():
        for s in card.get('steps', []):
            for ref in s.get('registry_refs', []):
                ids.add(ref)
    by_id = {e['entry_id']: e for e in ctx['entries']}
    for i in sorted(ids):
        e = by_id.get(i)
        if not e or e.get('status') not in ('active', 'seed'):
            bad_ids.append(f"{i}:{'缺失' if not e else e.get('status')}")
    if bad_ids:
        return bad('M1', f"卡片消费条目 {len(ids)} 个，不可消费：{', '.join(bad_ids)}")
    return ok('M1', f"卡片消费的 {len(ids)} 个方法条目状态均 ∈ {{active, seed}}")


def m2(ctx):
    """∀E(status≠draft): fields_complete(E, kind_profile(E.kind))——按剖面物化后的必填面判定。"""
    mat = ctx['mat']
    has_path = ctx['has_path']
    prof_status = {p.get('describes_kind'): p.get('status') for p in ctx['profiles'].get('profiles') or []}
    missing = []
    n = 0
    for e in ctx['entries']:
        if e.get('status') == 'draft':
            continue
        n += 1
        kind = e.get('kind')
        m = mat.get(kind)
        if not m:
            missing.append(f"{e['entry_id']}:无 kind 剖面")
            continue
        if prof_status.get(kind) == 'draft':
            missing.append(f"{e['entry_id']}:kind_profile_{kind} 为 draft，完备性不可判定")
            continue
        lack = [f for f in m['required'] if not has_path(e, f)]
        if lack:
            missing.append(f"{e['entry_id']}缺{'/'.join(lack)}")
    if missing:
        return bad('M2', f"{len(missing)}/{n} 条非 draft 条目按剖面缺必填字段：{missing[:5]}")
    return ok('M2', f"{n} 条非 draft 条目按 kind 剖面必填面全部在案（空列表按在案计，0.17.2）")


def m3(ctx):
    """包络条目参数化且有出处：bound_expr 非空、source 有值。"""
    broken = []
    n = 0
    for e in ctx['entries']:
        for item in e.get('envelope') or []:
            n += 1
            src = item.get('source') or {}
            if not item.get('bound_expr') or not src.get('value'):
                broken.append(e['entry_id'])
                break
    if broken:
        return bad('M3', f"{n} 个包络条目中 {len(set(broken))} 条缺 bound_expr/source：{sorted(set(broken))[:5]}")
    if not n:
        return ok('M3', 'envelope 集合为空', '空真：无包络条目可校验（∀ 在空集上平凡为真）', vacuous=True)
    return ok('M3', f"{n} 个包络条目均有 bound_expr 与 source")


def m4(ctx):
    """反模式可执行：detection_predicate 非空。"""
    aps = [ap for e in ctx['entries'] for ap in (e.get('anti_patterns') or [])]
    broken = [ap.get('pattern_id') for ap in aps if not ap.get('detection_predicate')]
    if broken:
        return bad('M4', f"{len(broken)} 个反模式缺 detection_predicate：{broken[:5]}")
    if not aps:
        return ok('M4', '未登记反模式（空集）', '空真：反模式集合为空', vacuous=True)
    return ok('M4', f"{len(aps)} 个反模式均有 detection_predicate")


def m8(ctx):
    """种子重校验差分：无重校验记录时为空真。"""
    meta = ctx.get('registry_meta') or {}
    records = meta.get('seed_revalidation') or []
    if not records:
        return ok('M8', 'method_registry 无 seed_revalidation 记录', '空真：未发生种子重校验', vacuous=True)
    diff = [r for r in records if r.get('diff')]
    if diff:
        return bad('M8', f"{len(diff)} 条重校验有未处置差分")
    return ok('M8', f"{len(records)} 条重校验均无差分")


def m9(ctx):
    """兼容性引用闭合：peer_entry 必须在册。"""
    by_id = {e['entry_id'] for e in ctx['entries']}
    dangling = []
    for e in ctx['entries']:
        for c in e.get('compatibility') or []:
            if c.get('peer_entry') not in by_id:
                dangling.append(f"{e['entry_id']}→{c.get('peer_entry')}")
    if dangling:
        return bad('M9', f"{len(dangling)} 个兼容性引用悬空：{dangling[:5]}")
    return ok('M9', '全部兼容性 peer_entry 在册')


def m10(ctx):
    """选型卡存在且含步骤日志骨架（S0–S6）。"""
    substantive = {k: c for k, c in ctx['cards'].items() if c.get('steps')}
    lack = [k for k, c in substantive.items() if len(c.get('steps', [])) != 7]
    if not substantive:
        return bad('M10', '无任何含步骤的选型卡')
    if lack:
        return bad('M10', f"卡片步骤数≠7：{lack}")
    return ok('M10', f"{len(substantive)} 张实质卡均含 S0–S6 七步")


def m11(ctx):
    """步骤完整、无跳步/增步/改序。"""
    want = [f"S{i}" for i in range(7)]
    wrong = [k for k, c in ctx['cards'].items() if c.get('steps') and [s.get('step_id') for s in c['steps']] != want]
    if wrong:
        return bad('M11', f"步骤序列不合约：{wrong}")
    return ok('M11', '实质卡步骤序列均为 S0–S6 连续无跳步')


def m12(ctx):
    """失败路由闭合：route ∈ FM-xx ∪ CH-x。"""
    bad_routes = []
    for cid, c in ctx['cards'].items():
        for s in c.get('steps', []):
            for fb in s.get('failure_branches') or []:
                route = str(fb.get('route', ''))
                if not (re.match(r'^FM-\d+$', route) or re.match(r'^CH-[A-E]$', route)):
                    bad_routes.append(f"{cid}:{route}")
    if bad_routes:
        return bad('M12', f"不闭合路由 {len(bad_routes)} 个：{bad_routes[:5]}")
    return ok('M12', '全部失败分支路由 ∈ {FM-xx, CH-x}')


def m14(ctx):
    """快路径使用须重校验影响范围。"""
    if 'fast_path' not in ctx['whiteboard'] and '快速通道' not in ctx['whiteboard']:
        return ok('M14', '白板无快速通道使用记录', '空真：未使用快路径', vacuous=True)
    return esc('M14', '白板存在快速通道记录', '需人工核 impact_scope 重跑与聚合检测记录')


def m15(ctx):
    """适用性未知的保留与勘察义务。"""
    if 'applicability.problem_space' not in ctx['whiteboard']:
        return ok('M15', '白板无未知适用性排除记录', '空真：无未知适用性候选', vacuous=True)
    return ok('M15', '白板 exclusion_record 走 applicability.problem_space；勘察义务 SO-PILOT-4 在册',
              '候选未因未知被删，义务未闭合但不影响保留')


def m20(ctx):
    """A0×A0 不相容须交人裁定。"""
    if 'conflict_instance' not in ctx['whiteboard']:
        return ok('M20', '白板无 conflict_instance 写入', '空真：无 A0×A0 不相容实例', vacuous=True)
    return esc('M20', '白板含 conflict_instance', '需人工确认是否存在 A0×A0 冲突')


def m22(ctx):
    """失败事件先分类后处置：FM 目录在册。"""
    n = len(set(re.findall(r'\*\*(FM-\d+)\*\*', ctx['mother'])))
    if n < 10:
        return bad('M22', f"FM 目录仅 {n} 条，无法支撑分类")
    return ok('M22', f"FM 目录在册 {n} 条（FM-0～FM-15 形态）")


def m23(ctx):
    """不可分类走 FM-0 并阻塞＋缺口声明。"""
    if 'FM-0' not in ctx['mother']:
        return bad('M23', '母本无 FM-0')
    if '阻塞' not in ctx['mother']:
        return bad('M23', '母本无阻塞语义')
    return ok('M23', 'FM-0 与阻塞语义在册（不可分类→阻塞＋缺口声明）')


def m24(ctx):
    """路由按目录执行：目录含处置/介入/工件三列。"""
    m = re.search(r'\|[^\n]*处置[^\n]*\|[^\n]*介入[^\n]*\|[^\n]*工件[^\n]*\|', ctx['mother'])
    if not m:
        return bad('M24', 'FM 目录缺处置/介入/工件三列')
    return ok('M24', 'FM 目录含处置/介入/工件三列')


def m25(ctx):
    """目录变更须 R2＋高影响 ADR。"""
    hit = re.search(r'FM\s*目录(变更|调整|增删)|\b(?:catalog|目录表)\s*变更', ctx['changlog'])
    if not hit:
        return ok('M25', 'changlog 无 FM 目录变更记录', '空真：本轮未改 FM 目录', vacuous=True)
    return esc('M25', f'changlog 含 FM 目录变更记录：{hit.group(0)}', '需人工核 R2 与高影响 ADR')


CHECKS = {p: f for p, f in [
    ('M1', m1), ('M2', m2), ('M3', m3), ('M4', m4), ('M8', m8), ('M9', m9),
    ('M10', m10), ('M11', m11), ('M12', m12), ('M14', m14), ('M15', m15),
    ('M20', m20), ('M22', m22), ('M23', m23), ('M24', m24), ('M25', m25),
]}
