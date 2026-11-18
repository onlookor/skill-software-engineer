# 交付物 schema：`repro.md`

> 归属阶段：S1。位置：仓根。一件可验收；缺字段或类型错即 S3 fail。

## 形态

Markdown，正文前必须有一段 YAML frontmatter（首行 `---`，闭合 `---`）。正文写复现说明，不参与自动判定。

## 必填字段（十项）

| 字段 | 类型 | 约束 | 可自动判定 | 只能由人判断 |
|---|---|---|---|---|
| `repo` | map | 含 `url`（非空字符串）、`commit`（7–40 位十六进制） | 齐全且类型正确 | — |
| `env` | map | 含 `os`（字符串）、`runtime`（字符串）、`dependencies`（map<string,string>） | 齐全且类型正确 | 版本是否与用户环境同构 |
| `command` | string | 非空、单行，且只能是 `python3 -I <仓内相对路径>`；脚本必须与元数据记录的测试文件是同一文件 | 形式与脚本绑定（V02 判）；实际运行（V02 在受控执行下跑） | 是否是用户实际使用的入口 |
| `under_test` | string 或 list | 非空，形如 `calc.add` 或 `calc.Calc.add`；可列多个；只允许点号函数或方法（不接受类、常量、模块名） | 入口必须真实存在且可调用；测试只能调用这些入口（V01／V03／V08 判） | 声明的入口是否就是用户报障的入口 |
| `observations` | map | 非空；键是 `observation_id`（字母／下划线开头，可含数字、点、连字符）；值是字面量（数字、字符串、`True/False/None`、字面量容器及其算术） | 键与测试 `observe()` 返回的键一一对应；值只做规范化 JSON 比较（V01／V03／V08 判） | 期望值是否来自用户而非 agent 自拟 |
| `expected` | string | 非空 | 存在且非空 | 期望值是否来自用户而非 agent 自拟 |
| `actual` | string | 非空 | 存在且非空 | `actual` 与用户所述失败是否同一件事 |
| `exit_code` | integer | ≠ 0 | 否（V02 以实跑为准） | — |
| `fingerprint` | map | 含 `run1`、`run2`（字符串），按下方归一化规则计算 | `run1 == run2`，且与 V02 实跑所算一致 | — |
| `first_observed` | string（YAML 裸日期会解析成 `date`／`datetime`，V01 一并接受） | ISO-8601 日期或日期时间 | 可解析 | 时间是否属实 |

## 测试文件契约（与 `observations` 配套）

- 测试文件**不调用任何断言 API**：不 `import unittest`、不 `assert`、不用 `self.assertEqual`。
- 只允许模块级导入、`sys.path.insert/append(…, ".")` 与一个无参函数 `observe()`（其余模块级语句一律拒绝）。
- `observe()` 返回字面量 `dict`：`observation_id → 观测值`，键集合必须与 `observations` 完全一致。
- 每个观测值必须**直接是 `under_test` 入口的调用**（`f(...)`／`mod.f(...)`／`Cls(...).m(...)`；经局部变量中转的调用不算）。
- 比对由引导完成：引导调用 `observe()`，按规范化 JSON（区分 `True` 与 `1`、`1` 与 `1.0`）比较，任一不一致即非 0 退出。

## 失败摘要的归一化规则（唯一口径）

对一次运行的 stdout＋stderr 合并文本，依次：

1. 去掉 ANSI 转义序列；
2. 把仓库绝对路径替换为 `<repo>`；
3. 把 `0x` 开头的十六进制串替换为 `<addr>`；
4. 把形如数字＋`s`／`ms`／`us` 的耗时片段替换为 `<t>`；
5. 把连续空白折叠为单个空格并去首尾空白；
6. 取 SHA-256，十六进制小写。

摘要定义＝「异常类型＋关键栈帧＋观测值差异」的文本化结果；上述规则只负责把它变成可比较的定长串。

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
command: python3 -I <仓内相对路径>
under_test: <module.entry>（或列表）
observations:
  <observation_id>: <字面量>
expected: <string>
actual: <string>
exit_code: <非零整数>
fingerprint:
  run1: <归一化 SHA-256>
  run2: <归一化 SHA-256>
first_observed: "<ISO-8601>"
---

<复现说明：设备、步骤、与用户所述失败的对应关系；不参与自动判定。>
```

## 判不了的部分

- `actual` 与用户报的问题是否同一件事：V01/V02 都不判，只能由人判断。
- `expected` 是否忠于用户意图：同上。
- `exit_code` 字段可以被写错；V02 以实跑退出码为准，不采信该字段。
- 命令虽引用了测试文件、但失败与测试无关（例如测试只读文件文本、不执行被测代码）：V02 只判「白名单命令形式、脚本绑定、非 0、输出非空、摘要一致」，不判语义；该缺口由 V08 在受控执行下采集的逐行覆盖证据与变异检验约束（补丁行必须被该测试实际执行到，且对该行的变异敏感）。V08 不构成对 V02 的兜底，它只复跑同一命令并核对覆盖与变异；同进程证据仍可被测试代码伪造，见 [validators/README.md 的「已知边界」](../validators/README.md#已知边界天花板)。
