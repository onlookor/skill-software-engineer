# validators：V01–V08 可执行、V09 人工

> 本目录校验的是**技能交付物**（`repro.md`、失败测试、`fix.patch`、`verify.log`），不是编译产物；与 `registry/` 下的检查器不共享路径与命名，禁止混用。

## 用法

```bash
python3 validate.py --config <挂载期配置快照.yaml>            # 跑 V01–V08 全部
python3 validate.py --config <挂载期配置快照.yaml> --only V01 V02
```

- 配置快照六项（`repo_path`／`test_command`／`build_command`／`repro_runs`／`repro_timeout_seconds`／`allowed_scope`）只从 `--config` 指向的文件读取。**本目录不含任何项的值、默认值、示例值、推荐值。**
- 缺项、类型不符、越界 → `cannot_evaluate`（退出码 3）；`build_command` 未配置不阻塞本组校验，但报告须标 `build_not_configured`，该项不判 pass。
- 交付物位置：`repro.md`、`localization.md`、`fix.patch`、`verify.log`、`fix-report.md` 在仓根；失败测试与元数据在 `tests/`。

## 退出码

`0`＝pass；`1`＝fail；`3`＝`cannot_evaluate`。三者之外无其它退出码。多项合跑时：任一 fail → 1；否则任一 cannot → 3；否则 0。

## 逐条：判什么／判不了什么

| ID | 类型 | 判什么 | 判不了什么 |
|---|---|---|---|
| V01 | schema | `repro.md` 八字段齐全、类型正确、`fingerprint.run1 == run2` | 内容是否真实；`expected`／`actual` 是否忠于用户所述 |
| V02 | 可执行命令 | 复现命令退出码 ≠ 0；连跑 `repro_runs` 次指纹一致；声明指纹与实跑一致 | 该失败是否就是用户报的那个问题；指纹归一化是否覆盖全部噪声 |
| V03 | 可执行命令 | `single_run_command` 单独运行即失败；HEAD 与 `base_commit` 一致 | 覆盖率；`single_run_command` 是否真的只跑了该用例；是否绕过真实路径 |
| V04 | 可执行命令 | `git apply --check` 通过 | 补丁语义是否正确；补丁是否最小 |
| V05 | 黑名单 | `touched_files ⊆ localization.md.files`，且 ⊆ `allowed_scope` | 声明范围本身是否完整（漏文件判不了） |
| V06 | 黑名单 | 测试断言行零改动；`evidence_kind` 取值合法；`hypothesis` 下禁止「根因已确认／彻底修复／问题已解决」且 `status` 不得为 `fixed` | 是否以其他方式把断言变恒真（等价改写判不了） |
| V07 | 可执行命令 | 挂载期 `test_command` 全绿 | 测试集本身是否足够；绿是否由本次补丁引起 |
| V08 | 可执行命令 | 三段顺序与退出码（非0／0／非0）；`patch_sha256` 与 `fix.patch` 一致；第②段同时含复现命令与全量测试命令 | 绿是否由本次补丁引起（靠第③段逼近，不绝对） |
| V09 | 人工清单 | 根因陈述与 `evidence_kind` 是否成立 | 无法机器判；见 [V09-checklist.md](V09-checklist.md) |

## 运行时机（状态相关，不是随便复跑）

| 项 | 应在何时跑 | 原因 |
|---|---|---|
| V01／V02／V03 | S1 写完交付物后、补丁前 | V03 要求 HEAD 等于 `base_commit` 且用例仍失败 |
| V04／V05／V06 | S2 写完 `fix.patch` 后、应用前 | `git apply --check` 要求补丁尚未应用 |
| V07 | S2 门／S3 第②段 | 要求补丁已应用且全量测试绿 |
| V08 | S3 写完 `verify.log` 后 | 只读日志与补丁，不重跑命令 |

## 判不了就不判

- 任何一项缺输入或执行超时 → 退出码 3，不当作 pass，也不当作 fail。
- 不得用「都跑过了」代替「每条都判过」；`cannot_evaluate` 必须原样上报。
