# 黄金样本集（P0）

> **状态：in_progress，已标注第 1–4 批共 40 条（40 文件已齐；冻结是人类门，未冻结）。** 单人标注；抽检由独立复核席在仓外执行、仓内只登记结论：第 1 批抽检 5 条一致、第 2 批抽检 6 条一致、第 3 批抽检 12 条全覆盖一致，合计 23 条一致、0 不一致、0 条无法判定；第 4 批（收尾批）抽检尚未执行；κ 不可估计。
> 标注对象：D1 叙事步记录、D2 增量同一性、D3 方面映射、D4 覆盖／豁免口径。
> 用法：P1 求值器实现前，样本只作人工判定依据；实现后作回归对照。

## 1. 目录

```
pilot/predicate-ization/golden/
├── README.md          # 本文件：标注口径
├── manifest.yaml      # 清单：配额、批次策略、当前计数
├── _template.yaml     # 单条样本模板（不是样本）
└── cases/             # 样本文件；第 1–4 批 40 条已就位
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
- **S8 期望值形态**：`predicate_write` 样本的 `expected` 写 `advanced_keys`（本步 `change=new` 且 `aspects` 非空的键的并集，去重升序；`no_op` 必为 `[]`）、`d3_disposition`、`d4_status`、`why`。`unqualified` 样本的 `expected` 只写 `verdict: unqualified` 与 `reject_code`；`d3_disposition`／`d4_status` 在该情形**不适用**，不是「可留空」——留空与不适用是两回事。本批定义并使用的 `reject_code` 为 `no_predicate_atom`（该判断没有可写入的机器层谓词原子）；新增码须先在本节登记。
- **S9 原子来源**：原子只由叙事步给出。卡片 `predicate_writes` 的条目整体——裸名与带签名条目（如 `selection_context(DP, F, C)`）——都只作名字存在性与命名空间校验，都不构成原子模板，都不得据此反推参数位或取值域；签名也只证明字面存在，推不出取值域（见 `TECH-DEBT.md` 第 14 条）。

## 4. 批次与配额（第 1–4 批已标，40 文件齐）

- 每批 **12 条**（末批可为余数，第 4 批 4 条）；标完一批即回改 `plans/predicate-ization-design.md` 一次（对应「每标一批黄金样本回改一次」）。第 3 批批次要求：**至少引入 2 个当前未出现的卡片谓词名**（不卡在 `min_distinct_names: 20` 上）；实际引入 8 个。第 4 批（收尾批）要求：3 条 `process_record`（至少 2 个新名字、至少 1 条 `no_op`）＋ 1 条 `unqualified`（只用已登记 `reject_code`）；实际引入 2 个新名字、`no_op` 1 条。
- 标注口径为**单人标注＋每批抽检**（执行计划第 3 节第 2 项）：不是原定的双人独立标注，也不是它的等效替代。
- P0 目标：**桶 36 条**（方面 4／5／9 各 10 条，过程记录 6 条），另 **`unqualified` 4 条**（`aspect = 0`，不占桶）；其中 `no_op` 至少 6 条（占桶）——第 4 批后共 7（`GC-0003`／`GC-0007`／`GC-0017`／`GC-0022`／`GC-0028`／`GC-0035`／`GC-0039`）。文件总数 40，已达成。
- 覆盖要求：33 个卡片名中至少 20 名各出现一次；未出现名在 `manifest.yaml` 的 `uncovered` 列出，不得静默。**覆盖进度（记账 2）**：第 2 批后 19／33；第 3 批引入 8 个新名字后 27／33，`min_distinct_names` 已满足；第 4 批再引入 2 个新名字（`exclusion_record`／`selection_procedure`）后 **29／33**；仍 `uncovered` 4 名（`cleanup_filed`／`flag`／`quality_impact_card`／`step_class`）。
- 标注由执行席单人完成；每批由独立复核席抽检 ≥ 20%，不一致时回改定义并重标该条。抽检一律由独立复核席**在仓外执行**，仓内只登记结论，不是仓内签署。当前结论：第 1 批抽检 5 条一致、第 2 批抽检 6 条一致、第 3 批抽检 12 条全覆盖一致，合计 23 条一致、0 不一致、0 条无法判定；第 4 批（收尾批）抽检尚未执行。κ 不可估计，不得作为任何结论依据；抽检记录逐条留档。
- **三层口径（2026-11-19 裁定）**：
  - **桶数 36**＝方面 4／5／9 各 10 ＋ `process_record` 6；这就是 `target_total`（旧名保留，与 `bucket_total` 同义）。
  - **`unqualified` 单列配额 4**：任何 `unqualified` 一律 `aspect = 0`、**不占桶**。不存在「带方面语境的 `unqualified`」这一中间态——被判不合格即无方面主张，样本里给它记一个方面，等于把「本来想写哪个方面」混进「实际产出了什么」。当前 4 条（`GC-0012`／`GC-0015`／`GC-0018`／`GC-0040`）。
  - **预期文件总数 40**＝桶 36 ＋ `unqualified` 4；第 4 批后已达成。
  - `counts.unqualified` 与配额进度是两个口径：前者数全部 `outcome_kind=unqualified`，后者只数已达配额口径的条目；当前两者都是 4，定义不同，不得互相替代或混用。
- **进度**：
  - 第 1 批 12 个文件：桶 11（方面 4／5／9 = 4／4／2，`process_record` 1）＋ `aspect: 0` 的 `unqualified` 1（`GC-0012`）。
  - 第 2 批 12 个文件：桶 10（方面 4／5／9 = 2／2／4，`process_record` 2）＋ `aspect: 0` 的 `unqualified` 2（`GC-0015`／`GC-0018`）；其中 `no_op` 2 条（`GC-0017`／`GC-0022`）。
  - 第 3 批 12 个文件：全部进桶（方面 4／5／9 = 4／4／4），无 `process_record`、无 `unqualified`；其中 `no_op` 2 条（`GC-0028`／`GC-0035`）；新引入谓词名 8 个（`owner`／`sensitivity`／`invariant`／`shared_write_exception`／`saga`／`orchestrator`／`compensation`／`interaction_flow`）。
  - 第 4 批 4 个文件（收尾批）：桶 3（全部 `process_record`：`GC-0037` `exclusion_record`／`GC-0038` `selection_procedure`／`GC-0039` `step_log`）＋ `aspect: 0` 的 `unqualified` 1（`GC-0040`）；其中 `no_op` 1 条（`GC-0039`，跨批复用 `GC-0011` 的增量原子，首个 `no_op` × `process_record` 交叉）；新引入谓词名 2 个（`exclusion_record`／`selection_procedure`）。
  - 累计 40 个文件＝桶 36（4／5／9 = 10／10／10，`process_record` 6）＋ `aspect: 0` 的 `unqualified` 4；`new` 29、`no_op` 7、`unqualified` 4。
  - `remaining_gap` 已归零：40 文件齐、桶 36 满、`unqualified` 4 满。`manifest.yaml` 的 `status` 仍 `in_progress`、`frozen_at` 仍 `null`——冻结是人类门，执行方不得自行冻结（见 §6）。
- **`cases[].aspect` 口径（记账 1）**：该字段表示案例所属方面——方面样本取源卡 `_aspect`（4／5／9）；过程记录写 `0`，记入独立的 `process_record` 桶；`unqualified` 一律写 `0`，记入 `'0'` 桶。`counts.by_aspect` 按此从 `cases[]` 重算：4／5／9 直接取该字段，`process_record` 取 `d3_disposition=process_record` 的条数，`'0'` 取 `aspect=0` 且非 `process_record` 的条数。
- **字段位置（记账 2）**：`target_total` 在 `quotas` 之下、`cases_per_batch` 在 `batch_policy` 之下；外部脚本不得再读顶层同名字段。

## 5. 定义缺口登记（已裁定）

第 1 批标注中撞上三条定义缺口，均已由人类裁定。裁定内容即现行定义；样本按裁定后口径重标，没有「先这么定、以后再说」的临时写法。

- **DG-0001（`unqualified` 样本的 `expected`）— 已裁定**：`unqualified` 不产生谓词增量，不套映射字段。`expected` 只写 `verdict: unqualified` 与 `reject_code`；`d3_disposition`／`d4_status` 在该情形**不适用**，不是「可留空」——留空与不适用是两回事，后者可判、前者不可判。涉及 `GC-0012`；schema R3 与 S8 已同步，该条已重标（撤销 `undecidable`）。
- **DG-0002（原 `vector_keys_after` 的语义）— 已裁定**：字段改名为 `advanced_keys`，语义定死为「本步 `change=new` 且 `aspects` 非空的键的并集」（去重升序；`no_op` 必为 `[]`）。不另设「步后全量键」字段——可从前序累积推出，多一个字段就多一个不一致的入口。涉及全部 12 条样本，`GC-0003`／`GC-0007` 已按新语义重标；schema 与设计稿已同步。
- **DG-0003（卡片条目到原子的桥）— 已裁定：不修，登记为债**：原子只由叙事步给出；卡片 `predicate_writes` 的条目整体（裸名与带签名条目一视同仁）只作名字存在性与命名空间校验，不构成原子模板，均不得据此反推参数位或取值域；带签名也只证明字面存在，推不出取值域（S9）。空白与关闭判据见 `TECH-DEBT.md` 第 14 条；设计稿第 10 章留有指针。

## 6. 冻结

P0 出口达成时，`manifest.yaml` 的 `status` 改为 `frozen` 并写 `frozen_at`；冻结后新增样本只追加，不改写既有样本的期望值。
