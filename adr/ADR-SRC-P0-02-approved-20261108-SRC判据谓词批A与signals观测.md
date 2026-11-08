# ADR-SRC-P0-02：SRC 判据谓词批 A 登记与 signals 观测（S-10／S-11）

| 项 | 值 |
|---|---|
| 编号 | `ADR-SRC-P0-02` |
| 状态 | approved（2026-11-08 人类责任方批准并当批落地） |
| 影响级别 | 中（词汇表 +2 名；1 条 `detection_predicate` 改写；工具增 2 项 info 观测；**母本 0 改动、M4 未改**） |
| 关联条款 | 母本 9.2.3（第 3615–3639 行信号源表）、9.5（谓词清单）、6.4／6.5（质量属性接口与 `burn_rate`）、5.5（`flag`／`expiry`）、3.2.1（`schema`） |
| 关联台账 | `predicate_vocabulary.yaml`: VG-06 `resolution_2026_11_08_bA`、VG-09 `resolution_2026_11_08_bA`；`method_registry.yaml`: `SRC-004.S1` |
| 关联规范 | `registry/CHECK-SPEC.md` C5.18（本批先例）、C6.2（检查项变更走 0.13） |
| 前例 | `ADR-VGEX-01`（VFAM 9 名一次性扩容）、`ADR-VG03-NR-01`（单名扩容）、`ADR-SRC-02`（signals 字段落盘与 M4 解耦声明） |
| 后续批 | 批 B（M4 扩至 `signals[]` 转硬）**未执行**，须另案批准 |

---

## 1. 授权与范围

### 1.1 授权

人类责任方 2026-11-08 指示：按 `G-SRC-1` 方案执行，**两批分开**。批 A 三件必须同批完成（缺一件则 M4 扩后即红）；S-9／S-10 只给 info、**不转硬**、不得顺手并入 M4。

### 1.2 本批范围

| # | 改动 | 面 |
|---|---|---|
| 1 | 登记 `metric_hit`（`kind: predicate`，arity 1） | 词汇表 `predicates` |
| 2 | 登记 `burn_rate`（`kind: term`，arity 1，VG-06 口径） | 词汇表 `predicates`（`kind: term` 行） |
| 3 | `SRC-004-S1` 判据 `expiry(flag)` → `expiry_of(flag)` | `method_registry.yaml` |
| 4 | 台账：VG-06／VG-09 各记 `resolution_2026_11_08_bA` | 词汇表 `vocabulary_gaps` |
| 5 | 工具：S-10／S-11 两项 **info** 观测 ＋ 台账「改判登记」放行 | `scripts/project.py` |

**未做**：母本零改动；M4 检查范围未改；`signals` 判据未转硬；未把 S-10 并入 M4；`consumed_by` 未动。

---

## 2. `metric_hit` 的登记与判据分工

### 2.1 登记

```yaml
- {name: metric_hit, arity: 1, kind: predicate, source: {source_type: clause_id, value: "9.5", verified: true},
   note: "metric_hit(adr)：可推翻指标命中（9.2.3 第 3635 行「保守假设可推翻指标命中」）…"}
```

### 2.2 与 `falsification_metric(adr, metric, threshold, window)` 的分工

| 谓词 | 元数 | 承载什么 | 判定面 |
|---|---|---|---|
| `falsification_metric(adr, metric, threshold, window)` | 4 | **登记声明**：某 ADR 的可推翻指标、其阈值、观察窗口 | 声明是否存在（静态可查） |
| `metric_hit(adr)` | 1 | **事件判定**：该 ADR 已登记的指标在登记窗口内越阈 | 观测事实（运行时/度量） |

- **为什么一元取 `adr`**：`SRC-006-S1` 现行判据逐字为 `∃ adr: falsification_metric(adr) ∧ metric_hit(adr)`。`falsification_metric(adr)` 是四槽的部分绑定（只绑首槽，是合法的 ∃ 绑定形态），`metric_hit(adr)` 因此以 **adr** 为唯一实参、语义为「该 ADR 的已登记指标在窗口内越阈」。若改取 `metric` 为实参，`∃ adr` 无法把 `metric_hit(metric)` 与所选 `adr` 关联，判据失义。故 arity 1 **必须取 adr**，且 `SRC-006-S1` **零改动**。
- **为什么不再带 metric／threshold／window**：三者已由 `falsification_metric` 登记；重复携带会造出第二个真源（与 `metric_hit` 原名下的旧散文式 `canary_gate.threshold ∧ window 判定命中` 同一病因）。
- **形态约束**：禁用 `metric_hit(adr, metric)` 等多元形态（M4 只校名不校元数，须靠 note 约束）。

### 2.3 与 VG-09 旧结论的关系

VG-09 的 `resolution_2026_11_06` 把 `metric_hit` 列为 `resolved_by_composition`（散文式）。本批把它改判为直接登记，理由是该散文式**不可执行**（`canary_gate.threshold ∧ window 判定命中` 无谓词骨架，M4 无法判）。旧块**原文保留**（0.22），改判记入 `resolution_2026_11_08_bA.registered[].was`。

---

## 3. `burn_rate` 的登记（VG-06 口径）

### 3.1 登记

```yaml
- {name: burn_rate, arity: 1, kind: term, source: {source_type: clause_id, value: "6.5", verified: true}, …}
```

### 3.2 为什么是 `term` 而非 `predicate`

- **出处双证**：9.2.3 第 3634 行「错误预算燃尽率、基线漂移」（信号源表第 2 行）＋ 6.4 施加项 Q7；6.5 第 2914 行逐字 `burn_rate monitored(→ aspect 9)`。
- **槽名充函数**：6.5 第 2913 行 `error_budget(service, slo, b, burn_rate)` 中 `burn_rate` 是**第四槽名（量值槽）**——与 `expiry` 同型（`flag` 第四槽名）。槽名充谓词属反模式（VG-04 (i)／VG-05 (i) 判读），故按 **term**（一元数值函数）登记，`burn_rate(service)` 返回燃尽率。
- **不并入 `monitored`**：「是否已接入监控」由在册 `monitored` 承载；`burn_rate` 只承载量值，两者不合并、不加别名。
- **不改 SRC-005-S1**：其判据逐字为 `burn_rate(·) 连续窗口越阈 ∧ 趋势同向`，一元通配与 arity 1 相容，改登记即通过。

---

## 4. `SRC-004-S1` 改写

| 项 | 值 |
|---|---|
| 改前 | `∃ flag: now > expiry(flag) ∧ ¬cleanup_filed(flag)` |
| 改后 | `∃ flag: now > expiry_of(flag) ∧ ¬cleanup_filed(flag)` |

- **只换名、不改语义**：`expiry_of` 是 5.5 第 2581 行的在册 term，语义即「开关到期时刻」；`now` 与 `cleanup_filed` 均在册（后者为 Z6 第四支）。
- **不加别名**：`expiry` 不单独登记、不设 alias；母本 5.5 第 2600 行 Z6 的 `expiry(G)` 保持原样（那是母本原文，槽名充函数的既有用法）。
- **行内注**：判据后附改写依据，避免后人回改。

---

## 5. 台账规则增补：改判登记（工具变更）

### 5.1 问题

`check_ledgers` 原规则：`resolved_by_composition` 里的名若同时出现在词汇表 → 硬失败「重复真源」。本批 `metric_hit` 正是这种情况（旧块按 0.22 必须保留原文）。

### 5.2 增补

新增「改判放行」：扫描全部 `resolution_*` 块的 `registered` 列表，凡在其中的名，若与旧复合式同名，**不再判重复真源**，改记 info「复合式已被后续 resolution 改判为直接词条（历史原文保留，0.22）」。

- **为什么不是删除旧块**：0.22 承诺「已登记批次不改写」；删旧条目等于篡改历史。
- **为什么不是放行一切同名**：无 resolution 依据的同名仍判硬失败——放行只承认**有 ADR 的显式改判**，防止「顺手重登」。
- **级别变化**：属检查语义变更，按 C6.2 记入 CHECK-SPEC C5.18，并在本 ADR 留痕；不改任何既有违规的级别（原硬判项除「已有改判依据」外全部不变）。

---

## 6. S-9／S-10 编号与落地

### 6.1 编号冲突（须记明）

`check_signals` 中 **S-9 已被占用**——`consumption.note` 缺失时的 info 行（ADR-SRC-02 既有）。为不重排既有标号（重排会使历史报告对不上），本批新检查编为：

- **S-10**：`signals[].detection_predicate` 与 `severity_condition.when_predicate` 的词表封闭观测；
- **S-11**：`detection_predicate` 至少含 1 个已登记谓词调用（纯散文观测）。

即用户指示中的「S-9」在本批落为 **S-10**，「S-10」落为 **S-11**；语义与级别（info）完全按指示，仅标号顺延。

### 6.2 实现要点

| 项 | 做法 |
|---|---|
| 词表来源 | 新增 `vocab_names_cached()`，与 `build_vocab` 同口径（`predicates ∪ formula_words ∪ clause_defined_predicates`），不产生报告行 |
| 提取器 | 复用 M4 的 `predicate_names`（`([A-Za-z_][A-Za-z0-9_]*)\s*\(`，剔方括号）——保证「S-10 的口径 = 将来扩 M4 的口径」 |
| 级别 | `level='info'`，且**独立 check id**（`S-10`／`S-11`）。不挂在 `M2` 下：C-ST 的 seed 资格按 `M2` 判定，挂 `M2` 会把 info 观测误当硬失败（首轮实测即出现 `SRC-003/004/007` 三条 `C-ST` 假失败，已改） |
| 渲染 | `自检报告.md` 增两节（S-10／S-11），使干跑结果可留档 |
| 退出码 | 不参与——`main` 只看 hard／soft |

### 6.3 干跑结果

- **S-10 命中 0**：批 A 之后，`signals` 全部 19 串（14 detection ＋ 5 非空 when）中的谓词调用**均在册**。
- **S-11 命中 6 条 detection**（3 个条目）：`SRC-003-S1`／`SRC-003-S2`／`SRC-004-S2`／`SRC-007-S1`／`SRC-007-S2`／`SRC-007-S3`。
- **when 侧（S-11 不覆盖，人工清点）**：5 条非空 `when_predicate` **全部零调用**（`SRC-001-S1`／`SRC-001-S2`／`SRC-004-S1`／`SRC-005-S1`／`SRC-007-S1`），属同一「纯散文」盲区。

---

## 7. 批 A 之后若扩 M4 转硬

### 7.1 预计红数

**0 条。** 实测以 M4 同款提取器扫 `signals` 全量（14 detection ＋ 5 when）：未登记调用 **0**。

> 批 A 前三处红点：`SRC-004-S1`（`expiry`）、`SRC-005-S1`（`burn_rate`）、`SRC-006-S1`（`metric_hit`）；本批分别以「改写为在册 term」「新登记 term」「新登记 predicate」消解。

### 7.2 会不会有意外

- **不会因造词变红**，但有三个须正视的**结构性盲区**，都不表现为红：
  1. **6 条 detection ＋ 5 条 when 是纯散文**——M4 判「无调用 = 通过」，扩 M4 不解决可执行性。这是最大的意外来源：账面全绿而判据仍不可执行。
  2. **元数不校验**——M4 只校名。`metric_hit(adr, metric)` 这类错元数写法可通过；`deployed_on` 三参那条历史问题即由此长期潜伏（2026-11-08 已单独修订）。
  3. **`burn_rate(·)` 通配**——通配符是否算「绑定」取决于运行器语义，静态检查无法判；`SRC-005-S1` 通过不代表运行时可得值。
- **结论**：可以扩，但若同时不上 S-11 转硬（或等价的可执行性判据），扩 M4 只闭合「造词」，不闭合「可判定」。

---

## 8. 母本与检查级别

- **母本**：**0 改动**（4,463 行／围栏 216 不变）。
- **M4**：范围未改（仍只扫 `anti_patterns[].detection_predicate` 与 `applicability`）。
- **级别**：S-10／S-11 为 info，**不参与** seed 资格与退出码；C1.11 的 seed 公式未改。
- **既有硬判项**：仅「改判登记」一条放宽（须有 resolution 依据），其余不变。

---

## 9. 被否方案

| 方案 | 否因 |
|---|---|
| A. 只登记 `metric_hit`，跳过 `burn_rate`／`expiry` | 扩 M4 立即红 2 处（`SRC-005-S1`、`SRC-004-S1`），等于用红信号倒逼后续批次 |
| B. `metric_hit` 取 `metric` 为实参 | `SRC-006-S1` 的 `∃ adr` 无法与之关联，须改判据；批 A 的边界是「登记＋改写 1 条」，不含改 `SRC-006` |
| C. `metric_hit` 四参照抄 `falsification_metric` | 两个真源登记同一阈值／窗口，正是 VG-09 旧散文式的病因 |
| D. `burn_rate` 立 `predicate` | 槽名充谓词，与 VG-04 (i)／VG-05 (i) 判读冲突；且「是否监控」与「燃尽多少」会混成一个词 |
| E. 直接删 VG-09 旧复合式条目 | 违反 0.22「已登记批次不改写」；且丢失「为何曾判为复合式」的历史依据 |
| F. S-10／S-11 挂 `M2` | `C-ST` 会把 info 观测当硬失败（实测已发生，见 §6.2） |
| G. 本轮顺手把 S-10 并入 M4 转硬 | 超出授权（用户明示「等我看完干跑结果再定」）；且有 §7.2 三个盲区未裁 |

---

## 10. 执行记录（实测）

- `--check`：1,216 条记录｜硬失败 **0**｜软警告 **0**｜info 记录 44（其中观测不成立 6：S-11×3 ＋ 既有 LEDGER×1、GAP-SO×2）｜占位符 **1,478**（事实 1＋槽 1,477，不变）｜指针反查 **2,397**（+4：两条新词目的 `source` 指针），miss **0**。
- 词表：`predicates` 块 **150 → 152**（predicate 141→142、term 8→9、constant 1）；`formula_words` 7；`clause_defined_predicates` 53；合计 **210 → 212**。
- `VG-09`：`vocabulary_gaps_count` 9 → **8**（`metric_hit` 由复合式改判为直接登记）。
- 条目 138／seed 138；gaps 24／SO 24；open SO 2（`SO-1`／`SO-6`）；open gap 2（`G-PRJ-1`／`G-SRC-1`，`G-SRC-1` 仍 open——批 A 只消解 3 处调用，9 名中 8 名仍无承载位置）。
- 提交：本批单独一笔；S-10／S-11 工具与规范另起一笔。
