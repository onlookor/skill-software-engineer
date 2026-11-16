---
stage: "S3-verify"
title: "验证"
requirements:
  entry_gate: "S2 已出门（fix.patch 存在且过门）"
  config: ["test_command", "repro_timeout_seconds"]
inputs:
  - "fix.patch"
  - "repro.md"
steps:
  - "git stash／干净检出，确认工作区无未提交改动"
  - "第①段：base 上跑复现命令，记录退出码（应 ≠ 0）"
  - "第②段：应用 fix.patch，跑复现命令与全量测试，记录退出码（均应为 0）"
  - "第③段：撤销 fix.patch，再跑复现命令，记录退出码（应 ≠ 0）"
  - "写 verify.log（含 test_command_used 原文；三段各含 command／exit_code／started_at／duration）与 fix-report.md"
outputs:
  - "verify.log"
  - "fix-report.md"
gate:
  - "从干净检出起跑，三段命令顺序固定：①base 上复现失败 ②应用补丁后复现转绿且全量测试绿 ③撤销补丁后复现再次失败"
  - "verify.log 记录 commit、patch sha256、每段命令、退出码、时间戳"
  - "三段缺一即 fail"
on_fail:
  - "任一段不成立 → fail，fix-report 写「未修复」，禁止降级为 pass"
validators: ["V08"]
---

# S3 验证

## 输入

- `fix.patch`（S2 输出，已过门）
- `repro.md`（S1 输出）
- 依赖的挂载期配置：`test_command`、`repro_timeout_seconds`。未约定 → `cannot_evaluate`。

S2 未出门即写 `verify.log` 属跳步；检出即停，回 S2。

## 步骤

1. `git stash`／干净检出，确认工作区无未提交改动；记录 commit。
2. 第①段：base 上跑复现命令，记录退出码。
3. 第②段：应用 `fix.patch`，跑复现命令与全量测试，记录退出码。
4. 第③段：撤销 `fix.patch`，再跑复现命令，记录退出码。
5. 写 `verify.log`（`test_command_used` 记逐字原文）与 `fix-report.md`。

## 输出

- `verify.log`
- `fix-report.md`

`fix-report.md` 是本 stage 的内部产物，不构成第五种出口交付物类型。

### `fix-report.md` 的机器可读部分

Markdown 前的 YAML frontmatter（V06／V09 读取）：

```yaml
---
status: fixed | fixed_unverified_root_cause | not_fixed
patch_sha256: <64 位小写十六进制>
touched_files:
  - <path>
evidence_kind: direct | indirect | hypothesis
---
```

- `evidence_kind: hypothesis` 时 `status` 不得写 `fixed`。
- 无人复核 V09 时 `status` 只能是 `fixed_unverified_root_cause`。
- 任一段验证不成立时 `status` 写 `not_fixed`。

## 通过门（全机器判）

1. 从干净检出起跑，三段命令顺序固定：**①base 上复现失败 ②应用补丁后复现转绿且全量测试绿 ③撤销补丁后复现再次失败**。
2. `verify.log` 记录 commit、patch sha256、每段命令、退出码、时间戳。
3. **三段缺一即 fail。**

判定者：V08。第③段（撤销后复败）是防「碰巧通过」的最低成本替代。

## 失败处理

- **任一段不成立 → fail，`fix-report` 写「未修复」，禁止降级为 pass。**
- 不得把「第二段绿」单独当成功；不得跳过第①或第③段。
- `evidence_kind` 为 `hypothesis` 时，`fix-report.md` 的状态只能是 `fixed_unverified_root_cause`，不得写 `fixed`；无人复核 V09 时状态保持该值，不得升格。
