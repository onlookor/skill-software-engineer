# 试跑示范 01：`·` 显式占位 vs 全谓词 variadic（draft）

- 性质：**试跑示范，不是规范**；不改母本、不改注册表数据、不新增 `gaps`。
- 状态：**draft**
- 场景来源：本仓已有决策——元数据校验为什么选「`·` 显式占位 + `argc = arity`」，而不是「全谓词 variadic」或「裸缺参按前缀投影放行」
- 原始决策落点：[ADR-SRC-P0-08](file:///home/wgz/projects/skills/software-engineering/adr/ADR-SRC-P0-08-approved-20261108-S12转硬与显式占位.md)、[DATA-SPEC D3.7／D3.8](file:///home/wgz/projects/skills/software-engineering/registry/DATA-SPEC.md)、[CHECK-SPEC C5.21](file:///home/wgz/projects/skills/software-engineering/registry/CHECK-SPEC.md)
- **本记录是追溯填写**（决策已发生，非模拟）：`retrospective: true`，原始决策时刻未留痕，`decided_at` 只能记填写时刻，见 §5 F6。

## §1 决策一句话

选择「**缺参必须写 `·` 显式占位、`argc = arity` 恰好相等、仅 `registry_entry` 允许 `argc ≥ 6`**」，拒绝「全谓词 variadic」与「裸缺参按前缀投影默认放行」。

## §2 候选

| id | 候选 | 结论 | 理由（指回事实/判断） |
|---|---|---|---|
| C1 | `·` 显式占位；默认 `argc = arity`；唯一 variadic 是 `registry_entry`（`argc ≥ 6`） | selected | F1–F5 支持；A3 |
| C2 | 全谓词 variadic（所有谓词一律 `argc ≥ arity`） | rejected | 会使 `f(x)` 对所有 f 合法；无母本依据（F1＋F6，A1） |
| C3 | 裸缺参按前缀投影默认放行（旧口径） | rejected | 无法区分「漏写」与「有意不约束」，S-12 归零但语义未修（F3＋F6，A2） |

## §3 事实（三值求值）

| id | 出处（`provenance.kind`） | 事实 | value | 定位符 |
|---|---|---|---|---|
| F1 | `编译规范/2.3` | 谓词语法含通配 `·`，且 `·` 表示有意不约束的槽位 | true | 编译规范 2.3 BNF 与语义表 |
| F2 | `0.17.8/registry_entry` | `registry_entry` 是词表中唯一可变长槽（固定 6 槽＋尾部 `fields...`） | true | 母本 @493 末槽；DATA-SPEC D1.4 第 11 行 |
| F3 | `检查面/全部判定串` | 干跑时 1,150 串中 43 处元数不匹配（12 名）：23 条槽位互换、9 条少参、11 条真错 | true | ADR-SRC-P0-08 §4；`--check` 干跑 |
| F4 | `formula_words/has` | 当时 `has` 无 `arity`，16 处调用无法判「错」还是「未覆盖」 | **unknown** | ADR-SRC-P0-10 §9–§10（后续裁定 arity=1） |
| F5 | `可变槽阈值` | 用户明定 N = 6（`argc ≥ 6`） | true | ADR-SRC-P0-08 §1 第 3 条；DATA-SPEC D3.8 |
| F6 | `历史口径` | 旧实现按「前缀投影」默认放行裸缺参，无显式判据 | true | ADR-SRC-P0-08 §1 第 1 条「不再默认投影」 |

F4 的处置（按 M15）：**候选不排除**，`has` 调用单列「未覆盖」，不计通过、不计失败；随后由 B1 裁定 `arity=1`，16→0。这一条是本次三值记录里唯一 `unknown`，处理方式可复算。

## §4 判断（与事实分栏）

| id | 判断 | 依据 | strength |
|---|---|---|---|
| A1 | 全谓词 variadic 会让任意 `f(x)` 合法，等于全局放宽，判定强度下降 | F1（母本只把 `·` 定为占位）＋F2（只有一个 variadic）＋F6 | strong |
| A2 | 前缀投影放行无法区分「漏写」与「有意不约束」，43 处会被静默吞掉 | F3＋F6 | strong |
| A3 | 显式占位 + 默认精确元数 + 唯一 variadic 例外，是同时保强度与可机器校的唯一形态 | F1–F5 | strong |

## §5 完整记录（按 [selection_log-schema](file:///home/wgz/projects/skills/software-engineering/pilot/selection_log-schema.md) 填写）

```yaml
selection_id: SEL-20261108-01
decided_at: 2026-11-08T17:26:10+08:00
retrospective: true          # 原始决策在 2026-11-08 早于本记录，决策时刻未留痕
decided_by:                  # 有名分、姓名未披露（C1 已闭合）
  state: unregistered
  role: 人类责任方
  name: null
  roster_ref: null
  name_absent_reason: withheld
deployment_instance:
  status: absent
  roster_ref: null
approval_status: approved    # 决策已获人类责任方批准；实例缺由 deployment_instance 表达
decision: 元数校验采用「`·` 显式占位 + `argc = arity`」，仅 registry_entry 允许 `argc ≥ 6`
adr_ref: ADR-SRC-P0-08 / DATA-SPEC D3.7-D3.8 / CHECK-SPEC C5.21
candidates:
  - id: C1
    statement: "`·` 显式占位；默认 argc = arity；唯一 variadic 为 registry_entry（argc ≥ 6）"
    verdict: selected
  - id: C2
    statement: 全谓词 variadic（一律 argc ≥ arity）
    verdict: rejected
    rejection_reason: 会让任意 f(x) 合法，全局放宽且无母本依据（A1，basis F1／F2／F6）
  - id: C3
    statement: 裸缺参按前缀投影默认放行
    verdict: rejected
    rejection_reason: 无法区分漏写与有意不约束，43 处被静默吞掉（A2，basis F3／F6）
facts:
  - id: F1
    provenance: {kind: clause, ref: "编译规范.md#2.3", anchor: "通配 · 表示有意不约束的槽位"}
    statement: 语法含通配 `·` 且表示有意不约束
    value: true
    note: ''
  - id: F2
    provenance: {kind: clause, ref: "软件工程元框架成文法.md#L493", anchor: "registry_entry（6 固定槽 + fields...）"}
    statement: registry_entry 是唯一可变长槽（6 固定＋fields...）
    value: true
    note: ''
  - id: F3
    provenance: {kind: adr, ref: "ADR-SRC-P0-08#§4", anchor: "1,150 串中 43 处元数不匹配"}
    statement: 1,150 串中 43 处元数不匹配（23 槽位互换／9 少参／11 真错）
    value: true
    note: ''
  - id: F4
    provenance: {kind: adr, ref: "ADR-SRC-P0-10#§9", anchor: "has 无 arity，16 处未覆盖"}
    statement: 当时 has 无 arity，16 处无法判定
    value: unknown
    note: '按 M15 单列未覆盖、候选保留；后续裁定 arity=1（16→0）'
  - id: F5
    provenance: {kind: adr, ref: "ADR-SRC-P0-08#§1.3", anchor: "N = 6"}
    statement: 用户明定 N=6
    value: true
    note: ''
  - id: F6
    provenance: {kind: adr, ref: "ADR-SRC-P0-08#§1.1", anchor: "不再默认前缀投影"}
    statement: 旧实现按前缀投影默认放行裸缺参
    value: true
    note: ''
slot_registry: []            # 本记录无 kind=slot 事实；条款/ADR 证据不登记
assessments:
  - {id: A1, statement: 全谓词 variadic 等于全局放宽，判定强度下降, basis: [F1, F2, F6], basis_kind: facts, strength: strong}
  - {id: A2, statement: 前缀投影放行会静默吞掉漏写, basis: [F3, F6], basis_kind: facts, strength: strong}
  - {id: A3, statement: 显式占位＋精确元数＋唯一 variadic 例外是保强度且可机器校的唯一形态, basis: [F1, F2, F3, F4, F5], basis_kind: facts, strength: strong}
open_obligations:
  - {what: 补部署实例声明（批准角色注册表）, owner: 人类责任方, due: 2026-11-30}
```

## §6 填写耗时（实测）

- 起始：`2026-11-08T17:26:10+08:00`（开始起草模板与 schema）
- 三件产物完成：`2026-11-08T17:29:53+08:00` → **总耗时 3 分 43 秒**（schema＋勘察模板＋本示范）
- **本示范记录单独耗时 ≈ 2 分钟**（6 条事实＋3 条判断＋3 候选）
- ⚠ 必须说明的低估因素：本次填写时 ADR-SRC-P0-08／D3.7／D3.8 的原文已在本会话上下文中，**没有冷启动查证成本**。真实场景里首次填的人大部分时间会花在「定位原文与行号」；按 §3 的 6 条事实估计，冷启动约 **5–10 分钟**，但这是估计、不是实测。
- 结论：**单次决策的记录成本不是瓶颈**（分钟级）；瓶颈是 F5 的全量逐槽填（小时级），以及 F1 的槽位定位（改写后失效）。

## §7 试跑发现的卡点（比 schema 本身更重要）

| # | 卡点 | 证据/表现 | 影响 | 建议方向（不在本批落地） |
|---|---|---|---|---|
| F1 | **方括号槽没有槽位编号** | `slot_ref` 只能拼 `entry_id/field/序号`；同一字段有多个槽时靠数逗号定位 | 改写槽序即失配；历史日志无法机械复核 | 需要一套稳定槽位编号（新检查面），否则 `selection_log` 的「逐条」只能人工对文本 |
| F2 | **仓库没有「部署实例」** | 0.5 @129 要求部署声明批准角色注册表；本仓无实例，`decided_by` 只能写「人类责任方」 | 严格按 0.5，高影响决策应整体阻塞；自举场景无法合规记录批准链 | 需要一层最小「部署实例声明」，至少含主批准人与升级链 |
| F3 | **事实与判断极易混栏** | 起草时三次想把「variadic 会放宽」写进 `facts.value` | 记录看似客观、实则结论先行 | schema 必须分 `facts`／`assessments`（已在 §4 固化） |
| F4 | **ADR 与日志双写** | 背景与取舍在 ADR 已写一遍，日志再写就是副本 | 第二份没人维护，最终 logs 全空 | 定分工：ADR 管叙述与后果，日志只管求值轨迹＋拒绝理由，以 `adr_ref` 连接 |
| F5 | **全量逐槽填不可行** | 762 项 applicability × 1 分钟 ≈ 12 小时；本次 6 条事实即 14 分钟 | 若要求「每次选型全量填」，流程必被绕过 | 强制先 S1 裁剪候选集（3–8 条），只对候选消费的槽求值；schema 允许候选前空记录 |
| F6 | **决策时刻没有留痕** | 原始决策在同日早些时候，无法复算「当时知道什么」 | 追溯记录的时间字段失真，三值求值可能被后见之明污染 | 日志必须在决策当场开；追溯填写须标 `retrospective: true`（已加字段） |

其中 **F1 与 F5 是结构性卡点**：前者决定「逐条」能否机械核对，后者决定流程是否有人真的走。F2 是本框架自举时的治理缺口，靠 schema 补不了。

## §8 按新 schema 回填（2026-11-08）

### §8.1 逐项耗时（口径：agent 编辑操作，**不是**人类填写耗时）

| 段 | 内容 | 起 | 止 | 耗时 |
|---|---|---|---|---|
| T0→T1 | §5 YAML 重排：`decided_by` 三态、`deployment_instance`、`approval_status`、6 条 facts 加 `id`／`slot_id`、3 条 assessments 加 `id`／`basis` 列表、`open_obligations` 补 2 条 | 19:04:29 | 19:04:51 | **22 秒** |
| T1→T2 | 提交前核对 §3／§4 与 §5 编号一致 | 19:04:51 | 19:05:07 | 16 秒 |
| T2→T3 | 本节记录 | 19:05:07 | 19:05:30 | 23 秒 |

**口径警告**：上表是 agent 的编辑器操作耗时，**不可换算人力成本**。与 §6 的 3 分 43 秒同源问题——原文都在同一会话上下文里，没有冷启动查证。人类首次填写的增量仍只能估计。

| 新增栏 | 条数 | agent 增量 | 人类预估增量 |
|---|---|---|---|
| `decided_by` 三态 | 1 | <5 秒 | +30–60 秒（要先判「算不算 unregistered」） |
| `deployment_instance` | 1 | <5 秒 | +30 秒（要判 absent 并接受 provisional） |
| `approval_status` | 1 | <5 秒 | +0（随 absent 固定） |
| `facts.id` | 6 | 均摊在 22 秒内 | +1–2 分钟（要与 §3 表编号一致） |
| 逐条判 `slot_ref` 填什么 | 6 | 同上 | **+2–3 分钟（最费时）** |
| `assessments.id`＋`basis: [F*]` | 3 | 同上 | +1 分钟 |
| `slot_registry` 空段 | 1 | <5 秒 | +10 秒 |
| `open_obligations` 补 2 条 | 2 | 同上 | +1 分钟 |

**最费时的一栏**：判定 `facts.slot_ref` 该填什么。本记录 6 条事实全部来自条款／ADR／干跑，**没有一条是 registry 条目的方括号槽**；旧写法可以随手写「编译规范/2.3」，新规则下要么 `null`＋理由、要么造一个不存在的槽号——每一条都要停下来判断。

### §8.2 露馅点（schema 是否要改，先列等裁）

| # | 冲突 | 表现 | 严重度 |
|---|---|---|---|
| C1 | `decided_by` 缺「有名分、无人名」档 | `unregistered` 定义要求 `name` 为真实人名；本记录只有角色「人类责任方」、无姓名 → 填 `name: null` 违反值域，填 `unknown` 又等于谎称「当场无人可署」。当前取 `unregistered + name: null + obligation`，属**越界填写** | 硬矛盾 |
| C2 | `slot_ref` 假设事实来自 applicability 槽 | 本记录 6/6 条事实是条款／ADR／干跑证据。`slot_ref: null` 时 §1.1 要求配 `not_applicable_reason`，但 `facts` 五字段里没有这个字段，只能塞进 `note` | 覆盖缺口 |
| C3 | §3 五字段无 `id`，§4.1 却要求 `basis: [F*]` | 回填被迫给 facts 加第 6 个字段 `id`，否则判断项无法指回事实 | **硬矛盾** |
| C4 | `slot_registry` 只管条目槽 | 条款证据无登记去向，机械复核只能靠 `source` 自由文本——F1 的「可复核」只覆盖一半 | 覆盖缺口 |
| C5 | `approval_status` 只有两值 | 本决策在人类层面已批准，但 `deployment_instance=absent` 强制 `provisional` → 「已批准但注册表缺」与「未批准」在记录上无法区分，读者会误读 | 语义失真 |

### §8.3 结论

规则**填得下**（§5 重排无死格，22 秒完成），但 C1／C3 是真矛盾：照规则填必须越界（加字段或填 null 违约）；C2／C4 是覆盖缺口；C5 是语义失真。按本批约束**未改 schema**，等裁定后再决定是加 `evidence_ref`／`id`／第四态，还是收紧为「仅条目槽事实适用本 schema」。

### §8.4 二次回填（schema 改造后，2026-11-08）

| 段 | 内容 | 起 | 止 | 耗时 |
|---|---|---|---|---|
| T6→T7 | §5 重写：6 条 facts 换 `provenance`、`decided_by` 加 `name_absent_reason`、`approval_status` 改 `approved`、§3 表头同步 | 19:11:45 | 19:12:16 | **31 秒** |
| T7→T8 | 本节记录与复核 | 19:12:16 | 19:12:46 | 30 秒 |

**耗时变化**：上一轮同段 22 秒，本轮 31 秒（+9 秒）。绝对值变长，但**结构成本下降**：上一轮最费时的「判定 `slot_ref` 填什么」消失（直接按载体选 `clause／adr／system`），新增的时间花在给每条事实补 `anchor` 与写 `ref` 定位符。人类预估增量从 +2–3 分钟降到 +1 分钟/条。

**C1–C5 处置结果**：

| # | 处置 | 依据 |
|---|---|---|
| C1 | **已闭合**：三态 + `name_absent_reason: withheld` | 裁定：不加第四态，姓名是另一轴 |
| C2 | **已闭合**：`kind` 分类替代 `slot_ref: null`，不再需要 `not_applicable_reason` | 裁定：合并为 `provenance` |
| C3 | **已闭合**：`id` 进字段表，`basis` 按 `[F1, F2]` 引用 | 裁定：`id` 是主键 |
| C4 | **已闭合**：`slot_registry` 只索引 `kind=slot`，其余靠 `ref` | 裁定：不强行登记 |
| C5 | **已闭合**：`approval_status: approved`，实例缺由 `deployment_instance` ＋ 义务表达 | 裁定：取消 `absent→provisional` 映射 |

**新发现（轻量，非矛盾）**：

1. `kind: clause` 的 `ref` 写行号（`#L493`）会随母本编辑漂移；`anchor` 可重锚，但需要一条「行号漂移→以 anchor 为准」的约定。当前靠 §3.1 的 `stale` 机制覆盖，够用。
2. `system` 类出处（`system:<系统名>#<记录ID>`）在本记录无实例，未被真实验证。
3. `provenance` 是嵌套块，单行流式写法在 6 条事实里可读，但字段一多就会因缩进出错；这是格式风险，不是 schema 缺陷。

**结论**：五处卡点全部闭合，二次回填无死格；未再发现需要改 schema 的矛盾。
