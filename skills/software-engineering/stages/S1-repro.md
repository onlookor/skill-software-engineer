---
stage: "S1-repro"
title: "复现"
requirements:
  config: ["repo_path", "test_command", "repro_runs", "repro_timeout_seconds", "allowed_scope"]
inputs:
  repo_path: {type: path, required: true}
  failure_signal: {type: text, required: true}     # 报错文本／失败用例 id／issue 摘要，三选一
  env_notes: {type: text, required: false}
steps:
  - "读构建文件与测试入口"
  - "按约定的 test_command 跑一次既有测试（命令形式为 `python3 -I <仓内相对路径>`）"
  - "写失败用例 tests/repro_<slug>.<ext>"
  - "连跑 repro_runs 次，取失败摘要（异常类型＋关键栈帧＋断言差异）"
outputs:
  - "repro.md"
  - "tests/repro_<slug>.<ext>"                     # 能稳定失败的用例
gate:
  - "复现命令退出码 ≠ 0"
  - "同一命令连跑 2 次，失败摘要一致（摘要＝异常类型＋关键栈帧＋断言差异）"
  - "失败用例单独运行即失败（不依赖全量测试的执行顺序）"
on_fail:
  - "不可复现 → 停，写 escalate（上报）记录；禁止进入 S2，禁止先写补丁"
  - "环境缺失 → 只输出 missing_env 清单，不改任何代码"
validators: ["V01", "V02", "V03"]
---

# S1 复现

## 输入

- `repo_path`（必填）：仓根路径；使用前已约定，未约定即 `cannot_evaluate`（无法判定）。
- `failure_signal`（必填）：报错文本／失败用例 id／issue 摘要，三选一。
- `env_notes`（可选）：环境备注。
- 依赖的使用前约定项：`test_command`、`repro_runs`、`repro_timeout_seconds`、`allowed_scope`。
  任一未约定 → `cannot_evaluate`，本阶段不启动。

## 步骤

1. 读构建文件与测试入口，确认测试框架与用例布局。
2. 按约定的 `test_command` 跑一次既有测试（命令形式为 `python3 -I <仓内相对路径>`），记录退出码。
3. 写失败用例 `tests/repro_<slug>.<ext>`：断言机制层可观察量（异常类型／返回码／状态字段），不写表层输出字符串。用例只能是「调用被测接口并用字面量期望值断言」的单元测试：不得 `open`、不得读取源码文本，不得使用 `os`／`subprocess`／`importlib`／`io`／`codecs`／`pkgutil`／`runpy` 等模块，不得 `exec`／`eval`／`__import__`／`getattr`／`hasattr`／`vars`／`globals`，不得读写环境变量，不得给已导入对象的属性赋值（猴补丁），不得读取被测入口之外的属性，不得使用 `unittest.mock`，不得导入 `tests.*` 或与 `under_test` 无关的仓内模块；`sys` 只允许 `sys.path.insert`／`append` 且路径只能是 `"."`。期望值必须是字面量（数字、字符串、`True/False/None`、字面量容器及其算术），不得用 `int("-1")` 之类调用构造。`repro.md` 用 `under_test: <module.entry>` 声明被测入口（可多个，只允许函数或类；常量与模块名会被 V01 拒绝），V03／V08 按它判。
4. 连跑 `repro_runs` 次，逐次记录退出码与失败摘要；`repro_timeout_seconds` 为单次超时上限。
5. 填 `repro.md`（九个字段，格式见 `schemas/repro.md`）。

## 输出

- `repro.md`
- `tests/repro_<slug>.<ext>`

两者缺一即本阶段未完成。**本阶段不产出补丁，不修改除新增失败用例之外的任何文件。**

## 通过条件（三条全部由自动检查判定，无人工项）

1. 复现命令退出码 ≠ 0。
2. 同一命令连跑 2 次，失败摘要一致（摘要＝异常类型＋关键栈帧＋断言差异）。
3. 失败用例单独运行即失败（不依赖全量测试的执行顺序）。

判定者：V01（格式）、V02（退出码与失败摘要）、V03（单独运行）。

## 失败处理

- **不可复现 → 停，写 escalate（上报）记录；禁止进入 S2，禁止先写补丁。**
  上报记录须写：已尝试的命令、各自退出码、为何不构成复现；随后结束本次任务。
- **环境缺失 → 只输出 missing_env 清单，不改任何代码。** 清单写明缺什么、缺在哪一步。
- 两个出口之外没有第三个出口。不得「先写补丁再回头补复现」。
