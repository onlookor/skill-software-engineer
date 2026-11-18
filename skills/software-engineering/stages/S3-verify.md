---
stage: "S3-verify"
title: "验证"
requirements:
  entry: "S2 已通过（fix.patch 存在且通过）"
  config: ["test_command", "repro_timeout_seconds"]
inputs:
  - "fix.patch"
  - "repro.md"
steps:
  - "git stash／干净检出，确认工作区无未提交改动"
  - "第①段：修复前跑复现命令，记录退出码（应 ≠ 0）"
  - "第②段：应用 fix.patch，跑复现命令与全量测试，记录退出码（均应为 0）"
  - "第③段：撤销 fix.patch，再跑复现命令，记录退出码（应 ≠ 0）"
  - "写 verify.log（含 test_command_used 原文；三段各含 command／exit_code／started_at／duration）与 fix-report.md"
outputs:
  - "verify.log"
  - "fix-report.md"
gate:
  - "从干净检出起跑，三段命令顺序固定：①修复前复现失败 ②应用补丁后复现转绿且全量测试绿 ③撤销补丁后复现再次失败"
  - "verify.log 记录 commit、patch sha256、每段命令、退出码、时间戳"
  - "三段缺一即 fail"
on_fail:
  - "任一段不成立 → fail，fix-report 写「未修复」，禁止降级为 pass"
validators: ["V08"]
---

# S3 验证

## 输入

- `fix.patch`（S2 输出，已通过）
- `repro.md`（S1 输出）
- 依赖的使用前约定项：`test_command`、`repro_timeout_seconds`。未约定 → `cannot_evaluate`。

S2 未通过就写 `verify.log` 属跳步；发现即停，回 S2。

## 步骤

1. `git stash`／干净检出，确认工作区无未提交改动；记录 commit。
2. 第①段：修复前跑复现命令，记录退出码。
3. 第②段：应用 `fix.patch`，跑复现命令与全量测试，记录退出码。
4. 第③段：撤销 `fix.patch`，再跑复现命令，记录退出码。
5. 写 `verify.log`（`test_command_used` 记逐字原文）与 `fix-report.md`。
6. 比对由引导完成：测试里的 `observe()` 只返回观测值，期望值来自 `repro.md.observations`；失败摘要写 `observation mismatch: <id> expected=… observed=…`，不得改写为断言错误。

## 输出

- `verify.log`
- `fix-report.md`

`fix-report.md` 是本阶段的内部产物，不构成第五种交付物类型。

### `fix-report.md` 的机器可读部分

Markdown 前的 YAML 头（V06／V09 读取）：

```yaml
---
status: fixed_unverified_root_cause | not_fixed
patch_sha256: <64 位小写十六进制>
touched_files:
  - <path>
evidence_kind: direct | indirect | hypothesis
---
```

- `evidence_kind: hypothesis` 时 `status` 不得写 `fixed`。
- 自动检查阶段 `status` 只能是 `fixed_unverified_root_cause` 或 `not_fixed`。**写 `fixed` 会被 V08 直接判 fail**：V09 必须人工执行，`v09_signoff` 等仓内字段可由执行方书写，不能作为复核成立的证据。
- 人工复核（V09）在自动检查之外进行，其结论不通过修改仓内字段来「自动成立」；详见 [validators/README.md 的「已知边界」](../validators/README.md#已知边界天花板)。
- 任一段验证不成立时 `status` 写 `not_fixed`。

## 通过条件（全部由自动检查判定）

1. 从干净检出起跑，三段命令顺序固定：**①修复前复现失败 ②应用补丁后复现转绿且全量测试绿 ③撤销补丁后复现再次失败**。
2. `verify.log` 记录 commit、patch sha256、每段命令、退出码、时间戳。
3. **三段缺一即 fail。**

判定者：V08。V08 不只读日志：它核对 `commit` 与 HEAD、识别已跟踪文件的脏改动，并实际重跑三段；第②段把**复现命令与测试命令分开单独重跑**，各自必须为 0（整条命令为 0 不能代替复现转绿），结束后撤销补丁。第③段（撤销后再次失败）是防「碰巧通过」的最低成本替代。

**执行证据**：第①段（base）与第②段的复现命令都在受控执行下采集覆盖行（含测试自己新建的线程与其拉起的子进程）。补丁在生产代码上删除的行必须在 base 态被复现测试执行到，新增的行必须在 patched 态被执行到；任一交集为空即 fail（理由：补丁行未被复现测试覆盖，无法证明该测试与修复相关）。每次受控执行还做**采集入口完整性**比对：引导在导入仓内代码前对 `trace`／`threading`/`sys.settrace`／`runpy.run_path`／`builtins` 执行入口／`sys.modules` 基线留可信原件，执行后逐项比对；被替换且未复原即 cannot_evaluate。它只能发现「替换后不复原」的改写，自恢复与 `os._exit` 提前退出发现不了。复现测试还须通过 `under_test` 入口限制与白名单（V03／V08 同判）：不 `import unittest`、不 `assert`、不用 `self.assertEqual`；只定义无参 `observe()` 返回 `observation_id → 观测值`，每个观测值必须直接是被测入口的调用；期望值只来自 `repro.md.observations` 的字面量，比对由引导自己完成。

**变异检验**：V08 还会对补丁触及的每一行生产代码造变异（翻转比较符、换运算符、常量 ±1、布尔取反），删除行做整块回退，在 patched 态重跑复现测试；测试必须出现**观测值与期望值不一致**（引导报告 `ObservationMismatch`）。崩溃、超时、`SystemExit`／`os._exit` 等提前退出都不算杀死变异——它们没走到比对。全部变异都存活，或整份补丁造不出可编译变异 → fail（理由：补丁行未被测试敏感覆盖）；docstring／注释／类型注解／`pass`／纯字符串这类改不动的行不产生变异，不能当作通过证据。纯新增补丁没有 base 侧删除行，但新增行同样要过这一关。

上述证据只证明「测试执行过补丁行，且对补丁行的正常变异产生观测值不一致」，不证明「该行就是根因」，也不证明「测试或生产补丁没有伪造证据」。引导不经过任何断言设施，因此改写 `unittest` 对判定无效；但**观测输入与期望值的语义独立性、以及同进程篡改仍判不了**（例如选用两态同值的输入、只把补丁新加的常量作为观测值、测试主动写回覆盖率 fd）；这条由 V09 第 8 项人工兜，不得写成「已解决」。

## 失败处理

- **任一段不成立 → fail，`fix-report` 写「未修复」，禁止降级为 pass。**
- 不得把「第二段绿」单独当成功；不得跳过第①或第③段。
- `evidence_kind` 为 `hypothesis` 时，`fix-report.md` 的状态只能是 `fixed_unverified_root_cause`；自动检查阶段一律保持该值，不得写 `fixed`（写 `fixed` 会被 V08 直接判 fail）。
