# ADR-SRC-P0-07：元数校验（S-12）info 干跑与解析规则

| 项 | 值 |
|---|---|
| 状态 | **approved（仅限 info 干跑）**；转硬未批准，须另批 |
| 日期 | 2026-11-08 |
| 范围 | `registry/scripts/project.py`（新增 `extract_calls`／`split_call_args`／`vocab_arity_cached`／`check_arity`／`check_arity_census`、报告渲染）；`registry/CHECK-SPEC.md` C5.21；**不改任何数据**（`method_registry.yaml`／`predicate_vocabulary.yaml` 零改动） |
| 检查标号 | **S-12**（info）——编号审计见 §6 |
| 上游 | ADR-SRC-P0-06（M4 覆盖 signals 两字段、S-11 转硬） |

## §1 授权与边界

用户指令（2026-11-08）：把调用实参个数与词表 `arity` 对上，覆盖 M4／S-10／S-11 现扫的全部面——`anti_patterns[].detection_predicate`、`applicability` 三空间、`signals[].detection_predicate`、`signals[].severity_condition.when_predicate`；**先只做 info 干跑，转硬等批**；**不改任何数据**；解析规则（深度 0 切分、通配／空槽、量词前缀、中文实参、无 arity 条目、子串误命中）须在 ADR 写明。

因此本 ADR 的批准范围**只到「观测与规则」**：S-12 为 info，不参与 seed 资格、不改变退出码、不产生硬失败。

## §2 解析规则（R1–R9，实现与判据的唯一依据）

| 编号 | 规则 | 理由／反例 |
|---|---|---|
| **R1** | 调用起点 = 标识符 `[A-Za-z_][A-Za-z0-9_]*` ＋ 可选空白 ＋ **半角** `(`；标识符前**不得紧邻** `[A-Za-z0-9_]` | 防子串误命中：`pyramid_distortion(` 只记 1 个调用，不再额外命中 `distortion(`。匹配整名后连同 `(` 一起消费，扫描指针跳过实参，嵌套名天然不会重复计数 |
| **R2** | 实参只在**深度 0** 的逗号（`,` 或 `，`）处切分；深度 = 半角圆括号／方括号／花括号＋全角圆括号／花括号 | `f(g(a,b),c)` = **2** 个；`dsm(D,{a,b,c})` = **2** 个（`{}` 内不切）；`distortion(system ∧ [（非瞬时抖动）])` = **1** 个 |
| **R3** | 位置占位符 `·`、`_`、`…`、`...` **各算 1 个实参位**（不按「省略」处理） | 母本 `flag(G,_,behavior,_)` 是 4 元；`timeout_budget(path, ·)` 是 2 元而不是 1 元。若把占位当省略，几乎所有合法串都会「多算成少」 |
| **R4** | 量词前缀 `∃ x:`／`∀ x:` **不产生调用**（变量表无圆括号）；量词域里的 `flag(G,_,behavior,_)` 是普通调用，按 4 元计 | 否则 `∃ flag:` 会被误当一次调用 |
| **R5** | `[…]` 内文本整体不参与抽取（事实占位符；与 M4 的 `outside_brackets` 同口径） | 与既有全部检查一致；代价是**方括号里写的调用不计入**（§9 盲点 1） |
| **R6** | 只有**半角** `(` 开启调用；全角 `（…）` 视为中文标点，不开启 | 避免把 `SLA（服务等级协议）`、`ADR（可推翻指标…）` 当成调用（实测这类「伪调用」17 处，全部是散文）。真实影响只有 1 处：`VFM-003` 的 applicability 引用了母本 Z4 原文 `timeout_budget（path）`，属引用文本，单列不判（§9 盲点 2） |
| **R7** | 无 `arity` 的条目**不判**，记「无 arity 可校」并计入普查行 | 当前只有 `formula_words` 五名（`approved`／`declared`／`registered`／`has`／`sourced`）。它们不是「登记错」，而是**本来就没有元数**（§4） |
| **R8** | 未在册名**跳过**，不重复报 | 已由 M4 硬失败覆盖；重复报会造成同一事实两条记录 |
| **R9** | 中文实参整段算 1 个实参，除非深度 0 处出现逗号；深度 0 的中文逗号**按分隔符处理** | `has_approved_exception(该交互)` = 1 元；若作者用中文逗号分隔实参，则按分隔符算——此规则可能把「散文里的中文逗号」误当分隔，故**所有全角逗号切分点都随不匹配一并输出**，由人工复核（本批未出现此类误切，§4 解析可疑 0） |

一条总则：**解析失败不静默**。括号未闭合、空实参（尾逗号）等一律进「解析可疑」行；本批实测 **0** 处。

## §3 量（干跑实测）

```
调用 501 处
  anti_patterns              470
  applicability                6
  signals.detection           19
  signals.when                 6
无调用串 870 处（余下的 applicability 多为 [中文事实占位] 项）
无 arity 可校 72 处（approved×8、declared×27、has×16、registered×18、sourced×3）
解析可疑 0 处
元数不匹配 43 处（12 个谓词名）
```

- 覆盖串数：1,150（与 M4 扫描面同口径），其中 280 串含 ≥1 个调用。
- `signals` 面 19＋6 = 25 处调用，全部解析成功；`when` 的 5 条非空串共 6 处调用。

## §4 不匹配清单（43 处 / 12 名）

| # | 谓词 | 词表 arity | 实得 | 处数 | 典型原串 |
|---|---|---|---|---|---|
| 1 | `registry_entry` | 6 | 2 | 23 | `registry_entry(·, VFM-001)` |
| 2 | `delivery_semantics` | 2 | 1 | 3 | `¬declared(delivery_semantics(I))` |
| 3 | `timeout_budget` | 2 | 1 | 3 | `Σ timeout_budget(path) > [SLA 上界]` |
| 4 | `shared_write_exception` | 3 | 1 | 3 | `¬approved(shared_write_exception(流程))` |
| 5 | `interaction_flow` | 3 | 2 / 1 | 2 / 1 | `interaction_flow(path, sync_chain)`／`interaction_flow(·)` |
| 6 | `selection_log` | 3 | 2 | 2 | `selection_log(d, ·)` |
| 7 | `quality_impact_card` | 2 | 1 | 1 | `quality_impact_card(模式)` |
| 8 | `verdict` | 2 | 3 | 1 | `verdict(·, ·, ·)` |
| 9 | `dsm` | 2 | 1 | 1 | `dsm(system)`（`SRC-001-S1`） |
| 10 | `has_approved_exception` | 3 | 1 | 1 | `has_approved_exception(该交互)`（`SRC-002-S1`） |
| 11 | `baseline` | 2 | 1 | 1 | `baseline(metric)`（`SRC-005-S2`） |
| 12 | `falsification_metric` | 4 | 1 | 1 | `falsification_metric(adr)`（`SRC-006-S1`） |

### §4.1 归类汇总

| 归类 | 处数 | 明细 |
|---|---|---|
| **A. 串写错** | **11** | `delivery_semantics(I)`×3（同文件另有 `(I, ·)` 的补位写法，属漏占位）；`timeout_budget(path)`×2＋`(·)`×1（漏第 2 槽）；`selection_log(d, ·)`×2（3 元只给 2）；`interaction_flow(path, sync_chain)`×2（把 kind 写进第 2 槽，participants 位错位）；`verdict(·,·,·)`×1（**多**给 1 个实参） |
| **B. 规则未覆盖** | **32** | B1：`registry_entry(·, VFM-001)`×23——同形批量；按定义为 6 元且第 2 槽是 `kind`，实参给的是**条目 ID**，疑似想表达「某条目的注册记录／某族条目」，当前无可表达此意的谓词。B2：单点前缀投影 9 处——`shared_write_exception(D)`×3、`quality_impact_card(模式)`×1、`interaction_flow(·)`×1、`dsm(system)`、`has_approved_exception(该交互)`、`baseline(metric)`、`falsification_metric(adr)` |
| **C. arity 登记错** | **0** | 12 名的登记值**全部**与母本定义行一致（`registry_entry` 6 @493、`interaction_flow` 3 @2569、`delivery_semantics` 2 @2573、`timeout_budget` 2 @2575、`shared_write_exception` 3 @2282、`selection_log` 3 @495、`quality_impact_card` 2 @2577、`verdict` 2 @2893、`dsm` 2 @1716、`has_approved_exception` 3 @1477、`baseline` 2 @3723、`falsification_metric` 4 @3727）。**无需改词表** |

B2 的「前缀投影」有母本先例：`interaction_flow(F).kind`（母本 4 处，属性投影）、`shared_write_exception(D)`（2288）、`has_approved_exception(S1,S2)`（1487，定义为 3 元却只给 2 元）、`verdict(c)`（564，定义为 2 元）；`quality_impact_card` 更含歧义——2499 以 1 元形式定义卡片内容，2577 以 2 元使用。因此**不能把「实参数 < 登记 arity」一律判错**——这正是本批只做 info 的原因。

## §5 若直接转硬

| 指标 | 数值 |
|---|---|
| 会红 | **43 条**（22 个条目 + 全量行，硬失败口径下记 22 条失败记录） |
| 其中真问题 | **11 条**（A 类，漏占位／槽位错位／多给实参） |
| 其中假阳性（规则未覆盖） | **32 条**——B1 23 条是**同一处模式错**（不是 23 个独立手误），B2 9 条是有母本先例的前缀投影 |
| 另有无法判定 | **72 处**（`formula_words` 无 arity）：转硬前必须先定「跳过算通过还是算未覆盖」，否则是**静默盲区** |

结论：**现在不能转硬**。转硬前至少要：① 对 B1 做一次批量裁决（改串 / 立谓词 / 显式允许「条目族投影」）；② 对 B2 写明「前缀投影是否合法」；③ 给 `formula_words` 一个显式处置（建议保持「无 arity 不判」并计入覆盖面报告，而不是给它们编 arity）。

## §6 编号审计（防 S-9 事故重演）

现有检查 id 全量清点（`scripts/project.py` 实际产出）：

```
M2 M3 M4 M5 M6 M9 C-ID C-ENV C-KP C-ST META PTR VCB LEDGER GAP-SO S-10 S-11
```

- **S-1～S-9**：不占用独立 id，全部经 `rep.*('M2', …)` 记录（S-9 为 info）；**S-9 已被 `consumption.note` 缺失占用**，不得改指。
- **S-10**（info）／**S-11**（hard）：由 ADR-SRC-P0-02 立面、ADR-SRC-P0-06 调整。
- **S-12**：本批采用前**逐一核对上表，确认未被占用**；本 ADR 即为占用记录。若后续批次声称 S-12 用于他项，以本 ADR 为在先占用，必须先改名并登记旧→新映射，**不得静默复用**。

## §7 被否方案

| 方案 | 否决理由 |
|---|---|
| A. 用 `PRED_CALL_RE.findall` 直接数名、不切分实参 | 无法回答元数；且 `findall` 不消费实参，嵌套与子串都可能重复命中 |
| B. 只做「实参数 ≤ arity」的宽松检查 | 会漏掉 `verdict(·,·,·)` 这类多给实参；且「少于」本身仍需规则 |
| C. 把前缀投影一律判错 | 与母本自身用法冲突（§4.1 B2 先例），会产出大量假阳性 |
| D. 顺手把 11 条 A 类串改掉 | 用户明令「不改任何数据」；且改串涉及判定面语义，须单独立项 |
| E. 给 `formula_words` 编 arity | 它们没有元数定义，编出来的值就是本地造词（违反编译规范 2.3） |
| F. 转硬并把 B 类登记成 waiver | 用户明令不加豁免压红；且会把「规则缺口」伪装成「已处置」 |

## §8 影响与不变量

- **数据零改动**：`method_registry.yaml`／`predicate_vocabulary.yaml` 无 diff；entries 138／138 seed；词表 218 名不变。
- 检查面新增 **1 个 info 检查**（S-12），记录数 1,212 → **1,235**（+23：22 条条目行＋1 条全量行）；硬 0／软 0 不变；退出码不变。
- `SEED_CHECKS`／`ENTRY_CHECKS` 未改，S-12 不影响 seed 资格。

## §9 已知盲点（本批刻意不覆盖，留待转硬前裁决）

1. **方括号内调用不计**（R5）：`[E 覆盖 pattern（参见 f(x)）]` 里的 `f(x)` 不参与元数校验。
2. **全角括号调用不计**（R6）：`timeout_budget（path）` 这类引文形态不判；实测仅 `VFM-003` 1 处，属引用母本原文。
3. **变长槽**：`registry_entry(..., fields...)` 的末槽是变长，严格元数在此处本身不可判定；本批按固定 6 元计，故把「给多」与「给少」都报出来，交人工裁决。
4. **字符串字面量与自然语言**：`description`／`narrative.*` 不在覆盖面（与 M4 同口径）。
5. **同形多义**：同名在不同 clauses 下可能取不同元数（如 `verdict` 母本有 1 元与 2 元两种用法）；本批以「词表登记的单一 arity」为唯一期望值，冲突即报。

---

**2026-11-08 状态更新（ADR-SRC-P0-08）**：§5 的转硬建议已执行；§4 的 43 条不匹配已按 A／B 归类修补（A 11 条、B 32 条；C 类仍为 0）。S-12 已由 info 转 hard，`--check` 硬 0／软 0、零豁免。本 ADR 原文与历史数字保留（0.22）；现状以 ADR-SRC-P0-08 与 `projections/自检报告.md` 为准。
