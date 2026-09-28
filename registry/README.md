# 方法注册表（registry/）

本目录是**方法注册表的机器层权威源**（母本 0.17）与其同源投影。母本各方面 x.2 的方法空间表格是**种子数据源视图**，不是决策权威（0.17.1）；权威在本目录的条目。选型只消费条目（0.18 S1），守护只消费条目的 `anti_patterns`/`compatibility`（0.17.4 消费者二），编译以条目为编译单元（编译规范 2.4）。

目录布局的新增属 0.13 制度性决定（简记级），已登记于母本 changelog、母本"配套文件说明"表、AGENTS.MD 与本仓 README。

## 1. 文件清单

| 文件 | 职责 | 权威关系 |
|---|---|---|
| `profiles.yaml` | 17 个 kind 的字段剖面（元注册条目，0.17.2「字段完备性按 kind 剖面」、0.17.8 `kind_profile(kind, required_fields, optional_fields)`）＋剖面级缺口台账（KP-G1…G4，R2 澄清候选） | 数据侧权威；剖面变更走 0.13 |
| `predicate_vocabulary.yaml` | 母本机器层谓词清单的**数据侧投影**（供 M4 词汇封闭校验） | **非权威**：权威在母本 x.5／0.17.8／0.18.6／0.20.4／0.21.6／10.5；本文件每条带 clause 指针，`project.py` 反向核验指针在母本中可查 |
| `method_registry.yaml` | 方法条目本体（当前批次：STY 24 条＋OWN 4 条＋CSL 5 条＋CRD 8 条＋DEC 8 条＋CTR 12 条＋STP 4 条＋DFL 5 条，共 70 条）＋缺口台账＋状态迁移简记＋Waiver＋人工判断登记 | 数据侧权威（条目 schema 逐字采用 0.17.2） |
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

行级书目登记面：母本 4.7（@2427-2437）九项中**行级**可引者仅书目 42（→ DFL-001 发件箱）与 43（→ DFL-002 CDC），覆盖 5 行中 2 行，故 DFL-003／DFL-004／DFL-005 的 `references` 为**空列表**（M6 平凡通过，非豁免）；缺口登记 `G-DFL-1`（含五个下探裁决口①-⑤，其一为书目 44 本地 EPUB 的 isbn13 与母本 @2750 著录形态不一致的处置）＋勘察义务 `SO-11`。E3 豁免 `WV-DFL-E3-01`（硬性质面 **3 项 6 实例**：Z2 3／Y2 2／Y1 1；软性质 Y4 5 实例＋Y7 1 实例**明列排除**）已于 **2026-09-28** 登记申请、`status: pending` **待人工裁决**——批准是人的裁决（0.10 第一条／1.1 纪律二），Agent 与工具不自行批准；DFL 五条的 seed 资格**不以该 Waiver 为前提**（C-ST 只查硬检查，批准延迟不阻断本批入库）。前七项 Waiver 全部 active，与本项合计覆盖 **70** 条 seed、scope 互不重叠。§4.2／§4.3／§4.4 末段的批次清单（含 DFL）同样**不回改**；其余 9 kind（RLP/SCH/CFG/QAT/VFM/GRD/DPS/PRJ/GOV）仍适用同一模式。

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
