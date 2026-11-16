# 交付物 schema：`verify.log`

> 归属 stage：S3。位置：仓根。文件名沿用 `.log`，内容为结构化 YAML（便于确定性判定）。

## 必填字段

| 字段 | 类型 | 约束 | 机器可判 | 只能人判 |
|---|---|---|---|---|
| `run_id` | string | 非空；唯一标识本次验证 | 存在且非空 | — |
| `commit` | string | 7–40 位十六进制；干净检出时的 HEAD | 存在且格式合法 | 是否确为干净检出 |
| `patch_sha256` | string | 64 位小写十六进制；等于 `fix.patch` 字节 sha256 | V08 比对 | — |
| `test_command_used` | string | 本次验证所用 `test_command` 的**逐字原文**，含缓存与构建产物相关部分；与挂载期配置快照逐字一致 | 非空、单行、与快照逐字一致（V08） | 该命令的缓存处理是否足以排除缓存与构建产物复用；是否确为本次实际执行的命令 |
| `phases` | list | 恰好 3 项，`phase` 依次为 1、2、3 | 顺序与条数 | — |
| `phases[].command` | string | 非空、单行 | 与 `repro.md`／`test_command` 的包含关系 | — |
| `phases[].exit_code` | integer | ①≠0 ②=0 ③≠0 | 退出码序列 | — |
| `phases[].started_at` | string | ISO-8601 | 可解析 | 时间是否属实 |
| `phases[].duration` | number 或 string | 非空 | 存在 | — |

## 三段语义（顺序固定，缺一即 fail）

1. base 上复现失败：`command` 含 `repro.md` 的 `command`。
2. 应用补丁后复现转绿且全量测试绿：`command` 同时含 `repro.md` 的 `command` 与挂载期 `test_command`。
3. 撤销补丁后复现再次失败：`command` 含 `repro.md` 的 `command`。

`test_command_used` 独立于三段 `command`：它记的是本次验证采用的全量测试命令原文，供读者判断第③段结论是否受缓存与构建产物复用影响。

## 模板（占位符不是值）

```yaml
run_id: "<string>"
commit: "<7–40 位十六进制>"
patch_sha256: "<64 位小写十六进制>"
test_command_used: "<挂载期 test_command 的逐字原文>"
phases:
  - phase: 1
    command: "<单行命令>"
    exit_code: <非零整数>
    started_at: "<ISO-8601>"
    duration: <number|string>
  - phase: 2
    command: "<同时含复现命令与全量测试命令的单行命令>"
    exit_code: <整数>
    started_at: "<ISO-8601>"
    duration: <number|string>
  - phase: 3
    command: "<单行命令>"
    exit_code: <非零整数>
    started_at: "<ISO-8601>"
    duration: <number|string>
```

## 判不了的部分

- `test_command_used` 的缓存处理是否**真的生效**：V08 只判逐字一致与存在性，判不了执行效果；只能人判（失效实例见 `validators/README.md`）。
- 第③段失败是否确因撤销补丁：只靠退出码序列逼近，不绝对；缓存复用的排除同样只能人判。
