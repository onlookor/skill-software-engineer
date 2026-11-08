# ADR-SRC-P0-05：`behavior_switch` 登记与两条 when 改写（护栏可判化）

| 项 | 值 |
|---|---|
| 状态 | **approved**（2026-11-08） |
| 范围 | `predicate_vocabulary.yaml`（+1 名＋VG-05 记 `resolution_2026_11_08`）；`method_registry.yaml` 的 `SRC-004-S1`／`SRC-007-S1` 两条 `when_predicate` |
| 母本 | **零改动**（4,463 行／围栏 216） |
| 级别 | `severity`／`raise_to` **均未改**；`detection_predicate` **均未改**；M4 未扩；S-10／S-11 仍 info |
| 上游 | ADR-SRC-P0-04（6 detection＋3 when 改写）、ADR-SRC-P0-03（批 B 登记） |

## §1 授权与范围

用户指令：① 登记 `behavior_switch`（predicate，arity 1，出处母本第 2600 行 Z6 的量词域 `flag(G,_,behavior,_)`），并把 `SRC-004-S1` 的 `when_predicate` 改为调用式，`raise_to`／`detection`／`consumption.note` 不动，方针「护栏只能变可判，不能变松」；② `SRC-007-S1` 的 `when_predicate` 补括号为 `distortion(system)`，若与 detection 同义则在 ADR 说明「when 保留以维持升级门槛语义」，不删。

## §2 `behavior_switch` 登记

```yaml
- {name: behavior_switch, arity: 1, kind: predicate, block: "5.5", line: 2600,
   source: {source_type: clause_id, value: "5.5", verified: true}, ...}
```

- **出处**：母本 5.5 第 2600 行 `Z6: ∀ flag(G,_,behavior,_): ∃ approved(ADR(G)) ∧ declared(expiry(G)) ∧ now ≤ expiry(G) ∨ cleanup_filed`。Z6 的**辖域本身就只含行为级**（第三槽 `level=behavior`），结构级开关不在其域内。
- **只判类别，不重述 Z6**：本谓词判 `flag` 的归属类别；Z6 的四支治理闭合由 `expiry_of`／`cleanup_filed` 与条目 `constraints_imposed`／`source_pointers` 承载，本条不复制合取式，故不构成重复真源。
- **台账**：`VG-05` 记 `resolution_2026_11_08`（`predicate_rows_added: 1`，`registered` 带 `was`＝`missing_need` (vi) 的类别判据面；`status_after: open`，残余 2 项「五槽登记判据／snapshot_changed」不变）。

### §2.1 对指令字符串的一处收紧（须用户复核）

指令给的 `when_predicate: "∃ flag: behavior_switch(flag)"`，本批落为 **`behavior_switch(flag)`**（去独立存在量词，自由变量回指 detection 的 `∃ flag` 绑定）。

**理由**：`when_predicate` 是升级触发条件，与 detection 的见证是同一实体；若自带独立 `∃ flag:`，则语义退化为「存在某个行为级开关」——**结构级僵尸开关叠加任意一个无关的行为级开关即升 P0**，与本轮硬前提「护栏不能变松」及核对点 ①（结构级开关不得升 P0）直接冲突。去掉量词后，`when` 只在「该被检出的僵尸开关本身属行为级」时成立，与母本 Z6 的辖域一致。此写法与既有惯例同型：`SRC-001-S1` 的 `monotonic_trend(dsm_metric, window)`、`SRC-005-S1` 的 `burn_rate(service) …`、`SRC-007-S1` 的 `distortion(system)` 均为自由变量。

若用户要求严格照原字符串，改回后核对点 ① 不通过，须重新裁定量词语义。

## §3 `SRC-007-S1` 的 when

| 改前 | 改后 |
|---|---|
| `distortion ∧ ∃ hard property 无下层覆盖` | `distortion(system)` |

- 第三合取项由 `distortion` 定义吸收，与 detection 侧同一处理口径（ADR-SRC-P0-04 §5）。
- **是否与 detection 完全同义**：否。detection 为 `pyramid_distortion(system) ∧ distortion(system)`（两合取支），when 只取第二支，是 detection 的**真子集**。改写前同样是子集（缺 `pyramid_distortion` 支），故**升级行为不变**。
- **when 保留以维持升级门槛语义**：`raise_to: P1` 的语义是「T5 失真出现即由 P2 监测转 P1 限期整改」，删掉 when 会把该条退化为纯 P2；按指令不删。

## §4 三项护栏核对

| # | 核对点 | 结论 | 依据 |
|---|---|---|---|
| ① | 结构级开关是否仍不会升 P0 | **通过** | `when` 的自由变量 `flag` 回指 detection 的 `∃ flag` 见证（第 11521 行）；结构级 flag 使 `behavior_switch(flag)` 为假 → `raise_to: P0` 不触发，保持 P2。若按独立存在量词读则不通过（§2.1） |
| ② | Z6 四支中 detection 未覆盖的两支（`¬∃approved(ADR(G))`／`¬declared(expiry(G))`）是否仍有挂靠 | **通过（条款级，非指针级）** | (a) `constraints_imposed` 第 11515 行逐字「行为级僵尸开关（Z6 违例）升 P0；其余按 P2 监测」覆盖整个 Z6 违例概念，不限两支；(b) `source_pointers` 的 9.2.3 行 `僵尸开关（expiry 超期）、隐式时序假设再现` 与 5.4 约束行「方面 9 守护对象：…僵尸开关（expiry 超期）」保留；(c) `formal_anchor` `G1 triggers` 未动；(d) `consumption.note`「行为级开关升 P0 后即时阻塞（9.2.1）」未动。**观察**：`source_pointers` 未含 5.5（Z6 形式化锚点所在节），Z6 的机器可查挂靠目前经 9.2.3 与 5.4 间接落地；补 5.5 指针属机器层字段变更，另批 ADR，本批不动 |
| ③ | `raise_to: P0` 的量词域是否与母本第 2600 行一致 | **通过** | 母本 `∀ flag(G,_,behavior,_)` 只辖行为级；`behavior_switch(flag)` 恰好把升级限定在该域内，既未扩到结构级，也未收窄到子类 |

## §5 自检与干跑

- `--check`：**1,213 条记录**｜硬失败 **0**｜软警告 **0**｜**info 41**（未成立 2＝`GAP-SO`×2）。
- S-10（现有检测面）：**0**；S-11（现有检测面）：**0**。
- **干跑 S-11 扩到 `when`（未转硬）**：**红 0**。5 条非空 `when` 全部含已登记调用——`SRC-001-S1` `monotonic_trend`、`SRC-001-S2` `monotonic_trend`、`SRC-004-S1` `behavior_switch`、`SRC-005-S1` `burn_rate`＋`error_budget`、`SRC-007-S1` `distortion`。
- 干跑 S-10 扩到 `when`：**未登记名 0**。
- 词表：`predicates` **157→158**（predicate 147→**148**、term 9、constant 1）；`formula_words` 7、`clause_defined_predicates` 53；合计 **217→218**。
- 母本 0 行；指针反查数不变（`source` 引用 clause 5.5 已在锚内，无新增 `@NNNN`）。

## §6 被否方案

| 方案 | 否决理由 |
|---|---|
| A. 照写 `∃ flag: behavior_switch(flag)` | 独立存在量词使护栏变松（§2.1），与核对点 ① 冲突 |
| B. 把 `behavior_switch(flag)` 折进 detection | 违反「detection 不动」；且 detection 是**发现**条件、when 是**升级**条件，混写会把 P2 信号抬成 P0 发现条件 |
| C. 删 `SRC-004-S1` 的 when | ADR-SRC-P0-04 §4 已判三处缺口（范围／两支／条款指代） |
| D. 删 `SRC-007-S1` 的 when | 会使该条退化为纯 P2，丢失 T5 的整改门槛 |
| E. 给 `behavior_switch` 立 arity 4（复刻 `flag` 四槽） | 该谓词只判类别，四槽属 `flag` 的定义面；复刻即重复真源 |
| F. 借本批把 5.5 补进 `source_pointers` | 属机器层字段变更，须单独 ADR；本批只报观察 |
