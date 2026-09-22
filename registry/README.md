# 方法注册表（registry/）

本目录是**方法注册表的机器层权威源**（母本 0.17）与其同源投影。母本各方面 x.2 的方法空间表格是**种子数据源视图**，不是决策权威（0.17.1）；权威在本目录的条目。选型只消费条目（0.18 S1），守护只消费条目的 `anti_patterns`/`compatibility`（0.17.4 消费者二），编译以条目为编译单元（编译规范 2.4）。

目录布局的新增属 0.13 制度性决定（简记级），已登记于母本 changelog、母本"配套文件说明"表、AGENTS.MD 与本仓 README。

## 1. 文件清单

| 文件 | 职责 | 权威关系 |
|---|---|---|
| `profiles.yaml` | 17 个 kind 的字段剖面（元注册条目，0.17.2「字段完备性按 kind 剖面」、0.17.8 `kind_profile(kind, required_fields, optional_fields)`）＋剖面级缺口台账（KP-G1…G4，R2 澄清候选） | 数据侧权威；剖面变更走 0.13 |
| `predicate_vocabulary.yaml` | 母本机器层谓词清单的**数据侧投影**（供 M4 词汇封闭校验） | **非权威**：权威在母本 x.5／0.17.8／0.18.6／0.20.4／0.21.6／10.5；本文件每条带 clause 指针，`project.py` 反向核验指针在母本中可查 |
| `method_registry.yaml` | 方法条目本体（当前批次：STY 24 条＋OWN 4 条，共 28 条）＋缺口台账＋状态迁移简记＋Waiver＋人工判断登记 | 数据侧权威（条目 schema 逐字采用 0.17.2） |
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
