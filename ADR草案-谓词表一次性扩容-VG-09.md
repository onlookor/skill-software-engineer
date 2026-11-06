# ADR-VG09-01：母本谓词表一次性扩容（VG-09 十七名）

- 状态：**approved（2026-11-06 批准；裁定 D1-A／D2-A／D3-A／D4-A／D5-A／D6-A／D7-A）**；决策类型：完整 ADR（0.13 高影响；母本条款文字变更）
- 范围声明：起草期为**零改动草案**（母本、`method_registry.yaml`、`predicate_vocabulary.yaml`、`profiles.yaml`、投影均未改）；批准后按 §10 执行，该批改动与本文同一笔提交入库。
- 上游：`G-SRC-1`（open）、`VG-09`（open，2026-11-06 登记，只登记不定义）。
- 硬约束：一次性完成，不接受分批；证据不足的族/名**明确排除**并留残余风险，不降格登记；编号不复用、历史只追加。

---

## 1 背景

### 1.1 卡点

`signals` 的 `detection_predicate` 需要可执行谓词名；`9.2.3` 只有自然语言信号描述（「DSM 跨边界密度」「错误预算燃尽率」「金字塔失真」），无谓词定义。`VG-09` 清点出 **17 个未登记名**（16 串判据）。M4 不扫 `signals`，故这些散文判据目前**不被 M4 校验**：不报错，也不可判定。

用户裁定：17 名**一次性**扩充母本谓词表，走 0.13 完整 ADR ＋批准路径；不做逐条小登记。

### 1.2 一个必须先纠正的前提

**母本没有「谓词表」这个表格。** 实测：

| 事实 | 值 |
|---|---|
| 谓词载体 | 各 `x.5` 形式化锚点节的**代码块**（如 `1.5` @1464–1473、`3.5` @1998–2006、`4.5` @2265–2276、`5.5`、`8.5` @3418–3428、`9.5` @3694–3704） |
| 行结构 | `name(arg1, arg2, …)  // 中文注释`，每行一名；无表头、无列 |
| 「列语义」 | **不存在**。若有人按「名称／语义／出处」三列理解，那是 `registry/predicate_vocabulary.yaml` 的投影形态，非母本形态 |
| 权威关系 | 母本 `x.5`＝权威；`predicate_vocabulary.yaml`＝数据侧投影（母本第 21 行自述「非权威」） |

因此「扩表」的实际动作是**在某个 `x.5` 代码块里加行**；零插行没有对应物（详见 §3.3）。

---

## 2 族划分（5 族，17 名）

处置三分：**进表**（新增谓词行）／**复合**（由既有母本谓词组合表达，不加新名）／**排除**（母本无定义载体，明确留残余）。

### 2.1 F1 度量与趋势族（4）

**语义边界**：判「可度量量的值、基线、时间窗趋势」；不判「阈值分级、整改动作、责任归属」。阈值与升级归 `9.2.1`／`T5`，不在此族。

| 名 | 处置 | 母本出处方案 | 说明 |
|---|---|---|---|
| `cross_boundary_density` | 进表 | `9.2.3` @3627–3628「DSM 通道一：跨边界调用密度」；**出处可挂，定义必须新写**（散文只给指标名，未给分母／口径／窗口参数） | 定义写在谓词行注释：`跨边界边数 / 内部边数` 按窗口聚合；`9.2.1` P2 的阈值与趋势判据消费它 |
| `baseline` | 进表 | `9.2.1` @3609 P2「相对基线漂移」；`0.17.7` 假精确门槛 | 定义：基线＝**登记值**（注册表或版本向量快照），不是运行时估计值；无登记值 → M15 勘察义务，不得默认 0 |
| `monotonic_trend` | **复合，不进表** | `9.5` @3696 `signal(..., trend_window_verdict)`＋`G7` @3732「threshold ∧ trend_window 双判据」 | 表达为：连续 N 窗口 `trend_window_verdict` 同向；`N` 为窗口参数，不另立名。**「连续 N 窗口」是 G7 已有的判定形态，不是新语义** |
| `cycle_scale` | **排除** | 无。`5.2.1` 只给「形成环／顺序语义缺失」，`1.5` 的 `cycle(forbidden_dependency)` 是**依赖环**，不是交互环规模 | 强行立名＝本地造义（违 0.4 条件 3）。残余：`SRC-001-S2` 的「环规模单调上升」暂不可判定，仅以散文＋`G7` 趋势面部分覆盖；`VG-09` 保留该残余 |

### 2.2 F2 结构与契约族（4）

**语义边界**：判「图结构（成环、顺序）、契约覆盖、覆盖层次」；不判「流量数值大小」（归 F1），不判「授权」（归 F3）。

| 名 | 处置 | 母本出处方案 | 说明 |
|---|---|---|---|
| `cycle` | **进表（改名 `interaction_cycle`）** | `5.2.1`「形成环」散文；`5.5` `interaction_flow` 已有 | **撞名**：`1.5` V1 已用 `cycle(forbidden_dependency)`。裸 `cycle` 进表会造成同名异义（0.22 编号不复用原则的同型风险）。改名 `interaction_cycle(graph)`，注释明示与 V1 的 `cycle` 不同指 |
| `execution_order` | 进表 | `5.2.1` @2199 附近「顺序/幂等/重复投递成为必答题」；`5.5` 有 `delivery_semantics` 面 | 定义：两交互间的偏序 `before(e1,e2)`；「未登记」由 `registered` 侧判定，不在本名内建 |
| `conforms_to` | **复合，不进表** | `3.5` X1 @2011：`∀ interaction(u1,u2): ∃C covers(C,u1,u2)` | 正是 X1 的**否定**：`connects(u1,u2,·) ∧ ¬∃C covers(C,u1,u2)`。再加一个 `conforms_to` 会与 X1 造第二真源 |
| `lower_layer_coverage` | **复合，不进表** | `8.5` `test_suite(S, layer, target_set)`＋`covers_check(property_id, …)`；`T5` @3439 散文 | 表达为 `∀p: hard(p) ∧ ¬∃S: test_suite(layer=lower, target ∋ p)`。T5 已用该形态，不另立名 |

### 2.3 F3 授权与追溯族（3）

**语义边界**：判「访问是否越权／决策是否可追溯」；不判「路径形态」（`access_path` 已有），不判「记录形态」（归 F4）。

| 名 | 处置 | 母本出处方案 | 说明 |
|---|---|---|---|
| `auth_bypass` | **复合，不进表** | `4.5` Y2 @2283：`access_path(D,c,…,C) ∧ registered(C) ∧ provider(C)=owner(D)` | 正是 Y2 的**否定**：`access_path ∧ (¬registered(C) ∨ provider≠owner)`。已有两名足够，新增即重复真源 |
| `traceable_to_fact` | 进表 | `0.3` 出处义务＋`0.4` 条件 3；`10.2.3` 血缘 | 定义：`decision.d` 的 `source_pointers` 非空且逐条可反查（与 `project.py` 的指针 miss 判定同口径） |
| `falsification_metric` | 进表 | `0.5` 保守假设 ADR 必含「可推翻指标」；`9.5` G8 @3733 | 定义：ADR 字段级谓词，`falsification_metric(adr, metric, threshold, window)`；`0.5` 只给义务，未给谓词名，故须新行承载 |

### 2.4 F4 记录与闭环族（4）

**语义边界**：判「记录是否存在、闭环是否完成」；不判「记录内容是否真实」（归 F5）。

| 名 | 处置 | 母本出处方案 | 说明 |
|---|---|---|---|
| `baseline_change_record` | **复合，不进表** | `9.5` `drift(D_approved, …, remediation_route)`；`baseline` 由 F1 新行提供 | 表达为 `baseline(m) ∧ drift ∧ ¬route_registered`。`drift` 已含「偏离必有闭环」（G6），不另立记录名 |
| `remediation_or_waiver_record` | **复合，不进表** | `9.5` `waiver(w, scope, deadline, …)`＋`debt_item(d, repayment_action, …)` | 表达为 `waiver(w, scope) ∨ debt_item(d, …)`。两名已在 9.5，新增即第三真源 |
| `supplement_evidence_record` | 进表 | `0.3` 出处登记；`0.17.7` M15 勘察义务 | 定义：`supplement_evidence_record(d)`＝补证工件已入库且指针可查；**与 `traceable_to_fact` 不同**：前者是**动作完成**，后者是**状态**，不可合并 |
| `metric_hit` | **复合，不进表** | `9.5` `canary_gate(strategy, metric, threshold, window)`；G4 @3726、G8 @3733 | 表达为 `canary_gate` 的 `threshold ∧ window` 判定产物；G4 已规定「非人工叙事」，不另立名 |

### 2.5 F5 验证证据族（2）

**语义边界**：判「证据与事实是否一致、失败是否连续」；不判「证据形态是否七要素齐备」（`T3` 已管）。

| 名 | 处置 | 母本出处方案 | 说明 |
|---|---|---|---|
| `assertion_fact_mismatch` | 进表 | `8.5` `evidence_artifact(E, seven_fields)`＋`verdict_of(E)`；`8.2.5` 触发 | 定义：`evidence_artifact(E) ∧ ¬matches(E, registered_fact)`；`matches` 不另立，作为本谓词内建比较（注释写清比较对象） |
| `consecutive_failure` | **复合，不进表** | `8.5` `test_suite`／`injection_case`＋`verdict_of(E)=fail`；`T9` @3446 | 表达为：同一 `case` 连续 N 周期 `verdict_of=fail`；`N` 为窗口参数。已有两名足够 |

### 2.6 计数

| 处置 | 数量 | 名单 |
|---|---|---|
| 进表 | **8** | `cross_boundary_density`、`baseline`、`interaction_cycle`（原名 `cycle`）、`execution_order`、`traceable_to_fact`、`falsification_metric`、`supplement_evidence_record`、`assertion_fact_mismatch` |
| 复合不进表 | **8** | `monotonic_trend`、`conforms_to`、`lower_layer_coverage`、`auth_bypass`、`baseline_change_record`、`remediation_or_waiver_record`、`metric_hit`、`consecutive_failure` |
| 排除 | **1** | `cycle_scale` |

**正面回答 0.4 条件 3**：`9.2.3`／`9.2.1` 的散文可作为**出处**（可追溯、可反查），但**不构成谓词定义**（无参数、无取值域、无判定边界）。因此 8 个进表名必须由**新谓词行的注释**充当定义载体（引出处条款＋写参数与边界），不允许写成「等价于 9.2.3 某句」了事。8 个复合名不需要定义载体，因为它们不新增语义，只写组合式。

---

## 3 载体与插行量

### 3.1 实际位置与现有行结构

候选载体：`9.5` @3694–3704 代码块（方面 9 的机器层谓词，信号面最近）：

```
3694 ```
3695 guard_rule(rule_id, monitored_predicate, level, means, params, obligation, waiver_clause, source_adr, version)
3696 signal(s, rule_id, value, t, trend_window_verdict)
…
3703 strangler_sequence(legacy_unit, steps, silent_period)
3704 ```
```

格式：每行一个谓词，`//` 后中文注释；**无表格列**。`9.5` 现有 9 行谓词、9 条性质（G1–G9）。

### 3.2 单块方案：8 行进 `9.5`（推荐）

插入点：`3704`（代码块闭合围栏之前），新增 **12 行**：

| # | 草案行 | 定义要点（注释全文见 §2 各表） |
|---|---|---|
| 1 | `# ── SRC 信号判据（VG-09 扩容；ADR-VG09-01）──` | 块内分节注释 |
| 2 | `cross_boundary_density(scope, window)` | 跨边界边数/内部边数，窗口聚合；引 9.2.3 @3627 |
| 3 | `baseline(metric, scope)` | 登记值快照；无登记 → M15；引 9.2.1 P2 |
| 4 | `interaction_cycle(graph)` | 交互有向环；**与 1.5 `cycle` 不同指**；引 5.2.1 |
| 5 | `execution_order(e1, e2)` | 交互偏序；「未登记」由 `covers`/`registered` 侧判 |
| 6 | `traceable_to_fact(d)` | `source_pointers` 非空且逐条可反查；引 0.3/0.4 |
| 7 | `falsification_metric(adr, metric, threshold, window)` | 保守假设 ADR 字段；引 0.5、G8 |
| 8 | `supplement_evidence_record(d)` | 补证工件入库且指针可查；引 M15 |
| 9 | `assertion_fact_mismatch(E)` | 证据断言 vs 在册事实；引 8.5 `evidence_artifact` |
| 10 | `# 复合式不进表：monotonic_trend／conforms_to／lower_layer_coverage／auth_bypass／` | 一行留痕，防止后人重复立名 |
| 11 | `# baseline_change_record／remediation_or_waiver_record／metric_hit／consecutive_failure` | 同上（续行） |
| 12 | `# 排除：cycle_scale（母本无定义载体；残余登记于 VG-09）` | 排除留痕 |

（第 1 与 10–12 行为注释行，不计谓词行；**正式谓词行 8 行**。）

### 3.3 零插行：判定为**不可行**

三条路径都堵死：

1. **行内追加**：把 8 个名字塞进既有行的 `//` 注释（如 `signal(...) // 另含 cross_boundary_density…`）。机器不可解析为独立谓词名，`project.py` 与后续 M4 都读不到；等于「有字无谓词」。
2. **并入已有谓词参数**：把 `cross_boundary_density` 当作 `signal` 的实参槽名。这是 `VG-04 (i)`／`VG-05 (i)` 已裁决的**槽名充谓词**反模式，直接复犯。
3. **只改 registry**：`predicate_vocabulary.yaml` 自述非权威（母本第 21 行）。只在投影里加名，母本无定义，违反 0.4 条件 3，且 M4 白名单会凭空放行。

`§10.3` 的「行号非权威」只解决**锚点漂移**，不解决**定义载体的有无**；不能用它替代插行。

### 3.4 对照方案：按方面分散进 `x.5`

把 8 名分回 `1.5`／`3.5`／`4.5`／`5.5`／`8.5`／`9.5`，总行数约 14–16 行、**6 个插入点**。语义上更贴方面归属，但锚点影响放大一个量级（§4），且 6 个插入点各产生 review 区间。代价对比如下。

---

## 4 锚点影响（实测，非估算）

演练副本（`/tmp/adr-sim`，母本＋registry 全量副本；真实仓库零改动）：

| 方案 | 插入点／行数 | 动锚 | 区间锚 | 位移端点 | `needs_review` | 空行落点 | 例外 |
|---|---|---|---|---|---|---|---|
| **A 单块进 9.5** | 3704／12 行（按 18 行实测同构推定；锚计数与行数无关，仅位移量差 6） | **569** | **53** | **622** | **5**（全部 `span_inside_insert`） | **0** | 演练未 `--apply` 报 622，属内容复核未执行；正式 `--apply` 须实测为 0 才算闭合 |
| B 分散 | 1473／4 行＋3704／8 行（分测相加） | 6,631＋569 ≈ **7,200** | 969＋53 ≈ **1,022** | 7,600＋622 ≈ **8,222** | 0＋5 ＝ **5**（其余 5 个插点未单独实测，按同型区间锚存在性另计） | 0 | 同上 |

- 5 条 review 全部是 `method_registry.yaml` 对 `@3694-3704`／`@3700-3714` 的区间锚（例：`method_registry.yaml:9632 @3700-3714`）。按 `§2.6`＋`§10.2` 第 1 条，**同批清零**：改条款锚（如 `@m:9.5`）或文字引用，不允许静默扩成 `@3694-3726`。
- **`2,244` 条 source pointer 需改字节数 = 0**：逐行核对 `569` 条动锚所在行，命中 `source_pointers` 的 46 处经抽样均为 `statement`／`note`／`narrative` 或 README 说明行，`value` 一律 `clause_id`／`row_id`／`bib_id`，**无行号形态**。
- 结论：方案 A 可由 `§2.6` 机械位移闭合；方案 B 也可闭合，但改动面约为 A 的 12–13 倍。

---

## 5 下游影响

| 面 | 影响 | 结论 |
|---|---|---|
| **M2** | 条目 schema 不变；S-1～S-9 不涉及谓词名 | **零改动** |
| **M4** | 现扫 `applicability`＋`anti_patterns.detection_predicate`，**不扫 `signals`** | **本轮不扩**（见 D5）；扩扫会让 16 串散文判据全红，属另一高影响变更 |
| **C-KP** | 剖面物化公式不变；`SRC` 的 `required_extra: [signals]` 不动 | **零改动** |
| **profiles** | 17 条 N-A 与 SRC 剖面均不涉及谓词名 | **零改动** |
| **vocabulary_gaps** | 9 条 → **仍 9 条**：`VG-09` 收窄为残余（`cycle_scale`＋「复合式的基词若后续要独立判定」），不关闭、不新开编号 | 见 D6 |
| **registry 投影** | 8 名需进 `predicate_vocabulary.yaml`（数据侧投影） | 批准后执行，非本轮 |
| **entries／checks** | 不加条目、不加检查 | 138／1,199 不变 |
| **占位符** | 新增行不用方括号（S-4 同口径） | 1,483 不变 |

---

## 6 执行清单（批准后）

| 步 | 动作 | 验收不变量 | 批准归属 |
|---|---|---|---|
| S1 | 母本 `9.5` 插 12 行（8 谓词＋4 注释行） | 母本 4,430→4,442；`git diff --numstat` 仅该文件 12/0 | **需整批批准**（本 ADR） |
| S2 | `anchor_shift.py` 机械位移；同批清零 5 条 review（改条款锚/文字引用） | 动锚 569±、`needs_review` 0、空行落点 0、例外 0 | 同上（已含在 S1 批准内） |
| S3 | `predicate_vocabulary.yaml` 加 8 名（source 指向 9.5，`verified: true`） | 在册名 76→84；指针 miss 0；M4 对既有条目零新增失败 | 自决（批准后） |
| S4 | `VG-09` statement **追加**收窄说明（不改原文） | 台账 `vocabulary_gaps` 9；`G-SRC-1` 保持 open | 自决 |
| S5 | 四件投影同一次 `--project` 重生成＋`--check`＋`anchor_index` | entries 138；记录 1,199；硬失败 0／软 0；指针 2,244→2,252／miss 0；占位 1,483；F-1 8,814；F-2～F-8 pass；`needs_review` 0 | 自决 |
| S6 | README 批次节＋changelog 追加 | 只追加不改写；一次性 commit | 自决 |
| S7 | （独立）M4 扩扫 `signals` | 另开 ADR，另批 | **逐项批** |

> S5 的指针数按「8 名 × 1 条 source」预估为 +8；以实测为准。

---

## 7 裁定点（集中拍板）

### D1 载体形态

| 选项 | 代价 | 推荐 |
|---|---|---|
| A 单块进 `9.5`（12 行） | 锚点 569／5 review；语义上「跨方面判据集中在 9.5」需要一行注释交代 | **推荐** |
| B 分散进 6 个 `x.5` | 锚点 ≈7,200／review 5–12；语义最贴方面归属 | 备选 |
| C 零插行 | 不可行（§3.3） | 否决 |

### D2 `cycle` 撞名

| 选项 | 代价 | 推荐 |
|---|---|---|
| `interaction_cycle`（改名） | 与 `VG-09` 原名不一致，须在 VG-09 追加映射 | **推荐** |
| 保留裸 `cycle` | 与 `1.5` V1 同名异义，后续读表歧义 | 否决 |
| 复合不进表 | 母本无「交互环」谓词，无法组合 | 不可行 |

### D3 复合式 8 名

| 选项 | 代价 | 推荐 |
|---|---|---|
| 复合不进表（写组合式） | 需在 ADR/注释里固定组合式；后人可能重复造名 | **推荐** |
| 全部进表 | 造 8 个第二真源，违「单一真源」；锚点 +8 行 | 否决 |
| 先补基础词再组合 | 需再登记 `registered`／`provider`／`matches` 等，范围外扩 | 不采纳 |

### D4 `cycle_scale`

| 选项 | 代价 | 推荐 |
|---|---|---|
| 明确排除、留残余 | `SRC-001-S2` 环规模不可判定，仅趋势面部分覆盖 | **推荐**（符合「不降格」约束） |
| 新增 5.2.1 条款文字后进表 | 需改 5.2.1 正文（方面 5 条款），影响面再扩一个方面 | 可另案 |
| 降格为普通缺口 | 违反用户硬约束 | 禁止 |

### D5 M4 是否同轮扩扫 `signals`

| 选项 | 代价 | 推荐 |
|---|---|---|
| 本轮不扩 | `signals` 仍不受 M4；已由 `G-SRC-1` 记录 | **推荐** |
| 同轮扩 | 16 串散文全红，须同时改写判据，工作量翻倍且混批 | 否决 |
| 永久不扩 | 与 `0.17.8` 校验面缺口长期并存 | 不采纳 |

### D6 `VG-09` 与 `vocabulary_gaps` 计数

| 选项 | 代价 | 推荐 |
|---|---|---|
| 保持 9 条、`VG-09` 收窄为残余 | 编号稳定，历史只追加 | **推荐** |
| 关闭 `VG-09`、新开 `VG-10`（仅 `cycle_scale`） | 编号 +1，需说明为何拆 | 备选 |
| 保持原文不动 | 与已登记的 8 名矛盾，台账失真 | 否决 |

### D7 批准粒度

| 选项 | 代价 | 推荐 |
|---|---|---|
| 整批一次批准（S1–S6） | 与「一次性」约束一致 | **推荐** |
| 按族分批 | 违反「不接受分批」 | 否决 |

---

## 8 残余风险

1. **8 个复合名不产生独立谓词**：`conforms_to`／`auth_bypass`／`lower_layer_coverage` 等若被后续条目直接引用为名，M4 会判「未登记」。缓解：ADR 与 9.5 注释各留一行「不得立名」。
2. **`cycle_scale` 排除**：`SRC-001-S2` 的规模趋势仍不可判定，属已登记残余（VG-09），不隐藏。
3. **单块进 9.5 的语义归属**：8 名中有 4 名语义属方面 3/4/8，放在方面 9 的块内，靠注释交代出处；若审阅要求「谓词必须落在所属方面 x.5」，则退到 D1-B。
4. **M4 缺口仍在**：本批只补词汇，不补校验；`signals` 仍无机器校验，直至 D5 另案。

---

## 9 参考与本轮状态

- 母本：`9.5` @3694–3704、`9.2.3` @3627–3628、`9.2.1` @3609–3623、`1.5` @1464–1484、`3.5` @1998–2020、`4.5` @2265–2287、`5.2.1` @2199 邻域、`8.5` @3418–3447、`0.3`／`0.4`／`0.5`／`0.17.7`／`0.17.8`、`10.2.3`。
- 注册表：`VG-09`、`G-SRC-1`、`predicate_vocabulary.yaml`（在册名 76，批后 84，见 §10）。
- 入库：本 ADR 由 draft 转 approved 后，与执行结果同一笔提交（文件范围与哈希见 `软件工程元框架成文法-changlog.md` 本批次记录）。

---

## 10 批准记录（2026-11-06）

| 裁定点 | 选定 | 落地结果 |
|---|---|---|
| D1 | **A** 单块进 `9.5` | 插 12 行（8 谓词＋4 注释行）；母本 4,430→4,442 |
| D2 | **A** 改名 `interaction_cycle` | 母本行、词汇表、`VG-09.renamed` 三处同步；未改 `1.5` 的 `cycle(forbidden_dependency)` |
| D3 | **A** 复合不进表 | `VG-09.resolution_2026_11_06.resolved_by_composition` 8 条结构化映射；`project.py` 增机器校验（每条 +1 自检记录，1,199→1,207） |
| D4 | **A** 排除 `cycle_scale` | `VG-09.resolution...residual` 一条；`vocabulary_gaps` 保持 9 |
| D5 | **A** 本轮不扩 M4 | 仅本节留句：M4 扩扫 `signals` 须另开 ADR（D5-C 路径），不新建文件 |
| D6 | **A** 保持 9 条、`VG-09` 收窄 | 编号不变，只追加 `resolution_2026_11_06` |
| D7 | **A** 整批一次批准 | S1–S6 同批执行、单笔提交 |

**执行口径**：机械位移实测 **579** 动锚（预估 569，差 +10＝本会话新增的 `VG-09`／README §4.27 中带行号引用的行数）；区间锚 53／端点 622 与预估一致；5 条 `span_inside_insert` 全部改为条款锚 `@m:9.5`，同批清零。

**行号注记**：§1.2／§3／§9 中的母本行号（如 `9.5` 3694–3704）为**批前基线**；批后定位以条款锚 `@m:9.5` 为权威，不按行号复算。
