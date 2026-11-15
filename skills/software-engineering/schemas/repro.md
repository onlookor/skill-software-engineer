# 交付物 schema：`repro.md`

> 归属 stage：S1。位置：仓根。一件可验收；缺字段或类型错即 S3 fail。

## 形态

Markdown，正文前必须有一段 YAML frontmatter（首行 `---`，闭合 `---`）。正文写复现说明，不参与机器判。

## 必填字段（八项）

| 字段 | 类型 | 约束 | 机器可判 | 只能人判 |
|---|---|---|---|---|
| `repo` | map | 含 `url`（非空字符串）、`commit`（7–40 位十六进制） | 齐全且类型正确 | — |
| `env` | map | 含 `os`（字符串）、`runtime`（字符串）、`dependencies`（map<string,string>） | 齐全且类型正确 | 版本是否与用户环境同构 |
| `command` | string | 非空、单行、可直接执行 | 可执行（V02 实际运行） | 是否是用户实际使用的入口 |
| `expected` | string | 非空 | 存在且非空 | 期望值是否来自用户而非 agent 自拟 |
| `actual` | string | 非空 | 存在且非空 | `actual` 与用户所述失败是否同一件事 |
| `exit_code` | integer | ≠ 0 | 否（V02 以实跑为准） | — |
| `fingerprint` | map | 含 `run1`、`run2`（字符串），按下方归一化规则计算 | `run1 == run2`，且与 V02 实跑所算一致 | — |
| `first_observed` | string | ISO-8601 日期或日期时间 | 可解析 | 时间是否属实 |

## 失败指纹的归一化规则（唯一口径）

对一次运行的 stdout＋stderr 合并文本，依次：

1. 去掉 ANSI 转义序列；
2. 把仓库绝对路径替换为 `<repo>`；
3. 把 `0x` 开头的十六进制串替换为 `<addr>`；
4. 把形如数字＋`s`／`ms`／`us` 的耗时片段替换为 `<t>`；
5. 把连续空白折叠为单个空格并去首尾空白；
6. 取 SHA-256，十六进制小写。

指纹定义＝「异常类型＋关键栈帧＋断言差异」的文本化结果；上述规则只负责把它变成可比较的定长串。

## 模板（占位符不是值）

```markdown
---
repo:
  url: <string>
  commit: <7–40 位十六进制>
env:
  os: <string>
  runtime: <string>
  dependencies:
    <name>: <version>
command: <单行命令>
expected: <string>
actual: <string>
exit_code: <非零整数>
fingerprint:
  run1: <归一化 SHA-256>
  run2: <归一化 SHA-256>
first_observed: <ISO-8601>
---

<复现说明：设备、步骤、与用户所述失败的对应关系；不参与机器判。>
```

## 判不了的部分

- `actual` 与用户报的问题是否同一件事：V01/V02 都不判，只能人判。
- `expected` 是否忠于用户意图：同上。
- `exit_code` 字段可以被写错；V02 以实跑退出码为准，不采信该字段。
