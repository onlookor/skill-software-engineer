---
stage: "S2-localize-fix"
title: "定位与最小修复"
requirements:
  entry: "S1 已通过（复现记录通过、失败用例可独立失败）"
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
  - "测试路径下已有文件零改动（diff 中 tests/ 与 *_test.* 的任何增删行）；只允许新增 tests/repro_* 测试文件"
  - "localization.md 的成因结论必须带 evidence_kind 标注（direct│indirect│hypothesis）"
on_fail:
  - "补丁不转绿 → 回滚补丁、保留定位记录，回 S1 复核复现，或判 blocked"
  - "必须改测试才能转绿 → fail（禁止）；在报告写明「修复未成立」"
validators: ["V04", "V05", "V06", "V07"]
---

# S2 定位与最小修复

## 输入

- `repro.md`（S1 输出，已通过）
- `tests/repro_<slug>.<ext>`（S1 输出）
- 依赖的使用前约定项：`test_command`、`allowed_scope`。未约定 → `cannot_evaluate`。

S1 未通过就进入本阶段属跳步；发现即停，回 S1。

## 步骤

1. 读失败栈与复现日志。
2. 用二分／日志／调用链把范围缩到文件与符号。
3. 写 `localization.md`：机制断言＋证据＋`evidence_kind`（`direct` │ `indirect` │ `hypothesis`）。
   - `direct` 仅当能在日志／栈中直接指出成因语句；
   - 无直接证据时只能是 `hypothesis`，不得写成结论句。
4. 写最小 diff，落为 `fix.patch`（统一 diff 格式，含 `touched_files`、`patch_sha256`）。
5. 跑「复现用例」与「既有测试」两条命令（后者命令与 S1 相同）。

## 输出

- `localization.md`
- `fix.patch`

`localization.md` 随 `fix.patch` 一起交出；它是本阶段的内部产物，不构成第五种交付物类型。

### `localization.md` 的机器可读部分

Markdown 前的 YAML 头（V05／V06／V09 读取）：

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

## 通过条件（前四条由自动检查判定；第五条只在「标注存在且取值合法」这一层自动判）

1. 复现用例转绿。
2. 既有测试全绿（命令与 S1 相同）。
3. `fix.patch` 只触及 `localization.md` 列出的文件。
4. 测试路径下已有文件零改动（`tests/` 与 `*_test.*` 的任何增删行，含测试数据与夹具）；只允许新增 `tests/repro_*` 测试文件。
5. `localization.md` 的成因结论必须带 `evidence_kind` 标注（`direct` │ `indirect` │ `hypothesis`）。

判定者：V04（能否干净应用）、V05（改动范围黑名单）、V06（测试路径零改动、最小性对照、措辞黑名单）、V07（既有测试全绿）。
第 5 条的标注是否**成立**只能由人判断，见 V09。

**最小性对照（V06 判定）**：`touched_files` 数与 diff 行数须与 `localization.md` 的 `estimated_touched_files`／`estimated_diff_lines` 一致。缺失或不一致 → **V06 判 fail**，须按实际改动重写 `localization.md`，并把 `evidence_kind` 按 `hypothesis` 处理。这里选择判 fail 而不是静默改值：静默降级会掩盖「预估与实际不符」这件事本身。

## 失败处理

- **补丁不转绿 → 回滚补丁、保留定位记录，回 S1 复核复现，或判 `blocked`。**
- **必须改测试才能转绿 → fail（禁止）；在报告写明「修复未成立」。**
- 若 S1 已确认可复现而 S2 无解，标 `blocked`，不得以「部分修复」结案。
- 不得为了通过而放宽断言、改验收命令或扩大 `allowed_scope`。
