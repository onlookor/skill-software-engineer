# 黄金样本集（P0 骨架）

> **状态：skeleton，0 条样本。** 本批只建目录骨架与标注口径，不开始大规模标注。
> 标注对象：D1 叙事步记录、D2 增量同一性、D3 方面映射、D4 覆盖／豁免口径。
> 用法：P1 求值器实现前，样本只作人工判定依据；实现后作回归对照。

## 1. 目录

```
pilot/predicate-ization/golden/
├── README.md          # 本文件：标注口径
├── manifest.yaml      # 骨架：配额、批次策略、当前计数
├── _template.yaml     # 单条样本模板（不是样本）
└── cases/             # 样本文件；当前为空
```

## 2. 一条样本是什么

一条样本 = **一个可独立判定的选择判断**，不是一张卡、不是一段散文。每条样本必须能回答：

1. 该判断写成哪个规范化原子（D2）；
2. 它推进哪个方面、推进几次（D3）；
3. 它是否属于 `mapped`／`process_record`／`exempt`（D4）；
4. 期望的 `change` 是 `new` 还是 `no_op`，以及基线快照里有什么。

样本不得包含解析器／求值器输出，也不得引用实现代码；期望值必须由标注者按《编译规范》T1.2／T2.1 手算。

## 3. 标注口径（逐条可核）

- **S1 原子**：`atom` 必须逐字符合 T1.2 的规范化形式；`atom_key = sha256(utf8(atom))`，标注者须给出计算命令或逐字结果，不得只写「同上」。
- **S2 同一性**：`change` 只由基线快照中是否存在同 `atom_key` 决定。样本须同时给出 `snapshot_before` 的谓词列表（可为最小列表），不得只写「已有」。
- **S3 方面**：`aspects` 取自 `registry/predicate_aspects.yaml` 的对应条目；多方面谓词每个方面各列一次，不合并。映射表没有的名字，样本不得自行发明方面，须标 `blocked: missing_aspect_mapping`。
- **S4 过程记录**：`process_record` 样本的 `aspects` 恒为空，`change` 恒为 `no_op`（不推进向量）；样本须写明它为何不是设计事实。
- **S5 豁免**：`exempt` 样本只用于 3 个已登记名（`step_log`／`selection_procedure`／`verdict_table`）；其它名字标 `exempt` 即样本无效。
- **S6 一步一条**：一条样本只含一个判断；出现两个独立判断时拆成两条，拆分理由记 `split_reason`。
- **S7 不可判定**：确实无法按字面判定时，`expected` 写 `undecidable` 并在 `undecidable_reason` 写明缺哪条定义；不得用「合理」「适当」代替判定。

## 4. 批次与配额（骨架，未开始）

- 每批 **12 条**；标完一批即回改 `plans/predicate-ization-design.md` 一次（对应「每标一批黄金样本回改一次」）。
- P0 目标 **36 条**：方面 4／5／9 各 10 条，过程记录 6 条；其中 `no_op` 至少 6 条、`unqualified` 至少 4 条。
- 覆盖要求：33 个卡片名中至少 20 名各出现一次；未出现名在 `manifest.yaml` 的 `uncovered` 列出，不得静默。
- 标注者与复核者不得为同一人；分歧记 `disagreement`，不强行取平均。

## 5. 冻结

P0 出口达成时，`manifest.yaml` 的 `status` 改为 `frozen` 并写 `frozen_at`；冻结后新增样本只追加，不改写既有样本的期望值。
