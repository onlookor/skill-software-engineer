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


_METRIC_VALUES = {'count', 'time'}


def _declaration_shape(tw):
    """校验趋势窗的**声明形态**（ADR-GUARD-02 D3）。

    通过条件：metric 声明为 count|time 枚举且 unconfigured=cannot_evaluate；
    value 声明为 number、带非空 range、且 unconfigured=cannot_evaluate。
    **值不参与判定**：直接给数值不构成声明（按形态缺失记）；给出数值时也不据此改判。
    """
    if not isinstance(tw, dict):
        return None, '缺 trend_window 声明'
    metric = tw.get('metric')
    if not isinstance(metric, dict):
        return None, 'metric 未以声明形态给出（需 {type, values, unconfigured}）'
    values = metric.get('values')
    if not isinstance(values, list) or set(values) != _METRIC_VALUES:
        return None, 'metric.values 未声明为 count|time 枚举'
    if metric.get('unconfigured') != 'cannot_evaluate':
        return None, 'metric 未声明未配置行为=cannot_evaluate'
    val = tw.get('value')
    if not isinstance(val, dict):
        return None, 'value 未以声明形态给出（需 {type, range, unconfigured}；给出数值本身不算声明）'
    if val.get('type') != 'number':
        return None, 'value.type 未声明为 number'
    rng = val.get('range')
    if not isinstance(rng, str) or not rng.strip():
        return None, 'value.range 未声明取值范围'
    if val.get('unconfigured') != 'cannot_evaluate':
        return None, 'value 未声明未配置行为=cannot_evaluate'
    return f'metric∈{{count,time}}；value:number {rng}（仅声明，无值）', None


def g7(ctx):
    """每条 P2 信号都声明告警阈值与可配置趋势窗（形态判据，值不参与判定）。"""
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
        shape, why = _declaration_shape(r.get('trend_window'))
        if shape is None:
            problems.append(f'{rid} 趋势窗声明形态不合规：{why}')
        else:
            windows.append(f'{rid}: {shape}')
    if problems:
        return bad('G7', f'{len(problems)}/{len(rows)} 条 P2 信号不满足：{problems}',
                   '形态判据：判定可配置项是否被正确声明；不合规即无法据以判趋势')
    return ok('G7', f'{len(rows)} 条 P2 信号均声明阈值与趋势窗形态（{"；".join(windows)}）',
              '形态判据（ADR-GUARD-02 D3）：判定「可配置项是否被正确声明」，'
              '不代表趋势检测已实现，也不构成对任何运行时窗口取值的验证。')


CHECKS = {'G3': g3, 'G7': g7}
