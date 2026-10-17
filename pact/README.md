# `pact/` — 软件工程元框架的 PACT 形式层声明

本目录是母本与《部署规模裁剪模板》的**形式投影**：把"什么必须先于什么存在""谁有权读/消费/生产什么"这两类结构命题，编译成 PACT v1 rev2 的 `.pact` 域声明，从而可被 `pact analyze` 机械校验。

## 1. 权威关系（最重要的一条）

```
软件工程元框架成文法.md（母本）  ┐
                                  ├─→  pact/*.pact（形式投影，本目录）
软件工程元框架-部署规模裁剪模板.md ┘        │
                                          └─→ 各 .pact 文件头注释（本档取值与表达边界的就地说明）
```

- `.pact` **不得新增任何规范命题**。若发现某条母本规则无法用 rev2 文法表达，正确处置是：记入该档文件头的"已知表达边界"（E 系列），把该规则留在配套内容层执行，并按母本 §0.13 提请裁决——**不是**在 `.pact` 里造语法。
- 反向亦成立：`.pact` 中出现的每个类型与每条前置规则都必须能回指母本条款；文件头已逐类型标注条款指针。回指不上即是幻觉条目，删除。
- 裁剪的合法性判据在裁剪模板 §1.1（红线 R1–R6 + 两项结构性必备）与 §1.2（三合法轴）。本目录只承载三轴中的**粒度**轴；**频次**与**工具形态**两轴在 rev2 中没有词汇，必须落配套内容层（见 §4）。

## 2. 文件清单

| 文件 | 档位 | 类型 | 前置规则 | 角色位 | seed 权威 | `m` | `N` |
|:--|:--|--:|--:|--:|--:|--:|--:|
| `se_tier1_solo.pact` | 档 I：单人 / 单 Agent | 40 | 31 | 15 | 9 | 1 | 1 |
| `se_tier2_small_team.pact` | 档 II：小团队 | 41 | 32 | 18 | 9 | 2 | 2 |
| `se_tier3_multi_team.pact` | 档 III：中大型 / 多团队多服务 | 41 | 32 | 20 | 9 | 3 | 3 |

`m` = 批准链深度（`count approval_escalation >= m` 判链耗尽）；`N` = 消解链深度上限（母本 §0.19.5，`not count concession_record >= N`）。

三档**不是**人数门槛，选档判据见裁剪模板 §3 的三档装配画像。要点：

- 档间差异只有三处：参与者名册与角色合并度、`count` 阈值、配套层的条目子集/频次/工具形态。
- 档 III 的类型集与前置图与档 II **完全一致，零增删**——多团队不引入新的结构命题，只引入新的角色位与更高的阈值。
- 档 III 即使"不裁剪"，也必须按裁剪模板 §1.3 登记"本部署按母本默认形态全量装配"这一事实。未登记的全量装配等同隐性裁剪（无基线可比），落入裁剪模板 §4 违例清单。

## 3. 校验

```bash
# 单档静态分析（六项）
pact analyze software-engineering/pact/se_tier1_solo.pact

# 与需求工程片段组合（§1.8 C1–C4）后终检
pact compose requirements-engineering/pact/re_fragment.pact \
             software-engineering/pact/se_tier3_multi_team.pact > /tmp/composed.pact
pact analyze /tmp/composed.pact
```

当前状态（宿主机 `~/projects/pact/target/debug/pact` 离线校验）：

| 检查项 | 档 I | 档 II | 档 III | RE × 档 III 合并域 |
|:--|:--|:--|:--|:--|
| `precondition_wf` | 良构 0/0 | 良构 0/0 | 良构 0/0 | 良构 0 违规 / 1 警告 |
| `reachability` 不可达 | 0 | 0 | 0 | 0 |
| `gate_coverage` | 0 | 0 | 0 | 0 |
| `structural_deadlock` | 0 | 0 | 0 | 0 |
| `stranding_risk` | 0 | 0 | 0 | 0 |
| `consumption_reachability` | 30 | 31 | 31 | 31 |

两项需知其所以然的非零输出：

- **`consumption_reachability` 30/31 项不是技术债**。逐项归类为三类：常驻注册表资产（8 项）、证据保全对象（10 项，母本 §8.2.6 要求 `auditor` 长期只读，消费即入 Archive 会切断审计口）、终态审计工件（12 项）。完整归类表见 PACT 仓库 `docs/skill-adaptation.md`。
- **合并域的 1 项警告 `SEED_PRODUCE_OVERLAP(re_baseline)`** 来自 SE 侧持有 `seeds re_baseline` 而 RE 侧持有 `produces re_baseline`。两者并存的意图是：SE **单独**部署时基线由外部导入（seed），RE+SE **同时**部署时基线必须由 RE 验证链生产（此时 SE 侧的 seed 权威应当撤除）。该警告是咨询性的（§1.4.3 Advisory），不阻塞加载；撤除 seed 会让 SE 单独部署时 `re_baseline` 不可达，故两份文件都保留现状，由部署决策裁决。详见 `docs/skill-adaptation.md`。

## 4. rev2 不表达的维度（一律落配套内容层）

以下母本命题在 rev2 中**没有词汇**，写进 `.pact` 即为造语法：

| 维度 | 母本出处举例 | 落点 |
|:--|:--|:--|
| 时间 / 频次 / 时限 | 批准时限、复审周期、"连续 3 轮未过闸则升级" | 各档装配说明、检查单 |
| 概率与模糊判据 | 风险 likelihood、"实质性影响"的程度判断 | 方法注册表条目的谓词 |
| OR 多路由 | 批准/驳回/延期三分支 | 表现为"不产生任何 Token"（§1.4 零隐式动作） |
| 图结构判据 | 冲突成环检测、血缘下游目检 | 走查规程（母本 x.6） |
| 三值语义与 unknown 传播 | M15 勘察义务占位符 | 注册表台账 |
| 成本数值 / SLO / 包络界表达式 | §0.15 包络、成本台账数值 | `cost_ledger` Token 的 ThingRef schema |
| 角色位互不兼任 | 三级批准链独立性、Waiver 利益无关性 | `approval_registry_entry` 条目 + 部署前检查单 |

第七条是档 III 最需要人类复核的表达缺口：PACT 参与者是**不透明标识**，无自然人身份、无互斥约束词汇。形式层能保证的只是"存在三个独立的 `produces approval_record` 角色位"，不能保证它们由三个不同的人填充。

## 5. 表达边界索引

各档文件头以 E 编号就地记录已知表达边界，跨档累积：

| 编号 | 命题 | 出现于 |
|:--|:--|:--|
| E1 | 前置唯一性（RHS Uniqueness）禁止 `selected_entry` 经两路汇聚到同一 `decision_landing`，故 ADR 路径与简记路径建成两条不相交 Token 流；互斥性编码为 `reads selected_entry when not exists adr_package` | 档 I 起 |
| E2 | `produces` 不得携带条件（`ProduceWithCondition`），故一切阈值/存在性判据改挂 `reads` / `consumes` | 档 I 起 |
| E3 | 权威六级全序 A0–A5 中只有 A0 有 Token（`external_mandate`）；A1–A5 的比较是配套层谓词 | 档 I 起 |
| E4 | 让步记录的三个强制消费端在形式层是 `reads`（Rule-R 非破坏）+ Archive 审计链 | 档 I 起 |
| E5 | rev2 无时序词汇，"会签先于批准"编码为 Counter 在场性 | 档 I 起 |
| E6 | `approval_escalation` **只读不消费**——否则 `count approval_escalation >= m` 永远无法累积，链耗尽判定失效 | 档 II 起 |
| E7 | "角色位互不兼任"不可表达 | 档 III |

## 6. 变更纪律

- 改 `.pact` 后必须重跑 §3 的两组命令，全绿方可提交。
- 变更按 `AGENTS.MD` 追加登记到 `../编译规范-changlog.md`（PACT 形式层属编译产物形态，规程面归《编译规范》）；语义裁决若触及母本，另走 `../软件工程元框架成文法-changlog.md`。
- 本目录的设计说明、验收清单与三档粒度差异矩阵不在此重复，权威记录在 PACT 仓库 `~/projects/pact/docs/skill-adaptation.md`。
