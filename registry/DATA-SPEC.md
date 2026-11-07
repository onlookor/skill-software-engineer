# 注册表数据侧规范（DATA-SPEC）

| 项 | 值 |
|---|---|
| 性质 | **本目录数据契约的唯一规约面**；`registry/README.md` 为下游导览（说明用，不承担规约） |
| 权威来源 | 母本 0.17.2（条目 schema）、0.17.3（kind 封闭枚举）、0.17.4（消费者）、0.12（参考文献治理）、0.13（注册表治理）、编译规范 2.1／2.3（键名与谓词语法） |
| 日期 | 2026-11-07 |
| 范围 | 文件角色、条目 schema、键名映射、字段语义、枚举、谓词书写、编号与批次先例、来源标注 |
| 不在本文 | 检查项、级别、量词、执行顺序、台账登记与变更审批 → [`CHECK-SPEC.md`](CHECK-SPEC.md) |
| 迁移对照 | 原 README 位置与新位置逐条见 [`CHECK-SPEC.md`](CHECK-SPEC.md) 附录 A（43 条全表） |

本文只把母本既有义务落到数据面，**不新增母本义务**；凡与母本冲突，以母本为准。原 README 中无母本明文依据的执行性细化，在此首次确立为子目录规约（附录 A「性质」列标「新立」）。

## D1 权威与文件角色

- **D1.1 机器层权威**：本目录是方法注册表的机器层权威源（母本 0.17）；母本各方面 x.2 的方法空间表格是**种子数据源视图**，不是决策权威（0.17.1）。选型只消费条目（0.18 S1），守护只消费 `anti_patterns`／`compatibility`（0.17.4 消费者二），编译以条目为编译单元（编译规范 2.4）。〔母本派生〕
- **D1.2 目录布局变更**：新增文件／子目录属 0.13 制度性决定（简记级），登记于母本 changelog、母本「配套文件说明」表、`AGENTS.MD` 与本仓变更记录；不得以新建文件本身替代登记。〔母本派生 0.13〕
- **D1.3 文件角色表**：

| 文件 | 角色 | 权威关系 |
|---|---|---|
| `profiles.yaml` | 18 个 kind 的字段剖面（元注册条目）＋剖面级缺口台账 | 数据侧权威；剖面变更走 0.13 |
| `predicate_vocabulary.yaml` | 母本机器层谓词清单的数据侧投影 | **非权威**：权威在母本 x.5／0.17.8／0.18.6／0.20.4／0.21.6／10.5；每条带 clause 指针，须可反查母本 |
| `method_registry.yaml` | 条目本体＋缺口台账＋状态迁移简记＋Waiver＋人工判断登记 | 数据侧权威；schema 逐字采用 0.17.2 |
| `scripts/project.py` | 自检与同源投影工具 | 工具，不含规范命题 |
| `projections/*.md` | 人类可读投影与自检报告 | **生成物**；只可重跑生成，不可手改 |

〔D1.3 中 profiles／predicate_vocabulary／method_registry 为母本派生；投影禁手改为母本 0.9／编译规范 E2 派生〕

## D2 条目 schema 与键名映射

- **D2.1 逐字采用**：条目 schema = 母本 0.17.2 **逐字采用**，不重定义、不扩展、不裁剪（编译规范 2.4）。〔母本派生〕
- **D2.2 键名映射**：YAML 侧仅做键名书写映射，语义零变更：

| 0.17.2 / 编译规范 2.1 | 本目录 YAML 键 |
|---|---|
| `provenance = {origin, 源指针}` | `provenance: {origin, source_pointers: [source_ref]}` |
| `source_ref = {source_type ∈ {clause_id, bib_id, row_id}, value, 核验状态}` | `{source_type, value, verified}` |
| `version`（语义版本 `{major, minor, patch}`） | `version: {major, minor, patch}` |
| `row_id`（表格行 ID） | `"{表号}-{行名}"`，如 `1.2.1-分层` |

〔母本派生〕
- **D2.3 字段封闭与顶层节**：条目内**不得出现 0.17.2 之外的字段**。注册表级信息（缺口、状态迁移简记、Waiver、人工判断登记、未闭合的冲突矩阵行）一律置于 `method_registry.yaml` 的**顶层节**，不进入条目。〔母本派生〕
- **D2.4 状态迁移简记 schema**：`status_transitions` 每条固定九字段 `transition_id`／`from`／`to`／`scope`／`date`／`condition`／`evidence`／`impact_level`／`provenance`，可选 `note`。`from`／`to` ∈ {`draft`,`seed`,`active`,`deprecated`,`retired`}。**撤回型 `seed→draft`（ADR-LC-01 §3.6）另需四字段**：
  - `seed_rejudication_ref`：重判批次号，指向同次重判的 `seed_rejudication` 差异记录；
  - `consumption_checked`：布尔，`true` 表示已查存量消费；
  - `affected_decisions`：已被消费的决策 ADR／编译产物清单，查过且无为 `[]`；
  - `disposition` ∈ {`revalidate`,`replace`,`retain-annotated`}：对已消费条目的处置。
  且 `impact_level` 必须为「高」（与 `active→deprecated` 同构）。`draft→seed` 的 `impact_level` 维持「低」。缺项由 `check_ledgers` 判硬失败（`CHECK-SPEC` C4.7）。〔ADR-LC-01 §3.2／§3.6〕

## D3 谓词书写约定（M4／M15 的校验对象）

- **D3.1 词汇封闭**：`applicability` 三空间谓词与 `anti_patterns.detection_predicate` 只能使用 `predicate_vocabulary.yaml` 登记的谓词名（编译规范 2.3「谓词名注册」）；缺失词汇 → R2 提议，**不得本地造词**；同时登记为 `gaps`。〔母本派生 0.17.8 M4／编译规范 2.3〕
- **D3.2 语法**：联接 `∧`、析取 `∨`、否定 `¬`、蕴含 `→`、量化 `∀`／`∃` 前置、通配 `·`（编译规范 2.3 BNF）。〔母本派生〕
- **D3.3 谓词槽与事实占位**：方括号 `[…]` 表示**谓词／参数槽**——`applicability` 三空间与 `detection_predicate` 是谓词，`cost_profile`／`envelope.bound_expr` 是参数；它们在决策期求值，**不计事实债**。待勘察事实必须带显式标记：以 `待勘察：` 开头，或整句以 `待勘察` 结尾；仅句中提及不计。`[已核验]`／`[存疑]`／`[未核验]`／`[待核验]` 按 0.12 是可信度标注，单列统计。事实占位求值 `unknown` 时按 M15：候选保留＋勘察义务登记，**禁沉默排除**（0.18.6）。旧口径（全部方括号计事实占位）按 §4.17 迁移记录不回改。〔2026-11-04 新口径，本轮确立为规约〕
- **D3.4 公式约定词**：`approved`／`declared`／`registered`／`sourced`／`compatible`／`has`／`now` 按编译规范 2.3 内建语义表使用，不算白板谓词。〔母本派生〕
- **D3.5 三值语义**：`{true, false, unknown}`；两值实现 = 编译缺陷（编译规范 2.3(3)）。〔母本派生〕

## D4 编号与批次先例（数据面）

- **D4.1 编号不复用**：编号一经发布永不复用、不重排（0.22 承诺一）；README §4 的历史裁决先例在本规范继续有效。
- **D4.2 STY 分块序**：母本反例 18-A 已引用 `STY-04`，故 STY 批按**分块序**编号，`provenance.origin=manual`。〔先例，承接 README §4.1〕
- **D4.3 DEC／OWN／CSL／CRD 解耦**：四批已按 2026-09-20 人类裁决完成既有引用解耦（判断见 `method_registry.yaml` MJ-13／14／15），编号按裁决后的表序。〔先例，§4.2〕
- **D4.4 无已发布数字引用批**：CTR／STP／DFL／RLP／SCH／CFG 六批经全文勘察，母本无 `KIND-数字` 形态已发布引用；按表序／清单序入库，无需 R2 改母本。〔先例，§4.3–4.8〕
- **D4.5 QAT／VFM／DPS 粒度**：QAT 按「15 条战术」、VFM 按「6 类手段」、DPS 按表序入库；粒度裁决与缺口（`G-VFM-1`）登记于 MJ 与批次记录，不得按属性／子项二次拆分。〔先例，§4.9–4.11〕
- **D4.6 GRD／PRJ／GOV 粒度**：GRD 按 9.2.1 表行序 3 条；PRJ 按 10.2.2 义务表＋评审点一–五 11 条（C4／arc42 实例表不作种子）；GOV 按 0.5 表六类 6 条，块头登记五字段格式约束。20 条均 `status: seed`，编号逐字取表首列。〔先例，§4.16〕

## D5 来源与出处标注

- **D5.1 出处门槛**：`source_pointers` 的 `source_type ∈ {clause_id, bib_id, row_id}`；`clause_id` 须可反查母本；`bib_id` 须指向参考文献已著录条目；`row_id` 形如 `"{表号}-{行名}"`。参考文献须同时声明 `compile_usage` 与 `trust_grade`（0.12）。〔母本派生 0.17.2／0.12〕
- **D5.2 出处类别**：`provenance` 增可选键 `source_class`；值域、`manual` 两类现状的区分、与 `origin` 的分工及判定程序全部见 [`../adr/ADR-STY-FIM-01-approved-20261107-框架内生元方法与source_class.md`](../adr/ADR-STY-FIM-01-approved-20261107-框架内生元方法与source_class.md) §5.5（本规范只做指引，不复述规则）。当前「未分类」条数见 `projections/自检报告.md` 汇总行。〔本轮新立（承接 README §4.31）〕
- **D5.3 部分指针**：来源只覆盖条目的部分面时，`references` 须以「限…；不覆盖…」显式登记覆盖边界；未覆盖面继续由对应缺口承接。〔先例，§4.30〕

## D6 数据侧变更口径

- **D6.1** 条目机器层字段任何变更 = 完整 ADR＋批准（0.17.4 消费者四／0.13 注册表类目）。〔母本派生〕
- **D6.2** `narrative` 变更 = 低影响（简记级），受 M5 抽查。〔母本派生〕
- **D6.3** `status` 迁移权限见 0.17.5。〔母本派生〕
- **D6.4** kind 剖面变更走 0.13；新增 kind = 高影响（枚举封闭，0.17.3）。〔母本派生〕
- **D6.5** 表格与条目冲突时**以条目为准**，冲突登记为成文法缺陷（FM-12 通道，0.17.1）。〔母本派生〕

## 附录 A：本规范承接的迁移条目（20 条）

逐条的原 README 行号、摘要、性质与去向见 [`CHECK-SPEC.md`](CHECK-SPEC.md) 附录 A 第 1–20 行；本附录不重复。
