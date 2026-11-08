# ADR-SRC-P0-03：SRC 判据谓词批 B（8 名清单核对与 5 名登记）

| 项 | 值 |
|---|---|
| 状态 | **approved**（2026-11-08） |
| 范围 | `predicate_vocabulary.yaml` 的 `predicates` 块与 `VG-09` 台账；`SRC` 条目机器层字符串**不改** |
| 母本 | **零改动**（4,463 行／围栏 216） |
| 检查面 | M4 未改；S-10／S-11 **维持 info**，不转硬 |
| 上游 | ADR-SRC-P0-02（批 A）、ADR-VG09-01 |

## §1 授权与范围

用户指令：把 `conforms_to`、`auth_bypass`、`execution_order`、`assertion_fact_mismatch`、`consecutive_failure`、`remediation_or_waiver_record`、`monotonic_trend`、`burn_rate` 按上一轮给出的 kind／arity／出处逐条立词条；`burn_rate` 批 A 已登记，只补它在 `SRC-005-S1` when 的调用面，不重复立词条。

边界：M4 扩 `signals`、S-10／S-11 升硬**三项均不做**；凡需改 8 条 SRC 机器层字符串者**只报改法、不改**；每件单独提交。

### §1.1 清单核对（先核后做）

| # | 名 | 本批前状态 | 本批动作 |
|---|---|---|---|
| 1 | `execution_order` | **已在册**（ADR-VG09-01 D1-A，词表第 98 行，arity 2） | 不重复登记 |
| 2 | `assertion_fact_mismatch` | **已在册**（ADR-VG09-01 D1-A，词表第 103 行，arity 1） | 不重复登记 |
| 3 | `burn_rate` | **已在册**（ADR-SRC-P0-02 批 A，term，arity 1） | 不重复立词条；调用面见 §3.3 |
| 4 | `conforms_to` | `VG-09.resolved_by_composition` | **本批登记**（predicate，arity 2） |
| 5 | `auth_bypass` | `VG-09.resolved_by_composition` | **本批登记**（predicate，arity 2） |
| 6 | `monotonic_trend` | `VG-09.resolved_by_composition` | **本批登记**（predicate，arity 2） |
| 7 | `remediation_or_waiver_record` | `VG-09.resolved_by_composition` | **本批登记**（predicate，arity 1） |
| 8 | `consecutive_failure` | `VG-09.resolved_by_composition` | **本批登记**（predicate，arity 2） |

故本批实际新增 **5 行**，不是 8 行。

## §2 逐条登记表

| 名 | kind | arity | 出处 | 签名 | 改判理由（相对原复合式） |
|---|---|---|---|---|---|
| `conforms_to` | predicate | 2 | 3.5 | `conforms_to(x, contract_C)` | 复合式 `connects ∧ ¬covers` 只覆盖「流量—契约」一路；`SRC-003-S1` 的 schema ↔ 报文结构面不在 `connects` 定义域 |
| `auth_bypass` | predicate | 2 | 4.5 | `auth_bypass(D, consumer)` | 基词 `provider` 不在母本与三表（LEDGER 已记该项基谓词缺失），复合式不可执行；绕过判定是单一二值判断 |
| `monotonic_trend` | predicate | 2 | 9.5 | `monotonic_trend(metric, window)` | 复合式依赖的 `trend_window_verdict` 是 `signal` 第 5 槽名（9.5 第 3712 行），槽名充谓词不可执行 |
| `remediation_or_waiver_record` | predicate | 1 | 9.5 | `remediation_or_waiver_record(case)` | Waiver（9.2.2 五要素）与 debt_item（9.5 利息表达式）分属不同台账、准入不同，`∨` 压成单值会丢失台账类型 |
| `consecutive_failure` | predicate | 2 | 8.5 | `consecutive_failure(case, window)` | `verdict_of(E)` 是单点三值（8.5 第 3433 行），无法表达「连续 N 周期」 |

五条均**只登记、不定义新规范命题**（0.17.1）：出处 clause 在母本可反查，语义取母本既有措辞（9.2.3 第 3615–3622 行、9.2.1 第 3601 行、6.4 第 1655 行、8.5、3.5、4.5）。

### §2.1 与在册名的撞名核查

- `conforms_to` 与 `registered`／`covers` 无同名；`auth_bypass` 与 `access_path`／`owner` 无同名；`monotonic_trend` 与 `drift`（9.5 第 3712 行）无同名（后者是登记值与观测集的偏差，非时间序列趋势）；`remediation_or_waiver_record` 与 `waiver`／`debt_item` 无同名；`consecutive_failure` 与 `verdict_of` 无同名。
- 五个名均不出现在 `pending_review`，不与 `consumed_by` 冲突。

## §3 §3.3 `burn_rate` 的调用面（只报改法，不改）

`burn_rate` 已是一元 `term`；它在 `SRC-005-S1` 的 `severity_condition.when_predicate` 里目前是散文「错误预算耗尽」，**没有调用式**。补调用面必须改 `method_registry.yaml` 的机器层字符串，属本批边界禁止项，故只给改法：

```text
现：when_predicate: "错误预算耗尽"
改：when_predicate: "burn_rate(service) ≥ error_budget(service, slo, b, ·) 的耗尽阈值"
```

- 该改法只用两个在册名（`burn_rate` term、`error_budget` 谓词）。
- 若下一批批准，须同时确认 `error_budget` 的四槽与 `burn_rate` 的一元是否匹配（`burn_rate` 只填量值槽）。
- 本批**不改**，`SRC-005-S1` 的 `when_predicate` 仍是散文，S-11 的检测面（只看 `detection_predicate`）不受影响。

## §4 台账与改判登记

- `VG-09.resolution_2026_11_08_bB`：`predicate_rows_added: 5`，`registered` 五条各带 `was`（原复合式原文）与 `reason`；`already_in_book` 记三条已在本册；`carried_2026_11_08_bB` 记残余（`cycle_scale` residual、`lower_layer_coverage`／`baseline_change_record` composition）；`vocabulary_gaps_count: 3`。
- **不记闭合**：VG-09 仍有 3 项未决（1 residual＋2 composition），本批只减项、不改状态。
- 改判规则沿用 `check_ledgers` 的 `_reassigned` 放行（ADR-SRC-P0-02 §5）：历史 `resolved_by_composition` 原文保留（0.22），有 `resolution_*.registered` 者记 info，无依据的同名仍硬失败。

## §5 干跑结果（登记不改变机器可判性）

| 检查 | 批 A 后 | 批 B 后 |
|---|---|---|
| S-10（signals 词表封闭，info） | 0 | **0** |
| S-11（detection 纯散文，info） | 6 | **6** |

**原因**：S-10 统计的是「调用式里出现了未登记名」；signals 面本来就没有未登记调用（批 A 已清零）。S-11 要求字符串里出现 `name(`；五条新登记名不会让散文串自动变成调用式，而本批又不许改字符串，故命中数不变。这不是回归，是「登记词条」与「机器可判」两件事的分离——本批只完成前者；后者在下一批改字符串时才发生。

S-11 的 6 条与 5 条 when 清单见批 A 报告，本批未变。

## §6 母本、M4、级别

- 母本 **0 行增减**；新增锚 **0**（本 ADR 与词表注释均不使用 `@NNNN` 形式）。
- M4 **未改**（仍只扫 `anti_patterns[].detection_predicate` 与 `applicability`）。
- S-10／S-11 **仍为 info**、不入 seed 资格、不改退出码（CHECK-SPEC C5.18／C5.19 未动）。
- 8 条 SRC 条目的任何机器层字符串**均未改**（含 `SRC-004-S2`、`SRC-007-S2`、`SRC-007-S3`、`SRC-005-S1`）。

## §7 被否方案

| 方案 | 否决理由 |
|---|---|
| A. 把 8 名全部重立一遍 | 会与 ADR-VG09-01／ADR-SRC-P0-02 的登记形成重复真源，触发 `check_ledgers` 硬失败 |
| B. 顺带改写 6 条散文 detection 为调用式 | 越界（用户明令只报改法）；且改写会改变信号判据文本，属另一批 ADR |
| C. 把 S-10／S-11 借机转硬 | 越界；且转硬前置（元数校验、纯散文裁定）未满足，会把「账面全绿而判据不可执行」固化 |
| D. 将 VG-09 一次记成 closed | 仍有 3 项未决；闭合须状态迁移授权，且会掩盖 `cycle_scale` 的定义缺口 |
| E. 给 `burn_rate` 再立一个 predicate 版本 | 同一名两种 kind 会破坏封闭集纪律；槽名充谓词的反模式已由 VG-06 判读排除 |

## §8 执行记录

- 词表编辑：新增 5 行（3.5／4.5／9.5×2／8.5 各就其方面）；`VG-09` 增 `resolution_2026_11_08_bB`。
- 自检：`--check` **1,216 条记录**｜硬失败 **0**｜软警告 **0**｜**info 44**（其中未成立 **5**：`S-11`×3、`GAP-SO`×2）；占位符 **1,478**（事实 1＋槽 1,477，不变）；指针反查 **2,397→2,407**（+10＝五条词条 source 5＋`resolution` 块 source 5），miss 0。
- 词表规模：`predicates` **152→157**（predicate 142→**147**、term 9、constant 1）；`formula_words` 7、`clause_defined_predicates` 53；合计 **212→217**。
- 级差说明：批 A 报告记 info 44／未成立 6，本批未成立降为 5——`LEDGER VG-09:auth_bypass` 由「基谓词不在母本/词汇表」未成立改为「已随 `resolution` 改判为直接词条」成立（该行仍为 info）。
