# `delivery_space` 勘察清单模板（试跑模板，draft）

- 性质：**试跑模板，不是规范**；不新增母本义务、不改注册表数据、不新增 `gaps`。
- 状态：**draft**
- 对象：`G-PRJ-1` 所指的四类待勘察事实（PRJ-001…PRJ-011 的 `delivery_space`，共 22 项＝11 条 × 2 项）
- 门槛：0.4 条件 3（可追溯至三空间具体事实）＋ 0.17.7 门槛 2（无出处的具体数值 = 假精确）

## 0. 使用方式

1. 每类事实先用 §1–§4 的「问题清单」问一遍；答不上来的保持 `[待勘察：…]`，并登记到 `selection_log.open_obligations`。
2. 一个事实一条。出处用 `provenance` 块（见 [selection_log-schema](file:///home/wgz/projects/skills/software-engineering/pilot/selection_log-schema.md) §3.0）：勘察事实多为 `kind: person`（访谈）／`system`（系统记录）／`other`（工单、邮件）；只有落在 registry 条目方括号槽上的事实才用 `kind: slot`，并按 §3.1 登记 `slot_registry`。`ref` 必须是可解析定位符，散文不接受。
3. 回填前先判 `answer_kind`：`fact` 才进本表；若写出来的是判断（含「会／应／风险」），按 schema §4.1 拆成「事实 + 判断」两条，事实进本表、判断进 `assessments`。
4. 只有**同时满足** §5 四条验收判据才允许回填；否则不得用方向性陈述降格填充。

## 1. 谁组织评审

**要回答**：
- 评审由哪个角色/小组发起与主持？（组织名＋角色名，不是「相关方」）
- 谁决定评审是否召开？谁有权宣布「本次不评审」？
- 评审记录由谁归档、归档到哪里？

**合格颗粒度示例**：
> 每周四 16:00 由架构组轮值主持；轮值表见 `架构组轮值-2026Q4`；不评审的例外须架构组负责人书面同意并归档到 `DEC-2026-xx`。

**不合格**：`由团队组织评审`／`需要时召开`（无法判定本次是否合规）。

## 2. 评审人能力门槛

**要回答**：
- 哪几类角色必须到场？（角色名＋最小人数）
- 对每类角色的能力要求是什么？以什么形式被证明（认证、既往评审记录、指定名单）？
- 缺人时能否用替代角色？替代条件是什么？

**合格颗粒度示例**：
> 必须到场的角色：架构负责人 1、安全评审员 1（持内部安全评审资格，名单见 `SEC-ROSTER-2026`）、运维代表 1；安全评审员缺位时不得以架构负责人兼任，须延期。

**不合格**：`具备相应能力`／`资深工程师参加`（无名单、无判据）。

## 3. 评审周期与时限

**要回答**：
- 从提交到出具结论的时限是多少？超时如何处理（升级／默认通过／阻塞）？
- 评审结论的有效期多长？过期后是否重评？
- 时限是否随影响级别分档？

**合格颗粒度示例**：
> P0 变更 2 个工作日内出结论；逾期未出结论按 0.5 升级链升一级（升级对象：架构负责人），不得视为通过；结论有效期 90 天。

**不合格**：`尽快评审`／`两周左右`（无出处、无超时处置；且「两周」属无出处具体数值）。

## 4. 批准角色注册表映射

**要回答**：
- 每类高影响决策（风格定案、分解主策略、注册表变更、冲突矩阵例外）的主批准人是谁？
- 备选批准链的有序名单是什么？
- 批准时限是多少？升级链穷尽后按哪条处置？

**合格颗粒度示例**：
> 风格定案：主批准人＝技术委员会主任；备选链＝架构组负责人 → CTO；时限 5 个工作日；穷尽后按 0.10 第三条记「批准不可达」并转保守通道。

**不合格**：`由领导批准`／`按公司流程`（无法构成 0.5 的批准角色注册表）。

## 4.1 没有批准角色注册表实例时怎么填（F2）

仓库自举场景（如本仓）没有部署实例，这一栏**填不了真值**，但不允许留空或编造。按三态回落：

| 情况 | `answer` | `provenance.ref` | `verified` | 义务 |
|---|---|---|---|---|
| 有注册表实例 | 主批准人＋备选链＋时限 | 注册表 ID＋版本 | `true` | 无 |
| 有真实责任人但无注册表 | 角色＋姓名，写明「无注册表实例」 | 人名来源（会议纪要／邮件 ID） | `true`（人名事实为真） | 登记「补部署实例声明」到 `open_obligations`；`approval_status` 仍可为 `approved`（可指认的批准人即可），实例缺由 `deployment_instance.status=absent` 表达 |
| 无人可署 | 字面 `unknown` | `null` ＋ `not_applicable_reason: null` 不适用 | `unknown` | 登记「升级到可署人」；此时 `approval_status` 不得为 `approved` |

**硬约定**：`unknown` ≠ 留空。留空是填写遗漏，评审打回；`unknown` 是已确认取不到，必须挂义务。禁止用「领导／架构组／按公司流程／相关方」充数，出现即判凭空填写。

## 5. 验收判据（四条全过才可回填）

| # | 判据 | 问法 |
|---|---|---|
| 1 | **可定位** | 能否给出文档名／条款号／名单 ID／会议纪要 ID，而不是「大家都知道」？ |
| 2 | **可复现** | 第二个人照这条事实执行，能否得出同一结论？ |
| 3 | **可判定** | 能否回答「这一次评审是否合规」的是／否？ |
| 4 | **可分类** | 写下的是事实（可判真假）还是判断（含模态词／依赖未来）？只有 `fact` 可进本表 |

四条缺一 → 保持 `[待勘察]`，不得填 `false` 冒充「不适用」（M2 允许显式义务，不允许伪造）。若第 4 条不过，按 schema §4.1 拆成事实与判断两条，不得整句塞进 `answer`。

## 6. 可接受来源（按 0.4 排序）

| 优先级 | 来源 | 形式要求 |
|---|---|---|
| 1 | 组织规程／团队公约 | 有版本号或生效日期；指明适用团队 |
| 2 | 既有 ADR（已生效） | 编号可查，且决策仍在有效期 |
| 3 | 可点名的人时承诺 | 角色＋姓名＋日期（「大家配合」不算） |
| 4 | 项目记录 | 会议纪要／评审单 ID，含时间与结论 |

**不接受**：方向性陈述（「评审要尽早」）、无出处的数字（「2 小时」）、口头同意无记录、其他项目的惯例直接平移。

## 7. 空白填写表（复制即用）

```yaml
- question: 谁组织评审
  provenance: {kind: slot, ref: "PRJ-001/delivery_space/1", slot_id: SLOT-PRJ-001-delivery_space-1, anchor: "<槽内原文，逐字取>"}
  answer_kind: fact                              # fact 才进本表；assessment 拆到 assessments
  answer: <组织/角色＋出处定位符>
  verified: <true|false|unknown>                 # unknown 必须配 open_obligations 一条
  not_applicable_reason: null                     # answer 为 null 时必填一句
- question: 评审人能力门槛
  provenance: {kind: person, ref: "person:架构组负责人@2026Q4轮值表", anchor: "<原话片段>"}
  answer_kind: fact
  answer: <角色＋人数＋资格形式>
  verified: <true|false|unknown>
  not_applicable_reason: null
```

## 7.1 可选观测扩展：同一事实的两处落点

当勘察出的事实**同时**被条目侧 `applicability.delivery_space` 槽与部署侧判据 6 状态声明引用时，在该行追加 `dual_site` 组（字段定义见 [selection_log-schema](file:///home/wgz/projects/skills/software-engineering/pilot/selection_log-schema.md) §3.2）。

```yaml
- question: 谁组织评审
  provenance: {kind: slot, ref: "PRJ-001/delivery_space/1", slot_id: SLOT-PRJ-001-delivery_space-1, anchor: "<槽内原文，逐字取>"}
  answer_kind: fact
  answer: <组织/角色＋出处定位符>
  verified: <true|false|unknown>
  not_applicable_reason: null
  dual_site:                                   # 可选；整组不写＝本次未观测，不判遗漏
    entry_side: <条目侧取值>
    deploy_side: <confirmed_present|confirmed_absent|undetermined>
    first_valued: selection | deployment | simultaneous
    same_fact: same | granularity_differs | contrary
    contradiction:                             # 仅 same_fact=contrary 时填；否则 null
      authoritative: <entry_side|deploy_side|other|unresolved>
      adr_recorded: <true|false|unknown>
      other_side_revised: <true|false|unknown>
    observation_note: <一句：null 的理由，或人当时的处置事实>
```

- **只观测**：不改变 `answer`／`verified` 的求值，不新增义务，不触发检查，不进 `registry`／`gaps`。
- **三档口径同 schema §1.1**：整组不写不判遗漏；写了就不得留空；取不到 `unknown` ＋ `open_obligations`；不适用 `null` ＋理由。
- **不预设正确答案**：`contradiction` 只记「以什么为准、有没有记 ADR、有没有改另一边」，不评价哪种处置才对。

## 8. 与试跑结论的关系

本模板解决「问什么、给到什么颗粒度才合格」；**不解决「没有真实项目就不存在这些事实」**。仓库自举场景下四类事实均无来源，只能保持 `[待勘察]`——这正是 `G-PRJ-1`／`SO-1` 无法在仓内闭合的原因（详见试跑报告 §5）。
