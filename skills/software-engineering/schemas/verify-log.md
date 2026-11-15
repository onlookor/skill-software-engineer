# 交付物 schema：`verify.log`

> 归属 stage：S3。位置：仓根。文件名沿用 `.log`，内容为结构化 YAML（便于确定性判定）。

## 必填字段

| 字段 | 类型 | 约束 | 机器可判 | 只能人判 |
|---|---|---|---|---|
| `run_id` | string | 非空；唯一标识本次验证 | 存在且非空 | — |
| `commit` | string | 7–40 位十六进制；干净检出时的 HEAD | 存在且格式合法 | 是否确为干净检出 |
| `patch_sha256` | string | 64 位小写十六进制；等于 `fix.patch` 字节 sha256 | V08 比对 | — |
| `phases` | list | 恰好 3 项，`phase` 依次为 1、2、3 | 顺序与条数 | — |
| `phases[].command` | string | 非空、单行 | 与 `repro.md`／`test_command` 的包含关系 | — |
| `phases[].exit_code` | integer | ①≠0 ②=0 ③≠0 | 退出码序列 | — |
| `phases[].started_at` | string | ISO-8601 | 可解析 | 时间是否属实 |
| `phases[].duration` | number 或 string | 非空 | 存在 | — |

## 三段语义（顺序固定，缺一即 fail）

1. base 上复现失败：`command` 含 `repro.md` 的 `command`。
2. 应用补丁后复现转绿且全量测试绿：`command` 同时含 `repro.md` 的 `command` 与挂载期 `test_command`。
3. 撤销补丁后复现再次失败：`command` 含 `repro.md` 的 `command`。

## 模板（占位符不是值）

```yaml
run_id: "<string>"
commit: "<7–40 位十六进制>"
patch_sha256: "<64 位小写十六进制>"
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

- 无。日志是纯证据，不作判断；绿是否由本次补丁引起，只靠第③段逼近，不绝对。
