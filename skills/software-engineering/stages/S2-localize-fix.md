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
  - "tests/ 路径下已有文件不被改写、不被改名、不被移出 tests/（改名按 diff 的 a 侧旧路径判定）；只允许新增 tests/repro_* 测试文件"
  - "fix.patch 的改动行只允许落在普通函数／方法体或模块级声明式改动（import、模块常量、类属性／dataclass 默认值、模块级 try/except 内赋值、docstring、声明式装饰器、def／class 头）；改到模块级可执行语句判 cannot_evaluate，并写明「该缺陷需要改模块级声明，超出本技能适用面」。导入期是否发生伪造不靠语法可达性推断：受控执行引导在导入仓内代码前对断言设施、内置执行入口、trace 与采集入口、sys.modules 基线留可信原件，执行后比对，被改写即 cannot_evaluate"
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
4. `tests/` 路径下已有文件不被改写、不被改名、不被移出 `tests/`（改名按 diff 的 a 侧旧路径判定）；只允许新增 `tests/repro_*` 测试文件。该条只保护 `tests/` 路径名，不保护行为：`tests/` 之外的夹具或数据文件被改动不在 V06 覆盖范围。`.py` 夹具若被复现测试 import，会作为执行代码出现在 V08 的覆盖里，但那只说明它被执行过，不构成「夹具未被篡改」的证明；非 `.py` 数据夹具完全没有覆盖约束。
5. `localization.md` 的成因结论必须带 `evidence_kind` 标注（`direct` │ `indirect` │ `hypothesis`）。

判定者：V04（能否干净应用）、V05（改动范围黑名单）、V06（`tests/` 路径改写／改名／移出、补丁改动行的执行时机、最小性对照、措辞黑名单）、V07（既有测试全绿）。
第 5 条的标注是否**成立**只能由人判断，见 V09。

**最小性对照（V06 判定）**：`touched_files` 数与 diff 行数须与 `localization.md` 的 `estimated_touched_files`／`estimated_diff_lines` 一致。缺失或不一致 → **V06 判 fail**，须按实际改动重写 `localization.md`，并把 `evidence_kind` 按 `hypothesis` 处理。这里选择判 fail 而不是静默改值：静默降级会掩盖「预估与实际不符」这件事本身。

## 失败处理

- **补丁不转绿 → 回滚补丁、保留定位记录，回 S1 复核复现，或判 `blocked`。**
- **必须改测试才能转绿 → fail（禁止）；在报告写明「修复未成立」。**
- 若 S1 已确认可复现而 S2 无解，标 `blocked`，不得以「部分修复」结案。
- 不得为了通过而放宽断言、改验收命令或扩大 `allowed_scope`。
