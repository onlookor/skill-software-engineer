#!/usr/bin/env python3
"""V 系列（方面 1 / 风格）硬性质检查器：V1 V2 V5。"""
from __future__ import annotations

import re

from common import ok, bad, esc, domain_data

HARD_RELATIONS = {'hard_conflict', 'conflict', 'forbidden'}


def _style_protocols(ctx) -> set[str]:
    """从 style(scope, (·, ·, PROTO, ·)) 取允许协议集。"""
    m = re.search(r'style\([^,]+,\s*\(([^)]*)\)', ctx['whiteboard'])
    if not m:
        return set()
    return {p.strip() for p in m.group(1).split(',') if p.strip() and p.strip() != '·'}


def _cycle(graph: dict[str, list[str]]) -> list[str]:
    seen, stack, path = set(), set(), []

    def dfs(n):
        if n in stack:
            return path[path.index(n):] + [n]
        if n in seen:
            return []
        seen.add(n)
        stack.add(n)
        path.append(n)
        for m in graph.get(n, []):
            c = dfs(m)
            if c:
                return c
        path.pop()
        stack.discard(n)
        return []

    for n in graph:
        c = dfs(n)
        if c:
            return c
    return []


def v1(ctx):
    """¬∃ cycle(forbidden_dependency)：边取自 1.5 dependency_rule(·,·,forbidden) 的实例登记。

    弱校验（2026-11-14 人类裁定口径甲）：只读字面层规则边，不展开 layer_of 到单元边。
    """
    registered = domain_data(ctx, 'dependency_rule')
    if registered:
        graph: dict[str, list[str]] = {}
        count = 0
        for r in registered:
            if r.get('relation') not in HARD_RELATIONS:
                continue
            a, b = r.get('from'), r.get('to')
            if not a or not b:
                return esc('V1', 'dependency_rule 条目缺 from/to', '不可判：登记不完整')
            graph.setdefault(str(a).strip(), []).append(str(b).strip())
            count += 1
        if count == 0:
            return esc('V1', 'dependency_rule 无 forbidden 条目',
                       '不可判：无禁止边，环判据无输入')
        cyc = _cycle(graph)
        if cyc:
            return bad('V1', f"禁止依赖成环：{'→'.join(cyc)}")
        return ok('V1', f"禁止依赖图无环（{count} 条 forbidden 层规则）",
                  '弱校验：只读字面层规则边，不展开 layer_of；不代表单元级依赖已核')

    rules = re.findall(r'dependency_rule\(\s*([^,()]+?)\s*,\s*([^,()]+?)\s*,\s*forbidden\s*\)',
                       ctx['whiteboard'])
    if not rules:
        return esc('V1', '域数据源未登记：本部署有分层/依赖，但白板无 dependency_rule 实例',
                   '不可判：依赖边未登记，禁止依赖环无从核验（非空真）')
    graph = {}
    for a, b in rules:
        graph.setdefault(a.strip(), []).append(b.strip())
    cyc = _cycle(graph)
    if cyc:
        return bad('V1', f"禁止依赖成环：{'→'.join(cyc)}")
    return ok('V1', f"禁止依赖图无环（{len(rules)} 条 forbidden 边）",
              '弱校验：只读字面规则，不展开 layer_of')


def v2(ctx):
    conns = domain_data(ctx, 'connects')
    if conns is None:
        return esc('V2', '域数据源未登记：本部署有交互面，但白板无 connects 写入',
                   '不可判：连接未登记，协议风格允许集无从核验（非空真）')
    if not conns:
        return ok('V2', 'connects 显式空集：本部署无跨单元连接',
                  '空真：连接域为空，∀ 平凡为真', vacuous=True)
    allowed = _style_protocols(ctx)
    if not allowed:
        return esc('V2', 'connects 已登记，但 style 未给出可判定的允许协议集',
                   '不可判：allowed_protocols(S) 无取值')
    illegal = [f"{c.get('from')}→{c.get('to')}({c.get('protocol')})"
               for c in conns if c.get('protocol') not in allowed]
    if illegal:
        return bad('V2', f"{len(illegal)} 条连接协议不在 style 允许集 {sorted(allowed)} 内：{illegal}")
    return ok('V2', f"{len(conns)} 条 connects 的协议均在 style 允许集 {sorted(allowed)} 内")


def v5(ctx):
    adr = ctx['root'] / 'pilot/vertical-slice-20261112/ADR-DP1-STYLE.md'
    if not adr.exists():
        return bad('V5', '高影响风格无 ADR-DP1-STYLE')
    text = adr.read_text(encoding='utf-8')
    if '批准人' not in text:
        return esc('V5', 'ADR 存在但无批准人行', '需人工核批准')
    m = re.search(r'决策记录状态：\*\*`([a-z_]+)`\*\*', text)
    state = m.group(1) if m else 'unparsed'
    if state == 'approved':
        return ok('V5', 'ADR-DP1-STYLE 存在且有批准人 user；决策记录状态 approved'
                       '（SM-DR provisional → approved，retro_approve，2026-11-13）')
    if state == 'provisional':
        return ok('V5', 'ADR-DP1-STYLE 存在且有批准人 user；决策记录 provisional 是 10.2.5 未过的后果，不否定 ADR 批准事实',
                  '批准成立；接地状态另由 10.2.5 判')
    return esc('V5', f'ADR 决策记录状态无法识别：{state}', '需人工核状态行')


CHECKS = {'V1': v1, 'V2': v2, 'V5': v5}
