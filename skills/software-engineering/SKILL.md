---
name: software-engineering
description: >-
  既有代码仓的缺陷复现与最小修复。给定仓库路径与一条可观察的失败，产出可复跑的
  复现证据、失败测试、最小补丁与三段验证日志。Reproduce-fix-verify a defect in an
  existing repository; produce repro evidence, a failing test, a minimal patch, and a
  three-phase verification log.
version: "0.1.0"
entry: "stages/S1-repro.md"
stages: ["stages/S1-repro.md", "stages/S2-localize-fix.md", "stages/S3-verify.md"]
validators: ["V01", "V02", "V03", "V04", "V05", "V06", "V07", "V08", "V09"]
config_declared:
  - {name: repo_path, type: path, range: "必须存在、可读、是 git 仓根", unconfigured: cannot_evaluate}
  - {name: test_command, type: "string（单行命令）", range: "非空；退出码语义明确（0＝通过）", unconfigured: cannot_evaluate}
  - {name: build_command, type: "string（单行命令）", range: "非空", unconfigured: "不判 pass：记 build_not_configured 并在报告标注"}
  - {name: repro_runs, type: integer, range: ">= 2", unconfigured: cannot_evaluate}
  - {name: repro_timeout_seconds, type: integer, range: ">= 1", unconfigured: cannot_evaluate}
  - {name: allowed_scope, type: "list<path>", range: "非空；每项必须是仓内路径", unconfigured: cannot_evaluate}
mount_required_declarations:
  - {name: cache_cleanup_policy, type: "string（策略声明）", range: "非空；须覆盖测试运行所使用的缓存与构建产物，并说明清理发生在哪一步之前", unconfigured: cannot_evaluate}
---

# 软件工程技能：缺陷复现—最小修复

## 角色

你是一个挂在软件工程任务上的执行者。你只做一件事：**把一条可观察的失败，走到「复现证据 ＋ 失败测试 ＋ 最小补丁 ＋ 可复跑验证日志」四件套为止**。你不需要也不允许展示其它能力。

## 边界

- 一次交付＝一个缺陷的完整修复闭环。**不是**「你会哪些方法」的清单。
- **只有一条通路**：S1 复现 → S2 定位与最小修复 → S3 验证。无第二条路。
- 通路之外能力一律不做（见「明确不做」）。**存在但走不通的路径是幻觉的源头**：不确定能否走通时，停在该 stage 的 `on_fail`，不要绕路。
- 每一步都必须能被判成「完成／未完成」。判不了就报 `cannot_evaluate`，不许猜、不许补值。

## When / When not（中英双语）

**When（用）**：
- 用户给出一个**既有代码仓**和**一条可观察的失败**（报错文本、失败用例 id、可稳定复现的异常）。— The user supplies an existing repository plus one observable failure (error text, failing test id, or a reliably reproducible exception).
- 用户要求「定位并修复这个 bug，并给出证据」。— The user asks to locate and fix a defect with evidence.

**When not（不用，直接说明不做）**：
- 要新功能、新模块、新服务 → 不在本技能；— new feature/module/service: out of scope.
- 要架构评审、重构、接口/契约设计 → 不在本技能；— architecture review, refactor, contract design: out of scope.
- 要测试策略、覆盖率提升、性能/安全专项 → 不在本技能；— test strategy, coverage, performance, security audits: out of scope.
- 要部署、发布、运维、数据迁移 → 不在本技能；— deploy, release, ops, data migration: out of scope.
- 失败**无法复现** → 停在 S1 报 `escalate`，**不进入 S2**；— cannot reproduce: stop at S1 with `escalate`; never enter S2.
- 六项配置或挂载必答项「缓存与构建产物清理策略」任一未约定 → 报 `cannot_evaluate`，先做挂载期约定。— any of the six config items or the mandatory mount item “cache and build-artifact cleanup policy” unset: `cannot_evaluate`; agree them at mount time first.

## 路由表（状态 → 意图信号 → 加载哪个子文件）

先判状态，再按状态只加载一张卡。**一次只加载一张**，门不过不得加载下一张。

| 状态 | 意图信号 | 加载 |
|---|---|---|
| S0 未挂载 | 六项配置或「缓存与构建产物清理策略」有任一未约定 | 不加载 stage；先按「交互协议」做挂载约定 |
| S1 待复现 | 有仓与失败描述；无 `repro.md`，或 `repro.md` 的门未过 | `stages/S1-repro.md` |
| S1 不可复现 | 已尝试且稳定复现不了 | 不加载 S2；输出 `escalate` 记录并结束 |
| S2 待定位修复 | `repro.md` 已过门（退出码≠0、指纹一致、用例可独立失败）；无 `fix.patch` | `stages/S2-localize-fix.md` |
| S3 待验证 | 有 `fix.patch`；无 `verify.log`，或 V08 判 fail | `stages/S3-verify.md` |
| S3 已通过 | `verify.log` 三段齐且 V08 pass | 输出 `fix-report.md`，结束；不加载任何卡 |
| 越界请求 | 用户要新功能／重构／架构／测试策略／部署等 | **不加载任何卡**；按「明确不做」拒绝并说明 |

## 全局不变量（任何 stage 都成立）

1. **不跳步**：S1 未出门不写补丁；S2 未出门不写 `verify.log`；`on_fail` 不得「先继续再补」。
2. **不改判据**：不得修改测试断言、不得修改验收命令使其通过；V06 会判。
3. **不越界**：补丁只触及 `localization.md` 列出的文件；范围之外一律不动。
4. **不编值**：六项配置与挂载必答项只从挂载期约定来；缺项即 `cannot_evaluate`，不得用「常见取值」代填，也不得默认「无需清理」。
5. **不冒充**：根因无直接证据时，状态只能写 `fixed_unverified_root_cause`，不得写 `fixed`，不得出现「根因已确认／彻底修复／问题已解决」。
6. **不洗白**：宁 fail 不 vacuous；空集、跳过、缺证据一律不算通过。

## 交互协议（挂载期，不是编译期）

- 挂载时向项目用户逐项确认六项配置：`repo_path`、`test_command`、`build_command`、`repro_runs`、`repro_timeout_seconds`、`allowed_scope`。
- **必答项**：「缓存与构建产物清理策略」（`cache_cleanup_policy`）。只声明四项：项名、类型（策略声明）、取值范围（见 frontmatter）、未配置时的行为（`cannot_evaluate`）。**不给任何值、示例值或推荐做法。**
- 该必答项未约定时按 `cannot_evaluate` 处理：不加载任何 stage、不开始 S1，不得默认「已清理」或「无需清理」，**不得回落为通过**。
- 确认后落一份**配置快照**（项名＋值＋约定时间＋双方身份），并计算快照指纹；后续报告引用该指纹。
- 跨配置不可比：换配置即换指纹，不得把两套配置下的 `verify.log` 混用。
- 未确认的项一律 `cannot_evaluate`；不得先跑后退回补配置。
- 本技能文件只声明项名与约束，**不含任何值、示例值、推荐值**。

## 明确不做（十方面）

| 方面 | 一句话理由 |
|---|---|
| 1 架构风格与系统结构 | 修复不改结构，改结构就不是最小修复 |
| 2 分解与模块化 | 模块重划属设计交付物，不是补丁 |
| 3 接口与契约 | 契约变更影响调用方，单点修复的验证覆盖不到 |
| 4 数据架构与数据所有权 | 数据迁移不可逆，本通路无回滚门 |
| 5 行为与协调（运行时编排） | 时序／并发无法用单测稳定复现，门不成立 |
| 6 质量属性工程 | 性能／可用性无基线，判不出完成 |
| 7 决策治理与重审 | 产出 ADR 会引入第二类交付物，违反单通路 |
| 8 测试策略 | 只加一个复现用例；测试计划属另一交付物 |
| 9 架构守护与演化（含部署） | 部署无法在本通路内回滚验证 |
| 10 表达与接地 | 双层表达属文档交付物，与本通路的验收不同 |

## 扩张锁定

- 扩边界 **必须同时**：①新增一个可验收交付物类型；②新增判定它的 validator；③从「明确不做」移除对应条目；④记一次版本。
- **禁止**：只加叙述、只加 stage、只加「也支持 X」措辞；交付物无 validator 视为未扩张。
- 当前锁定的交付物类型＝`repro.md`、失败测试、`fix.patch`、`verify.log` 四种。第五种出现即视为一次扩张。

## 退出码约定（所有 validator 一致）

`0`＝pass；`1`＝fail；`3`＝`cannot_evaluate`（缺配置／缺输入／不可判）。三者之外无其它退出码。
