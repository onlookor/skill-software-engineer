# 注册表自检与台账规范（CHECK-SPEC）

| 项 | 值 |
|---|---|
| 性质 | **本目录检查矩阵与台账登记的唯一规约面**；`registry/README.md` 为下游导览（说明用，不承担规约） |
| 权威来源 | 母本 0.17.5（生命周期与迁移权限）、0.17.7（准入六项）、0.17.8（M 系列检查式与级别）、0.17.3（kind 枚举）、9.2.1／9.2.2（严重级别与 Waiver）、0.13（注册表治理）、0.18.6（M15） |
| 日期 | 2026-11-07 |
| 范围 | 检查项、级别、量词、执行顺序、退出码、台账登记、批次先例、变更审批 |
| 不在本文 | 文件角色、schema、键名映射、谓词书写与来源标注 → [`DATA-SPEC.md`](DATA-SPEC.md) |
| 实现 | `scripts/project.py`；本文是判据文本面，代码是执行面，二者冲突以本文＋母本为准并即时修码 |

本文只把母本既有义务可执行化，**不新增母本义务、不改变检查级别与适用范围**；凡与母本冲突，以母本为准。原 README 中无母本明文依据的执行性细化，在此首次确立为子目录规约（附录 A「性质」列标「新立」）。

## C1 检查矩阵

检查项与级别如下（`seed` 资格只取硬项；逐项编号见左列，表下为来源）：

| 检查 | 内容 | 级别 | 量词／范围 |
|---|---|---|---|
| M2 | 按 kind 剖面必填字段在案；所属 kind 剖面 `status=draft` 时完备性不可判定 → M2 不成立（KP-G3） | 硬 | `∀E(status ≠ draft)` |
| M3 | 每个 envelope 项 `bound_expr` 参数化 ∧ `source` 过 0.4 出处门槛（`clause_id` 反查母本可查） | 硬 | 逐 envelope 项 |
| M4 | `detection_predicate` 词汇封闭（DATA-SPEC D3.1）＝可执行 | 硬 | 逐 `detection_predicate` |
| M5 | narrative_sync：决策性叙事已形式化或带 `clue:` 标记 | 软（P2 抽查，积累升 P1；**不阻断 seed／准入**） | 逐条目 |
| M6 | 每条 reference 声明 `compile_usage` ＋ `trust_grade`；存疑级不得为 envelope／detection 唯一出处 | 硬 | 逐 reference |
| M9 | `compatibility.peer_entry` 全部存在于本注册表 | 硬 | 逐 peer_entry |
| C-ENV | 母本 0.8「每种方法条目必须声明质量属性包络」＋0.17.2 澄清「每种方法条目」指 0.17.3 全部 kind：kind 不以质量属性为选择判据时，可在剖面把 `envelope` 登记为 `not_applicable`（逐项附 `reason` 引本条），属显式豁免而非省略。所有 kind 的条目 `envelope` 必须取值；空值须有显式登记（剖面 `not_applicable`，或 `entry_level_exemptions` 的 `field: envelope`／`check: C-ENV`／`scope`／`reason`）；无值且无登记 = 硬失败（**禁默认放行**） | 硬（阻断 seed） | 逐条目、逐 envelope 项 |
| C-KP | 元注册条目（`kind_profile_*`）的完备性判据 = 物化后的 required_fields／optional_fields 两列表在案（不受 M2 按 kind 剖面判定，避免自指循环；`profiles.yaml: gaps/KP-G2`） | 硬 | 逐元条目 |
| C-ST | 声明状态与自检资格一致：`status=seed` 必须全过硬检查；未过者必须为 `draft`（剖面 `draft` 的情形由 M2 承担）。本检查只判 seed 资格；`active`／`deprecated`／`retired` 的资格由 0.17.5／0.17.7 管辖，工具只记 info、不判失败 | 硬（仅 seed 资格） | `∀E(status=seed)` |
| C-ID | `entry_id` 唯一、格式 `{kind前缀}-{三位序号}`、kind ∈ 0.17.3 封闭枚举、无与母本既有引用冲突的重排；元条目例外：`kind_profile_{KIND}` | 硬（注册表级身份前置，失败仅阻断涉事 `entry_id`） | 全体条目 |

〔M2–M6／M9 母本派生 0.17.8；C-ENV 母本派生 0.8＋0.17.2；C-KP 母本派生 0.17.2／0.17.8；C-ST 母本派生 0.17.5／0.17.7；C-ID 母本派生 0.17.3〕

- **C1.11 seed 资格**：`seed 资格 = M2 ∧ M3 ∧ M4 ∧ M6 ∧ M9 ∧ C-ENV ∧ C-ST ∧ C-ID`（M5 为软，记警告不阻断；C-ID 按全体条目判定，失败时仅阻断涉事 `entry_id`）。生命周期与迁移权限见 0.17.5；`draft→seed` 为 bootstrap 期专用（条件 M2–M6 全过；M5 级别按 0.17.8 为软）。〔母本派生 0.17.5／0.17.7／0.17.8〕

## C2 判定语义

- **C2.1 硬／软／信息**：硬失败 → 退出码 1；软项（P2）只记警告；info 项只登记、不参与 `seed` 资格、不作硬失败。M5 是软项，**不得**提升为阻断门槛（0.17.8 为 M 系列级别权威；他处「M2–M6 全过」为摘要）。
- **C2.2 量词**：除表中已注明者，检查均为逐条目全称判定；「不可判定」不等于「通过」（M2 的 `draft` 剖面、C-ENV 的空值均按不成立处理）。
- **C2.3 三值**：`unknown` 按 M15 保留候选＋登记勘察义务，**禁沉默排除**。

## C3 执行顺序、产物与退出码

- **C3.1 工具性质**：`scripts/project.py` 是工具，不含规范命题；检查项的权威在母本与本文，工具只执行。
- **C3.2 生成物**：`projections/*.md`（`STY.md`、`自检报告.md`、`勘察义务清单.md`、`索引.md`）由工具生成，**禁手改**；变更须改 YAML 源后重跑。检查报告的锚点列由生成时点决定，不承诺跨批次稳定。
- **C3.3 用法**：

```bash
cd registry
python3 scripts/project.py --check      # 仅自检，写 projections/自检报告.md
python3 scripts/project.py --project    # 自检 + 生成人类层投影
```

退出码：`0` = 无硬检查失败；`1` = 存在硬检查失败（含指针反查失败）。

## C4 台账登记

- **C4.1 台账位置**：缺口（`gaps`）、勘察义务（`survey_obligations`）、状态迁移简记（`status_transitions`）、Waiver、人工判断登记（`manual_judgments`）一律置于 `method_registry.yaml` 顶层节，不进入条目（DATA-SPEC D2.3）。
- **C4.2 缺口与 SO**：每条 open gap 应有承接的 open SO；关闭须写 `closure` 块（`gap_ref`／`date`／`ruled_by`／`basis`／`evidence`／`preserved`），原文 `statement`／`impact`／`route` 逐字保留（0.22）。G-STY-5 以「随数据关闭」先例登记（2026-11-07）。
- **C4.3 Waiver**：按 9.2.2 五要素登记；P0 豁免仅限外部不可控并须 `external_cause` 前置；不得以 Waiver 替代整改或回退。
- **C4.4 闭合登记**：KP-G3 类闭合以 `status: open → closed` ＋同条目 `closure` 块完成；闭合不改 gap 原文。〔先例，原 README §4.15〕
- **C4.5 台账承接归一**：只为既有无承接的 open gap 补登记 SO，不改任何 gap 原文、不改条目、不改剖面。〔先例，§4.19〕
- **C4.6 gap↔SO 完整性**：`check_gap_so_integrity` 校验 open gap 是否有 open SO、SO 的 `gap_ref` 是否指向存在 gap、open SO 是否指向 closed gap；该检查为 **info 级**，不参与 seed 资格、不作硬失败；白名单悬空须有 ADR 依据（`G-PRJ-1`）。〔先例，§4.20〕
- **C4.7 状态迁移**：每条简记登记 `transition_id`／`from`／`to`／`scope`／`date`／`condition`／`evidence`／`impact_level`／`provenance`；`check_ledgers` 按时间切片＋迁入覆盖校验，合法回退不误判、未登记迁移仍硬失败。〔2026-11-07 实现〕

## C5 批次先例（检查与台账面）

- **C5.1 KP-G3 R2 澄清**：宽读闭合 `envelope`／`cost_profile` 轴；`applicability` 不纳入 N-A（另案）；PRJ 的 `applicability.delivery_space` 保持必填（诚实失败）；母本只允许 0.17.2 同行末追加一句、零插行。〔母本派生 R2，§4.12〕
- **C5.2 词汇欠账收口**：VG-06／VG-07 以「只登记、不定义、不造词」收口；在册名不变。〔新立，§4.13〕
- **C5.3 KP-G3 剖面执行**：剖面的 `not_applicable` 由 `reason` 逐项引用；`manual` 口径收窄按人类裁决执行，不改条目数据。〔新立，§4.14〕
- **C5.4 占位符三账**：判定式 `FACT_PLACEHOLDER_RE`；`all／facts／slots` 三账输出；旧口径（全部方括号计事实占位）不回改。〔新立，§4.17〕
- **C5.5 谓词槽纠正**：`delivery_space` 保持谓词槽形态；按 ADR-PRJ-2-01 §8 清单执行，母本零改动、零锚点位移。〔新立，§4.18〕
- **C5.6 行内出处补写**：G-OWN-1／G-CSL-1 以同行单元格追加完成，零插行、锚点位移 0，gap 原文保留。〔新立，§4.21〕
- **C5.7 1.4 表边界**：1.4 表只定方面级 obligation；风格实例措辞的权威面在 STY 条目 `constraints_imposed`／`compatibility`；新增风格只加 STY 条目，不改 1.4。〔新立（人类方案 B），§4.22〕
- **C5.8 G-STY-1 职责边界**：1.2.1–1.2.4「适用条件」只承担问题空间条件；现状／交付空间条件属部署事实，由接地编译期填写；`[]` = 尚未勘察，**不得**读作不适用；`SO-1` 保持 open。〔新立，§4.23 一〕
- **C5.9 G-ENV-1 指标族映射**：包络要点按最相近族映射，未覆盖项显式归 `cost_profile`，不得静默近似；不扩 6.2.1 封闭词汇，`predicate_vocabulary.yaml` 零改动。〔新立，§4.23 二〕
- **C5.10 G-QAT-1**：可伸缩性／合规／可观测性三族不设常备战术；`priority=high` 时按 CH-B 登记显式缺口，不得本地发明战术，不得静默跳过。〔新立，§4.24〕
- **C5.11 SRC kind 与 9.2.3 接线**：0.17.3 增 SRC 行；9.2.3 非部署八项立 SRC、部署三项归 DPS；行号按插行后登记。〔母本派生 ADR-SRC-01，§4.25〕
- **C5.12 signals 字段**：0.17.2 块内插入 `signals` 定义（块内写法，使正式形状与 M2 校验面一致）；插行后的锚点清债须在同批完成。〔母本派生 ADR-SRC-02，§4.26〕
- **C5.13 G-SRC-1 与 VG-09**：只登记缺口、不定义、不造词；`missing_need` 逐条列名。〔新立，§4.27〕
- **C5.14 VG-09 扩容**：母本 9.5 插行扩容；同名异义谓词改名并登记映射（`cycle`→`interaction_cycle`）。〔新立，§4.28〕
- **C5.15 R2-APPL-01**：仅 `problem_space` 触发 H1；剥离括注与破折号注释；完成态谓词抑制；主句须为疑问式。只改 2 条，其余不动。〔新立，§4.29〕
- **C5.16 部分指针与 FROZEN**：部分覆盖以「限…；不覆盖…」登记；已执行 ADR 进 FROZEN 只做快照复算。〔新立，§4.30〕

## C6 变更纪律

- **C6.1** 条目机器层字段变更 = 完整 ADR＋批准；`narrative` = 简记级；`status` 见 0.17.5；kind 剖面走 0.13、新增 kind 高影响；表格与条目冲突以条目为准（0.17.1／FM-12）。〔母本派生〕
- **C6.2** 本规范或 `DATA-SPEC.md` 的修订：检查项／级别的变更走 0.13（可能影响 seed 资格者按方案甲回溯重判）；仅措辞澄清可简记，但不得改变判据语义。

## 附录 A：README 口径迁移对照表（43 条）

计数单位：§1–§3 按语义单元；§4 按先例族（4.1、4.2 独立，4.3–4.8／4.9–4.11 各合 1，4.12–4.31 逐节）；§5 按「检查矩阵」「seed 公式」2 条；§6、§7 各 1 条。合计 **43** 条；DATA **20**、CHECK **23**；母本派生 **19**、新立 **24**。

| # | 原 README 位置 | 摘要 | 性质 | 新位置 |
|---|---|---|---|---|
| 1 | L3 | 注册表为机器层权威，x.2 表为种子视图 | 母本派生（0.17／0.17.1） | DATA-SPEC D1.1 |
| 2 | L5 | 目录布局新增属 0.13 制度性决定 | 母本派生（0.13） | DATA-SPEC D1.2 |
| 3 | L11 | profiles.yaml 为剖面权威，变更走 0.13 | 母本派生 | DATA-SPEC D1.3 |
| 4 | L12 | predicate_vocabulary 非权威、指针须反查 | 母本派生 | DATA-SPEC D1.3 |
| 5 | L13 | method_registry 为条目权威 | 母本派生 | DATA-SPEC D1.3 |
| 6 | L14 | project.py 为工具、不含规范命题 | 新立 | DATA-SPEC D1.3／CHECK-SPEC C3.1 |
| 7 | L15 | projections 为生成物、禁手改 | 母本派生（0.9） | DATA-SPEC D1.3／CHECK-SPEC C3.2 |
| 8 | L19 | schema 逐字采用 0.17.2 | 母本派生 | DATA-SPEC D2.1 |
| 9 | L21–26 | 键名映射、语义零变更 | 母本派生 | DATA-SPEC D2.2 |
| 10 | L28 | 禁 0.17.2 外字段；注册表级信息入顶层节 | 母本派生 | DATA-SPEC D2.3 |
| 11 | L32 | 谓词词汇封闭、缺词走 R2、不得造词 | 母本派生（0.17.8／编译 2.3） | DATA-SPEC D3.1 |
| 12 | L33 | 谓词语法（∧∨¬→∀∃·） | 母本派生 | DATA-SPEC D3.2 |
| 13 | L34 | 谓词槽 vs 事实占位、`待勘察` 标记、M15 | 新立（2026-11-04 口径） | DATA-SPEC D3.3／CHECK-SPEC C2.3 |
| 14 | L35 | 公式约定词 | 母本派生 | DATA-SPEC D3.4 |
| 15 | L36 | 三值语义、两值实现为缺陷 | 母本派生 | DATA-SPEC D3.5 |
| 16 | §4.1 L40–51 | STY 分块序编号先例 | 新立（承接先例） | DATA-SPEC D4.2 |
| 17 | §4.2 L53–64 | DEC／OWN／CSL／CRD 解耦先例 | 新立（承接先例） | DATA-SPEC D4.3 |
| 18 | §4.3–4.8 L66–173 | 六批无已发布数字引用、表序入库 | 新立（承接先例） | DATA-SPEC D4.4 |
| 19 | §4.9–4.11 L175–244 | QAT／VFM／DPS 粒度裁决 | 新立（承接先例） | DATA-SPEC D4.5 |
| 20 | §4.31 L498–500 | `source_class` 指引 | 新立 | DATA-SPEC D5.2 |
| 21 | §4.12 L246–254 | KP-G3 R2 宽读与授权边界 | 母本派生（R2） | CHECK-SPEC C5.1 |
| 22 | §4.13 L256–270 | VG-06／VG-07 只登记不定义 | 新立 | CHECK-SPEC C5.2 |
| 23 | §4.14 L272–282 | KP-G3 剖面执行与 `manual` 收窄 | 新立 | CHECK-SPEC C5.3 |
| 24 | §4.15 L284–313 | KP-G3 闭合登记形态 | 新立 | CHECK-SPEC C4.4 |
| 25 | §4.17 L331–354 | 占位符三账与旧口径不回改 | 新立 | CHECK-SPEC C5.4 |
| 26 | §4.18 L356–364 | PRJ `delivery_space` 谓词槽纠正 | 新立 | CHECK-SPEC C5.5 |
| 27 | §4.19 L366–375 | 台账承接归一（只补 SO） | 新立 | CHECK-SPEC C4.5 |
| 28 | §4.20 L377–383 | gap↔SO 信息级检查与白名单 | 新立 | CHECK-SPEC C4.6 |
| 29 | §4.21 L385–393 | 行内出处补写、零插行 | 新立 | CHECK-SPEC C5.6 |
| 30 | §4.22 L395–404 | 1.4 表职责边界（方案 B） | 新立（人类裁定） | CHECK-SPEC C5.7 |
| 31 | §4.23 一 L406–413 | G-STY-1 职责边界与 `[]` 语义 | 新立 | CHECK-SPEC C5.8 |
| 32 | §4.23 二 L415–429 | G-ENV-1 指标族映射约束 | 新立 | CHECK-SPEC C5.9 |
| 33 | §4.24 L431–436 | G-QAT-1 三族显式缺口 | 新立 | CHECK-SPEC C5.10 |
| 34 | §4.25 L438–448 | SRC kind 与 9.2.3 接线 | 母本派生（ADR-SRC-01） | CHECK-SPEC C5.11 |
| 35 | §4.26 L450–460 | signals 字段块内落盘 | 母本派生（ADR-SRC-02） | CHECK-SPEC C5.12 |
| 36 | §4.27 L462–468 | G-SRC-1 清点与 VG-09 登记 | 新立 | CHECK-SPEC C5.13 |
| 37 | §4.28 L470–477 | VG-09 扩容与改名 | 新立 | CHECK-SPEC C5.14 |
| 38 | §4.29 L479–487 | R2-APPL-01 判据收紧 | 新立 | CHECK-SPEC C5.15 |
| 39 | §4.30 L489–496 | 部分指针与已执行 ADR 进 FROZEN | 新立 | CHECK-SPEC C5.16／DATA-SPEC D5.3 |
| 40 | §5 L506–518 | 检查矩阵 M2–M6/M9、C-ENV/KP/ST/ID | 母本派生（0.17.8 等） | CHECK-SPEC C1 表 |
| 41 | L504、L519 | `draft→seed` 条件与 seed 资格公式 | 母本派生（0.17.5／0.17.7） | CHECK-SPEC C1.11 |
| 42 | §6 L521–529 | 执行入口、产物与退出码 | 新立 | CHECK-SPEC C3.3 |
| 43 | §7 L531–537 | 变更纪律五条 | 母本派生 | CHECK-SPEC C6.1／DATA-SPEC D6 |

统计：DATA 20（#1–20）、CHECK 23（#21–43）；母本派生 19（#1–5、7–12、14、15、21、34、35、40、41、43）、新立 24（其余）。
