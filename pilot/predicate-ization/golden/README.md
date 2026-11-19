# 黄金样本集（P0）

> **状态：in_progress，已标注第 1 批 12 条。** 单人标注；独立复核席抽检尚未执行；κ 不可估计。
> 标注对象：D1 叙事步记录、D2 增量同一性、D3 方面映射、D4 覆盖／豁免口径。
> 用法：P1 求值器实现前，样本只作人工判定依据；实现后作回归对照。

## 1. 目录

```
pilot/predicate-ization/golden/
├── README.md          # 本文件：标注口径
├── manifest.yaml      # 清单：配额、批次策略、当前计数
├── _template.yaml     # 单条样本模板（不是样本）
└── cases/             # 样本文件；第 1 批 12 条已就位
```

## 2. 一条样本是什么

一条样本 = **一个可独立判定的选择判断**，不是一张卡、不是一段散文。每条样本必须能回答：

1. 该判断写成哪个规范化原子（D2）；
2. 它推进哪个方面、推进几次（D3）；
3. D3 上它属于 `aspect_mapped` 还是 `process_record`（是否推进方面）；D4 上属于 `mapped` 还是 `exempt`（是否纳入覆盖）；
4. 期望的 `change` 是 `new` 还是 `no_op`，以及基线快照里有什么。

样本不得包含解析器／求值器输出，也不得引用实现代码；期望值必须由标注者按《编译规范》T1.2／T2.1 手算。

## 3. 标注口径（逐条可核）

- **S1 原子**：`atom` 必须逐字符合 T1.2 的规范化形式；`atom_key = sha256(utf8(atom))`，标注者须给出计算命令或逐字结果，不得只写「同上」。
- **S2 同一性**：`change` 只由 `snapshot_before.atoms` 中是否存在同 `atom_key` 决定。样本须逐项给出 `snapshot_before.atoms`（每项含 `atom_key` 与规范化原子原文，可为最小列表），按 `atom_key` 升序、不得重复；`ref`／`sha256` 只是摘要，不得只写摘要或只写「已有」。
- **S3 方面**：`aspects` 取自 `registry/predicate_aspects.yaml` 的对应条目；多方面谓词每个方面各列一次，不合并。映射表没有的名字，样本不得自行发明方面，须标 `blocked: missing_aspect_mapping`。
- **S4 过程记录**：`process_record` 样本的 `aspects` 为空数组——schema 只在该 disposition 下允许空数组；`change` 仍按 `atom_key` 判 `new`／`no_op`，即使判 `new` 也不推进任何方面向量。样本须写明它为何不是设计事实。
- **S5 豁免**：`exempt` 样本只用于 3 个已登记名（`step_log`／`selection_procedure`／`verdict_table`）；其它名字标 `exempt` 即样本无效。
- **S6 一步一条**：一条样本只含一个判断；出现两个独立判断时拆成两条，拆分理由记 `split_reason`。
- **S7 不可判定**：确实无法按字面判定时，`expected` 写 `undecidable` 并在 `undecidable_reason` 写明缺哪条定义；不得用「合理」「适当」代替判定。

## 4. 批次与配额（第 1 批已标）

- 每批 **12 条**；标完一批即回改 `plans/predicate-ization-design.md` 一次（对应「每标一批黄金样本回改一次」）。
- 标注口径为**单人标注＋每批抽检**（执行计划第 3 节第 2 项）：不是原定的双人独立标注，也不是它的等效替代。
- P0 目标 **36 条**：方面 4／5／9 各 10 条，过程记录 6 条；其中 `no_op` 至少 6 条、`unqualified` 至少 4 条。
- 覆盖要求：33 个卡片名中至少 20 名各出现一次；未出现名在 `manifest.yaml` 的 `uncovered` 列出，不得静默。
- 标注由执行席单人完成；每批由独立复核席抽检 ≥ 20%，不一致时回改定义并重标该条。κ 不可估计，不得作为任何结论依据；抽检记录逐条留档。

## 5. 冻结

P0 出口达成时，`manifest.yaml` 的 `status` 改为 `frozen` 并写 `frozen_at`；冻结后新增样本只追加，不改写既有样本的期望值。
