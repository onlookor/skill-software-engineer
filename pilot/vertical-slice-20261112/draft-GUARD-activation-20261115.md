# 草案 ①：guard_registry 5 条 `draft → active`（已批准并执行）

> 性质：已按 9.2.2 完成「完整 ADR＋批准」：`ADR-GUARD-ACT-01`（2026-11-15，人类 user 批准）。
> 已执行：approval_registry 1.1.0→1.2.0 增「守护规则注册表变更」；guard_registry 1.0.0→1.1.0、5 条 active、GR-003 阈值、GR-004/005 日期订正。
> 未执行：产物 `.11` 重编译（另批）；母本改动；检查器改动。

## 1 待激活条目与核对结果

| rule_id | 监控谓词 | 级别 | 检测手段 | `source_adr` 现值 | 9.2.2 出处形态 | 核对结论 |
|---|---|---|---|---|---|---|
| GR-001 | `version_consistent(artifact)（E4）` | P0 | static_check | 母本 10.2.3 E4；编译规范 8.2 | **不是 ADR、不是外部强加** | 需裁定（P-1） |
| GR-002 | `no_manual_divergence(projection)（E2／F-11）` | P0 | static_check | 编译规范 E2／F-11；CHECK-SPEC C3.2 | **不是 ADR、不是外部强加** | 需裁定（P-1） |
| GR-003 | `fvr_covers_all_hard_properties(card)（10.2.5 判据四）` | P1 | static_check | 母本 10.2.4；10.2.5 判据四 | **不是 ADR、不是外部强加** | 需裁定（P-1）＋参数陈旧（P-2） |
| GR-004 | `anchor_fingerprint_stable(unit)（F-3）` | P1 | static_check | `ADR-ANCHOR-01（approved 2026-11-11）` | 是 ADR | 日期不符（P-3） |
| GR-005 | `frozen_line_anchor_drift_registered(INFO-2)` | P2 | static_check | `ADR-ANCHOR-01（approved 2026-11-11）D3` | 是 ADR | 日期不符（P-3） |

## 2 核对发现（5 项，均未自行处置）

**P-1｜GR-001/002/003 的「出处」不是 ADR。**
9.2.2 条目形态写的是「出处（该规则依据的决策 ADR 或外部强加）」。母本条款与编译规范条款既不是决策 ADR，也不是外部强加（外部强加指监管、合同、平台强制）。可选处置：
- (a) 补 3 份规则级 ADR（把「本规则据以成立」写成决策记录）；
- (b) 人类裁定「母本条款/编译规范条款可作为出处」，并在注册表头写明该解释；
- (c) 把 3 条规则合并进一份「仓库既有闸门登记」ADR，逐条给依据。
> Agent 未选。三选一需人类裁定。

**P-2｜GR-003 参数陈旧（事实错误）。**
现值 `threshold: "覆盖 39/39；当前 5/39"`。**实际已是 39/39**（`fvr-full-run-1.json`，2026-11-14）。「当前 5/39」是切片初期读数。改参属 9.2.2 注册表变更，须随 ADR 一并改，**不得静默修正**。建议新值：`"覆盖 39/39；当前 39/39（pass 39 / fail 0 / escalate 0 / vacuous 9）"`。

**P-3｜GR-004/005 的 ADR 日期不一致。**
注册表写 `approved 2026-11-11`；[ADR-ANCHOR-01](file:///home/user/projects/skills/software-engineering/adr/ADR-ANCHOR-01-approved-20261109-锚点结构地址化与行号禁用.md) 文件名与正文均为 **2026-11-09 人类责任方批准**。二者必有一处错。需更正（同样属改参/改出处，走 ADR）。

**P-4｜批准路由未登记（阻塞前置）。**
`registry/approval_registry.yaml` v1.1.0 的 5 个决策类是：风格定案、分解主策略、方法注册表变更、冲突矩阵例外覆盖、编译规程变更。**「守护规则注册表变更」不在其中**；且「方法注册表变更」的 `applies_to` 明写只覆盖 `registry/method_registry.yaml`。按 0.5.1「未声明批准角色注册表的部署，所有高影响决策一律走阻塞路径」，9.2.2 的批准在类别层面**无受理方**。
> 处置：先由人类声明第 6 个决策类（或明确扩展「方法注册表变更」的适用范围），approval_registry 升版。**这是激活的前置，不是激活本身。**

**P-5｜激活的消费后果。**
`consumption_states: [active, seed]`（编译规范 2.3(a)）——激活后规则可被编译消费。`artifact.yaml` 的 `registry_snapshot.guard_registry` 记有 `version: "1.0.0"`、`status_note: "5 条均 draft，待 9.2.2 批准"`；激活将改版本与注记 → **产物内容变，需重编译 `.11`**（18 卡版本对齐、C7 报告复跑）。母本、锚索引、`pattern_version` 均不动。

## 3 ADR 包形态（推荐＋待裁）

| 方案 | 形态 | 优点 | 缺点 |
|---|---|---|---|
| **甲（推荐）** | 1 份总 ADR ＋ 5 份逐条附录（每份含 9.2.2 的 9 字段与依据） | 一次批准完成 5 条；逐条内容仍完整 | 需要人类确认「附录是否算完整 ADR」 |
| 乙 | 5 份独立 ADR | 字面最稳 | 5 倍批准开销，内容高度同质 |
| 丙 | 1 份 ADR 只说「批量激活」 | 最省 | 无逐条依据，**不建议**（易被当作形式合规） |

推荐甲。是否采纳由人类裁定（S-GUARD-2）。

## 4 逐条激活记录模板（填好后即为 ADR 附录）

```yaml
- rule_id: GR-00X
  monitored_predicate: "…"
  level: "P0|P1|P2"
  means: "static_check|prod_monitor|periodic_survey"
  params: {…}
  obligation: "…"
  waiver_clause: "…|null"
  source_adr: "…"                    # 按 P-1 的裁定结果填写
  version: "1.0.0 → 1.1.0"
  status: "draft → active"
  adr_ref: "ADR-GUARD-ACT-01 §X"      # 待创建
  approval: {approved_by: null, approver_kind: "human", approved_at: null}   # agent 不填
```

## 5 自主完成的部分（本轮已做，只读）

| 预检项 | 结果 |
|---|---|
| GR-001 检查器 `pilot/vertical-slice-20261112/check-card.py E4` | 文件存在，`E4` 判定已产出 `match=true` |
| GR-002 检查器 `registry/scripts/project.py --check` | 文件存在，当前硬失败 0 |
| GR-003 检查器 `check-card.py F3（全量）` | 文件存在，当前 39/39 |
| GR-004/005 检查器 `registry/scripts/anchor_index.py` | 文件存在，F-1～F-10 `failures: []`、986 对 drift |
| 条目字段完整性 | 5 条 9 字段齐备（`monitored_predicate`/`level`/`means`/`params`/`obligation`/`waiver_clause`/`source_adr`/`version`/`status`） |
| 陈旧参数 | 发现 1 处（GR-003，见 P-2） |

未做：未改状态、未改版本、未写批准记录、未重编译产物。

## 6 待签

| 编号 | 待签内容 | 授权方 | 阻塞关系 |
|---|---|---|---|
| S-GUARD-1 | P-1：GR-001/002/003 的出处形态（a 补 ADR／b 裁定条款可作出处／c 合并 ADR） | 人类责任方 | 阻塞全部 5 条 |
| S-GUARD-2 | 第 3 节包形态（推荐甲） | 人类责任方 | 阻塞 ADR 起草 |
| S-GUARD-3 | P-4：声明第 6 个批准决策类（或扩展既有类） | 人类责任方 | **硬前置**：无受理方则不得激活 |
| S-GUARD-4 | P-2 参数更新（39/39） | 人类责任方 | 随 ADR 批准生效 |
| S-GUARD-5 | P-3 日期更正（2026-11-09） | 人类责任方 | 随 ADR 批准生效 |
| S-GUARD-6 | 5 条激活的最终批准 | 人类责任方 | 9.2.2；agent 不自批 |
