#!/usr/bin/env python3
"""T 系列（方面 8 / 测试）硬性质检查器：T1 T4 T6。

2026-11-14 升级（D-B）：T4/T6 由「键是否存在」改为校验内容。
缺失数据源 → escalate；显式空集 → pass+vacuous；数据在案但不满足 → fail。
"""
from __future__ import annotations

from common import ok, bad, esc, domain_data


def t1(ctx):
    missing = [p for p in ctx['hard'] if p not in ctx['plan']]
    if missing:
        return bad('T1', f"方案未覆盖 {len(missing)} 条硬性质的检查手段：{missing[:8]}")
    return ok('T1', f"{len(ctx['hard'])} 条硬性质在方案 §4 均有检查手段／检查器组")


def t4(ctx):
    """每个单元都有非空测试集（单元目录以 module_inventory 为准，含入口单元）。"""
    units = domain_data(ctx, 'module_inventory')
    inv = domain_data(ctx, 'unit_test_inventory')
    if units is None or inv is None:
        return esc('T4', '域数据源未登记：白板无 module_inventory 或 unit_test_inventory',
                   '不可判：单元目录/测试清单未登记，测试集非空无从核验（非空真）')
    if not units:
        return ok('T4', 'module_inventory 显式空集：本部署无单元',
                  '空真：单元域为空，∀ 平凡为真', vacuous=True)
    suites = {}
    for row in inv or []:
        if row.get('unit') and row.get('test_files'):
            suites.setdefault(row['unit'], []).extend(row['test_files'])
    testless = [u.get('id', '?') for u in units if not suites.get(u.get('id'))]
    if testless:
        return bad('T4', f'{len(testless)}/{len(units)} 个单元无非空测试集：{testless}',
                   '入口单元按独立单元计（D-C）：无直测即不满足 ∀UNIT')
    return ok('T4', f'{len(units)} 个单元均有非空测试集（共 {sum(len(v) for v in suites.values())} 个测试文件）')


def t6(ctx):
    """已发布契约的契约测试在 CI 中执行。"""
    cons = domain_data(ctx, 'contract')
    if cons is None:
        return esc('T6', '域数据源未登记：白板无 contract 注册',
                   '不可判：契约未登记，契约测试执行无从核验（非空真）')
    published = [c for c in cons if c.get('lifecycle') == 'published']
    if not published:
        return ok('T6', '无已发布契约（生命周期域为空）',
                  '空真：无 published 契约，∀ 平凡为真', vacuous=True)
    tests = domain_data(ctx, 'contract_tests')
    if tests is None:
        return esc('T6', f'{len(published)} 份已发布契约存在，但白板无 contract_tests 登记',
                   '不可判：契约测试清单未登记（批 B 数据源）')
    covered = {r.get('contract'): r for r in (tests or [])}
    problems = []
    for c in published:
        r = covered.get(c.get('id'))
        if r is None or not r.get('file'):
            problems.append(f"{c.get('id')} 无契约测试")
        elif r.get('in_ci') is not True:
            problems.append(f"{c.get('id')} 的契约测试未在 CI 执行")
    if problems:
        return bad('T6', f'{len(problems)} 份契约的测试不满足：{problems}')
    return ok('T6', f'{len(published)} 份已发布契约的契约测试均在 CI 执行')


CHECKS = {'T1': t1, 'T4': t4, 'T6': t6}
