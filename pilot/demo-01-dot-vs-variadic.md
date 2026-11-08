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

| id | slot_ref | 事实 | value | 出处 |
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
decided_by: 人类责任方（本仓用户，经任务书裁定）   # 无批准角色注册表实例，见 F2
decision: 元数校验采用「`·` 显式占位 + `argc = arity`」，仅 registry_entry 允许 `argc ≥ 6`
adr_ref: ADR-SRC-P0-08 / DATA-SPEC D3.7-D3.8 / CHECK-SPEC C5.21
candidates:
  - id: C1
    statement: `·` 显式占位；默认 argc = arity；唯一 variadic 为 registry_entry（argc ≥ 6）
    verdict: selected
  - id: C2
    statement: 全谓词 variadic（一律 argc ≥ arity）
    verdict: rejected
    rejection_reason: 会让任意 f(x) 合法，全局放宽且无母本依据（F1／F2／F6，A1）
  - id: C3
    statement: 裸缺参按前缀投影默认放行
    verdict: rejected
    rejection_reason: 无法区分漏写与有意不约束，43 处被静默吞掉（F3／F6，A2）
facts:
  - {slot_ref: 编译规范/2.3, statement: 语法含通配 `·` 且表示有意不约束, value: true, source: 编译规范 2.3 BNF, note: ''}
  - {slot_ref: 0.17.8/registry_entry, statement: registry_entry 是唯一可变长槽（6 固定＋fields...）, value: true, source: 母本 @493；DATA-SPEC D1.4 #11, note: ''}
  - {slot_ref: 检查面/全部判定串, statement: 1,150 串中 43 处元数不匹配（23 槽位互换／9 少参／11 真错）, value: true, source: ADR-SRC-P0-08 §4, note: ''}
  - {slot_ref: formula_words/has, statement: 当时 has 无 arity，16 处无法判定, value: unknown, source: ADR-SRC-P0-10 §9, note: 按 M15 单列未覆盖、候选保留；后续裁定 arity=1（16→0）}
  - {slot_ref: 可变槽阈值, statement: 用户明定 N=6, value: true, source: ADR-SRC-P0-08 §1.3, note: ''}
  - {slot_ref: 历史口径, statement: 旧实现按前缀投影默认放行裸缺参, value: true, source: ADR-SRC-P0-08 §1.1, note: ''}
assessments:
  - {statement: 全谓词 variadic 等于全局放宽，判定强度下降, basis: F1／F2／F6, strength: strong}
  - {statement: 前缀投影放行会静默吞掉漏写, basis: F3／F6, strength: strong}
  - {statement: 显式占位＋精确元数＋唯一 variadic 例外是保强度且可机器校的唯一形态, basis: F1–F5, strength: strong}
open_obligations: []         # 本次未产生新勘察任务；has 的未知已由后续 ADR 关闭
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
