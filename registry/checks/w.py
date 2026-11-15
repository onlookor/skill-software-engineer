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

# --- W1 候选 B（2026-11-15 人类裁定）：静态导入名 ⊆ 目标导出集，且每单元至少一个导出 ---
IMPORT_RE = re.compile(
    r"import\s+(?:(?P<clause>[^;'\"]*?)\s+from\s+)?['\"](?P<spec>[^'\"]+)['\"]")
NAMED_RE = re.compile(r'\{(?P<names>[^}]*)\}')
EXPORT_DECL_RE = re.compile(
    r'^\s*export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|let|var)\s+'
    r'([A-Za-z_$][\w$]*)', re.M)
EXPORT_LIST_RE = re.compile(r'^\s*export\s*\{([^}]*)\}', re.M)
EXPORT_DEFAULT_RE = re.compile(r'^\s*export\s+default\b', re.M)
DYNAMIC_IMPORT_RE = re.compile(r'\bimport\s*\(')
REQUIRE_RE = re.compile(r'\brequire\s*\(')
DYN_OR_REQ_RE = re.compile(r'\b(?:import|require)\s*\(')
DYN_STATIC_RE = re.compile(r'\b(?:import|require)\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)')
STAR_IMPORT_RE = re.compile(r'\*\s*as\s+[A-Za-z_$]')


def _exports(text):
    """返回 (命名导出集, 是否有 default)；支持 export 声明与 export { … } 列表。"""
    named = set(EXPORT_DECL_RE.findall(text))
    has_default = bool(EXPORT_DEFAULT_RE.search(text))
    for block in EXPORT_LIST_RE.findall(text):
        for item in block.split(','):
            item = item.strip()
            if not item:
                continue
            if item.endswith(' as default'):
                has_default = True
                continue
            named.add(item.split(' as ')[-1].strip())
    return named, has_default


def _w1_metrics(units=None, pairs=None, bindings=None, violations=None, injected=None):
    """W1 证据的固定字段契约：excluded_dynamic_loads 每轮必报（null = 未能测量）。"""
    return {
        'units': len(units) if units is not None else None,
        'import_edges': pairs,
        'bindings': bindings,
        'violations': violations,
        'excluded_dynamic_loads': len(injected) if injected is not None else None,
        'excluded_dynamic_load_units': sorted({x.split(':')[0] for x in injected}) if injected else [],
    }


def w1(ctx):
    """每个单元接缝封闭（候选 B，机械校验，2026-11-15）。

    判据：exports_static(M) ≠ ∅ ∧ ∀(M1→M2, n): n ∈ exports_static(M2)
          ∧ 目标路径 ∈ module_inventory；包外访问只经 package.json exports。
    边界（2026-11-15 人类批准）：静态相对路径的动态加载 → escalate；
          非字面量/非相对路径 = 外部注入，排除但每轮必报 excluded_dynamic_loads；
          import * as → escalate。
    """
    units = domain_data(ctx, 'module_inventory')
    if units is None:
        return esc('W1', NOTE, '不可判：模块目录未登记，接缝封闭无从核验（非空真）', _w1_metrics())
    if not units:
        return esc('W1', 'module_inventory 显式空集', '不可判：本部署有模块，目录不得为空',
                   _w1_metrics(units=[]))

    files, why = source_files(ctx)
    if files is None:
        return esc('W1', why, '不可判：无法读取目标仓库源码，机械校验不成立',
                   _w1_metrics(units=units))

    texts = {u: p.read_text(encoding='utf-8') for u, p in files}
    path_to_unit = {p.resolve(): u for u, p in files}
    exports = {u: _exports(t) for u, t in texts.items()}

    # 动态 import()/require()：静态相对路径 = 绕过静态接缝 → escalate；
    # 非相对路径或非字面量 = 外部/注入依赖，排除于内部接缝范围。
    # 「外部注入排除」是可被滥用的口子，故作为**固定观测字段**每次都报（2026-11-15 人类批准）。
    injected, internal_dynamic = [], []
    for u, t in texts.items():
        for m in DYN_OR_REQ_RE.finditer(t):
            sm = DYN_STATIC_RE.match(t, m.start())
            if sm and sm.group(1).startswith('.'):
                internal_dynamic.append(f'{u}→{sm.group(1)}')
            elif not sm:
                injected.append(f'{u}:非字面量')

    def metrics(pairs=0, bindings=0, violations=0):
        return _w1_metrics(units, pairs, bindings, violations, injected)

    if internal_dynamic:
        return esc('W1', f'以动态方式加载内部模块：{internal_dynamic}；动态加载排除计数={len(injected)}',
                   '不可判：内部接缝被动态加载绕过', metrics())
    out_of_scope = [u for u, t in texts.items() if STAR_IMPORT_RE.search(t)]
    if out_of_scope:
        return esc('W1', f'出现命名空间导入（import * as）：{out_of_scope}；动态加载排除计数={len(injected)}',
                   '不可判：import * as 不在判据 B 的静态绑定范围', metrics())

    empty = sorted(u for u, (named, default) in exports.items() if not named and not default)
    if empty:
        return bad('W1', f'{len(empty)}/{len(units)} 个单元无静态导出，接缝不存在：{empty}；'
                         f'动态加载排除计数={len(injected)}', '判据 B 第二项不满足', metrics())

    pairs, bindings, violations = set(), 0, []
    for unit, p in files:
        for m in IMPORT_RE.finditer(texts[unit]):
            spec = m.group('spec')
            if not spec.startswith('.'):
                continue                      # 外部包/内置模块不在单元接缝范围
            target_path = (p.parent / spec).resolve()
            target = path_to_unit.get(target_path)
            if target is None:
                violations.append(f'{unit}→{spec} 目标不在 module_inventory')
                continue
            pairs.add((unit, target))
            clause = (m.group('clause') or '').strip()
            if not clause:
                continue                      # 副作用导入，无绑定
            if clause.startswith('{'):
                block = NAMED_RE.search(clause)
                names = [x.strip().split(' as ')[0] for x in (block.group('names').split(',') if block else [])]
                names = [x for x in names if x]
            else:
                names = ['default']
            named, has_default = exports[target]
            for n in names:
                bindings += 1
                if n == 'default':
                    declared = has_default
                else:
                    declared = n in named
                if not declared:
                    violations.append(f'{unit}→{target} 导入 {n} 不在目标导出集')

    if violations:
        return bad('W1', f'机械核对不通过：{violations}；动态加载排除计数={len(injected)}',
                   '静态导入名超出目标单元导出集', metrics(len(pairs), bindings, len(violations)))
    return ok('W1', f'机械校验：{len(units)} 单元 / {len(pairs)} 边 / {bindings} 绑定 / 0 违规'
                   f'（每单元导出非空；静态 ESM 范围内无越界访问）；'
                   f'动态加载排除计数={len(injected)}（外部/注入依赖，固定观测项）',
              metrics=metrics(len(pairs), bindings, 0))


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
