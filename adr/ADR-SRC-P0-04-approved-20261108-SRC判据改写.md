# ADR-SRC-P0-04：SRC 判据改写（6 条 detection ＋ 3 条 when；`SRC-004-S1` 删 when 评估）

| 项 | 值 |
|---|---|
| 状态 | **approved**（2026-11-08） |
| 范围 | `method_registry.yaml` 的 `signals[].detection_predicate` 6 条、`signals[].severity_condition.when_predicate` 3 条 |
| 母本 | **零改动**（4,463 行／围栏 216） |
| 级别 | 信号 `severity`／`raise_to` **均未改**；M4 未扩；S-10／S-11 仍 info |
| 上游 | ADR-SRC-P0-02（批 A）、ADR-SRC-P0-03（批 B） |

## §1 授权与范围

用户指令：把 6 条纯散文 `detection_predicate` 改写为含已登记调用的判据，使 S-11 归 0；改写后**语义不得收窄、不得放宽**；凡因写调用式而丢掉的条件须单列；`SRC-004-S1` 的 `when_predicate` 删除前须核 `detection` 是否已完整承载门槛，有缺口即停。

三次提交：①6 条 detection；②3 条 when；③`SRC-004-S1` 删 when（本 ADR §4 判定后**停做**）。

## §2 六条 detection 改写（第一笔）

| 条目 | 改前原文 | 改后原文 |
|---|---|---|
| `SRC-003-S1` | `schema 声明与实际报文结构不一致 ∧ 偏离持续（非瞬时抖动）` | `¬conforms_to(schema_decl, 报文实际结构) ∧ 偏离持续（非瞬时抖动）` |
| `SRC-003-S2` | `access_path 绕过 owner 授权 ∧ 违例流量可指认到具体单元` | `∃ D, consumer: access_path(D, consumer, ·, ·) ∧ auth_bypass(D, consumer) ∧ 违例流量可指认到具体单元` |
| `SRC-004-S2` | `∃ 交互: 依赖未登记的执行顺序 ∧ 该顺序被观测到再次生效` | `∃ 交互: execution_order(e1, e2) ∧ 该顺序未登记 ∧ 该顺序被观测到再次生效` |
| `SRC-007-S1` | `pyramid_distortion ∧ distortion ∧ ∃ hard property 无下层覆盖` | `pyramid_distortion(system) ∧ distortion(system)` |
| `SRC-007-S2` | `∃ 测试: 套件断言与在册事实不符 ∧ 该断言被当作通过依据` | `∃ 测试: assertion_fact_mismatch(该测试) ∧ 该断言被当作通过依据` |
| `SRC-007-S3` | `∃ 用例: 连续周期失败 ∧ 未进入整改或豁免记录` | `∃ 用例: consecutive_failure(该用例, window) ∧ ¬remediation_or_waiver_record(该用例)` |

### §2.1 语义保持逐条

- `SRC-003-S1`：主判据「schema 声明与报文实际结构不一致」由 `¬conforms_to` 承载（`conforms_to(x, contract_C)`，ADR-SRC-P0-03）；「偏离持续（非瞬时抖动）」**原样保留为散文合取项**，未压掉。
- `SRC-003-S2`：`access_path` 四槽保留路径存在性（后两槽用通配 `·`，与 `deploy_on` 的先例同类）；`auth_bypass(D, consumer)` 承载「绕过 owner 授权」；「违例流量可指认到具体单元」原样保留。
- `SRC-004-S2`：`execution_order(e1, e2)` 承载「存在一条执行顺序」；「未登记」原样保留（该词的未登记判定按 `execution_order` 条目注属 `covers`／`registered` 侧，不并入谓词）；「被观测到再次生效」原样保留。
- `SRC-007-S1`：两个合取项各成一元调用；第三个合取项「∃ hard property 无下层覆盖」**由 `distortion` 的定义吸收**（`distortion(system)` 条目注：T5 失真且 hard property 无下层覆盖；母本 8.5）。见 §5。
- `SRC-007-S2`：主判据由 `assertion_fact_mismatch(该测试)` 承载；「该断言被当作通过依据」原样保留——它是「被采信」这一条件，不含在 mismatch 判据内。
- `SRC-007-S3`：`consecutive_failure(该用例, window)` 承载「连续周期失败」；`¬remediation_or_waiver_record(该用例)` 承载否定项「未进入整改或豁免记录」，**否定号保留**，未改成肯定式。

## §3 三条 when 改写（第二笔）

| 条目 | 改前原文 | 改后原文 |
|---|---|---|
| `SRC-001-S1` | `恶化持续（连续窗口同向漂移）` | `monotonic_trend(dsm_metric, window)` |
| `SRC-001-S2` | `恶化持续（连续窗口同向漂移）` | `monotonic_trend(环规模, window)` |
| `SRC-005-S1` | `错误预算耗尽` | `burn_rate(service) ≥ error_budget(service, slo, ·, ·) 的耗尽阈` |

- `SRC-001-S1`：D 的指标是「跨边界调用密度」，故实参用 `dsm_metric`（与 D 的 `dsm(system)` 同源）。
- `SRC-001-S2`：**对指令的一处最小偏离**——其 D 的指标是「环规模随时间单调上升」，不是 `dsm_metric`；若照抄 `dsm_metric` 会把判据绑到 S1 的指标上，属**语义收窄**。故实参取 `环规模`。
- `SRC-005-S1`：阈值不填数值，改为对**在册 `error_budget(service, slo, budget, burn_rate)`**（6.5 第 2897 行）的 budget 槽取「耗尽阈」；`service` 前缀保留，未引入任何精确数。备选写法 `burn_rate(service) ≥ 1` 未采用（`1` 无母本出处，属 0.4 门槛禁止的假精确）。

## §4 `SRC-004-S1` 删 when 评估（第三笔：**停做**）

指令要求先核 `detection`（`∃ flag: now > expiry_of(flag) ∧ ¬cleanup_filed(flag)`）是否完整承载「行为级开关（Z6 违例）」的门槛，有缺口即停。

**结论：有缺口，停做。** 三处缺口：

1. **适用范围缺口**：`detection` 对**全部** flag 成立，不区分行为级与结构级；`when` 的「行为级开关」正是把 `raise_to: P0` 收窄到 `flag(G,_,behavior,_)` 的护栏（母本第 2600 行 Z6 的量词域）。删 `when` 但保留 `raise_to` → 结构级开关超期未清理也会升 P0，属**判定面放宽**；连 `raise_to` 一起删 → 9.2.3 第 3633 行「Z6 违例 → P0（行为级开关）」的 P0 路整条消失。
2. **支路缺口**：Z6 违例含四个合取支（`approved(ADR(G))`／`declared(expiry(G))`／`now ≤ expiry(G)`／`cleanup_filed(gate)`），`detection` 只覆盖后两支的否定（超期 ∧ 未清理）；「无批准 ADR」「无 expiry 声明」两支不在 `detection` 内。
3. **条款指代缺口**：`when` 同时把判定挂到 Z6 条款（9.2.3 第 3633 行引 Z6），删掉后该 SRC 与 Z6 的接线只剩 `consumption.note` 文字，不构成机器可判挂钩。

**待用户裁定**的三条替代路径（未执行）：

| 路径 | 动作 | 后果 |
|---|---|---|
| i. 保留 `when`，改写为可调用式 | `∃ G: flag(G, ·, behavior, ·) ∧ ¬cleanup_filed(G)` 之类 | `flag` 若未在册则须先走 R2；判定面不变，仅机器可判性提升 |
| ii. 把「行为级」下沉到 `detection` | `∃ flag: now > expiry_of(flag) ∧ ¬cleanup_filed(flag) ∧ 行为级(flag)` | 仍留散文，但删 `when` 后 P0 收窄由 D 承担；须核 `behavior` 是否可判 |
| iii. 维持现状 | 不改 | `when` 留作散文；S-11 覆盖 `when` 后仍红 1 条 |

## §5 丢弃／调整的条件清单（显式）

| 条目 | 处理 | 说明 |
|---|---|---|
| `SRC-007-S1` 第三合取项「∃ hard property 无下层覆盖」 | **由定义吸收**（非静默丢弃） | `distortion` 条目注即「T5 失真且 hard property 无下层覆盖」；若日后修订 `distortion` 定义，本项须同步回评 |
| `SRC-001-S2` when 实参 `dsm_metric` → `环规模` | **调整**（非丢弃） | 原指令给的实参与该条 D 的指标不符，照抄会收窄语义 |
| 其余改写 | 无条件丢弃 | 所有散文合取项原样保留 |

## §6 自检与命中数

- `--check`：**1,213 条记录**｜硬失败 **0**｜软警告 **0**｜**info 41**（未成立 **2**＝`GAP-SO`×2）。记录数由 1,216 降为 1,213，因 S-11 的三条命中行消失。
- S-10／S-11 干跑：**S-10 = 0，S-11 = 0**（第一笔后）。
- 占位符 1,478（不变，改写未引入方括号）；指针反查数不变（未新增 source）。

## §7 母本、M4、级别

母本 **0 行增减**；M4 **未扩**（仍只扫 `anti_patterns[]` 与 `applicability`）；S-10／S-11 **仍 info**；全部信号 `severity`／`raise_to` 未改。

## §8 被否方案

| 方案 | 否决理由 |
|---|---|
| A. 全部压成单一干净表达式 | 会削掉「偏离持续」「被当作通过依据」「可指认到具体单元」等条件，违反“语义不得收窄” |
| B. `SRC-007-S1` 静默丢掉第三合取项 | 违反“不得静默丢弃”；本 ADR §5 显式登记由定义吸收 |
| C. `SRC-005-S1` 用 `burn_rate ≥ 1` | `1` 无母本出处（0.4 门槛） |
| D. `SRC-004-S1` 按指令直接删 `when` | §4 三处缺口，推销定面或放宽，故停做报裁 |
| E. 借机把 S-11 覆盖 `when` / 转硬 | 越界；转硬前置（元数校验、纯散文裁定）未满足 |
