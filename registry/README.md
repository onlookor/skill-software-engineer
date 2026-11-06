# 方法注册表（registry/）

本目录是**方法注册表的机器层权威源**（母本 0.17）与其同源投影。母本各方面 x.2 的方法空间表格是**种子数据源视图**，不是决策权威（0.17.1）；权威在本目录的条目。选型只消费条目（0.18 S1），守护只消费条目的 `anti_patterns`/`compatibility`（0.17.4 消费者二），编译以条目为编译单元（编译规范 2.4）。

目录布局的新增属 0.13 制度性决定（简记级），已登记于母本 changelog、母本"配套文件说明"表、AGENTS.MD 与本仓 README。

## 1. 文件清单

| 文件 | 职责 | 权威关系 |
|---|---|---|
| `profiles.yaml` | 17 个 kind 的字段剖面（元注册条目，0.17.2「字段完备性按 kind 剖面」、0.17.8 `kind_profile(kind, required_fields, optional_fields)`）＋剖面级缺口台账（KP-G1…G4，R2 澄清候选） | 数据侧权威；剖面变更走 0.13 |
| `predicate_vocabulary.yaml` | 母本机器层谓词清单的**数据侧投影**（供 M4 词汇封闭校验） | **非权威**：权威在母本 x.5／0.17.8／0.18.6／0.20.4／0.21.6／10.5；本文件每条带 clause 指针，`project.py` 反向核验指针在母本中可查 |
| `method_registry.yaml` | 方法条目本体（当前批次：STY 24 条＋OWN 4 条＋CSL 5 条＋CRD 8 条＋DEC 8 条＋CTR 12 条＋STP 4 条＋DFL 5 条＋RLP 7 条＋SCH 3 条＋CFG 4 条＋QAT 15 条＋VFM 6 条＋DPS 5 条＋GRD 3 条＋PRJ 11 条＋GOV 6 条，共 130 条）＋缺口台账＋状态迁移简记＋Waiver＋人工判断登记 | 数据侧权威（条目 schema 逐字采用 0.17.2） |
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
3. **谓词／参数槽与事实占位（新口径，2026-11-04）**：方括号 `[…]` 表示**谓词／参数槽**——`applicability` 三空间与 `detection_predicate` 是谓词，`cost_profile`／`envelope.bound_expr` 是参数；它们在决策期求值，**不计事实债**。**待勘察事实必须带显式标记**：以 `待勘察：` 开头（如 `[待勘察：本部署是否…]`），或整句以 `待勘察` 结尾（值位未定，如 `[到期时刻具体值待勘察]`）；仅句中提及（如叙事里的「待勘察事实」）不计。`[已核验]`／`[存疑]`／`[未核验]`／`[待核验]` 按 0.12 是可信度标注，单列统计、不计入任一类。事实占位求值 `unknown` 时按 **M15**：候选保留 ＋ 勘察义务登记，**禁沉默排除**（0.18.6）。`project.py` 输出「总数＝事实＋槽」三行与按字段／按 kind 两张分解表；`勘察义务清单.md` 只逐条枚举事实占位。旧口径（全部方括号计为事实占位，1480 处）见 §4.16 与 changlog，**不回改**。
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
| `CTR-gRPC` | 3.6 示例一（@2033 事实集内 `contract(gRPC, …)`；@2037 `CTR-gRPC.envelope.latency_bound`） | 3.2.1「同步 API 契约」行 = **CTR-002**（叙述式书写 ≠ 三位 id，等同判断承 MJ-14） |
| `CTR.compatibility.policy`（additive-only/backward/full） | 3.6 示例二消费字段（@2051-2052） | 策略值落 **CTR-008**（3.2.2「兼容性规则」行）；其**取值枚举与登记面**属 **CTR-007**（「版本化策略」行），二者不合并 |
| `CTR.lifecycle_state`（published/deprecated） | 3.6 示例三消费字段（@2066-2067） | **CTR-010**（3.2.2「契约生命周期」行） |

编号方案＝**两表分块序**（承 §4.1 的分块序形态）：

| 块 | 母本源 | entry_id 区间 |
|---|---|---|
| 契约形态（六形态） | 3.2.1（六行 @1920-1925） | CTR-001 … CTR-006（进程内接口／同步 API 契约／异步消息契约／事件契约／数据契约／UI-端契约） |
| 契约治理（六维度） | 3.2.2（六行 @1933-1938） | CTR-007 … CTR-012（版本化策略／兼容性规则／消费者驱动契约测试（CDC）／契约生命周期／破坏性变更流程／发现与注册） |

采分块序而非单一混合行序的理由：两表在母本为并列的两张表（形态面／治理面），3.2.2 内容列明记「每契约登记其一」即治理维度对全部形态正交适用，混编会使「形态 → 治理」的施加关系在 id 面上不可读；块内行序即 id 序，块序按母本小节序。`name` 一律取表首列逐字（含母本自带括注）。0.18.4「契约形态（3）」行（@591）的三点规程变体要点（S2 消费风格硬约束（1.4 接收）／S4 检验 X 系列／CDC 要求按 X4 分级入 cost_profile）已由 `profiles.yaml` 的 `kind_profile_CTR.selection_profile.variant` 承载，不参与编号裁决。

§4.2 末段的批次清单（含 CTR）系该时点的预告面，本批入库后**不回改该句**（0.22 承诺一同型：已发布文本以新增登记留痕，不以改写消解差异）；其余 11 kind（STP/DFL/RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用「先解母本既有已发布引用（如有）」的同一模式。

### 4.4 STP 批（单表表序入库，母本零改动）

母本既有已发布引用勘察结论（2026-09-27）：母本全文 `STP` 仅**两处**——@394（0.17.3 kind 封闭枚举行「STP｜存储拓扑｜方面 4 · 4.2.2」）与 @2348（4.6 示例三【形式化注释】的消费字段行「STP/R 阈值注册表（P99）」）。**无 `STP-数字` 形态的已发布引用**（与 STY/CSL/CRD/DEC 四批不同，同 CTR 批），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。@2348 的 `STP/R` 系**消费字段称呼、非 entry_id**（判读承 §4.3 CTR 批对 3.6 三处称呼的同型处置，MJ-21 (i) 同型）。

编号方案＝**单表表序**（承 §4.2 的 MJ-13 (iv) 同型：4.2.2 为一张表，行序即 id 序）：

| entry_id | 母本源行（4.2.2，@2177-2180） | name（取表首列逐字） |
|---|---|---|
| STP-001 | 第 1 行 | 每服务自有数据库 |
| STP-002 | 第 2 行 | 共享数据库 |
| STP-003 | 第 3 行 | 事件日志为权威状态 |
| STP-004 | 第 4 行 | 多语言持久化 |

`profiles.yaml` 的 `kind_profile_STP.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实。三列源表（拓扑｜定义｜与风格的关系）到条目字段的归类判读、`latency_budget_delta` 一律填实的依据、`compatibility` 七行的方向与级别、`constraints_imposed` 28 项的级别分布（与 CTR 批施→8 取 conditional 的差异据实记载）、`references` 的行级/性质级定性、谓词面精确事实（4.2.2 侧七词不入 M4 扫描面 ＋ 母本 4.5 公式七词缺口）与 **Read 工具行号偏一的据实记载**，全文见 `method_registry.yaml` MJ-22 (i)–(vii)。

行级书目登记面：母本 4.7（@2429-2439）九项中**行级**可引者仅书目 37（→ STP-003）与 38（→ STP-004），故 STP-001／STP-002 的 `references` 为**空列表**（M6 平凡通过，非豁免）；缺口登记 `G-STP-1` ＋ 勘察义务 `SO-10`。E3 豁免 `WV-STP-E3-01`（5 项 11 实例）已于 **2026-09-28** 经人类裁决批准、`status: active`（申请登记 2026-09-27，跨 1 日；裁决全文见台账 `approval.ruling`）；七项 Waiver 全部 active，累计覆盖 **65** 条 seed、scope 互不重叠。§4.2／§4.3 末段的批次清单（含 STP）同样**不回改**；其余 10 kind（DFL/RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.5 DFL 批（单表表序入库，母本零改动）

母本既有已发布引用勘察结论（2026-09-28）：母本全文 `DFL` 仅**一处**——@396（0.17.3 kind 封闭枚举行「DFL｜数据流动机制｜方面 4 · 4.2.4」）。**无 `DFL-数字` 形态的已发布引用**（同 CTR／STP 两批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**单表表序**（承 §4.2 的 MJ-13 (iv) 同型：4.2.4 为一张表，行序即 id 序）：

| entry_id | 母本源行（4.2.4，@2200-2204） | name（取表首列逐字） |
|---|---|---|
| DFL-001 | 第 1 行 | 事务性发件箱（outbox） |
| DFL-002 | 第 2 行 | 变更数据捕获（CDC） |
| DFL-003 | 第 3 行 | 流处理 |
| DFL-004 | 第 4 行 | ETL/ELT 批（母本首列原形即含斜杠 → 按 MJ-21 (iii) 原形登记，不改写为术语表 @4286 的「ETL / ELT」形态） |
| DFL-005 | 第 5 行 | 物化视图 |

`profiles.yaml` 的 `kind_profile_DFL.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实。四列源表（机制｜定义｜适用条件｜质量影响要点）到条目字段的归类判读、CDC 一词在母本的双义隔离（数据域 @4280 归 DFL-002／契约域 @4281 归 CTR-009）、`latency_budget_delta` 五条一律填实但理由不平移 STP 批措辞、22 条 `signal_level` 的定级依据（P0 11／P1 5／P2 6）、谓词面精确事实（本批 11 个调用词全部已登记 → 零新增候选，累计仍 19 词）、`formal_anchor` 12 实例的角色分配、`compatibility` 十行（composable 8／tension 2）与 RLP 批重叠处置、6.6 示例四 800ms 不入 `bound_expr` 的边界、书目 44 的 ISBN 观察项、同批镜像与 `pending_conflict_rows` 口径，全文见 `method_registry.yaml` MJ-23 (i)–(xi)。

行级书目登记面：母本 4.7（@2429-2439）九项中**行级**可引者仅书目 42（→ DFL-001 发件箱）与 43（→ DFL-002 CDC），覆盖 5 行中 2 行，故 DFL-003／DFL-004／DFL-005 的 `references` 为**空列表**（M6 平凡通过，非豁免）；缺口登记 `G-DFL-1`（含五个下探裁决口①-⑤，其一为书目 44 本地 EPUB 的 isbn13 与母本 @2752 著录形态不一致的处置）＋勘察义务 `SO-11`。E3 豁免 `WV-DFL-E3-01`（硬性质面 **3 项 6 实例**：Z2 3／Y2 2／Y1 1；软性质 Y4 5 实例＋Y7 1 实例**明列排除**）已于 **2026-10-04** 经人类裁决批准、`status: active`（申请登记 2026-09-28，跨 6 日；裁决全文见台账 `approval.ruling`）；八项 Waiver 全部 active，累计覆盖 **70** 条 seed、scope 互不重叠。§4.2／§4.3／§4.4 末段的批次清单（含 DFL）同样**不回改**；其余 9 kind（RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.6 RLP 批（行内清单序入库，母本零改动）

母本既有已发布引用勘察结论（2026-10-05）：母本全文 `RLP` 仅**一处**——@398（0.17.3 kind 封闭枚举行「RLP｜可靠性模式｜方面 5 · 5.2.3」）。**无 `RLP-数字` 形态的已发布引用**（同 CTR／STP／DFL 三批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**行内清单序**（本库首例：骨架源非表格）：母本 5.2.3（heading @2477）的注册表条目清单在 **@2479** 以『注册表条目（每条带质量影响卡片）：』引导、分号分隔七项，无 4.2.2／4.2.4／3.2.1 类的表格行列结构，故七条 `source_pointers` 一律 `{source_type: clause_id, value: "5.2.3"}`（＋bib_id），**不含 `row_id` 维度**；id 序即 @2479 的列举序：

| entry_id | @2479 列举序 | name（取各项引导词逐字） |
|---|---|---|
| RLP-001 | 第 1 项 | 幂等 |
| RLP-002 | 第 2 项 | 收件箱（inbox） |
| RLP-003 | 第 3 项 | 发件箱（outbox） |
| RLP-004 | 第 4 项 | 重试 + 指数退避 + 抖动 |
| RLP-005 | 第 5 项 | 超时预算 |
| RLP-006 | 第 6 项 | 断路器 |
| RLP-007 | 第 7 项 | 舱壁 |

`profiles.yaml` 的 `kind_profile_RLP.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实。非表格源的 `provenance` 口径（不含 `row_id`、`name` 取引导词逐字）、书目 46 以「等」概括覆盖「重试」而书目 51 目录面只作工程参照、@2721 六项／@2732 五项与 @2479 七项的枚举差异处置（以 @2479 为准、不本地合并；@2734 的 800ms 系现状测量值不入 `bound_expr`）、DFL-001↔RLP-003 发件箱重叠的**定义面归 DFL／行为面归 RLP** 兑现（单向 `requires` ＋ RLP-003 envelope 只 3 族）、`formal_anchor` 20 实例与 Waiver scope 的对位、M4 四词六行改写落点（@5617／@5984／@6029／@6090／@6086／@6204，不本地扩表）、M9 同批镜像补登两处（`compatibility` 30→32，不对称累计第三例）、`aggregation_semantics` 首次出现 `additive`（RLP-004／005，母本明文求和语义）、方面 8 `conditional` 首次成批使用（表源＝**5.4**『施加约束』@2545-2555，与前八批所引 **4.4** 表 @2253-2259 系两张同名不同源的表，不得混引）、32 条 `signal_level` 定级（P0 11／P1 13／P2 8）、书目 46 的 ISBN 分组与页数两说据实登记不改写，以及**本批四处自我纠错的教训与四条纪律**，全文见 `method_registry.yaml` MJ-24 (i)–(xiv)。

行级书目登记面：本批七条 `references` **无空列表**（书目 44×3／46×4／51×7），故 M6 不以空集平凡满足；缺口面落在**可机器判定性**（无 `row_id` → `kind_profile_RLP.table_rows` 不可逐表反查，覆盖宣称系人工清点）与**出处强度**（RLP-004 依书目 46「等」概括面）两处，登记 `G-RLP-1`（含六个裁决口①-⑥）＋勘察义务 `SO-12`。E3 豁免 `WV-RLP-E3-01`（硬性质面 **5 项 8 实例** ＋ Z4 条件硬 4 实例；软性质 Z5 1 实例与升级型 Z7 7 实例**明列排除**）已于 **2026-10-06** 经人类裁决批准、`status: active`（申请登记 2026-10-05，跨 1 日；裁决全文见台账 `approval.ruling`）；九项 Waiver 全部 active，累计覆盖 **77** 条 seed、scope 互不重叠。§4.2／§4.3／§4.4／§4.5 末段的批次清单（含 RLP）同样**不回改**；其余 8 kind（SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.7 SCH 批（单段落分号序入库，母本零改动）

母本既有已发布引用勘察结论（2026-10-06）：母本全文 `SCH` 仅**一处**——@399（0.17.3 kind 封闭枚举行「SCH｜调度/时间语义策略｜方面 5 · 5.2.4」）。**无 `SCH-数字` 形态的已发布引用**（同 CTR／STP／DFL／RLP 四批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**单段落分号序**（本库首例：骨架源既非表格亦非行内清单）：母本 5.2.4（heading @2483）的正文仅 **@2485** 一段，以分号分隔三项子命题，既无『注册表条目：』类引导词亦无行标识，且三项中仅第二子命题含加粗、该加粗只覆盖术语对『事件时间 vs 处理时间』而非整个子命题（不足以充当条目名），故三条 `source_pointers` 一律 `{source_type: clause_id, value: "5.2.4"}`（＋bib_id），**不含 `row_id` 维度**；`name` 取子命题引导词**原形**（`vs` 与半角斜杠一律不改写为顿号或中文『对比』）；id 序即 @2485 的分号列举序：

| entry_id | @2485 分号列举序 | name（取子命题引导词原形） |
|---|---|---|
| SCH-001 | 第 1 项 | 定时器/截止期/cron 的登记 |
| SCH-002 | 第 2 项 | 事件时间 vs 处理时间的显式选择 |
| SCH-003 | 第 3 项 | 调度冲突与资源竞争的归属声明 |

`profiles.yaml` 的 `kind_profile_SCH.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实，其中 `table_rows` 记「不适用」（非表格源、无逐表行数可给，覆盖宣称系人工清点）。非表格非清单源的 `provenance` 口径（不含 `row_id`、`name` 取子命题原形）、无 `row_id` → C-ENV 落 `elif env` 分支系**数据形态所致而非豁免**、5.5 @2571 `time_semantics` 在册而 @2574 触发条件行未列 → **不为 SCH-002 绑任何 Z 性质**（不扩权，AP1 定 P0 依 @2485＋4.2.4 @2202 双重明文）、`formal_anchor` 空列表**全库首例**（SCH-001／SCH-002）与 SCH-002→DFL-003 跨 kind 单向 `composable` 不回填镜像、同批镜像一对 SCH-001↔SCH-003（5.3 @2523）、5.2.6 @2507／@2508 两处清单均未明列 cron → **不下探 CFG 面**、Y1 取 `consumed_by`（计息 10→11）与不增 Y8 实例、书目 49 的 2026-10-06 在线复核事实与书目 51 本批不引（Scheduler-Agent-Supervisor 专页未归档）、`aggregation_semantics` 一律 `additive`（依 5.2.5 @2501 Σ 明文）、`constraints_imposed` 21 项（hard 18／conditional 3／soft 0，表源＝**5.4**『施加约束』@2545-2555）、15 条 `signal_level` 定级（P0 3／P1 10／P2 2）、M4 零未登记谓词与 snake_case 占位 **0 处**（累计候选仍 31 词、本批零新增）、5.6 @2661『求值调度』同名异指的排除，以及**本批七处自我纠错的教训与五条纪律**，全文见 `method_registry.yaml` MJ-25 (i)–(xiv)。

行级书目登记面：本批三条 `references` 为**两条空列表＋一行书目 49**（SCH-002 系全库**首个** bib_id 49 的 carrier；SCH-001／SCH-003 为空列表 → M6 平凡通过，非豁免）；书目 49 的登记面逐字只覆盖第二子命题，第一／第三子命题**无任何行级书目登记面** → 缺口登记 `G-SCH-1`（含七个裁决口①-⑦）＋勘察义务 `SO-13`（含书目 51 的 Scheduler-Agent-Supervisor 在线专页**先归档再提取**的前置义务，与 cron／CFG 分工对账口）。E3 豁免 `WV-SCH-E3-01`（硬性质面 **1 项 1 实例**：Y1 `consumed_by`；**无排除面**——SCH 侧 Z5／Z7 计息均为 0）已于 **2026-10-07** 经人类裁决批准、`status: active`（申请登记 2026-10-06，跨 1 日；裁决全文见台账 `approval.ruling`；0.10 第一条／1.1 纪律二：批准是人的裁决，Agent 与工具不自行批准——本次裁决由用户在会话中直接指令作出并**明列 Waiver 编号**；SCH 三条的 seed 资格不以该 Waiver 为前提——C-ST 只查硬检查，故批准延迟未阻断本批入库，该批已于提交 `d8b22c3` 入库在先）。十项 Waiver 全部 active，累计覆盖 **80** 条 seed（STY 24＋OWN 4＋CSL 5＋CRD 8＋DEC 8＋CTR 12＋STP 4＋DFL 5＋RLP 7＋SCH 3）、scope 互不重叠。§4.2–§4.6 末段的批次清单（含 SCH）同样**不回改**；其余 7 kind（CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.8 CFG 批（行内加粗清单序入库，母本零改动）

母本既有已发布引用勘察结论（2026-10-08）：母本全文 `CFG` 仅**两处**——@400（0.17.3 kind 封闭枚举行「CFG｜配置治理策略｜方面 5 · 5.2.6」）与 @3175（7.6 示例二形式化注释块的「消费字段」行散文「CFG 开关注册表默认值」，系 configuration 的缩写用法、非 entry_id 形态）。**无 `CFG-数字` 形态的已发布引用**（同 CTR／STP／DFL／RLP／SCH 五批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**行内加粗清单序**（与 5.2.3 @2479 的 RLP 批同型：骨架源非表格）：母本 5.2.6（heading @2503）的正文＝准决策通道引言 @2505（逐字「构成**准决策通道**——它们能在不走 ADR 的情况下改变运行时行为，是纪律的潜在旁路」→ 不单独成条，作四条共同的 `problem_space` 源）＋行内加粗清单四项 @2507-2510，既无表格行列结构亦无行标识，故四条 `source_pointers` 一律 `{source_type: clause_id, value: "5.2.6"}`（＋交叉表源 clause_id 与 bib_id），**不含 `row_id` 维度**（实测 40 处＝clause_id 39＋bib_id 1、零 row_id）；`name` 取加粗引导词**逐字去粗体**，CFG-002 的括注「（登记入注册表，不允许运行时即兴判断）」位于加粗标记**之外** → 不入 name，改登记于该条 `provenance.origin` 行内注；三处原形不改写（拉丁词 `schema`、半角斜杠「决策/参数」、条款号「与 0.10 权力条款的联动」，MJ-21 (iii) 与 RLP-004 同理）。**分块序裁决**（兑现 `profiles.yaml` @p:CFG#seed_source.entry_id_range 末句「裁决见 README §4.8」的强制指针）：非表源无行序可依 → 取清单列举序，MJ-13 (iv)「表行序」不直接适用；与 RLP-001…007（§4.6）、SCH-001…003（§4.7）三批同型，判读全文见 MJ-26 (i)：

| entry_id | @2507-2510 列举序 | name（取加粗引导词原形） |
|---|---|---|
| CFG-001 | 第 1 项 | 配置 schema 注册 |
| CFG-002 | 第 2 项 | 决策/参数判别谓词 |
| CFG-003 | 第 3 项 | 开关生命周期 |
| CFG-004 | 第 4 项 | 与 0.10 权力条款的联动 |

`profiles.yaml` 的 `kind_profile_CFG.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实，其中 `table_rows` 记「不适用」（引言＋行内加粗清单，非表格、无行标识，覆盖宣称系人工清点）。无 `row_id` → C-ENV 落 `elif env` @d:registry/scripts/project.py#fn-check_cenv 并以 envelope 非空判 ok 系**数据形态所致而非豁免**（四条 envelope 各 4 项、合计 16 项均非空）、**Z6 首建计息 0→2**（CFG-003 `implements`／CFG-004 `consumed_by`，两面不双计）而母本 Z6 共 4 行（@2590／@3587／@3618／@3643）→ 后三行分属分级、汇聚信号与 DPS 面用法，不构成额外计息面亦不回填 DPS 镜像、Z4 增第三个计息面 7→8（条件硬 → 计息增加不扩豁免面）、`formal_anchor` 合计 242→245 且 CFG-001 空列表系**全库第三例**（前两例 SCH-001／SCH-002；SCH-002 行内注自称「全库首例」系序数误标，不改写只登记）、@2509＋@3587 的 P2 与 @3618 的 P0 **量词域不同故并存不矛盾**（归一属母本条文改动 → G-CFG-1 route ④）、`compatibility` 仅 3 行（同批镜像一对 CFG-001↔CFG-003＋CFG-002→CFG-001 单向 `requires`＋CFG-004 空集）系方向不对称**第四例**、`aggregation_semantics` 一律 `itemwise` 且四条一律省略 `latency_budget_delta`（剖面 optional（profiles.yaml 的 CFG 剖面）→ 无被求和项，取 `additive` 即凭空宣称可加性）、`constraints_imposed` 28 项（hard 24／conditional 4／soft 0，`target_aspect` 取 {1,3,4,6,8,9,10} 七面各 4 项）、20 条 `signal_level` 定级（P0 9／P1 7／P2 4）、`typical_reversibility` bounded 3＋costly 1（CFG-002）、书目 48 系全库**首个** bib_id carrier 而其 longevity／dynamism 四类轴与母本 @2508 二分法**不同轴** → `support_claim` 不宣称支撑二分法（书目 65 经 @2756 已降为补充读物、不充出处）、2026-10-08 在线复核与本地 epub 九项实测（文内出版日以 `find` 检索返回 −1 → 据实登记不改写著录）、M4 双口径（56 项 → 经 `outside_brackets` 得调用 22 处／distinct 5／未登记 0；不经则 24 处／distinct 6／未登记集含 C → 通道号必须外包方括号）与占位符三口径 **53／60／742** 不得互代、累计候选仍 **31** 词、本批零新增，以及**四处既有误标不改写只登记与本批初稿缺漏的落盘前补正**，全文见 `method_registry.yaml` MJ-26 (i)–(x)。

行级书目登记面：本批四条 `references` 为**三条空列表＋一行书目 48**（CFG-003 系该 bib_id 在全库的唯一 carrier；三条空列表 → M6 平凡通过，非豁免）；缺口面落在**可机器判定性**（无 `row_id` → `kind_profile_CFG.table_rows` 不可逐表反查）与**出处强度**（四条中仅一条有行级书目登记面，且其分类轴与母本不同轴）两处，登记 `G-CFG-1`（含七个裁决口①-⑦）＋勘察义务 `SO-14`（承接存量开关到期日面、存量规避面、cron 补列对账未闭合面、词汇面与级别／镜像面）＋词汇缺口 `VG-05`（expiry／cleanup_filed／ADR 三词不在册、在册 76，一律以方括号事实占位符承载、**绝不写调用式**）。E3 豁免 `WV-CFG-E3-01`（硬性质面 **2 项 3 实例**：Z6 硬 2〔CFG-003 `implements`／CFG-004 `consumed_by`〕＋Z4 条件硬 1〔CFG-002 `consumed_by`〕；软性质 Z5 与升级型 Z7 在 CFG 侧计息均为 **0** → 明列排除）已于 **2026-10-09** 经人类裁决批准、`status: active`（系防扩宽条款 (ii) 之下的**第十一次**单独申请；申请登记 2026-10-08，跨 1 日；裁决全文见台账 `approval.ruling`；0.10 第一条／1.1 纪律二：批准是人的裁决，Agent 与工具不自行批准——本次裁决由用户在会话中直接指令作出并**明列 Waiver 编号**；CFG 四条的 seed 资格不以该 Waiver 为前提——C-ST 只查硬检查，故批准延迟未阻断本批入库，该批已于提交 `132ff3c` 入库在先）。十一项 Waiver 全部 active，累计覆盖 **84** 条 seed（STY 24＋OWN 4＋CSL 5＋CRD 8＋DEC 8＋CTR 12＋STP 4＋DFL 5＋RLP 7＋SCH 3＋CFG 4）、scope 互不重叠。§4.7 末段「十项 Waiver 全部 active，累计覆盖 80 条 seed」与 §4.2–§4.6 末段的批次清单同样**不回改**（0.22 承诺一：已发布登记不改写、差异只登记）；其余 **6** kind（QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。**另据实登记一处指称差异**：人类裁决所在的同一条指令后半作『推进 s5e-7 RLP 批』，而 @d:todo.md#sec-3.8 方法注册表种子数据整理（独立工作项，原 3.4(3) 升格）／@115 与 changlog 实测记载 RLP 批系 **s5e-4**、已于 2026-10-05／10-06 入库（RLP-001…007 共 7 条）并经提交 `e50498a` 批准（`WV-RLP-E3-01` 现 active）→ 本批**不据该表述重启、改动或重编号任何已发布批次**（0.22 承诺一），s5e-7 的 kind 指称另行请示用户确认后再启动（MJ-22 (vii) 实测优先于记忆）。

### 4.9 QAT 批（四属性行内顿号清单序入库，母本零改动）

**两项用户裁决（2026-10-09）先行留痕**：① 本批 kind 指称经用户裁决定为 **QAT**——原指令后半作『推进 s5e-7 RLP 批』，而批次映射实测为 s5e-1 CTR／2 STP／3 DFL／**4 RLP**／5 SCH／6 CFG，RLP 批已于 2026-10-05／10-06 入库 7 条（RLP-001…007）并经提交 `e50498a` 批准（`WV-RLP-E3-01` 现 active）→ §4.8 末段所登『s5e-7 的 kind 指称另行请示用户确认后再启动』据此闭合；本批**不重启、不改动、不重编号任何已发布批次**（0.22 承诺一），指称冲突四处留痕（`method_registry.yaml` @9412＝`WV-CFG-E3-01` 的 `approved_by` 行／本文件 @d:registry/README.md#sec-4.8 CFG 批（行内加粗清单序入库，母本零改动）／`todo.md` @125／@d:软件工程元框架成文法-changlog.md#sec-2026-10-09：批准 Waiver `WV-CFG-E3-01`（评审点五人类裁决，申请登记 2026-10-08／裁决 2026-10-09，**跨 1 日**）——CFG 批 E3 seed 期限期豁免生效（`status: active`），十一项 Waiver 全部 `active`、防扩宽条款 (ii) 的单独申请纪律经**十一次**履行，注册表 **84** 条 seed 的数据面与豁免面全部对齐，零新增规范命题）；② 条目粒度经用户裁决定为 **15 条战术**（依 6.2.5 @2829『属性 → 战术映射为注册表条目，禁止即兴发明战术』＋@2836『每个战术条目携带自身的质量影响卡片』），而非按 6.2.1 四属性行拆 4 条、亦非按质量影响卡片面另拆。批次台账日期为 **2026-10-10**（机器 `date` 实测），与裁决日 2026-10-09 系跨日两口径，不得互代。

母本既有已发布引用勘察结论（2026-10-10）：母本全文 `QAT` 仅**两处**——@401（0.17.3 kind 封闭枚举行「QAT | 质量战术 | 方面 6 · 6.2.5」）与 @594（0.18.4 规程变体要点行「质量战术（6） | S1 候选 = QAT 条目按目标属性过滤；S4 = 战术卡片 vs 剩余预算」）。**无 `QAT-数字` 形态的已发布引用**（同 CTR／STP／DFL／RLP／SCH／CFG 六批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**四属性行内顿号清单序**（本库首例：骨架源既非表格、非单段落分号子命题、非行内加粗清单，而是四行属性各带顿号列举项）：母本 6.2.5（heading @2827）的正文＝引言 @2829＋四行属性清单 @2831-2834＋卡片与 Q6 义务 @2836，既无表格行列结构亦无行标识，故十五条 `source_pointers` 一律 `{source_type: clause_id, value: "6.2.5"}`（＋交叉表源 6.4 方面 6 八行 @2864-2871 与 6.3 三空间行），**不含 `row_id` 维度**（实测 120 处＝15×8、全 clause_id、零 row_id）；`name` 取各项战术词**逐字去括注**（括注内容降入 `narrative` 与 `compatibility`／`formal_anchor`，故 QAT-007 作『恢复』而非『恢复（主动冗余/被动冗余/ spare）』）；三处母本原形不改写（@2832 半角斜杠后空格、@2832 与 @2834 的半角斜杠不改顿号、@2834『限流/熔断联动 5.2.3』无顿号）。**分块序裁决**（兑现 `profiles.yaml` @p:QAT#seed_source.entry_id_range 末句「裁决见 README §4.9」的强制指针）：非表源无行序可依 → 取『四属性行的属性先后序 × 行内顿号列举序』，MJ-13 (iv)「表行序」判据的源为表格 → 不直接适用而是同型推广（列举序即源序）；与 RLP-001…007（§4.6）、SCH-001…003（§4.7）、CFG-001…004（§4.8）三批同型，判读全文见 MJ-27 (i)：

| entry_id | @2831-2834 属性行 · 行内顿号列举序 | name（取战术词逐字、去括注） |
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

`profiles.yaml` 的 `kind_profile_QAT.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实，其中 `table_rows` 记「不适用」（四属性行内顿号清单，非表格、无行标识，覆盖宣称系人工清点）；该 kind 剖面的 `required_extra`／`optional`／`not_applicable`／`entry_level_exemptions` 四表**全空**（@p:QAT，未因本批改动）→ 十五条 `cost_profile.latency_budget_delta` **一律填实**（与 CFG 批依 CFG 剖面 optional 一律省略相反）。无 `row_id` → C-ENV 落 `elif env` 分支并以 envelope 非空判 ok 系**数据形态所致而非豁免**（十五条 envelope 各 4 项、合计 60 项均非空；metric 用 **13** 种、全库 distinct **19** 未增新词）、**Q 系列首建计息**（Q6 `implements` 15／Q5 `triggers` 15／Q4 `triggers` 2＝@7476＋@7661／Y5 `consumed_by` 1＝@8540，`formal_anchor` 合计 245→**278**、role 名零新增）、**两处『三族』不同指不得互代**（G-ENV-1 @8678 自称 6.2.1「只含四族」→ 实测七族 @2783-2789，其所缺三族＝安全 @2787／合规 @2788／可观测性 @2789〔指标族在册口径〕；G-QAT-1 与块头 @7262-7265 的三族＝可伸缩性 @2786／合规 @2788／可观测性 @2789〔6.2.5 战术覆盖口径〕→ 两集合仅「合规／可观测性」重叠；差异只登记不改写）、`aggregation_semantics` 一律 **itemwise**（15/15；5.2.5 @2501 的 Σ 明文只覆盖「流程各步骤卡片 latency_budget_delta」，不覆盖同一目标下多战术叠加 → 不本地造法，MJ-19 同型、先例 `method_registry.yaml` @r:CRD-007#aggregation_semantics〔STY-018 同键行内注「并行分支聚合式母本未给，不本地造法」〕；全库 itemwise 75→**90**／additive 9 未变）、`constraints_imposed` **120** 项（hard 75／soft 30／conditional 15；`target_aspect` 取 {1,2,3,4,5,8,9,10} **八面各 15 项**，交叉表源 6.4 @2864-2871）、60 条 `signal_level` 定级（**P0 17／P1 28／P2 15**，分布非一律：十二条 P0 1／P1 2／P2 1，QAT-007／QAT-011／QAT-013 三条 P0 2／P1 1／P2 1，QAT-015 一条 P0 0／P1 3／P2 1，逐项依据见块头 @7285-7292 与行内注 @8624／@8628／@8632／@8636，定级依 9.2.1 @3585-3587 与 MJ-4）、`typical_reversibility` costly 9／bounded 3／free 2／**irreversible 1（QAT-013，全库首例）**、`compatibility` 仅 **4** 行且**全为单向**（QAT-002→CSL-001 与 QAT-004→CSL-004 两 `tension`、QAT-011→CFG-001 与 QAT-015→RLP-006 两 `requires`，evidence 一律 6.2.5；@2833『联动方面 3 契约』系方面级指引而无母本明文指定对侧 entry_id → 不造关系，先例 CFG-001 @6855-6862；全库 compatibility 132→**136**：requires 16→18／tension 14→16／composable 97／hard_conflict 5）、M4 双通道（QAT 侧扫描 **195** 处＝detection_predicate 60＋applicability 135 → 调用词 **70** 处／distinct **5**〔tactic 54／goal 13／tactic_card 1／verdict 1／cost_ledger 1〕／未登记 **0**；本批方括号内无「词＋左圆括号」形态 → 经与不经 `outside_brackets` @d:registry/scripts/project.py#fn-outside_brackets 结果相同，与 CFG 批 `[CH-C(2)]` 被误读的情形不同；全库 scanned 623→**818**）、占位符三口径 **217／248／990** 不得互代（`bracket_spans` @d:registry/scripts/project.py#fn-bracket_spans 在 QAT 块内命中 217 处／distinct 214；QAT 十五条经 `census_placeholders` @d:registry/scripts/project.py#fn-census_placeholders 得 248 处；全库 990 处／99 条）、累计候选仍 **31** 词、本批零新增（`predicate_vocabulary.yaml` 在册名 **76** 未变），以及 **waiver rule 行母本条款号既有误标**（前六条 @9177／9199／9221／9243／9265／9287 写作『E3（母本 @4011）』，而实测 @4011 系 E2、E3 在 @4012，后五条 @9309／9331／9353／9375／9397 已校正并带行内注 → 前六条属已发布登记，据 0.22 承诺一**只登记不改写**）与**块内自指行号更正纪律**（块内 @NNNN 合计 1320 处／指向块内 73 处／distinct 21；off-by-10 六处共 20 个出现已更正、旧形态 0 处），全文见 `method_registry.yaml` MJ-27 (i)–(xi)。

行级书目登记面：本批十五条 `references` **一律空列表**（全库**首例整批零书目登记面**；空列表条目 32→**47**，`references` 项总数 **83** 批前＝批后、本批零新增）→ M6 严格式平凡为真，**不得读作无外部文献支撑**，亦非豁免；6.7 文献 56 系尾注非独立著录行、书目 12 @1877 的 `compile_usage` 归 1.2.4 面 → 行级面不下探。缺口面落在**目标-手段闭合**（6.2.1 七族中可伸缩性／合规／可观测性三族在 6.2.5 无对应战术 → Q6 @2903 对该三族恒不成立）、**卡片参数化无母本据**（@2836 只给『战术也有代价』的两个示例，未给 `failure_modes` @2494／`observability_requires` @2496 的封闭词汇与量化门槛 → 本批一律不填数值以守 0.4 与 @2791 量化纪律）、**可机器判定性**（无 `row_id` → `table_rows` 不可逐表反查）与**词汇面**（6.5 Q4-Q6 公式侧六词未登记）四处，登记 `G-QAT-1`（含七个裁决口①-⑦）＋勘察义务 `SO-15`（入库期义务，consumer M6，逐口承接该七项）＋词汇缺口 `VG-06`（六词 consumed／mapped／recorded_in／approved_waiver／observability_requires／tactic_registry；另关系词 satisfied 亦缺，系关系词而非谓词 → **待登**，`predicate_vocabulary.yaml` 的 `vocabulary_gaps` 本批仍为 5〔VG-01…VG-05〕、在册名 76 未变，实际追加归 **s5g**；本批**绝不写调用式**，以免制造未登记谓词的既成事实）。状态迁移 `ST-QAT-01`（全 99 条 scope、date 2026-10-10、M2-M6 硬检查全过）。E3 豁免 `WV-QAT-E3-01`（硬性质面 **3 项 18 实例**：Q5 `triggers` **15**〔无条件硬，@2901-2902『行为预算不豁免（Z7 对偶）〕，十五条逐条各 1〕＋Q4 `triggers` **2**〔QAT-002／QAT-004，条件硬〕＋Y5 `consumed_by` **1**〔QAT-014〕；软性质 Q6 `implements` **15** 系**唯一登记的排除面**；`deadline.type` 为 **event**〔编译器首次成功运行，0.17.6(2) 指定的 LRM〕、无日历期限 → 不虚构日期〔0.4〕）已于 **2026-10-11** 经人类裁决批准、`status: active`（系防扩宽条款 (ii) 之下的**第十二次**单独申请；申请登记 2026-10-10，**跨 1 日**；裁决全文见台账 `approval.ruling`；0.10 第一条 @m:235／母本 9.2.2 @3602／1.1 纪律二：批准是人的裁决，Agent 与工具不自行批准——本次裁决由用户在会话中直接指令作出并**明列 Waiver 编号**；QAT 十五条的 seed 资格不以该 Waiver 为前提——C-ST 只查硬检查，故批准延迟未阻断本批入库；与前十一项不同，本项申请与本批入库**同属一次提交** `278baf6`〔不存在『先入库后批准』的跨提交时序〕；0.17.5 的 `draft→seed` 条件为 M2-M6 硬检查全过，E3 属 FVR 接线面而非条目字段面，二者不同轴，SCH／CFG 批同型判读）。**十二项 Waiver 全部 active**，累计覆盖 **99** 条 seed（STY 24＋OWN 4＋CSL 5＋CRD 8＋DEC 8＋CTR 12＋STP 4＋DFL 5＋RLP 7＋SCH 3＋CFG 4＋**QAT 15**）、scope 互不重叠。原「现 `status: pending`」与「十二项 Waiver 中十一项 active、一项 pending」两句系**当时事实**，其逐字形态留存于本文件 git 历史（提交 `278baf6`）与 @d:软件工程元框架成文法-changlog.md#sec-2026-10-10：QAT 批入库（s5e-7）——质量战术 **15** 条（母本 6.2.5 四属性行内顿号清单 **@2829-2832**，**四属性行内清单序**、`provenance` 不含 `row_id`）入库为 `seed`、台账增量七件、`WV-QAT-E3-01` 按防扩宽条款 (ii) **第十二次**单独申请（`pending`，待人类裁决），母本零改动（全文 `QAT` 仅 @400 与 @592 两处、无 `QAT-数字` 形态已发布引用）、注册表达 **99** 条 seed；kind 指称冲突经用户裁决定为 QAT（原指令称「s5e-7 RLP 批」而 RLP 已于 s5e-4 入库并批准），零新增规范命题，本行改写为**现状态**陈述、与 CFG 批准时改写 §4.8 末段 @d:registry/README.md#sec-4.8 CFG 批（行内加粗清单序入库，母本零改动） 同型。§4.7 末段「十项 Waiver 全部 active，累计覆盖 80 条 seed」、§4.8 末段「十一项 Waiver 全部 active，累计覆盖 84 条 seed」与「其余 6 kind（QAT/VFM/GRD/DPS/PRJ/GOV）」、以及 §4.2–§4.6 末段的批次清单同样**不回改**（0.22 承诺一：已发布登记不改写、差异只登记）；其余 **5** kind（VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.10 VFM 批（单行内六类顿号清单序入库，母本零改动）

**两项用户裁决（2026-10-11）先行留痕**：① 条目粒度经用户裁决定为 **6 条**——源＝8.2.1 @3319『手段映射注册表』单行内六类顿号清单，而非按 8.2 各子节拆；『测试』一类的五个括注子项（单元/集成/契约/行为注入/端到端）**不拆**为五条，三根据＝8.2.2 四层表（表头 @3325-3326＋四数据行 @3327-3330）系职责分配面而非手段面、@3332『金字塔失真』信号系单一承载于测试类的判据、T4／T5／T6／T7（@3438-3443）的执行域分别为单元层／金字塔结构／契约层／注入用例，拆则同一性质被多条目重复承载 → 违 0.9 唯一真相；8.2 其余子节按面降入各条（8.2.2＋8.2.3 → VFM-004；8.2.4 → VFM-001；8.2.5＋8.2.6 → VFM-002，其中 8.2.6 系**双承载**〔另由 VFM-005 承载人工评审记录面〕；8.2.7 → VFM-005）；@3319 的『计划矩阵形态』五元组在六类清单内**无承载条目** → 缺口登记 `G-VFM-1`、**不增第七条**（MJ-9 不扩张／0.17.1 零新增规范命题）。② `constraints_imposed.target_aspect` 的『全部方面』编码经用户裁决定为 **`0`**（8.4 施加表 @3408『全部方面』行，含义固定为「全部方面（1–10）」），**不得与 {1,…,10} 十面逐列互代**，判读入 MJ-28 (ii)、登记于块头 @8668-8678。批次台账日期系多口径：两项裁决日 **2026-10-11**、`G-VFM-1` 落盘日 **2026-10-16**、`ST-VFM-01` 及其后台账项落盘日 **2026-10-17**、机器 `date` 实测 **2026-10-18**（与系统环境所载 2026-10-17 不一致 → 两口径并列登记于 MJ-28 basis 末段 @10445，已落盘处的 2026-10-17 不回改），四者不得互代。判读全文见 MJ-28 (i)／(ii)、块头 @8650-8663 与 @8668-8678。

母本既有已发布引用勘察结论（2026-10-17）：母本全文 `VFM` 仅**三处**——@402（0.17.3 kind 封闭枚举行「VFM | 验证手段 | 方面 8 · 8.2」）、@3480（8.6 消费字段行「VFM 卡片.failure_modes{可逆性标记}」）与 @3536（8.6 内「T1/T7; VFM 验证手段注册表条目」行）。**无 `VFM-数字` 形态的已发布引用**（同 CTR／STP／DFL／RLP／SCH／CFG／QAT 七批，与 STY/CSL/CRD/DEC 四批不同），故本批无需 R2 修订母本，母本 4427 行／围栏 216 不变。

编号方案＝**单行内六类顿号清单序**（本库**第五种**源形态：既非表格〔CTR／STP／DFL〕，亦非 5.2.4 类单段落分号子命题〔SCH〕、非 5.2.6 类行内加粗清单〔CFG〕、非 6.2.5 类四属性行内顿号清单〔QAT〕——六类同处母本**一行**之内，加粗只落引导词『手段映射注册表』而不到项级）：母本 8.2.1（heading @3311）的正文＝三方面输入 @3313-3317（@3315 系『性质 → 手段』存在量词）＋计划矩阵形态与手段映射注册表 @3319（**单行**），既无表格行列结构亦无行标识，故六条 `source_pointers` 一律 clause 形态、实测 **73** 处（11／11／9／15／12／15）**全 `clause_id`、零 `row_id` 零 `bib_id`**；`name` 取六类词**逐字去括注与粗体标记**（括注内容降入 `narrative` 与 `compatibility`／`formal_anchor`，故 VFM-004 作『测试』而非『测试（单元/集成/契约/行为注入/端到端）』、VFM-005 去 @3319 的粗体作『人工评审』）；母本原形不改写＝@3319 三处括注内半角斜杠（结构性性质 V1/W4/X1 类、状态机性质 Z3/Z8 类、单元/集成/契约/行为注入/端到端）一律不改顿号；8.2 全节唯一表格（8.2.2 测试分层表 @3325-3330）系四层职责分配面 → 降入 VFM-004、**不作分块源**。**分块序裁决**（兑现 `profiles.yaml` @p:VFM#seed_source.entry_id_range 末句「裁决见 README §4.10」的强制指针）：非表源无行序可依 → 取 @3319 单行内六类顿号列举序，MJ-13 (iv)「表行序」判据的源为表格 → 不直接适用而是同型推广（列举序即源序）；与 RLP-001…007（§4.6）、SCH-001…003（§4.7）、CFG-001…004（§4.8）、QAT-001…015（§4.9）四批同型，判读全文见 MJ-28 (i)：

| entry_id | @3319 顿号列举序 | name（取六类词逐字、去括注与粗体） |
|---|---|---|
| VFM-001 | 第 1 类 | 静态分析 |
| VFM-002 | 第 2 类 | 可执行检查程序 |
| VFM-003 | 第 3 类 | 模型检查 |
| VFM-004 | 第 4 类 | 测试 |
| VFM-005 | 第 5 类 | 人工评审 |
| VFM-006 | 第 6 类 | 生产监测 |

`profiles.yaml` 的 `kind_profile_VFM.seed_source` 两占位符（`table_rows`／`entry_id_range`）本批填实（@p:VFM#seed_source.table_rows／@p:VFM#seed_source.entry_id_range），其中 `table_rows` 记「不适用」（单行内六类顿号清单，非表格、无行标识，覆盖宣称系人工清点 → 不可机器判定，META 侧据此落 info；此形态系 `G-VFM-1` impact (a)／route ① 之预定而非本项自拟）；填实系**行数中性**（该文件仍 wc 585／split 586），因 registry 内多处引用 @p:VFM#seed_source.table_rows／@p:VFM#seed_source.entry_id_range／@435／@p:VFM#optional／@p:VFM#narrative.note → 行数中性系硬约束（MJ-28 (xii)(丙)）。无 `row_id` → C-ENV 落 `elif env` 分支 @d:registry/scripts/project.py#fn-check_cenv 并以 envelope 非空判 ok 系**数据形态所致而非豁免**；六条 envelope 各 4／4／3／5／3／4 项、合计 **23** 项且 `bound_expr` **互不相同**（`source` 一律 `clause_id: 6.2.1`，键行 @8820／8912／9001／9101／9224／9320；**M3 全过**＝23 项全部参数化且 source 反查命中，含数值比较符 **0** 处）、metric 用 **11** 种而全库 distinct **19** 未增新词（@p:VFM#narrative.note note 所记验证效能类三指标在册**无形态** → 本批改以被守护质量属性族为轴，不虚构指标名以守 0.4）；剖面 `optional` 明列 `cost_profile.latency_budget_delta`（@p:VFM#optional）→ 六条中**仅 VFM-006 填实**该键（键行 @9334，全库键行 96）、余五条省略（与 CFG 批依 optional 一律省略、QAT 批四表全空故一律填实**两种处置均不同**）；**T 系列全系首建计息**（`formal_anchor` 合计 278→**293**、distinct `property_id` 38→**47**〔＋9＝T1…T9 全系首次入库〕、role 分布 `implements` 107→**122** 而 `consumed_by` 141／`triggers` 30 **零增** → 十三批中唯一不增该两 role 者；裸词口径 T1 80／T2 28／T3 37／T4 28／T5 17／T6 45／T7 31／T8 34／T9 36 系引述面而非计息面）、**不登 Z3／Z8 与 V1／W4／X1**（@3319 括注系举例而非成对绑定，MJ-28 (iv)）、`aggregation_semantics` 一律 **itemwise**（6/6，键行 @8839／8931／9017／9123／9240／9340；全库 itemwise 90→**96**／additive 9 未变）、`constraints_imposed` **30** 项（hard 18／soft 12／conditional 0；`target_aspect` 取 {0,1,7,9,10} **五面各 6 项**，其中 **0 系『全部方面』编码、不得与十面逐列互代**，交叉表源 8.4 @3408-3412；全库 654 项＝hard 478／soft 127／conditional 49）、**24** 条 `signal_level` 定级（**P0 4／P1 12／P2 8**；逐条 1/2/1・2/2/0・0/2/2・0/2/2・1/1/2・0/3/1；P0 四项母本据＝VFM-001-AP1←T1 @3433、VFM-002-AP1←T-F1 @3353、VFM-002-AP3←T3 @3436-3437＋@3361、VFM-005-AP1←T8 @3444-3445＋@3368；全库 294＝P0 101／P1 139／P2 54）、`typical_reversibility` free 1／bounded 3／costly 2（六条依序 free／bounded／bounded／costly／costly／bounded，键行 @8806／8898／8987／9087／9210／9306，系**条目顶层键**而非 `cost_profile` 内键；全库 costly 50／bounded 44／free 10／irreversible 1）、`compatibility` 仅 **3** 行且**全为单向 `requires`**（VFM-001→CFG-001、VFM-004→CTR-009、VFM-004→CTR-010；@3319『与方面 9 共享信号源』系方面级指引而无母本明文指定对侧 entry_id → 不造关系，先例 CFG-001 @6855-6862；全库 139＝composable 97／requires 21／tension 16／hard_conflict 5、空块 37）、M4 双通道（VFM 侧扫描 **78** 处＝`anti_patterns` 24〔6×4〕＋`applicability` 54〔6×9〕→ 调用词 **39** 处／distinct **11**／未登记 **0**；全库 scanned 818→**896**）、`applicability` 三空间 **54** 项（逐条 9）而质量影响卡片三字段 `failure_modes` 39／`observability_requires` 32／`skill` 33（逐条 [6,4,5]／[7,6,5]／[6,5,5]／[8,6,7]／[6,5,5]／[6,6,6]；本 kind 剖面**无 `quality_impact_card` 键** → 与 QAT 卡片面不同轴；全库 548→**602**）、占位符三口径 **96／102／1092** 不得互代（`bracket_spans` @d:registry/scripts/project.py#fn-bracket_spans 在 VFM 块内命中 **96** 处／distinct 94〔重数 2 者两处〕；VFM 六条经 `census_placeholders` @d:registry/scripts/project.py#fn-census_placeholders 得 **102** 处〔17／15／17／19／16／18〕；全库 **1092** 处／**105** 条）、`trust_marks` 本批 **7** 处／4 条（001:1／002:1／003:0／004:4／005:0／006:1，一律 `[已核验]`；全库 83→**90** 处／52→**56** 条）、累计候选仍 **31** 词、本批零新增（`predicate_vocabulary.yaml` 在册名 **76** 未变）、**四处既有差异只登记不改写**（MJ-28 (xi)）与**门槛编号错位系全库性**（HEAD 61 处／59 行、工作文件 71 处／69 行、本批新增 10 处／10 行 @8873／@8964／@9181-9184／@9380／@9539／@9951／@10239 → 与前批 localized 型不同，MJ-28 (xiii)），全文见 `method_registry.yaml` MJ-28 (i)–(xiii)。

行级书目登记面：本批六条 `references` 为**两条空列表＋四条非空合计 7 项**（VFM-001〔书目 13〕／VFM-002〔61〕／VFM-004〔60／62／63／65〕／VFM-006〔64〕；VFM-003／VFM-005 空列表 → 全库空块 47→**49**、项总数 83→**90**、非空块 52→**56**）。成因与 QAT 批（6.7 系尾注、无著录槽位 → 整批零书目）**不同型**：8.7（heading @3557）的 @3559-3565 系**行级登记表**（带 ISBN／`trust_grade`／`compile_usage`），符合本文件 CSL-005 `references` 第 2297–2298 行（bib_id 36）所确立的行级登记条件 → 系既有先例而非新造。VFM-003／VFM-005 留空**不得读作『无外部文献支撑』**（unknown ≠ false，0.18.6 M15），M6 对空集**平凡为真、非豁免**；书目 65 的 `compile_usage: case_study` 系**本批唯一非 `metadata_extraction` 项**，而全库实测该取值共 **2** 处（第一处＝书目 19／carrier STY-016 第 1223 行，HEAD 已发布）→ 本批系**第二处、非全库唯一**（原判读经 MJ-28 (xii)(壬) ④ 自纠留痕），其用途边界＝只作成例证据、不提取规范命题（0.17.7 门槛 6）；@3565『不重复著录』→ 书目 28／29／5／47 **不重复登记**（carrier CTR-009／STY-001…004·016／CRD-005·006 已在案）。缺口三面＝`G-VFM-1`（含**十个**裁决口，route @9539，`status: open`）＋勘察义务 `SO-16`（consumer M6，`status: open`）＋词汇缺口 `VG-07`（**待登**；`predicate_vocabulary.yaml` 的 `vocabulary_gaps` 本批仍为 5〔VG-01…VG-05〕、在册名 76 未变，实际追加归 **s5g**；本批**绝不写调用式**，以免制造未登记谓词的既成事实）。状态迁移 `ST-VFM-01`（全 **105** 条 scope、date **2026-10-17**、M2-M6 硬检查全过）。E3 豁免 `WV-VFM-E3-01`（rule 母本 @4012；硬性质面 **7 项 13 实例**＝T1 6／T2 1／T3 2／T4 1／T6 1／T8 1／T9 1，软性质 T5／T7 计 **2** 项 2 实例系**明文排除面**——若二者升为硬则豁免面**扩张**、须另起新 Waiver〔防扩宽条款〕，合计 scope **9 项 15 实例**；`deadline.type` 为 **event**〔编译器首次成功运行，0.17.6(2) 指定的 LRM〕、`calendar_date: null` → 不虚构日期〔0.4〕）已于 **2026-10-18** 经人类裁决批准、条目级 `status: active`（`approval.status: approved`；系防扩宽条款 (ii) 之下的**第十三次**单独申请；申请登记 **2026-10-17**、**跨 1 日**；裁决全文见台账 `approval.ruling`；0.10 第一条 @m:235／母本 9.2.2 @3602／1.1 纪律二：批准是人的裁决，Agent 与工具不自行批准——本次裁决由用户在会话中直接指令作出、**未复述 Waiver 编号**，按『台账中唯一 pending 者』解析（与 DEC 项同型、与 QAT／CFG 两项明列编号不同型），`approved_by`／`approved_date`／`ruling` 三键于裁决后落盘、未预置空键）；VFM 六条的 seed 资格**不以该 Waiver 为前提**——C-ST 只查硬检查，0.17.5 的 `draft→seed` 条件为 M2-M6 硬检查全过，E3 属 FVR 接线面而非条目字段面，二者不同轴（SCH／CFG／QAT 三批同型判读）；`anti_widening` 记其余 **4** kind（GRD/DPS/PRJ/GOV）同型待办 @10249（经本项三键插入位移 +3，原 @10246 系本段撰写时实测值，其逐字形态留存于 git 历史与 changlog）。**十三项 Waiver 全部 active**（本项落盘后），累计覆盖 **105** 条 seed（STY 24＋OWN 4＋CSL 5＋CRD 8＋DEC 8＋CTR 12＋STP 4＋DFL 5＋RLP 7＋SCH 3＋CFG 4＋QAT 15＋**VFM 6**）、scope 互不重叠；原「现 `status: pending`、批准日待定」与「本批六条**尚未计入**（待人类裁决后另行改写为十三项／105 条）」二句系**当时事实**，其逐字形态留存于本文件 git 历史（提交 ed9e271）与 @d:软件工程元框架成文法-changlog.md#sec-2026-10-17：VFM 批入库（s5e-8）——验证手段 **6** 条（母本 8.2.1 @3317 手段映射注册表六类，**单行内六类顿号清单序**、`provenance` 不含 `row_id`）入库为 `seed`、台账增量七件、`WV-VFM-E3-01` 按防扩宽条款 (ii) **第十三次**单独申请（`pending`，待人类裁决），母本零改动（**4427**／围栏 **216** 不变）、注册表达 **105** 条 seed；`--check` **907｜硬失败 0｜软警告 0｜占位符 1092**、投影四件 **3629→3891**，零新增规范命题，本段改写为**现状态**陈述、与 QAT 批准时改写 §4.9 末段 @203 同型；§4.7／§4.8 末段与 §4.2–§4.6 末段的批次清单同样**不回改**（0.22 承诺一：已发布登记不改写、差异只登记）；其余 **4** kind（GRD/DPS/PRJ/GOV）仍适用同一模式。

### 4.11 DPS 批（单表表序入库，母本零改动）

母本既有已发布引用勘察结论（2026-11-03，M1 强制核查）：母本全文 **无 `DPS-数字` 形态的已发布引用**；@3241／@3742／@3775 三处 `DPS.xxx` 均为**消费字段称呼、非 entry_id**（同 §4.3 CTR 批对 `CTR-gRPC`／`CTR.compatibility.policy`／`CTR.lifecycle_state` 三处称呼的处置，MJ-21 (i) 同型）→ 本批无需 R2 修订母本，母本 4427 行／围栏 216 不变（同 CTR／STP／DFL／RLP／SCH／CFG／QAT／VFM 八批模式）。

编号方案＝**单表表序**（承 §4.2 MJ-13 (iv) 同型：9.2.5 为一张表，行序即 id 序）：

| entry_id | 母本源行（9.2.5，@3640-3644） | name（取表首列逐字） |
|---|---|---|
| DPS-001 | 第 1 行 | 滚动发布 |
| DPS-002 | 第 2 行 | 蓝绿发布 |
| DPS-003 | 第 3 行 | 金丝雀发布 |
| DPS-004 | 第 4 行 | 功能开关驱动发布 |
| DPS-005 | 第 5 行 | 回滚规程 |

**DPS-005『回滚规程』跨策略义务判读（2026-11-03 用户裁决：维持现状）**：其『适用条件』列 @3644 逐字『全部策略（无回滚规程的部署策略不予注册）』→ 语义上系**跨策略义务**而非独立发布策略；但母本将其置于 @3638 表头『策略』列、且 0.17.3 的 DPS kind 由 9.2.5 整节承载 → **按表行序取 DPS-005、不跳过不改序、不另立义务 kind**（0.22 编号永不复用/重排）；判读痕迹留于块头 @9385-9419、`ST-DPS-01.note` 与 `MJ-29` (i)，三处并列留痕、互不替代。**MJ-9 不扩张三面**（母本未把条目明文成对者只留注、不造关系）：① DPS-002 ↔ DFL-002——@3641『数据层双写/迁移方案是必答项（联动 Y 域）』系方面级联动、未明指 CDC 条目；② DPS-001 ↔ CTR-007／CTR-008——@3640『版本间协议兼容（X 系列契约约束）』系属性族指针、CTR 侧未成对；③ DPS-003 ↔ VFM-006——@3642『生产观测能力就绪』与 VFM-006 同源但两批均未写成对。三面判读载块头 @9407-9417 与 `MJ-29` (iii)。

条目字段面（YAML 解析实测）：`provenance.source_pointers` 五条 **53** 处（11／10／10／11／11，一律 `{clause_id: "9.2.5"}` ＋ `{row_id: "9.2.5-{策略}"}` 双支，`origin` 一律 `hybrid`）；`envelope` **15** 项（5×3，`latency_budget_delta` 五条一律填实——DPS 剖面 required）；`applicability` **30** 项（5×6，三空间各 2）；`constraints_imposed` **35** 项（7 行 × 5 条，表源 9.4『施加约束』@3682-3688；hard **20**／soft **10**／conditional **5**；`target_aspect`＝方面 1 **10** 项、其余 {0,2,7,8,10} 各 **5** 项）；`anti_patterns` **15** 条（`signal_level` P0 **6**／P1 **5**／P2 **4**，`pattern_id` 严格 `DPS-00N-APi`）；`formal_anchor` **7** 项（G3 implements **5**→首次入账、G4 implements **1**→DPS-003 首次入账、Z6 implements **1**→DPS-004，Z6 系跨批共享性质、全库第 3 实例且前 2 实例由 `WV-CFG-E3-01` 承担）；`references` **6** 项、五条**全非空**（DPS-001…004 各 1＝书目 67；DPS-005 2＝书目 46＋67；9.7 @3839 `compile_usage=metadata_extraction`、@3842 第 70 条『不重复著录』）；`compatibility` **9** 行（requires **5**／composable **4**：同批跨策略镜像 8 行——DPS-001／002／003／004 → DPS-005 requires ＋ DPS-005 → DPS-001…004 composable；跨 kind 单侧 1 行——DPS-004 → CFG-003 requires，CFG-003 侧按 MJ-5 不回填）。

台账与计数面（终值以 `--check`／`--project` 实跑为准）：`ST-DPS-01`（draft→seed，scope **110** 条全集形式面、实际迁移对象为末 **5** 条，date 2026-11-03）；`WV-DPS-E3-01`（**第十四次**单独申请，`approval.status: approved`／条目 `status: active`／`approved_date: 2026-11-03`，**未给具体时刻→不写时点、不写近似值**；scope 硬性质 **3 项 7 实例**＝G3 5／G4 1／Z6 1）；`MJ-29`；词汇缺口 **`VG-08`**（9.5 @3700-3703 的 deploy_strategy／canary_gate／evolution_path／strangler_sequence ＋ 公式侧 `gate_verdict`，只登记、不扩词，归 s5g）；**`G-DPS-1` 经评估不成立**（9.2.5 五行全覆盖、五条 references 全非空、G3／G4／Z6 锚点均落位，唯一未闭合者系词汇面 → 由 `VG-08` 承载）→ gaps 仍 **18**、`survey_obligations` 仍 **16**。全批计数：entries **105 → 110**；占位符 **1092 → 1165** 处／**110** 条（DPS **73**＝15／17／15／13／13）；指针 **1848 → 1931（M2）→ 1934（M3）**／miss **0**（`method_registry` 1647→1730→**1733**／`profiles` **125**／`predicate_vocabulary` **76**）；自检记录 **906（M1 基线）→ 947（M2）→ 948（M3）**｜硬失败 **14 → 0**｜软警告 **0**；`status_transitions` **13→14**；`waivers` **13→14**（**全部 active·全部 approved**，累计覆盖 **110** 条 seed、scope 互不重叠）；`manual_judgments` **28→29**；`vocabulary_gaps` **5→6**；`profiles.gaps` 仍 **4**；`pending_conflict_rows` 开放 **0**／已闭合 **4**。四件投影重生成：`STY.md` 1657→**1741**／`勘察义务清单.md` 1714→**1817**（逐条枚举 1165 处、DPS 侧 73）／`索引.md` 263→**271**／`自检报告.md` 256→**269**（`--check` 先行生成）＝合计 3890→**4098**；源哈希 `method_registry.yaml`→**`872d1def4067`**、`profiles.yaml`→**`0f225f62cc1e`**、`predicate_vocabulary.yaml`→**`cbdf6da217fa`**。母本零改动（4427 行／围栏 216）；§4.2–§4.10 末段的批次清单**不回改**（0.22 承诺一）；其余 **3** kind（GRD/PRJ/GOV）仍适用同一模式，且受 s5e-10 阻断口限制。

### 4.12 KP-G3 R2 母本澄清（0.17.2 同行追加；母本 1/1、行数中性）

2026-11-03 用户批准 `R2提案-KP-G3-包络义务适用范围.md` 的推荐读法（**宽读**）与拟改写文本，并给出四项授权边界：①只闭合 `envelope`／`cost_profile` 轴；②`applicability` 不纳入 N-A（另案，本轮不做）；③PRJ 的 `applicability.delivery_space` 保持必填、不按 N-A（保留「诚实失败」）；④母本改动只允许在 0.17.2 同一行末尾追加一句，不新增行、不改其他条款。

改写位置（锚点实测，非盲信提案行号）：母本 `软件工程元框架成文法.md` @**381** 行末；单行本 `软件工程元框架总纲单行本.md` @**363** 行末（同一句、逐字一致）。追加句界定 0.8 所称「每种方法条目」＝0.17.3 封闭枚举的全部 kind，并允许 kind 不以质量属性为选择判据时把 `envelope`／`cost_profile` 在本剖面登记为 `not_applicable`（逐项附 `reason` 引用本条、`provenance.origin=compiled`），此为显式豁免而非省略；该句只界定 0.8 包络义务，不改变其他字段的必填判定。

断言实测：母本 `split('\n')` **4428**／行数 **4427**／围栏 **216**，改前改后**不变**；`git diff --numstat`＝**1/1**（`--word-diff` 只出现该句追加词）；sha256 `206c018ce309…` → `2663fc119f39…`。单行本 `git diff` 只含该句（numstat **1/1**），行数 **1285**／`split('\n')` **1286**／围栏 **36** 不变；sha256 `6fdb3d084507…` → `93fd7406db4b…`。

**本轮不产生条目、不改剖面**：`entries` 仍 **110**；`profiles.yaml` 三 kind 的 `status`／`undecided_fields`／`not_applicable`／`entry_level_exemptions` **未动**（待 `entry_id_range` 与「条目面两读」裁决，见 `ADR草案-GRD-PRJ-GOV-剖面变更.md`）；`--check`／`--project` 未跑、四件投影未重生成；s5e-10 M2 仍**未启动**。§4.2–§4.11 末段的批次清单**不回改**（0.22 承诺一）。

### 4.13 s5g 词汇表欠账收口（VG-06／VG-07；两项裁决；无新增条目、母本零改动）

> 编号注：**§4.12 已由 KP-G3 R2 登记占用**（@246-254），本节按顺延取 **§4.13**；§4.11 及更早的批次清单与计数陈述**不回改**（0.22 承诺一）。

**来源**：QAT 批块头 @7279-7284 ＋ G-QAT-1 statement (8)／route ⑥（`method_registry.yaml` @9987／@9990）预告 `VG-06`；VFM 批块头 @8708-8716 ＋ G-VFM-1 statement (3)／route ②（@9995／@9998）预告 `VG-07`。两处只预告未落盘；`VG-08` 因避撞号先落于 s5e-9（DPS）。

**落盘**：`predicate_vocabulary.yaml` 新增 `VG-06`／`VG-07`，五字段（`id`／`missing_need`／`workaround`／`affected`／`route`）与 `VG-04`／`VG-05` 同型；编号 **VG-01…VG-08** 连续，`VG-08` 既有文本未改。

**裁决一（`mapped` 并条）**：`mapped` 归 `VG-06`（母本唯一出处 6.5 @2903 Q6）；`VG-07` 移除该词并在 `missing_need` 留移出注、`route` 留编号注（8.5／T1–T9 @3419-3447 实测无此词）→ `VG-07` 覆盖 **十七→十六** 词（九机器层＋七公式侧）。G-VFM-1 预告文本不改写（0.22 承诺一）。

**裁决二（QAT 七词并入）**：批次块头 @7279-7283 的 Q1–Q3／Q7 面七词（`routed_to`／`weight_source`／`band`／`defined`／`monitored`／`human_ruling_pending`／`selected`）并入 `VG-06` 补充组，**不另立 `VG-09`**；`VG-06` 合计 **十三词**（六＋七）。G-QAT-1「六词」正式口径不改写、差异在条内登记；`satisfied` 仍按关系词排除。

**计数**：`vocabulary_gaps` **6→8**（VG-01…VG-08 连续）；在册谓词 **76**（predicates 59＋formula_words 7＋clause_defined_predicates 10）**未变**；两批 `detection_predicate`／`applicability` 未登记调用式实测 **0**（缺口只在定义面）；`entries` 仍 **110**，`gaps` 18／`survey_obligations` 16／`manual_judgments` 29／`status_transitions` 14／`waivers` 14 未动。

**自检与投影**：948 条记录｜硬失败 **0**｜软警告 **0**｜占位符 **1165** 处／110 条｜指针 **1934**／miss **0**；四件投影重生成，行数 `STY.md` **1741**／`勘察义务清单.md` **1817**／`索引.md` **271**／`自检报告.md` **269**（合计 4098）**未变**，三件仅 footer 更新、`自检报告.md` 另含台账行 `vocabulary_gaps 6→8`；源哈希 `predicate_vocabulary.yaml` `cbdf6da217fa`→`67a11b81cec1`→**`025b999d0251`**（两轮迭代终值），`method_registry.yaml` `872d1def4067`／`profiles.yaml` `0f225f62cc1e` 未变。母本零改动（4427 行／围栏 216）。

### 4.14 KP-G3 剖面执行＋`manual` 口径收窄（2026-11-03；母本零改动）

> 编号注：**§4.12／§4.13 已分别由 KP-G3 R2 与 s5g 占用**，本节按顺延取 **§4.14**；§4.2–§4.13 的历史陈述与计数**不回改**（0.22 承诺一）。

**一、剖面变更（ADR-KP-G3-01 落地，仅 `profiles.yaml`）**。用户裁定种子面三读：GRD 只取 **9.2.1 主表 3 条**（P0／P1／P2），9.2.3 九信号源暂不收（部署类信号与 DPS 9.2.5 重叠，须先分工）；PRJ 只取 **10.2.2 义务表 11 条**，C4／arc42 16 行实例表母本明文「实例级，非规范」→ 不作种子；GOV 只取 **0.5 六行**，7.2.3 简记格式不单列条目、作 note 内格式约束。三件 `status` `draft`→`seed`；`undecided_fields`→`[]`（PRJ 的 `applicability.delivery_space` **移出但仍必填**，note 追加「该字段仍须逐条勘察取值，非 N-A」——保留诚实失败，不伪装成豁免）；`not_applicable` 每 kind **8 项**（`envelope` ＋ 7 个 `cost_profile.*`），依据 0.17.2 @382 末句、`provenance: compiled`；`entry_level_exemptions` 每 kind **1 条 `C-ENV` 全批豁免**（scope＝GRD-001…GRD-003／PRJ-001…PRJ-011／GOV-001…GOV-006）；`seed_source` 两占位符填实。

**二、`provenance.origin = manual` 口径收窄（头注 @13-14 追加）**。裁定人＝用户。头注原文保留，其后追加：「`provenance.origin = manual` 仅适用于字段取值与 `optional` 判定；`not_applicable` 属完备性判定，须有母本明文依据，不得以 `manual` 替代。」理由：`manual` 管「取值／是否 optional」，`not_applicable` 管「完备性判定」，两者不是同一层——没有母本依据时可以承认「这是人判断的值」，但不能声称「这不需要该字段」。**与 GOV note（原 @560、本轮改后 @p:GOV#narrative.note，原文不改写）的关系**：本节只收窄头注适用范围，使「头注允许 manual N-A」与「需母本明文方可 N-A」不再两读；三 kind 的 N-A 依据为 0.17.2 @382 末句（`provenance: compiled`），不依赖 `manual`。

**三、自检与投影**（`--check`／`--project` 实跑，两轮同值）：**948** 条记录｜硬失败 **0**｜软警告 **0**｜entries **110**｜占位符 **1165** 处／110 条｜指针 **1960**／miss **0**（`profiles` **125→151**，`method_registry` **1733**，`predicate_vocabulary` **76**）｜`vocabulary_gaps` **8**｜`gaps` **18**／`survey_obligations` **16**。`索引.md` 剖面表三行＝`status` **seed**／required **18**／optional **0**／N-A **8**／undecided **0**／豁免 **1**。四件投影行数 `STY.md` **1741**／`勘察义务清单.md` **1817**／`索引.md` **271**／`自检报告.md` **269**（合计 4098）**不变**；哈希 `ca4a5f5696af`→`b7626efa62e5`／`e92bb0b6ac4c`→`cd51a10d32d2`／`b1b85bf54ae4`→`3f1cdd32d274`／`0191383b78df`→`df001852ce8e`（两轮重生成终值）；`profiles.yaml` 哈希 `0f225f62cc1e`→**`42de431a30db`**。**无 GRD／PRJ／GOV 条目 → C-ST／META／C-ENV 均无条目级记录；META 的 draft＋条目硬失败面因 `status=seed` 不再成立**（判定依脚本实测，非宣称）。

**四、未做**：`method_registry.yaml`、母本、单行本零改动；无条目 → s5e-10 M2 未启动；**不 commit、不 push**。

### 4.15 KP-G3 闭合登记（`status: open → closed` ＋ 同条目 `closure` 块；母本零改动）

> 编号注：**§4.12／§4.13／§4.14 已分别由 KP-G3 R2、s5g、KP-G3 剖面执行占用**，本节按顺延取 **§4.15**；§4.2–§4.14 的历史陈述与计数**不回改**（0.22 承诺一）。

**一、闭合形态＝改 `status` ＋ 同文件就地追加闭合登记（不另起 `KP-G3-closed`）**。工具依据：`check_ledgers` 对 `profiles.yaml: gaps` 只做**要素齐备**检查（[project.py](file:///home/wgz/projects/skills/software-engineering/registry/scripts/project.py#L1069-L1073)：`gap_id`／`type`／`statement`／`impact`／`route`／`status` 六键非空即过），**`status` 取值不参与任何硬／软判据**；`--project` 的缺口表只遍历 `method_registry.yaml` 的 `gaps`（@1548-1552），剖面缺口不进投影 → `open → closed` 不新增、不减少任何检查记录。与「已发布登记不改写」（0.22 承诺一）的边界：**`statement`／`impact` 逐字未动**，改动的只是一个状态标量；闭合依据以**同条目内新增 `closure` 块**留痕（`gap_ref`／`date`／`ruled_by`／`basis`／`evidence`／`preserved`），并在 `preserved.impact` 显式声明「三剖面 `status=draft`」系 2026-11-03 前的事实、闭合后已过期、以 `closure` 为准。不另起 `KP-G3-closed` 的理由：另起一条会使 `profiles.gaps` **4→5** 且原条目仍 `open`，台账同时出现「仍开放」与「已闭合」两条互相矛盾的记录；就地改状态并留痕，后来人一处可读「原始问题→当时为何 open→现在凭什么闭合」。

**二、实际改动（仅 `registry/profiles.yaml` 的 `gaps` 段）**。@**686-704**（KP-G3 条目，原 @686-691）：`status: open → closed`（@**691**，行内注指向 `closure`）；新增 `closure` 块 @**692-704**（六键）；`statement`（@**688**）／`impact`（@**689**）原文逐字未动；numstat **+14/−1**。`gaps` 仍 **4**，状态计数 `open` **3**／`closed` **1**（首次出现 `closed` 取值；工具无枚举约束，见第一节）。

**三、闭合依据（裁定人＝用户；2026-11-03）**。母本 **0.17.2 @382** 行末追加句（单行本 @**363** 逐字一致）界定 0.8「每种方法条目」含 0.17.3 全部 kind、非质量属性判据者可登记 `not_applicable` 并附 `reason` 与 `provenance.origin=compiled`（R2-KP-G3-01）；数据侧 ADR-KP-G3-01 已执行：三剖面 `status` @**477**／@**546**／@**611** 均为 `seed`、`undecided_fields: []`、`not_applicable` 各 **8** 项、`entry_level_exemptions` 各 **1** 条 `C-ENV`、`seed_source` 两占位符填实。原 `impact` 所述阻断面（C-ST 禁 `seed`）**已不成立**。

**四、验证（`--check`／`--project` 实跑，改前 → 改后）**：

| 指标 | 改前 | 改后 |
|---|---|---|
| 自检记录 | 948 | 948 |
| 硬检查通过／失败 | 807／0 | 807／0 |
| 软警告 | 0 | 0 |
| entries | 110 | 110 |
| 占位符 | 1165 | 1165 |
| 指针／miss | 1960／0 | 1960／0 |
| `gaps`（method_registry） | 18 | 18 |
| `profiles.gaps`（open／closed） | 4（open 4） | 4（open 3／closed 1） |
| `vocabulary_gaps` | 8 | 8 |
| `profiles.yaml` sha256 前 12 位 | `42de431a30db` | `13f961d61ff1` |

**五、投影四件（`--project` 重生成）**。行数 `STY.md` **1741**／`勘察义务清单.md` **1817**／`索引.md` **271**／`自检报告.md` **269**（合计 **4098**）**不变**；每件仅 footer **1/1**（生成戳＋`profiles.yaml` 源哈希），四件正文零差异；哈希 `b7626efa62e5`→`8f4674f6a939`／`cd51a10d32d2`→`32343f916677`／`3f1cdd32d274`→`b2ff7b8aa8af`／`c8b11e31bff9`→`70f0bba344f7`（前三项改前取 HEAD 定稿值；`自检报告.md` 改前取 HEAD 定稿值，基线 `--check` 本身会更新生成戳）。

**六、围栏复核**：本文件 **2**（偶数）／`todo.md` **0**／`软件工程元框架成文法-changlog.md` **0**／`profiles.yaml` **0**。

**七、未做**：`method_registry.yaml`（并行任务面，本轮实测工作区未改动）、母本、单行本、`predicate_vocabulary.yaml` **零改动**；**不 commit、不 push**。

### 4.16 s5e-10：GRD／PRJ／GOV 三 kind 入库与 M3 收账（2026-11-03）

**一、批次定义与粒度**。s5e-10 M2 按三个 kind 分批，共 20 条：GRD 3 条（9.2.1 @3583-3587 主表 P0 阻塞级／P1 限期级／P2 监测级，严格表行序；9.2.3 @m:9.2.3 九信号源本期不收）＋PRJ 11 条（10.2.2 义务表 @3874-3884：1.4／2.4／4.4／5.4／8.4／9.4＋8.2.7 评审点一–五；C4／arc42 的 16 行实例表 @3892-3903 按母本「实例级，非规范」不作种子）＋GOV 6 条（0.5 表 @117-122 六类 ADR，表行序；7.2.3 @3044-3051 简记格式不单列条目，登记为 GOV 块头格式约束：五字段 {唯一ID, 一句话决策, 依据指针, 时间戳, 执行者}＋打包／复查／禁令）。20 条一律 `status: seed`，编号逐字取表首列，0.22 承诺一零改写。

**二、schema 与剖面**。条目字段逐字采用 0.17.2；三 kind 剖面均 status=seed、undecided_fields=[]，各 8 项 N-A（envelope＋cost_profile.*，@382 末句 R2 澄清），C-ENV scope 分别覆盖 GRD-001…003／PRJ-001…011／GOV-001…006；GRD required_extra 为 anti_patterns／formal_anchor，PRJ／GOV 无 extra。PRJ 的 `applicability.delivery_space` 逐条为显式勘察义务（11×2，方括弧形；不空、不伪造、不登记 N-A）→ M2 判待补属预期的诚实状态，登记 G-PRJ-1／SO-18。

**三、台账增量**。`gaps` 18→**21**：G-GRD-1（9.2.3 九信号源未收，与 DPS 9.2.5 部署观测面分工未决）、G-PRJ-1（PRJ delivery_space 待勘察）、G-GOV-1（既有 14 份 WV-*-E3-01 的 scope 均排除三 kind，E3 豁免须逐 kind 申请）。`survey_obligations` 16→**19**：SO-17／SO-18／SO-19 分别对应上述三项。`vocabulary_gaps` **8→8 不变**：本批未引入新谓词（M4 未登记 0），故不新增；`waivers` **14→14 不变**：E3 豁免属人类裁决，M3 不伪造豁免、不预支批准（见 G-GOV-1）。

**四、ST 简记**。既有简记实测为 **14** 条（ST-STY-01…ST-DPS-01，非 13），`scope` 一律 110→**130**，只追加 GRD/PRJ/GOV 二十个 id、不改既有行内注（0.22 承诺一）；新增 ST-GRD-01／ST-PRJ-01／ST-GOV-01，体例沿用「一 kind 一条」（既有台账无按批一条的先例），scope 同为 130；`status_transitions` 14→**17**，全部 scope 与实际 130 条 seed 集合逐项相等。

**五、计数与投影**。`meta.entry_count` 110→**130**；本文件 §1 计数 110→**130**；entries 130（唯一 130）、status=seed 130；事实占位符 1165→**1480**（+315）；硬检查通过 **910**／失败 **0**／软警告 **0**；指针反查 **2130**／miss **0**（method_registry 1903）；seed 资格成立 130；自检记录 1114。四件投影 `--project` 重生成：`STY.md` **1946**／`勘察义务清单.md` **2236**／`索引.md` **300**／`自检报告.md` **298**（合计 **4780**，4098→4780）；sha256 前 12 位 `c92b911980eb`／`9e45f8f0b984`／`bf908a0adbe2`／`cc620d23fdc`（按 STY／勘察／索引／自检顺序）。

**六、围栏复核**：母本 **216**（零改动）／单行本 **36**（零改动）／本文件 **2**（偶数）／`todo.md` **0**／`软件工程元框架成文法-changlog.md` 本批追加段 **0**（全文件 2 处系前序未提交段，只追加不覆盖）／`profiles.yaml` **0**／`method_registry.yaml` **0**。

**七、未做**：不 commit、不 push；E3 Waiver 未申请（待人类裁决，SO-19）；PRJ `delivery_space` 与 GRD 9.2.3 信号源分工为开放勘察项（G-PRJ-1／G-GRD-1）。本轮改动仅 `method_registry.yaml`、本文件、`todo.md`、`软件工程元框架成文法-changlog.md` 与四件投影。

### 4.17 占位符口径改造（方案 b，2026-11-04）

丙类工具改造：不改母本、不改任何条目、不改 `status`、不改 `profiles.yaml`。判定式显式化为 `FACT_PLACEHOLDER_RE`（以 `待勘察：` 开头，或整句以 `待勘察` 结尾；仅句中提及不计），`census_placeholders` 返回 `all/facts/slots` 三账，`render_survey`／`render_self_check`／CLI 改用新口径。

**旧口径（历史，不回改）**：§4.16 记 1165→**1480**（全部方括号一律计为待勘察事实）。

**新口径（本次实测）**：方括号总数 **1480 ＝ 事实占位 23 ＋ 未绑定槽 1457**。

| 字段类别 | 事实 | 槽 | 合计 |
|---|---|---|---|
| `applicability.problem_space` | 0 | 173 | 173 |
| `applicability.current_space` | 0 | 207 | 207 |
| `applicability.delivery_space` | 22 | 169 | 191 |
| `anti_patterns.detection_predicate` | 0 | 764 | 764 |
| `cost_profile` | 0 | 127 | 127 |
| `envelope.bound_expr` | 1 | 16 | 17 |
| `narrative` | 0 | 1 | 1 |
| **合计** | **23** | **1457** | **1480** |

按 kind（事实＋槽）：QAT 248／STY 166／PRJ 165（含事实 22）／CTR 115／RLP 110／VFM 102／GOV 95／DPS 73（含事实 1）／CRD 67／DFL 63／CFG 60／GRD 55／DEC 54／SCH 40／STP 36／OWN 16／CSL 15。

**不变量（本次实测）**：entries **130**、seed **130**、自检记录 **1114**、硬失败 **0**／软警告 **0**、指针 **2130**／miss **0** 全部不变；源哈希未变（`method_registry.yaml`→`13712a329e91`、`profiles.yaml`→`13f961d61ff1`、`predicate_vocabulary.yaml`→`025b999d0251`）。四件投影 `--project` 重生成：`STY.md` **1946** 行／`勘察义务清单.md` **206** 行／`索引.md` **300** 行／`自检报告.md` **372** 行；本次 sha256 前 12 位 `23f54527f1a7`／`3c853e99093b`／`8e7be57b5897`／`56b1c2472eaa`（按 STY／勘察／索引／自检顺序）。勘察清单由 2236 行降至 206 行，是把 1457 个槽移出义务清单的直接结果（事实仅 23 条）。

**遗留**：PRJ 22 项「问句式事实写入 `delivery_space` 谓词槽」仍是类型错误，处置见 `../ADR草案-PRJ交付空间-谓词槽纠正.md`（ADR-PRJ-2-01；2026-11-04 已批准并执行，见 §4.18）；问句式硬检查（方案 c）仍待裁（先需解决 schema 无事实槽的问题）。

### 4.18 PRJ 交付空间谓词槽纠正执行（ADR-PRJ-2-01 落地，2026-11-04）

按 `ADR草案-PRJ交付空间-谓词槽纠正.md`（ADR-PRJ-2-01）§8 清单执行；人类批准依据 0.13 @m:271。**母本零改动**（@m:342 原已是 `delivery_space: [谓词]`），不触发 `@行号` 锚点位移。

- **条目**：PRJ-001…PRJ-011 共 22 项处置——14 项迁入 `current_space`（陈述式现状谓词）、8 项留 `delivery_space` 改写为 `∃` 能力前提谓词；PRJ-007／009／010 各补 1 项交付能力谓词（批准材料投影／R2 材料性判定投影／验证计划投影）。11 条 `version` 1.0.0→**1.1.0**（0.17.2 @333）；`status` 仍 `seed`。
- **台账**：新增 `G-PRJ-2`（`delivery_space` 类型误用，closed）；`SO-18` 的 `gap_ref` 改指 `G-PRJ-2` 并置 `closed`（obligation 原文逐字保留）；新增 `SO-20`（执行义务，已执行 closed）。既有记录零改写。
- **新口径实测**：方括号总数 **1483 ＝ 事实 1 ＋ 槽 1482**，与 ADR §6 估算一致。按字段：problem 173／current **221**（+14）／delivery **180**（−11，22 项事实退出，11 项能力谓词入账）／detection 764／cost 127／bound 17／narrative 1。PRJ 侧 applicability `待勘察` 残留 **0**、`delivery_space` 问句（`是否`／`？`）残留 **0**（11 项全部以 `∃` 开头）；剩余 11 处 `是否` 系 problem_space 的问题名与 current_space 的「问题」取值，属合法问题陈述。
- **不变量**：entries **130**／seed **130**／`meta.entry_count` **130**；自检记录 **1114**、硬失败 **0**／软警告 **0**、指针 **2130**／miss **0**；`profiles.yaml`、`predicate_vocabulary.yaml` 未动（新文本无 ASCII 调用式，M4 无需扩词）。
- **四件投影（同一次 `--project`）**：`STY.md` **1946** 行／`勘察义务清单.md` **130** 行／`索引.md` **302** 行／`自检报告.md` **350** 行；sha256 前 12 位 `5433b7e5566f`／`fcb767a5660b`／`8128989f3080`／`e529841f995b`（按 STY／勘察／索引／自检顺序）。

### 4.19 台账承接归一（2026-11-04）

现状清点后的最小整理：**只为既有无承接的 open gap 补登记勘察义务，不改任何 gap 原文、不改条目、不改剖面**。

- 剖面：0.17.3 枚举 17 个 kind **全部 `seed`**，`undecided_fields` 全 0；`entry_level_exemptions` 仅 STY／GRD／PRJ／GOV 各 1 条。无缺失剖面。
- 承接：21 个 open gap 中，20 个有 open SO 承接（`SO-3` 同时覆盖 `G-STY-3`／`G-STY-5`）；唯一悬空者为 **`G-PRJ-1`**——ADR-PRJ-2-01 指定其作为「曾把类型错误误判为数据缺口」的历史记录保留 open，**不补 SO、不改写**。
- 新增 **`SO-21`（G-STY-2）／`SO-22`（G-OWN-1）／`SO-23`（G-CSL-1）**，均为 `open`，义务面分别是 1.4 风格实例措辞、4.2.1 三行行级书目、4.2.3 行级出处裁决；三条 route 均须 R2／ADR 或人类裁决，本批不预支结论。
- 不变量：entries／seed／`meta.entry_count` **130**；自检记录 **1114**、硬失败 **0**／软警告 **0**、指针 **2130**／miss **0**；新口径 **1483＝事实 1＋槽 1482**。
- 四件投影（同一次 `--project`）：`STY.md` **1946**／`勘察义务清单.md` **133**／`索引.md` **305**／`自检报告.md` **350**；sha256 前 12 位 `512bac30e1e2`／`225936646e9d`／`127e9818afd3`／`b6361cea330c`。
- 边界：母本、`profiles.yaml`、`predicate_vocabulary.yaml` 零改动；条目 `version` 不变（未改条目内容）。

### 4.20 gap↔SO 完整性检查与 G-PRJ-1 留痕 ADR（2026-11-04）

- **`GAP-SO` 信息级检查**（`project.py` `check_gap_so_integrity`）：校验 open gap 是否有 open SO、SO 的 `gap_ref` 是否指向存在 gap、open SO 是否指向 closed gap。实测：open gaps **21**｜有 open SO 承接 **20**｜白名单悬空 **1**（`G-PRJ-1`，理由引用 ADR-PRJ-2-01 §5.2）｜无承接 **0**｜SO **23**｜坏引用 **0**。该检查**不参与 seed 资格、不作硬失败**；`gap_ref` 中的 `VG-*`／README 等交叉引用不计坏引用（实测 3 处）。自检记录 1114→**1116**（+2：白名单 1＋汇总 1）。
- **G-PRJ-1 留痕 ADR**：新增 `ADR草案-G-PRJ-1-悬空保留.md`（ADR-G-PRJ-1-01，草案）：保留理由、呈现规则（不补 SO／不关闭）、关闭条件与新 ADR 授权路径。**不改台账**。
- **G-OWN-1／G-CSL-1 扩母本：阻塞（未执行）**。测算：插入点 4.2.1 表后（@2171）与 4.2.3 表后（@2194），计划 delta **+4** 行；其后受影响锚点 **8,367** 处（method_registry **7,397**，其中 YAML 字符串值内 **4,896**；profiles **38**／README **185**／changelog **747**）。阻塞原因是**引用目标混合**：同一文件内既有指向母本的 `@2789`，也有指向 `method_registry` 自身的 `@7272-7275`，还有指向 `profiles.yaml` 的 `@407-410`／`@435-438`——纯偏移脚本无法判定目标，会改错自引用。按用户指令“重映射不可行即停”，**母本 0 行改动、锚点 0 处重写**；解除需先建立“锚点目标显式化”（例如 `@mother:`／`@registry:` 前缀）或人工逐条分类，二者均须 R2／ADR。
- 不变量：entries／seed／`meta.entry_count` **130**；自检记录 **1116**、硬失败 **0**／软警告 **0**、指针 **2130**／miss **0**；占位符 **1483＝事实 1＋槽 1482**。
- 四件投影（同一次 `--project`）：`STY.md` **1946**／`勘察义务清单.md` **133**／`索引.md` **305**／`自检报告.md` **350**；sha256 前 12 位 `e73259c1f70f`／`d2c646ec8104`／`ad2166e912b5`／`837e7ebc8e17`。

### 4.21 G-OWN-1／G-CSL-1 行内出处补写（2026-11-04）

- 母本 **8 行内追加**，零插行：4.2.1 @2168／@2169 →「行级出处：书目 35」，@2171 → 书目 39；4.2.3 @2188／@2189／@2190 →「出处：书目 35」，@2191 → 书目 39，@2192 → 书目 36。
- 母本总行数 **4427→4427 不变**；`git diff` **8 增／8 删**，全为同行单元格追加；`@行号` 位移 **0**；4.7 零改动；@2170（数据产品）未动。
- 条目、`profiles.yaml`、`predicate_vocabulary.yaml` 零改动；条目 `version` 不变。
- 不变量：entries／seed／`meta.entry_count` **130**；自检记录 **1116**、硬检查通过 **910**／失败 **0**／软警告 **0**；指针 **2130**／miss **0**；占位符 **1483＝事实 1＋槽 1482**；M6 逐条全过。
- 四件投影（同一次 `--project`）：`STY.md` **1946**／`勘察义务清单.md` **133**／`索引.md` **305**／`自检报告.md` **350**；sha256 前 12 位 `713a27ae693b`／`4a0e743fb13a`／`804a98517bb2`／`6af78282e60f`。
- ADR：[ADR草案-G-OWN-CSL-行内出处.md](ADR草案-G-OWN-CSL-行内出处.md)（ADR-G-OWN-CSL-01，草案；方向已批、落盘后执行）。
- 边界：本批只改母本；`G-OWN-1`／`G-CSL-1` 的收口与 @2170 补 41 见 §4.22；`G-STY-5` 仍未动。

### 4.22 1.4 表职责边界裁定（方案 B）与台账收口（2026-11-04）

**裁定（人类 2026-11-04 方案 B）**：1.4 表只定**方面级 obligation**（每个方面该问什么）；风格实例措辞的权威面在 **STY 条目的 `constraints_imposed`／`compatibility`**。1.4 不是风格注册表，不承担逐风格实例措辞。

- **新增风格只加 STY 条目**，不改 1.4、不插行、不触发 0.13 的母本变更路径；条目仍按既有 seed 流程登记。
- **为何不选 A**：A 需在 1.4 补约 10 风格×7 方面 ≈ 70 格，并让 24 条 STY 条目的约 48–100 字段回指表单元格（全部 `minor+1` 并重过 M2／M3）；现有 schema 无“表单元格引用”字段，还需先 R2。B 为零返工、零插行、零锚点位移。
- **`G-STY-2` 收口判据**：文档指向问题，非母本缺实例；`basis` 引本裁定与 1.4／STY 现状。`SO-21` 同步置 closed。
- **`G-STY-5` 保持 open**：其范围是 1.2.4 元方法在书目 2 的行级覆盖（STY-021／024），**不是 4.2.3 五行**；本次 4.2.3 补出处不覆盖它，不为凑数关闭。
- **同批收口**：`G-OWN-1`（4.2.1 @2168／@2169／@2171）与 `G-CSL-1`（4.2.3 @2188–@2192）按 ADR-G-OWN-CSL-01 置 closed；@2170 补书目 41 见该 ADR §9 追加授权。gap 原文均逐字保留。
- **台账实测**：open gap **21→18**（关闭 G-STY-2／G-OWN-1／G-CSL-1；G-STY-5 仍 open）；open SO **21→18**（SO-21／22／23 关闭）；`G-PRJ-1` 仍为唯一白名单历史悬空。

### 4.23 接地编译前两闸裁定（2026-11-04）

**一、`G-STY-1` 职责边界**

1. 1.2.1–1.2.4 的「适用条件」列只承担**问题空间条件**；现状空间（棕地／在役系统／既有中间件与平台）与交付空间（团队规模与能力、运维能力）条件属**部署事实**。
2. 部署事实由接地编译期在 STY 条目的 `applicability.current_space`／`delivery_space` 填写。
3. `[]` 的语义固定为「**该部署尚未勘察**」，**不得**读作「该维不适用」（unknown ≠ false，0.18.6 M15）。
4. 过滤偏宽由接地编译期填报解决；母本 **0 行改动**，不以「母本已补」结案。`SO-1` 保持 open，作为部署期勘察义务。

**二、`G-ENV-1` 定性要点 → 指标族映射**

| 1.2.x 包络要点 | 映射族 | 落点 |
|---|---|---|
| 可测试性↑↑ | 可修改性 | 核心可脱离适配器单测的变更成本 |
| 可重用性↑ | 可修改性 | 跨上下文复用所需的契约变更成本 |
| 可扩展性↑↑ | 可修改性 | 新增单元的触达面与前置时间 |
| 带宽↓ | 性能 | 资源占用 |
| 一致性管理复杂度↑ | 不入 metric | 记 `cost_profile.consistency_impact` |

约束：

1. **不扩 6.2.1 封闭词汇**，不新增 `envelope.metric` 名；`predicate_vocabulary.yaml` 零改动。
2. 未覆盖项（灵活性↑／可预测性↓／可调试性↓／互操作性↑ 等）按语义最相近族逐条行内注记映射理由；无对应族者显式归 `cost_profile`，不得静默近似。
3. 全部映射为人工判断；不得读作母本已登记该指标族。

### 4.24 `G-QAT-1` 三族显式缺口（路 B，2026-11-04）

1. 6.2.1 七族中的**可伸缩性**（@2786）、**合规**（@2788）、**可观测性**（@2789）在 6.2.5 **不设常备战术**；本裁定**不给 6.2.5 补行**。
2. 操作口径：当上述三族中出现 `priority = high` 的目标时，按 `CH-B`（不决定）**登记显式缺口**——Q6 目标-手段闭合对该三族恒不成立，缺口登记后由 6.5 `goal(...)` 与 CH-B 处置流程承接。
3. 不得因缺口而本地发明战术（@2829 禁令、0.17.1 零新增规范命题）；不得以「目标只是愿望」静默跳过。
4. 15 项既有战术已逐条可引用：`[Q-01]`…`[Q-15]`（@2831–@2834），QAT-001…015 各带 `row_id 6.2.5-Q-01…15`。

### 4.25 SRC kind 登记与 9.2.3 九信号源接线（ADR-SRC-01／R2-SRC-01，2026-11-06）

1. **母本（阶段 3 已落盘）**：0.17.3 kind 表新增 `| SRC | 漂移/腐化信号源 | 方面 9 · 9.2.3 |`（插行后现行第 405 行）；9.2.3 表后新增导航注记 `> 表内非部署八项另立 SRC 条目登记；部署三项（部署失败率／回滚率／变更前置时间）归 DPS。`（插行后现行第 3624 行）。母本 4,427→**4,429** 行，`git diff --numstat` **2/0**；仅 I-A／I-B 两行，I-D（0.18.4 加行）不执行。
2. **行号口径**：插行后 9.2.3 表数据行为 **3615–3622**（8 行非部署）＋**3623**（1 行部署、行内含 3 指标）；`kind_profile_SRC.seed_source.table_rows` 已按插行后行号登记。ADR §2.1 的 3613–3621 为插行前 as-of 记录，已加插行注记、不改写原表。
3. **剖面**：`profiles.yaml` 新增 `kind_profile_SRC`（`status: seed`）：`not_applicable` 8 项＝`envelope`＋7 个 `cost_profile.*`（逐项 `reason`＋`provenance`）；`compatibility`／`constraints_imposed`／`applicability` 照常必填；`undecided_fields: []`；`entry_level_exemptions` 1 条 C-ENV（scope＝SRC 全批）。
4. **0.18.2 S1 排除**：SRC 是信号源登记面、不是可选方法，`kind=SRC` 不进入 S1 候选集；该规则登记于 `kind_profile_SRC.selection_profile.variant`。本目录的 `project.py` 不实现 S1 候选装配（无对应代码面），故本轮无代码改动；外部选型执行器消费本剖面时须按此排除。
5. **0.18.4**：`R1.5` 裁定不加行（SRC 不参与选型），方面表保持现状；若未来参与选型须另案重裁并另测插行。
6. **G-GRD-1／SO-17**：按四数对齐结论追加 `note`（原文逐字不改）——9 个表数据行＝8 行非部署＋1 行部署（含 3 指标）；非部署八项由 SRC 承载（编号待发布），部署三指标归 DPS。两笔保持 `open`，直至 8 条 SRC 编号发布并入册。
7. **冻结快照**：仅追加 1 行订正注记（「其余六项」→ 8 项），不改写历史文字；`G-GRD-1`／`SO-17` 仍在冻结面，规划完成 ≠ 解冻。
8. **待发布**：`SRC-001…008` 八条条目不写入 `method_registry.yaml`，编号待用户确认后一次性发布；编号一经落册不可复用／重排（0.22）。
9. **不变量**：entries **130**（未新增）；`--check` **1,124** 条记录／硬通过 **916**／硬失败 **0**／软警告 **0**；指针 **2,180**／miss **0**；占位符 **1,483＝事实 1＋槽 1,482**；四件投影同源重生成。

### 4.26 signals 字段落盘与 SRC-001…008 发布（ADR-SRC-02，2026-11-06）

1. **母本**：0.17.2 `registry_entry` 块内插入 `signals` 定义 1 行（第 364 行 `]` 后、`formal_anchor` 前）——**写法 I**（块内定义），使正式形状与 M2 校验面同一约定。母本 **4,429→4,430** 行，`git diff --numstat` **1/0**。否决零插行：块外定义会造成正式形状与 M2 校验面两处约定不一致，与 `delivery_space` 旧病同源。
2. **位移与清债（同批完成）**：动锚 **6,839**、区间锚 **993**、端点 **7,832**；例外 **0**、撞串补前缀 **0**、`prefix_unresolved=0`。插行引入的 **7 条 `needs_review` 已清零**：1 条 `@322-381` 区间锚改条款锚 `@m:0.17.2`，6 条空行锚改文字引用（不以「下一行」等相对表述留债）。F-2～F-8 全 pass；F-1 为现状度量（**8,814**，非失败）。
3. **M2 增量 S-1～S-9**：S-1 数组非空／项对象／键集、S-2 六键必现及五键非空、S-3 `signal_id={eid}-S{i+1}`、S-4 `name`／`detection_predicate` 非空且禁方括号、S-5 `severity` 闭集、S-6 `severity_condition` 恰两键且 `raise_to` 严格高于基级（P0 必须 null）、S-7 `consumption` 非空且键集／`action` 闭集、S-8 `gate` 仅 `re_review`＋`R2`（`re_review` 缺 gate 失败）——S-1～S-8 **hard**；S-9 `note` 缺失／空串 **info**。`detection_predicate` **不走 M4**，只做 S-4 非空校验，禁方括号占位（方括号会虚增槽数并误触发 M15 事实口径）。
4. **剖面**：`signals` 进 `common_required`（source 0.17.2）；**17 个非 SRC kind** 逐条 `not_applicable`（`reason`＋`provenance.origin=compiled`＋source 0.17.2）；`kind_profile_SRC` 走 `required_extra: [signals]` 必填。风险：若审阅要求逐句反证，17 条 uniform reason 将变成 17 条独立论证（工作量按 ADR §9 高档）。
5. **8 条 SRC**：`SRC-001…SRC-008` 严格按 0.22 分块序发布（不复用／不重排），14 个子信号逐条进 `signals`（001×2／002×1／003×2／004×2／005×2／006×1／007×3／008×1）；5 条 `severity_condition`；`SRC-006` 的 `re_review` 带 `gate: R2`；`name` 逐字取母本子信号名。第 9 数据行（部署失败率／回滚率／变更前置时间 3 指标）归 DPS，不立 SRC（9＝8＋1）。
6. **台账**：新增 `G-SRC-1`（SRC 谓词词汇未登记，open；后续逐条登记进 `predicate_vocabulary.yaml` 走 R2，登记后另开 ADR 扩 M4）；`G-GRD-1`／`SO-17` 置 closed 并写 closure／evidence（statement／impact／route 逐字保留；既有 `note` 不改写）。`ST-SRC-01` 新增（draft→seed，scope 与全部 138 条 seed 条目一致）。
7. **不变量（前后对比）**：entries **130→138**；`meta.entry_count` **130→138**；kind 计数 **17→18**（17 个既有 kind 不变，SRC 新增 8 条）；`--check` 记录 **1,124→1,199**（+8 条 SRC 记录＋gap／简记记录）；硬通过 **916→965**／硬失败 **0→0**／软警告 **0**；指针 **2,180→2,244**／miss **0**；占位符 **1,483＝事实 1＋槽 1,482（不变）**——SRC 的 `detection_predicate`／`when_predicate` 全无方括号，证明本批未虚增槽；`needs_review` **0**；母本 **4,429→4,430**。
8. **投影四件（同一次 `--project`）**：`STY.md` **2,012** 行／`勘察义务清单.md` **133**／`索引.md` **316**／`自检报告.md` **361**；sha256 前 12 位 `68327ab9b54e`／`738d09dd5352`／`3acb1eaba746`／`09e8741faf67`。
9. **口径**：`signals` 的可执行性**不宣称**——`G-SRC-1` 未关闭前，`detection_predicate` 只是非空文本（M4 不覆盖）。`severity` 与 `consumption` 无交叉校验（母本无对应表，不本地加规则）。

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

投影产物：`projections/STY.md`（条目人类可读视图，含四层数据源标注）、`projections/自检报告.md`（含「占位符口径」新分解）、`projections/勘察义务清单.md`（事实占位逐条＋槽汇总）、`projections/索引.md`。

## 7. 变更纪律

- 条目**机器层字段**任何变更 = 完整 ADR + 批准（0.17.4 消费者四 / 0.13 注册表类目）；
- `narrative` 变更 = 低影响（简记级），受 M5 抽查；
- `status` 迁移权限见 0.17.5；
- kind 剖面变更走 0.13；新增 kind = 高影响（枚举封闭，0.17.3）；
- 表格与条目冲突时**以条目为准**，冲突登记为成文法缺陷（FM-12 通道，0.17.1）。
