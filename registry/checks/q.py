#!/usr/bin/env python3
"""Q 系列（方面 6 / 质量目标）硬性质检查器：Q1。"""
from __future__ import annotations

from common import ROOT, load_yaml, ok, bad

SIX = ['stimulus_source', 'stimulus', 'artifact', 'environment', 'response', 'response_measure']


def q1(ctx):
    p = ROOT / 'pilot/vertical-slice-20261112/target-set-pact-dsh.yaml'
    if not p.exists():
        return bad('Q1', '目标集文件缺失')
    d = load_yaml(p).get('target_set') or {}
    broken = []
    hard_goals = [g for g in d.get('goals') or [] if g.get('hard')]
    for g in hard_goals:
        se = g.get('six_elements') or {}
        lack = [k for k in SIX if not se.get(k)]
        if lack or not g.get('unit') or not g.get('target'):
            broken.append(f"{g.get('id')}缺{lack or 'unit/target'}")
    if broken:
        return bad('Q1', f"{len(hard_goals)} 个硬目标中 {len(broken)} 个六要素不全：{broken[:4]}")
    if not d.get('source'):
        return bad('Q1', '目标集缺 source')
    return ok('Q1', f"{len(hard_goals)} 个硬目标六要素齐全、有单位/目标值、目标集有出处")


CHECKS = {'Q1': q1}
