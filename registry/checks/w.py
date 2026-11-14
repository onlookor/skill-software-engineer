#!/usr/bin/env python3
"""W 系列（方面 2 / 分解）硬性质检查器：W1 W2 W4 W7。"""
from __future__ import annotations

from common import ok, esc, domain_data

NOTE = '域数据源未登记：本部署有模块，但白板无 module_inventory（不是空集）'


def w1(ctx):
    if 'module_inventory' not in ctx['whiteboard']:
        return esc('W1', NOTE, '不可判：模块目录未登记，接缝封闭无从核验（非空真）')
    return esc('W1', '存在 module_inventory', '需人工核接缝封闭')


def w2(ctx):
    if 'module_inventory' not in ctx['whiteboard']:
        return esc('W2', NOTE, '不可判：模块目录未登记，可独立验证无从核验（非空真）')
    return esc('W2', '存在 module_inventory', '需人工核可独立验证')


def w4(ctx):
    entries = domain_data(ctx, 'owned_by')
    if entries is None:
        if 'owned_by(' not in ctx['whiteboard'] and 'data_owner' not in ctx['whiteboard']:
            return esc('W4', '域数据源未登记：白板无 owned_by 写入，但部署数据实体存在',
                       '不可判：数据所有权未登记，单一所有者无从核验（非空真）')
        return esc('W4', '白板存在数据所有权写入', '需人工核单一所有者')
    if not entries:
        return esc('W4', 'owned_by 显式空集', '不可判：本部署存在数据实体，所有权不得为空')
    pairs = '；'.join(f"{e.get('owner')}→{e.get('object')}({e.get('right')})" for e in entries)
    for e in entries:
        r = e.get('human_review') or {}
        if r.get('approver_kind') != 'human' or not r.get('approved_by'):
            return esc('W4', f"已登记 {len(entries)} 条所有权：{pairs}",
                       '所有权已登记，但缺人类确认记录；需人工核单一所有者')
    first = entries[0].get('human_review') or {}
    return ok('W4',
              f"单一所有者经人类确认（{first.get('approved_by')}，{first.get('approved_at')}）：{pairs}",
              '人工核结论，非机械校验：归属由人确认；已与 V1 打包为将来机械校验升级项')


def w7(ctx):
    adr = (ctx['root'] / 'pilot/vertical-slice-20261112')
    if not any('DECOMP' in p.name for p in adr.glob('ADR-*.md')):
        return ok('W7', '无分解主策略决策（DP-*-DECOMP 未启动）', '空真：主策略未选择', vacuous=True)
    return esc('W7', '存在分解主策略 ADR', '需人工核批准')


CHECKS = {'W1': w1, 'W2': w2, 'W4': w4, 'W7': w7}
