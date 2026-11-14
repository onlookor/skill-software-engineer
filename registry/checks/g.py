#!/usr/bin/env python3
"""G 系列（方面 9 / 部署与治理）硬性质检查器：G3 G7。

2026-11-14 升级（D-B）：由「键是否存在」改为校验内容。
缺失数据源 → escalate；显式空集 → pass+vacuous；数据在案但不满足 → fail。
"""
from __future__ import annotations

from common import ok, bad, esc, domain_data


def g3(ctx):
    """每条部署策略都有回滚，且风格兼容已判定。"""
    rows = domain_data(ctx, 'deploy_strategy')
    if rows is None:
        return esc('G3', '域数据源未登记：白板无 deploy_strategy 写入',
                   '不可判：部署策略未登记，回滚/兼容检查无从核验（非空真）')
    if not rows:
        return ok('G3', 'deploy_strategy 显式空集：本部署无发布动作',
                  '空真：部署策略域为空，∀ 平凡为真', vacuous=True)
    problems = []
    for r in rows:
        miss = []
        if not r.get('rollback'):
            miss.append('rollback')
        if r.get('compatible_with_style') is not True:
            miss.append('compatible_with_style')
        if miss:
            problems.append(f"{r.get('id', '?')} 缺 {miss}")
    if problems:
        return bad('G3', f'{len(problems)}/{len(rows)} 条部署策略不满足：{problems}')
    return ok('G3', f'{len(rows)} 条部署策略均含回滚且风格兼容判定为真')


def _trend_window(tw):
    """校验可配置趋势窗：{metric: count|time, value: >0}；metric 默认 count。"""
    if not isinstance(tw, dict):
        return None
    metric = tw.get('metric', 'count')
    value = tw.get('value')
    if metric not in ('count', 'time'):
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        return None
    return metric, value


def g7(ctx):
    """每条 P2 信号都配置告警阈值与可配置趋势窗口。"""
    rows = domain_data(ctx, 'p2_signals')
    if rows is None:
        return esc('G7', '域数据源未登记：白板无 P2 信号与告警阈值',
                   '不可判：P2 信号未登记（非空真）')
    if not rows:
        return ok('G7', 'p2_signals 显式空集：本部署无 P2 信号',
                  '空真：P2 信号域为空，∀ 平凡为真', vacuous=True)
    problems, windows = [], []
    for r in rows:
        rid = r.get('id', '?')
        if not r.get('alarm_threshold'):
            problems.append(f'{rid} 缺 alarm_threshold')
            continue
        tw = _trend_window(r.get('trend_window'))
        if tw is None:
            problems.append(f"{rid} 的趋势窗缺失或非法（需 metric∈{{count,time}} 且 value>0）")
        else:
            windows.append(f'{rid}={tw[0]}/{tw[1]}')
    if problems:
        return bad('G7', f'{len(problems)}/{len(rows)} 条 P2 信号不满足：{problems}')
    return ok('G7', f'{len(rows)} 条 P2 信号均配置阈值与趋势窗（{"；".join(windows)}；'
                    f'metric 与 value 可配置）')


CHECKS = {'G3': g3, 'G7': g7}
