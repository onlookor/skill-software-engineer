# ADR-GUARD-02：GR-005 趋势窗改为无值声明，G7 改判声明形态

| 项 | 值 |
|---|---|
| 编号 | `ADR-GUARD-02` |
| 状态 | approved |
| 批准日期 | 2026-11-15 |
| 影响级别 | 中（`registry/guard_registry.yaml` GR-005 改参＋版本 1.1.0→1.2.0；`registry/checks/g.py` G7 判据形态变更；白板 `p2_signals` 去值；产物重编译为 `pilot-20261112.13`。不改母本、不改锚索引、不改 `pattern_version`） |
| 关联条款 | 母本 9.2.2（规则改参＝注册表变更＝完整 ADR＋批准）；0.5.1（批准角色注册表）；0.17.2（条目状态枚举）；9.5 G7（P2 信号告警 → threshold ∧ trend_window 双判据成立） |
| 批准决策类 | 批准注册表第 6 类「守护规则注册表变更」（`applies_to` 含改参）；主批准人 user（human）；备选链为空 |
| 批准来源 | 人类用户 user 于 2026-11-15 经父会话明确裁定：「选 B，`guard_registry` 升 1.2.0，并重编译为 `.13`」；agent 未自批，也未把 agent 写为批准人 |

## 1. 范围与判定依据

- **范围**：`registry/guard_registry.yaml` 的 GR-005 `params.trend_window`；`registry/checks/g.py` 的 G7 判据；白板 `domain_data.p2_signals` 的 GR-005 实例；`pilot-20261112.13` 重编译。
- **依据**：人类对「技能配置」的硬界定——技能配置是运行时产物，是运用到具体项目时由 agent 与项目用户约定的，不是编译期决定的值；编译期只能声明可配置项，不得给默认值／示例值／推荐值；未约定即 `cannot_evaluate`。
- **前状态**：`trend_window: {metric: count, value: 10, configurable: true}` —— 编译期写死值 `10`，属该界定要禁的形态（`翻新方案-对照project-management-20261115.md` §6.6.2 已登记为待裁项）。
- **不改**：母本、锚索引、`pattern_version`、GR-001～GR-004、`p2_signals` 条目数量。

## 2. 决策

- **D1 无值声明**：GR-005 `params.trend_window` 只保留可配置项声明，删除 `value: 10` 与 `configurable` 标志，不保留任何默认值、示例值、推荐值：
  - `metric`：`type: "enum: count|time"`、`values: [count, time]`、`required: true`、`unconfigured: "cannot_evaluate"`、`unit_note: "count＝次数；time＝天"`；
  - `value`：`type: number`、`range: ">= 1"`、`required: true`、`unconfigured: "cannot_evaluate"`。
  - 值的产生时机只有一个：挂载期由 agent 与项目用户约定，并留配置快照指纹；编译期产物不承载值。
- **D2 版本**：`registry_version` 1.1.0→1.2.0；GR-005 `version` 1.1.0→1.2.0，`status` 仍为 `active`（改参不改级）。
- **D3 G7 改判形态**：`registry/checks/g.py` 的 G7 由「校验 `value > 0`」改为「校验 `trend_window` 的声明形态」——`metric` 须声明为 `count|time` 枚举、`value` 须声明为 `number` 且带非空 `range`，两者均须声明 `unconfigured: cannot_evaluate`。**值不参与判定**：直接给数值不构成声明，给出数值时也不据此改判。`g7` 的 pass 记「形态判据」并自带弱判据标签。
- **D4 白板去值、保留条目**：`p2_signals` 保留 GR-005 条目本身，删除 `value: 10`，改为与注册表同形的无值声明，并置 `value_state: "not_agreed"`（值未约定 → `cannot_evaluate`）。**不删空 `p2_signals`**：显式空集会走「pass ＋ vacuous」，属洗白。
- **D5 重编译 `.13`**：`artifact.yaml` 的 `registry_snapshot.guard_registry` 升 1.2.0 并重算 `sha256`（旧的 `de732c36…` 已成伪记录）；18 张卡 `artifact_version` 对齐 `.13`；白板 `SM-CA` 记 `.12 → stale → .13 valid`；C7 与判据二／三证据同步。`release.artifact_version` 仍指 `.10`，不予改动。
- **D6 弱判据标签入证据**：G7 现为形态判据，判定「可配置项是否被正确声明」，**不代表趋势检测已实现**，也**不构成对任何运行时窗口取值的验证**。该标签同时写入 `10.2.5-verdict` 判据二／判据四的 `evidence`/`caveat`，不只留在方案文档。
- **D7 批准记录**：属批准注册表第 6 类「守护规则注册表变更」的第二个适用实例（首个为 ADR-GUARD-ACT-01）；在 `approval_registry.yaml` 该类 `note` 中登记实例并升 patch 到 1.2.1。
- **D8 未做**：未改母本；未改锚索引与 `pattern_version`；未新增或删除任何守护规则；未发布（对外发布仍需人类单独指令）。

## 3. GR-005 改后形态

| 字段 | 值 |
|---|---|
| `rule_id` | GR-005 |
| `monitored_predicate` | `frozen_line_anchor_drift_registered(INFO-2)` |
| `level` | P2 |
| `means` | static_check |
| `params.check` | `anchor_index.py INFO-2（快照比对）` |
| `params.threshold` | `漂移只登记不追（ADR-ANCHOR-01 D3）` |
| `params.trend_window` | `{metric: {type: "enum: count\|time", values: [count, time], required: true, unconfigured: cannot_evaluate, unit_note: "count＝次数；time＝天"}, value: {type: number, range: ">= 1", required: true, unconfigured: cannot_evaluate}}`（**无值**） |
| `obligation` | 记录 + 趋势观察（窗口参数于挂载期约定；未约定即不可判） |
| `waiver_clause` | null |
| `source_adr` | `ADR-ANCHOR-01（approved 2026-11-09）D3；ADR-GUARD-02（approved 2026-11-15）D1/D2` |
| `version` | 1.2.0 |
| `status` | active |

## 4. 批准与执行记录

| 项 | 值 |
|---|---|
| 批准人 | user（human） |
| 批准日期 | 2026-11-15 |
| 批准依据 | 人类用户经父会话明确裁定（见首表「批准来源」） |
| 执行者 | agent（仅执行登记与改动，非批准人） |
| 执行内容 | guard_registry 1.1.0→1.2.0（GR-005 无值声明）；`g.py` G7 改形态判据；白板去值；approval_registry 1.2.0→1.2.1（实例登记）；重编译 `.13` |
| 复跑 | `runner`（39 条）、`project.py --check`、判据一、`check-card.py --all`、C7 |
| 未执行 | 母本改动；锚索引改动；对外发布；git 推送 |

## 5. 残余解释点（供人类复核，不阻塞本次登记）

- **「项名」是否允许改动**：本轮沿用既有项名 `metric` / `value`，未把 `value` 改名为 `window_length`。代价是同一字段名在「声明」与「实例值」两种形态下出现，读者需靠值形态区分；收益是不引入字段改名带来的额外迁移。若人类认为应改名，另行裁定。
- **`unconfigured: cannot_evaluate` 的落地语义**：当前 `g7` 只校验该声明存在，不校验「未约定时上游确实不判」。真正的运行时行为由挂载期实现承担，本仓无可执行载体，故未做端到端验证。
- **白板 `value_state` 字段**：`not_agreed` 是本轮新增的部署级状态字段，母本与 9.2.2 均无此字段；若人类要求白板字段与母本严格同形，可移除该字段（声明形态本身已足以表达「未约定」）。
