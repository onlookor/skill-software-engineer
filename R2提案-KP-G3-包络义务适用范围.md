# R2 提案：KP-G3「适用性无据」——0.8 包络义务与 kind 剖面的适用范围歧义

| 项 | 值 |
|---|---|
| 提案编号 | R2-KP-G3-01（草案） |
| 状态 | 草案；待人类责任方批准；本轮**不执行**母本改动 |
| 日期 | 2026-11-03 |
| 触发 | `profiles.yaml` `KP-G3` @574-579；0.17.6 (c) @463 |
| 关联 | `KP-G1` @562-567、`KP-G4` @580-584；`registry/README.md` @260 `C-ST`；`todo.md` @143 |
| 拟改 | 母本 `软件工程元框架成文法.md` @381（**同行追加**一句） |
| 本轮不改 | `profiles.yaml`／`method_registry.yaml`／`predicate_vocabulary.yaml`／四件投影 |
| 批准 | 0.13 @271、0.5 @127／@129、0.10 @235；Agent 不得自批 |

## 1. 歧义事实

### 1.1 母本原句

0.8 @199：

> 每种方法条目（风格、策略）必须声明**质量属性包络**：一组参数化公式/区间，刻画“选择此方法后，各项质量指标可达范围的形状”。

0.17.2 @381：

> **字段完备性按 kind 剖面**：并非每个 kind 都需全字段（如 projection_vocabulary 条目无 latency_budget_delta）。每 kind 的必填/选填字段剖面（kind profile）本身是注册表条目（元注册），变更走 0.13。M2 检查按剖面判定完备性。

0.17.1 @313（「方法条目」的枚举面，节引）：

> 方法注册表是**全部方法条目的带元数据登记库**：各方面 2 节的方法空间表格（风格条目、分解策略、契约形态、所有权模式、协调模式、战术、部署策略、投影规则……）一律降格为**种子数据源视图**……

0.17.3 @402／@404／@405（三个争议 kind 的行）：

> | GRD | 守护规则模板 | 方面 9 · 9.2 |
> | PRJ | 投影词汇/规则 | 方面 10 · 10.2.2 |
> | GOV | 治理模板（ADR 亚型、简记格式等） | 0.5/7.2.3 |

0.17.4 @415／@418／@424／@428（消费面，节引）：

> | S1 候选装配 | `kind` + `status` + `applicability`（三空间谓词对 S0 上下文求值） |
> | S4 包络校验 | `envelope` + `cost_profile`（卡片聚合，方面 6 三值判定） |
> **消费者二：守护（方面 9）。** `anti_patterns.detection_predicate` 直接播种 G 规则……
> **消费者四：治理（0.13/方面 7）。** 条目任何机器层字段变更 = 完整 ADR + 批准……

0.17.6 @455（人工兜底）：

> | 人工判断兜底 | 无表格无文献支撑的字段（如 typical_reversibility） | 显式 `provenance={origin: manual}` 登记，禁止留默认值假充来源 |

0.17.6 @463（本歧义的路由）：

> - **(c) 成文法歧义**（两个合理编译器读出不同语义）→ R2 重审提议（成文法条款澄清）。

### 1.2 数据侧现状

`profiles.yaml` 头注 @13-14：

> optional / not_applicable 每项必须带 reason 与 provenance（0.17.6 第四层：人工判断兜底，禁默认值假充）；无母本依据者 provenance.origin = manual。

三个剖面现状（逐行实测）：

| kind | status | undecided_fields | not_applicable | entry_level_exemptions |
|---|---|---|---|---|
| GRD @471-499 | `draft` @475 | `[envelope, cost_profile, compatibility, constraints_imposed, applicability]` @496 | `[]` @495 | `[]` @497 |
| PRJ @502-530 | `draft` @506 | `[envelope, cost_profile.consistency_impact, cost_profile.ops_cost, compatibility, applicability.delivery_space]` @527 | 仅 `cost_profile.latency_budget_delta` @522-527（唯一明文 N-A） | `[]` @528 |
| GOV @533-558 | `draft` @537 | `[envelope, cost_profile, compatibility, constraints_imposed, applicability]` @555 | `[]` @554 | `[]` @556 |

GOV 剖面 note @558：

> 治理模板（ADR 亚型、简记格式）不改变系统质量属性包络，但「不改变」需母本明文方可作 N-A 判定，否则为默认值假充（0.17.6 第四层禁令）→ gaps KP-G3。

**数据侧自相矛盾（必须单列）**：头注 @13-14 明文允许「无母本依据者 `provenance.origin = manual`」，而 @558 又要求「需母本明文」。若头注为准，三 kind 可走 manual N-A 的数据登记；若 @558 为准，则必须 R2。本提案按用户裁决走 R2，但建议批准时同时裁定该口径（见 §6.1），不能两读并存。

### 1.3 检查器事实（决定「改哪些字段」）

- `project.py` @405-419 物化：`required = common_required − optional − not_applicable + required_extra`；`not_applicable` 与 `common_required` 的子字段做**精确字符串**匹配（@416）。因此 `not_applicable: [cost_profile]` **不会**移除 7 个 `cost_profile.*` 子字段，必须逐项列出。
- `project.py` @847-862 `C-ENV`：豁免来源是 `entry_level_exemptions`（@847-848），**不是** `not_applicable`；非 1.2.1／1.2.2／1.2.3 源行且 `envelope` 为空时，若无 `C-ENV` 豁免，@861-862 直接 `fail`。因此仅把 `envelope` 放进 `not_applicable` **不足以**过 `C-ENV`。
- `project.py` @958-961 `META`：剖面 `draft` 且该 kind 已有条目 → 硬失败。
- `project.py` @964-981 `C-ST`：剖面 `draft` → 条目不得声明 `seed`；`registry/README.md` @260 同文：

> 条目所属 kind 的剖面若为 `draft`（`profiles.yaml`，适用性无据 → KP-G3），该条目**不得**声明 `seed`。

## 2. 两种读法

### 读法一（窄）：GRD／PRJ／GOV 不属「方法条目」

主张：0.8 的「方法条目」只指 0.18 S1–S6 可装配、可选择的条目；GRD 由消费者二（守护）消费、GOV 由消费者四（治理）消费、PRJ 由方面 10 消费，均不进入消费者一，故不适用 0.8；其 `envelope`／`cost_profile` 可不填或 N-A。

支持面：

- 0.17.4 @415-420 的字段消费表只列消费者一（S1–S6）；`envelope`／`cost_profile` 只在 S4／S5 出现。
- 0.17.4 @424 明说 GRD 的消费面是 `anti_patterns.detection_predicate`；@428 明说 GOV 的消费面是治理变更控制。
- 0.17.6 @455 允许人工兜底。

反证／代价：

- 0.17.1 @313 的「方法条目」枚举**逐字包含「投影规则」**，而 0.17.3 @404 的 PRJ 正是「投影词汇/规则」；读法一必须把 @313 的枚举解释为「注册表内容」而非 0.8 的范围，文本代价高。
- 读法一需要新增一条母本没有的判据——「是否进入 S1 候选装配」；这比读法二更接近「新机制」。
- 对 GRD／GOV 尚可争辩，对 PRJ 很难自洽；若强行排除 PRJ，会与 @313 正面冲突。

### 读法二（宽）：三 kind 均属方法条目，但可按剖面容差登记 N-A

主张：0.17.3 封闭枚举中的全部 kind 都是「方法条目」，0.8 的「必须声明」不等于「必须填非空 `envelope`」；0.17.2 @381 已授权按 kind 剖面判定完备性，因此 `envelope`／`cost_profile` 可以登记为 `not_applicable`，但必须是**显式、带理由、带 provenance 的豁免**，不是省略。

支持面：

- 0.17.2 @381 逐字：`并非每个 kind 都需全字段`，并给出 `projection_vocabulary` 无 `latency_budget_delta` 的明例。
- 0.17.3 @402-405 把三者都列为 kind；0.17.3 @407 只说「新增 kind = 高影响」，未说三者不是方法条目。
- 0.17.4 @428 规定「条目任何机器层字段变更 = 完整 ADR + 批准」，正是 N-A 登记应走的路径。
- 0.17.6 @455 的 manual 兜底与 `profiles.yaml` @13-14 的 `provenance.origin = manual` 提供了登记形态。

风险：

- 若没有一句母本明文把「N-A 也是声明」说清，N-A 容易被读成「默认值假充」（@558 的担心）。
- 因此读法二必须配一条**范围澄清**，而不是只改数据。

### 对照表

| 判据 | 读法一（窄） | 读法二（宽） |
|---|---|---|
| 0.8 @199「每种方法条目」 | 仅 S1–S6 可选条目 | 0.17.3 全部 kind |
| 0.17.1 @313「投影规则」 | 需解释为注册表内容，非 0.8 范围 | 直接包含 PRJ |
| 0.17.2 @381「并非每个 kind 都需全字段」 | 可用，但不是主要依据 | 主要依据 |
| 0.17.3 @402-405 | 三者是 kind，但不是「方法条目」 | 三者都是方法条目 |
| 0.17.4 @415-420／@424／@428 | 按消费者排除 | 按消费者决定字段，不排除 kind |
| 新增判据 | 「是否进入 S1」 | 无（沿用 kind 剖面） |
| 主要风险 | 与 @313 冲突；PRJ 难自洽 | N-A 需显式依据，否则像默认填充 |

**结论：选读法二。** 它以 @381 的既有机制为支点，不新增「S1 准入」判据，也不与 @313 的「投影规则」枚举冲突；代价是必须把 N-A 写成显式豁免。

## 3. 推荐的最小自洽改写

### 3.1 拟插入文本（追加在 @381 同一行末尾）

> **0.8 包络义务的适用范围**：0.8 所称「每种方法条目」指 0.17.3 封闭枚举的全部 kind；kind 不以质量属性为选择判据时，其 `envelope` 与 `cost_profile` 可在本剖面登记为 `not_applicable`（逐项附 `reason` 引用本条、`provenance.origin=compiled`），此为显式豁免而非省略；本句只界定 0.8 包络义务，不改变其他字段的必填判定。

### 3.2 为什么这是「最小」

- 不新增 kind、字段、消费者、检查项或编号；只解释 0.8 的「方法条目」范围。
- 复用 0.17.2 @381 的 kind 剖面机制与 0.17.6 @455 的显式 provenance 形态；不新建通道。
- 只落在 @381 一行内：`split('\n')` 行数、代码围栏数、条款编号、其他表格行号均不变；对 0.22 锚点最友好。
- 明确「只界定 0.8 包络义务」，不把 `applicability`、`compatibility`、`constraints_imposed` 一并卷进来（这三项另按 §6 处理，不并入 R2）。

### 3.3 不推荐的替代写法

- 改 0.8 @199 加括注「（本条所称方法条目指……）」：直接改义务句，影响面大于 @381；且 0.8 是「校验机制条款」（@203），把 kind 范围写进义务句会与 0.17.2 的剖面机制重复。
- 把三 kind 直接写死为「不属方法条目」：与 @313「投影规则」冲突，且等于用 R2 重划 kind 语义，超出「歧义消解」。
- 在 @381 写「GRD／PRJ／GOV 一律 N-A」：这是 ADR 的数据裁决，不应写进母本；母本只给判据，具体 kind 由剖面登记。

## 4. 影响面清单

| 面 | 影响 | 处理 |
|---|---|---|
| kind | GRD／PRJ／GOV 三件获得 N-A 的母本判据；其余 14 kind 不受影响（其剖面 `envelope` 本就在 required，或已有明示 optional／N-A） | ADR 逐 kind 落数据 |
| 字段 | `envelope` + `cost_profile` 的 7 个子字段；**不含** `applicability`／`compatibility`／`constraints_imposed` | ADR 精确列 7 子字段（@416 精确匹配） |
| 既有条目 | 110 条中 GRD／PRJ／GOV 条目为 **0**；其余 110 条不受影响 | 无需回改 |
| 既有豁免 | STY-020…024 的 `C-ENV` 豁免 @98-103 保留；R2 只是给它一个更一般的依据，不回写 | 0.22：只登记不改写 |
| 既有 optional | DEC／OWN／CFG／VFM 的 `cost_profile.latency_budget_delta` optional（如 @129-132）不受影响 | 无需回改 |
| 检查 | M2 走 `not_applicable`；`C-ENV` 走 `entry_level_exemptions`；`META`／`C-ST` 要求剖面非 draft | ADR 必须同时改 `not_applicable` 与 `entry_level_exemptions` |
| 投影 | 本轮不改 registry，四件投影不动；R2 批准并改 profiles 后再重生成 | 下一轮 |

## 5. 行数／围栏／单行本／changlog 中性方案

### 5.1 母本

- 改前基线（2026-11-03 实测）：`split('\n')` = **4428**（即 4427 行 + 末尾空串）、代码围栏 = **216**、sha256 前 12 位 = `206c018ce309`。
- 改法：只在 @381 行末追加 §3.1 句，不新增换行。
- 改后断言：`split('\n')` 仍 4428；围栏仍 216；`git diff --numstat` = `1 1`；`git diff --word-diff` 只应出现 @381 的追加词。
- 若批准方要求独立成段，则允许 +2 行（空行＋段），但必须重跑上述断言并登记行号位移；**推荐同行追加**，避免位移。

### 5.2 单行本

- 以标题边界重抽（`## 全局约定` 至 `## 方面一` 前），不假定旧的 26–1302 范围不变（历史程序见 changelog @248）。
- 重抽后与旧单行本逐字 diff：只应出现 @381 句的差异；若范围变化，更新出处头；若范围不变，出处头不动。
- 单行本抽印段覆盖 @381（0.17.2 在 26–1302 内），必须同步；不得只改母本。

### 5.3 changlog

- 只在文件末尾追加一条「KP-G3 R2 提案起草」登记（0.22 承诺一：历史条目零改写）。
- 不插入旧条目中间，不改旧条目措辞。

### 5.4 全库围栏

- 本提案与 ADR 草案**不使用代码围栏**（只用表格、引用、行内代码）；`todo.md` 与 changelog 追加同样不带围栏。
- 预期全库 md 真围栏行仍 **368**（184 对）；以实测为准。

## 6. 依赖与未闭合项（不得并入本 R2）

### 6.1 头注 @13-14 与 GOV note @558 的冲突（必须先裁定口径）

头注允许 `provenance.origin = manual` 的无母本依据 N-A；@558 要求「需母本明文」。本提案按 R2 走，但若批准方认为头注优先，则三 kind 的 N-A 可以纯数据登记，R2 可降为「备而不用」。**建议在批准 R2 时同时裁定：是以头注为准（manual 可用），还是以 @558 为准（必须 R2）；不能两读并存。** 这是本提案发现的最重要的一致性问题。

### 6.2 PRJ `applicability.delivery_space`

- 不在 R2 文本内。ADR 的处理是「回到 `common_required` 默认必填」（`profiles.yaml` @35-40；0.17.2 @339-343；0.17.4 @417），**不按 N-A**。
- 若 M2 时某 PRJ 条目无法给出交付空间谓词，按 M2 失败处理，不得静默豁免；若批准方希望 N-A，则需第二条 R2 句，不能借本条掩盖。

### 6.3 其余未闭合

- `KP-G1` @562-567：0.18.4 缺 GRD／PRJ／GOV 的逐 kind 变体 → 影响 `selection_profile.variant`，不影响 `envelope`／`cost_profile` 的 N-A；归 s5e-10 后续或另案。
- `KP-G4` @580-584：`projection_vocabulary` 与 PRJ 术语不一致 → 影响 reason 措辞，不影响 N-A 决定；另案。
- 三件 `seed_source` 占位符 @486-487／@515-516／@547-548：属 M1／M2 数据，不是字段适用性；不在 R2 内。
- E3 Waiver 逐 kind 另起（防扩宽）：属 M2 之后，不在 R2 内。
- `entry_level_exemptions.scope` 的终值依赖 M1 批次定义的 `entry_id_range`（GRD 3 vs 9、PRJ 11 vs 16、GOV 6 vs 6+1）→ ADR 只能给形态，不能给假精确范围（0.4）。

## 7. 批准后执行步骤（本轮不执行）

1. 人类责任方批准 R2 文本（0.5 @127／@129；0.10 @235）。
2. 另起一轮：只改母本 @381 同行追加；按 §5 断言行数／围栏／单行本。
3. 改 `profiles.yaml` 三件（按 `ADR草案-GRD-PRJ-GOV-剖面变更.md`）；重生成四件投影；跑 `--check`／`--project`，记录 entries／checks／hard／soft／占位符／指针。
4. 更新 `registry/README.md` 相关计数与新增节（若需要）；按 0.22 只追加。
5. `todo.md` 与 changelog 登记执行结果；不 commit，待确认。

## 8. 本轮未改动清单

- 母本：零改动（4428 split／216 围栏／sha256 `206c018ce309`）。
- `profiles.yaml`：零改动（sha256 `0f225f62cc1e`）。
- `method_registry.yaml`／`predicate_vocabulary.yaml`／四件投影：零改动（并行 s5g 任务占用词汇表与投影）。
- 仅新增本文件、ADR 草案，并在 `todo.md`／changlog 追加登记；不 commit、不 push。
