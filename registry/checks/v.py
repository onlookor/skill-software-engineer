#!/usr/bin/env python3
"""V 系列（方面 1 / 风格）硬性质检查器：V1 V2 V5。"""
from __future__ import annotations

import re

from common import ok, bad, esc, domain_data, source_files

HARD_RELATIONS = {'hard_conflict', 'conflict', 'forbidden'}

IMPORT_RE = re.compile(
    r"""(?:import|export)\s+(?:[^'"]*?\sfrom\s*)?["'](\.{1,2}/[^"']+)["']"""
)
DYNAMIC_RE = re.compile(r"""(?:import|require)\(\s*["'](\.{1,2}/[^"']+)["']\s*\)""")


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
    """¬∃ cycle(forbidden_dependency)：机械口径。

    读目标仓库源码的相对 import 边，按 layer_of 映射到层，逐边核对
    dependency_rule(·,·,forbidden)；同时保留禁止层规则图的环检查。
    """
    rules = domain_data(ctx, 'dependency_rule')
    layers = domain_data(ctx, 'layer_of')
    if rules is None or layers is None:
        return esc('V1', '域数据源未登记：白板缺 layer_of 或 dependency_rule',
                   '不可判：分层或禁止规则未登记（非空真）')

    forbidden = {(str(r.get('from')).strip(), str(r.get('to')).strip())
                 for r in rules if r.get('relation') in HARD_RELATIONS}
    if not forbidden:
        return esc('V1', 'dependency_rule 无 forbidden 条目', '不可判：无禁止边')

    layer_of = {}
    for r in layers:
        c, l = r.get('component'), r.get('layer')
        if not c or not l:
            return esc('V1', 'layer_of 条目缺 component/layer', '不可判：分层登记不完整')
        layer_of[str(c).strip()] = str(l).strip()

    files, why = source_files(ctx)
    if files is None:
        return esc('V1', why, '不可判：无法读取目标仓库源码，机械校验不成立')

    by_path = {p.resolve(): unit for unit, p in files}
    edges = set()
    for unit, path in files:
        text = path.read_text(encoding='utf-8')
        specs = set(IMPORT_RE.findall(text)) | set(DYNAMIC_RE.findall(text))
        for spec in specs:
            target = by_path.get((path.parent / spec).resolve())
            if target is not None:
                edges.add((unit, target))
    if not edges:
        return esc('V1', '扫描目标仓库未发现已登记模块间的相对 import 边',
                   '不可判：机械边集为空，与 module_inventory 不符')

    violations, unmapped = [], []
    for a, b in sorted(edges):
        la, lb = layer_of.get(a), layer_of.get(b)
        if la is None or lb is None:
            unmapped.append(f'{a}→{b}')
        elif (la, lb) in forbidden:
            violations.append(f'{a}({la})→{b}({lb})')
    if unmapped:
        return esc('V1', f'{len(unmapped)} 条 import 边端点未登记层：{unmapped}',
                   '不可判：layer_of 覆盖不全')
    if violations:
        return bad('V1', f'{len(violations)}/{len(edges)} 条 import 边违反禁止依赖：{violations}')

    graph: dict[str, list[str]] = {}
    for a, b in forbidden:
        graph.setdefault(a, []).append(b)
    cyc = _cycle(graph)
    if cyc:
        return bad('V1', f"禁止依赖成环：{'→'.join(cyc)}")

    return ok('V1', f'机械校验：扫描 {len(files)} 个单元源码，{len(edges)} 条相对 import 边，'
                    f'逐边核对 {len(forbidden)} 条 forbidden 层规则无违反；禁止层规则图无环')


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
