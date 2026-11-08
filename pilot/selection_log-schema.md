# 选型日志最小 schema（试跑模板，draft）

- 性质：**试跑模板，不是规范**。不新增母本义务、不改注册表数据、不新增 `gaps`。
- 状态：**draft**（未批准；试跑后按反馈修订）
- 上游依据：0.18 S0–S6（选型规程）、0.18.2 S1（applicability 求值）、0.18.6 M15（unknown → 候选保留＋勘察义务）、0.17.7 门槛 2（无出处阈值禁填）、0.4 条件 3（硬约束须有出处）
- 设计目标：**填得下去**。核心字段只留 7 个，其余可选；一条记录默认一屏填完。字段每多一个，实际填写率就降一截。

## 1. 最小记录（核心 7 字段）

```yaml
selection_id: SEL-20261108-01        # 一次选型一个 ID；同日多选型顺延 -02
decided_at: 2026-11-08T17:26:10+08:00  # ISO8601；决策当场打点，事后补记须标 retrospective
decided_by: <见 §1.2 值域>            # named / unregistered / unknown 三态，禁占位词
decision: <一句话，动词开头：选了什么>   # 不写背景，背景在 ADR
adr_ref: <ADR 编号或路径>              # 决策叙述与后果的唯一归属地
candidates: [...]                     # 见 §2
facts: [...]                          # 见 §3；只填候选实际消费的事实
```

**不设的字段（默认不填，防膨胀）**：会议地点、参与人全名单、评分权重、备选方案详述、风险登记、后续行动项。这些留在 ADR 或项目工具里。

## 1.1 三种「没有值」：`null` / `unknown` / 留空（F2 基础）

任何字段「没有值」，必须落到下列三档之一。混用是试跑中最常见的记录腐化源。

| 档 | 写法 | 含义 | 附带义务 |
|---|---|---|---|
| 不适用 | `null` ＋ `not_applicable_reason: <一句>` | 本次记录本就不该有此值（如 `selected` 候选没有 `rejection_reason`） | 必须写一句「为什么不适用」 |
| 未知 | `unknown` | **本应有值、当前取不到**（0.18.6 M15） | 必须同时产生 `open_obligations` 一条，候选不得沉默排除 |
| 遗漏 | **禁止**（字段不写） | 该填而未填 | 评审直接打回，不进入求值 |

判据顺序：先问「本次该不该有值」——该有而拿不到 → `unknown`；不该有 → `null` ＋理由。禁止用 `false`／`无`／`N/A`／`待定` 冒充 `unknown`。

## 1.2 `deployment_instance` 与 `decided_by` 值域（F2）

试跑发现：本仓没有 0.5 @129 意义上的**部署实例**（批准角色注册表），按严格读法高影响决策应整体阻塞。schema 不给「假装有」的办法，只给**可记录的不合规**：

```yaml
deployment_instance:
  status: declared | absent
  roster_ref: <批准角色注册表 ID／路径> | null    # declared 时必填
approval_status: approved | provisional          # 条件字段：absent 时只能是 provisional
```

`decided_by` 三态值域：

| 值 | 何时用 | 写法 |
|---|---|---|
| `named` | `deployment_instance.status=declared` | `{role: <角色名>, name: <姓名>, roster_ref: <注册表ID>}` |
| `unregistered` | 有真实责任人但无注册表实例 | `{name: <姓名>, roster_ref: null}` ＋ 一条 `open_obligations`（补部署实例声明） |
| `unknown` | 决策当场无人可署 | 字面 `unknown` ＋ 一条 `open_obligations`（升级到可署人） |

规则（三条，均为**硬约定**，不是建议）：
1. **`absent` 时不得编造批准链**：`roster_ref` 留 `null`，不得写「架构组 → CTO」这类看起来有序但无出处的链。
2. **禁止占位词充数**：`领导`／`架构组`／`按公司流程`／`相关方` 不是批准人，出现即判为凭空填写，评审打回。
3. **`absent` 不等于记录无效**：允许记录，但 `approval_status` 固定 `provisional`，且必须在 ADR 里写明「待补部署实例后追认」，否则视为绕过 0.5。

## 2. `candidates`（每条候选 4 字段）

```yaml
candidates:
  - id: C1
    statement: <候选一句话>
    verdict: selected | rejected | deferred
    rejection_reason: <仅 rejected：哪条事实/判断不支持它，一句话>
```

规则：
- `deferred` 只用于「缺事实、按 M15 保留候选」，必须同时产生一条 `open_obligations`。
- `rejected` 必须给理由，且理由要能指回 `facts` 或 `assessments` 的条目；「感觉不好」不接受。

## 3. `facts`（三值求值，每条 5 字段）

```yaml
facts:
  - slot_ref: <entry_id>/<field>[/<序号>]   # 例：STY-001/applicability.current_space/2
    statement: <事实一句话，可判真假>
    value: true | false | unknown           # 三值；禁止二值化
    source: <出处>                           # 0.4：可定位到文档+条款/行/记录ID
    note: <unknown 的处置，或求值说明>
```

规则（每条都来自试跑的真实教训）：
1. **三值**：`unknown` 不得写成 `false`；`unknown` 的候选一律保留（M15），并登记 `open_obligations`，禁沉默排除。
2. **有出处才进 `facts`**：无出处的说法进 `open_obligations`，对应字段保持 `[待勘察]`；不得用「方向性陈述」冒充事实。
3. **判断不进 `facts`**：凡带「会／应当／更好／风险大」的句子是判断，不是事实，见 §4。混进来会让记录看似客观、实则夹带结论（试跑 F3）。
4. **只填候选消费的事实**：未进候选集的条目不逐槽填（全量 applicability 762 项按每条 1 分钟≈12 小时，不可行；必须先 S1 裁剪）。
5. `slot_ref` 的序号目前只能按「条目＋字段＋出现序」拼——**这是临时办法**，必须同时登记 §3.1 的 `slot_registry`；只写裸序号、无锚文本的记录不可复核。

## 3.1 方括号槽的临时代号与登记去向（F1）

母本 0.17.2 没有槽位编号字段，检查器也不产出。因此 `slot_ref` 里的「序号」是临时办法，按下列规则收敛到一张可复核的表。

**编法**：`SLOT-<entry_id>-<field>-<n>`
- `<field>` 取字段路径末段：`problem_space`／`current_space`／`delivery_space`／`detection_predicate`／`bound_expr`。
- `<n>` = 该字段**当前文本**中从左到右第 n 个方括号槽（1-based）。
- 必须同时登记 `anchor`：槽内原文逐字片段（≤20 字），如 `[需要即时结果]`。
- 同一字段内两槽文本完全相同 → 追加出现序后缀 `-a`／`-b`。

**作用域**：以 `selection_id` 为界，只在本日志内有效；**不得跨日志复用、不得写进 `registry`、不得当谓词名**。

**登记去向**：本日志顶层 `slot_registry`。评审与复核只认这张表，不认 `slot_ref` 里的裸序号。

```yaml
slot_registry:
  - slot_id: SLOT-STY-001-current_space-1
    entry_id: STY-001
    field: applicability.current_space
    ordinal: 1
    anchor: "[需要即时结果]"
    state: used | closed | proposed | promoted | stale
    promoted_to: null          # promoted 时填正式编号
```

**注销 / 转正**：

| 时机 | 动作 |
|---|---|
| 日志关闭，该槽不再被任何记录引用 | `state: closed`，**保留行**（0.22 历史不改写） |
| 同一 `entry_id + field + anchor` 已在 ≥2 份日志出现 | `state: proposed`，并在 `open_obligations` 记「槽位编号转正」；转正须新检查面，不在本批 |
| 转正落地后 | `state: promoted` ＋ `promoted_to: <正式编号>`；原临时号不删 |
| 源文本改动使锚不再逐字匹配 | `state: stale`，**不得静默改序**；重锚后补 `reanchored_at` |

## 4. `assessments`（判断项，与事实分栏）

```yaml
assessments:
  - statement: <判断一句话>
    basis: <基于哪些 facts / 哪条原则>
    strength: strong | weak | assumption
```

规则：
- `strong`：可指回多条已求值事实；`weak`：只有单条或间接支撑；`assumption`：无事实支撑的保守假设（须在 ADR 记可推翻指标，0.5 保守假设类）。
- 判断项与 `facts` **互不复用编号**（`F*` vs `A*`），避免把结论当证据引用。

## 4.1 事实 / 判断的判定与同格拆分（F3）

**三问测试**（任一命中即判为判断，进 `assessments`）：

1. 有模态词：会／应当／必须／更好／更差／风险／建议／可行／大概率。
2. 结论依赖未来或未观测状态（预测、经验外推、他人意愿）。
3. 去掉该句后其余记录仍独立成立——说明它不承担证据角色。

**互斥规则**：
- 同一 `statement` 不得同时出现在 `facts` 与 `assessments`。
- `assessments.basis` 只能指向 `facts` 的 `F*`；指向另一条判断时必须标 `basis_kind: derived` 并写出推导链，禁止循环引用。
- `rejection_reason` 其实是判断时，写 `A*` 编号，不得伪装成 `F*`。

**同一格内两者并存时的拆法**（标准两步）：

1. 抽出可判真假的那一半 → `facts`，给 `F*`，按 §3 求值（可为 `unknown`）。
2. 剩下的结论 → `assessments`，`basis` 指回刚抽出的 `F*`。

例：原句「variadic 会放宽元数校验，因为当前只校验首参」

```yaml
facts:
  - {id: F7, statement: 当前实现只校验首参, value: true, source: 源码 X 第 n 行}
assessments:
  - {id: A4, statement: variadic 会放宽元数校验, basis: [F7], strength: weak}
```

拆完后 `F7` 单独成立，`A4` 可被反驳而 `F7` 不被动摇——这才是分栏的目的。

## 5. `open_obligations`（本次产生的勘察任务）

```yaml
open_obligations:
  - what: <缺什么事实>
    owner: <谁去查；可空>
    due: <日期或「下次评审前」；可空>
```

规则：
- **只登记本次产生的任务，不写进 `registry` 的 `gaps`**（试跑约束）。
- 同一事实在多个选型里反复 unknown → 应由 S0 汇总成一次勘察，而不是每份日志各记一条。

## 6. 最小可接受记录（5 分钟能填完的形态）

```yaml
selection_id: SEL-20261109-01
decided_at: 2026-11-09T10:05:00+08:00
decided_by: {name: 张三, roster_ref: null}       # unregistered：有人名、无注册表
deployment_instance: {status: absent, roster_ref: null}
approval_status: provisional                     # absent 时的固定值
decision: 选择「事件溯源 + CQRS」作为订单域通信风格
adr_ref: ADR-ORDER-01
candidates:
  - {id: C1, statement: 事件溯源+CQRS, verdict: selected}
  - {id: C2, statement: 同步请求-响应, verdict: rejected, rejection_reason: 峰值吞吐事实为 false}
facts:
  - slot_ref: STY-004/applicability.current_space/1
    slot_id: SLOT-STY-004-current_space-1
    statement: 订单写入峰值 ≥ 3k TPS
    value: true
    source: 生产监控 2026-10 月报（记录 ID OPS-2026-10-03）
  - slot_ref: STY-001/applicability.delivery_space/2
    slot_id: SLOT-STY-001-delivery_space-2
    statement: 团队具备事件版本迁移经验
    value: unknown
    source: null
    note: 按 M15 保留 C1；已登记 open_obligations
slot_registry:
  - {slot_id: SLOT-STY-004-current_space-1, entry_id: STY-004, field: applicability.current_space, ordinal: 1, anchor: "[高写入吞吐]", state: used}
  - {slot_id: SLOT-STY-001-delivery_space-2, entry_id: STY-001, field: applicability.delivery_space, ordinal: 2, anchor: "[具备事件版本迁移经验]", state: used}
open_obligations:
  - {what: 团队事件版本迁移经验, owner: 张三, due: 2026-11-16}
  - {what: 补部署实例声明（批准角色注册表）, owner: 张三, due: 2026-11-30}
```

## 7. 反模式（试跑中确认过的失败形态）

| 反模式 | 后果 |
|---|---|
| 把「我认为 X 会放宽」写进 `facts.value` | 记录看似客观，实则结论先行（F3） |
| `unknown` 填 `false` | 候选被沉默排除，违反 M15 |
| 同一段话同时写 ADR 和 `selection_log` | 双写，第二次就没人维护（F4） |
| 对全部条目逐槽填 applicability | 单次选型 12 小时+，实际不可执行（F5） |
| 事后补记不标 retrospective | 时间字段失真，无法复算决策时的事实状态（F6） |
| 用「领导／架构组／按公司流程」填 `decided_by` | 批准链看似齐备，实际无出处（F2） |
| 用 `null` 或 `false` 代 `unknown` | 该查的事实被记成不适用，M15 失效（F2） |
| 一个格子同时写事实与结论 | 复核时分不清哪句可被反驳，等于结论先行（F3） |
| 改写槽序后沿用旧裸序号 | 历史日志与源文本失配，且没有锚可重锚（F1） |
