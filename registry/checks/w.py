#!/usr/bin/env python3
"""W 系列（方面 2 / 分解）硬性质检查器：W1 W2 W4 W7。"""
from __future__ import annotations

from common import ok, esc

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
    if 'owned_by(' not in ctx['whiteboard'] and 'data_owner' not in ctx['whiteboard']:
        return esc('W4', '域数据源未登记：白板无 owned_by 写入，但部署数据实体存在',
                   '不可判：数据所有权未登记，单一所有者无从核验（非空真）')
    return esc('W4', '白板存在数据所有权写入', '需人工核单一所有者')


def w7(ctx):
    adr = (ctx['root'] / 'pilot/vertical-slice-20261112')
    if not any('DECOMP' in p.name for p in adr.glob('ADR-*.md')):
        return ok('W7', '无分解主策略决策（DP-*-DECOMP 未启动）', '空真：主策略未选择', vacuous=True)
    return esc('W7', '存在分解主策略 ADR', '需人工核批准')


CHECKS = {'W1': w1, 'W2': w2, 'W4': w4, 'W7': w7}
