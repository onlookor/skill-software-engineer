# 交付物 schema：失败测试

> 归属阶段：S1。一件交付物＝测试文件本体＋同名元数据文件两件，缺一即未交付。

## 构成

| 件 | 路径 |
|---|---|
| 测试文件 | `tests/repro_<slug>.<ext>`（`<ext>` 随项目测试框架） |
| 元数据 | `tests/repro_<slug>.meta.yaml`（与测试文件同目录、同 slug） |

元数据是**同一交付物的组成部分**，不是第五种出口交付物。

## 元数据必填字段（五项）

| 字段 | 类型 | 约束 | 可自动判定 | 只能由人判断 |
|---|---|---|---|---|
| `file` | string | 指向测试文件，**仓内 `tests/` 相对路径**（绝对路径、仓外路径、软链出仓均不合格），文件存在、非空，且定义无参 `observe()` | 路径形式、存在、非空、`observe()` 契约与入口调用（V03） | 观测值是否覆盖用户所述失败 |
| `test_id` | string | 非空 | 存在且非空；被 `single_run_command` 引用 | 用例 id 是否确为该用例 |
| `single_run_command` | string | 非空、单行，且只能是 `python3 -I <仓内相对路径>`；脚本必须与 `file` 是同一文件；只跑该用例 | V03 实际运行必失败；白名单形式与脚本绑定（V03 判） | 命令语义上是否真的只跑了该用例（仍可绕过） |
| `base_commit` | string | 7–40 位十六进制；等于 S1 时的 HEAD | V03 比对 HEAD | 该 commit 是否为用户所指版本 |
| `expected_failure` | string | 非空；期望的失败信息 | 存在且非空 | 失败信息是否对应机制层可观察量 |

## 测试文件要求

- 不调用任何断言 API：不 `import unittest`、不 `assert`、不用 `self.assertEqual`。
- 只允许模块级导入、`sys.path` 设置与无参函数 `observe()`；`observe()` 返回字面量 `dict`（`observation_id → 观测值`），每个观测值必须直接是被测入口的调用。
- 观测机制层可观察量：返回值／状态字段，**不写表层输出字符串**。
- 单独运行即失败（由引导比对观测值与 `repro.md` 的期望值），不依赖全量测试的执行顺序。
- 只新增该文件；S1 不改动既有测试与源码。

## 模板（占位符不是值）

```yaml
file: "tests/repro_<slug>.<ext>"
test_id: "<string>"
single_run_command: "python3 -I tests/repro_<slug>.<ext>"
base_commit: "<7–40 位十六进制>"
expected_failure: "<string>"
```

## 判不了的部分

- 用例是否覆盖真实使用场景：没有可自动判定的标准，只能由人判断。
- `single_run_command` 是否真的只跑了该用例：V03 只认「`python3 -I <仓内相对路径>`＋脚本与 `file` 同一文件＋实际失败」，无法证明命令内部没有绕过；`bash`／`env`／赋值前缀／`-m`／`-c`／参数与复合命令直接拒绝。
- 观测值是否语义上真的来自被测入口：V03 只做静态判定（返回值必须直接是入口调用）；经局部变量中转、包装函数、同进程篡改仍判不了。
- `base_commit` 对应版本是否就是用户报障的版本：只能由人判断。
