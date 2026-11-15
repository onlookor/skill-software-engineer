# 草案 D-16：生产排期登记（模板已落盘，六项事实待补）

> 性质：登记模板已落盘 `registry/production_schedule.yaml`（status=pending），**六项排期事实仍待人类提供**。
> 授权属性：排期事实只能由人类责任方提供；agent 不代填、不推测、不用决策日期冒充排期日期。
> 本轮不改母本；模板中 `declared_by` 为 null，未写 agent。

## 1 缺口是什么

`10.2.5-verdict-pact-dsh.yaml` 判据六的 `p0_response` 维度为 `undetermined`：

| 字段 | 现值 | 说明 |
|---|---|---|
| `state` | `undetermined` | 仓库无值班表、无 pager/on-call、无告警通道 |
| `conversion_event` | `首次生产部署前` | 母本 10.2.5 判据六指定 |
| `deadline` | `2026-12-31` | **决策日期，不是排期日期**（`deadline_basis` 已如实标注） |
| `deadline_basis` | `人类用户 user 于 2026-11-12 批准推荐值；不等于生产排期` | 同上 |

**D-16 的实质**：本部署**没有生产排期这一事实**。判据六之所以仍判 `pass`，依据是 2026-11-08 R7-11 的口径——判据六只判「声明完整＋转换期限在案」，不判能力存在。因此 D-16 不是判据造假，而是**事实缺口**：转换事件 `首次生产部署前` 没有可绑定的具体时点。

## 2 缺失事实清单（需人类逐项填）

| # | 事实 | 为什么必须由人类给 | 缺失后果 |
|---|---|---|---|
| M-1 | 首次生产部署的**日期**（或「本阶段不部署」的明示结论） | Agent 无法观测未发生的部署 | `conversion_event` 无法落到时点；2026-12-31 到期只能按「未转」处理 |
| M-2 | 部署**环境**（本机 / 内网 / 云；是否含 npm 公网发布） | 属于外部条件与授权范围 | P0 响应能力判定面无法确定 |
| M-3 | 部署**形态**（单写入方 / 多写入方） | 决定 #9 并发协议是否触发（编译规范 11.4） | #9 的触发时点无法预判 |
| M-4 | P0 响应的**责任人**（值班人或单人明示） | 批准角色注册表只有 `user`，值班责任未声明 | `p0_response` 无法由 `undetermined` 转 `confirmed_present` |
| M-5 | P0 响应的**通道与时限**（告警去向、确认 SLA） | 属于组织事实 | 同上；`confirmed_absent` 将按 9.3 判部署形态可行性缺陷 |
| M-6 | 回滚窗口与回滚责任人 | 与 `DEP-PACT-DSH-01`（npm 发补丁版回退）配套 | P0 响应声明不完整 |

## 3 登记模板（供人类填写；**本轮不落盘为注册表实例**）

建议落点：`registry/production_schedule.yaml`（新文件），或并入 `registry/approval_registry.yaml` 的 `deployments` 节点。二者都需人类确认落点后再写。

```yaml
meta:
  law_file: ../软件工程元框架成文法.md
  obligation_anchor:
    source_type: clause_id
    value: "10.2.5-6"      # 判据六：conversion_event＝首次生产部署前
    quote: "P0 响应＝首次生产部署前；到期未转 → 强制转 confirmed_absent"
    verified: true
  schema_status: schema-only      # 尚未有实例，直到人类填写
  instance_state: none

entries:
  - deployment: "pact-dsh"
    first_production_deployment:
      date: null                  # M-1；null = 人类尚未给出，不得以 2026-12-31 顶替
      decision: null              # "deploy" | "not_in_scope"（人类明示结论）
      environment: null           # M-2
      deployment_shape: null      # M-3: "single_writer" | "multi_writer"
      release_mechanism: "npm publish（release.yml tag+OIDC）＋ cordis.patch.yml"
      rollback_window: null       # M-6
      rollback_owner: null        # M-6
    p0_response:
      on_call_owner: null         # M-4
      alert_channel: null         # M-5
      pager: null                 # M-5
      ack_sla: null               # M-5
      state: "undetermined"       # 人类填完后按 10.2.5 改 confirmed_present / confirmed_absent
    declared_by: null             # 必须是人类本人，不得写 agent
    declared_at: null
    source: null                  # 例："人类用户 user 于 YYYY-MM-DD 书面确认"
```

## 4 填完之后会发生什么（后果映射，非本次执行）

| 人类填写结果 | 10.2.5 判据六 `p0_response` | 连带 |
|---|---|---|
| 给出日期＋值班人＋通道 | 可转 `confirmed_present`，需 `confirmed_by`/`confirmed_at` | 判据六 `pass` 从「声明完整」升级为「能力声明存在」 |
| 明示「本阶段不部署」 | 仍 `undetermined` 但 `conversion_event` 可改为「决定部署时」 | 需人类确认是否仍算声明完整 |
| 2026-12-31 到期仍空白 | 强制转 `confirmed_absent` | 按 9.3 判部署形态可行性缺陷；判据六仍需如实登记 |

## 5 与其它四项的接口

- **#9 并发协议**：M-3 是触发条件（第一个多写入方部署决策）。M-3 未定 → #9 不启动。
- **判据五 RP-4**：`2026-12-31` 是发布节点的兜底日期；M-1 给出后应以真实发布节点替换。
- **D-17**：scheduled(rp) 的 schema 与「责任人」字段归属（见 `draft-D17-scheduled-schema-R2-20261115.md`），与本项 M-4/M-6 共用「责任人」概念，但一个是评审点责任人、一个是 P0 值班责任人，不合并。

## 6 待签

| 编号 | 待签内容 | 授权方 | 备注 |
|---|---|---|---|
| S-D16-1 | M-1～M-6 六项事实 | 人类责任方 | agent 不代填 |
| S-D16-2 | 登记落点（新文件 vs 并入 approval_registry） | 人类责任方 | 影响后续 `--check` 口径 |
