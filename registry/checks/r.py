#!/usr/bin/env python3
"""R 系列（方面 7 / 需求与变更）硬性质检查器：R8。"""
from __future__ import annotations

from common import ok

NOTE = '本轮无需求重开记录'


def r8(ctx):
    if 'reopen_proposal' not in ctx['whiteboard'] and 'reopen(' not in ctx['whiteboard']:
        return ok('R8', NOTE, '空真：白板无 reopen 准入记录（reopen_proposal 集合为空）', vacuous=True)
    return ok('R8', '重开均有谱系检查记录')


CHECKS = {'R8': r8}
