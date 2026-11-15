---
stage: "S2-localize-fix"
title: "定位与最小修复"
requirements:
  entry_gate: "S1 已出门（repro.md 过门、失败用例可独立失败）"
  config: ["test_command", "allowed_scope"]
inputs:
  - "repro.md"
  - "tests/repro_<slug>.<ext>"
steps:
  - "读失败栈与复现日志"
  - "用二分／日志／调用链把范围缩到文件与符号"
  - "写 localization.md（机制断言＋证据＋evidence_kind）"
  - "写最小 diff → fix.patch"
  - "跑「复现用例」与「既有测试」两条命令"
outputs:
  - "localization.md"
  - "fix.patch"
gate:
  - "复现用例转绿"
  - "既有测试全绿（命令与 S1 相同）"
  - "fix.patch 只触及 localization.md 列出的文件"
  - "fix.patch 的测试断言行零改动（diff 中 tests/ 与 *_test.* 的断言行）"
  - "localization.md 的成因结论必须带 evidence_kind 标注（direct│indirect│hypothesis）"
on_fail:
  - "补丁不转绿 → 回滚补丁、保留定位记录，回 S1 复核复现，或判 blocked"
  - "必须改测试才能转绿 → fail（禁止）；在报告写明「修复未成立」"
validators: ["V04", "V05", "V06", "V07"]
---

# S2 定位与最小修复

## 输入

- `repro.md`（S1 输出，已过门）
- `tests/repro_<slug>.<ext>`（S1 输出）
- 依赖的挂载期配置：`test_command`、`allowed_scope`。未约定 → `cannot_evaluate`。

S1 未出门即进入本 stage 属跳步；检出即停，回 S1。

## 步骤

1. 读失败栈与复现日志。
2. 用二分／日志／调用链把范围缩到文件与符号。
3. 写 `localization.md`：机制断言＋证据＋`evidence_kind`（`direct` │ `indirect` │ `hypothesis`）。
   - `direct` 仅当能在日志／栈中直接指出成因语句；
   - 无直接证据时只能是 `hypothesis`，不得写成结论句。
4. 写最小 diff，落为 `fix.patch`（unified diff，含 `touched_files`、`patch_sha256`）。
5. 跑「复现用例」与「既有测试」两条命令（后者命令与 S1 相同）。

## 输出

- `localization.md`
- `fix.patch`

`localization.md` 随 `fix.patch` 一起交出；它是本 stage 的内部产物，不构成第五种出口交付物类型。

### `localization.md` 的机器可读部分

Markdown 前的 YAML frontmatter（V05／V06／V09 读取）：

```yaml
---
evidence_kind: direct | indirect | hypothesis
files:                      # 本补丁允许触及的文件或目录（仓内相对路径）
  - <path>
estimated_touched_files: <integer>
estimated_diff_lines: <integer>
---
```

正文写机制断言与证据。`files` 之外的文件不得出现在 `fix.patch` 中；`evidence_kind` 非法或缺席即 V06 fail。

## 通过门（前四条机器判；第五条只在「标注存在且取值合法」这一层机器判）

1. 复现用例转绿。
2. 既有测试全绿（命令与 S1 相同）。
3. `fix.patch` 只触及 `localization.md` 列出的文件。
4. `fix.patch` 的测试断言行零改动（diff 中 `tests/` 与 `*_test.*` 的断言行）。
5. `localization.md` 的成因结论必须带 `evidence_kind` 标注（`direct` │ `indirect` │ `hypothesis`）。

判定者：V04（`git apply --check`）、V05（范围黑名单）、V06（断言行与措辞黑名单）、V07（既有测试全绿）。
第 5 条的标注是否**成立**靠人判，见 V09。

**最小性对照**：`touched_files` 数与 diff 行数须与 `localization.md` 的预估一致；不一致即把 `evidence_kind` 强制降为 `hypothesis`。

## 失败处理

- **补丁不转绿 → 回滚补丁、保留定位记录，回 S1 复核复现，或判 `blocked`。**
- **必须改测试才能转绿 → fail（禁止）；在报告写明「修复未成立」。**
- 若 S1 已确认可复现而 S2 无解，标 `blocked`，不得以「部分修复」结案。
- 不得为了过门而放宽断言、改验收命令或扩大 `allowed_scope`。
