#!/usr/bin/env python3
"""W 系列（方面 2 / 分解）硬性质检查器：W1 W2 W4 W7。"""
from __future__ import annotations

import re

from common import ok, bad, esc, domain_data, source_files

NOTE = '域数据源未登记：本部署有模块，但白板无 module_inventory（不是空集）'

WRITE_CALL_RE = re.compile(
    r'\b(?:appendFileSync|writeFileSync|appendFile|writeFile|createWriteStream)\s*\(')
CLASS_RE = re.compile(r'\bclass\s+([A-Za-z_$][\w$]*)')
NEW_RE = re.compile(r'\bnew\s+([A-Za-z_$][\w$]*)\s*\(')


def w1(ctx):
    """每个模块的接缝封闭（人工核结论，2026-11-14 人类裁定方案 A）。"""
    if domain_data(ctx, 'module_inventory') is None:
        return esc('W1', NOTE, '不可判：模块目录未登记，接缝封闭无从核验（非空真）')
    reviews = domain_data(ctx, 'human_review') or []
    for r in reviews:
        if r.get('property') != 'W1':
            continue
        if r.get('approver_kind') != 'human' or not r.get('approved_by') or not r.get('conclusion'):
            return esc('W1', '存在 W1 人工核记录，但缺批准人或结论文本',
                       '不可判：人工核记录不完整')
        return ok('W1', r['conclusion'],
                  f"人工核结论，非机械校验：{r.get('approved_by')} 于 {r.get('approved_at')} 确认")
    return esc('W1', '存在 module_inventory，但无 W1 人工核结论', '需人工核接缝封闭')


def w2(ctx):
    """每个单元可独立验证：以「单元是否有自己的测试文件」为机械口径。"""
    units = domain_data(ctx, 'module_inventory')
    inv = domain_data(ctx, 'unit_test_inventory')
    if units is None or inv is None:
        return esc('W2', NOTE, '不可判：模块目录/测试清单未登记，可独立验证无从核验（非空真）')
    suites = {}
    for row in inv or []:
        if row.get('unit') and row.get('test_files'):
            suites.setdefault(row['unit'], []).extend(row['test_files'])
    untestable = [u.get('id', '?') for u in units if not suites.get(u.get('id'))]
    if untestable:
        return bad('W2', f'{len(untestable)}/{len(units)} 个单元无独立测试，不可独立验证：{untestable}')
    return ok('W2', f'{len(units)} 个单元均有独立测试文件，可独立验证')


def w4(ctx):
    """每个数据实体单一所有者：机械核对源码写点与创建点。"""
    entries = domain_data(ctx, 'owned_by')
    if entries is None:
        return esc('W4', '域数据源未登记：白板无 owned_by 写入',
                   '不可判：数据所有权未登记，单一所有者无从核验（非空真）')
    if not entries:
        return esc('W4', 'owned_by 显式空集', '不可判：本部署存在数据实体，所有权不得为空')

    files, why = source_files(ctx)
    if files is None:
        return esc('W4', why, '不可判：无法读取目标仓库源码，机械校验不成立')

    texts = {unit: p.read_text(encoding='utf-8') for unit, p in files}
    units = set(texts)
    for e in entries:
        if e.get('owner') not in units:
            return esc('W4', f"所有权登记 owner={e.get('owner')} 不在 module_inventory",
                       '不可判：所有者不是已登记单元，机械核对无基准')

    classes_in = {unit: set(CLASS_RE.findall(text)) for unit, text in texts.items()}
    problems, evidence = [], []
    for e in entries:
        owner, obj, right = e.get('owner'), e.get('object'), e.get('right')
        if not owner or not obj or right not in ('write', 'create_and_configure'):
            return esc('W4', f'所有权条目缺字段或 right 非法：{e}', '不可判：登记不完整')

        writers = [u for u, t in texts.items() if obj in t and WRITE_CALL_RE.search(t)]
        if not writers:
            return esc('W4', f'源码中未定位到 {obj} 的写点', '不可判：机械核对缺证据')

        if right == 'write':
            if len(writers) != 1 or writers[0] != owner:
                problems.append(f'{obj} 写点={writers}，登记 write owner={owner}')
            else:
                evidence.append(f'{obj} 唯一写点 {owner}')
            continue

        sink_classes = set().union(*(classes_in[u] for u in writers))
        creators = [u for u, t in texts.items() if set(NEW_RE.findall(t)) & sink_classes]
        if owner in writers:
            problems.append(f'{owner} 同时持 {obj} 的写入权与创建/配置权')
        elif len(creators) != 1 or creators[0] != owner:
            problems.append(f'{obj} 创建点={creators}，登记 create owner={owner}')
        else:
            evidence.append(f'{obj} 唯一创建点 {owner}（构造 {sorted(sink_classes)}）')

    if problems:
        return bad('W4', f'机械核对不通过：{problems}', '源码写点/创建点与登记不一致')
    return ok('W4', f'机械校验：{len(entries)} 条所有权与源码写点一致（{"；".join(evidence)}）')


def w7(ctx):
    adr = (ctx['root'] / 'pilot/vertical-slice-20261112')
    if not any('DECOMP' in p.name for p in adr.glob('ADR-*.md')):
        return ok('W7', '无分解主策略决策（DP-*-DECOMP 未启动）', '空真：主策略未选择', vacuous=True)
    return esc('W7', '存在分解主策略 ADR', '需人工核批准')


CHECKS = {'W1': w1, 'W2': w2, 'W4': w4, 'W7': w7}
