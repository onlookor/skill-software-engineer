# 方法注册表（registry/）

本目录是**方法注册表的机器层权威源**（母本 0.17）与其同源投影。母本各方面 x.2 的方法空间表格是**种子数据源视图**，不是决策权威（0.17.1）；权威在本目录的条目。选型只消费条目（0.18 S1），守护只消费条目的 `anti_patterns`/`compatibility`（0.17.4 消费者二），编译以条目为编译单元（编译规范 2.4）。

目录布局的新增属 0.13 制度性决定（简记级），已登记于母本 changelog、母本"配套文件说明"表、AGENTS.MD 与本仓 README。

## 1. 文件清单

| 文件 | 职责 | 权威关系 |
|---|---|---|
| `profiles.yaml` | 17 个 kind 的字段剖面（元注册条目，0.17.2「字段完备性按 kind 剖面」、0.17.8 `kind_profile(kind, required_fields, optional_fields)`）＋剖面级缺口台账（KP-G1…G4，R2 澄清候选） | 数据侧权威；剖面变更走 0.13 |
| `predicate_vocabulary.yaml` | 母本机器层谓词清单的**数据侧投影**（供 M4 词汇封闭校验） | **非权威**：权威在母本 x.5／0.17.8／0.18.6／0.20.4／0.21.6／10.5；本文件每条带 clause 指针，`project.py` 反向核验指针在母本中可查 |
| `method_registry.yaml` | 方法条目本体（当前批次：STY 24 条＋OWN 4 条＋CSL 5 条＋CRD 8 条＋DEC 8 条＋CTR 12 条＋STP 4 条＋DFL 5 条＋RLP 7 条＋SCH 3 条＋CFG 4 条＋QAT 15 条，共 99 条）＋缺口台账＋状态迁移简记＋Waiver＋人工判断登记 | 数据侧权威（条目 schema 逐字采用 0.17.2） |
| `scripts/project.py` | 自检（M2/M3/M4/M5/M6/M9 ＋本目录登记的 C 系列）＋同源投影（0.9/E2：人类层由机器层生成，不手写） | 工具；不含规范命题 |
| `projections/*.md` | 生成物：人类可读投影视图＋自检报告 | **生成物，禁手改**；改源后重跑 `project.py` |

## 2. schema 采用声明与键名映射

条目 schema = 母本 **0.17.2 逐字采用**，不重定义、不扩展、不裁剪（编译规范 2.4）。YAML 侧仅做**键名书写映射**，语义零变更：

| 0.17.2 / 编译规范 2.1 | 本目录 YAML 键 |
|---|---|
| `provenance = {origin, 源指针}` | `provenance: {origin, source_pointers: [source_ref]}` |
| `source_ref = {source_type ∈ {clause_id, bib_id, row_id}, value, 核验状态}` | `{source_type, value, verified}` |
| `version`（语义版本 `{major, minor, patch}`） | `version: {major, minor, patch}` |
| `row_id`（表格行 ID） | `"{表号}-{行名}"`，如 `1.2.1-分层` |

**条目内不得出现 0.17.2 之外的字段**。注册表级信息（缺口、状态迁移简记、Waiver、人工判断登记、未闭合的冲突矩阵行）一律置于 `method_registry.yaml` 的**顶层节**，不进入条目。

## 3. 谓词书写约定（数据侧，M4/M15 校验对象）

1. **词汇封闭**：`applicability` 三空间谓词与 `anti_patterns.detection_predicate` 只能使用 `predicate_vocabulary.yaml` 登记的谓词名（编译规范 2.3「谓词名注册」：发现缺失 → R2 提议，**不得本地造词**）。缺失词汇登记为缺口（见 `gaps`）。
2. **语法**：联接 `∧`、析取 `∨`、否定 `¬`、蕴含 `→`、量化 `∀`/`∃` 前置、通配 `·`（编译规范 2.3 BNF）。
3. **事实占位符**：方括号 `[…]` 表示待勘察事实（如 `[关注点可按抽象级别自然切分]`）。占位符求值结果为 `unknown` 时按 **M15**：候选保留 ＋ 勘察义务登记，**禁沉默排除**（0.18.6）。`project.py` 统计占位符数量并输出勘察义务清单。
4. **公式约定词**（`approved`/`declared`/`registered`/`sourced`/`compatible`/`has`/`now`）按编译规范 2.3 内建语义表使用，不算白板谓词。
5. **三值语义**：`{true, false, unknown}`；两值实现 = 编译缺陷（编译规范 2.3(3)）。

## 4. 编号裁决留痕

### 4.1 STY 批（分块序）

母本反例 18-A 已发布引用 `STY-04（事件溯源）`。0.22 承诺一：编号一经发布永不复用、不重排。故 STY 批采用**分块序**（人工判断，`provenance.origin=manual`）：

| 块 | 母本源 | entry_id 区间 |
|---|---|---|
| 子维度三：通信/协调风格 | 1.2.3 | STY-001 … STY-006（**事件溯源+CQRS = STY-004**，与母本既有引用一致） |
| 子维度一：抽象/代码结构风格 | 1.2.1 | STY-007 … STY-013 |
| 子维度二：部署/运行单元风格 | 1.2.2 | STY-014 … STY-019 |
| 子维度四：风格选择元方法 | 1.2.4 | STY-020 … STY-024 |

书写形态统一为三位数字（`STY-004`）；母本 `STY-04` 为同一 entry_id 的既有书写形态，**母本零改动**，二者等价关系登记于此与 changelog。

### 4.2 DEC/OWN/CSL/CRD 四批（既有已发布引用解耦完毕）

四批的母本既有已发布引用勘察与裁决（2026-09-20，评审点五人类裁决人两次答复；判断全文见 `method_registry.yaml` MJ-13/MJ-14/MJ-15）：

| kind | 源表 | entry_id 区间 | 既有已发布引用的处置 |
|---|---|---|---|
| DEC | 2.2.1（8 行，S1…S8） | DEC-001…DEC-008（表序） | 正例 20-1 `DEC-05（事件驱动分解）` 与源表不一致（八策略表无该行）→ 裁决 = 表序入库 + **R2 修订母本示例**（最小自洽改写，5 处），DEC-005 = S5 按变更频率 |
| OWN | 4.2.1（4 行） | OWN-001…OWN-004（表序） | 正例 18-B 候选集与表序 1:1 一致，**母本零改动** |
| CSL | 4.2.3（5 行） | CSL-001…CSL-005（表行序） | 反例 18-A `CSL-03（最终一致流动机制）` 与表序不一致（CSL-03 = 因果一致）→ 裁决 = **R2 修订母本反例**为 `CSL-04（最终一致）` |
| CRD | 5.2.1（4 行）/5.2.2（4 行） | CRD-001…CRD-008（分块序） | 已发布 CRD-02（事件协同）= 5.2.1 行「协同（choreography）」（等同判断 MJ-14），表序直接满足，**母本零改动**；叙述式 CRD-Saga 非 entry_id |

书写形态同 §4.1：统一三位数字，母本两位数形态为同一 entry_id 的既有书写形态。母本 R2 修订（CSL 1 处 + DEC 5 处，0.22.3 措辞澄清通道，行数 4426/围栏 216 不变）与单行本同步 6 处已执行，详情见成文法 changlog 2026-09-20 条目。后续其余 kind 批次（CTR/STP/DFL/RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）的编号仍须先解母本既有已发布引用（如有），模式同本节。

### 4.3 CTR 批（表序入库，母本零改动）

母本既有已发布引用勘察结论（2026-09-27）：**母本全文无 `CTR-数字` 形态的已发布引用**（与 STY 反例 18-A `STY-04`、CSL 反例 18-A `CSL-03`、CRD `CRD-02`、DEC 正例 20-1 `DEC-05` 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。3.6 三处 `CTR` 前缀书写均为**消费字段称呼、非 entry_id**（判断全文见 `method_registry.yaml` MJ-21 (i)(ii)(iii)）：

| 母本称呼 | 出处 | 映射 |
|---|---|---|
| `CTR-gRPC` | 3.6 示例一（@2031 事实集内 `contract(gRPC, …)`；@2035 `CTR-gRPC.envelope.latency_bound`） | 3.2.1「同步 API 契约」行 = **CTR-002**（叙述式书写 ≠ 三位 id，等同判断承 MJ-14） |
| `CTR.compatibility.policy`（additive-only/backward/full） | 3.6 示例二消费字段（@2049-2050） | 策略值落 **CTR-008**（3.2.2「兼容性规则」行）；其**取值枚举与登记面**属 **CTR-007**（「版本化策略」行），二者不合并 |
| `CTR.lifecycle_state`（published/deprecated） | 3.6 示例三消费字段（@2064-2065） | **CTR-010**（3.2.2「契约生命周期」行） |

编号方案＝**两表分块序**（承 §4.1 的分块序形态）：

| 块 | 母本源 | entry_id 区间 |
|---|---|---|
| 契约形态（六形态） | 3.2.1（六行 @1918-1923） | CTR-001 … CTR-006（进程内接口／同步 API 契约／异步消息契约／事件契约／数据契约／UI-端契约） |
| 契约治理（六维度） | 3.2.2（六行 @1931-1936） | CTR-007 … CTR-012（版本化策略／兼容性规则／消费者驱动契约测试（CDC）／契约生命周期／破坏性变更流程／发现与注册） |

采分块序而非单一混合行序的理由：两表在母本为并列的两张表（形态面／治理面），3.2.2 内容列明记「每契约登记其一」即治理维度对全部形态正交适用，混编会使「形态 → 治理」的施加关系在 id 面上不可读；块内行序即 id 序，块序按母本小节序。`name` 一律取表首列逐字（含母本自带括注）。0.18.4「契约形态（3）」行（@589）的三点规程变体要点（S2 消费风格硬约束（1.4 接收）／S4 检验 X 系列／CDC 要求按 X4 分级入 cost_profile）已由 `profiles.yaml` 的 `kind_profile_CTR.selection_profile.variant` 承载，不参与编号裁决。

§4.2 末段的批次清单（含 CTR）系该时点的预告面，本批入库后**不回改该句**（0.22 承诺一同型：已发布文本以新增登记留痕，不以改写消解差异）；其余 11 kind（STP/DFL/RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用「先解母本既有已发布引用（如有）」的同一模式。

### 4.4 STP 批（单表表序入库，母本零改动）

母本既有已发布引用勘察结论（2026-09-27）：母本全文 `STP` 仅**两处**——@393（0.17.3 kind 封闭枚举行「STP｜存储拓扑｜方面 4 · 4.2.2」）与 @2346（4.6 示例三【形式化注释】的消费字段行「STP/R 阈值注册表（P99）」）。**无 `STP-数字` 形态的已发布引用**（与 STY/CSL/CRD/DEC 四批不同，同 CTR 批），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。@2346 的 `STP/R` 系**消费字段称呼、非 entry_id**（判读承 §4.3 CTR 批对 3.6 三处称呼的同型处置，MJ-21 (i) 同型）。

编号方案＝**单表表序**（承 §4.2 的 MJ-13 (iv) 同型：4.2.2 为一张表，行序即 id 序）：

| entry_id | 母本源行（4.2.2，@2175-2178） | name（取表首列逐字） |
|---|---|---|
| STP-001 | 第 1 行 | 每服务自有数据库 |
| STP-002 | 第 2 行 | 共享数据库 |
| STP-003 | 第 3 行 | 事件日志为权威状态 |
| STP-004 | 第 4 行 | 多语言持久化 |

`profiles.yaml` 的 `kind_profile_STP.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实。三列源表（拓扑｜定义｜与风格的关系）到条目字段的归类判读、`latency_budget_delta` 一律填实的依据、`compatibility` 七行的方向与级别、`constraints_imposed` 28 项的级别分布（与 CTR 批施→8 取 conditional 的差异据实记载）、`references` 的行级/性质级定性、谓词面精确事实（4.2.2 侧七词不入 M4 扫描面 ＋ 母本 4.5 公式七词缺口）与 **Read 工具行号偏一的据实记载**，全文见 `method_registry.yaml` MJ-22 (i)–(vii)。

行级书目登记面：母本 4.7（@2427-2437）九项中**行级**可引者仅书目 37（→ STP-003）与 38（→ STP-004），故 STP-001／STP-002 的 `references` 为**空列表**（M6 平凡通过，非豁免）；缺口登记 `G-STP-1` ＋ 勘察义务 `SO-10`。E3 豁免 `WV-STP-E3-01`（5 项 11 实例）已于 **2026-09-28** 经人类裁决批准、`status: active`（申请登记 2026-09-27，跨 1 日；裁决全文见台账 `approval.ruling`）；七项 Waiver 全部 active，累计覆盖 **65** 条 seed、scope 互不重叠。§4.2／§4.3 末段的批次清单（含 STP）同样**不回改**；其余 10 kind（DFL/RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.5 DFL 批（单表表序入库，母本零改动）

母本既有已发布引用勘察结论（2026-09-28）：母本全文 `DFL` 仅**一处**——@395（0.17.3 kind 封闭枚举行「DFL｜数据流动机制｜方面 4 · 4.2.4」）。**无 `DFL-数字` 形态的已发布引用**（同 CTR／STP 两批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**单表表序**（承 §4.2 的 MJ-13 (iv) 同型：4.2.4 为一张表，行序即 id 序）：

| entry_id | 母本源行（4.2.4，@2198-2202） | name（取表首列逐字） |
|---|---|---|
| DFL-001 | 第 1 行 | 事务性发件箱（outbox） |
| DFL-002 | 第 2 行 | 变更数据捕获（CDC） |
| DFL-003 | 第 3 行 | 流处理 |
| DFL-004 | 第 4 行 | ETL/ELT 批（母本首列原形即含斜杠 → 按 MJ-21 (iii) 原形登记，不改写为术语表 @4283 的「ETL / ELT」形态） |
| DFL-005 | 第 5 行 | 物化视图 |

`profiles.yaml` 的 `kind_profile_DFL.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实。四列源表（机制｜定义｜适用条件｜质量影响要点）到条目字段的归类判读、CDC 一词在母本的双义隔离（数据域 @4277 归 DFL-002／契约域 @4278 归 CTR-009）、`latency_budget_delta` 五条一律填实但理由不平移 STP 批措辞、22 条 `signal_level` 的定级依据（P0 11／P1 5／P2 6）、谓词面精确事实（本批 11 个调用词全部已登记 → 零新增候选，累计仍 19 词）、`formal_anchor` 12 实例的角色分配、`compatibility` 十行（composable 8／tension 2）与 RLP 批重叠处置、6.6 示例四 800ms 不入 `bound_expr` 的边界、书目 44 的 ISBN 观察项、同批镜像与 `pending_conflict_rows` 口径，全文见 `method_registry.yaml` MJ-23 (i)–(xi)。

行级书目登记面：母本 4.7（@2427-2437）九项中**行级**可引者仅书目 42（→ DFL-001 发件箱）与 43（→ DFL-002 CDC），覆盖 5 行中 2 行，故 DFL-003／DFL-004／DFL-005 的 `references` 为**空列表**（M6 平凡通过，非豁免）；缺口登记 `G-DFL-1`（含五个下探裁决口①-⑤，其一为书目 44 本地 EPUB 的 isbn13 与母本 @2750 著录形态不一致的处置）＋勘察义务 `SO-11`。E3 豁免 `WV-DFL-E3-01`（硬性质面 **3 项 6 实例**：Z2 3／Y2 2／Y1 1；软性质 Y4 5 实例＋Y7 1 实例**明列排除**）已于 **2026-10-04** 经人类裁决批准、`status: active`（申请登记 2026-09-28，跨 6 日；裁决全文见台账 `approval.ruling`）；八项 Waiver 全部 active，累计覆盖 **70** 条 seed、scope 互不重叠。§4.2／§4.3／§4.4 末段的批次清单（含 DFL）同样**不回改**；其余 9 kind（RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.6 RLP 批（行内清单序入库，母本零改动）

母本既有已发布引用勘察结论（2026-10-05）：母本全文 `RLP` 仅**一处**——@397（0.17.3 kind 封闭枚举行「RLP｜可靠性模式｜方面 5 · 5.2.3」）。**无 `RLP-数字` 形态的已发布引用**（同 CTR／STP／DFL 三批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**行内清单序**（本库首例：骨架源非表格）：母本 5.2.3（heading @2475）的注册表条目清单在 **@2477** 以『注册表条目（每条带质量影响卡片）：』引导、分号分隔七项，无 4.2.2／4.2.4／3.2.1 类的表格行列结构，故七条 `source_pointers` 一律 `{source_type: clause_id, value: "5.2.3"}`（＋bib_id），**不含 `row_id` 维度**；id 序即 @2477 的列举序：

| entry_id | @2477 列举序 | name（取各项引导词逐字） |
|---|---|---|
| RLP-001 | 第 1 项 | 幂等 |
| RLP-002 | 第 2 项 | 收件箱（inbox） |
| RLP-003 | 第 3 项 | 发件箱（outbox） |
| RLP-004 | 第 4 项 | 重试 + 指数退避 + 抖动 |
| RLP-005 | 第 5 项 | 超时预算 |
| RLP-006 | 第 6 项 | 断路器 |
| RLP-007 | 第 7 项 | 舱壁 |

`profiles.yaml` 的 `kind_profile_RLP.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实。非表格源的 `provenance` 口径（不含 `row_id`、`name` 取引导词逐字）、书目 46 以「等」概括覆盖「重试」而书目 51 目录面只作工程参照、@2719 六项／@2730 五项与 @2477 七项的枚举差异处置（以 @2477 为准、不本地合并；@2732 的 800ms 系现状测量值不入 `bound_expr`）、DFL-001↔RLP-003 发件箱重叠的**定义面归 DFL／行为面归 RLP** 兑现（单向 `requires` ＋ RLP-003 envelope 只 3 族）、`formal_anchor` 20 实例与 Waiver scope 的对位、M4 四词六行改写落点（@5617／@5984／@6029／@6090／@6086／@6204，不本地扩表）、M9 同批镜像补登两处（`compatibility` 30→32，不对称累计第三例）、`aggregation_semantics` 首次出现 `additive`（RLP-004／005，母本明文求和语义）、方面 8 `conditional` 首次成批使用（表源＝**5.4**『施加约束』@2543-2553，与前八批所引 **4.4** 表 @2251-2257 系两张同名不同源的表，不得混引）、32 条 `signal_level` 定级（P0 11／P1 13／P2 8）、书目 46 的 ISBN 分组与页数两说据实登记不改写，以及**本批四处自我纠错的教训与四条纪律**，全文见 `method_registry.yaml` MJ-24 (i)–(xiv)。

行级书目登记面：本批七条 `references` **无空列表**（书目 44×3／46×4／51×7），故 M6 不以空集平凡满足；缺口面落在**可机器判定性**（无 `row_id` → `kind_profile_RLP.table_rows` 不可逐表反查，覆盖宣称系人工清点）与**出处强度**（RLP-004 依书目 46「等」概括面）两处，登记 `G-RLP-1`（含六个裁决口①-⑥）＋勘察义务 `SO-12`。E3 豁免 `WV-RLP-E3-01`（硬性质面 **5 项 8 实例** ＋ Z4 条件硬 4 实例；软性质 Z5 1 实例与升级型 Z7 7 实例**明列排除**）已于 **2026-10-06** 经人类裁决批准、`status: active`（申请登记 2026-10-05，跨 1 日；裁决全文见台账 `approval.ruling`）；九项 Waiver 全部 active，累计覆盖 **77** 条 seed、scope 互不重叠。§4.2／§4.3／§4.4／§4.5 末段的批次清单（含 RLP）同样**不回改**；其余 8 kind（SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.7 SCH 批（单段落分号序入库，母本零改动）

母本既有已发布引用勘察结论（2026-10-06）：母本全文 `SCH` 仅**一处**——@398（0.17.3 kind 封闭枚举行「SCH｜调度/时间语义策略｜方面 5 · 5.2.4」）。**无 `SCH-数字` 形态的已发布引用**（同 CTR／STP／DFL／RLP 四批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**单段落分号序**（本库首例：骨架源既非表格亦非行内清单）：母本 5.2.4（heading @2481）的正文仅 **@2483** 一段，以分号分隔三项子命题，既无『注册表条目：』类引导词亦无行标识，且三项中仅第二子命题含加粗、该加粗只覆盖术语对『事件时间 vs 处理时间』而非整个子命题（不足以充当条目名），故三条 `source_pointers` 一律 `{source_type: clause_id, value: "5.2.4"}`（＋bib_id），**不含 `row_id` 维度**；`name` 取子命题引导词**原形**（`vs` 与半角斜杠一律不改写为顿号或中文『对比』）；id 序即 @2483 的分号列举序：

| entry_id | @2483 分号列举序 | name（取子命题引导词原形） |
|---|---|---|
| SCH-001 | 第 1 项 | 定时器/截止期/cron 的登记 |
| SCH-002 | 第 2 项 | 事件时间 vs 处理时间的显式选择 |
| SCH-003 | 第 3 项 | 调度冲突与资源竞争的归属声明 |

`profiles.yaml` 的 `kind_profile_SCH.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实，其中 `table_rows` 记「不适用」（非表格源、无逐表行数可给，覆盖宣称系人工清点）。非表格非清单源的 `provenance` 口径（不含 `row_id`、`name` 取子命题原形）、无 `row_id` → C-ENV 落 `elif env` 分支系**数据形态所致而非豁免**、5.5 @2569 `time_semantics` 在册而 @2572 触发条件行未列 → **不为 SCH-002 绑任何 Z 性质**（不扩权，AP1 定 P0 依 @2483＋4.2.4 @2200 双重明文）、`formal_anchor` 空列表**全库首例**（SCH-001／SCH-002）与 SCH-002→DFL-003 跨 kind 单向 `composable` 不回填镜像、同批镜像一对 SCH-001↔SCH-003（5.3 @2521）、5.2.6 @2505／@2506 两处清单均未明列 cron → **不下探 CFG 面**、Y1 取 `consumed_by`（计息 10→11）与不增 Y8 实例、书目 49 的 2026-10-06 在线复核事实与书目 51 本批不引（Scheduler-Agent-Supervisor 专页未归档）、`aggregation_semantics` 一律 `additive`（依 5.2.5 @2499 Σ 明文）、`constraints_imposed` 21 项（hard 18／conditional 3／soft 0，表源＝**5.4**『施加约束』@2543-2553）、15 条 `signal_level` 定级（P0 3／P1 10／P2 2）、M4 零未登记谓词与 snake_case 占位 **0 处**（累计候选仍 31 词、本批零新增）、5.6 @2659『求值调度』同名异指的排除，以及**本批七处自我纠错的教训与五条纪律**，全文见 `method_registry.yaml` MJ-25 (i)–(xiv)。

行级书目登记面：本批三条 `references` 为**两条空列表＋一行书目 49**（SCH-002 系全库**首个** bib_id 49 的 carrier；SCH-001／SCH-003 为空列表 → M6 平凡通过，非豁免）；书目 49 的登记面逐字只覆盖第二子命题，第一／第三子命题**无任何行级书目登记面** → 缺口登记 `G-SCH-1`（含七个裁决口①-⑦）＋勘察义务 `SO-13`（含书目 51 的 Scheduler-Agent-Supervisor 在线专页**先归档再提取**的前置义务，与 cron／CFG 分工对账口）。E3 豁免 `WV-SCH-E3-01`（硬性质面 **1 项 1 实例**：Y1 `consumed_by`；**无排除面**——SCH 侧 Z5／Z7 计息均为 0）已于 **2026-10-07** 经人类裁决批准、`status: active`（申请登记 2026-10-06，跨 1 日；裁决全文见台账 `approval.ruling`；0.10 第一条／1.1 纪律二：批准是人的裁决，Agent 与工具不自行批准——本次裁决由用户在会话中直接指令作出并**明列 Waiver 编号**；SCH 三条的 seed 资格不以该 Waiver 为前提——C-ST 只查硬检查，故批准延迟未阻断本批入库，该批已于提交 `d8b22c3` 入库在先）。十项 Waiver 全部 active，累计覆盖 **80** 条 seed（STY 24＋OWN 4＋CSL 5＋CRD 8＋DEC 8＋CTR 12＋STP 4＋DFL 5＋RLP 7＋SCH 3）、scope 互不重叠。§4.2–§4.6 末段的批次清单（含 SCH）同样**不回改**；其余 7 kind（CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.8 CFG 批（行内加粗清单序入库，母本零改动）

母本既有已发布引用勘察结论（2026-10-08）：母本全文 `CFG` 仅**两处**——@399（0.17.3 kind 封闭枚举行「CFG｜配置治理策略｜方面 5 · 5.2.6」）与 @3173（7.6 示例二形式化注释块的「消费字段」行散文「CFG 开关注册表默认值」，系 configuration 的缩写用法、非 entry_id 形态）。**无 `CFG-数字` 形态的已发布引用**（同 CTR／STP／DFL／RLP／SCH 五批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**行内加粗清单序**（与 5.2.3 @2477 的 RLP 批同型：骨架源非表格）：母本 5.2.6（heading @2501）的正文＝准决策通道引言 @2503（逐字「构成**准决策通道**——它们能在不走 ADR 的情况下改变运行时行为，是纪律的潜在旁路」→ 不单独成条，作四条共同的 `problem_space` 源）＋行内加粗清单四项 @2505-2508，既无表格行列结构亦无行标识，故四条 `source_pointers` 一律 `{source_type: clause_id, value: "5.2.6"}`（＋交叉表源 clause_id 与 bib_id），**不含 `row_id` 维度**（实测 40 处＝clause_id 39＋bib_id 1、零 row_id）；`name` 取加粗引导词**逐字去粗体**，CFG-002 的括注「（登记入注册表，不允许运行时即兴判断）」位于加粗标记**之外** → 不入 name，改登记于该条 `provenance.origin` 行内注；三处原形不改写（拉丁词 `schema`、半角斜杠「决策/参数」、条款号「与 0.10 权力条款的联动」，MJ-21 (iii) 与 RLP-004 同理）。**分块序裁决**（兑现 `profiles.yaml` @372 末句「裁决见 README §4.8」的强制指针）：非表源无行序可依 → 取清单列举序，MJ-13 (iv)「表行序」不直接适用；与 RLP-001…007（§4.6）、SCH-001…003（§4.7）三批同型，判读全文见 MJ-26 (i)：

| entry_id | @2505-2508 列举序 | name（取加粗引导词原形） |
|---|---|---|
| CFG-001 | 第 1 项 | 配置 schema 注册 |
| CFG-002 | 第 2 项 | 决策/参数判别谓词 |
| CFG-003 | 第 3 项 | 开关生命周期 |
| CFG-004 | 第 4 项 | 与 0.10 权力条款的联动 |

`profiles.yaml` 的 `kind_profile_CFG.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实，其中 `table_rows` 记「不适用」（引言＋行内加粗清单，非表格、无行标识，覆盖宣称系人工清点）。无 `row_id` → C-ENV 落 `elif env` @858-859 并以 envelope 非空判 ok 系**数据形态所致而非豁免**（四条 envelope 各 4 项、合计 16 项均非空）、**Z6 首建计息 0→2**（CFG-003 `implements`／CFG-004 `consumed_by`，两面不双计）而母本 Z6 共 4 行（@2588／@3585／@3616／@3640）→ 后三行分属分级、汇聚信号与 DPS 面用法，不构成额外计息面亦不回填 DPS 镜像、Z4 增第三个计息面 7→8（条件硬 → 计息增加不扩豁免面）、`formal_anchor` 合计 242→245 且 CFG-001 空列表系**全库第三例**（前两例 SCH-001／SCH-002；SCH-002 行内注自称「全库首例」系序数误标，不改写只登记）、@2507＋@3585 的 P2 与 @3616 的 P0 **量词域不同故并存不矛盾**（归一属母本条文改动 → G-CFG-1 route ④）、`compatibility` 仅 3 行（同批镜像一对 CFG-001↔CFG-003＋CFG-002→CFG-001 单向 `requires`＋CFG-004 空集）系方向不对称**第四例**、`aggregation_semantics` 一律 `itemwise` 且四条一律省略 `latency_budget_delta`（剖面 optional @377-380 → 无被求和项，取 `additive` 即凭空宣称可加性）、`constraints_imposed` 28 项（hard 24／conditional 4／soft 0，`target_aspect` 取 {1,3,4,6,8,9,10} 七面各 4 项）、20 条 `signal_level` 定级（P0 9／P1 7／P2 4）、`typical_reversibility` bounded 3＋costly 1（CFG-002）、书目 48 系全库**首个** bib_id carrier 而其 longevity／dynamism 四类轴与母本 @2506 二分法**不同轴** → `support_claim` 不宣称支撑二分法（书目 65 经 @2754 已降为补充读物、不充出处）、2026-10-08 在线复核与本地 epub 九项实测（文内出版日以 `find` 检索返回 −1 → 据实登记不改写著录）、M4 双口径（56 项 → 经 `outside_brackets` 得调用 22 处／distinct 5／未登记 0；不经则 24 处／distinct 6／未登记集含 C → 通道号必须外包方括号）与占位符三口径 **53／60／742** 不得互代、累计候选仍 **31** 词、本批零新增，以及**四处既有误标不改写只登记与本批初稿缺漏的落盘前补正**，全文见 `method_registry.yaml` MJ-26 (i)–(x)。

行级书目登记面：本批四条 `references` 为**三条空列表＋一行书目 48**（CFG-003 系该 bib_id 在全库的唯一 carrier；三条空列表 → M6 平凡通过，非豁免）；缺口面落在**可机器判定性**（无 `row_id` → `kind_profile_CFG.table_rows` 不可逐表反查）与**出处强度**（四条中仅一条有行级书目登记面，且其分类轴与母本不同轴）两处，登记 `G-CFG-1`（含七个裁决口①-⑦）＋勘察义务 `SO-14`（承接存量开关到期日面、存量规避面、cron 补列对账未闭合面、词汇面与级别／镜像面）＋词汇缺口 `VG-05`（expiry／cleanup_filed／ADR 三词不在册、在册 76，一律以方括号事实占位符承载、**绝不写调用式**）。E3 豁免 `WV-CFG-E3-01`（硬性质面 **2 项 3 实例**：Z6 硬 2〔CFG-003 `implements`／CFG-004 `consumed_by`〕＋Z4 条件硬 1〔CFG-002 `consumed_by`〕；软性质 Z5 与升级型 Z7 在 CFG 侧计息均为 **0** → 明列排除）已于 **2026-10-09** 经人类裁决批准、`status: active`（系防扩宽条款 (ii) 之下的**第十一次**单独申请；申请登记 2026-10-08，跨 1 日；裁决全文见台账 `approval.ruling`；0.10 第一条／1.1 纪律二：批准是人的裁决，Agent 与工具不自行批准——本次裁决由用户在会话中直接指令作出并**明列 Waiver 编号**；CFG 四条的 seed 资格不以该 Waiver 为前提——C-ST 只查硬检查，故批准延迟未阻断本批入库，该批已于提交 `132ff3c` 入库在先）。十一项 Waiver 全部 active，累计覆盖 **84** 条 seed（STY 24＋OWN 4＋CSL 5＋CRD 8＋DEC 8＋CTR 12＋STP 4＋DFL 5＋RLP 7＋SCH 3＋CFG 4）、scope 互不重叠。§4.7 末段「十项 Waiver 全部 active，累计覆盖 80 条 seed」与 §4.2–§4.6 末段的批次清单同样**不回改**（0.22 承诺一：已发布登记不改写、差异只登记）；其余 **6** kind（QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。**另据实登记一处指称差异**：人类裁决所在的同一条指令后半作『推进 s5e-7 RLP 批』，而 todo.md @111／@115 与 changlog 实测记载 RLP 批系 **s5e-4**、已于 2026-10-05／10-06 入库（RLP-001…007 共 7 条）并经提交 `e50498a` 批准（`WV-RLP-E3-01` 现 active）→ 本批**不据该表述重启、改动或重编号任何已发布批次**（0.22 承诺一），s5e-7 的 kind 指称另行请示用户确认后再启动（MJ-22 (vii) 实测优先于记忆）。

### 4.9 QAT 批（四属性行内顿号清单序入库，母本零改动）

**两项用户裁决（2026-10-09）先行留痕**：① 本批 kind 指称经用户裁决定为 **QAT**——原指令后半作『推进 s5e-7 RLP 批』，而批次映射实测为 s5e-1 CTR／2 STP／3 DFL／**4 RLP**／5 SCH／6 CFG，RLP 批已于 2026-10-05／10-06 入库 7 条（RLP-001…007）并经提交 `e50498a` 批准（`WV-RLP-E3-01` 现 active）→ §4.8 末段所登『s5e-7 的 kind 指称另行请示用户确认后再启动』据此闭合；本批**不重启、不改动、不重编号任何已发布批次**（0.22 承诺一），指称冲突四处留痕（`method_registry.yaml` @9412＝`WV-CFG-E3-01` 的 `approved_by` 行／本文件 @173／`todo.md` @125／changlog @1009）；② 条目粒度经用户裁决定为 **15 条战术**（依 6.2.5 @2827『属性 → 战术映射为注册表条目，禁止即兴发明战术』＋@2834『每个战术条目携带自身的质量影响卡片』），而非按 6.2.1 四属性行拆 4 条、亦非按质量影响卡片面另拆。批次台账日期为 **2026-10-10**（机器 `date` 实测），与裁决日 2026-10-09 系跨日两口径，不得互代。

母本既有已发布引用勘察结论（2026-10-10）：母本全文 `QAT` 仅**两处**——@400（0.17.3 kind 封闭枚举行「QAT | 质量战术 | 方面 6 · 6.2.5」）与 @592（0.18.4 规程变体要点行「质量战术（6） | S1 候选 = QAT 条目按目标属性过滤；S4 = 战术卡片 vs 剩余预算」）。**无 `QAT-数字` 形态的已发布引用**（同 CTR／STP／DFL／RLP／SCH／CFG 六批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**四属性行内顿号清单序**（本库首例：骨架源既非表格、非单段落分号子命题、非行内加粗清单，而是四行属性各带顿号列举项）：母本 6.2.5（heading @2825）的正文＝引言 @2827＋四行属性清单 @2829-2832＋卡片与 Q6 义务 @2834，既无表格行列结构亦无行标识，故十五条 `source_pointers` 一律 `{source_type: clause_id, value: "6.2.5"}`（＋交叉表源 6.4 方面 6 八行 @2862-2869 与 6.3 三空间行），**不含 `row_id` 维度**（实测 120 处＝15×8、全 clause_id、零 row_id）；`name` 取各项战术词**逐字去括注**（括注内容降入 `narrative` 与 `compatibility`／`formal_anchor`，故 QAT-007 作『恢复』而非『恢复（主动冗余/被动冗余/ spare）』）；三处母本原形不改写（@2830 半角斜杠后空格、@2830 与 @2832 的半角斜杠不改顿号、@2832『限流/熔断联动 5.2.3』无顿号）。**分块序裁决**（兑现 `profiles.yaml` @403 末句「裁决见 README §4.9」的强制指针）：非表源无行序可依 → 取『四属性行的属性先后序 × 行内顿号列举序』，MJ-13 (iv)「表行序」判据的源为表格 → 不直接适用而是同型推广（列举序即源序）；与 RLP-001…007（§4.6）、SCH-001…003（§4.7）、CFG-001…004（§4.8）三批同型，判读全文见 MJ-27 (i)：

| entry_id | @2829-2832 属性行 · 行内顿号列举序 | name（取战术词逐字、去括注） |
|---|---|---|
| QAT-001 | 性能 · 第 1 项 | 引入并发 |
| QAT-002 | 性能 · 第 2 项 | 维持多副本 |
| QAT-003 | 性能 · 第 3 项 | 增加资源 |
| QAT-004 | 性能 · 第 4 项 | 减少开销 |
| QAT-005 | 性能 · 第 5 项 | 限制排队 |
| QAT-006 | 可用性 · 第 1 项 | 故障检测 |
| QAT-007 | 可用性 · 第 2 项 | 恢复 |
| QAT-008 | 可用性 · 第 3 项 | 故障预防 |
| QAT-009 | 可修改性 · 第 1 项 | 语义内聚 |
| QAT-010 | 可修改性 · 第 2 项 | 限制依赖 |
| QAT-011 | 可修改性 · 第 3 项 | 参数化配置 |
| QAT-012 | 可修改性 · 第 4 项 | 抽象中介 |
| QAT-013 | 安全 · 第 1 项 | 抵抗攻击 |
| QAT-014 | 安全 · 第 2 项 | 检测攻击 |
| QAT-015 | 安全 · 第 3 项 | 从攻击恢复 |

`profiles.yaml` 的 `kind_profile_QAT.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实，其中 `table_rows` 记「不适用」（四属性行内顿号清单，非表格、无行标识，覆盖宣称系人工清点）；该 kind 剖面的 `required_extra`／`optional`／`not_applicable`／`entry_level_exemptions` 四表**全空**（@407-410，未因本批改动）→ 十五条 `cost_profile.latency_budget_delta` **一律填实**（与 CFG 批依 optional @377-380 一律省略相反）。无 `row_id` → C-ENV 落 `elif env` 分支并以 envelope 非空判 ok 系**数据形态所致而非豁免**（十五条 envelope 各 4 项、合计 60 项均非空；metric 用 **13** 种、全库 distinct **19** 未增新词）、**Q 系列首建计息**（Q6 `implements` 15／Q5 `triggers` 15／Q4 `triggers` 2＝@7476＋@7661／Y5 `consumed_by` 1＝@8540，`formal_anchor` 合计 245→**278**、role 名零新增）、**两处『三族』不同指不得互代**（G-ENV-1 @8678 自称 6.2.1「只含四族」→ 实测七族 @2781-2787，其所缺三族＝安全 @2785／合规 @2786／可观测性 @2787〔指标族在册口径〕；G-QAT-1 与块头 @7262-7265 的三族＝可伸缩性 @2784／合规 @2786／可观测性 @2787〔6.2.5 战术覆盖口径〕→ 两集合仅「合规／可观测性」重叠；差异只登记不改写）、`aggregation_semantics` 一律 **itemwise**（15/15；5.2.5 @2499 的 Σ 明文只覆盖「流程各步骤卡片 latency_budget_delta」，不覆盖同一目标下多战术叠加 → 不本地造法，MJ-19 同型、先例 `method_registry.yaml` @2854〔STY-018 同键行内注「并行分支聚合式母本未给，不本地造法」〕；全库 itemwise 75→**90**／additive 9 未变）、`constraints_imposed` **120** 项（hard 75／soft 30／conditional 15；`target_aspect` 取 {1,2,3,4,5,8,9,10} **八面各 15 项**，交叉表源 6.4 @2862-2869）、60 条 `signal_level` 定级（**P0 17／P1 28／P2 15**，分布非一律：十二条 P0 1／P1 2／P2 1，QAT-007／QAT-011／QAT-013 三条 P0 2／P1 1／P2 1，QAT-015 一条 P0 0／P1 3／P2 1，逐项依据见块头 @7285-7292 与行内注 @8624／@8628／@8632／@8636，定级依 9.2.1 @3583-3585 与 MJ-4）、`typical_reversibility` costly 9／bounded 3／free 2／**irreversible 1（QAT-013，全库首例）**、`compatibility` 仅 **4** 行且**全为单向**（QAT-002→CSL-001 与 QAT-004→CSL-004 两 `tension`、QAT-011→CFG-001 与 QAT-015→RLP-006 两 `requires`，evidence 一律 6.2.5；@2831『联动方面 3 契约』系方面级指引而无母本明文指定对侧 entry_id → 不造关系，先例 CFG-001 @6855-6862；全库 compatibility 132→**136**：requires 16→18／tension 14→16／composable 97／hard_conflict 5）、M4 双通道（QAT 侧扫描 **195** 处＝detection_predicate 60＋applicability 135 → 调用词 **70** 处／distinct **5**〔tactic 54／goal 13／tactic_card 1／verdict 1／cost_ledger 1〕／未登记 **0**；本批方括号内无「词＋左圆括号」形态 → 经与不经 `outside_brackets` @208 结果相同，与 CFG 批 `[CH-C(2)]` 被误读的情形不同；全库 scanned 623→**818**）、占位符三口径 **217／248／990** 不得互代（`bracket_spans` @189-206 在 QAT 块内命中 217 处／distinct 214；QAT 十五条经 `census_placeholders` @1084 得 248 处；全库 990 处／99 条）、累计候选仍 **31** 词、本批零新增（`predicate_vocabulary.yaml` 在册名 **76** 未变），以及 **waiver rule 行母本条款号既有误标**（前六条 @9177／9199／9221／9243／9265／9287 写作『E3（母本 @4008）』，而实测 @4008 系 E2、E3 在 @4009，后五条 @9309／9331／9353／9375／9397 已校正并带行内注 → 前六条属已发布登记，据 0.22 承诺一**只登记不改写**）与**块内自指行号更正纪律**（块内 @NNNN 合计 1320 处／指向块内 73 处／distinct 21；off-by-10 六处共 20 个出现已更正、旧形态 0 处），全文见 `method_registry.yaml` MJ-27 (i)–(xi)。

行级书目登记面：本批十五条 `references` **一律空列表**（全库**首例整批零书目登记面**；空列表条目 32→**47**，`references` 项总数 **83** 批前＝批后、本批零新增）→ M6 严格式平凡为真，**不得读作无外部文献支撑**，亦非豁免；6.7 文献 56 系尾注非独立著录行、书目 12 @1875 的 `compile_usage` 归 1.2.4 面 → 行级面不下探。缺口面落在**目标-手段闭合**（6.2.1 七族中可伸缩性／合规／可观测性三族在 6.2.5 无对应战术 → Q6 @2901 对该三族恒不成立）、**卡片参数化无母本据**（@2834 只给『战术也有代价』的两个示例，未给 `failure_modes` @2492／`observability_requires` @2494 的封闭词汇与量化门槛 → 本批一律不填数值以守 0.4 与 @2789 量化纪律）、**可机器判定性**（无 `row_id` → `table_rows` 不可逐表反查）与**词汇面**（6.5 Q4-Q6 公式侧六词未登记）四处，登记 `G-QAT-1`（含七个裁决口①-⑦）＋勘察义务 `SO-15`（入库期义务，consumer M6，逐口承接该七项）＋词汇缺口 `VG-06`（六词 consumed／mapped／recorded_in／approved_waiver／observability_requires／tactic_registry；另关系词 satisfied 亦缺，系关系词而非谓词 → **待登**，`predicate_vocabulary.yaml` 的 `vocabulary_gaps` 本批仍为 5〔VG-01…VG-05〕、在册名 76 未变，实际追加归 **s5g**；本批**绝不写调用式**，以免制造未登记谓词的既成事实）。状态迁移 `ST-QAT-01`（全 99 条 scope、date 2026-10-10、M2-M6 硬检查全过）。E3 豁免 `WV-QAT-E3-01`（硬性质面 **3 项 18 实例**：Q5 `triggers` **15**〔无条件硬，@2899-2900『行为预算不豁免（Z7 对偶）〕，十五条逐条各 1〕＋Q4 `triggers` **2**〔QAT-002／QAT-004，条件硬〕＋Y5 `consumed_by` **1**〔QAT-014〕；软性质 Q6 `implements` **15** 系**唯一登记的排除面**；`deadline.type` 为 **event**〔编译器首次成功运行，0.17.6(2) 指定的 LRM〕、无日历期限 → 不虚构日期〔0.4〕）现 **`status: pending`**——**登记即申请，批准是人的裁决，Agent 与工具不自行批准**（0.10 第一条 @235／母本 9.2.2 @3600）；与前十一项不同，本项申请与本批入库**同属一次提交**（不存在『先入库后批准』的跨提交时序），而 pending 不阻断本迁移（0.17.5 的 `draft→seed` 条件为 M2-M6 硬检查全过，E3 属 FVR 接线面而非条目字段面，二者不同轴；SCH／CFG 批同型判读）。十二项 Waiver 中**十一项 active、一项 pending**；已批准者累计覆盖 **84** 条 seed（STY 24＋OWN 4＋CSL 5＋CRD 8＋DEC 8＋CTR 12＋STP 4＋DFL 5＋RLP 7＋SCH 3＋CFG 4），`WV-QAT-E3-01` 若经人工批准则累计 **99** 条（＋QAT 15）、scope 互不重叠。§4.7 末段「十项 Waiver 全部 active，累计覆盖 80 条 seed」、§4.8 末段「十一项 Waiver 全部 active，累计覆盖 84 条 seed」与「其余 6 kind（QAT/VFM/GRD/DPS/PRJ/GOV）」、以及 §4.2–§4.6 末段的批次清单同样**不回改**（0.22 承诺一：已发布登记不改写、差异只登记）；其余 **5** kind（VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

## 5. 状态纪律与自检清单

生命周期见 0.17.5。`draft→seed` = bootstrap 期专用迁移，条件 **M2–M6 全过**（低影响：简记 ＋ provenance 登记，简记见 `method_registry.yaml: status_transitions`）。`project.py` 执行：

| 检查 | 内容 | 级别 |
|---|---|---|
| M2 | 按 kind 剖面必填字段在案（量词 `∀E(status ≠ draft)`） | 硬 |
| M3 | 每个 envelope 项 `bound_expr` 参数化 ∧ `source` 过 0.4 出处门槛（clause_id 反查母本可查） | 硬 |
| M4 | `detection_predicate` 词汇封闭（第 3 节约定 1）＝可执行 | 硬 |
| M5 | narrative_sync：决策性叙事已形式化或带 `clue:` 标记 | 软（P2） |
| M6 | 每条 reference 声明 `compile_usage` + `trust_grade`；存疑级不得为 envelope/detection 唯一出处 | 硬 |
| M9 | `compatibility.peer_entry` 全部存在于本注册表 | 硬 |
| C-ENV | 0.8「每种方法条目必须声明包络」：源行属 1.2.1/1.2.2/1.2.3 的条目 envelope 非空（子维度四元方法条目豁免，理由见剖面 note） | 硬（阻断 seed） |
| C-KP | 元注册条目（`kind_profile_*`）的完备性判据 = 物化后的 required_fields/optional_fields 两列表在案（不受 M2 按 kind 剖面判定，避免自指循环；已登记 `profiles.yaml: gaps/KP-G2`） | 硬 |
| C-ST | 声明状态与自检资格一致：`status=seed` 必须全过硬检查；未过者必须为 `draft`。附加：条目所属 kind 的剖面若为 `draft`（`profiles.yaml`，适用性无据 → KP-G3），该条目**不得**声明 `seed` | 硬 |
| C-ID | entry_id 唯一、格式 `{kind前缀}-{三位序号}`、kind ∈ 0.17.3 封闭枚举、无与母本既有引用冲突的重排。元条目例外：id 形态 `kind_profile_{KIND}`（0.17.8 谓词以 kind 为键） | 硬 |

**seed 资格 = M2 ∧ M3 ∧ M4 ∧ M6 ∧ M9 ∧ C-ENV ∧ C-ST**（M5 为软，记警告不阻断）。

## 6. 用法

```bash
cd registry
python3 scripts/project.py --check      # 仅自检，输出报告并写 projections/自检报告.md
python3 scripts/project.py --project    # 自检 + 生成人类层投影（projections/）
```

投影产物：`projections/STY.md`（条目人类可读视图，含四层数据源标注）、`projections/自检报告.md`、`projections/勘察义务清单.md`（M15 占位符汇总）、`projections/索引.md`。

## 7. 变更纪律

- 条目**机器层字段**任何变更 = 完整 ADR + 批准（0.17.4 消费者四 / 0.13 注册表类目）；
- `narrative` 变更 = 低影响（简记级），受 M5 抽查；
- `status` 迁移权限见 0.17.5；
- kind 剖面变更走 0.13；新增 kind = 高影响（枚举封闭，0.17.3）；
- 表格与条目冲突时**以条目为准**，冲突登记为成文法缺陷（FM-12 通道，0.17.1）。
