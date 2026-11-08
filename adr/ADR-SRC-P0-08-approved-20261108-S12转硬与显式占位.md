# ADR-SRC-P0-08：S-12 元数校验转硬、显式占位与可变长槽

| 项 | 值 |
|---|---|
| ADR 编号 | **ADR-SRC-P0-08** |
| 状态 | approved（人类责任方 2026-11-08 经任务书授权；Agent 只执行、不自行裁定，0.10 第一条） |
| 日期 | 2026-11-08 |
| 决策类目 | 检查级别变更（S-12 info → hard）；数据面书写修补（43 处）；规范新增（DATA-SPEC D3.7／D3.8）；CHECK-SPEC C5.21 级别变更 |
| 前置 | `ADR-SRC-P0-07`（S-12 info 干跑与解析规则 R1–R9） |
| 影响面 | `registry/DATA-SPEC.md`（D3.7／D3.8）；`registry/CHECK-SPEC.md`（C5.21）；`registry/method_registry.yaml`（43 处 detection_predicate）；`registry/scripts/project.py`；`adr/INDEX.md`；changelog；**母本 0 行、`predicate_vocabulary.yaml` 0 改动** |
| 批准 | 人类责任方；两轮裁定见 §1 |

> **结论摘要**：23 条 `registry_entry(·, VFM-00x)` 的必要性评估结论为 **A（不需要族级谓词）**——它们是「本条目已登记」的作用域守卫，不是「整族存在」断言；按用户裁定改为 **6 实参** `registry_entry(VFM-00x, ·, ·, ·, ·, ·)`。43 处全部修补后，S-12 转 hard，`--check` **硬 0／软 0**，**零豁免、零新增例外、零 arity 改动**。

## §1 授权与范围

人类责任方 2026-11-08 两轮裁定：

1. **立规矩**：少给参数必须用 `·` 显式占位（`dsm(system)` → `dsm(system, ·)`）；裸缺参按错误处理，不再默认「投影」。投影只用于「引用某槽的具体值」，不得替代一次完整调用，须给判据。落点 = DATA-SPEC D3 + 本 ADR。
2. **修 43 条**：23 条 `registry_entry`、9 条少参、11 条真错；逐条给「原串 → 新串 → 语义是否变化」。
3. **可变长槽按 ≥N**：`fields...` 类尾部可变槽按「至少 N 个实参」判定；含可变槽的调用在报告中单列计数。**N = 6**（用户明示「≥ 6 那条已定」）。
4. **`·` 的语义**：`·` = 该槽有意不约束，与「少写一个实参」是两件事；前者合法、后者报错。凡补 `·` 处，ADR 须说明该槽为何可不约束。
5. **未覆盖**：72 处无 `arity` 的 `formula_words` 不计通过、不计失败，`--check` 报告单列分组。
6. **转硬**：修完 S-12 由 info 转 hard；验收硬 0／软 0，且不得靠豁免或新增例外；若红即停上报。
7. **23 条先评估再落地**：评估「该条目已登记」还是「整族条目全部存在」；不需要族级谓词则选 A、立即按 6 实参改完；需要则选 B、先给方案不登记。
8. **词表 `arity` 不许改**（C 类为 0，登记值与母本一致）。

## §2 三条规矩的落点

| 规矩 | 文件 | 小节 |
|---|---|---|
| `·` 显式占位；写漏 vs 有意不约束；投影判据 | `registry/DATA-SPEC.md` | **D3.7 显式占位与投影边界** |
| 可变长槽 `argc ≥ arity`；含可变槽调用单列计数 | `registry/DATA-SPEC.md` | **D3.8 可变长槽的 ≥N 判定** |
| S-12 由 info 改 hard；判定式、投影、未覆盖分组、编号审计 | `registry/CHECK-SPEC.md` | **C5.21 元数校验（S-12，hard）** |
| 决策、评估、43 条对照、被否方案与盲点 | 本文件 | §3–§9 |

## §3 23 条 `registry_entry`：必要性评估（结论 A）

### 3.1 判据

按用户给定三步取证：① 逐个 AP 看它抓的违规是「少了一个应该存在的条目」还是「某个已存在的条目字段／记录不全」；② 看否决条件需要什么前提；③ 看「整族存在」是否已由其他检查承担、是否已有消费者。

### 3.2 逐条判定面（VFM-001…006 共 24 个 AP）

| 条目 | AP | 想抓的违规 | 被约束的变量 | 是否需要「整族存在」 |
|---|---|---|---|---|
| VFM-001 | AP1 | 结构性硬性质只有叙事结论、无静态检查程序 | 单条性质 | 否 |
| VFM-001 | AP2 | 适应度函数在册而未接线到 CI | 单条检查 | 否 |
| VFM-001 | AP3 | DSM 通道二未在发布节点全量消费 | 单个发布节点 | 否 |
| VFM-001 | AP4 | 配置注册表比对缺项／版本非当前 | 单个配置项 | 否 |
| VFM-002 | AP1 | 叙事性结论触发或解除阻塞 | 单条结论 | 否 |
| VFM-002 | AP2 | T-F2 命中而未形式化为可执行检查 | 单个验证项 | 否 |
| VFM-002 | AP3 | 证据工件七要素不齐备即入库／被引用 | 单个工件 E | 否 |
| VFM-002 | AP4 | 工件无输入指纹或程序版本、不可重放 | 单个工件 E | 否 |
| VFM-003 | AP1 | 状态机硬性质以测试抽样替代模型检查 | 单条性质 | 否 |
| VFM-003 | AP2 | 模型检查结论无可重放工件 | 单个结论 E | 否 |
| VFM-003 | AP3 | 被检模型与实现漂移、未按触发条件重建 | 单个模型 | 否 |
| VFM-003 | AP4 | 覆盖性质集与已登记 Z 系列不对账 | 单个计划项 | 否 |
| VFM-004 | AP1 | 金字塔失真（层占比越限／覆盖率背离） | 单个计划项 | 否 |
| VFM-004 | AP2 | 集成层用测试替身而未登记 | 单条用例 | 否 |
| VFM-004 | AP3 | 已发布契约的契约测试缺项或未入 CI | 单个契约 C | 否 |
| VFM-004 | AP4 | 注入用例不覆盖卡片 `failure_modes` | 单个行为模式 | 否 |
| VFM-005 | AP1 | 五评审点之一被静默删减 | 单个评审点 rp | 否 |
| VFM-005 | AP2 | 评审记录未按七要素保全／不可重放 | 单条记录 E | 否 |
| VFM-005 | AP3 | 评审点按部署裁剪而未记 ADR | 单个裁剪项 | 否 |
| VFM-005 | AP4 | 材料性判定机械求值而无人工抽查 | 单次判定 | 否 |
| VFM-006 | AP1 | 行为模式已选用而观测面未满足卡片 | 单个模式（**无 registry_entry**） | 否 |
| VFM-006 | AP2 | 单点越阈即告警、无趋势窗口判据 | 单条告警 s | 否 |
| VFM-006 | AP3 | 放量／回滚判据以人工叙事替代注册参数 | 单次事件 d | 否 |
| VFM-006 | AP4 | 生产信号未登记入汇聚清单、无整改闭环 | 单个信号 | 否 |

### 3.3 否决条件分析

23 条的被否条件全部落在**绑定变量自身**的属性上：`¬[covers_check …]`、`¬registered(项)`、`¬executable(项)`、`¬fields_complete(E)`、`¬independently_verifiable(E)`、`¬[模型已重建]`、`¬[覆盖子集已声明]`、`¬[契约测试已入 CI]`、`¬[rp 已排期且记录保全]`、`¬[人工抽查记录]`、`¬[threshold ∧ trend_window]`、`¬parameterized(…)`、`¬registered(信号)`。

没有一条是「`∄ registry_entry(…)`」或「族中缺一条」。若原意是「族里有缺」，违规应表现为**条目级存在性缺失**，其否定也应在条目上，而不是在性质／检查／工件／用例／评审点／信号上。故否决条件不需要族级前提。

### 3.4 「整族存在」的消费者核查

- 条目身份与 schema：`C-ID`（身份前置）与 `M2`（0.17.2 schema）逐条判定；kind 封闭枚举见 0.17.3；剖面必填见 `profiles.yaml`。
- 现有检查中**没有**一条断言「VFM 族六条全部存在」；但这不构成缺口——23 条 AP 没有任何一条需要该断言。若未来治理层确需族级完整性，应落在 kind 级准入／基数检查（如 `kind_profile` 侧），而不是在 23 条检测式里重复同一族级谓词。
- 反证：若 `registry_entry(·, VFM-00x)` 真是「族级存在」，同一断言不会在 6 个条目的 23 个 AP 中逐条重复且各自绑定不同变量；重复的**自指 ID** 是「本条目作用域」的强证据。

### 3.5 结论

**选 A：不需要族级谓词，不登记新词。** 23 条的真实意图是「本条目 VFM-00x 已登记」的作用域守卫；`VFM-00x` 是条目 ID 而非 `kind`，原写法把 ID 塞进了 `kind` 槽（错类型），应做**槽位互换**。按 `registry_entry(E, kind, version, status, provenance, fields...)`（母本 @493）与 `arity: 6`、`variadic: true`，采用 **6 实参**：

```
registry_entry(VFM-00x, ·, ·, ·, ·, ·)
```

五个 `·` 依次为 `kind`／`version`／`status`／`provenance`／`fields...`。前四槽不约束的理由：`kind` 由 E 的在册记录唯一确定；`version`／`status`／`provenance` 与「是否存在」这一守卫目的无关。末槽 `fields...` 为空时按 D3.8 仍须显式占位，故写 `·` 而不是省略。

## §4 43 条逐条对照

> 「语义」列的判定口径：是否改变检测目标（抓什么违规），而非是否改变字面。

### 4.1 23 条 `registry_entry`（槽位互换 + 6 实参）

| # | AP | 行 | 原串 | 新串 | 语义 |
|---|---|---|---|---|---|
| 1 | VFM-001-AP1 | 9103 | `registry_entry(·, VFM-001)` | `registry_entry(VFM-001, ·, ·, ·, ·, ·)` | 错类型修正；目标不变 |
| 2 | VFM-001-AP2 | 9107 | 同上 | 同上 | 同上 |
| 3 | VFM-001-AP3 | 9111 | 同上 | 同上 | 同上 |
| 4 | VFM-001-AP4 | 9115 | 同上 | 同上 | 同上 |
| 5 | VFM-002-AP1 | 9195 | `registry_entry(·, VFM-002)` | `registry_entry(VFM-002, ·, ·, ·, ·, ·)` | 同上 |
| 6 | VFM-002-AP2 | 9199 | 同上 | 同上 | 同上 |
| 7 | VFM-002-AP3 | 9203 | 同上 | 同上 | 同上 |
| 8 | VFM-002-AP4 | 9207 | 同上 | 同上 | 同上 |
| 9 | VFM-003-AP1 | 9284 | `registry_entry(·, VFM-003)` | `registry_entry(VFM-003, ·, ·, ·, ·, ·)` | 同上 |
| 10 | VFM-003-AP2 | 9288 | 同上 | 同上 | 同上 |
| 11 | VFM-003-AP3 | 9292 | 同上 | 同上 | 同上 |
| 12 | VFM-003-AP4 | 9296 | 同上 | 同上 | 同上 |
| 13 | VFM-004-AP1 | 9404 | `registry_entry(·, VFM-004)` | `registry_entry(VFM-004, ·, ·, ·, ·, ·)` | 同上 |
| 14 | VFM-004-AP2 | 9408 | 同上 | 同上 | 同上 |
| 15 | VFM-004-AP3 | 9412 | 同上 | 同上 | 同上 |
| 16 | VFM-004-AP4 | 9416 | 同上 | 同上 | 同上 |
| 17 | VFM-005-AP1 | 9513 | `registry_entry(·, VFM-005)` | `registry_entry(VFM-005, ·, ·, ·, ·, ·)` | 同上 |
| 18 | VFM-005-AP2 | 9517 | 同上 | 同上 | 同上 |
| 19 | VFM-005-AP3 | 9521 | 同上 | 同上 | 同上 |
| 20 | VFM-005-AP4 | 9525 | 同上 | 同上 | 同上 |
| 21 | VFM-006-AP2 | 9620 | `registry_entry(·, VFM-006)` | `registry_entry(VFM-006, ·, ·, ·, ·, ·)` | 同上 |
| 22 | VFM-006-AP3 | 9624 | 同上 | 同上 | 同上 |
| 23 | VFM-006-AP4 | 9628 | 同上 | 同上 | 同上 |

### 4.2 9 条少参（补 `·`）

| # | AP／信号 | 行 | 原串 | 新串 | 语义 |
|---|---|---|---|---|---|
| 24 | SCH-001-AP2 | 6656 | `shared_write_exception(dataset(任务))` | `shared_write_exception(dataset(任务), ·, ·)` | 无（补 exit_plan／deadline） |
| 25 | SCH-003-AP1 | 6854 | `shared_write_exception(流程)` | `shared_write_exception(流程, ·, ·)` | 无 |
| 26 | SCH-003-AP3 | 6862 | `shared_write_exception(流程)` | `shared_write_exception(流程, ·, ·)` | 无 |
| 27 | VFM-006-AP1 | 9616 | `quality_impact_card(模式)` | `quality_impact_card(模式, ·)` | 无（补 card） |
| 28 | SRC-001-S1 | 11382 | `dsm(system)` | `dsm(system, ·)` | 无（补 metric 集） |
| 29 | SRC-001-S2 | 11392 | `interaction_flow(·)` | `interaction_flow(·, ·, ·)` | 无（补 participants／kind） |
| 30 | SRC-002-S1 | 11434 | `has_approved_exception(该交互)` | `has_approved_exception(该交互, ·, ·)` | 无（补 S2／exception_id） |
| 31 | SRC-005-S2 | 11581 | `baseline(metric)` | `baseline(metric, ·)` | 无（补 scope） |
| 32 | SRC-006-S1 | 11621 | `falsification_metric(adr)` | `falsification_metric(adr, ·, ·, ·)` | 无（补 metric／threshold／window） |

### 4.3 11 条真错（逐条改）

| # | AP | 行 | 原串 | 新串 | 语义变化 |
|---|---|---|---|---|---|
| 33 | DFL-001-AP2 | 5275 | `delivery_semantics(I)` | `delivery_semantics(I, ·)` | 无（补 semantics 槽） |
| 34 | RLP-002-AP2 | 5942 | `delivery_semantics(I)` | `delivery_semantics(I, ·)` | 无 |
| 35 | RLP-003-AP2 | 6041 | `delivery_semantics(I)` | `delivery_semantics(I, ·)` | 无 |
| 36 | RLP-004-AP3 | 6156 | `timeout_budget(path)` | `timeout_budget(path, ·)` | 无（补 allocations） |
| 37 | RLP-005-AP2 | 6265 | `timeout_budget(path)` | `timeout_budget(path, ·)` | 无 |
| 38 | RLP-005-AP4 | 6273 | `timeout_budget(·)` | `timeout_budget(·, ·)` | 无（path／allocations 均不约束） |
| 39 | DPS-002-AP1 | 9836 | `selection_log(d, ·)` | `selection_log(d, ·, ·)` | 无（补 consumed_entries） |
| 40 | DPS-004-AP3 | 10016 | `selection_log(G, ·)` | `selection_log(G, ·, ·)` | 无 |
| 41 | **STY-001-AP1** | 96 | `interaction_flow(path, sync_chain)` | `interaction_flow(path, ·, sync_chain)` | **有**：kind 从 participants 槽移入第 3 槽 |
| 42 | **STY-002-AP1** | 169 | `interaction_flow(u1, sync_chain)` | `interaction_flow(u1, ·, sync_chain)` | **有**：同上 |
| 43 | **DPS-003-AP2** | 9924 | `verdict(·, ·, ·)` | `verdict(·, ·)` | **有（轻）**：删去不存在的第 3 槽；判定目标不变 |

**语义变化三处的说明**：

- **STY-001-AP1／STY-002-AP1**：母本 @2569 的槽序是 `interaction_flow(F, participants, kind)`。原串把 `sync_chain` 放在第 2 槽，按定义会被读成「参与者是 sync_chain」，是**类型错误**；改后 `sync_chain` 落回 `kind` 槽，`participants` 显式不约束。检测目标（同步链上超时分层是否超深／查询调用是否被同步链拖住）不变，但**谓词真值的可判性**从错类型恢复为正确类型。
- **DPS-003-AP2**：`verdict(check_id, candidate_set)` 只有 2 槽（@2893）。原 3 实参中的第 3 槽无定义，属多余实参；删除不损失任何约束。判定目标（放量时观测窗未覆盖）不变。

## §5 `·` 逐槽「为何可不约束」

| 谓词（母本出处） | 槽位 | 本批补 `·` 的位置 | 为何该槽可不约束 |
|---|---|---|---|
| `registry_entry(E, kind, version, status, provenance, fields...)` @493 | kind／version／status／provenance／fields | 23 条，均在后五槽 | 守卫只断言「E 已登记」；kind 由 E 的在册记录唯一确定；version／status／provenance 与存在性无关；fields 可为空 |
| `shared_write_exception(D, exit_plan, deadline)` @2282 | exit_plan／deadline | SCH-001-AP2、SCH-003-AP1／AP3 | 条件只问「是否已有获批例外」；退出计划与截止时刻由该 AP 的后续分句单独检查 |
| `quality_impact_card(pattern, card)` @2577 | card | VFM-006-AP1 | 条件问的是该模式的 `observability_requires` 是否被满足；卡片载荷本身不参与判定 |
| `dsm(decomposition, {cross_density, feedback_loops, cohesion})` @1716 | metric 集 | SRC-001-S1 | 条件只问跨边界密度趋势；具体指标集不影响漂移判定 |
| `interaction_flow(F, participants, kind)` @2569 | participants／kind（SRC-001-S2 三槽全空） | SRC-001-S2 | 环检测对任意流程、任意参与者、任意协调方式成立 |
| `has_approved_exception(S1, S2, exception_id)` @1477 | S2／exception_id | SRC-002-S1 | 只问「该交互是否存在获批例外」；冲突对端与例外 ID 不影响存在性 |
| `baseline(metric, scope)` @3723 | scope | SRC-005-S2 | 漂移按 metric 判定；作用域聚合方式不影响「相对登记值漂移」 |
| `falsification_metric(adr, metric, threshold, window)` @3727 | metric／threshold／window | SRC-006-S1 | 只问该 ADR 是否登记了可推翻指标；具体指标、阈值与窗口不参与「是否登记」判定 |
| `delivery_semantics(interaction, semantics)` @2573 | semantics | DFL-001-AP2、RLP-002-AP2、RLP-003-AP2 | `¬declared(...)` 只问「是否声明」，不关心声明成哪一种投递语义 |
| `timeout_budget(path, allocations)` @2575 | allocations（AP4 两槽全空） | RLP-004-AP3、RLP-005-AP2／AP4 | 求和遍历该路径全部分配；AP4 只问「是否存在已登记的超时预算」，路径与分配均可为任意 |
| `selection_log(DP, steps, consumed_entries)` @495 | steps／consumed_entries | DPS-002-AP1、DPS-004-AP3 | 只问该决策点是否有选择日志；日志步骤与消费条目明细不参与存在性判定 |

## §6 72 处无 arity：未覆盖处理

| 分组 | 计数 | 处理 |
|---|---|---|
| `approved` | 8 | 不计通过、不计失败 |
| `declared` | 27 | 同上 |
| `has` | 16 | 同上 |
| `registered` | 18 | 同上 |
| `sourced` | 3 | 同上 |
| **合计** | **72** | `--check` 单列 `S-12／未覆盖` info 行，按名分组计数 |

理由：这些是 `formula_words`（公式约定词／运算符），词表本就不登记 `arity`；把它们按「恰好 N 元」判会凭空造 N，按「通过」判则掩盖可能的书写错误。故本批明确保留为**非判定面**，并在报告中显式披露（见 §9 盲点 4）。

## §7 S-12 转硬：验收与零豁免证明

### 7.1 转硬前后

| 项 | 转硬前（P0-07 终态） | 转硬后（本 ADR） |
|---|---|---|
| `--check` 记录数 | 1,235 | **1,214** |
| 硬失败 | 0 | **0** |
| 软警告 | 0 | **0** |
| info | 63（含 22 条 S-12 条目行＋1 条全量行） | 41（S-12 仅未覆盖 1 行） |
| S-12 元数不匹配 | 43 | **0** |
| S-12 解析可疑 | 0 | **0** |
| 投影（不计 arity） | — | **0** |
| variadic 调用／固定元数调用 | — | **23／406** |
| 无调用串 | 870 | 870 |
| 退出码 | 0 | **0** |

记录数变化：−22（S-12 逐条失败行消失）−1（旧 info 全量行）+2（新 hard 全量行＋info 未覆盖行）= **−21**，即 1,235 → 1,214。

### 7.2 零豁免证明

- 未改任何 `waivers`、`GAP_SO_WHITELIST`、例外表；未新增 `G-*` gap。
- 未在 `check_arity`／`check_arity_census` 中加入 `rep.skip` 或按条目白名单；42 条按数据修补消化，1 条（`verdict` 第 3 槽）按删多余实参消化。
- `predicate_vocabulary.yaml` 的 `arity` 零改动；12 个涉事名的登记值仍与母本定义一致（C 类 0）。
- 母本 `软件工程元框架成文法.md` 零 diff。
- 可变槽按用户裁定的 `argc ≥ 6` 判定，未以「恰好 6」或「≥5」放宽/收紧。

## §8 被否方案

| 方案 | 内容 | 否决理由 |
|---|---|---|
| A | 维持 info 干跑 | 用户裁定转硬；且 43 条已可判定，继续 info 只会积累账面噪声 |
| B | 23 条写成 2 实参 `registry_entry(VFM-00x, ·)` | 词表 `arity: 6`，转硬后必红 23 条；唯一变绿途径是例外或改 arity，二者均被禁 |
| C | 为 23 条新登记「整族存在」谓词 | 评估结论 A：无 AP 需要族级断言；新词无消费者，违反「不自行登记新词」 |
| D | 把 72 处 `formula_words` 判失败 | 它们本无 `arity`；判失败等于用不存在的期望值制造假红 |
| E | 改词表 `arity` 迁就数据 | 用户明令不许改；且 12 名登记值与母本一致，错在数据不在词表 |
| F | 给已知正确写法加 S-12 例外 | 违反「零豁免」验收；例外会掩盖后续真错 |
| G | 顺手修 `bound_expr`／注释里的 `Σ timeout_budget(path)` | 超出四个扫描面；本批只动 `detection_predicate`，避免扩大范围 |

## §9 盲点与残余风险

1. **投影只做语法识别**：`f(…).槽名` 被识别为投影并跳过 arity；「值位 vs 布尔位」「投影是否替代完整调用」的语义边界写入 D3.7，但机器不判。当前四个扫描面 0 处投影，故不影响本批。
2. **variadic 规则较粗**：`argc ≥ arity` 假定固定前缀槽全部必填、只有尾部可变。若未来出现「中部可选槽」或多段可变槽，本规则会误判；当前仅 `registry_entry` 一项 variadic。
3. **23 条守卫语义空转**：`registry_entry(VFM-00x, …)` 在条目已登记时恒真，对检测不增加约束力。形式与类型已正确，但「名字对、形式对、意思不对」的空间仍在；是否删除该守卫或改为作用域注解，另案处理。
4. **72 处未覆盖仍是账面盲区**：`approved／declared／has／registered／sourced` 的实参个数未被校验，可能隐藏书写错误；需另案决定「赋 arity」还是「归类为运算符不判」。
5. **`Σ timeout_budget(path, ·)` 的语义**：`·` 表示「全部分配」，但谓词无法区分「未登记分配」与「分配不约束」；M15／`registered` 侧需继续承担存在性判定。
6. **全角括号不解析**（P0-07 R6）：`timeout_budget（path）` 这类引文形态仍不判；当前仅母本引用处存在。
7. **同名多义**：母本 `verdict` 有 1 元与 2 元两种用法，词表只登记 2 元；S-12 以登记值为唯一期望，1 元用法会报错（本批未出现）。

## §10 批准记录

- 2026-11-08：人类责任方裁定「按上一轮的三个裁定执行，修完把 S-12 转硬」；同日补充「23 条按 6 实参形态走」「可变长槽按 ≥N」「`·` 的语义」「23 条先评估再落地」。
- 评估结论 A（不需要族级谓词）由本 ADR §3 逐条证据给出；按用户授权，选 A 后立即改完、不再等复审。
- Agent 只执行本 ADR 所列改动，未新增谓词、未改 `arity`、未加豁免。
