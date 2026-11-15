# ADR-GUARD-ACT-01：守护规则注册表 5 条激活与参数订正

| 项 | 值 |
|---|---|
| 编号 | `ADR-GUARD-ACT-01` |
| 状态 | approved |
| 批准日期 | 2026-11-15 |
| 影响级别 | 中（`registry/guard_registry.yaml` 5 条状态迁移＋版本；不改母本、不改锚索引、不改 `pattern_version`） |
| 关联条款 | 母本 9.2.2（守护规则注册表条目形态／变更＝完整 ADR＋批准）；0.5.1（批准角色注册表）；0.17.2（条目状态枚举）；编译规范 2.3(a)（draft 不可消费） |
| 关联缺口 | D-22（守护规则注册表 schema）、D-13/D-20（批准角色注册表 schema） |
| 批准来源 | 人类用户 user 于 2026-11-15 经父会话明确指示「先声明『守护规则注册表变更』这个决策类，再处理 5 条 `draft→active`。同时修正两处已查出的不一致」；agent 未自批，也未把 agent 写为批准人 |

## 1. 范围与判定依据

- **范围**：`registry/guard_registry.yaml` 的 5 条（GR-001～GR-005）由 `draft` 迁至 `active`；GR-003 参数订正；GR-004/005 的 ADR 日期订正；同批声明批准决策类「守护规则注册表变更」。
- **依据**：9.2.2「规则的新增/改级/改参＝注册表变更＝完整 ADR＋批准」；本 ADR 即该变更的决策记录，§3 每条为一份完整的规则记录（9 字段＋依据）。
- **不改**：母本、锚索引、`pattern_version`、检查器实现、任何产物版本标签。

## 2. 决策

- **D1 决策类声明**：在 `registry/approval_registry.yaml` 新增第 6 个决策类「守护规则注册表变更」，`applies_to: ["registry/guard_registry.yaml 的规则新增/改级/改参/状态迁移"]`，主批准人 user（human），备选链为空（沿用单人项目明示）。approval_registry 升版 1.1.0 → 1.2.0。
  - 理由：原 5 类中「方法注册表变更」的 `applies_to` 只覆盖 `method_registry.yaml`；按 0.5.1，未声明类别的高影响决策无受理方、须走阻塞路径。此为该路径的解除条件。
- **D2 五条激活**：GR-001～GR-005 全部 `draft → active`，`version: 1.0.0 → 1.1.0`。`consumption_states: [active, seed]` 不变；激活后规则可被编译消费。
- **D3 出处形态**：GR-001/002/003 原 `source_adr` 填的是母本/编译规范条款，不满足 9.2.2「出处＝决策 ADR 或外部强加」的字面。本 ADR 作为三条规则的决策记录（草案选项 c：合并 ADR、逐条给依据），`source_adr` 分别改为 `ADR-GUARD-ACT-01 §3.1/§3.2/§3.3`，母本条款退为「依据」列。
- **D4 GR-003 参数订正**：`params.threshold` 由 `"覆盖 39/39；当前 5/39"` 订正为 `"覆盖 39/39；当前 39/39（pass 39 / fail 0 / escalate 0 / vacuous 9）"`。旧值是切片初期读数，与 2026-11-15 全量复跑不符。
- **D5 GR-004/005 日期订正**：`source_adr` 中 `approved 2026-11-11` 订正为 `approved 2026-11-09`，与 ADR 本体一致。
- **D6 批准**：本 ADR 由人类用户 user 批准（来源见上表）。agent 只执行登记，不充当批准人。
- **D7 产物影响**：`artifact.yaml` 的 `registry_snapshot.guard_registry` 仍记 v1.0.0／5 条 draft，将随下一次 `.11` 重编译更新；本轮不重编译。
- **D8 未做**：未改母本；未改任何检查器；未改 `review_points`／`production_schedule`（另案）。

## 3. 逐条规则记录（激活后形态）

### 3.1 GR-001

| 字段 | 值 |
|---|---|
| `rule_id` | GR-001 |
| `monitored_predicate` | `version_consistent(artifact)（E4）` |
| `level` | P0 |
| `means` | static_check |
| `params` | `{check: "pilot/vertical-slice-20261112/check-card.py E4", threshold: "match == true"}` |
| `obligation` | 拒绝装配 + 触发重编译（E4 失败路由） |
| `waiver_clause` | null |
| `source_adr` | `ADR-GUARD-ACT-01 §3.1`（依据：母本 10.2.3 E4；编译规范 8.2） |
| `version` | 1.1.0 |
| `status` | active |

### 3.2 GR-002

| 字段 | 值 |
|---|---|
| `rule_id` | GR-002 |
| `monitored_predicate` | `no_manual_divergence(projection)（E2／F-11）` |
| `level` | P0 |
| `means` | static_check |
| `params` | `{check: "registry/scripts/project.py --check（F-11）", threshold: "hard_fail == 0"}` |
| `obligation` | 投影重生成或按 `file_bulk` 声明变更；不得手工改投影 |
| `waiver_clause` | `F-11 --expected-changes` 的 waiver 字段（须 ADR 或可解析 commit） |
| `source_adr` | `ADR-GUARD-ACT-01 §3.2`（依据：编译规范 E2／F-11；CHECK-SPEC C3.2） |
| `version` | 1.1.0 |
| `status` | active |

### 3.3 GR-003

| 字段 | 值 |
|---|---|
| `rule_id` | GR-003 |
| `monitored_predicate` | `fvr_covers_all_hard_properties(card)（10.2.5 判据四）` |
| `level` | P1 |
| `means` | static_check |
| `params` | `{check: "check-card.py F3（全量口径）", threshold: "覆盖 39/39；当前 39/39（pass 39 / fail 0 / escalate 0 / vacuous 9）"}` |
| `obligation` | 限期整改；逾期升 P0（9.2.1） |
| `waiver_clause` | 切片口径不是规范判据，不得作为豁免依据 |
| `source_adr` | `ADR-GUARD-ACT-01 §3.3`（依据：母本 10.2.4；10.2.5 判据四） |
| `version` | 1.1.0 |
| `status` | active |

### 3.4 GR-004

| 字段 | 值 |
|---|---|
| `rule_id` | GR-004 |
| `monitored_predicate` | `anchor_fingerprint_stable(unit)（F-3）` |
| `level` | P1 |
| `means` | static_check |
| `params` | `{check: "registry/scripts/anchor_index.py（F-3）", threshold: "failures == 0"}` |
| `obligation` | 拒改结构地址；按 ADR-ANCHOR-01 处置漂移 |
| `waiver_clause` | null |
| `source_adr` | `ADR-ANCHOR-01（approved 2026-11-09）` |
| `version` | 1.1.0 |
| `status` | active |

### 3.5 GR-005

| 字段 | 值 |
|---|---|
| `rule_id` | GR-005 |
| `monitored_predicate` | `frozen_line_anchor_drift_registered(INFO-2)` |
| `level` | P2 |
| `means` | static_check |
| `params` | `{check: "anchor_index.py INFO-2（快照比对）", threshold: "漂移只登记不追（ADR-ANCHOR-01 D3）", trend_window: {metric: count, value: 10, configurable: true}}` |
| `obligation` | 记录 + 趋势观察（默认按次数，趋势窗口可配置） |
| `waiver_clause` | null |
| `source_adr` | `ADR-ANCHOR-01（approved 2026-11-09）D3` |
| `version` | 1.1.0 |
| `status` | active |

## 4. 批准与执行记录

| 项 | 值 |
|---|---|
| 批准人 | user（human） |
| 批准日期 | 2026-11-15 |
| 批准依据 | 人类用户经父会话明确指示（见首表「批准来源」） |
| 执行者 | agent（仅登记，非批准人） |
| 执行内容 | approval_registry 1.1.0→1.2.0 增决策类；guard_registry 1.0.0→1.1.0、5 条 draft→active、GR-003 参数、GR-004/005 日期 |
| F-11 声明 | `registry/projections/STY.md`、`勘察义务清单.md`、`索引.md` 各 1 行变更（ADR 计数 35→36 引起），`file_bulk` waiver＝ADR-GUARD-ACT-01；`project.py --check` 硬失败 0 |
| 未执行 | 产物重编译（`.11`）、母本改动、检查器改动 |

## 5. 残余解释点（供人类复核，不阻塞本次登记）

- 9.2.2 的「完整 ADR」是否允许一份 ADR 承载 5 条规则（每条含完整 9 字段）。本 ADR 按草案推荐的「甲」执行；若人类要求一条一 ADR，可拆分而不改已生效的状态。
- GR-001/002/003 的出处由「条款」改为「本 ADR」是否满足 9.2.2 的「出处」语义。本 ADR 的判断是满足（决策记录存在且被批准），但不代替人类解释。
