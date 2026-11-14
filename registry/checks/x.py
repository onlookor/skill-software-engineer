#!/usr/bin/env python3
"""X 系列（方面 3 / 交互与契约）硬性质检查器：X1 X2 X5 X6。

2026-11-14 升级（D-B）：由「键是否存在」改为校验内容。
缺失数据源 → escalate；显式空集 → pass+vacuous；数据在案但不满足 → fail。
"""
from __future__ import annotations

import re

from common import ok, bad, esc, domain_data, target_repo

PILOT = 'pilot/vertical-slice-20261112'


def _contracts(ctx):
    return domain_data(ctx, 'contract')


def _adr_state(ctx, name: str):
    """ADR 先按 target_repo 解析（契约归属仓），再回退 pilot 目录。"""
    candidates = []
    repo = target_repo(ctx)
    if repo is not None:
        candidates.append(repo / name)
    candidates.append(ctx['root'] / PILOT / name)
    for p in candidates:
        if p.is_file():
            m = re.search(r'决策记录状态：\*\*`([a-z_]+)`\*\*', p.read_text(encoding='utf-8'))
            return m.group(1) if m else None
    return None


def x1(ctx):
    """每条 connects 都被已登记契约覆盖（provider/consumer 同时命中）。"""
    conns = domain_data(ctx, 'connects')
    if conns is None:
        return esc('X1', '域数据源未登记：本部署有交互面，但白板无 connects 写入',
                   '不可判：交互未登记，契约覆盖无从核验（非空真）')
    if not conns:
        return ok('X1', 'connects 显式空集：无跨单元交互需契约覆盖',
                  '空真：交互域为空，∀ 平凡为真', vacuous=True)
    cons = _contracts(ctx)
    if cons is None:
        return esc('X1', f'{len(conns)} 条 connects 已登记，但无 contract 注册',
                   '不可判：契约集未登记，覆盖关系无从核验')
    if not cons:
        return bad('X1', f'{len(conns)} 条 connects 存在但契约集为空')
    uncovered = []
    for c in conns:
        ok_cover = any(c.get('to') == ct.get('provider')
                       and c.get('from') in (ct.get('consumers') or [])
                       for ct in cons)
        if not ok_cover:
            uncovered.append(f"{c.get('from')}→{c.get('to')}")
    if uncovered:
        return bad('X1', f'{len(uncovered)} 条 connects 无契约覆盖：{uncovered}')
    return ok('X1', f'{len(conns)} 条 connects 均被已登记契约（provider＋consumer 命中）覆盖')


def x2(ctx):
    """每份已登记契约都有版本与兼容策略。"""
    cons = _contracts(ctx)
    if cons is None:
        return esc('X2', '域数据源未登记：白板无 contract 注册',
                   '不可判：契约未登记，版本/兼容策略无从核验（非空真）')
    if not cons:
        return ok('X2', 'contract 显式空集：无对外契约',
                  '空真：契约域为空，∀ 平凡为真', vacuous=True)
    missing = [c.get('id', '?') for c in cons
               if not c.get('version') or not c.get('compat_policy')]
    if missing:
        return bad('X2', f'{len(missing)} 份契约缺 version 或 compat_policy：{missing}')
    return ok('X2', f'{len(cons)} 份契约均带 version 与 compat_policy')


def x5(ctx):
    """已发布契约必须有已批准 ADR。"""
    cons = _contracts(ctx)
    if cons is None:
        return esc('X5', '域数据源未登记：白板无 contract 注册',
                   '不可判：契约未登记，生命周期批准无从核验（非空真）')
    published = [c for c in cons if c.get('lifecycle') == 'published']
    if not published:
        return ok('X5', '无已发布契约（生命周期域为空）',
                  '空真：无 published 契约，∀ 平凡为真', vacuous=True)
    bad_rows = []
    for c in published:
        adr = c.get('adr')
        if not adr:
            bad_rows.append(f"{c.get('id')} 无 ADR")
            continue
        state = _adr_state(ctx, adr)
        if state != 'approved':
            bad_rows.append(f"{c.get('id')} 的 ADR {adr} 状态={state}")
    if bad_rows:
        return bad('X5', f'{len(bad_rows)} 份已发布契约缺已批准 ADR：{bad_rows}')
    return ok('X5', f'{len(published)} 份已发布契约均有已批准 ADR')


def x6(ctx):
    """共享数据访问须满足 3.2.3 四条件并显式记录；显式空集记 vacuous。"""
    rows = domain_data(ctx, 'shared_data_access')
    if rows is None:
        return esc('X6', '域数据源未登记：白板无 shared_data_access 写入',
                   '不可判：共享数据访问未登记，四条件无从核验（非空真）')
    if not rows:
        return ok('X6', 'shared_data_access 显式空集：本部署无跨单元共享数据',
                  '空真：共享数据域为空（D-C 裁定按 vacuous，不记 pass 实质）', vacuous=True)
    need = ('weak_coupling', 'read_only_or_single_writer',
            'no_cross_unit_transaction', 'via_data_contract')
    bad_rows = []
    for r in rows:
        conds = r.get('conditions') or {}
        miss = [k for k in need if conds.get(k) is not True]
        if miss:
            bad_rows.append(f"{r.get('id', '?')} 缺/未满足 {miss}")
    if bad_rows:
        return bad('X6', f'{len(bad_rows)} 条共享数据访问未满足四条件：{bad_rows}')
    return ok('X6', f'{len(rows)} 条共享数据访问均满足 3.2.3 四条件并已记录')


CHECKS = {'X1': x1, 'X2': x2, 'X5': x5, 'X6': x6}
