# ADR 索引

> 本目录收纳全部架构决策记录（ADR）。**本文件是收纳之后唯一需要人工维护的清单**：新增／变更状态／取代关系时逐条登记，其余字段随 ADR 正文走。
> 历史文档中的旧路径引用按 0.22 保持 as-of，其映射见 §4。

## 1. 位置与命名规约

**位置＝仓库根目录 `adr/`。** 理由：ADR 同时约束母本条款与 `registry/` 实现，服务对象跨两者；`adr/` 与 `软件工程元框架成文法.md`、`registry/` 平级，正确表达「跨域治理记录」的位阶。`registry/adr/` 会把 ADR 错误限定为注册表专属（如 ADR-M5-01 改的是母本条款，与注册表数据无关）；`docs/adr/` 需新引入本仓库不存在的 `docs/` 层级，与现有扁平布局不一致。

**文件名＝`{ADR 编号}-{状态}-{YYYYMMDD}-{短标题}.md`。**

| 段 | 取值 |
|---|---|
| ADR 编号 | **原编号逐字保留，作为主键**（`ADR-README-01`、`ADR-LC-01`、`ADR-R2-APPL-01`…）。不重排全序：重排会使已推送历史、changelog、台账 evidence、其他会话记录中的编号集体失效，且 13 份 ADR 的编号已带领域前缀（`LC`/`R2-APPL`/`README`/`SRC`/`VG09`/`STY-FIM`/`M5`），已有可读语义 |
| 状态 | `draft`（草案）／`approved`（已批准）／`rejected`（已否决）／`superseded`（已取代）／`proposed`（已成形、待责任方裁定；2026-11-08 新增，用于只出方案不落地的 ADR） |
| 日期 | 批准日期（draft 则为起草日期），`YYYYMMDD` |
| 短标题 | 去标点、不加空格的中文短语；与 H1 标题可不逐字相同 |

**候选方案对比**（择一已采纳，其余记录理由）：

| 方案 | 形态 | 取舍 |
|---|---|---|
| **A（采纳）** | `{原编号}-{状态}-{日期}-{短标题}.md` | 编号即主键；状态与日期可排序可检索；不破坏任何既有引用 |
| B | `ADR-{000}-{状态}-{日期}-{短标题}.md`（全局重排） | 序号连续好看，但全量重排编号＝全仓引用与历史记录失效，违反 0.22 编号不复用／锚点纪律 |
| C | `{日期}-{原编号}-{状态}-{短标题}.md`（日期前置） | 便于按时间浏览，但按编号检索退化，且与现有 `ADR-*` 前缀惯例断裂 |

**状态 token 的判定来源**：以 ADR 正文的批准记录／changelog 批次／台账 `closure.ruled_by` 为准；三者矛盾时以台账与 changelog 的执行证据为准，并在 §3 记明。

## 2. 索引

| 编号 | 标题 | 状态 | 批准日期 | 被取代 | 影响的母本条款／注册表区段 | 文件 |
|---|---|---|---|---|---|---|
| `ADR-INLINE-MARK-01` | T2 五项行内标记方案（VFM／CFG／SCH／RLP／STY-4） | approved | 2026-11-04 | — | 母本 1.5(@1467)／5.2.3(@2484)／5.2.4(@2490)／5.2.6(@2510-2518)／5.5(@2564)／8.2.1(@3321)；`project.py` row_id 解析与 META；gaps `G-VFM-1`／`G-CFG-1`／`G-SCH-1`／`G-RLP-1`／`G-STY-4` | `ADR-INLINE-MARK-01-approved-20261104-五项行内标记方案.md` |
| `ADR-STY-FIM-01` | 框架内生元方法与 `provenance.source_class` | approved | 2026-11-07 | — | 母本 0.12／0.13／0.17.2（@335 `source_class`、@462 `origin`）／0.17.6／0.22；`project.py` `ENUM_ORIGIN` 与 `source_class` 校验；条目 `STY-021`／`STY-024`；gaps `G-STY-5`／`G-GOV-2`；SO-3／SO-24 | `ADR-STY-FIM-01-approved-20261107-框架内生元方法与source_class.md` |
| `ADR-VG09-01` | 母本谓词表一次性扩容（VG-09 十七名） | approved | 2026-11-06 | — | 母本 9.5 谓词表；`registry/predicate_vocabulary.yaml` `VOCAB`；gap `VG-09`（另记 `cycle_scale` 残余） | `ADR-VG09-01-approved-20261106-谓词表一次性扩容.md` |
| `ADR-VGEX-01` | VG-01～VG-08 谓词表扩容（20 名入表） | approved | 2026-11-07 | — | 母本 5.5(@2579)／8.5(@3435)／9.5(@3711)；`registry/predicate_vocabulary.yaml` 20 名与 VG-01～08 resolution；`node_role` 后置 | `ADR-VGEX-01-approved-20261107-VG01-08谓词表扩容.md` |
| `ADR-G-OWN-CSL-01` | G-OWN-1／G-CSL-1 行内出处补写（零插行母本改写） | approved | 2026-11-04 | — | 母本 4.2.1(@2166-2171)／4.2.3(@2186-2194)／4.7(@2431/@2432/@2435)；gaps `G-OWN-1`／`G-CSL-1` | `ADR-G-OWN-CSL-01-approved-20261104-行内出处补写.md` |
| `ADR-G-PRJ-1-01` | G-PRJ-1 有意保留悬空 | approved | 2026-11-06 | — | 台账 gap `G-PRJ-1`（保留理由与关闭条件）；`project.py` `GAP_SO_WHITELIST` | `ADR-G-PRJ-1-01-approved-20261106-有意保留悬空.md` |
| `ADR-KP-G3-01` | GRD／PRJ／GOV 三 kind 剖面变更（KP-G3 的 R2 落地） | approved | 2026-11-03 | — | 母本 0.17.2 @387 末句；`registry/profiles.yaml` `GRD`／`PRJ`／`GOV` 三剖面；`project.py` C-ENV 读 `entry_level_exemptions`；gap `KP-G3` | `ADR-KP-G3-01-approved-20261103-GRD-PRJ-GOV剖面变更.md` |
| `ADR-G-STY-ENV-01` | 接地编译前两闸（G-STY-1 三空间条件／G-ENV-1 指标映射） | approved | 2026-11-04 | — | 母本 1.2.1–1.2.4／1.3／6.2.1；0.18.2 S1；0.18.6 M15；0.17.7 门槛 2；gaps `G-STY-1`／`G-ENV-1`；SO-1 | `ADR-G-STY-ENV-01-approved-20261104-接地编译前置两闸.md` |
| `ADR-PRJ-2-01` | PRJ 交付空间谓词槽纠正（G-PRJ-2） | approved | 2026-11-04 | — | 母本 0.17.2 @342；10.2.2；`method_registry.yaml` 条目 `PRJ-001…PRJ-011`；gap `G-PRJ-2` | `ADR-PRJ-2-01-approved-20261104-PRJ交付空间谓词槽纠正.md` |
| `ADR-SRC-01` | 方案③：以 SRC kind 承载 9.2.3 九信号源 | draft | 2026-11-05（起草；方向 R1.0–R1.7 已批准） | — | 母本 0.17.3 kind 表（SRC 行，I-A）／0.17.4（I-B）／9.2.3；0.18.2 S1；`registry/profiles.yaml` SRC 剖面；gap `G-GRD-1`／SO-17 | `ADR-SRC-01-draft-20261105-9.2.3九信号源方案③.md` |
| `ADR-SRC-02` | 方案 A：0.17.2 增 `signals` 字段 | approved | 2026-11-06 | — | 母本 0.17.2 `signals`；`registry/profiles.yaml` 全 18 剖面；条目 `SRC-001…SRC-008`；gaps `G-GRD-1`（closed）／`G-SRC-1`（open） | `ADR-SRC-02-approved-20261106-signals字段方案A.md` |
| `ADR-LC-01` | 0.17.5 增补 `seed→draft` 迁移权限 | approved | 2026-11-07 | — | 母本 0.17.5 L451（已增补 `seed→draft`，同行）；总纲单行本同步；0.17.6／0.17.7／0.17.8 M5／9.2.1；`registry/CHECK-SPEC.md` C1 C-ST 行（§2.5 回落依据）；`method_registry.yaml` `status_transitions` 迁移记录 schema；`project.py` `check_ledgers`／`check_cst` | `ADR-LC-01-approved-20261107-seed到draft迁移权限.md` |
| `ADR-R2-APPL-01` | applicability 项级事实槽与问句式判据 | approved | 2026-11-06 | — | 母本 0.17.2 `applicability_item`（+5 行）；`project.py` `check_r2_applicability`；`profiles.yaml` 开关；130 条 `problem_space` | `ADR-R2-APPL-01-approved-20261106-applicability事实槽.md` |
| `ADR-README-01` | 子目录自检矩阵的授权边界与 README §5 公式拆解 | approved | 2026-11-07 | — | `registry/README.md` §5（迁入 `registry/CHECK-SPEC.md` C1）；`project.py` `check_m2`／`check_cenv`／`check_cst`／`SEED_CHECKS`；母本配套文件说明表 L21；`AGENTS.MD` L15 | `ADR-README-01-approved-20261107-子目录自检矩阵授权边界.md` |
| `ADR-M5-01` | M5（`narrative_sync`）软硬冲突裁决 | approved | 2026-11-07 | — | 母本 0.17.8 L500 行内追加（同行）；总纲单行本 L475 同步；`CHECK-SPEC` C1 M5 行；`ST-STY-01.condition`；`project.py` `check_m5`／`SEED_CHECKS` | `ADR-M5-01-approved-20261107-M5软硬冲突裁决.md` |
| `ADR-GAP-01` | 登记面下探与 gap 闭合规则（三态） | approved | 2026-11-07 | — | 0.12／0.17.7 门槛 6／0.17.8 M6；`ADR-STY-FIM-01` §5.5；gaps `G-CRD-1`／`G-DEC-1`／`G-CTR-1`／`G-STP-1`／`G-DFL-1`（均 closed）；SO-7～SO-11（均 closed） | `ADR-GAP-01-approved-20261107-登记面下探与gap闭合规则.md` |
| `ADR-STY-3-01` | `G-STY-3`／STY-012 的 MVC 行级外部出处补登记 | approved | 2026-11-07 | — | 母本 0.12 @11／@1869（编号 81、增补区 10.8）；书目 81；`method_registry.yaml` `STY-012`；gap `G-STY-3`；SO-3 | `ADR-STY-3-01-approved-20261107-MVC行级外部出处补登记.md` |
| `ADR-VG03-NR-01` | 节点角色谓词单族扩容（`node_role`，1 名） | approved | 2026-11-07 | — | 母本 1.5 @1479（+2 行，4,461→4,463；闭合围栏 @1480）；`registry/predicate_vocabulary.yaml` `node_role`（arity 2）与 VG-03 resolution；`method_registry.yaml` `STY-019-AP1` 改写（1 方括号）／SO-4 未闭合项 6→4 | `ADR-VG03-NR-01-approved-20261107-节点角色谓词单族扩容.md` |
| `ADR-VG02VG04-01` | VG-02／VG-04 残余四词裁决（R0 零母本改动） | approved | 2026-11-07 | — | 母本 **0 行**（载体 1.2.1 行 1348／2.2.3 行 1638／2.5 行 1724、行 1729／3.2.1 行 1929）；`registry/predicate_vocabulary.yaml` `schema`／`error_handling`（`kind: term`，arity 1）与 VG-02／VG-04 resolution；`method_registry.yaml` `STY-016-AP2`／`STY-011-AP1`／`STY-013-AP2` 改写（共 4 方括号）；SO-4 未闭合项 4→0 | `ADR-VG02VG04-01-approved-20261107-VG02-VG04残余词条款补写评估.md` |
| `ADR-STY015-P0-01` | V1 严格逐字读收口与 `STY-015-AP1` 升 P0 | approved | 2026-11-08 | — | 母本 9.2.1（第 3600 行，**0 行增减**，围栏 216 不变）／1.5 第 1474 行三族、第 1485 行 V1；`method_registry.yaml` `STY-015-AP1`（P1→P0）／`MJ-4` P0 判据／`G-STY-4` `correction_2026_11_08`／`SO-4` `decision_basis`；`registry/CHECK-SPEC.md` C2.4／C5.17／C6.3 | `ADR-STY015-P0-01-approved-20261108-V1严格逐字读与STY-015-AP1升P0.md` |
| `ADR-SRC-P0-02` | SRC 判据谓词批 A 登记与 signals 观测（S-10／S-11） | approved | 2026-11-08 | — | 母本 **0 行**；`predicate_vocabulary.yaml` +2 名（`metric_hit` predicate arity 1、`burn_rate` term arity 1）＋VG-06／VG-09 各记 `resolution_2026_11_08_bA`；`method_registry.yaml` `SRC-004-S1` 判据 `expiry`→`expiry_of`；`scripts/project.py` 增 S-10／S-11（info）与改判登记放行；`CHECK-SPEC.md` C5.18／C5.19 | `ADR-SRC-P0-02-approved-20261108-SRC判据谓词批A与signals观测.md` |
| `ADR-SRC-P0-03` | SRC 判据谓词批 B（8 名清单核对与 5 名登记） | approved | 2026-11-08 | — | 母本 **0 行**；`predicate_vocabulary.yaml` +5 名（`conforms_to` 2／`auth_bypass` 2／`monotonic_trend` 2／`remediation_or_waiver_record` 1／`consecutive_failure` 2，均 predicate）＋VG-09 记 `resolution_2026_11_08_bB`；`execution_order`／`assertion_fact_mismatch`／`burn_rate` 已在册不重复；8 条 SRC 机器层字符串**未改**；S-10／S-11 仍 info、命中 0／6 不变 | `ADR-SRC-P0-03-approved-20261108-SRC判据谓词批B.md` |
| `ADR-SRC-P0-04` | SRC 判据改写（6 detection＋3 when；`SRC-004-S1` 删 when 评估后停做） | approved | 2026-11-08 | — | 母本 **0 行**；`method_registry.yaml` 改 6 条 `detection_predicate`（S-11 6→0）与 3 条 `when_predicate`；`SRC-004-S1` 删 when 经评估有三处缺口（适用范围／Z6 支路／条款指代），**停做报裁**；`severity`／`raise_to` 未改；S-10／S-11 仍 info | `ADR-SRC-P0-04-approved-20261108-SRC判据改写.md` |
| `ADR-SRC-P0-05` | `behavior_switch` 登记与两条 when 护栏可判化 | approved | 2026-11-08 | — | 母本 **0 行**；`predicate_vocabulary.yaml` +1 名（`behavior_switch` predicate arity 1，出处 5.5 第 2600 行 Z6 量词域）＋VG-05 记 `resolution_2026_11_08`；`SRC-004-S1` when → `behavior_switch(flag)`（去独立 `∃`，自由变量回指 detection 绑定）、`SRC-007-S1` when → `distortion(system)`；三项护栏核对全通过；S-11 扩 when 干跑红 **0** | `ADR-SRC-P0-05-approved-20261108-behavior_switch与两条when护栏.md` |
| `ADR-SRC-P0-06` | M4 扩到 signals 两字段与 S-11 转硬 | approved | 2026-11-08 | — | 母本 **0 行**；`predicate_vocabulary.yaml` **零增删**（VG-09 记 `resolution_2026_11_08_bC`）；`scripts/project.py` `check_m4` 覆盖 `signals[].detection_predicate`＋`severity_condition.when_predicate`（扫描面 1,131→1,150），`check_signals` 的 S-11 **info→hard** 并覆盖 when、S-10 仍 info；`CHECK-SPEC.md` C1 M4 行／C5.13／C5.18／C5.20；`DATA-SPEC.md` D3.1；`method_registry.yaml` `G-SRC-1` **closed**（closure）＋5 处旧说明改写；`--check` 1,212 条｜硬 0｜软 0，零豁免 | `ADR-SRC-P0-06-approved-20261108-M4扩signals与S-11转硬.md` |
| `ADR-SRC-P0-07` | 元数校验（S-12）info 干跑与解析规则 | approved（仅 info 干跑；转硬未批） | 2026-11-08 | — | 母本 **0 行**；**数据零改动**（`method_registry.yaml`／`predicate_vocabulary.yaml` 无 diff）；`scripts/project.py` 新增 `extract_calls`／`split_call_args`／`vocab_arity_cached`／`check_arity`／`check_arity_census`，覆盖 4 个面 1,150 串；实测调用 **501** 处、元数不匹配 **43**（12 名）、无 arity 可校 **72**（formula_words）、解析可疑 **0**；归类 A 串写错 11／B 规则未覆盖 32／C arity 登记错 **0**；`CHECK-SPEC.md` 新增 C5.21（含 S-12 编号审计）；`--check` 1,235 条｜硬 0｜软 0 | `ADR-SRC-P0-07-approved-20261108-元数校验S-12-info干跑.md` |
| `ADR-SRC-P0-08` | S-12 转硬、显式占位与可变长槽 | approved | 2026-11-08 | — | `DATA-SPEC.md` 新增 D3.7（`·` 显式占位／写漏 vs 有意不约束／投影判据）、D3.8（variadic `argc ≥ arity`，N=6）；`CHECK-SPEC.md` C5.21 info → **hard**；`method_registry.yaml` **43 处**修补（23 `registry_entry` 槽位互换 + 6 实参、9 少参补 `·`、11 真错；语义变化 3 条：STY-001-AP1／STY-002-AP1／DPS-003-AP2）；23 条评估结论 **A**（无族级谓词）；72 处无 arity 记未覆盖分组；`--check` **1,214** 条｜硬 **0**｜软 **0**｜info **41**；零豁免；母本 0 行、`arity` 零改动 | `ADR-SRC-P0-08-approved-20261108-S12转硬与显式占位.md` |
| `ADR-SRC-P0-09` | 背景守卫移出检测式（23 条 `registry_entry` 恒真合取项清理） | approved | 2026-11-08 | — | `registry/method_registry.yaml` **23 条** `detection_predicate` 删除首合取项（`VFM-001…006` 各 AP）；`DATA-SPEC.md` 新增 **D3.9**（背景守卫不得入检测式）；`CHECK-SPEC.md` C5.21 追加口径；`--check` 1,214 条｜硬 0｜软 0｜info 41；S-12 调用 **501→478**、variadic **23→0**；零豁免 | `ADR-SRC-P0-09-approved-20261108-背景守卫移出检测式.md` |
| `ADR-SRC-P0-10` | `formula_words` 元数登记（四词 arity=1）与 `has` 的 B1 待裁表 | approved（四词已落地；`has` 九条**待签认未落地**；**复核后 §9：9 条全部落地、`has` arity=1**） | 2026-11-08 | — | `predicate_vocabulary.yaml` 四词加 `arity: 1`（`approved`／`declared`／`registered`／`sourced`），`has`／`compatible`／`now` 未动；`scripts/project.py` 新增 `mask_bracket_contents`（方括号整体占位计 1 实参）；`DATA-SPEC.md` 新增 **D3.10**；`CHECK-SPEC.md` C5.21 追加；`--check` 1,214 条｜硬 **0**｜软 **0**｜info 41；未覆盖 **72→16**（`has`×16）、固定元数 **406→462**；9 条 `has` 数据零改动、C 类 2 条单列。**§9 复核**：C 2 条改判为同一命题的规范化（`[五槽齐备](键)`／`[可求值的快照面](判据)`）、F 2 条改条件式（`[超时值变更](变更)`／`[快照比对记录](变更)`）、P 5 条一元化；`has` 登记 `arity: 1`；`--check` **1,213 条**｜硬 **0**｜软 **0**｜info **40**；未覆盖 **16→0**、调用 **478→474**、固定元数 **462→474**、无调用串 **881→883**。**§10 续批**：P 5 条 `has(parameter)`／`has(behavior)` 改条件式，`has` 余 **7** 处全为字段名（非字段名 **0**）；M4 与 S-12 共用 `mask_bracket_contents`（当前 0 差异）；调用 **469**、固定元数 **469**、无调用串 **888**、占位符 **1,483**、记录 **1,213**｜硬 0｜软 0｜info 40。**§11 续批二**：S-12 扩到方括号内「整段即单一调用式」（DATA-SPEC D3.11），豁免三类留痕（混合 26／通道号 3／投影 0），准入 47 处调用（元数不符 0，未在册 1 `shared_data_access`／CTR）；RLP-005 改 `timeout_budget(path, ·)`；**母本 5.5 @2575 二槽与 @2595 Z4 一实参矛盾登记为待办、未裁决**；硬 0／软 0，检查行 1,213→1,215（+2 info）。**§12 续批三**：`compatible` 登记 `arity: 2`（2.3 明定二元，0 调用，判定不变）；`now` 保持常量不登记 arity（理由入 D3.10）；三处造词暂不入册，改写方案 §12.3（STY-001 跳数表述／CTR-005 与 AP1 同形 `access_path`／DFL-004 批窗口长度），待批准后落地。**§13 执行**：三条全部落地（2B→1→3），CTR-005 改为 `dataset(D)`＋`access_path` 派生见证（补正理由：原见证 `a` 无来源，与 D3.9 背景守卫同型缺陷）；`depth` 只余 `bound_expr` 值位（不参与名注册／元数判定）；准入 47→46、不在册 1→0、豁免 29→**27**（预估 28 有误）、顶层调用 469→471、硬 0／软 0。**§14 P0 执行**：`blocking_registered` 按 R2 登记（`clause_defined_predicates`，arity 0，母本 @3738 G1 逐字）；D3.11 补「方括号内裸谓词名」识名通道（谓词头／实参值位／零元裸名按位置判）；双盲收单盲后检出裸谓词位 **22** 处、值位跳过 **14** 处、不在册 **8 名 21 处**（`ADR`×1＋RLP 族 `retry`／`backoff`／`jitter`／`fallback`／`circuit_breaker`／`half_open`／`bulkhead`），均只计 info；检查行 1,214→**1,216**、硬 0／软 0。**§15 P1 判据裁决**：不取 A／B，按 2.3 逐字读（对象有无「带 `status`／`lifecycle_state` 字段的注册面」三问）；B 以「覆盖面 +32」为据属以结论证前提、且会把 `registered` 退化为万能谓词，明确否掉，不得包装为「扩面」；逐条三问核对表另出，数据待批。**§16 三点裁定执行**：总规矩 S1–S5 立为 **DATA-SPEC D3.12**（改写不得悄悄改变判定强度）；① 26 处三分 = 换 `declared` **5**／降叙述 **11**／保留并标注 **10**（逐条核母本有无出处要求）；② 8 无注册面＋4 无状态一律降叙述；③ 5 条语义误用逐条「找到什么／没找到什么」（`property(hard)` @3448 未在册→降叙述×2；`fitness_function` @3437 在册→换谓词；`node_role` @1479 域不同→降叙述；`guard_rule.means` 是槽名→降叙述）；同型另 5 条；2.3c **6 处**统一后置式（**M4／S-12 都不识，覆盖增量 0**）；RLP **7 名 21 处**逐名改写为中文事实槽、不登记。数据侧检测串改写 **67 行**；`--check` **1,216** 条｜硬 **0**｜软 **0**；调用 477、准入 47／豁免 26、**裸谓词位 22→2**、**不在册 8 名 21 处→1 名 1 处**；母本 **0 行**、零豁免。**§17 框架缺口清单** → DATA-SPEC 附录 C：C.1 无注册面 **9** 项、C.2 有表缺 `status` **4** 项（不编号为谓词、不进词表）。**§18 残余敞口排序（仅方案，未落地，待批）**：①6 处后置式 `X registered`（M4／S-12 双盲＋对象无状态注册面 → AP 恒不触发＝假绿）列 P0，方案 B 数据侧先降叙述、A 检查器侧后立后置式识名通道；②`registered(键)`×3／`registered(项)`×1 配置注册表无 `status`，待核；③散文实参契约 1 处为观察项；④`ADR`×1 仅 info；⑤`property(hard)` 0 处使用；⑥母本 `timeout_budget` 元数矛盾未裁决。**§19 B／A 已落地（2026-11-08）**：B 6 处后置式按 S4 降为事实槽（逐条给「本应表／缺 `status`／母本是否设想登记面」证据），对象归入附录 C **C-14～C-17**（4 行覆盖 6 对象，`契约变更`＋`breaking_change` 合并、`漏洞` 两处合并）；A 新增 `postfix_sites()` 后置式识名通道（**名称不限 `registered`**，`approved`／`declared`／`sourced` 同通道；头部 argc=1 判 hard、对象内调用递归、不在册名只 info），新 info 行 `postfix_predicate_no_surface`（与「未覆盖」的区别写入 D3.13）。后置式 **6→0**，检查行 **1,216→1,217**，硬 0／软 0。**P1 复核**：`registered(键)`×3／`registered(项)`×1 的配置注册表五槽无 `status`（「生命周期」是值级 expiry，非条目状态）→ 同样不满足 2.3(a)，**本批未改**，建议降事实槽并立 C-18，待批。**§20 P1 执行**：4 处按 S2 降事实槽（CFG-001 AP1／AP2／AP5、VFM-001 AP4），原命题以「[该键／项已登记入配置注册表]」保留、否定位置不变；**C-18** 立入 `DATA-SPEC` 附录 C.2（4→5 项，写明「生命周期」为值级 `expiry`、补 `status` 属母本 5.2.6 实质变更须另走变更权、本批母本 0 行 diff）；影响面：补面之前这 4 条 AP **不可机械判定**，判定责任回人工，AP3／AP4 不受影响，补面后先 info 试跑再决定是否恢复 `registered`；新增 **S-13 文面完整性**（`)` 后紧跟 `(` 两类：合取／析取式后接主体无 bind 目标／双重调用或悬空施动，hard，数据 0 处）；`--check` **1,218** 条｜硬 **0**｜软 **0**｜占位符 **1,485**；母本 **0 行** diff、零豁免。 | `ADR-SRC-P0-10-approved-20261108-formula_words元数与has待裁.md` |
| `ADR-CFG-STATUS-01` | 母本 5.2.6 补「配置项条目状态」字段（加第六槽 `status`） | approved | 2026-11-08 | — | 母本 5.2.6 @2514（**1 行内改写，0 行增删**；加第六槽 `status`，与 0.17.2 同一词汇表，配置项启用 `{seed, active, retired}`，可消费 `{active, seed}`）；`编译规范.md` 2.3(a)（步 2）；`DATA-SPEC` C-18（步 3 闭合）；CFG-001／CFG-002／VFM-004 五槽表述（步 5）；4 条 AP 恢复（步 4）。**步 1 已落地**；0.17.2 五值枚举／0.17.5 迁移／18 条台账未动 | `ADR-CFG-STATUS-01-approved-20261108-5.2.6补条目状态字段.md` |
| `ADR-GS-C6-01` | 10.2.5 判据 6 改「三值状态声明」（取消能力前置；否决 `capability_undetermined` 触发器） | approved | 2026-11-08（起草并批准同日；三步落地见 ADR §8） | — | 母本 **6 处同行末追加、0 行新增、锚点位移 0**：10.2.5 @3994（判据 6 重定义）／@3996（依赖 `undetermined` 不标 `provisional`）、10.3 @4006（判定权拆两段）、10.5 @4032（`criteria6_verdicts` 字段表）、0.5 @129（「治理缺陷」标签分时态）、0.21.2 @973（`grounded`「正常产出」加限定，末词「无限制产出」）；落地提交 `cff8e75`／`661cc96`／`3625876`；`registry/` 数据零改动；不新增表／不改 0.21 状态机／不改检查器 | `ADR-GS-C6-01-approved-20261108-10.2.5判据6三值声明.md` |

**统计**：31 份；approved 30、draft 1（`ADR-SRC-01`）、proposed 0；无 rejected、无 superseded。

## 3. 状态存疑项（正文头部与执行证据不一致，已按证据裁定）

| 编号 | 正文头部写法 | 执行证据 | 裁定 |
|---|---|---|---|
| `ADR-G-OWN-CSL-01` | 「方向已获批准…落盘后执行」 | §5 记批准；changelog 2026-11-04 记执行；gaps `G-OWN-1`／`G-CSL-1` 已 closed | approved（2026-11-04） |
| `ADR-PRJ-2-01` | 「草案；条目未改写」 | changelog §4.18 记「人类批准…执行清单…本轮只改 method_registry.yaml」；gap `G-PRJ-2` 已 closed | approved（2026-11-04）；头部为执行前遗留 |
| `ADR-SRC-01` | 「草案；R1.0–R1.7 方向已批准；仍未落盘」 | 方向已批准；I-A（kind 行）／I-B 两行已落盘；其余待续 | **维持 draft**：文档未转 approved，批准仅及于方向 |
| `ADR-SRC-02` | 「草案；2026-11-06 已获人类责任方批准」 | §11 记批准并执行；`SRC-001…008` 已落地 | approved（2026-11-06） |

> 以上头部文本按 0.22 不改写；本表为状态权威读法。若将来统一正文头部，须另立变更批次。

## 4. 旧路径 → 现路径映射

迁移前的文件名（根目录平铺）与现名对照。历史文档（changelog、`todo.md`、`R2提案-*`、`adr/` 内 FROZEN 文件的 as-of 引用）保留旧名，按本表解析。

| 旧文件名 | 现文件名 |
|---|---|
| `ADR草案-行内标记方案-五项gap.md` | `ADR-INLINE-MARK-01-approved-20261104-五项行内标记方案.md` |
| `ADR草案-框架内生元方法-STY-021-024.md` | `ADR-STY-FIM-01-approved-20261107-框架内生元方法与source_class.md` |
| `ADR草案-谓词表一次性扩容-VG-09.md` | `ADR-VG09-01-approved-20261106-谓词表一次性扩容.md` |
| `ADR草案-G-OWN-CSL-行内出处.md` | `ADR-G-OWN-CSL-01-approved-20261104-行内出处补写.md` |
| `ADR草案-G-PRJ-1-悬空保留.md` | `ADR-G-PRJ-1-01-approved-20261106-有意保留悬空.md` |
| `ADR草案-GRD-PRJ-GOV-剖面变更.md` | `ADR-KP-G3-01-approved-20261103-GRD-PRJ-GOV剖面变更.md` |
| `ADR草案-G-STY-1-G-ENV-1-接地编译前置.md` | `ADR-G-STY-ENV-01-approved-20261104-接地编译前置两闸.md` |
| `ADR草案-PRJ交付空间-谓词槽纠正.md` | `ADR-PRJ-2-01-approved-20261104-PRJ交付空间谓词槽纠正.md` |
| `ADR草案-SRC-9.2.3九信号源-方案③.md` | `ADR-SRC-01-draft-20261105-9.2.3九信号源方案③.md` |
| `ADR草案-SRC-signals字段-方案A.md` | `ADR-SRC-02-approved-20261106-signals字段方案A.md` |
| `ADR-LC-01-seed到draft迁移权限.md` | `ADR-LC-01-approved-20261107-seed到draft迁移权限.md` |
| `ADR-R2-APPL-01-applicability事实槽.md` | `ADR-R2-APPL-01-approved-20261106-applicability事实槽.md` |
| `ADR-README-01-子目录自检矩阵授权边界.md` | `ADR-README-01-approved-20261107-子目录自检矩阵授权边界.md` |
| `ADR-GAP-01-draft-20261107-登记面下探与gap闭合规则.md` | `ADR-GAP-01-approved-20261107-登记面下探与gap闭合规则.md` |
| `ADR-CFG-STATUS-01-proposed-20261108-5.2.6补条目状态字段.md` | `ADR-CFG-STATUS-01-approved-20261108-5.2.6补条目状态字段.md`（起草同日批准） |
| `决策建议-M5-软硬冲突-2026-11-07.md` | `ADR-M5-01-approved-20261107-M5软硬冲突裁决.md`（原件已删除） |

## 5. 维护规则

1. **新增 ADR**：按 §1 命名，登记 §2 一行；若取代既有 ADR，被取代者文件名状态改为 `superseded` 并在其「被取代」列填后继编号。
2. **状态变更**：改文件名状态 token ＋ 改本表状态列；`draft` → `approved` 必须有批准记录（changelog 或台账 `closure.ruled_by`）。
3. **编号不复用**（0.22）：废弃编号永久保留于本表，不得回收。
4. 本文件是索引，不是规约；ADR 的效力以各自正文为准。
