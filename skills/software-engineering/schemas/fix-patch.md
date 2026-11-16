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
- 测试断言行零改动（`tests/` 与 `*_test.*` 的断言行）。
- 不得为了让检查通过而改验收命令、放宽断言或扩大 `allowed_scope`。
- 最小性对照：`touched_files` 数与 diff 行数须与 `localization.md` 的预估一致；不一致即把 `evidence_kind` 强制降为 `hypothesis`。

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
- 是否以其他方式把断言变恒真：V06 只扫断言行与措辞，不判等价改写。
