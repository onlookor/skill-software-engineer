# R2 提案：SRC kind 的剖面 N-A 适用范围与字段清单

| 项 | 值 |
|---|---|
| 提案编号 | R2-SRC-01（草案） |
| 状态 | **已批准并落盘**（2026-11-06）：母本第 381 行**同行追加**澄清句，零插行；落盘记录见 §9 |
| 日期 | 2026-11-05（草案）；2026-11-06（批准与落盘） |
| 触发 | `ADR草案-SRC-9.2.3九信号源-方案③.md` §2.8（R1.4 裁定）；母本 9.2.3；0.17.2 剖面机制 |
| 关联 | `R2-KP-G3-01`／`ADR-KP-G3-01`（先例）；`registry/profiles.yaml`；`registry/README.md` §4.17／§4.18；`project.py`（M2／`C-ENV`／`C-ST`／`META`） |
| 拟改 | 母本第 381 行**同行追加**一句（零插行，见 §9）；另新增 `kind_profile_SRC` 剖面（`profiles.yaml`，第四步执行） |
| 本轮不改 | `profiles.yaml`／`method_registry.yaml`／`predicate_vocabulary.yaml`／四件投影；不发布 `SRC-001…` 编号 |
| 批准 | 0.13、0.5、0.10；Agent 不得自批 |

## 1. 为什么需要这条 R2，而不是沿用 `R2-KP-G3-01`

1. 母本第 381 行已落 `R2-KP-G3-01` 的句子：0.8 所称「每种方法条目」指 0.17.3 **封闭枚举的全部 kind**；不以质量属性为选择判据的 kind，其 `envelope` 与 `cost_profile` 可登记 `not_applicable`（逐项附 `reason`，`provenance.origin=compiled`）。
2. 该句是**一般判据**，覆盖「枚举内的 kind」；但 `SRC` 尚未进入枚举（须先落 I-A），且该句只界定 0.8 包络义务，**未回答**：`cost_profile` 的 7 个子字段是否全部 N-A、`applicability` 对信号源应写什么、`entry_level_exemptions` 的 `scope` 形态。
3. 因此本提案只做两件事：**确认适用范围**（SRC 落入第 381 行的判据，不需新母本句）＋**裁定字段清单**（逐项 N-A 与必填边界）。这是 0.13 要求的「kind 剖面变更」材料，不是重复裁 KP-G3。

## 2. 拟登记的剖面（形态，非执行）

| 字段 | 处置 | `reason` 要点 |
|---|---|---|
| `envelope` | `not_applicable` | SRC 是漂移/腐化信号源登记，不以质量属性为选择判据（母本 9.2.3 表；第 381 行判据） |
| `cost_profile.latency_budget_delta` | `not_applicable` | 信号源不被「选择」，无延迟预算影响面 |
| `cost_profile.failure_modes` | `not_applicable` | 信号源不是可选方法，无失败模式卡片 |
| `cost_profile.consistency_impact` | `not_applicable` | 信号源不改变一致性级别 |
| `cost_profile.observability_requires` | `not_applicable` | 观测能力在 GRD／9.2.5 侧登记，不在 SRC 条目 |
| `cost_profile.ops_cost` | `not_applicable` | 同上；消费成本在 GRD 侧卡片 |
| `cost_profile.skill_prerequisites` | `not_applicable` | 信号源不要求新技能前提 |
| `cost_profile.aggregation_semantics` | `not_applicable` | 信号源无跨条目聚合语义 |
| `compatibility` | **必填** | 信号源与既有 G 规则／DPS 指标的兼容关系须逐条写 |
| `constraints_imposed` | **必填** | 信号越阈后施加的处置（P0／P1／P2）是真实约束 |
| `applicability` | **必填** | 信号的适用条件（源方面活跃、观测能力就绪）须可求值 |
| `undecided_fields` | `[]`（留痕不删键） | 全部字段已定处置 |
| `entry_level_exemptions` | 1 条 `C-ENV`（全批 `scope`） | `envelope` 为 N-A 时 `C-ENV` 须由豁免而非 N-A 兜底 |
| `status` | `draft → seed`（`C-KP` 通过后） | `C-ST`／`META` 要求剖面非 `draft` 才可声明 `seed` |

**关键约束（沿用 `project.py` 实测行为）**：

- `not_applicable` 与 `common_required` 是**精确字符串**匹配，写 `cost_profile` 不会移除 7 个子字段，**必须逐项列**。
- `C-ENV` 的豁免来源是 `entry_level_exemptions`，**不是** `not_applicable`；只把 `envelope` 放进 N-A **不足以**过 `C-ENV`。
- 剖面 `draft` 且该 kind 已有条目 → `META` 硬失败；剖面 `draft` → 条目不得声明 `seed`（`C-ST`）。

## 3. 影响面清单

| 面 | 影响 | 处理 |
|---|---|---|
| kind | 新增 `SRC`（0.17.3 枚举 17→18） | 由 ADR 的 I-A 落行；本提案只准备剖面 |
| 字段 | `envelope`＋`cost_profile.*` 7 子字段 N-A；3 字段必填 | 逐项 `reason`＋`provenance` |
| 既有条目 | 0 条（`SRC` 尚无条目） | 无需回改 |
| 既有豁免 | `STY-020…024` 的 `C-ENV` 保留，不回写 | 0.22 只登记不改写 |
| 检查 | M2／`C-ENV`／`C-ST`／`META`；0.18.2 S1 过滤（ADR R1.3） | 执行轮改 `project.py` |
| 投影 | 本轮不动 | 剖面登记后重生成 |

## 4. 依赖与未闭合项（不得并入本 R2）

1. **I-A 必须先落**：`SRC` 不在 0.17.3 枚举内时，第 381 行判据不覆盖它；本 R2 批准后仍须等 I-A 生效才能登记剖面。
2. **条目内容未定**：8 条 SRC 的 `applicability`／`compatibility`／`constraints_imposed` 具体谓词属条目撰写（ADR §6），不在本 R2。
3. **`scope` 终值**：`entry_level_exemptions.scope` 依赖 `SRC-001…008` 的实际编号区间；本轮不发布编号，故只能给形态，不能给假精确范围（0.4）。
4. **E3 Waiver**：SRC 的 E3 豁免另案，不在本 R2。
5. **S1 过滤实现**：ADR R1.3 已裁「排除」，具体实现与用例属执行轮，不在本 R2 文本内。

## 5. 批准后执行步骤（本轮不执行）

1. 人类责任方批准本提案（0.5／0.10）。
2. 另起一轮：先落 I-A（0.17.3 枚举加 `SRC` 行）＋I-B（9.2.3 注记），按 ADR §3.1 联合位移实测数字执行（6,847 锚／95 review）。
3. 在 `profiles.yaml` 登记 `kind_profile_SRC`（按 §2 清单）；`registry/README.md` 补 4.x 节。
4. `project.py` 加 S1 过滤；跑 `--check`／`--project`，记录 entries／checks／hard／soft。
5. 重生成四件投影；`todo.md`／changlog 追加登记；不 push，待确认。

## 6. 本轮未改动清单

- 母本：0 行改动。
- `profiles.yaml`／`method_registry.yaml`／`predicate_vocabulary.yaml`／四件投影：0 改动。
- 仅新增本文件；ADR 草案更新；规范新增 §10.3；冻结快照追加 1 行订正注记。

## 9. 落盘记录（2026-11-06）

| 项 | 内容 |
|---|---|
| 批准 | 用户（2026-11-05 批「R2-SRC-01」，2026-11-06 执行） |
| 母本形态 | 第 381 行**同行追加**一句，**零插行**：`上述 not_applicable 判据同样适用于 9.2.3 漂移／腐化信号源（kind SRC）：其 envelope 与 cost_profile 登记为 not_applicable（逐项附 reason），compatibility／constraints_imposed／applicability 仍必填。` |
| 行数断言 | `split_lines` 4428→**4428**；代码围栏 216→**216**；`git diff --numstat`＝**1 1**；sha256 前 12 位 `74f46007eb8b`→`eca8a10908dd` |
| `--check` 前 | 条目 **130**；记录 **1123**；硬失败 **0**；软警告 **0**；指针 **2165**（miss 0）；占位符 **1483**（事实 1＋槽 1482） |
| `--check` 后 | 条目 **130**；记录 **1123**；硬失败 **0**；软警告 **0**；指针 **2165**（miss 0）；占位符 **1483**（事实 1＋槽 1482） |
| 四件投影 | 重生成；diff **仅生成时间戳**，源哈希不变（`84afba013620`／`b31adcb5aacc`／`1f990b772c83`） |
| 未执行 | `profiles.yaml` 的 `kind_profile_SRC` 登记留给第四步；`SRC-001…008` 编号未发布 |

> §6／§8 的「本轮未改动清单」为**批准前 as-of 陈述**，历史文字不改；实际落盘以本节为准。
