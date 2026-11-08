# 选型日志最小 schema（试跑模板，draft）

- 性质：**试跑模板，不是规范**。不新增母本义务、不改注册表数据、不新增 `gaps`。
- 状态：**draft**（未批准；试跑后按反馈修订）
- 上游依据：0.18 S0–S6（选型规程）、0.18.2 S1（applicability 求值）、0.18.6 M15（unknown → 候选保留＋勘察义务）、0.17.7 门槛 2（无出处阈值禁填）、0.4 条件 3（硬约束须有出处）
- 设计目标：**填得下去**。核心字段只留 7 个，其余可选；一条记录默认一屏填完。字段每多一个，实际填写率就降一截。

## 1. 最小记录（核心 7 字段）

```yaml
selection_id: SEL-20261108-01        # 一次选型一个 ID；同日多选型顺延 -02
decided_at: 2026-11-08T17:26:10+08:00  # ISO8601；决策当场打点，事后补记须标 retrospective
decided_by: <人类责任方姓名/角色>       # 无角色注册表实例时写「未声明（见试跑报告 F2）」
decision: <一句话，动词开头：选了什么>   # 不写背景，背景在 ADR
adr_ref: <ADR 编号或路径>              # 决策叙述与后果的唯一归属地
candidates: [...]                     # 见 §2
facts: [...]                          # 见 §3；只填候选实际消费的事实
```

**不设的字段（默认不填，防膨胀）**：会议地点、参与人全名单、评分权重、备选方案详述、风险登记、后续行动项。这些留在 ADR 或项目工具里。

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
5. `slot_ref` 目前只能按「条目＋字段＋序号」拼——**这是临时办法**，见试跑报告 F1。

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
decided_by: 张三（架构组）
decision: 选择「事件溯源 + CQRS」作为订单域通信风格
adr_ref: ADR-ORDER-01
candidates:
  - {id: C1, statement: 事件溯源+CQRS, verdict: selected}
  - {id: C2, statement: 同步请求-响应, verdict: rejected, rejection_reason: 峰值吞吐事实 F2 为 false}
facts:
  - slot_ref: STY-004/applicability.current_space/1
    statement: 订单写入峰值 ≥ 3k TPS
    value: true
    source: 生产监控 2026-10 月报（记录 ID OPS-2026-10-03）
  - slot_ref: STY-001/applicability.delivery_space/2
    statement: 团队具备事件版本迁移经验
    value: unknown
    source: 无（团队能力事实未采集）
    note: 按 M15 保留 C1；已登记 open_obligations
open_obligations:
  - {what: 团队事件版本迁移经验，owner: 张三, due: 2026-11-16}
```

## 7. 反模式（试跑中确认过的失败形态）

| 反模式 | 后果 |
|---|---|
| 把「我认为 X 会放宽」写进 `facts.value` | 记录看似客观，实则结论先行（F3） |
| `unknown` 填 `false` | 候选被沉默排除，违反 M15 |
| 同一段话同时写 ADR 和 `selection_log` | 双写，第二次就没人维护（F4） |
| 对全部条目逐槽填 applicability | 单次选型 12 小时+，实际不可执行（F5） |
| 事后补记不标 retrospective | 时间字段失真，无法复算决策时的事实状态（F6） |
