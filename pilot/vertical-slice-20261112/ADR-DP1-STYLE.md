# ADR-DP1-STYLE：pact-dsh 通信/协调风格定案（同步请求-响应）

- 决策点：`DP-1-STYLE`
- 步骤：`0.18.2 S6`（决策落地）
- 日期：2026-11-12
- 执行者：agent（本会话）
- 批准人：`wgz`（人类用户本人，批准角色注册表 `registry/approval_registry.yaml` 的"风格定案"主批准人）
- 批准时间：2026-11-12T21:29:21+08:00
- 批准时限：48 小时（届满 2026-11-14T21:29:21+08:00）
- 备选链：空（`GOV-PACT-001`：主批准人不可用即构成批准不可达）
- 决策记录状态：**`provisional`**（见 §7；SM-DR 迁移 `blocked → under_review → approved → provisional`）

---

## 1 背景

`pact-dsh` 是 DSH agent loop 的治理插件：在 `onPreStep` / `onPreTool` 上同步调用 backend 判定参与者是否 enabled，据此 allow/deny。方法选型规程 `0.18.2 S0–S6` 在 S5 选中 `STY-001`（同步请求-响应），S4 在本轮首次拿到 verdict，S6 需给出决策落地。

## 2 决策

采用 `STY-001`（同步请求-响应）作为 `pact-dsh` 方面 1 的通信/协调风格，写入白板谓词：

```
style(pact-dsh, (·, ·, 同步请求-响应, ·))
```

- 谓词形态由编译规范 5.7 P1–P3 生成：`scope=pact-dsh`，`S=(·,·,同步请求-响应,·)`（`row_id=1.2.3-同步请求-响应` 填槽 1.2.3，其余槽 `·`）。
- 版本向量推进：`aspect_1 0→1`（style 写入）、`aspect_6 0→1`（verdict_table 写入）、`aspect_10 0→0`（无投影物化）。
- 决策状态为 `provisional`：谓词可写，但下游消费只许按软约束并附张力承认 ADR（7.2.5）。

## 3 被拒候选（S2 必备节）

| 候选 | 处置 | 依据 |
|---|---|---|
| STY-002（异步消息） | S1 排除 | `applicability=false`：无消息中间件（F3）、无需削峰（F5）、无需时间解耦（F6）、无可靠投递要求（F7）；四者均为 false 而非 unknown，无 M15 勘察义务 |
| STY-004（事件溯源） | 未进入候选集 | `applicability` 不满足；仅与 STY-001 存在 `compatibility(tension)`，不在候选集 |

## 4 证据集

| 项 | 位置 | 指纹 |
|---|---|---|
| 母本（框架版本） | `软件工程元框架成文法.md` | `sha256:6d4b0100c7a87ee2d4b18c9d20840ad2600095dd32901aa2bf17cf4f792c34f0` |
| 方法注册表 STY-001 v0.1.0 | `registry/method_registry.yaml` | `sha256:c235265add5ca6ea3fc626c3d328a4d861c05bfffd6a27d91d4c4af1900ffa7b` |
| 目标集 | `pilot/vertical-slice-20261112/target-set-pact-dsh.yaml` | `sha256:3cf0433cfbb79b37c741279e3e378cfa704ce586e8c5c081f94fb89266074a23` |
| 包络实参绑定 | `pilot/vertical-slice-20261112/envelope-bindings-pact-dsh.yaml` | `sha256:93bc90cfcb64f145ad8016e2c9061a0368651e6420c56614bca21bcf571a0d8c` |
| S4 verdict | `pilot/vertical-slice-20261112/s4-verdict-pact-dsh.yaml` | `sha256:b8d91cffd4b3b82d045060f305dda375cb15dbfdeaf236b8f44e1095aa873537` |
| 批准角色注册表 | `registry/approval_registry.yaml` | `sha256:a0457a4e3b8f197f29cee2051ae91b8a5a93827766b831493c94c4926a529013` |
| 检查程序 | `pilot/vertical-slice-20261112/check-card.py` | `sha256:9a66eb0b774c5a627ec3398f9376052cde0a40c351b13d8dd3b2dcaff1799f9e` |
| 产物清单 | `pilot/vertical-slice-20261112/artifact.yaml` | 见 `pilot-20261112.2` |
| 步骤日志 | `pilot/vertical-slice-20261112/run-log.md` §3、§11、§12 | — |
| 白板快照 | `pilot/vertical-slice-20261112/whiteboard-pact-dsh.yaml`（version_vector `{1:1, 6:1, 10:0}`） | — |

执行记录：仓库内本地执行，无 CI 运行标识（本切片未触发 CI）；环境 Linux / Python 3 / Node 20–22（CI 矩阵见 `.github/workflows/ci.yml`）。

> **输入版本更新（2026-11-12 第 1 批，ADR-STY-ENV-01）**：本表所列目标集、包络绑定、S4 verdict 与方法注册表指纹为批准时的记录，保留不改写。第 1 批（D-15-A＋D-14-A）后的现行版本为：方法注册表 1.1.0 `sha256:aaa8361e…435ffd`、目标集 v1.1.0 `sha256:d2c1338d…a54386`、包络绑定 v1.1.0 `sha256:9fb4908c…6488ad`、S4 verdict v1.1.0 `sha256:43506f54…0c28509`。四行 verdict 与判定谓词未变。
>
> **输入版本更新（2026-11-12 第 2 批，ADR-TS-CON-01b）**：目标集 v1.2.0 `sha256:7a37e340…fa2990`、包络绑定 v1.2.0 `sha256:3bfb3f89…0fc6ac`、S4 verdict v1.2.0 `sha256:11e82e3f…0f76ae`。G-CON-01 拆为 G-CON-01a（硬）＋ G-CON-01b（软）；判定谓词仍 pass。

## 5 代价量化清单（6.2.4 Q4：有代价可达必入 ADR）

| 目标 | 代入值 | 目标界 | 余量 | 代价项 |
|---|---|---|---|---|
| G-LAT-01 延迟 | 450 ms | ≤ 500 ms | 50 ms | 三段各 150 ms 的 P99 预算上界（预算分配，非实测） |
| G-AVL-01 可用性 | 99.5%（上界） | ≥ 99.0% | 0.5 pp | 单机可用性预算 99.5%（自定） |
| G-LT-01 变更前置时间 | 0.5 工作日 | ≤ 1 工作日 | 0.5 工作日 | 单可部署单元 0.5 工作日（自定） |
| G-CON-01a 数据一致性（单库） | 单线程单写者，读己之写成立 | 单库强一致 | 结构性成立 | 无额外代价（结构事实） |

四条硬目标均为 `reachable_with_cost`，已在 `s4-verdict-pact-dsh.yaml` 的 `cost_ledger_ref` 指回本节。**G-CON-01b（跨服务 ≤5 s）已于第 2 批按 0.4 降为软目标**，不参与 S4 判定，其保守假设见 `ADR-TS-CON-01b.md`。

**可推翻指标**：
- 任一段实测 P99 > 150 ms → G-LAT-01 binding 失效；
- 出现第二个独立故障域（远端 backend）→ G-AVL-01 必须按 Π 重算；
- 变更需跨单元协同发布 → G-LT-01 按 max 重算；
- 引入远端 backend 或第二写者 → G-CON-01 无包络可依。

## 6 影响分级（7.2.2）

- `impact_scope = {2, 6, 10}`：STY-001 的 `constraints_imposed` 明确施加到方面 2（分解候选集收窄）、方面 6（envelope = 质量目标可达性上界）、方面 10（投影视图必须表达所选风格）。
- `reversibility = costly`：`typical_reversibility: costly`，上下文无覆写证据。
- 分级：`|impact_scope| = 3 > 1` → **高影响** → 完整 ADR + 批准。ADR 即本文件；批准见头部。

## 7 10.2.5 接地状态（决定决策记录状态）

本轮 10.2.5 六判据结果见 `10.2.5-verdict-pact-dsh.yaml`：**3 pass / 3 fail**（判据三、五、六 pass；判据一、二、四 fail）。

> 判据五、六已于 2026-11-12 第三轮按人类批准补齐（评审点五触发点、P0 的 `deadline=2026-12-31`）。判据六的 pass **只代表声明完整，不代表 P0 响应能力存在**。判据五的点一是追溯评审：本 ADR 已于 2026-11-12 批准，"批准前"时序未满足，不得记为时序合规。

按母本 10.2.5 末段：「未过验收判据而开始产出设计决策 = 框架未接地运行，其产出决策全部标 `provisional`」。故本决策记录：

- 已获 `wgz` 按批准角色注册表批准（S6(ii) 成立、S6(v) 解除）；
- 但因 10.2.5 未过，状态由 `approved` 转 `provisional`（SM-DR `* → provisional`，trigger `grounding_fail`，权限 system）；
- 下游消费限制：只许软约束消费，消费处须附张力承认 ADR（7.2.5）；不得创造不可逆事实。

## 8 治理风险

- `GOV-PACT-001`：批准链为空。主批准人不可用时，升级链立即穷尽，构成批准不可达；`reversibility=costly` 下只许阻塞等待。当前不构成阻塞——批准已实际取得。
- 接地未完成（10.2.5 3/6）：剩余未闭合项是判据一（白板模式版本号无定义）、判据二（注册表 2/5）、判据四（FVR 5/39）。判据五、六已在本轮闭合记录层面的缺口，但判据五的评审时序欠账与判据六的 P0 能力缺口仍然存在。

## 9 本轮登记的决策点（不改母本）

| ID | 决策点 | 本轮处置 |
|---|---|---|
| D-12 | 目标集无正式 schema/注册表落点（S4 要输入，五注册表不含它） | 落在 pilot 文件 `target-set-pact-dsh.yaml`，标 `[自定]` |
| D-13 | 0.5.1 要求声明批准角色注册表，但无文件/字段 schema | 按 registry 辅助注册表惯例自建 `approval_registry.yaml`，标 `[自定]` |
| D-14 | STY-001 用同一 `path` 承载延迟求和与可用性乘积，分解粒度未定义 | **已闭合（D-14-A）**：条目拆 `path_lat`/`path_f`，注册表 1.1.0／MJ-30 |
| D-15 | 可用性统计窗口与计划内维护口径未指定 | **已闭合（D-15-A）**：自然月窗口、探针判据、维护口径写入目标集 v1.1.0 |
| D-16 | 判据六 `undetermined` 的 `deadline` 无可绑定日期 | 本轮按人类批准填 `2026-12-31`；「无生产排期」事实未消除，母本未规定 deadline 数据类型 |
| D-17 | 判据五评审点排期无 `scheduled(rp)` schema | 五点触发点已补（`2026-11-19`＋季度 `2026-12-31`）；字段形态仍为本轮部署级约定 |
| D-18 | S4 三值 verdict 无 `n/a` | **已闭合（D-18-B）**：不改值域，用 0.4 把跨服务子句降为软目标（G-CON-01b） |
| D-19 | STY-001 envelope 无一致性 metric | G-CON-01 判定标 `[自定]` 外推 |
| D-20 | 0.5.1 未规定备选批准链是否允许为空 | 按"已声明空链、穷尽即不可达"执行，记 `GOV-PACT-002` |
| D-21 | 上界式包络下 `reachable_with_cost` 只能读作"未被反驳" | 已在 S4 逐行加 `proof_strength` 注解（D-21-B）；母本语义澄清待第 3 批（D-21-A） |

## 10 结论三元组

- S4 判定谓词：`pass`（STY-001 对 4 个硬目标均 `reachable_with_cost`）
- S6(ii)：`pass`（完整 ADR + 批准；批准人 `wgz`，2026-11-12T21:29:21+08:00）
- S6(v)：`解除`（批准可达；`GOV-PACT-001` 仍为已知风险）
- 决策记录状态：`provisional`（接地未过，10.2.5 3/6；判据一/二/四仍 fail）
