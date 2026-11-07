# ADR-VGEX-01：VG-01～VG-08 谓词表扩容（20 名入表）

| 项 | 值 |
|---|---|
| 编号 | `ADR-VGEX-01` |
| 状态 | approved |
| 批准日期 | 2026-11-07 |
| 影响级别 | 高（母本 x.5 条款正文＋词汇表投影；涉 4,747 处锚位移） |
| 关联条款 | 母本 5.2.6／5.5／6.5／8.5／9.5；编译规范 2.3；0.13（完整 ADR＋批准）；0.22 |
| 关联缺口 | `VG-01`～`VG-08`（`registry/predicate_vocabulary.yaml`）；`SO-4` |
| 前例 | `ADR-VG09-01`（一次性扩容／按族登记／拒绝槽名充谓词／可复合者走复合映射） |

## 1. 范围与判定依据

- **范围**：`VG-01`～`VG-08` 一次性扩容。**不含 `VG-03` 的 `node_role`**（后置，另立单族 ADR）。
- **判定依据**：①母本 x.5 逐字可查；②无逐字者，基词须在母本或词汇表内方可复合；③两者皆无者不立词，登记残余；④槽名／字段名／工件名／量词域不得充谓词；⑤既不重复母本已有谓词行，也不为凑数把已复合消解项入表。
- **规模**：真实缺口 34 词（剔除 13 个既有承载后），处置为入表 20／复合消解 19／既有覆盖更正 1／排除 3／残余 13（含后置 1）。

## 2. 决策

- **D1 配置治理族（VG-05，2 名入表）**：`expiry_of`（arity 1，term function）、`cleanup_filed`（arity 1），源 5.5。
- **D2 验证计划族（VG-07，13 名入表）**：9 名母本 8.5 已有逐字定义（`verification_plan`／`covers_check`／`test_suite`／`evidence_artifact`／`verdict_of`／`replayable`／`review_point`／`injection_case`／`fitness_function`），仅补词汇表投影；4 名新增（`retention_valid`／`cited_by`／`pyramid_distortion`／`distortion`）写入母本 8.5。
- **D3 部署策略族（VG-08，5 名入表）**：4 名母本 9.5 已有逐字定义（`deploy_strategy`／`canary_gate`／`evolution_path`／`strangler_sequence`）；`gate_verdict` 新增（G4 金丝雀门判定）。
- **D4 复合消解与排除**：`recorded_in` 改走复合（`decision_lineage ∧ cost_ledger`）；`selected` 为量词域，由 `selection_log` 承载；`review_period`／`expiry_date` 为参数而非谓词；`mapped` 属普查误判（`tactic(g,t)` 已覆盖），更正描述不入表。其余按 §3 表执行。
- **D5 VG-03 只做复合，`node_role` 后置**：方向三面以 `dependency_rule`／`layer_of`／`boundary_type`／`depends_on` 复合表达；`node_role` 边际成本 1,784 处锚／244 token（占活跃锚 24.9%）且只增行数不减跨点，另立单族 ADR。`affected` 清单补列 `STY-009-AP2`；`STY-009-AP1` 的转发／语义翻译／签名同构三项登记残余。
- **D6 承载面**：母本 x.5 正文与词汇表投影同步，不接受「只写词汇表」；母本改动走 0.13 完整 ADR＋批准。
- **D7 跨点裁定**：5 条跨越插入点的区间锚按「扩成」处理（§5）。

## 3. 逐词处置表（53 词）

### VG-01 部署类依赖（2）

| 词 | 状态 | 处置 | 依据 |
|---|---|---|---|
| `co_deployed` | 部分覆盖 | 复合 | `depends_on(u1,u2,deploy,·) ∧ depends_on(u2,u1,deploy,·)`；基词在册（2.5） |
| `independently_deployable` | 部分覆盖 | 复合 | 双向 `¬∃ depends_on(·, ·, deploy, ·)`；基词在册 |

### VG-02 粒度（2，全部残余）

| 词 | 状态 | 处置 | 依据 |
|---|---|---|---|
| `over_decomposed` | MISSING | 残余 | 母本无粒度判据与阈值；STY-016-AP2 仍靠方括号事实 |
| `responsibility_over_fragmented` | MISSING | 残余 | 同上，职责粒度判据无母本定义 |

### VG-03 方向（4）

| 词 | 状态 | 处置 | 依据 |
|---|---|---|---|
| 端口方向 | 部分覆盖 | 复合 | `layer_of(core,·) ∧ layer_of(ext,·) ∧ dependency_rule(core,adapter,forbidden) ∧ depends_on(core,ext,call,·)`；基词在册 |
| 环方向 | 部分覆盖 | 复合 | `dependency_rule(inner,outer,forbidden) ∧ depends_on(outer,inner,·)`；基词在册 |
| 模块边界方向 | 部分覆盖 | 复合 | `boundary_type`＋`layer_of`＋`depends_on`＋`contract`／`covers`（母本逐字可查） |
| `node_role` | MISSING | **后置** | 另立单族 ADR（锚成本 24.9%） |

### VG-04 契约形态（3）

| 词 | 状态 | 处置 | 依据 |
|---|---|---|---|
| `compat_policy` | 部分覆盖 | 复合（既有覆盖） | `contract(C,·,·,extension_point,·,·,·) ∧ has(C,compat_policy)`；槽名不充谓词 |
| `schema` | MISSING | 残余 | 是契约工件名（3.2.1），非 x.5 谓词 |
| `error_handling` | MISSING | 残余 | 母本无谓词载体；1.2.1 管道行仅自然语言反模式名 |

### VG-05 配置治理（8）

| 词 | 状态 | 处置 | 依据 |
|---|---|---|---|
| `expiry` | 部分覆盖（flag 第 4 槽） | 入表 `expiry_of`（term function） | Z6 需时刻比较；改名避免槽名充谓词 |
| `cleanup_filed` | MISSING | 入表 | Z6 第四支裸谓词，母本逐字 |
| `ADR` | 部分覆盖 | 复合 | `approved(adr) ∧ decision_lineage(adr,·,·)`；基词母本 7.5 可查 |
| 五槽「已登记」判据 | 部分覆盖 | 残余 | 类型／值域缺口，非谓词缺口 |
| `snapshot_changed` | MISSING | 残余 | 母本无比对函数、无快照工件名与采集口径 |
| `review_period` | MISSING | 排除（参数） | 由 `flag` 第四槽取值承载 |
| `expiry_date` | 部分覆盖 | 排除（参数） | 是 `expiry_of` 的返回值 |
| `zombie_flag` | 部分覆盖 | 复合 | `expiry_of(G) < now ∧ ¬cleanup_filed(G)` |

### VG-06 质量目标-手段闭合（13）

| 词 | 状态 | 处置 | 依据 |
|---|---|---|---|
| `consumed` | 部分覆盖 | 复合 | `∃p: card_consumed(p,card,·)`（6.5 在册） |
| `mapped` | **已覆盖（普查误判）** | 更正描述 | `tactic(g,t)` 与 Q6 同义；不入表、不改写既有文本 |
| `recorded_in` | 部分覆盖 | 复合 | `decision_lineage(adr,·,·) ∧ cost_ledger(x,·)` |
| `approved_waiver` | 部分覆盖 | 复合 | `∃w: waiver(..., approval=approved)` |
| `observability_requires` | 部分覆盖（字段名） | 残余 | 字段名充谓词属反模式；`satisfied` 无词 |
| `tactic_registry` | 部分覆盖 | 复合 | `∃t: tactic(g,t)`；集合名不立谓词 |
| `routed_to` | MISSING | 残余 | CH-B 路由通道语义无母本载体 |
| `weight_source` | 部分覆盖（goal 第 6 槽） | 复合 | `goal(g,·,·,·,·,weight_source,·)` |
| `band` | 部分覆盖（goal 第 7 槽） | 复合 | `goal(g,·,·,·,·,·,band)` |
| `defined` | 部分覆盖 | 复合 | `∃b: error_budget(service,slo,b,burn_rate)` |
| `monitored` | 部分覆盖 | 复合 | `∃s: signal(s,burn_rate,·,·,·)`（母本 9.5 可查） |
| `human_ruling_pending` | MISSING | 残余 | escalation 台账状态标记，非方法空间谓词 |
| `selected` | 部分覆盖 | 排除（量词域） | 由 `selection_log`（0.18.6）承载 |

### VG-07 验证计划（16）

| 词 | 状态 | 处置 | 依据 |
|---|---|---|---|
| 9 名机器层词（见 D2） | 母本有逐字、词汇表未投影 | 入表（不插母本行） | 8.5 @3424-3432（改前）逐字 |
| `retention_valid`／`cited_by`／`pyramid_distortion`／`distortion` | MISSING | 入表（插母本行） | T3／T5 判据，母本有语义无谓词名 |
| `seven_fields_complete` | 部分覆盖 | 复合 | `evidence_artifact(E,fields) ∧ fields_complete(fields)` |
| `scheduled`／`records` | 部分覆盖（review_point 第 3／4 槽） | 复合 | 槽绑定，不重复立名 |

### VG-08 部署策略（5，全部入表）

`deploy_strategy`／`canary_gate`／`evolution_path`／`strangler_sequence`（母本 9.5 逐字）＋`gate_verdict`（新增）。

## 4. 母本改动（3 处、10 行；4,451 → 4,461）

| 节 | 插入点（改前） | 插入内容 | 行数 |
|---|---|---|---:|
| 5.5 | @2577（`time_semantics` 行后、闭合围栏前） | 块头注释＋`expiry_of`＋`cleanup_filed` | 3 |
| 8.5 | @3433（`fitness_function` 行后、闭合围栏前） | 块头注释＋`retention_valid`＋`cited_by`＋`pyramid_distortion`＋`distortion` | 5 |
| 9.5 | @3709（VG-09 扩容块之前） | 块头注释＋`gate_verdict` | 2 |
| **合计** | — | — | **10** |

**与预演 23 行的偏差（重要）**：预演假设「20 名全部需在母本插行」，实测 **14 名母本已有逐字定义**（9 名在 8.5 @3424-3432、5 名在 9.5 @3704-3708），只有 **7 名**需插行；若照 23 行执行将产生 13 行重复谓词（违 0.22 不重复与「不重定义」）。故按 10 行落地。**受影响锚集合不变**（由插入位置而非行数决定），仅位移量由 +25／+19 降为 +10／+8。

## 5. 跨点裁定（5 条区间锚，按「扩成」）

| 锚 | 位置 | 改前 | 改后 | 理由 |
|---|---|---|---|---|
| 5.5 整节 | `registry/method_registry.yaml` | `@2564-2600` | `@2564-2603` | 块内 +3 |
| 5.5 谓词块（3 条） | `registry/method_registry.yaml` | `@2566-2577` | `@2566-2580` | 块内 +3 |
| 8.5 谓词块 | `registry/predicate_vocabulary.yaml` | `@3424-3452` | `@3424-3457` | 块内 +5 |

不选「重锚」（丢失「整块」语义）与「降 D3」（等于承认锚点管不了自身所在块）。

## 6. 锚点实测与预演偏差

| 指标 | 预演 A（25 行） | 预演 B（23 行） | 实测（10 行） |
|---|---:|---:|---:|
| anchors_changed | 6,531 | 4,747 | **4,747** |
| range_anchors | 923 | 645 | **645** |
| endpoints_shifted | 7,454 | 5,392 | **5,392** |
| collision_prefixed | 0 | 0 | **0** |
| exceptions | 0 | 0 | **0** |
| span_inside_insert | 5 | 5 | **5（已按 §5 扩成）** |
| blank_landing（位移集合内检出） | 16 | 4 | **4** |

实测与预演 B 逐项一致（同插入点）；与预演 A 的差 1,784 处即 `node_role` 后置的节省。**`blank_landing` 由 16 降为 4** 亦因 1.5 未插行（16 是 A 的更宽位移集合内的检出数，非「全库总数」——全库清扫未做，见 §9）。

## 7. 残余清单（13 行，本轮只登记不扩表）

| # | 名 | 族 | 为什么不立词 | 后续路径 |
|---:|---|---|---|---|
| 1 | `over_decomposed` | VG-02 | 无判据／阈值 | 母本 1.2.x 新条款 |
| 2 | `responsibility_over_fragmented` | VG-02 | 同上 | 同上 |
| 3 | `schema` | VG-04 | 工件名，非谓词 | 母本 3.5 补条款 |
| 4 | `error_handling` | VG-04 | 无谓词载体 | 母本 3.5／1.2.1 补条款 |
| 5 | 五槽「已登记」判据 | VG-05 | 类型／值域缺口 | 母本 5.2.6 补类型 |
| 6 | `snapshot_changed` | VG-05 | 无函数／工件／采集口径 | `G-CFG-1` route ① |
| 7 | `observability_requires` | VG-06 | 字段名充谓词 | 母本 5.2.5 补判据 |
| 8 | `routed_to` | VG-06 | 通道语义无载体 | 另开 ADR |
| 9 | `human_ruling_pending` | VG-06 | 台账状态标记 | 0.18.6 状态字段 |
| 10 | 转发 | VG-03（STY-009-AP1） | 不在方向面 | 单族 ADR |
| 11 | 语义翻译 | 同上 | 同上 | 同上 |
| 12 | 签名同构 | 同上 | 同上 | 同上 |
| 13 | `node_role` | VG-03 | 锚成本 24.9%，后置 | 单族 ADR |

**说明**：前表「11 项残余」含 `review_period`／`expiry_date`，按 D4 归入「参数排除」，故不在本表；另补 `node_role` 与 STY-009-AP1 三事实，净 13 行。`cycle_scale`（VG-09 残余）沿旧判，不随本批改判。

## 8. 被否方案

| 方案 | 内容 | 否决理由 |
|---|---|---|
| A | 含 `node_role`（21 名／25 行） | 边际 1,784 处锚／244 token（24.9%）且只增行数不减跨点 |
| 只写词汇表 | 母本零插行，21 名仅登记投影 | 违 D6 与 `ADR-VG09-01` D2「母本与数据侧同步」 |
| 重锚 | 5 条跨越区间改指新位置 | 丢失「整块」语义 |
| 降 D3 | 承认区间锚管不了插入 | 自指失效，后续无法校验块内新词 |
| 逐条小登记 | 每个词单独立 ADR | 反复小扩表，违 `ADR-VG09-01` 一次性扩充口径 |
| 并入参数 | 把 `expiry`／`schema` 等并入已有谓词参数 | 槽名充谓词反模式（`ADR-VG09-01` §2 已明确否定） |

## 9. 备查项

1. **`deployed_on` 三参／二参不一致**：1.5 定义为 `deployed_on(unit,node)`，DPS 批多处写作 `deployed_on(d,·,deploy)`。本批不改数据，记录待裁定。
2. **`blank_landing` 4 处**（本次位移集合内检出；预演 A 为 16 处）：既有锚落在空行，非本次插行造成；全库全量清扫未做，单列待办。
3. **母本谓词未投影于词汇表**：`contract`／`covers`／`decision_lineage`／`waiver`／`signal`／`evidence_artifact`／`review_point` 在母本有逐字定义但不在 `predicate_vocabulary.yaml`。本批只登记 VG 缺口面，未做全量对账（防范围蔓延）。
4. **不动既有 `detection_predicate`**：本批只补词汇，不改写条目谓词串；MJ-4「词汇补齐后升 P0」的复核随 VG-03 单族 ADR 一并处理。

## 10. 核验与落地清单

- 自检：1,213 条记录｜硬失败 0｜软警告 0｜占位符 1,483 处＝事实 1＋槽 1,482。
- 母本：4,461 行；围栏 216 不变。
- 词汇表：`predicates` 67→87、在册名 84→104；`vocabulary_gaps` 9 条，其中 8 条有 `resolution_2026_11_07`。
- 条目状态：138／138 seed 不变；gaps 24／SO 24 不变；open gap 2（`G-PRJ-1`／`G-SRC-1`）、open SO 3（`SO-1`／`SO-4`／`SO-6`）。
