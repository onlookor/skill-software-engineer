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

## 输出

- `verify.log`
- `fix-report.md`

`fix-report.md` 是本阶段的内部产物，不构成第五种交付物类型。

### `fix-report.md` 的机器可读部分

Markdown 前的 YAML 头（V06／V09 读取）：

```yaml
---
status: fixed | fixed_unverified_root_cause | not_fixed
patch_sha256: <64 位小写十六进制>
touched_files:
  - <path>
evidence_kind: direct | indirect | hypothesis
v09_signoff:            # 仅当 status: fixed 时必填
  reviewer: <非空身份>
  date: <ISO-8601>
---
```

- `evidence_kind: hypothesis` 时 `status` 不得写 `fixed`。
- 无人复核 V09 时 `status` 只能是 `fixed_unverified_root_cause`；写 `fixed` 必须带 `v09_signoff`（复核者身份＋日期），否则 **V08 判 fail**。
- **V09 签字的边界**：V08 只能检查 `v09_signoff.reviewer` 非空、`date` 是 ISO-8601，**不能证明签字人真的做过复核、也不能证明其身份**。字段填谁都一样通过。`fixed` 是否成立最终由人负责，V08 只挡住「写 `fixed` 却连签字字段都没有」这一种情况。
- 任一段验证不成立时 `status` 写 `not_fixed`。

## 通过条件（全部由自动检查判定）

1. 从干净检出起跑，三段命令顺序固定：**①修复前复现失败 ②应用补丁后复现转绿且全量测试绿 ③撤销补丁后复现再次失败**。
2. `verify.log` 记录 commit、patch sha256、每段命令、退出码、时间戳。
3. **三段缺一即 fail。**

判定者：V08。V08 不只读日志：它核对 `commit` 与 HEAD、识别已跟踪文件的脏改动，并实际重跑三段；第②段把**复现命令与测试命令分开单独重跑**，各自必须为 0（整条命令为 0 不能代替复现转绿），结束后撤销补丁。第③段（撤销后再次失败）是防「碰巧通过」的最低成本替代。

## 失败处理

- **任一段不成立 → fail，`fix-report` 写「未修复」，禁止降级为 pass。**
- 不得把「第二段绿」单独当成功；不得跳过第①或第③段。
- `evidence_kind` 为 `hypothesis` 时，`fix-report.md` 的状态只能是 `fixed_unverified_root_cause`，不得写 `fixed`；无人复核 V09 时状态保持该值，不得升格（写 `fixed` 而无 `v09_signoff` 会被 V08 判 fail）。
