# validators：V01–V08 可执行、V09 人工

> 本目录校验的是**技能交付物**（`repro.md`、失败测试、`fix.patch`、`verify.log`），不是仓库内部产物；与 `registry/` 下的检查器不共享路径与命名，禁止混用。

## 用法

```bash
python3 validate.py --config <使用前配置快照.yaml>            # 跑 V01–V08 全部
python3 validate.py --config <使用前配置快照.yaml> --only V01 V02
```

- 配置快照七项（`repo_path`／`test_command`／`build_command`／`repro_runs`／`repro_timeout_seconds`／`allowed_scope`／`cache_cleanup_policy`）只从 `--config` 指向的文件读取，与 `SKILL.md` 的 `mount_declarations` 一一对应。**本目录不含任何项的值、默认值、示例值、推荐值。**
- 快照可另带元数据 `agreed_at`（ISO-8601）与 `agreed_by`（恰好两项非空身份）。它们不属于七项、不参与缺项判定；给出时校验格式，其它未声明键判非法。
- 缺任一项 → 退出码 3，不静默通过。前六项由自动检查直接使用或核对；`build_command` 只校验类型与单行，**V01–V08 不执行构建**（交付物不依赖构建，执行构建只引入副作用与超时），因此不设 `build_not_configured` 状态。`cache_cleanup_policy` 只判存在、类型与非空，策略是否足以排除缓存与构建产物复用只能由人判断。
- 交付物位置：`repro.md`、`localization.md`、`fix.patch`、`verify.log`、`fix-report.md` 在仓根；失败测试与元数据在 `tests/`。

## 退出码

`0`＝pass；`1`＝fail；`3`＝`cannot_evaluate`。三者之外无其它退出码。多项合跑时：任一 fail → 1；否则任一 cannot → 3；否则 0。

## 逐条：判什么／判不了什么

| ID | 类型 | 判什么 | 判不了什么 |
|---|---|---|---|
| V01 | schema | `repro.md` 八字段齐全、类型正确、`fingerprint.run1 == run2` | 内容是否真实；`expected`／`actual` 是否忠于用户所述 |
| V02 | 可执行命令 | 复现命令退出码 ≠ 0；输出非空；连跑 `repro_runs` 次摘要一致；声明摘要与实跑一致；复现命令必须引用元数据记录的测试文件或 `test_id` | 该失败是否就是用户报的那个问题；摘要归一化是否覆盖全部噪声；带引用的恒真失败命令仍可能漏过（靠 S3 第②段与 V08 重跑兜底） |
| V03 | 可执行命令 | 测试文件存在、非空、含断言或测试定义；`single_run_command` 引用该测试文件或 `test_id`；单独运行即失败；HEAD 与 `base_commit` 一致 | 覆盖率；命令是否真的只跑了该用例；是否绕过真实路径 |
| V04 | 可执行命令 | `git apply --check` 通过 | 补丁语义是否正确；补丁是否最小 |
| V05 | 黑名单 | `touched_files ⊆ localization.md.files`，且 ⊆ `allowed_scope` | 声明范围本身是否完整（漏文件判不了） |
| V06 | 黑名单与最小性 | 测试断言行零改动；`evidence_kind` 取值合法；`estimated_touched_files`／`estimated_diff_lines` 与实际补丁一致；`hypothesis` 下禁止「根因已确认／彻底修复／问题已解决」且 `status` 不得为 `fixed` | 是否以其他方式把断言变恒真（等价改写判不了）；预估数字是否诚实地反映设计意图（只判与实际是否一致） |
| V07 | 可执行命令 | 使用前 `test_command` 全绿 | 测试集本身是否足够；绿是否由本次补丁引起 |
| V08 | 可执行命令 | 三段顺序与退出码（非0／0／非0）；`patch_sha256` 与 `fix.patch` 一致；`test_command_used` 与使用前快照逐字一致；`commit` 与当前 HEAD 一致；已跟踪文件无未提交改动；**实际重跑三段**并与日志退出码逐段比对；`fix-report.md.status=fixed` 必须有 `v09_signoff` | 缓存与构建产物是否真的被清理（重跑沿用同一环境，不能替代清理策略）；绿是否由本次补丁引起（靠第③段逼近，不绝对） |
| V09 | 人工清单 | 根因陈述与 `evidence_kind` 是否成立 | 无法自动判定；见 [V09-checklist.md](V09-checklist.md) |

## 运行时机（状态相关，不是随便复跑）

| 项 | 应在何时跑 | 原因 |
|---|---|---|
| V01／V02／V03 | S1 写完交付物后、补丁前 | V03 要求 HEAD 等于 `base_commit` 且用例仍失败 |
| V04／V05／V06 | S2 写完 `fix.patch` 后、应用前 | `git apply --check` 要求补丁尚未应用 |
| V07 | S2 通过条件／S3 第②段 | 要求补丁已应用且全量测试绿 |
| V08 | S3 写完 `verify.log` 后 | 会实际重跑三段：要求补丁尚未应用、已跟踪文件干净；重跑后自动撤销补丁，不改动交付物 |

## 第③段（撤补丁复败）的证据有效性前提

第③段的结论只有在**排除缓存与构建产物复用**之后才可采信。若撤补丁后复现用例仍是**绿**的：

- 不得直接当成「补丁无效」，也不得把「三段日志已齐」当成任务完成；
- 必须先用使用前「缓存与构建产物清理策略」排除缓存与构建产物复用；
- 排除后仍绿，才是真的没有复败；仍绿时第③段退出码为 0，V08 会判 fail（期望非 0），不得改写退出码凑通过。

**实例（2026-11-16，随包示例仓实测）**：Python 撤补丁后复现用例仍绿，原因是 `__pycache__/calc.cpython-*.pyc` 复用了补丁态字节码。
- 触发条件：撤补丁后的源文件与补丁态在**同一秒内**被写入（pyc 头部记录秒级 mtime），且**字节长度相同**（如 `a - b` 与 `a + b`）；两项同时成立时 pyc 的 mtime＋size 校验通过，缓存被复用。
- 后果：第③段「撤补丁复败」假绿——三轮验证看似走完，实际没有复败；若把日志齐备当证据，就会把未验证的修复记成已修复。
- 处置：属使用前「缓存与构建产物清理策略」应覆盖的范围。自动检查不清理、也不判清理是否生效；只能由人核对 `test_command_used` 原文与清理策略后再采信第③段。

## 判不了就不判

- 任何一项缺输入或执行超时 → 退出码 3，不当作 pass，也不当作 fail。
- 不得用「都跑过了」代替「每条都判过」；`cannot_evaluate` 必须原样上报。

## 附：卡点日志校验（不属于 V01–V09）

`check_blocker_log.py` 校验部署侧「卡点日志」的形状与脱敏黑名单，规则源见 [../schemas/blocker-log.md](../schemas/blocker-log.md)。

- 用法：`python3 check_blocker_log.py <blocker-log.yaml>`；
- 文件不存在或为空 → 输出「未记录」，退出码 0，**不判 fail**；
- 存在不合格记录 → 退出码 1；
- 机器校验通过 ≠ 可提交：不带点的仓库名／主机名／账号与「描述是否真的抽象」只能由人判断；默认不上传，由人看过再决定是否提交。
- 它不改变技能能执行哪些任务，不属于任务交付物，也不参与 V01–V09 的判定。
