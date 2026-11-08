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

**边界（与枚举值同名，但不同层）**：字段级 `unknown`（如 `value: unknown`）触发本文务；枚举里的 `unknown` 只是某个附注字段的取值说明（如 `name_absent_reason: unknown`），**不触发** `open_obligations`。

## 1.2 `deployment_instance`、`decided_by` 与 `approval_status`（F2）

本仓没有 0.5 @129 意义上的**部署实例**（批准角色注册表）。schema 不假装有，只把三件事分开记：**有没有可指认的批准人**（`decided_by`）、**这个决策有没有被人类批准**（`approval_status`）、**部署实例缺不缺**（`deployment_instance`）。

```yaml
deployment_instance:
  status: declared | absent
  roster_ref: <批准角色注册表 ID／路径> | null    # declared 时必填
approval_status: approved | provisional
decided_by:
  state: named | unregistered | unknown
  role: <角色名> | null
  name: <人名> | null
  roster_ref: <注册表 ID> | null
  name_absent_reason: no_person_assigned | withheld | unknown   # 仅 unregistered 且 name=null 时必填
```

`decided_by.state` 三态：

| 值 | 何时用 | 写法约束 |
|---|---|---|
| `named` | 有注册表实例 | `name`／`role`／`roster_ref` 必填 |
| `unregistered` | 有可指认的批准人，但不在册 | `role` 必填；`name` 可空，空时必填 `name_absent_reason`；`roster_ref: null` ＋ 一条 `open_obligations`（补部署实例声明） |
| `unknown` | 决策当场无人可署 | 字面 `unknown` ＋ 一条 `open_obligations`（升级到可署人） |

规则：
1. **`absent` 时不编造批准链**：`roster_ref` 留 `null`，不得写「架构组 → CTO」这类无出处的链。
2. **禁止占位词充数**：`领导`／`架构组`／`按公司流程`／`相关方` 不是批准人，出现即判凭空填写。
3. **`approval_status` 只说批准**：`approved` 要求 `decided_by.state ∈ {named, unregistered}`（可指认的批准人，哪怕不在册）；`deployment_instance.status=absent` **不再**强制 `provisional`——实例缺不缺由 `deployment_instance` ＋ `open_obligations` 表达，两者不压进同一字段。
4. **`absent` 不等于记录无效**：允许记录，但必须在 ADR 写明「待补部署实例后追认」，否则视为绕过 0.5。

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
  - id: F1
    provenance:                      # 出处唯一承载（已删自由文本 source）
      kind: slot | clause | adr | dry_run | other | person | system
      ref: <可解析定位符>             # 见 §3.0；不接受散文
      anchor: <原文片段>              # other 可为 null（材料本身即锚）
      slot_id: SLOT-<...>            # 仅 kind=slot 时必填
      source_class: <可选，见下>
    statement: <事实一句话，可判真假>
    value: true | false | unknown    # 三值；禁止二值化
    note: <unknown 的处置，或求值说明>
```

### 3.0 定位符格式（对应 0.4：来源文档／来源人／来源系统）

| kind | `ref` 形式 | `anchor` |
|---|---|---|
| `slot` | `<entry_id>/<field>/<n>` | 槽内原文逐字片段（≤20 字） |
| `clause` | `<文件名>#<条款号或行号>`，如 `软件工程元框架成文法.md#5.2.6`／`#L2514` | 条款原句片段 |
| `adr` | `<ADR 编号或路径>#<小节>` | 决定原句片段 |
| `dry_run` | `<命令或报告>#<记录ID或行>`，如 `--check@2026-11-08#summary` | 输出片段 |
| `other` | 材料 ID：`mail:<ID>`／`ticket:<ID>`／`chat:<截图ID>`，限**已存在但形式不规整**的可复核材料 | 可为 `null` |
| `person` | `person:<角色或姓名>@<日期或会议ID>` | 原话片段 |
| `system` | `system:<系统名>#<记录ID>` | 记录字段片段 |

`clause` 的 `ref` 里**行号仅作导航，复核以 `anchor` 为准**：母本编辑后行号会漂移，按 §3.1 的 `stale` 重锚，不得拿行号当证据。

`source_class` 可选，仅在出处门槛需要分类时填；取值**逐字**取母本 0.17.2 条目 schema（@335）：`external｜mother-row｜mother-clause｜mother-definition｜fallback`。**出处是 0.17.2，不是 0.4**。

口语类输入按 0.4 处理：有「来源人＋日期」→ `kind: person` 记事实；无任何载体 → 仍记 `unknown` 事实 ＋ `note: 出处不明` ＋ `open_obligations`（**不得**因「说不清缺什么」降为判断）；只有内容本身是**评价性／预测性命题**时，才进 `assessments.assumption`。

规则（每条都来自试跑的真实教训）：
1. **三值**：`unknown` 不得写成 `false`；`unknown` 的候选一律保留（M15），并登记 `open_obligations`，禁沉默排除。
2. **有出处才进 `facts`**：`provenance.ref` 必须可解析；无出处的说法进 `open_obligations`，对应字段保持 `[待勘察]`；不得用「方向性陈述」冒充事实。
3. **判断不进 `facts`**：凡带「会／应当／更好／风险大」的句子是判断，不是事实，见 §4。混进来会让记录看似客观、实则夹带结论（试跑 F3）。
4. **只填候选消费的事实**：未进候选集的条目不逐槽填（全量 applicability 762 项按每条 1 分钟≈12 小时，不可行；必须先 S1 裁剪）。
5. **`id` 是主键**：`F*` 唯一，`assessments.basis` 按 `[F1, F2]` 引用它；`provenance` 可空、不可当主键。`kind=slot` 时必须登记 §3.1 的 `slot_registry`。

## 3.1 方括号槽的临时代号与登记去向（F1）

母本 0.17.2 没有槽位编号字段，检查器也不产出。因此 `provenance.kind=slot` 时 `ref` 里的 `<n>` 是临时办法，按下列规则收敛到一张可复核的表。

**编法**：`SLOT-<entry_id>-<field>-<n>`
- `<field>` 取字段路径末段：`problem_space`／`current_space`／`delivery_space`／`detection_predicate`／`bound_expr`。
- `<n>` = 该字段**当前文本**中从左到右第 n 个方括号槽（1-based）。
- 必须同时登记 `anchor`：槽内原文逐字片段（≤20 字），如 `[需要即时结果]`。
- 同一字段内两槽文本完全相同 → 追加出现序后缀 `-a`／`-b`。

**作用域**：以 `selection_id` 为界，只在本日志内有效；**不得跨日志复用、不得写进 `registry`、不得当谓词名**。

**登记去向**：本日志顶层 `slot_registry`，**只索引 `kind=slot` 的条目**；`clause／adr／dry_run／other／person／system` 不登记（它们的 `ref` 本身即定位符）。评审只认这张表，不认 `ref` 里的裸序号。

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
  - id: A1
    statement: <判断一句话>
    basis: [F1, F2] | [<原则条号>]    # 指向 facts 的 id
    basis_kind: facts | derived      # derived 时须写推导链
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
  - {id: F7, provenance: {kind: clause, ref: "源码X#第n行", anchor: "只校验首参"}, statement: 当前实现只校验首参, value: true, note: ''}
assessments:
  - {id: A4, statement: variadic 会放宽元数校验, basis: [F7], basis_kind: facts, strength: weak}
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
decided_by: {state: unregistered, role: 架构组负责人, name: 张三, roster_ref: null, name_absent_reason: null}
deployment_instance: {status: absent, roster_ref: null}
approval_status: approved        # 有可指认的批准人；实例缺不缺不压进本字段
decision: 选择「事件溯源 + CQRS」作为订单域通信风格
adr_ref: ADR-ORDER-01
candidates:
  - {id: C1, statement: 事件溯源+CQRS, verdict: selected}
  - {id: C2, statement: 同步请求-响应, verdict: rejected, rejection_reason: 峰值吞吐事实 F1 不满足}
facts:
  - id: F1
    provenance: {kind: system, ref: "system:生产监控#OPS-2026-10-03", anchor: "峰值 3.2k TPS"}
    statement: 订单写入峰值 ≥ 3k TPS
    value: true
    note: ''
  - id: F2
    provenance: {kind: slot, ref: "STY-001/applicability.delivery_space/2", slot_id: SLOT-STY-001-delivery_space-2, anchor: "[具备事件版本迁移经验]"}
    statement: 团队具备事件版本迁移经验
    value: unknown
    note: 按 M15 保留 C1；已登记 open_obligations
slot_registry:                   # 只索引 kind=slot
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
| 用「领导／架构组／按公司流程」填 `decided_by` | 批准链看似齐备，实际无出处（F2） |
| 用 `null` 或 `false` 代 `unknown` | 该查的事实被记成不适用，M15 失效（F2） |
| 一个格子同时写事实与结论 | 复核时分不清哪句可被反驳，等于结论先行（F3） |
| 改写槽序后沿用旧裸序号 | 历史日志与源文本失配，且没有锚可重锚（F1） |
| `provenance.ref` 写成散文（「大家都知道」「会议上说过」） | 不可解析，等于无出处（0.4 公理 A2） |
| 无来源人的口述记成 `facts` | 把「来源人」来源伪造出来；应记 `unknown`＋勘察，或降 `assumption` |
| 把部署实例缺失写进 `approval_status` | 批准与否、实例缺不缺两轴混压，导致「已批准但无实例」与「未批准」同形（C5） |
| F4：在日志里复制 ADR 的背景与取舍段 | 双写必然腐化；**挡法**：日志只留 `decision` 一行＋`adr_ref`，论证与后果归 ADR |
| F5：为未进候选补槽，或候选未定先填 | 762 项≈12 小时，流程被绕过；**挡法**：先裁 3–8 条候选，只填候选消费的事实，其余进 `open_obligations` |
| F6：补记不标 `retrospective`，或 `decided_at` 写补记时刻 | 无法复算「当时知道什么」；**挡法**：决策当场开日志，补记标 `retrospective: true`，`decided_at` 记原决策时刻 |
