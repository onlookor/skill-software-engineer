# ADR 草案：GRD／PRJ／GOV 三 kind 剖面变更（KP-G3 的 R2 落地）

| 项 | 值 |
|---|---|
| ADR 编号 | ADR-KP-G3-01（草案） |
| 状态 | 草案；待 `R2-KP-G3-01` 批准后提交人类批准；本轮**不改** `profiles.yaml` |
| 日期 | 2026-11-03 |
| 决策类目 | 注册表变更（kind 剖面 = 元注册条目，0.17.2 @381；0.13 @271；0.17.4 @428） |
| 关联 | `R2提案-KP-G3-包络义务适用范围.md`；`KP-G3` @574-579；`registry/README.md` @260 `C-ST`；`project.py` @847-862 `C-ENV` |
| 批准 | 人类责任方；Agent 仅备材料（0.10 @235） |

## 1. 背景

`KP-G3` @574-579 记录：非 0.18 选型路径的 GRD／PRJ／GOV 是否须声明 0.8 包络与 `cost_profile`，母本无明文；三剖面均为 `status: draft`（@475／@506／@537），`undecided_fields` 明列（@496／@527／@555）。`C-ST`（README @260）与 `META`（`project.py` @958-961）使「draft 剖面 + 条目」不可行。

本 ADR 是 `R2-KP-G3-01` 的数据侧落地：R2 只给「`envelope`／`cost_profile` 可显式 N-A」的判据；本 ADR 决定三个剖面各字段的目标值。**两者必须同时批准**，否则剖面仍为 draft，s5e-10 M2 不得启动。

## 2. 决策摘要

批准后对 GRD／PRJ／GOV 三件剖面：

1. `envelope` 与 `cost_profile` 的 **7 个** `cost_profile.*` 子字段 → `not_applicable`，逐项带 `reason`（引用 R2 句）、`provenance: compiled`、`source`。
2. `compatibility`／`constraints_imposed`／`applicability` → **回到 `common_required` 默认必填**（从 `undecided_fields` 移除，**不**进 `not_applicable`）；条目可用空列表 `[]` 表达「无该关系／无该前提」，但不得把字段缺失当作豁免。
3. PRJ 的 `applicability.delivery_space` → 同上，**必填、不按 N-A**；若某条目无法给出交付空间谓词，按 M2 失败处理，不静默放行。
4. `status: draft` → `seed`：在上述字段落定且 `C-KP` 通过后执行；依据 0.17.5 @444（draft→seed 属 bootstrap 低影响）与 `KP-G2` @568-573（元条目完备性由 `C-KP` 判定）。
5. `entry_level_exemptions` → 每个 kind 增加 **1 条** `C-ENV` 豁免，`scope` 覆盖该 kind 全批；**这是 `C-ENV` 通过的必要条件**（`not_applicable` 不被 `C-ENV` 读取，`project.py` @847-848）。
6. `undecided_fields: []`（留痕用空列表，不删键）。

## 3. 变更总表

| kind | 字段（现状行号） | 现值 | 目标值 | 依据 |
|---|---|---|---|---|
| GRD | `status` @475 | `draft` | `seed` | 0.17.5 @444；`KP-G2` @568-573；README @259 `C-KP` |
| GRD | `not_applicable` @495 | `[]` | `envelope` + 7 个 `cost_profile.*`（共 8 项） | R2 @381；0.17.2 @381；0.8 @199 |
| GRD | `undecided_fields` @496 | `[envelope, cost_profile, compatibility, constraints_imposed, applicability]` | `[]` | 0.17.2 @339-361；`common_required` @35-61 |
| GRD | `entry_level_exemptions` @497 | `[]` | 1 条（`envelope`／`C-ENV`／全批 scope） | `project.py` @847-862；STY 先例 @98-103 |
| GRD | `required_extra` @491-493 | `[anti_patterns, formal_anchor]` | 不变 | 0.17.4 @424；9.2.1 |
| PRJ | `status` @506 | `draft` | `seed` | 0.17.5 @444；`KP-G2` @568-573 |
| PRJ | `not_applicable` @522-527 | 仅 `cost_profile.latency_budget_delta` | 原项保留 + `envelope` + 其余 6 个 `cost_profile.*`（共 8 项） | R2 @381；0.17.2 @381（latency 明例） |
| PRJ | `undecided_fields` @527 | `[envelope, cost_profile.consistency_impact, cost_profile.ops_cost, compatibility, applicability.delivery_space]` | `[]`（`delivery_space` 必填，不 N-A） | 0.17.2 @339-343；0.17.4 @417；`common_required` @35-40 |
| PRJ | `entry_level_exemptions` @528 | `[]` | 1 条（`envelope`／`C-ENV`／全批 scope） | `project.py` @847-862 |
| PRJ | `required_extra` @520 | `[]` | 不变 | — |
| GOV | `status` @537 | `draft` | `seed` | 0.17.5 @444；`KP-G2` @568-573 |
| GOV | `not_applicable` @554 | `[]` | `envelope` + 7 个 `cost_profile.*`（共 8 项） | R2 @381；0.17.2 @381；0.8 @199 |
| GOV | `undecided_fields` @555 | `[envelope, cost_profile, compatibility, constraints_imposed, applicability]` | `[]` | 0.17.2 @339-361；`common_required` @35-61 |
| GOV | `entry_level_exemptions` @556 | `[]` | 1 条（`envelope`／`C-ENV`／全批 scope） | `project.py` @847-862 |

## 4. 逐 kind 字段清单

### 4.1 GRD（@471-499）

- `@475 status: draft` → `seed`。
- `@495 not_applicable: []` → 以下 8 项（每项均带 `reason`、`provenance: compiled`、`source: {source_type: clause_id, value: "0.17.2", verified: true}`）：
  - `field: envelope`
  - `field: cost_profile.latency_budget_delta`
  - `field: cost_profile.failure_modes`
  - `field: cost_profile.consistency_impact`
  - `field: cost_profile.observability_requires`
  - `field: cost_profile.ops_cost`
  - `field: cost_profile.skill_prerequisites`
  - `field: cost_profile.aggregation_semantics`
- 8 项共用理由模板（`envelope` 与 7 子字段分别写，不合并）：
  - `envelope`：`R2 澄清（0.17.2 @381）：GRD 守护规则模板不以质量属性为选择判据，0.8 包络义务按本剖面登记为 not_applicable；显式豁免而非省略。`
  - `cost_profile.*`：`R2 澄清（0.17.2 @381）：cost_profile 随 envelope 一并 N-A；本子字段无独立质量影响面。`
- `@496 undecided_fields: [...]` → `[]`（`compatibility`／`constraints_imposed`／`applicability` 回到 `common_required` 默认必填）。
- `@497 entry_level_exemptions: []` → 1 条：
  - `scope: "GRD-001…GRD-{终值}"`（**终值由 M1 批次定义裁决后填实；不得写非数字占位**，`scope_covers` 只识别 `GRD-数字`）
  - `field: envelope`
  - `check: C-ENV`
  - `reason: "GRD 守护规则模板不改变质量属性包络；0.8 包络义务经 R2-KP-G3-01 澄清为 not_applicable；C-ENV 对非 1.2.x 源行且 envelope 为空的条目按本豁免显式放行（project.py @847-862）。"`
  - `provenance: compiled`
  - `source: {source_type: clause_id, value: "0.17.2", verified: true}`
- `@491-493 required_extra`、`@494 optional` 不变。
- `@499 note`：保留原文（历史），**追加**一句：`2026-11-03：R2-KP-G3-01／ADR-KP-G3-01 闭合，本剖面 status 由 draft 转 seed；原文保留为历史。`

### 4.2 PRJ（@502-530）

- `@506 status: draft` → `seed`。
- `@522-527 not_applicable`：保留 `cost_profile.latency_budget_delta` 原项（理由与 source 不动，0.22），再增 7 项：
  - `field: envelope`
  - `field: cost_profile.failure_modes`
  - `field: cost_profile.consistency_impact`
  - `field: cost_profile.observability_requires`
  - `field: cost_profile.ops_cost`
  - `field: cost_profile.skill_prerequisites`
  - `field: cost_profile.aggregation_semantics`
- 新增 7 项的理由模板同 GRD（`envelope` 一项、`cost_profile.*` 六项）。
- `@527 undecided_fields: [...]` → `[]`。**`applicability.delivery_space` 明确按必填处理，不 N-A**；若条目无法给出谓词，M2 失败。
- `@528 entry_level_exemptions: []` → 1 条，形态同 GRD，`scope: "PRJ-001…PRJ-{终值}"`，`reason` 改为「PRJ 投影词汇/规则不改变质量属性包络」。
- `@520 required_extra: []` 不变。

### 4.3 GOV（@533-558）

- `@537 status: draft` → `seed`。
- `@554 not_applicable: []` → 8 项，字段与理由模板同 GRD；`reason` 改为「GOV 治理模板（ADR 亚型、简记格式）不改变质量属性包络」。
- `@555 undecided_fields: [...]` → `[]`。
- `@556 entry_level_exemptions: []` → 1 条，`scope: "GOV-001…GOV-{终值}"`，形态同 GRD。
- `@558 note`：保留原文，**追加**一句：`2026-11-03：R2-KP-G3-01／ADR-KP-G3-01 闭合；原文保留为历史。`

## 5. 字段级依据

- **`envelope`／`cost_profile` N-A**：R2-KP-G3-01 拟追加句（0.17.2 @381）；0.8 @199；0.17.2 @381 的「并非每个 kind 都需全字段」明例。
- **7 个子字段必须逐项列**：`project.py` @405-419 的物化是精确字符串匹配（@416）；`common_required` 的子字段在 `profiles.yaml` @44-53。写 `cost_profile` 整体**不会**移除子字段。
- **`compatibility`／`constraints_imposed`／`applicability` 必填**：`common_required` @35-40／@54-61（来源 0.17.4 @415-417）；0.17.2 @339-343／@356-361。它们回归默认，不需要新增母本命题；条目的空列表 `[]` 是合法值（`has_path` 只判存在，@170-177）。
- **PRJ `delivery_space` 必填**：`common_required` @35-40；0.17.2 @339-343（三空间字段）；0.17.4 @417（S3 消费 `delivery_space`）。**这是本 ADR 的独立决定，不是 R2 的推论**。
- **`status: seed`**：0.17.5 @444（draft→seed 属 bootstrap 专用、低影响）；`KP-G2` @568-573（元条目完备性由 `C-KP` 判定）；README @259 `C-KP`。
- **`entry_level_exemptions`**：`project.py` @847-862（`C-ENV` 只读 `exemptions`）；STY 先例 @98-103；`C-KP` @516-519 要求 `scope`／`field`／`check`／`reason`／`provenance`。
- **状态迁移不改写历史**：0.22 承诺一 @1137（编号永不复用／不重排）；本 ADR 对既有条目只登记、不回写。

## 6. 检查器可验证性与预期终值

执行后（**尚无 GRD／PRJ／GOV 条目**）：

- `entries`：仍 **110**（本 ADR 不加条目）。
- `checks`：预期仍 **948**（`C-KP` 每剖面一遍，N-A 项不新增检查）；`hard` **0**、`soft` **0**（以实跑为准，不预写死）。
- `M2`：三剖面 required 列表移除 `envelope` 与 7 个 `cost_profile.*`；`compatibility`／`constraints_imposed`／`applicability` 仍在 required。
- `C-ENV`：无条目，暂不触发；M2 加条目后，空 `envelope` 走 `entry_level_exemptions` 的 `skip`，不 `fail`。
- `META`：剖面 `seed` + 条目 → 不再触发 @958-961 的 draft 硬失败。
- `C-ST`：剖面 `seed` → 条目可声明 `seed`（README @260）。
- `C-KP`：8 项 N-A 均带 `reason`／`provenance`／`source`，通过。
- `M3`：缺 `envelope` 的条目会记 `skip`（消息文案「envelope 字段缺失（由 M2 记失败）」是旧文案）；因 `envelope` 已 N-A，M2 不会失败，此 `skip` 不是硬失败，也不影响 seed 资格。若需消除误导文案，另案修 `project.py`，不在本 ADR 范围。
- **不可验证项**：「守护规则模板／投影词汇／治理模板不改变质量属性」是语义判断，检查器只能验证「N-A 有据」，不能验证「N-A 为真」；后者由 R2＋人类批准承担。

## 7. 影响面

- **目标 kind**：GRD／PRJ／GOV 三件；`profiles.yaml` 行数增加（8+7+8 项 N-A + 3 条豁免），@466 之后所有行号位移。
- **既有条目**：`method_registry.yaml` 中 GRD／PRJ／GOV 条目为 **0**；其余 110 条不受影响（其 kind 剖面的物化列表不变）。
- **既有豁免**：STY-020…024 的 `C-ENV` 豁免 @98-103 保留；R2 只是给它更一般的依据，不回写。
- **既有 optional**：DEC／OWN／CFG／VFM 的 `cost_profile.latency_budget_delta` optional 不受影响。
- **投影**：改 `profiles.yaml` 后四件投影必须重生成（`project.py --project`）；本轮不动，且并行 s5g 任务占用词汇表与投影——执行前须与 s5g 任务协调。
- **README／文档引用**：本 ADR 与 R2 提案引用的 `profiles.yaml` 行号是**改前基线**；执行后须按实测更新（锚点先行），但不得改写已发布登记（0.22）。

## 8. 风险与缓解

| 风险 | 缓解 |
|---|---|
| `cost_profile` 整体 N-A 可能掩盖真实的 observability／ops 成本 | `not_applicable` 只影响 **M2 必填**，不禁止条目填写；若某 GRD 条目确有观测要求，条目仍可填 `cost_profile`（schema 允许），并在条目层说明。 |
| `entry_level_exemptions.scope` 需要终值 | 不在草案编造范围；等 M1 批次定义裁决 `entry_id_range` 后再写 YAML（0.4 禁假精确）。 |
| 头注 @13-14 与 @558 的口径冲突未裁 | 批准 R2 时同时裁定（R2 提案 §6.1）；未裁前不写 `profiles.yaml`。 |
| PRJ `delivery_space` 必填可能卡住 M2 | 这是**有意**的诚实失败：不把未闭合缺口伪装成 N-A；若批准方要 N-A，另起第二条 R2。 |
| 23 项 N-A 条目冗长且依赖精确字段名 | schema 已冻结（0.17.2），字段名固定；执行时用脚本比对 `common_required`，不手抄漂移。 |
| `status: seed` 与 `seed_source` 占位符并存 | `seed_source` 是批次数据，不是字段适用性；M1／M2 填实，不在本 ADR 断言。 |
| 高影响变更 | 0.13 @271、0.17.4 @428：完整 ADR + 人类批准；0.10 @235：Agent 不自批。 |

## 9. 批准与执行前置

1. 人类批准 `R2-KP-G3-01` 文本。
2. 人类批准本 ADR。
3. 裁定 `profiles.yaml` @13-14 与 @558 的口径冲突。
4. 确定 GRD／PRJ／GOV 的 `entry_id_range`（M1 批次定义），以便写 `scope` 终值。
5. 与并行 s5g 任务协调：`predicate_vocabulary.yaml` 与四件投影归 s5g；本 ADR 执行时只改 `profiles.yaml`，重生成投影需串行。
6. 执行后跑 `--check`／`--project`，记录 entries／checks／hard／soft／占位符／指针；按 0.22 只追加 changelog。

## 10. 本轮不做

- 不改母本、不改 `profiles.yaml`、不改 `method_registry.yaml`、不改 `predicate_vocabulary.yaml`、不改四件投影。
- 不 commit、不 push。
- 仅新增本文件与 R2 提案，并在 `todo.md`／changlog 追加登记。
