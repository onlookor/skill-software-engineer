# ADR-SRC-P0-06：M4 扩到 signals 两字段与 S-11 转硬

| 项 | 值 |
|---|---|
| 状态 | **approved**（2026-11-08） |
| 范围 | `registry/scripts/project.py`（`check_m4`／`check_signals`）；`registry/CHECK-SPEC.md`（C1 M4 行／C5.13／C5.18／C5.20）；`registry/DATA-SPEC.md` D3.1；`method_registry.yaml`（`G-SRC-1` 闭合＋5 处旧说明）；`predicate_vocabulary.yaml`（VG-09 记 `resolution_2026_11_08_bC`） |
| 母本 | **零改动**（4,463 行／围栏 216）；`predicate_vocabulary.yaml` 在册名 **零增删** |
| 级别变更 | **S-11：info → hard**（并覆盖 `when_predicate`）；S-10 仍 info（观测面同步扩到 `when`）；M4 硬项，覆盖面扩 2 字段 |
| 上游 | ADR-SRC-P0-02（S-10／S-11 立为 info）、ADR-SRC-P0-03（批 B 登记）、ADR-SRC-P0-04（6 detection＋3 when 改写）、ADR-SRC-P0-05（`behavior_switch`＋两条 when） |
| 闭合 | **`G-SRC-1` → closed**（closure 块；statement／impact／affected／route 原文逐字保留，0.22） |

## §1 授权与范围

用户指令（2026-11-08，一笔做完）：① **M4 扩面**——校验范围从 `anti_patterns[].detection_predicate` ＋ `applicability` 扩到 `signals[].detection_predicate` 与 `severity_condition.when_predicate`；② **S-11 覆盖 `when` 并转硬**——纯散文在 `when` 里也算失败，不再只报 info；③ 顺带把 S-10 的观测面同步扩到 `when`（原本就是 0，扩面不会红）。验收标准：转硬后 `--check` 仍硬 0／软 0，且**不是靠豁免达成**。

边界：若真出现红，**不加豁免规则去压**，停下逐条报；旧注释／旧说明（「S-9 与 M4 解耦」「signals 暂不校验」「由 G-SRC-1 承接」）一并改成现状；`G-SRC-1` 若可闭合按流程记 `resolution` 与 gap 状态，不顺手改别的 gap。

## §2 M4 扩面

### §2.1 覆盖面（改前 → 改后）

| 字段 | 改前 | 改后 | 条目数 |
|---|---|---|---|
| `anti_patterns[].detection_predicate` | ✓ | ✓ | 369 处 |
| `applicability.{problem,current,delivery}_space` | ✓ | ✓ | 762 处 |
| `signals[].detection_predicate` | ✗ | **✓** | **14 处**（8 条 SRC 的 14 个子信号） |
| `signals[].severity_condition.when_predicate` | ✗ | **✓** | **5 处**（`SRC-001-S1`／`SRC-001-S2`／`SRC-004-S1`／`SRC-005-S1`／`SRC-007-S1`；其余 9 个子信号 `severity_condition: null`） |

- **M4 扫描面 1,131 → 1,150 处**（+19：14 条 detection_predicate ＋ 5 条 when_predicate）。
- 实现：`check_m4` 在既有两段之后追加 `signals` 段；空值跳过（空值由 S-2／S-4／S-6 承担，避免同一事实两处判失败）；`severity_condition` 非 dict 时跳过（形状由 S-6 承担）。
- 判据未变：仍只做**词汇封闭**（名 ∈ `predicates ∪ formula_words ∪ clause_defined_predicates`），与 anti_patterns／applicability 全项同口径。

### §2.2 为什么是「并入 M4」而不是「S-11 独自转硬」

M4 是 0.17.8 的 seed 资格项（`SEED_CHECKS`），S-11 不是。若只把 S-11 转硬而不并入 M4，则「signals 用本地造词」会让 `--check` 硬失败，却不影响 seed 资格——账面与资格脱节。并入 M4 后，未登记谓词同时触发 M4 硬失败与 C-ST 回落，与 anti_patterns 的处理完全一致。

S-11 保留为**独立 check id**（不挂 M2），理由同前批：C-ST 按 M2 判 seed 资格，若 S-11 复用 M2 会把「纯散文」记录成 M2 失败，造成 seed 资格误判。

## §3 S-11 转硬（核心裁决）

### §3.1 为什么现在可以硬——依据是实测数字，不是设计推断

| 观测 | info 期实测 | 说明 |
|---|---|---|
| S-10（词表未登记调用） | **恒 0** | 自 ADR-SRC-P0-02 立面以来每次 `--check` 均为 0；说明 19 串判据的**全部**谓词调用都已在册 |
| S-11（纯散文） | **6 → 0** | 首立时 6 条（ADR-SRC-P0-02 清点）；经 ADR-SRC-P0-04 改写 6 条 detection 后归 **0**，ADR-SRC-P0-05 再补两条 when 后仍 **0** |
| 扩到 `when` 的干跑（ADR-SRC-P0-05 §5） | **红 0** | 5 条非空 `when` 全部含已登记调用 |

三项合起来说明：**不是「预计不会红」，而是「在 info 期已经红过、已经修完、现在真的不红」**。这正是 C5.19 要求的前置条件，也是本批不再等一批观察期的理由。

### §3.2 判据形式

- **量词**：`∀ it ∈ signals: (detection_predicate 非空 → ∃ n ∈ predicate_names(detection_predicate), n ∈ vocab) ∧ (when_predicate 非空 → 同上)`。
- **判定**：不满足 → `rep.fail('S-11', …)` **硬失败**，报文逐条列出 `signal_id`、字段名与原串（`「…」`），便于直接定位。
- **与 S-10 的分工**：S-11 判「有没有至少一个已登记调用」（存在性）；S-10 列出「哪些调用未在册」（封闭性明细）。两者提取器完全相同（`predicate_names()`），故 S-10 恒 0 是 S-11 可硬的**必要条件**，不是重复检查。
- **与 M4 的分工**：M4 判「每个调用都已在册」（全称），S-11 判「至少有一个调用」（存在性）。S-11 比 M4 弱，但覆盖面不同——M4 空值跳过（由 S-2／S-4 判失败），S-11 对空值同样跳过；两者都不判元数。

### §3.3 C5.19 三条件的达成情况（含残余，逐条记账）

| # | 条件 | 结论 | 依据 |
|---|---|---|---|
| (i) | 全部 `signals` 串的谓词调用在册且元数可判 | **已满足（名）/ 部分（元数）** | 名：S-10 恒 0。元数：`PRED_CALL_RE` 只校名、不校元数——与 M4 对 anti_patterns／applicability 的既有口径完全一致，非 signals 独有；故不构成 signals 的单独阻断项，登记为**全检查面共有残余**（§9） |
| (ii) | 纯散文判据逐条裁定「改写为表达式」或「显式豁免并登记」 | **已满足，且零豁免** | 6 条全部改写（ADR-SRC-P0-04 §2），**未新增任何 waiver／entry_level_exemptions／白名单** |
| (iii) | 元数校验纳入检查面 | **未满足（显式登记）** | 同 (i)。若强求先补元数校验再转硬，则等于要求一次性改造 M4 全项，范围远超本批；且元数失配在 signals 与 anti_patterns 上是同一风险，单点收紧会造成不一致 |

### §3.4 转硬后的实际结果（验收）

```
自检：1212 条记录｜硬失败 0｜软警告 0｜占位符 1478 处＝事实 1＋槽 1477
```

- **零豁免**：`waivers` 台账、`entry_level_exemptions`、`GAP_SO_WHITELIST` 本批**均未新增项**；S-11 没有任何 `skip`／白名单分支。
- 记录数 1,213 → **1,212**：不是 S-11 造成的（S-11 在转硬前后均为 0 行），而是 `G-SRC-1` 闭合后其原「open gap 无 open SO 承接」的 1 条 info 记录消失。
- info 41 → **40**（未成立 2 → 1，余 `G-PRJ-1`）。

## §4 S-10 同步扩到 `when`

- 改前：S-10 已扫 `detection_predicate` 与 `when_predicate` 两字段（ADR-SRC-P0-02 实现时即已两字段），本批只把**报文口径**明确为「判据在 M4 硬检查」。
- 实测：未登记调用 **0**（扩面不产生任何记录）。
- 级别保持 **info**：它现在承担的是「分项可读性」——M4 只报「某条目有多少未登记谓词」，S-10 报「具体哪个 signal 的哪个字段用了哪个未登记名」。不转硬，避免与 M4 在同一事实上产生两条硬失败。

## §5 `G-SRC-1` 闭合

- **闭合依据**：route 原文写「逐条把谓词登记进 `predicate_vocabulary.yaml` → 登记完成后另开 ADR，把 M4 扩到 `signals[].detection_predicate` 并重跑 M4」。前段由 ADR-VG09-01／ADR-SRC-P0-02／ADR-SRC-P0-03／ADR-SRC-P0-05 完成；后段由本 ADR 完成并重跑。**闭合条件已逐字满足**。
- **登记形态**：`status: open → closed` ＋ 同条目 `closure` 块（`gap_ref`／`date`／`ruled_by`／`basis`／`evidence`／`preserved`），statement／impact／affected／route **原文逐字保留**（0.22）。
- **反向指引处理**：statement／impact／affected 中的「本批 M4 不扫 signals」「signals.detection_predicate 是未机器封闭的文本」是 2026-11-06 登记时点的事实，不能改写原文，故另加 `note` 明确「不再指向现状，今后以 closure 与 ADR-SRC-P0-06 为准」。
- **未动其他 gap**：`G-PRJ-1` 维持 open；`G-GOV-2`／`G-GRD-1`／`G-STY-*` 等未触碰。SO 台账未增删（`SO-1`／`SO-6` 仍 open，均不指向 `G-SRC-1`）。
- **VG-09 未随之闭合**：该 gap 仍有 2 项残余（`cycle_scale` 待 5.2.1 环规模定义；`lower_layer_coverage`／`baseline_change_record` 仍为 `resolved_by_composition`），与本批无关，保持 open。

## §6 旧注释／旧说明改写清单

| # | 位置 | 旧文（摘） | 改后 |
|---|---|---|---|
| 1 | `project.py` `check_signals` docstring | 「S-10 info…S-11（原 info）」 | S-1～S-8 hard／S-9 info／S-10 info／**S-11 hard**；并写明「signals 两字段已并入 M4（ADR-SRC-P0-06）」「此前『signals 暂不校验／由 G-SRC-1 承接』的口径已终止」 |
| 2 | `project.py` S-4 报文 | 「本批禁；谓词缺口走 G-SRC-1」 | 「S-4 禁；谓词缺口走 R2 提议并登记 vocabulary_gaps」（不再指向已闭合的 gap） |
| 3 | `project.py` S-10／S-11 段前注释 | 「info，只报不判；转硬属下一批，等干跑结果裁定」 | 「S-10（info：词表封闭观测…判据在 M4）」「S-11（hard：…2026-11-08 ADR-SRC-P0-06 转硬，依据是 info 期实测 6→0）」 |
| 4 | `project.py` S-10 报文 | 「info 不判」 | 「info 不判；判据在 M4 硬检查」（明确分工，不留「无人判」的错觉） |
| 5 | `project.py` 报告渲染 | 「S-10／S-11（info，只报不判；转硬须另批 ADR）」 | 分项渲染：S-10 注「判据在 M4 硬检查」；S-11 注「hard（ADR-SRC-P0-06…）」 |
| 6 | `project.py` `vocab_names_cached` docstring | 「供 S-10/S-11 的 info 级观测使用」 | 「供 S-10（info 观测）与 S-11（纯散文硬判据）使用」 |
| 7 | `project.py` `check_m4` docstring | 只写 anti_patterns＋applicability | 增「signals 两字段」与「G-SRC-1 据此闭合，旧口径已终止」 |
| 8 | `method_registry.yaml` `SRC-001.constraints_imposed` | 「signals.detection_predicate 须最终可执行（**G-SRC-1 结清前不宣称**）」 | 「detection_predicate 与 when_predicate 须词汇封闭、可执行（**2026-11-08 起由 M4 硬校验，S-11 硬判纯散文**）」 |
| 9 | `method_registry.yaml` `SRC-001.narrative.common_misuse` | 「（本批禁，谓词缺口走 **G-SRC-1**）」 | 「（S-4 禁，谓词缺口走 R2 提议并登记 vocabulary_gaps）」 |
| 10 | `method_registry.yaml` `SRC-004.narrative.benefit_cost_analysis` | 「属于 **G-SRC-1 待登记谓词**」 | 「（expiry_of／cleanup_filed／behavior_switch）已于 2026-11-08 登记，但其取值仍依赖台账与人工分类」 |
| 11 | `method_registry.yaml` `SRC-007.narrative.benefit_cost_analysis` | 「依赖 T5 谓词登记（**G-SRC-1**）」 | 「（pyramid_distortion／distortion 已于 2026-11-08 登记）」 |
| 12 | `method_registry.yaml` `ST-SRC-01.note` | 「通过 S-1～S-9；detection_predicate 的可执行性不宣称（**G-SRC-1 保持 open**）」 | 「通过 S-1～S-11；detection_predicate 与 when_predicate 的词汇封闭性由 M4 硬校验、纯散文由 S-11 硬判（2026-11-08 ADR-SRC-P0-06）」 |
| 13 | `method_registry.yaml` `G-SRC-1` | `status: open` | `status: closed` ＋ closure ＋ note（原文逐字保留） |
| 14 | `CHECK-SPEC.md` C1 M4 行 | 「`detection_predicate` 词汇封闭…逐 `detection_predicate`」 | 四字段全覆盖，量词列逐字段展开 |
| 15 | `CHECK-SPEC.md` C5.18 | 「S-10／S-11 **均为 info 级、只报不判**」 | S-11 hard（两字段）、S-10 info（分项明细）；附「2026-11-08 级别变更」注 |
| 16 | `CHECK-SPEC.md` C5.13 | 只写「只登记缺口、不定义、不造词」 | 追加「G-SRC-1 已 closed（ADR-SRC-P0-06）…不再指向任何在办事项」（原文保留） |
| 17 | `DATA-SPEC.md` D3.1 | 「applicability＋anti_patterns.detection_predicate 只能使用登记谓词名」 | 四字段并列，并注明「由同一检查 M4 硬校验」「G-SRC-1 据此闭合」 |
| 18 | `predicate_vocabulary.yaml` VG-09 | `workaround`「保持自然语言散文判据，不写调用式」／`affected`「M4 现不扫 signals」／`route`「登记后另开 ADR 扩扫」 | 原文保留，新增 `resolution_2026_11_08_bC.superseded` 三条逐条标明「已终止／已过期／已履行」 |

## §7 被否方案

| 方案 | 否决理由 |
|---|---|
| A. 只转硬 S-11、不并入 M4 | 未登记谓词不进 seed 资格，账面与资格脱节（§2.2） |
| B. 把 S-11 挂在 M2 上转硬 | C-ST 按 M2 判 seed 资格 → 纯散文会被记成 M2 失败，seed 资格误判（历史已踩过） |
| C. 给 S-11 加白名单／豁免把残余散文压掉 | 用户明令禁止；且会把「账面全绿而判据不可执行」固化（C5.19 原意） |
| D. 先补元数校验再转硬 | 需改造 M4 全项（369＋762＋19 处），远超本批范围；元数是全检查面共有缺口，单点收紧反致不一致（§3.3） |
| E. 转硬后保留 S-10 的 info「未登记」为只报不判 | 保留——但明确其**判据在 M4**，避免读者以为「未登记也没事」 |
| F. 把 `G-SRC-1` 一并标成 `resolved` 而不写 `closure` | 违反 C4.4／C4.2 的闭合形态；且会丢失 statement／impact 的原文留痕 |

## §8 影响与不变量

- entries **138／138 seed** 不变；硬检查通过项 **968**、软警告 **0**。
- 词表零增删：`predicates` **158**（predicate 148、term 9、constant 1）＋`formula_words` 7＋`clause_defined_predicates` 53＝**218**。
- 占位符 **1,478**（事实 1＋槽 1,477）不变；指针反查 miss **0**；母本 **0 行增减**。
- gap：24 项不变，open **2 → 1**（余 `G-PRJ-1`）；open SO **2**（`SO-1`／`SO-6`）不变。

## §9 残余：「写了散文也能过」的口子

本批只关掉了两类口子（signals 两字段的**未登记谓词**与**纯散文**）。**仍然存在的口子**（按风险从高到低）：

1. **零调用但含非中文的串**：S-11 只要求「至少一个已登记调用」。形如 `distortion(system) ∧ 实际总是成立` 的串——后半段是散文，但因为前半段有调用而通过。**这是本批最大的口子**：判据的「可执行」只验了名，没验整串是否都可求值。
2. **元数失配**：`monotonic_trend()`／`burn_rate(a, b, c)` 等调用名在册、实参个数不对，M4 与 S-11 均不判（`PRED_CALL_RE` 只取名）。
3. **`applicability` 之外的其他文本字段**：`envelope.bound_expr`（M3 只判参数化与出处，不判词汇封闭——`Σ`／自由散文可混写）、`cost_profile.*`、`constraints_imposed.constraint`、`narrative.*`、`consumption.note` 全部是自由文本，无任何词汇封闭检查。
4. **`anti_patterns[].description` 与 `signals[].name`**：S-4 只判非空，纯中文描述永远通过。
5. **`when` 与 `detection` 的语义关系**：无交叉校验——`when_predicate` 可以与 detection 无关（甚至恒真），只要「至少一个调用在册」即过。S-11 不判「when 是否为 detection 的子集」（ADR-SRC-P0-05 §3 对 `SRC-007-S1` 是人工核的，不是机器判的）。
6. **中文量词与关系词**：`predicate_names` 只识别 ASCII 标识符后跟 `(`；`∀ 硬性质`／`无下层覆盖` 这类中文表达式不产生调用，若串里另有一处调用则整串通过。

一句话：**现在的检查面能保证「signals 两字段都以已登记谓词开头/为主干」，不能保证「整串只由已登记词与合式公式构成」**——后者需要「全串解析」（BNF 级）而非「名闭包」，是下一个独立的检查项。
