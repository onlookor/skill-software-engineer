# R2 提案：`selection_context` 机器层谓词登记（R2-PRED-SC-01）

| 项 | 值 |
|---|---|
| 提案编号 | `R2-PRED-SC-01` |
| 缺口类别 | **甲类**（成文法应补），依 `编译规范.md` §1.4(2) |
| 触发来源 | 试点切片 C6／F2 R2：8 张实质卡全部 escalate，同一谓词名 |
| 关联记录 | `pilot/vertical-slice-20261112/run-log.md` §4、§10、§29；`escalate-adjudication-20261113.md` §14 |
| 起草 | 2026-11-14，Agent（本会话） |
| 决策记录状态 | **`approved`** |
| `approved_by` | `onlookor` |
| `approver_kind` | `human` |
| `approved_at` | `2026-11-14` |
| 批准依据 | 2026-11-14 人类批准（父会话转达，取建议默认 A）；**Agent 未自批** |
| 母本指纹（批准前） | `sha256:c0bb9879…c17c4510`（4,811 行） |

## 1 缺口描述

`selection_context` 在母本中被当成白板谓词使用，但从未进入机器层谓词块：

| 位置 | 内容 | 说明 |
|---|---|---|
| 母本 L328 | 0.18.2 **S0 输出**：`selection_context(DP, F, C)` 写入白板 | 定义性使用（三元） |
| 母本 L333 | 0.18.2 **S1 输入**：`selection_context` | 下游消费 |
| 母本 L440 | 0.18.7 示范的「谓词变化：∅ → {selection_context(DP-41,…), …}」 | 作为白板谓词出现 |
| 母本 L411–415 | 0.18.6 **机器层谓词块**：只有 `selection_procedure`／`step_log`／`exclusion_record`／`verdict_table` | **缺 `selection_context`** |
| `编译规范.md` L90 | `predicate_name // 白板谓词名（成文法机器层谓词，如 selection_context、verdict_table）` | 编译规范已把它当作机器层谓词示例 |
| `registry/predicate_vocabulary.yaml` | 无 `selection_context` | F2 的 `vocab_names` 取自此处 → R2 判 escalate |

结论：母本内部三处按谓词使用、0.18.6 块漏登记，编译规范又把它举为机器层示例——这是登记遗漏，不是语义争议。

**编译期后果**：`check-card.py --all` 的 F2（引用闭合）R2 对 8 张实质卡全部 escalate（`selection_context`），C6 的 `fidelity_verdict` 因此不能记 `pass`。正式启动编译后，每个方法选型类决策都会命中同一 escalate，属结构性缺口，不是单卡瑕疵。

## 2 归类判定

甲类。理由：
- 丙类（编译规范自行解决）不成立——卡片侧无法消除：删去该谓词则 0.18.2 S0 的输出无处落，且与母本 L328／L333 字面冲突；
- `编译规范.md` §1.4(4) 禁止「以编译限制为由降低成文法要求」，故不能靠卡片改写绕过。

## 3 影响分析

- **阻塞**：C6 判据（`fidelity_verdict = pass`）；随之阻塞 C7（发布与版本对齐）。
- **不阻塞**：试点产物发布本身。`编译规范.md` §6.5「escalate 的批量形态：不阻塞发布，但 escalate 清单随产物发布」。
- **正式路径**：该缺口按决策数量线性放大，且每次增量重编译都会重现。

## 4 候选方案

| 方案 | 做法 | 代价 | 收益 | 风险 |
|---|---|---|---|---|
| **A（建议默认）** | 母本 0.18.6 谓词块补 `selection_context(DP, F, C)` 一行（附语义注：S0 装配的三空间事实集与生效约束集快照）；`registry/predicate_vocabulary.yaml` 增 `name`／`arity: 3`；0.7 `pattern_version` `pv-1.0 → pv-1.1`（语义变更，MINOR）；`软件工程元框架成文法-changlog.md` 登记 | 母本 +1 行；`pattern_version` 递增后，白板声明与全部产物基线需同步到 `pv-1.1`（机械可做） | F2 转 pass、C6 可记 pass；8 张卡无需改动（已按母本写该谓词）；后续批次不再重复上报 | 判据一「模式版本一致」的比较基线整体切换，需一次全量重跑确认 |
| B（不推荐） | 卡片侧改写：用 `selection_procedure(DP, S0, ctx)` 或 `step_log.inputs` 承载 F／C，不动母本 | 改 8 张卡的 S0 输出与依赖文本；F1 锚定需引入映射豁免 | 免母本改动 | 与母本 L328 字面冲突；实质是降低成文法要求，触碰 §1.4(4) 禁令 |
| C（可接受但不推荐） | 维持 escalate，按 §6.5 随产物发布清单 | C6 不能记 pass、C7 不闭合；每次重编译重报 | 零改动 | 结构性缺口留给正式编译，规模放大 |

## 5 建议默认值

**方案 A**。理由：只补登记、不改语义；母本两处用法与编译规范示例已把该名视作机器层谓词；方案 B 触碰禁令，方案 C 把结构性缺口后移。

## 6 批准后的执行清单（供人类勾选）

1. 母本 0.18.6 谓词块 +1 行 `selection_context(DP, F, C)`；
2. 0.7 `pattern_version` → `pv-1.1`（附 changlog 登记）；
3. `registry/predicate_vocabulary.yaml` +1 条（`arity: 3`）；
4. 白板与 `artifact.yaml` 的 `pattern_version` 同步；
5. 重跑 `check-card.py --all`，F2 应转 `pass`；再重跑 `registry/checks/runner.py` 确认 39 条分布不回退。

## 7 明确不做

- 不自行修改母本、不自行递增 `pattern_version`、不修改 C6 检查程序；
- 不通过改卡片"消掉"该谓词（方案 B 只在人类选定后执行）。

## 8 执行记录（2026-11-14，方案 A 已执行）

| 动作 | 结果 |
|---|---|
| 母本 0.18.6 谓词块补 `selection_context(DP, F, C)` | 已补；**同段行内追加（占用原空行），总行数 4,811 不变** |
| 0.7 声明值 `pv-1.0 → pv-1.1` | 已改（同一行内替换，行数不变） |
| `registry/predicate_vocabulary.yaml` | 已增 `selection_context`（arity 3），`registry_version` 升 1.1.0 |
| `pattern_version_baseline.yaml` | 首冻 14 块（`0753e743d6f0…`）；**D1 后重冻 17 块（`f329ce90ad77…`）** |
| 白板／artifact／10.2.5 判据一 | 已同步到 `pv-1.1` |
| 判据一 | `check_pattern_version.py` PV-0/1/2/3 全 **pass** |
| 锚漂移 | 见 `pilot/vertical-slice-20261112/run-log.md` §30 |
| `C6-F2` | 见 §30（vocab 已含该名，F2 预期转 pass） |

**副作用与处置（D1 已闭合）**：首冻时 `check_pattern_version.py` 只发现带 `**机器层谓词**` 标记的 **14** 块，而 `registry/DATA-SPEC.md` D1.4 的权威清单是 **17** 块（含 0.18.6／0.22.4／0.23.5），导致 `pv-1.1` 与 `pv-1.0` aggregate 相同（`0753e743d6f0…`）。

人类批准 D1（2026-11-14，`user`）后：检查器改为按 D1.4 权威清单发现（每节首个围栏块），重冻 `pv-1.1` 为 17 块、aggregate **`f329ce90ad77dc2249bd467b47ffee9e12ddcf43d2969e59c100662383b44c4c`**，与 `pv-1.0` 分离；母本未再改动（4,811 行、sha `469d64c0…`），锚漂移 0。重冻理由与批准依据已记入基线条目 note、`artifact.yaml` 与 run-log §31。
