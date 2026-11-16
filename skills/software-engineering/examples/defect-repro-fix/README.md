# 示例：缺陷复现—最小修复

一个真 bug、一个稳定失败的用例、一个最小补丁、三段验证日志，全部在本目录内，一条命令重跑。

## 一条命令

```bash
python3 skills/software-engineering/examples/defect-repro-fix/run.py
```

脚本在 `work/` 下重建临时 git 仓（`work/` 已被本目录 `.gitignore` 忽略），按 S1→S2→S3 生成交付物并调用自动检查；V01–V08 全 pass 时退出码 0，任一 fail 时退出码 1。每次运行都会先删掉 `work/` 再重建，产物保留在 `work/` 供检查。

依赖：`python3` 与 `PyYAML`（`validators/validate.py` 已要求），无其它依赖；git 身份是 `example@example.invalid`／`example`，不含任何真实凭证。

## 目录

| 路径 | 内容 |
|---|---|
| `base/calc.py` | 真 bug：`add()` 写成了减法 |
| `base/tests/test_calc.py` | 既有测试（base 上全绿） |
| `artifacts/repro_add.py` | 失败测试：单独运行即失败 |
| `artifacts/fix.patch` | 最小补丁：只改 `calc.py` 一行 |
| `artifacts/localization.md` | 定位记录：`evidence_kind: direct` |
| `config.yaml` | **使用前快照样例**（七项声明各有值） |
| `run.py` | 编排脚本 |
| `work/` | 运行后生成：`repro.md`、`tests/repro_add.meta.yaml`、`verify.log`、`fix-report.md` 等 |

`repro.md` 的 commit、失败摘要、时间戳，以及 `verify.log` 的 patch sha 与三段结果都依赖实际运行，因此由 `run.py` 现场生成，不静态保存。

## 它如何被 `validate.py` 消费

**是 V01–V08 的真实输入，不只作演示。** 消费方式：本目录的 `config.yaml` 就是 `validate.py --config` 的输入（使用前快照），`work/` 就是其中的 `repo_path`；`run.py` 只是按 S1→S2→S3 的时序把交付物写进 `work/`，再在三个正确的状态点调用同一个自动检查：

| 时点 | 调用 | 原因 |
|---|---|---|
| 补丁前 | V01 V02 V03 | V03 要求 HEAD 等于 `base_commit` 且用例仍失败 |
| 补丁未应用 | V04 V05 V06 | `git apply --check` 要求补丁尚未应用 |
| 补丁应用后 | V07 | 既有测试全绿 |
| 写完 `verify.log` | V08 | 实际重跑三段，并与日志逐段比对退出码 |

它**不是**仓的常驻检查：只证明示例自身的闭环能跑通，不替代真实仓的验收；`V09` 是人工清单，本脚本不跑。`config.yaml` 是使用前快照（运行时产物），与 `SKILL.md` 的 `mount_declarations` 声明是两回事——声明本身不含任何值。

## 缓存与构建产物

示例的缓存清理策略写在 `config.yaml` 的 `cache_cleanup_policy` 中并被执行：S3 第②、③段前清空 `__pycache__`，测试命令带 `PYTHONDONTWRITEBYTECODE=1`。第③段的失效实例与触发条件见 [validators/README.md](../../validators/README.md) 的「第③段（撤补丁复败）的证据有效性前提」。
