# D-16 生产排期填报说明（M-1～M-6）

> 对象：[registry/production_schedule.yaml](production_schedule.yaml) 的 `entries[0]`（deployment: pact-dsh）。
> 用途：供人类责任方逐项填写 M-1～M-6。**本说明不提供默认值、不提供推荐值、不代填任何一项。**
> 约定：YAML 中 `null` 一律表示「未回答」，不是「无」或「不适用」；「无」「不适用」「本阶段不做」必须显式写出。

## 0 填写纪律

1. **只由人类填写**：`declared_by` 必须是人名，`declared_at` 为填写时间；agent 不充当声明人。
2. **不得用决策日期顶替排期日期**：`2026-12-31` 是判据六的转换期限（决策日期），不是部署日期。
3. **部分填写时保持 `status: pending`**：六项未齐不得改 `confirmed_present`；`missing` 列表只删除已填项。
4. **填写后自检**：文件须能被 YAML 解析；`first_production_deployment` 与 `p0_response` 的字段名不得改动；`trigger` 等日期统一 `YYYY-MM-DD`。
5. **当前无自动检查器读取本文件**：消费方是 10.2.5 判据六的人工裁定与后续排期规划。不要把它当成已被机械校验的字段。

---

## M-1 首次生产部署日期

**定义**
回答：pact-dsh 第一次面向真实使用者的生产部署发生在哪一天？边界：
- 「已承诺的排期日」算答；「希望/预计/尽快」不算。
- 仓库内发布（npm 发包但无人使用）不等于生产部署；若发布即生产，必须明说。
- 「本阶段不部署」是合法答案，但必须显式写 `decision: not_in_scope`，并给一个复核日期。

**格式／取值范围**
- `date: "YYYY-MM-DD"`（Asia/Shanghai）＋ `decision: "deploy"`；或
- `decision: "not_in_scope"`（不填 `date`），并给出复核日期：写入条目的 `source`（自由文本，例 `"本阶段不部署；复核日 2027-01-31"`），或先改 `entry_fields` 增补 `review_at` 再填。
- 不允许空字符串；未答时 `date`／`decision` 均保持 `null`。

**谁消费它**
- 10.2.5 判据六 `p0_response.conversion_event`（「首次生产部署前」）的具体时点。
- [10.2.5-verdict](pilot/vertical-slice-20261112/10.2.5-verdict-pact-dsh.yaml) 判据六 `deadline`／`deadline_basis` 的替换依据（现为决策日期 2026-12-31）。
- 评审点 RP-4（验证计划评审，现 `fallback: true`）的兜底日期替换。
- 编译规范 11.4 #9 的**完成期限**（仅当 M-3=`multi_writer` 时有效；#9 的触发事件由 M-3 决定，不由 M-1 决定）。
- **未填时保持 pending 的项**：`production_schedule.yaml` 的 `status` 保持 `pending`、`missing` 保留 M-1；判据六 `p0_response` 维度不得转 `confirmed_present`。

**缺失的具体后果**
- `p0_response` 永久停在 `undetermined`；到 2026-12-31 仍空 → 强制转 `confirmed_absent`，按 9.3 判部署形态可行性缺陷。
- RP-4 只能继续用「兜底日期」，无法换成真实发布节点。
- #9 只能写「待部署决策」，无法排入任何批次。

**示例答案（虚构，不是建议值）**
```yaml
first_production_deployment:
  date: "2027-04-01"
  decision: "deploy"
```
或
```yaml
first_production_deployment:
  decision: "not_in_scope"
source: "本阶段不部署；复核日 2027-01-31"
```

---

## M-2 部署环境

**定义**
回答：首次生产部署运行在哪里、谁能访问、通过什么通道交付。边界：
- 「CI 通过」不是环境；「staging」不是生产（除非明说 staging 即生产）。
- 仅本机运行也是合法答案，但必须写明「仅本机可达」。
- 需同时说明是否包含 npm 公网发布（公网发布本身可能构成生产暴露面）。

**格式／取值范围**
写成 `<运行位置>｜<可达范围>`；两段都不可省。
- 运行位置：本机／内网主机／云主机／容器平台（写明具体形态即可，不限定枚举；仅本机也是合法答案）。
- 可达范围：仅本机／内网／公网；若公网可达，必须写明暴露面（包、端口、端点）。
- 发布通道不在本字段重复：它由同条目的独立字段 `release_mechanism` 承载（现有值 `npm publish（release.yml tag+OIDC）＋ cordis.patch.yml`）。填报时须核对它与事实是否一致，不一致一并更正。

**谁消费它**
- 判据六 `p0_response` 的可行性判断（告警通道是否可达）。
- 部署形态与回滚方案（M-6）的前提。
- #9 的写入方分析（环境是否允许多写入方）。
- **未填时保持 pending 的项**：`production_schedule.yaml` 的 `status` 保持 `pending`、`missing` 保留 M-2；判据六 `p0_response` 维度不得转 `confirmed_present`。

**缺失的具体后果**
- P0 响应只能记「声明完整」，不能判「能力存在」；告警通道是否可达无法核。
- 回滚窗口写得再具体也无法验证（不知道回到哪里）。
- 若环境含公网暴露，缺失会漏掉外部强加约束的登记。
- 9.3 部署形态可行性勘察缺少落点，无法判断该部署是否需要额外约束。

**示例答案（虚构，不是建议值）**
```yaml
environment: "本机容器｜仅本机可达"
```

---

## M-3 写入方形态（**六项中唯一有跨制度连带效应的一项**）

**定义**
回答：生产运行时，能否有**两个及以上独立写入方**同时写 PACT 状态（条目、白板、注册表投影）？边界：
- 「多个用户」不等于多写入方——若应用把写入串行化，仍是 `single_writer`。
- 单进程内的异步并发，只要不并发修改同一不变量，按 `single_writer` 计。
- 只读副本、只读观察者不计入写入方。
- 多写入方包括：多 agent 实例、人工与 agent 同时写、多个服务实例写同一状态。

**格式／取值范围**
- `deployment_shape: "single_writer"` 或 `"multi_writer"`，二者只能取一个。
- 判定依据（写入方数量、共享对象、为何串行化仍算单写）写入条目的 `source`（自由文本）；如需独立字段，先改 `entry_fields` 增补 `writer_count`／`shared_state`。
- 不接受 `null` 之外的模糊值（如「可能」「看情况」）；无法判断就保持 `null`，并在 `source` 写明待查事项。

**谁消费它**
- **编译规范 11.4 #9 并发协议的唯一触发条件**：`multi_writer` → #9 由「条件触发」转为「部署前阻塞」。
- 母本 0.21.5 五条并发不变式的适用性。
- 判据六的部署可行性判断。
- M-1 的排期（#9 未完成不得进入多写入方生产）。
- **未填时保持 pending 的项**：`production_schedule.yaml` 的 `status` 保持 `pending`、`missing` 保留 M-3；#9 只能记「条件待定」；判据六 `p0_response` 维度不得转 `confirmed_present`。

**缺失的具体后果（这是六项里唯一的制度性后果）**
- #9 不能宣布「未触发」，只能保持「条件待定」；多写入方部署若先上线，等于绕过 11.4 的三项前置（算法实现、运行时监测接线、五不变式验证证据）。
- 白板与注册表投影的并发写入假设无法登记，后续冲突无法归因。
- M-1 的日期即使填了，也无法判断该日期前是否必须先完成 #9。

**示例答案（虚构，不是建议值）**
```yaml
first_production_deployment:
  deployment_shape: "single_writer"
source: "单进程串行写入；无并发实例（只读观察者不写入）"
```

---

## M-4 P0 响应值班责任人

**定义**
回答：P0 事件发生时，**具名的个人**负责响应。边界：
- 「团队」「后端组」不是责任人；若用团队别名，必须再给该别名的具名负责人。
- agent 不能担任值班人。
- 可以有备份人；若没有，必须显式写「无备份」，不能留空。

**格式／取值范围**
`姓名（角色）`。如需备份人，写在同一个字符串内（例 `"张三（主）/李四（备）"`）；如无备份，必须显式写「无备份」，不能留空。`p0_response` 目前无 `backup` 字段；确需独立字段，先改 `entry_fields` 再填。

**谁消费它**
- 判据六 `p0_response.state`：没有具名 owner 就不能转 `confirmed_present`。
- 9.2.1 P0 信号的响应义务。
- 8.2.7 材料性抽查（RP-3）的责任面核对。
- **未填时保持 pending 的项**：`production_schedule.yaml` 的 `status` 保持 `pending`、`missing` 保留 M-4；`p0_response.state` 保持 `undetermined`。

**缺失的具体后果**
- `p0_response` 保持 `undetermined`；判据六只能停留在「声明完整」。
- 到转换事件仍空 → `confirmed_absent`，部署可行性按缺陷处理。
- P0 信号登记后无人可派，响应义务无法履行。

**示例答案（虚构，不是建议值）**
```yaml
p0_response:
  on_call_owner: "张三（后端负责人）；无备份"
```

---

## M-5 P0 响应通道与确认 SLA

**定义**
回答：P0 告警通过什么通道到达值班人，以及多久内必须**确认收到**。边界：
- 通道是「告警去向」，不是「事后通知」；仅有文档记录不算通道。
- SLA 是**确认时限**，不是解决时限；两者不可混写。
- 若当前没有任何告警能力，必须写 `alert_channel: "none"`——这是事实，会导向 `confirmed_absent`，不得用「邮件」搪塞。

**格式／取值范围**
- `alert_channel`：`pager｜IM 群（写明群标识）｜电话｜邮件｜none` 之一，可附目标标识。
- `ack_sla`：ISO 8601 时长（如 `PT30M`）或「≤30 分钟」。
- `pager`：有则写服务名/号码；没有则写显式字符串 `"未配置"`——**不得写 `null`**（本文件 `null` 专指「未回答」，两者必须区分）。

**谁消费它**
- 判据六 `p0_response` 的「能力存在」判断。
- 9.2.1 的 P0 响应时限。
- 部署形态可行性（无人可通知 = 不可行）。
- **未填时保持 pending 的项**：`production_schedule.yaml` 的 `status` 保持 `pending`、`missing` 保留 M-5；`p0_response` 只能停在「声明完整」，不得转 `confirmed_present`。

**缺失的具体后果**
- 即使 M-4 有值班人，没有通道和 SLA 仍不能判 `confirmed_present`。
- P0 事件只能靠事后发现，响应义务无法计时。
- 与 M-2 联动：环境不可达时，通道声明会被判为不可行。

**示例答案（虚构，不是建议值）**
```yaml
p0_response:
  alert_channel: "IM 群「示例告警群」＋@值班人"
  pager: "示例 pager 服务"
  ack_sla: "PT30M"
```

---

## M-6 回滚窗口与回滚责任人

**定义**
回答：一次失败的生产发布，从发现到恢复到上一可用版本需要多久、由谁执行。边界：
- 「重新部署」不等于回滚；回滚要求上一版本产物仍可取回。
- `npm unpublish` 不是回滚；它改变的是包本身，不是运行态。
- 若没有回滚路径，必须写 `rollback_window: "none"` 并说明原因。

**格式／取值范围**
- `rollback_window`：时长或「从检测到恢复 ≤ X」；无路径写 `"none"`。
- `rollback_owner`：具名个人。
- 可另附回滚步骤说明，但只能写进已声明的字段（如 `source`）或发布手册；**不得新增 `production_schedule.yaml` 未在 `entry_fields` 声明的字段**，确需新增字段须先改 `entry_fields` 再填。

**谁消费它**
- 判据六 `p0_response` 的完整性。
- `DEP-PACT-DSH-01`（npm 发补丁版回退）的实际可执行性。
- 9.3 部署可行性（不可回滚 = 形态缺陷）。
- **未填时保持 pending 的项**：`production_schedule.yaml` 的 `status` 保持 `pending`、`missing` 保留 M-6；判据六 `p0_response` 维度不得转 `confirmed_present`。

**缺失的具体后果**
- P0 响应声明不完整；即使有值班人和通道，也无法承诺恢复时间。
- 发布事故时无指定执行人，回滚靠临场决定。
- 与 M-2 联动：环境决定回滚目标（包、容器镜像、源码目录）；环境未定时回滚动作无法写成可执行步骤。

**示例答案（虚构，不是建议值）**
```yaml
first_production_deployment:
  rollback_window: "从检测到恢复 ≤ 2 小时"
  rollback_owner: "李四（发布负责人）"
```
（`source` 可写「发布手册 §3」之类依据；该字段属条目级，不在 `first_production_deployment` 内。）

---

## 六项依赖关系

| 依赖 | 说明 |
|---|---|
| M-3 → M-1 | `multi_writer` 会把 #9 变成部署前阻塞项，可能推迟 M-1 的日期；`single_writer` 则 #9 不触发。 |
| M-3 → M-2 | 环境是否允许并发实例，决定 M-3 能否成立；两者必须一致。 |
| M-2 → M-5 | 环境的可达范围决定告警通道是否可行（仅本机 vs 公网）。 |
| M-2 → M-6 | 环境决定回滚目标与手段（源码/制品/镜像）。 |
| M-4 ↔ M-5 | 只有责任人、没有通道/SLA，仍不能判 `confirmed_present`；反之亦然。 |
| M-4 ↔ M-6 | 值班人与回滚执行人可以不同；若相同，需确认其可同时承担两职。 |
| M-1 → 全部 | M-1 是转换事件的时点；若 `not_in_scope`，其余五项转为「决定部署时再填」，但必须给复核日期。 |

**重点：M-3 是六项中唯一有跨制度连带效应的一项。**
- `single_writer`：编译规范 11.4 #9 不触发，0.21.5 五不变式在单写入方场景平凡满足。
- `multi_writer`：**部署前必须完成 #9**——算法实现、运行时监测接线、五不变式验证证据，三项缺一不可进入生产。
- M-3 未填（`null`）：#9 只能记「条件待定」，不能记「未触发」；任何多写入方上线都属于绕过 11.4。

## 填完后如何登记

1. 修改 [production_schedule.yaml](production_schedule.yaml)：填六项，删 `missing` 中对应条目。
2. 六项齐备后把 `status` 从 `pending` 改为 `confirmed_present`（若明确不部署则按 `not_in_scope` 处理），并填 `declared_by`／`declared_at`／`source`。
3. 同步 [10.2.5-verdict](pilot/vertical-slice-20261112/10.2.5-verdict-pact-dsh.yaml) 判据六的 `p0_response` 维度与 `gap_status`；若 M-3 为 `multi_writer`，同时登记 #9 触发。
4. 复跑 `python3 registry/checks/runner.py` 与 `python3 registry/scripts/project.py --check`，按既有口径报完整分布。
