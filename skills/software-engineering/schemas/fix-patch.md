# 交付物 schema：`fix.patch`

> 归属阶段：S2。位置：仓根。一件可验收：文件本体必须是可 `git apply` 的 unified diff。

## 必填字段（三项，均由文件本体派生）

| 字段 | 类型 | 载体与约束 | 可自动判定 | 只能由人判断 |
|---|---|---|---|---|
| unified diff | text | 文件本体；`git apply --check` 通过 | V04 | — |
| `touched_files` | list<path> | 从 `diff --git a/… b/…` 行解析；必须 ⊆ `localization.md` 的 `files`，且 ⊆ `allowed_scope` | V05 | 范围本身是否完整（漏文件判不了） |
| `patch_sha256` | string | 文件字节的 SHA-256（小写十六进制）；由 V08 与 `verify.log` 比对 | V08 | — |

`touched_files` 与 `patch_sha256` 不另写清单文件：前者可从 diff 头行确定性导出，后者可从文件字节确定性计算；两者均记录在 `verify.log` 与 `fix-report.md` 中供复核。

## 硬约束

- 只触及 `localization.md` 列出的文件。
- 测试路径零改动：`tests/` 与 `*_test.*` 下**已有文件**不得出现任何增删行（断言、测试数据、夹具一律不改）；只允许新增 `tests/repro_*` 失败测试文件。
- 不得为了让检查通过而改验收命令、放宽断言或扩大 `allowed_scope`。
- 最小性对照：`touched_files` 数与 diff 行数须与 `localization.md` 的 `estimated_touched_files`／`estimated_diff_lines` 一致；缺失或不一致即由 V06 判 fail，须按实际重写 `localization.md`，并把 `evidence_kind` 按 `hypothesis` 处理。

## 模板（占位符不是值）

```diff
diff --git a/<path> b/<path>
--- a/<path>
+++ b/<path>
@@ <hunk> @@
 <context>
-<removed>
+<added>
```

## 判不了的部分

- 补丁语义是否正确：V04 只判可应用，不判语义。
- 改动是否「最小」：没有可自动判定的标准；只登记 `touched_files` 数与 diff 行数供复核。
- 是否以其他方式把测试变恒真：V06 判「测试目录已有文件零改动」与「新增文件必须是 repro_*」，但新增 repro 测试内部是否恒真只由 V03 的固定写法识别兜底。
