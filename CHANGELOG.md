# CHANGELOG：变更历史

> 本文件是**变更历史的唯一登记处**（schedule 纪律见 [AGENTS.MD](AGENTS.MD) 第 3 条）。
> 只追加，**不得改写已登记批次**；发现登记错误时追加一条更正条目并引用原批次。批次号一经发布永不复用。
> 本文件不写版本号、不携带版本头；技能包版本以 `SKILL.md` 的 `version` 为唯一来源。
> 每批格式：`{批次号, 日期, 涉及文件, 变更摘要, 关联 ADR}`。

## 批次 0001 — 2026-11-16

- **批次号**：0001
- **日期**：2026-11-16
- **涉及文件**：
  - 新增：`ROADMAP.md`、`STATE.md`、`CHANGELOG.md`
  - 调度：`todo.md`（状态块新增「阶段」字段；新增排期字段表）、`registry/scripts/project.py`（从事实生成阶段字段）
  - 文档：`README.md`、`AGENTS.MD`、`编译规范.md`、`翻新方案-对照project-management-20261115.md`、`skills/software-engineering/README.md`、`skills/software-engineering/PACKAGING.md`、`skills/software-engineering/stages/S3-verify.md`、`skills/software-engineering/validators/README.md`、`skills/software-engineering/validators/V09-checklist.md`、`skills/software-engineering/schemas/*.md`
  - 检查器：`skills/software-engineering/validators/validate.py`、`skills/software-engineering/validators/check_blocker_log.py`
  - 打包：`skills/software-engineering/scripts/build_package.py`、`skills/software-engineering/examples/defect-repro-fix/*`、`dist/`
  - 负向用例：`skills/software-engineering/tests/negative/run_negative.py`
- **变更摘要**：
  1. **调度层落地**：按 schedule 纪律建立 `ROADMAP.md`（M0–M7 与出口条件）、`STATE.md`（文件状态）、`CHANGELOG.md`（本文件）；`todo.md` 保持单点台账职责，并新增「里程碑」排期字段表。阶段 A–D 的释义迁入 `ROADMAP.md`，运行状态由 `todo.md` 状态块的「阶段」字段承载、由 `project.py` 从事实生成。
  2. **阶段语义（人类裁定变更）**：根 `README.md` 中「阶段 B：种子引导（当前所处阶段）」判为**过时**，改写为「已越过 LRM、待补阶段记录」。这是人类批准的**语义变更**，**不是笔误修正，也不是文字澄清**。M4（技能层）与 M5（分发件）作为**新增里程碑**，不并入 C／D 的出口；两者与 M3 并行，不因 M3 未闭合而阻塞；M5 的关闭条件不绑定复核制度批准或第三轮复核（复核批准归 M6）。
  3. **核心闭环加固**：V02／V03 要求复现命令与测试文件／`test_id` 可执行绑定，拒绝 `;`、`&&`、`||`、管道、重定向、注释、子命令等可夹带第二条命令的写法，并识别固定写法的恒真断言；V08 第②段分别重跑复现命令（期望 0）与测试命令（期望 0），不再只校验整条命令；V06 将测试路径下已有文件的任何改动（含测试数据与夹具）判 fail。
  4. **打包与版本**：任意层级的 `tests/` 目录不再随包分发（示例仓既有测试夹具改名为 `base/existing-tests/`）；打包脚本对版本字面量做反向断言（只允许出现在 `SKILL.md` 与 `PACKAGE-MANIFEST.txt`）；`dist/` 旧版本产物清理后重新打包。
  5. **文档同步**：技能 `README.md` 与 `PACKAGING.md` 删除版本字面量；`PACKAGING.md` 八处路径改 `${VERSION}` 占位；`编译规范.md` 文件头删除「当前状态」，改为指向 `todo.md` 3.7 的登记指针；`AGENTS.MD` 补充第 11–12 条的适用范围，并登记 `skills/`、`dist/`、`review/`；`翻新方案` §76 的现状数字按实测修正。
- **关联 ADR**：无
- **备注**：`独立复核规程.md` 仍为草案（待人类批准）；本批次不据此声称任何产物「已复核」或「已验证」。

## 批次 0002 — 2026-11-16

- **批次号**：0002
- **日期**：2026-11-16
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（V02／V03／V06／V07／V08、受控执行引导、覆盖采集、补丁区域解析）
  - 文档：`skills/software-engineering/SKILL.md`、`validators/README.md`、`schemas/repro.md`、`schemas/failing-test.md`、`schemas/fix-patch.md`、`stages/S1-repro.md`、`stages/S2-localize-fix.md`、`stages/S3-verify.md`、`examples/defect-repro-fix/*`
  - 打包：`skills/software-engineering/scripts/build_package.py`
  - 负向用例：`skills/software-engineering/tests/negative/run_negative.py`
  - 调度：`registry/scripts/project.py`、`ROADMAP.md`、`README.md`、`STATE.md`
- **变更摘要**：
  1. **环境隔离（人类批准「执行证据」路径）**：复现命令与测试命令只接受 `python3 -I <仓内相对路径>` 恰好三词；`bash`／`env`／赋值前缀／`-m`／`-c`／参数与复合命令直接拒绝，不再剥前缀兼容。执行时清空全部 `PYTHON*` 环境变量，以 `-I -S -B` 启动引导，显式屏蔽 `sitecustomize`／`usercustomize`，工作目录钉在仓根。V03 的测试文件路径只接受仓内 `tests/` 相对路径，绝对路径／仓外／软链出仓直接判 fail，与 schema 对齐。
  2. **执行证据（覆盖率）**：base 与 patched 两态都在受控执行下用标准库 `trace` 采集覆盖行；补丁在生产代码上删除的行必须在 base 态被复现测试执行到，新增的行必须在 patched 态被执行到，任一交集为空即 fail。覆盖率工具不可执行时返回 `cannot_evaluate`。标准库实现，不新增挂载期声明、不新增交付物，按扩张锁定口径不构成扩张。
  3. **文档承诺清理**：删除 `validators/README.md` 与 `schemas/repro.md` 中「V08 兜底」的不实表述（V08 只复跑同一命令并核对覆盖交集）；V06 的覆盖范围改为事实口径（`tests/` 路径的改写、改名、移出；`tests/` 之外夹具不在其内），改名按 diff 的 a 侧旧路径判定；`schemas/failing-test.md` 与 V03 实现对齐。
  4. **打包断言收紧**：内部资产与 `tests/` 判定改为大小写不敏感并忽略前导点；软链按解析后的真实路径判定，指向仓外或内部资产即拒包；版本字面量匹配前做字符串常量折叠，拒绝 `"0.6." + "0"` 这类邻接拼接。
  5. **调度层假门**：M2 改用 `artifact_seq`／卡片数／重编译次数作为独立出口，与 M1 的标签判据不同源；M6 改为要求 `review/approval.md`（`decision/approved_by/approved_at`＋与当前复核规程内容哈希一致），删除「文档里出现某个词」判据；M7 要求 annotated tag 且指向当前 HEAD，轻量 tag 不算；根 `README.md` 的阶段释义收敛为指向 `ROADMAP.md` 的单份语义。
- **关联 ADR**：无
- **备注**：本批次只提交，不推送、不打标签；未做自评，不写「已验证」。五个复核变体（C1／C2／C4／C6／C7）已自测，结果见第二份阶段报告，不以本条目替代报告。

## 批次 0003 — 2026-11-17


- **批次号**：0003
- **日期**：2026-11-17
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（变异检验、线程／子进程覆盖、V03 注释与字符串排除、V09 出口、受控执行 fd）
  - 打包：`skills/software-engineering/scripts/build_package.py`（同形字／空白路径、硬链接、版本号多种内嵌形式）
  - 用例：`skills/software-engineering/tests/negative/run_negative.py`、`skills/software-engineering/tests/positive/run_positive.py`（新增）
  - 调度：`registry/scripts/project.py`（M2 绑定本轮编译、M6 不再读仓内批准）、`ROADMAP.md`、`STATE.md`、`todo.md`
  - 文档：`skills/software-engineering/SKILL.md`、`validators/README.md`、`stages/S2-localize-fix.md`、`stages/S3-verify.md`、`schemas/repro.md`
- **变更摘要**：
  1. **变异检验**：V08 对补丁触及的每一行生产代码造变异（比较符翻转、运算符替换、常量 ±1、布尔取反），删除行做整块回退，在 patched 态重跑复现测试，必须变红；全部存活或造不出可编译变异即 fail。纯新增补丁的 base 侧仍为空，但新增行同样要过变异检验。
  2. **修误杀**：覆盖率引导增加 `threading.settrace` 并合并子进程覆盖率（`sitecustomize` 注入，父引导汇总）；新增正向套件证明子线程断言、子进程断言与纯新增补丁都不会被 V08 误杀。
  3. **承认天花板**：`validators/README.md` 新增「已知边界」；明确 `V01–V08` 全 pass 不等于修复成立。V09 不再有自动出口（`status: fixed` 直接 fail），M6 固定显示「未提供外部批准」。
  4. **第四轮余账**：覆盖率输出改经继承 fd，不再把输出路径放进 argv；V03 按 tokenize 去掉注释与字符串后匹配断言；M2 绑定 `label`／最新重编译记录／母本哈希与提交日期；打包拒绝同形字与含空白路径、硬链接，并对 f-string／`format`／转义／UTF-16 内嵌版本号做反向断言；`first_observed` 口径统一为接受 `str`／`date`／`datetime`；解释器收紧为字面量 `python3`；`validate.py` 在 `python3 -I` 下可自行补回站点目录导入 PyYAML；修正 S2／README 关于夹具覆盖范围与 ROADMAP M6 的不实表述。
- **关联 ADR**：无
- **备注**：本批次只提交，不推送、不打标签；未做自评，不写「已验证」。

## 批次 0004 — 2026-11-17

- **批次号**：0004
- **日期**：2026-11-17
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（变异判据、补丁结构、测试白名单、B3b 多改点回退）
  - 打包：`skills/software-engineering/scripts/build_package.py`（特殊位拒收与归一、断链／目录软链／特殊文件显式拒收）
  - 用例：`skills/software-engineering/tests/negative/run_negative.py`、`skills/software-engineering/tests/positive/run_positive.py`
  - 调度：`registry/scripts/project.py`（删除 M2 自动出口）、`ROADMAP.md`、`todo.md`
  - 文档：`skills/software-engineering/SKILL.md`、`validators/README.md`、`validators/V09-checklist.md`、`stages/S1-repro.md`、`stages/S2-localize-fix.md`、`stages/S3-verify.md`、`PACKAGING.md`
- **变更摘要**：
  1. **变异判据**：只认断言失败（`AssertionError`／unittest `failures>0`／pytest `failed>0`）；崩溃、超时、`SystemExit`／`os._exit` 等提前退出不再算杀死变异。受控执行引导把未捕获异常类型写进覆盖率 JSON。整份补丁造不出可编译变异即 fail，不把 docstring／注释／纯字符串等改不动的行当通过证据。
  2. **结构约束**：V06 用 AST 校验 `.py` 生产补丁的每个增行／删行都落在函数／方法体内（a 侧按 base、b 侧按补丁后源码），模块级赋值、模块 docstring、导入期调用、类属性猴补丁、装饰器、顶层 `def` 行一律拦。V03／V08 增加复现测试白名单：禁止 `open`、读源码文本、`os`／`subprocess`／`exec`／`eval`／`__import__`、读写环境变量、改写外部文件；正常 `import`／`from ... import` 放行。
  3. **修 B3b 误杀**：`patch_mutation_targets()` 按上下文行把同一 hunk 切成多个连续改动块，各自记录插入位置并独立回退；同一 hunk 内相隔上下文的两处修改不再报「无法定位删除块」。
  4. **M2 假出口**：删除 `_artifact_shape()`。`artifact.yaml` 的序号／标签／日期／母本哈希可被写成互相一致的假值，历史产物原样放回也能通过；本仓没有能区分「本轮编译」与「历史产物」的可执行动作。`project.py` 固定显示「C 未判定（M2 无自动出口）」，`ROADMAP.md` 的 M2 改为不设自动出口。
  5. **打包**：源文件带 setuid／setgid／sticky 即拒收并写明「未入包」；staging 统一 `0644`，tar 成员强制 `0644`／`REGTYPE`，归档后反向核对权限。断链、目录软链、FIFO／设备文件显式拒收，不再被 `is_file()` 静默跳过；打包输出登记「未入包项：0」。
  6. **文档边界**：天花板段落改为输出通道走环境变量 `SE_COV_FD`，并承认生产补丁同样能伪造；新增「预言取自被测代码本身时任何机械检查都判不出来」的边界，落入 V09 第 8 项，明确不得写成「已解决」。
- **关联 ADR**：无
- **备注**：版本 0.7.0 → 0.8.0；负向 34/34、正向 5/5；本批次只提交，不推送、不打标签；未做自评，不写「已验证」。

## 批次 0005 — 2026-11-17

- **批次号**：0005
- **日期**：2026-11-17
- **更正（引用批次 0004）**：批次 0004 第 5 条称「FIFO／设备文件显式拒收」，实际当时 `iter_files()` 仍以 `elif not p.is_file(): continue` 静默跳过 FIFO；该缺口在 0005 第 5 条修复，以本条为准。
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（导入期可达性、声明式放行、白名单收紧、`under_test`）
  - 打包：`skills/software-engineering/scripts/build_package.py`（FIFO／设备显式拒收）
  - 用例：`skills/software-engineering/tests/negative/run_negative.py`、`skills/software-engineering/tests/positive/run_positive.py`
  - 示例与 schema：`skills/software-engineering/examples/defect-repro-fix/run.py`、`skills/software-engineering/schemas/repro.md`
  - 文档：`skills/software-engineering/SKILL.md`、`validators/README.md`、`validators/V09-checklist.md`、`stages/S1-repro.md`、`stages/S2-localize-fix.md`、`stages/S3-verify.md`
- **变更摘要**：
  1. **不再用「行在函数体」当导入期代理**：V06 新增 AST 导入期可达性分析（元类钩子、`__init_subclass__`、`__set_name__`、模块级 `__getattr__`、装饰器、模块级调用链），落入其中的改动判 `cannot_evaluate`；README 第 67 行「导入期伪造已被拦住」的承诺撤回，改为「保守近似 + 已知边界」，并新增「导入期不可达不是可判定性质」条目。
  2. **V06 不再罚正确修复**：模块常量、纯 `import`、类属性默认值、dataclass field 默认值、模块级 `try/except` 内赋值、docstring、声明式装饰器、`def`／`class` 头都放行；新建生产模块可过。真正改到模块级可执行语句（Expr 调用、属性目标猴补丁、控制流头）判 `cannot_evaluate` 并写明「该缺陷需要改模块级声明，超出本技能适用面」。
  3. **白名单补洞**：`sys.modules`、`hasattr`、`getattr`、`vars`／`globals`、`sys.__dict__`、`type.__subclasses__`、`io`／`codecs`／`mmap`／`runpy`／`pkgutil`／`operator`／`pathlib` 等一律拦；`sys` 只允许 `sys.path.insert/append(…, ".")`；禁止给已导入对象属性赋值（猴补丁）。
  4. **预言独立性**：`repro.md` 新增必填字段 `under_test: module.entry`（可列表）。V01 校验形式，V03／V08 要求复现测试只能使用声明的入口，`calc.EXPECTED`、`add._se_fixed`、`from calc import EXPECTED`、`hasattr(calc, …)` 都被拦；A1 不再只靠 V06。
  5. **打包**：`iter_files()` 对 FIFO／设备／套接字显式报「特殊文件（FIFO／设备／套接字），未入包」并退出 1，不再静默跳过；目录仍正常跳过。
  6. **文档口径**：`sitecustomize`／`usercustomize` 屏蔽只对父进程成立，子进程覆盖率注入是另一条路径；V03 条目按实际白名单重写；V09 第 8 项补充「只能使用 `under_test` 入口」。
- **关联 ADR**：无
- **备注**：版本号待适用面收窄的裁定后再定，本批次不改 `SKILL.md` 的 `version`、不重打包；负向 34/34、正向 6/6、示例 `run.py` 退出 0；只提交，不推送、不打标签；未做自评，不写「已验证」。

## 批次 0006 — 2026-11-17

- **批次号**：0006
- **日期**：2026-11-17
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（运行时完整性、期望值字面量、`under_test` 可调用入口、`_pure_value`、移除导入期 AST 推断）
  - 打包：`skills/software-engineering/scripts/build_package.py`（「未入包项」真实计数）
  - 用例：`skills/software-engineering/tests/negative/run_negative.py`、`skills/software-engineering/tests/positive/run_positive.py`
  - 文档：`skills/software-engineering/SKILL.md`、`validators/README.md`、`validators/V09-checklist.md`、`stages/S1-repro.md`、`stages/S2-localize-fix.md`、`stages/S3-verify.md`、`schemas/repro.md`
  - 技术债：新增仓根 `TECH-DEBT.md`（不随包分发）
- **变更摘要**：
  1. **换到运行时完整性基底**：受控执行引导在导入任何仓内代码之前，对 `unittest.TestCase` 断言族、`builtins` 执行入口、`trace`／采集入口、`sys.modules` 基线留可信原件；执行后逐项比对，任一被替换／删除 → `cannot_evaluate`，理由「断言设施在导入期被改写」。不依赖触发方式（元类、`__init_subclass__`、描述符、`cached_property`、`Enum.__new__`、装饰器工厂、新建模块都一视同仁）。V02／V03／V07／V08 与变异检验共用这条判据。
  2. **V06 停止用语法位置代理导入期可达性**：删除 `IMPORT_TIME_HOOK_NAMES`／`_import_time_function_ids` 等 AST 近似；普通函数／方法体一律放行，只保留「模块级可执行语句 → cannot」与声明式放行。README「导入期」整段改为由运行时完整性覆盖。
  3. **期望值独立**：断言里的期望值必须是字面量（数字、字符串、`True/False/None`、字面量容器及负号／`~`／`1 << 4`／`2**3` 等算术）；禁止 `int("-1")` 这类调用构造期望值、`unittest.mock`（含 `from unittest import mock`）、`tests.*`、相对导入、与 `under_test` 无关的仓内模块。`under_test` 只允许模块级函数或类，常量与模块名在 V01 就拒（源码定位不到时判 cannot）。
  4. **修 `_pure_value` 误判**：运算符节点（`ast.operator`／`unaryop`／`cmpop`／`boolop`）不再被当成不纯表达式，`EXPECTED = -1`、`0 - 1`、`~0` 按声明式纯值放行。
  5. **打包计数**：`iter_files()` 返回实际被排除的普通文件数，输出「未入包项：N」，不再固定打印 0。
  6. **技术债单独立项**：新增 `TECH-DEBT.md`，逐条记录导入期可达性漏判的 10 类钩子、新建模块与 `allowed_scope` 矛盾、`_pure_value` 误判、`under_test` 允许常量、`mock`／本地夹具、同进程伪造、以及「用句法特征代理语义性质」的共同缺陷；写明将来改版方向需要调用图／动态追踪＋沙箱，不是继续加 AST 规则。
- **关联 ADR**：无
- **备注**：版本号仍待「适用面收窄算 minor 还是 major」的人类裁定，本批次不改 `SKILL.md` 的 `version`、不重打包；负向 36/36、正向 6/6、示例 `run.py` 退出 0；只提交，不推送、不打标签；未做自评，不写「已验证」。

## 批次 0007 — 2026-11-18

- **批次号**：0007
- **日期**：2026-11-18
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（观测值契约、`load_observations`、`observe()` 静态形状、`under_test` 收紧到点号函数／方法、采集入口快照、变异判据改口径）
  - 用例：`skills/software-engineering/tests/negative/run_negative.py`、`skills/software-engineering/tests/positive/run_positive.py`
  - 示例与 schema：`skills/software-engineering/examples/defect-repro-fix/run.py`、`skills/software-engineering/examples/defect-repro-fix/artifacts/repro_add.py`、`skills/software-engineering/schemas/repro.md`、`skills/software-engineering/schemas/failing-test.md`
  - 文档：`skills/software-engineering/SKILL.md`、`validators/README.md`、`validators/V09-checklist.md`、`stages/S1-repro.md`、`stages/S2-localize-fix.md`、`stages/S3-verify.md`
  - 技术债：仓根 `TECH-DEBT.md`（重写，仍不随包分发）
- **变更摘要**：
  1. **断言 API 整体移出判定链**：复现测试不再 `import unittest`、不再 `assert`、不再 `self.assertEqual`；只定义一个无参 `observe()`，返回 `observation_id → 观测值` 的 dict。期望值写在 `repro.md.observations`（只允许字面量），由受控执行引导（`python3 -I -S -B`）自己调用、自己比较、自己产出 pass／fail。引导不再导入 `unittest`，因此也不再有「插路径后导入 `unittest` 被仓根影子顶替」的依赖。
  2. **返回值静态约束**：每个观测值必须直接是 `under_test` 声明入口的调用（`f(...)`／`mod.f(...)`／`Cls(...).m(...)`／`mod.Cls(...).m(...)`／`Cls.m(...)`）；硬编码常量、先算别的再返回常量、返回值加壳（`add(...) + 0`）、`observe()` 缺参／带参／返回非 dict、id 与 `repro.md` 不一一对应都在 V03 拦住。
  3. **`under_test` 收紧**：只接受点号函数或方法；类、常量、模块名在 V01 直接拒（`calc.EXPECTED`、`calc.Calc` 均被拒），类入口脱钩不再成立。
  4. **采集入口完整性降级**：运行时快照只覆盖 `trace`／`threading`/`sys.settrace`／`runpy.run_path`／`builtins` 执行入口／`sys.modules` 基线，只发现「替换后不复原」；自恢复与 `os._exit` 提前退出如实写明发现不了，且不再承担断言语义。
  5. **变异判据改口径**：只认「观测值与期望值不一致」（引导报告 `ObservationMismatch`）；崩溃、超时、`SystemExit`／`os._exit` 不算杀死变异。
  6. **文档失真逐条修正**：撤回「任一断言设施被替换／删除即判 cannot」「元类、新建模块一视同仁」与「导入期伪造由运行时完整性覆盖」等表述；`V09-checklist.md` 第 8 项改为「观测值与期望值独立」，并写明运行时完整性不再是可采信证据；`SCHEMA` 的「测试只能使用这些可调用入口及其调用结果」改为新契约；`TECH-DEBT.md` 纠正第 1／2／6 条措辞，补记第八轮新证实的五类缺口（自恢复假断言、`__code__`／`_baseAssertEqual`、换 `TestCase` 绑定、新建模块导入期安装、类入口脱钩）及其在新契约下的状态；`validators/README.md` 的 `../../../TECH-DEBT.md` 断链改为「仓根 TECH-DEBT.md（不随包分发）」文字说明。
- **关联 ADR**：无
- **备注**：版本号仍待「适用面收窄算 minor 还是 major」的人类裁定，本批次不改 `SKILL.md` 的 `version`、不重打包；负向 37/37、正向 6/6、示例 `run.py` 退出 0；只提交，不推送、不打标签；未做自评，不写「已验证」。

## 批次 0008 — 2026-11-18

- **批次号**：0008
- **日期**：2026-11-18
- **版本**：0.8.0 → 0.9.0（按 BACKFLOW 属 minor：改了测试契约与 V01／V03／V08 判定）
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（分类改认 `stage=mismatch`；`observe()` 体只允许单条 `return`；`type` 入黑名单）
  - 用例：`skills/software-engineering/tests/negative/run_negative.py`（新增 E1j／E1c／E1f 与分类单元用例）
  - 文档：`skills/software-engineering/validators/README.md`、`skills/software-engineering/stages/S1-repro.md`、`skills/software-engineering/SKILL.md`（版本号）
  - 技术债：仓根 `TECH-DEBT.md`（新增第 9 条；8.1–8.3 措辞收紧）
  - 分发：`dist/software-engineering-0.9.0/`、`.tar.gz`、`.sha256`（重打包）
- **变更摘要**：
  1. **P0-1 分类信号移出异常名**：引导在完成自身比对后把 `stage="mismatch"` 写进结构化 failure；`classify_test_outcome` 只认该标记，不再看 `type(exc).__name__`。生产代码或测试侧自定义同名异常一律归入 crash，不能伪造「观测值不一致」。
  2. **P0-2 约束 `observe()` 函数体**：V03 要求函数体只有单条 `return`，禁 `Assign`／`AugAssign`／`If`／`Try`／`Raise`／`With`／`For`／`While`／局部函数定义／局部重绑定；`type` 加入黑名单。E1f 被 V03 拦住。
  3. **文档与债务**：README V02 行改为「退出码非 0（可能是观测不一致，也可能是崩溃；V02 不消费分类标记）」；V03／V08 行同步新口径；`TECH-DEBT.md` 新增「判定标签可被同名异常伪造」条目并记录 E1j／E1c／E1f 与修法状态；8.1–8.3 的「根除」改为「该载荷根除；测试仍可在 `observe()` 体内自行比较并伪造标签」；N2/N3 用例 docstring 与断言口径对齐；`S1-repro.md` 注明「测试里不出现期望值」由 V03 的函数体约束承接。
  4. **版本与 dist**：`SKILL.md` 升 0.9.0，重打包，重跑负向 40/40、正向 6/6、示例退出 0、`project.py --check` 硬失败 0。
- **关联 ADR**：无
- **备注**：「适用面收窄走 minor 还是 major」仍待人类裁定，本批次未自行决定；本批次只提交，不推送、不打标签，不自评。

## 批次 0009 — 2026-11-18

- **批次号**：0009
- **日期**：2026-11-18
- **更正（引用批次 0008）**：批次 0008 变更摘要第 3 条「测试仍可在 `observe()` 体内自行比较并伪造标签」已过时——0008 自身的「`observe()` 函数体只允许单条 `return`」已关闭该路径，现状以 `TECH-DEBT.md` 8.1–8.3 与 `validators/README.md` 为准。**程序记录**：批次 0008 实际按 BACKFLOW 以 minor 从 0.8.0 升到 0.9.0；「适用面收窄算 minor 还是 major」的裁定仍待补，不得把升版事实当作裁定已完成。
- **涉及文件**：
  - 检查器：`skills/software-engineering/validators/validate.py`（`observe()` 实参拦 `NamedExpr`）
  - 用例：`skills/software-engineering/tests/negative/run_negative.py`（白名单新增海象赋值变体）
  - 文档：`skills/software-engineering/validators/README.md`、`skills/software-engineering/stages/S1-repro.md`、`skills/software-engineering/schemas/repro.md`
  - 技术债：仓根 `TECH-DEBT.md`
  - 分发：`dist/software-engineering-0.9.0/`、`dist/software-engineering-0.9.0.tar.gz`、`dist/software-engineering-0.9.0.tar.gz.sha256`（重打包）
- **变更摘要**：
  1. **README 口径改准**：`__code__`／`_baseAssertEqual` 绕法的「根除」限定为测试侧断言设施，生产侧导入期改写 `add.__code__` 仍不会被判定链发现；删除「选用让 base 与 patched 产生同一观测的输入……使变异被杀死」的矛盾说法，改为 V08 只要求 base 在该 observation 上失败、不校验该失败与用户所述缺陷同源（交 V09）；V08 的提前退出例外加「未伪造 `SE_COV_FD` 输出通道」前提，并写明 `stage`／`exit`／覆盖率同走一 fd、无签名、可被生产代码伪造；新增「全绿证明什么」限定段落。
  2. **技术债对齐现状**：8.1–8.3 改为「测试侧体内自比较已由 0008 单条 `return` 关闭」；8.4 补「既有休眠 shim ＋ 一行 `import`、只对观测输入硬编码」同样漏（实测全绿）。
  3. **方法入口适用面**：`S1-repro.md` 与 `schemas/repro.md` 写明只能用单表达式构造实例，多步构造（先赋局部变量再调用）不可表达。
  4. **小漏网**：`observe()` 实参中的 `NamedExpr`（`add((x := 2), 3)`）与「禁局部重绑定」矛盾，V03 一并拦；不扩展其他表达式。
- **关联 ADR**：无
- **备注**：版本保持 0.9.0（口径修正不改判定，不升版）；负向 40/40（白名单变体 28 种）、正向 6/6、示例 `run.py` 退出 0、`project.py --check` 硬失败 0；本批次只提交，不推送、不打标签，不自评。

## 批次 0010 — 2026-11-18

- **批次号**：0010
- **日期**：2026-11-18
- **裁定事项**：**适用面收窄按 minor 处理**（人类裁定，2026-11-18）。收窄内容：复现必须能在单进程、无子进程、无目录／文件级夹具的条件下表达；需要子进程断言或目录级夹具的缺陷不再由本技能承载。此前批次 0009 的程序记录与批次 0008 备注中的「适用面收窄算 minor 还是 major／裁定待补」就此关闭，由本次裁定结清。
- **版本归属**：并入 0.9.0，不单独升版本号。
- **涉及文件**：
  - 文档：`CHANGELOG.md`（本批次）、`skills/software-engineering/SKILL.md`（When not 中英双语各补一条）、`skills/software-engineering/README.md`（适用面段落补一句）
  - 分发：`dist/software-engineering-0.9.0/`、`dist/software-engineering-0.9.0.tar.gz`、`dist/software-engineering-0.9.0.tar.gz.sha256`（重打包）
- **变更摘要**：
  1. **披露到使用面**：`SKILL.md` 的 When not 中英双语分别写明「缺陷只能通过子进程断言、或需要目录／文件级夹具才能复现 → 本技能不适用：停在 S1／前置判据并 `escalate`，不得改写成单进程观测来强行套用」。
  2. **README 同步**：适用面段落补同义一句，说明复现需能在单进程、无子进程、无目录／文件级夹具下表达。
  3. **口径确认**：`schemas/repro.md` 的「方法入口只能单表达式构造实例」是观测表达式的文法限制，与本次 when-not 不冲突，不改。
- **关联 ADR**：无
- **备注**：版本保持 0.9.0（并入本轮，不单独升号）；负向 40/40、正向 6/6、示例 `run.py` 退出 0、`project.py --check` 硬失败 0；本批次只提交，不推送、不打标签，不自评。

## 批次 0011 — 2026-11-18

- **批次号**：0011
- **日期**：2026-11-18
- **补正事项**：**阶段释义迁移时谓词化失位**。阶段语义迁入 `ROADMAP.md` 时，C 行只保留了「编译产物、忠实性检查、FVR 接线」，遗漏「层次二＝设计过程谓词化（10.2.3bis）」；原句留在根 `README.md` §5 第 6 条，形成两处语义。
- **涉及文件**：
  - `ROADMAP.md`：§一阶段表 C 行补回「层次一＝技能卡片；层次二＝设计过程谓词化，10.2.3bis」，并在判据栏与 M2 出口条件栏如实登记现状——定义（母本 4533–4541）／规程（编译规范 532–566，T1–T5）／接线（14 张卡 S6；CFG／CRD／DPS／SRC 四张无 S6）在，执行级为零、当前无自动判定。
  - `README.md`：§5 第 6 条收为指向 `ROADMAP.md` §一阶段 C 的指针，阶段语义单一来源归 ROADMAP，不再保留第二份。
- **未改动**：母本、编译规范、卡片均未改。
- **关联 ADR**：无
- **备注**：本轮为文档补正，不改判定；版本保持 0.9.0，dist 不重打包；只提交，不推送、不打标签，不自评。

## 批次 0012 — 2026-11-18

- **批次号**：0012
- **日期**：2026-11-18
- **事项**：谓词化按「先从定义做起」推进，新增执行级计划。
- **涉及文件**：
  - `plans/predicate-ization-execution-plan.md`（新增）：四个定义（叙事步载体、增量同一性、谓词→方面映射、非 `style` 投影或豁免）、四期出口、定义完成的验收证据、技术债衔接。
  - `ROADMAP.md`：新增 §五“谓词化推进计划”，只登记指针。
- **未改动**：母本、《编译规范》正文、卡片、技能包均未改；计划内涉及《编译规范》或母本的条目均标「待批」。
- **关联 ADR**：无
- **备注**：版本保持 0.9.0；不写检查器、不加校验规则；dist 不重打包；只提交，不推送、不打标签，不自评。

## 批次 0013 — 2026-11-18

- **批次号**：0013
- **日期**：2026-11-18
- **事项**：外部审计摘取与归位。PM 项目对软工谓词化出具 `AUDIT.md` 与 `ADR-0022`；本批登记其中与软工直接相关的 24 条结论（A 类 6、B 类 12、C 类 6），给出设计文档判断与谓词化计划的 15 条修订点。
- **涉及文件**：
  - `plans/audit-intake-20261118.md`（新增）：源文件与读法限制、逐条摘取与归位表、三类划分、待批清单、设计文档事实与判断（含目录草案）、计划修订点 R1–R15、本轮落盘清单。
  - `TECH-DEBT.md`：新增第 10 条 `TD-SE-PRED-001`（谓词求值级缺失），含证据、7 项缺失定义、影响面、落点顺序、代价与关闭判据；文件头补一句范围说明，区分第 1–9 条 AST 债与本条。
  - `ROADMAP.md`：§五加本文件与 `TD-SE-PRED-001` 指针。
- **未改动**：`plans/predicate-ization-execution-plan.md` 未改，修订点只在归位文件登记；母本、《编译规范》正文、`SKILL.md` 判据、卡片、`dist/` 均未改；不新建设计文档。
- **关联 ADR**：`project-management/adr/0022-predication-scope-and-authority.md`（仅作来源，不改其内容）
- **备注**：版本保持 0.9.0；dist 不重打包；只提交，不推送、不打标签，不自评。

## 批次 0014 — 2026-11-18

- **批次号**：0014
- **日期**：2026-11-18
- **事项**：谓词引擎技术路径选型（待裁定）与设计文档触发口径变更。
- **涉及文件**：
  - `plans/predicate-engine-selection.md`（新增）：五条轴（载体与语法／求值语义／求值器形态／接线范围／判定链接缝）各自路径的收益、代价、失效模式与不可逆点；与 PM `ADR-0022` 的分歧处理；推荐组合 A2+B2+C1+D2+E1，输出 token 56k–91k、生成侧墙钟 0.7–3.8 h（三空间另 14k–22k token、11–54 min，可延后）；三套备选。
  - `plans/predicate-ization-execution-plan.md`：§2.1 新增设计文档同步与冻结口径；§5 加选型文档指针。
  - `plans/audit-intake-20261118.md`：顶部状态、§2.3、§2.4、§3、§3.4、§4 由“触发后写设计文档”改为“随 P0 同步成稿、每标一批黄金样本回改一次定义、P0 通过时冻结、冻结后才允许写 AST 与求值器实现”。
  - `ROADMAP.md`：§五加选型文档指针并标注“待裁定”。
- **变更摘要**：
  1. **设计文档口径变更（已获批）**：原“P0 四组证据全过再开写设计文档”存在循环依赖（样本标注依赖定义成形），已否决；改为随 P0 同步成稿、逐批回改、P0 通过时冻结；冻结之后才允许写 AST 与求值器实现。P0 未过时保持 draft，不得用“先写实现再倒推定义”绕过。
  2. **选型结论（待人类裁定，不生效）**：推荐受限表达式 DSL＋三值语义＋手写 AST 解释器＋33 个卡片谓词名全覆盖（`style` 为第一垂直切片）＋独立引擎模块；`validate.py` V01–V09 不调用引擎。备选为最小闭环、转译执行、规则引擎。
  3. **与 PM `ADR-0022` 的分歧**：明确 PM 的“不造引擎”应读作“不造通用／整层引擎”，其决定 5 把受限 DSL＋求值器列为唯一合理中期扩展；软工不照抄“schema + Python”，因 220 名跨设计事实且 T1–T5 要求谓词增量。
- **未改动**：母本、《编译规范》正文、`SKILL.md` 判据、14 张卡片正文、`skills/software-engineering/validators/`、`dist/`；未写解析器／求值器代码，未新建 ADR，未新建设计文档。
- **关联 ADR**：`project-management/adr/0022-predication-scope-and-authority.md`（仅作对照，不改其内容）；本仓 ADR 待路径圈定后再落。
- **备注**：版本保持 0.9.0；dist 不重打包；只提交，不推送、不打标签，不自评。

## 批次 0015 — 2026-11-18

- **批次号**：0015
- **日期**：2026-11-18
- **事项**：谓词引擎选型获批准后的三件落盘——估算口径统一、三空间 `applicability` 入技术债、ADR 落定。
- **涉及文件**：
  - `adr/ADR-PRED-ENG-01-approved-20261118-谓词引擎选型与A2B2C1D2E1落地.md`（新增）：造谓词引擎、A2+B2+C1+D2+E1、各轴否决理由、不可逆点、与 PM `ADR-0022` 分歧处理、P0 顺序（`style` 为第一垂直切片）。
  - `adr/INDEX.md`：登记 `ADR-PRED-ENG-01`；统计更新为 38 份；注明 `ADR-GUARD-ACT-01`／`ADR-GUARD-02` 两份既有 ADR 尚未逐条登记。
  - `TECH-DEBT.md`：新增第 11 条 `TD-SE-PRED-002`（三空间 `applicability` 语义求值缺失）；文件头补范围说明；第 10 条“本轮不改计划”改为批次 0014 已落设计文档口径。
  - `plans/predicate-engine-selection.md`：工作量全部改为 token 预算／生成侧墙钟／闸门数；新增 §1.5 估算口径与缺口说明；状态由“待裁定”改为“分析记录（已裁定）”。
  - `plans/audit-intake-20261118.md`：C-03 与设计文档代价对照中的工时单位表述改为 token／墙钟口径。
  - `ROADMAP.md`：§五选型指针由“待裁定”改为已裁定并指向 ADR；补 `TD-SE-PRED-002` 指针。
- **变更摘要**：
  1. **估算口径统一**：采用 PM `spec/ESTIMATION_METHOD.md` 与 `adr/0023` 的 token／墙钟／闸门三件并列数；本仓无 D6 式吞吐锚、无 agent usage 记账、无历史行数—墙钟对照，全部数值标 `estimate`，并声明输入可能高于 3–6× 上界。`plans/`、`ROADMAP.md`、`CHANGELOG.md` 中本轮引入的工时单位表述已清除；批次 0014 对应表述按本批口径更正，旧数字不再有效。
  2. **三空间 `applicability` 入债**：登记 `TD-SE-PRED-002`，写明做什么、为什么现在不做、不做期间的判定面空白、启动条件与关闭判据；与 `TD-SE-PRED-001` 分立，第 10 条必须先于第 11 条。
  3. **ADR 落定**：`ADR-PRED-ENG-01` 记录“造谓词引擎”与五轴选型；`validate.py` V01–V09 不调用引擎；设计文档冻结前不开工 AST／求值器。
- **未改动**：母本、《编译规范》正文、`SKILL.md` 判据、14 张卡片正文、`skills/software-engineering/validators/`、`dist/`；未写解析器／求值器代码，未新建 `predicate_engine` 模块。
- **关联 ADR**：`ADR-PRED-ENG-01`（本批落定）；`project-management/adr/0022-predication-scope-and-authority.md`（对照，不改其内容）。
- **备注**：版本保持 0.9.0；dist 不重打包；只提交，不推送、不打标签，不自评。

## 批次 0016 — 2026-11-18

- **批次号**：0016
- **日期**：2026-11-18
- **事项**：按独立复核两轮意见整改；不新增功能、不写实现。
- **涉及文件**：
  - `plans/audit-intake-20261118.md`：C-03 恢复 PM `ADR-0022` 原文「P0+P1 粗估 4–7 人日」，另附 PM `ESTIMATION_METHOD.md` §5 对外换算 600k–1.05M 总 token 并标注“换算值”；C-01 行号由 `§6.4 L426` 改为 `§6.1 L375`。
  - `plans/predicate-engine-selection.md`：A3 生成侧墙钟由 29–151 min 改为 21.6–108 min；A 轴表补输入 token 列（A3 为 86.4k–259.2k）；8.69× 量级提示改为先去掉 1.5–3 再乘，得 4–11 h；拆分实测锚（100／150 tok/s）与折算系数（18 token/行、1.5–3）；输入比统一为 3–6 子区间并注明 PM 原文 2–6；删除“不复制其正文”与复述公式的矛盾表述；删除把本轮新值换算回人日的表述，改为 token 对照（旧值约 6.75M–9.75M total token，新值为其 1/11–1/44）；收窄“已清除”声明并注明历史单位保留；统一人类决策计数（基准 2 个，含 D3 另加 1）。
  - `TECH-DEBT.md`：第 11 条注明 `TD-SE-PRED-002` 为本仓编号；启动条件 2 补 owner 与定义位置，收窄“无成文定义”为“缺快照与时效规则”，条件 3 补触发事件；关闭判据定义“试点”；D2／14 卡依赖写入第 10 条关闭判据第 5 项；第 10 条判据 5 补豁免边界、上限与映射工件；新增第 12 条登记 `dist/` 未跟踪导致的 M5 缺口。
  - `adr/ADR-PRED-ENG-01-...md`：§5 改为“从 PM 与审计借用”，第 4 条溯至 `AUDIT.md` §9.1，并注明“不造谓词引擎”是审计转述；§7 统一复核轮次为 3–5（上限 5）、人类决策 2 个（含 D3 另加 1，合计 3）、拆分实测锚与折算系数；§9 去掉自指证据，补复核规程未生效说明与外部证据定义。
  - `todo.md` 与 `registry/projections/*`：由 `registry/scripts/project.py --project` 重新生成，`todo.md` STATUS 的 ADR 计数由 37 更新为 38。
- **变更摘要**：
  1. **0014／0015 记账更正**：0014 原文的工作量表述为「约 45–65 人日（三空间另 15–25 人日可延后）」，来源提交 `da4b1d7`；该段已被**就地改写**为 token／墙钟口径，0014 自此冻结，**此后不得再动 0014**。0015 已逐字恢复为提交 `5608121` 的原文；0015 第 1 条「`plans/`、`ROADMAP.md`、`CHANGELOG.md` 中本轮引入的工时单位表述已清除」表述过宽——实际只覆盖本轮新增与改写的文档，全仓历史文档仍有人日 9 处（`ADR-SRC-02` 2 处为真实工作量，另两文件 7 处为量纲示例），按 PM `ESTIMATION_METHOD.md` §5 保留原单位。以上更正同时引用 0014、0015。
  2. **第一轮复核整改**：C-03 原文与换算分列；C-01 行号更正；A3 墙钟更正；8.69× 去重乘；实测锚与折算系数分列；输入比统一；引用矛盾删除；历史单位声明收窄；TECH-DEBT 第 11 条补 owner／触发／试点／依赖；ADR §5／§7／§9 标注更正；todo 与投影重生成。
  3. **第二轮复核整改**：删除 selection 中把本轮新值换算回人日的回流；重写 0015 并把两次更正移入本条；人类决策点基准改为 2 个并注明含 D3 另加 1，同步备选 1 与 D3 轴；第 10 条判据 5 的豁免不免除判据 1，设 ≤3 个名字上限并逐名登记责任人／到期日／批准人，映射工件位置与形态写入判据；第 11 条条件 2 收窄；A 轴补输入 token 列；修正“五阶段”指代；ADR §9 补外部证据定义；登记 `dist/` 未跟踪导致的 M5 缺口与处置方向。
- **未改动**：母本、《编译规范》正文、`SKILL.md` 判据、18 张卡正文、`skills/software-engineering/validators/`、`dist/`；未写实现代码；未改历史 ADR 中的人日原文。
- **关联 ADR**：`ADR-PRED-ENG-01`（本批整改，不改变批准结论）；历史批次 0014、0015 只作引用与更正对象。
- **备注**：版本保持 0.9.0；dist 不重打包；只提交，不推送、不打标签，不自评；退回复核席再核一轮。

## 批次 0017 — 第三轮复核整改（2026-11-18）

- **事项**：按第三轮复核整改；不新增功能、不写实现。
- **批次纪律（本批新增）**：**未推送批次在推送前可合并整改；推送后严格只追加，不再就地改写**。0016 曾在本批前就地合并前两轮整改；**0016 自本批起冻结，此后只读不改**。0014、0015 按各自冻结状态处理，本批未动其正文。
- **涉及文件**：
  - `adr/ADR-PRED-ENG-01-...md`：§9「什么算外部证据」删去仓内文件，改为只认仓外留痕——人类在仓外签署并另行留痕的批准，以及带签名与时间戳的仓外裁定条目；复核记录与父会话转达只作转录。与 `ROADMAP.md` M6 一致，M6 未动。
  - `TECH-DEBT.md`：第 11 条条件 2 与条件 3 的互斥消除——具名要求留在条件 2，条件 3 改为「自动进入 D3 待具名队列，具名后方可裁定，未具名则裁定挂起」；条件 4 改为「按第 10 条判据 5（含 ≤3 豁免）完成」；第 10 条判据 5 的豁免上限注明「由人类核定，不由比例推导」；映射台账的权威方向与漂移检测指向 `DATA-SPEC.md` D3.18，检查器未落地前不宣称机检；第 12 条引用范围收窄为「今后新增的引用」，历史 ADR 与 `pilot` run-log 不回改，`todo.md` 由生成器带上条件。
  - `registry/predicate_map.yaml`（新增）：卡片谓词覆盖与豁免台账 schema＋空表；`entries: []`，填充属 D2 阶段。
  - `registry/DATA-SPEC.md`：D1.3 补文件角色；新增 D3.18（权威方向、`expr_refs` 形态、漂移判定与检测、豁免上限、当前状态）。
  - `registry/README.md`：目录导览补 `predicate_map.yaml` 行。
  - `registry/scripts/project.py`：状态块在「`--check` 硬失败 N」后自动注明以含 `dist/` 的工作区为条件。
  - `todo.md` 与 `registry/projections/*`：重新生成，带上该条件。
- **未改动**：第 12 条的「首选处置」与「关闭判据」按指示未动，待人类后续裁定；母本、《编译规范》正文、`SKILL.md` 判据、18 张卡正文、`validators/`、`dist/`、历史 ADR 的人日原文均未动；未写实现代码。
- **备注**：版本保持 0.9.0；只提交，不推送、不打标签。

## 批次 0018 — 2026-11-19

- **批次号**：0018
- **日期**：2026-11-19
- **事项**：按人类裁定处置 `TECH-DEBT.md` 第 12 条——走「提交发布清单」，不重打包、不动 `dist/`。
- **涉及文件**：
  - `registry/release_manifest.yaml`（新增）：M5 发布清单；仅 0.9.0 条目，记录真实 `sha256 d5c51ff8…68809`、68371 字节、源提交 `a199981`；`build_time` 取归档 gzip 头 MTIME（字节 4–8，little-endian uint32，值 1795001998）＝`2026-11-18T19:39:58+08:00`；note 只称内容与 `a199981` 树一致，不称唯一确定由该提交构建。
  - `registry/scripts/project.py`：删除 `DIST_DIR` 事实源；新增 `M5R`（hard，仓库级）与清单读取函数；工作区有归档时重算 `sha256`／字节比对，不一致给出期望／实际值；M5 状态串改为只读清单（`v0.9.0 清单在案`）；状态块移除「以含 `dist/` 的工作区为条件」尾注。
  - `ROADMAP.md`：L23 分发件说明与 M5 出口改为以清单记录为准，归档不入库；工作区有归档时 `--check` 比对；验证强度从「有物」降为「有记录」如实写明；未降级 M5 为「无需产出」。
  - `registry/DATA-SPEC.md`：D1.3 补文件角色；新增 D7.1（清单 schema、权威方向、M5R、验证强度降级与残余空洞）。
  - `registry/CHECK-SPEC.md`：新增 C5.23（M5R 判据、归档比对、不做项、编号审计）。
  - `registry/README.md`：目录导览补 `release_manifest.yaml` 行。
  - `TECH-DEBT.md`：第 12 条改写为已关闭，保留原现象、裁定、落地内容、关闭判据与证据、残余空洞；文件头说明同步。
  - `todo.md` 与 `registry/projections/*`：由 `registry/scripts/project.py --project` 重新生成。
- **变更摘要**：
  1. **人类裁定（2026-11-19）**：入库清单，`project.py` 改验清单而非归档文件；仓库不放二进制。批准时明确接受验证强度从「有物」降到「有记录」，不得表述为「已解决」或「等价于归档存在」。
  2. **第 12 条关闭证据**：提交 `7da640e` 后于干净 clone（无 `dist/`）实测 `--check` 硬失败 0、软警告 20、退出码 0；工作区实测 `M5R ✓ 清单与实际归档一致（68371 字节，sha256 d5c51ff8247d…）`；临时副本中把清单 `sha256` 改为合法但不符的值，实测 `M5R` 硬红并给出期望／实际值、退出码 1。第四轮复核后，有归档与无归档两种情形重新复验，均为退出码 0、硬失败 0、软警告 20。
  3. **残余空洞**：工作区无 `dist/` 时清单无法与实际归档比对；干净 clone 只验清单存在与字段合法，M5R 通过信息如实写明该残余；不校验归档内部、不重跑包内示例。
  4. **`build_time` 更正（第四轮复核 M1）**：原写「未记录／无法推出」是事实错误——归档 gzip 头第 4–8 字节为 little-endian uint32 MTIME，0.9.0 读得 1795001998＝`2026-11-18T19:39:58+08:00`（并用 0.8.0 归档交叉验证：其 gzip 头时间与文件 mtime 一致）。该时刻 UTC 11:39:58 早于 `a199981` 的提交时间 19:40:03，说明归档由提交前工作树构建。清单 note 中「逐文件比对确定」降级为「内容与 `a199981` 树一致」，不称唯一确定由该提交构建。
  5. **9 条可加固项登记**：第四轮复核列出、不阻塞推送的清单校验缺口，原样登记于 `TECH-DEBT.md` 第 12 条「后续可加固项」，并在 `todo.md` 候选可见；本轮不实施。
- **未改动**：未重打包、未改 `dist/`、未改 `.gitignore`；母本、《编译规范》正文、`SKILL.md` 判据、18 张卡正文、`validators/`、历史 ADR 的人日原文未动；未写谓词引擎实现代码；0014／0015／0016／0017 未动。
- **关联 ADR**：无（本条为发布面事实口径，不新增 ADR）。
- **备注**：版本保持 0.9.0；只提交，不推送、不打标签，不自评。

## 批次 0019 — 2026-11-19

- **批次号**：0019
- **日期**：2026-11-19
- **事项**：人类批准开工 P0 定义期（谓词化，10.2.3bis 层次二），落 D1–D4 的定义与登记载体；顺带上批遗留两处记账。不写解析器／求值器／引擎。
- **涉及文件**：
  - `pilot/schemas/narrative-step.schema.yaml`（新增）：P0-D1 叙事步记录 schema，draft；18 字段、R1–R10 规则、`atom_grammar` 规范化与同一性示例；快照携带 `atoms`（`atom_key`＋原子原文），`ref`／`sha256` 为摘要。
  - `编译规范.md`：T1 增 T1.1（叙事步记录，D1）与 T1.2（原子与同一性，D2），T2 增 T2.1（`no_op` 与向量推进，D2）；T1.2 按 Unicode `White_Space` 补齐结构空白、无引号实参禁空白、引号内原文保留、转义与零长度实参边界，T1.1 第 7 条改快照须带原子列表。仅动 T1／T2 的谓词化相关段落，未重排格式。
  - `registry/predicate_aspects.yaml`（新增）：P0-D3 方面映射，33 名；`aspect_mapped` 28 名（方面 4／5／9），`process_record` 5 名（0.18.6，不推进向量）；`vector_keys = [4,5,9]`。D3 的 `mapped` 全改 `aspect_mapped`，与 D4 覆盖口径 `mapped` 区分。
  - `registry/predicate_map.yaml`：D4 填充 33 名，`mapped` 30／`exempt` 3（`step_log`／`selection_procedure`／`verdict_table`）；豁免条目带 owner／due／approved_by／reason 且 `generated_by_pact: false`；`entry_fields` 增 `reason`／`generated_by_pact`；`expr_refs` 键 `step_id` 全部改 `layer`（值 `outputs`），头注与字段说明写明 `expr_sha256` 是卡片 `predicate_writes` 原文的 sha256、不是 `atom_key`。
  - `plans/predicate-ization-design.md`（新增）：P0 设计稿；第 2／4／5／6／11 章成稿到可引用，第 3／7／8／9 章明写未成稿，第 10 章为完整非目标清单；快照口径改为携带 `atoms`、摘要降级。
  - `pilot/predicate-ization/golden/`（新增）：骨架与标注口径，0 条样本；`README.md`、`manifest.yaml`、`_template.yaml`、`cases/.gitkeep`；S2 按 `snapshot_before.atoms` 对齐，S4 说明空 `aspects` 仅限 `process_record`，模板补齐 schema 必填项与前后快照。
  - `registry/DATA-SPEC.md`：D1.3 补两行；D3.18 把 `step_id` 改 `layer` 并写明 `expr_sha256` 口径；D7.1 补 `build_time` 取 gzip 头 MTIME；新增 D8（叙事步 schema，规则 R1–R10、快照带 `atoms`）与 D9（方面映射）。
  - `registry/CHECK-SPEC.md`：C5.23 补 `build_time` 取 gzip 头 MTIME 口径。
  - `registry/README.md`：目录导览补叙事步 schema 与 `predicate_aspects.yaml` 两行。
  - `ROADMAP.md`：M5 出口补构建时间取法。
  - `CHANGELOG.md`：本条追加两条更正记录——`todo.md` 状态块由 `--project` 重生成、3.11 为人工登记；第 10 章为完整非目标清单、未成稿标记在 3／7／8／9 章。0018 原文不改。
  - `registry/projections/STY.md`、`registry/projections/台账义务清单.md`、`registry/projections/索引.md`、`registry/projections/自检报告.md`：仅「生成于」时间戳随 `--project` 重生成而变，源哈希未变，不是内容更新。
- **变更摘要**：
  1. **D1**：叙事步记录形态落 schema，T1.1 给出 7 条字面判据；`predicate_write` 要求前后快照，`artifact_preservation` 与 `unqualified` 分道。
  2. **D2**：规范化原子 `name(args...)`、`atom_key = sha256(utf8(atom))`；同名同参＝`no_op`，不推进向量；`new` 才推进并在多方面各 +1；判定规则写入 T2.1。
  3. **D3**：选独立文件而非改词表，理由与 A1–A5 写在 D9；映射并集＝`vector_keys` 已机械核对。
  4. **D4**：33 名逐名登记；豁免用满 3 名上限，生成型 pact 不得豁免；名单独列待人类复核。
  5. **设计文档**：按「随 P0 同步成稿、每标一批黄金样本回改一次、P0 通过时冻结」写；第 3／7／8／9 章明写未成稿，第 10 章为完整非目标清单。
  6. **黄金样本**：只建骨架与标注口径（S1–S7、批次 12 条、P0 目标 36 条），0 条样本。
  7. **第六轮复核整改**（全部文档与 schema 级）：① 0018 恢复 `5e2e13f` 原文，两处更正改为本条追加，0014–0017 逐字未动；② 已推送批次不得就地改写，本条只追加；③ T1.2 与 `atom_grammar` 按 Unicode `White_Space` 属性全集处理结构位置空白（`name (x)`／`name\t(x)`／`name　(x)` 同键），无引号实参含任何空白即判不合格，引号内空白按原文保留（`name("a b")` 与 `name("a　b")` 不同键），并补转义与零长度实参规则；④ 快照改为必须携带 `atoms`（`atom_key`＋原子原文），`ref`／`sha256` 降为摘要，S2 按此对齐不削弱；⑤ 模板补齐 `predicate_increments`、`aspects_touched`、前后快照，删去非 schema 字段 `snapshot_before.predicates`；schema 的空 `aspects` 仅限 `process_record`，S4 同步；⑥ `predicate_map.yaml` 头注与 `entry_fields` 写明 `expr_sha256` 是卡片 `predicate_writes` 原文的 sha256、不是 `atom_key`；逐条复算 98 条一致（去重 33 名：28 名×1＋5 名×14）；⑦ `step_id` 改 `layer`，值 `outputs`；⑧ D3 的 `mapped` 全改 `aspect_mapped`，与 D4 的 `mapped` 分开。
  8. **第七轮复核整改**：① T1.2 改为三阶段——边界与区域识别（左到右扫描标出引用区、转义区与实参边界）→ 结构空白去除（限定在引用区与转义区之外）→ 实参校验；删去「上下文无关」这一断言，并补 `note("a , b")` 与 `note("a,b")` 不同键；② 写明转义规则在引号内外一律生效、引号内「原文保留」不豁免转义集，补 `note("C:\\temp")` 有效与 `note("C:\temp")` 判不合格；③ T2.1 第 1 条精确到 `snapshot_before.atoms`，与 schema R5 一致；④ T1.1 第 7 条与 schema R10 补 `atoms[].atom_key = sha256(utf8(atom))`；⑤ 0019 涉及文件补登 `7cece15` 夹带的 4 个投影文件（仅生成时间戳变化，源哈希未变）。
- **未改动**：母本、`SKILL.md` 判据、18 张卡正文、`validators/`、`dist/`、`.gitignore` 未动；未重打包、未写解析器／求值器／引擎；0014／0015／0016／0017／0018 逐字未动。
- **关联 ADR**：`ADR-PRED-ENG-01`（P0 冻结口径；本批在冻结前落地）。
- **备注**：只提交，不推送、不打标签。

## 批次 0020 — 2026-11-19

- **批次号**：0020
- **日期**：2026-11-19
- **涉及文件**：
  - `plans/predicate-ization-execution-plan.md`：P0 验收第一组降级。
  - `TECH-DEBT.md`：新增第 13 条。
  - `编译规范.md`：T1.2 三条记账、T1.1 第 7 条空基线说明。
  - `pilot/schemas/narrative-step.schema.yaml`：`atom_grammar` 三条记账、R10 空基线说明。
  - `pilot/predicate-ization/golden/README.md`、`manifest.yaml`：状态与第 1 批 12 条。
  - 新增：`pilot/predicate-ization/golden/cases/GC-0001.yaml` ～ `GC-0012.yaml`。
- **变更摘要**：
  1. **验收第一组降级**：原「双人独立标注（κ ≥ 0.80、一致率 ≥ 90%、分歧 > 2 条改定义重标）」改为「单人标注＋每批抽检」——执行席单人标注，独立复核席抽检 ≥ 20%（12 条批至少 3 条，必含全部 `undecidable` 与 `no_op` 边界条），不一致时回改定义并重标该条。计划明写这不是原定的双人独立标注、也不是等效替代；Cohen's κ 不可估计，任何一致性表述不得作为 P0 出口、定义质量或样本可靠性的依据。原「两次独立 agent 标注＋人工裁决替代」的说法已删除。
  2. **技术债第 13 条**：恢复双人独立标注并报 κ；为何现在不做（无第二独立标注者）；三项空白（标注者偏差不可检出、定义歧义只能靠抽检偶然暴露、κ 无从估计）；启动条件（出现与执行席无共同上下文的独立标注者或受训流程）；关闭判据（两次独立标注可算 κ 且达原阈值，抽检降级口径同时废止）。编号为本仓自铸，非审计编号。
  3. **四条记账**：`atom_grammar`／T1.2 的「该实参此前只有结构空白」改为「此前只有空白字符」；补「闭合引号必须与开启引号同类型」；T1.1 第 7 条与 schema R10 注明 `atoms` 允许空数组（首次写入空基线合法）；4 个投影的「生成于」时间戳未专改，留待下次重生成自然刷新。
  4. **黄金样本第 1 批**：12 条（`GC-0001`–`GC-0012`），按降级口径单人标注；9 条 `new`、2 条 `no_op`、1 条 `unqualified`；方面 4／5／9 为 4／4／2，过程记录 1；覆盖 11 个不同名字，`uncovered` 剩 22 名；`manifest.status` 由 `skeleton` 改为 `in_progress`，`counts` 与 `cases` 如实更新。
  5. **本批撞上的定义缺口**：`DG-0001`（`unqualified` 样本的 `expected.d3_disposition`／`d4_status` 无取值定义，`GC-0012` 记 `undecidable`）；`DG-0002`（`expected.vector_keys_after` 是「本步推进的键」还是「步后全部键」未定义，本批按前者标注，`no_op` 记空数组）；`DG-0003`（卡片 `predicate_writes` 多为裸名，到 `name(args)` 原子的参数位与取值域未定义，本批原子由叙事步直接给出）。三条均未改定义，待人类裁定。
- **未改动**：母本、`SKILL.md` 判据、18 张卡正文、`validators/`、`dist/`、4 个投影内容未动；未重打包、未写解析器／求值器／引擎；0014–0019 逐字未动。
- **关联 ADR**：无
- **备注**：单人标注，独立复核席抽检尚未执行；κ 不可估计。只提交，不推送、不打标签。

## 批次 0021 — 2026-11-19

- **批次号**：0021
- **日期**：2026-11-19
- **事项**：批次 0020 登记的三条定义缺口（`DG-0001`–`DG-0003`）经人类裁定后落地：改定义、按新口径重标受影响样本、把不修的一条登记为技术债。不留「先这么定、以后再说」的临时写法。
- **涉及文件**：
  - `pilot/predicate-ization/golden/README.md`：新增 S8 期望值形态、S9 原子来源；新增第 5 节「定义缺口登记（已裁定）」，原第 5 节冻结顺延为第 6 节。
  - `pilot/predicate-ization/golden/_template.yaml`：`vector_keys_after` 改 `advanced_keys`，补 `unqualified` 的 `expected` 形态注释。
  - `pilot/predicate-ization/golden/manifest.yaml`：`counts.undecidable` 改 0；`GC-0012` 条目改 `verdict`／`reject_code`；三条 `definition_gaps` 改「已裁定」并写裁定内容。
  - `pilot/predicate-ization/golden/cases/GC-0001.yaml`–`GC-0012.yaml`：字段改名与按新口径重标。
  - `pilot/schemas/narrative-step.schema.yaml`：R3 补 `unqualified` 样本 `expected` 字段的「不适用」说明；`aspects_touched` 注明与 `expected.advanced_keys` 同口径。
  - `TECH-DEBT.md`：新增第 14 条（DG-0003，五要素齐全，本仓自铸编号）。
  - `plans/predicate-ization-design.md`：第 5 章定义 `advanced_keys`；第 10 章加 DG-0003 指针。
- **变更摘要**：
  1. **DG-0001（`unqualified` 样本）**：`unqualified` 不产生谓词增量，不套映射字段。`expected` 只保留 `verdict: unqualified` 与 `reject_code`（本批为 `no_predicate_atom`），不含 `d3_disposition`／`d4_status`；schema R3 与 README S8 写明这两个字段在该情形**不适用**（没有可映射对象），不是「可留空」——留空不可判，不适用可判。`GC-0012` 按此重标，撤销 `undecidable`。
  2. **DG-0002（原 `vector_keys_after` 语义）**：改名 `advanced_keys`，语义定死为「本步 `change=new` 且 `aspects` 非空的键的并集」，去重升序；`no_op` 必为 `[]`。不加「步后全量键」字段——可从前序累积推出，多一个字段就多一个不一致的入口。同步 schema、设计稿与全部 12 条样本；`GC-0003`／`GC-0007` 的 `why` 删去「待裁定」表述。
  3. **DG-0003（卡片裸名到原子的桥）**：不修，登记为技术债。原子只由叙事步给出；卡片 `predicate_writes` 的裸名只作名字存在性与命名空间校验，不构成原子模板，不得据此反推参数。`TECH-DEBT.md` 第 14 条写全做什么／为何现在不做／不做期间的空白（卡片到原子无机器可核的桥、P3 的 18 张卡投影不能从卡片自动生成、覆盖核对只到名字一级）／启动条件／关闭判据（映射可从卡片推导且与叙事步原子一致，不一致项按定义回改）；设计稿第 10 章留指针。
  4. **重标与登记**：受影响条目 `GC-0001`–`GC-0012` 全部按新口径复核；`GC-0012`、`GC-0003`、`GC-0007` 按裁定重写 `expected`／`why`；README 第 5 节把 `DG-0001`–`DG-0003` 登记为「已裁定」并写明裁定内容。
  5. **校验**：用仓外临时脚本（`/tmp`，不入库）按定义复算 12 条——`atom_key = sha256(atom)`、`change` 只按 `snapshot_before.atoms` 判、`advanced_keys` 与 `aspects_touched` 一致、`no_op` 为空数组、`unqualified` 的 `expected` 只含 `verdict`／`reject_code`、manifest 计数与缺口状态一致，全部通过。
- **未改动**：母本、`SKILL.md` 判据、18 张卡正文、`validators/`、`dist/` 未动；未重打包；未写解析器／求值器／引擎；`编译规范.md` 不含 `expected` 字段，本批无对应改动；0014–0020 逐字未动。
- **关联 ADR**：无
- **备注**：抽检由独立复核席执行，执行席未自抽检。只提交，不推送、不打标签。

## 批次 0022 — 2026-11-19

- **批次号**：0022
- **日期**：2026-11-19
- **事项**：黄金样本第 2 批 12 条（`GC-0013`–`GC-0024`）；同时做掉第 1 批复核留的两条记账（`cases[].aspect` 与 `counts.by_aspect` 口径统一、`target_total`／`cases_per_batch` 嵌套位置说明）。
- **涉及文件**：
  - 新增：`pilot/predicate-ization/golden/cases/GC-0013.yaml`–`GC-0024.yaml`
  - 修改：`pilot/predicate-ization/golden/cases/GC-0011.yaml`（`aspect: 4` → `0`）
  - 修改：`pilot/predicate-ization/golden/manifest.yaml`（计数、`cases`、`uncovered`、`definition_gaps` 注记、两条记账）
  - 修改：`pilot/predicate-ization/golden/README.md`（批次进度、`cases[].aspect` 与 `by_aspect` 口径、字段位置）
  - 修改：`plans/predicate-ization-design.md`（第 11 章追加「回改记录」：第 1、2 批）
- **变更摘要**：
  1. **第 2 批 12 条**：方面 4／5／9＝3／3／4，`process_record` 2；`no_op` 2（`GC-0017`／`GC-0022`）、`unqualified` 2（`GC-0015` 记方面 4、`GC-0018` 记方面 5）。累计 24 条：`new` 17、`no_op` 4、`unqualified` 3、`undecidable` 0。
  2. **难度取向**：不堆简单 `new`，按定义压力点取材——结构空白重述后同 `atom_key` 判 `no_op`（`GC-0017`）、引号内空白是内容（`GC-0013`／`0016`／`0019`）、转义逗号与引号内逗号不切分实参（`GC-0014`／`0021`）、实参顺序不同即不同键（`GC-0020`）、同名前缀引号内外对照（`GC-0022`）、`process_record` 对 `mapped`／`exempt` 的对照（`GC-0023`／`0024`）。
  3. **覆盖**：新增名字 8 个（`consistency_rationale`／`data_lineage`／`expiry_of`／`idempotent`／`canary_gate`／`evolution_path`／`selection_context`／`verdict_table`）；累计 19／33，`uncovered` 14 名，未静默。
  4. **记账 1**：`GC-0011` 的 `aspect` 改为 `0`（与模板「过程记录写 0」一致）；`cases[].aspect` 语义写清为「案例所属方面，取自源卡 `_aspect`」，`counts.by_aspect` 按 4／5／9 取该字段、`process_record` 取 `d3_disposition` 计数、`'0'` 取 `aspect=0` 且非 `process_record` 计数，从 `cases[]` 重算与清单相等。
  5. **记账 2**：`manifest.yaml` 顶部与 README §4 注明 `target_total` 在 `quotas` 下、`cases_per_batch` 在 `batch_policy` 下，外部脚本不得读顶层同名字段。
  6. **校验**：仓外临时脚本（`/tmp`，不入库）复算 24 条——`atom_key = sha256(atom)`、`change` 只按 `snapshot_before.atoms` 判、`advanced_keys` 与 `aspects_touched` 一致、`no_op` 为空、`unqualified` 的 `expected` 键集精确、`cases[]` 重算的 `by_aspect` 与清单相等、`uncovered` 与「33 名减已用名」一致，0 错误。
  7. **配额三层口径（人类 2026-11-19 裁定）**：桶数 36（方面 4／5／9 各 10 ＋ `process_record` 6）；`unqualified` 单列配额 4，只数 `aspect=0` 的样本、不占桶；文件总数 40＝36＋4。当前 24 个文件＝桶 23＋`aspect=0` 的 `unqualified` 1（`GC-0012`）；`counts.unqualified` 为 3（含占桶的 `GC-0015`／`GC-0018`），与配额进度 1 不是同一口径，已在 `quotas.unqualified_note` 写清。剩余 16 条＝桶 13（4:3、5:3、9:4、`process_record`:3）＋ `aspect=0` 的 `unqualified` 3；第 3 批 12 条＝桶 12，第 4 批 4 条＝桶 1＋`unqualified` 3。
- **未改动**：母本、`SKILL.md` 判据、18 张卡、`validators/`、`dist/`；未写解析器／求值器／引擎；0020–0021 逐字未动。
- **关联 ADR**：无
- **备注**：单人标注，第 2 批抽检尚未执行，`sampling_status` 保持 `pending`，执行席未自抽检。只提交，不推送、不打标签。

## 批次 0023 — 2026-11-19

- **批次号**：0023
- **日期**：2026-11-19
- **事项**：两处口径裁定落地——① 任何 `unqualified` 一律 `aspect = 0`、不占桶；② S9 的约束对象扩到卡片 `predicate_writes` 条目整体（含带签名条目）。
- **涉及文件**：
  - 修改：`pilot/predicate-ization/golden/cases/GC-0015.yaml`、`pilot/predicate-ization/golden/cases/GC-0018.yaml`（`aspect` 4／5 → 0，原指向方面记入 `notes`，不进统计）
  - 修改：`pilot/predicate-ization/golden/manifest.yaml`（`quotas.unqualified_note`／`unqualified_progress`／`remaining_gap`、`counts.by_aspect`／`by_aspect_basis`、`cases[]` 两条、DG-0003 的 `text`／`resolution`）
  - 修改：`pilot/predicate-ization/golden/README.md`（S9、§4 三层口径与进度、`cases[].aspect` 口径、§5 DG-0003 表述）
  - 修改：`pilot/predicate-ization/golden/_template.yaml`（`aspect` 注释、原子来源注释）
  - 修改：`TECH-DEBT.md` 第 14 条（裸名 → 条目整体，含带签名条目）
  - 修改：`plans/predicate-ization-design.md`（第 10 章 DG-0003 指针、第 11 章回改记录）
- **变更摘要**：
  1. **`unqualified` 一律 `aspect = 0`**：不存在「带方面语境的 `unqualified`」中间态——被判不合格即无方面主张，给它记方面等于把「本来想写哪个方面」混进「实际产出了什么」。`GC-0015`／`GC-0018` 的 `aspect` 改为 0，原本指向的方面 4／5 写进该条 `narrative_step.notes`，不进任何统计。
  2. **配额重算**：当前 24 个文件＝桶 21（4／5／9 = 6／6／6、`process_record` 3）＋ `aspect=0` 的 `unqualified` 3；`counts.by_aspect` = `{4:6, 5:6, 9:6, process_record:3, 0:3}`。剩余 16 条＝桶 15（4:4、5:4、9:4、`process_record`:3）＋ `unqualified` 1。批次分配：第 3 批 12 条全走桶（4:4、5:4、9:4）；第 4 批 4 条＝桶 3（`process_record`:3）＋ `unqualified` 1。文件总数 24＋12＋4＝40。
  3. **两个口径继续单列**：`counts.unqualified` 数全部 `outcome_kind=unqualified`；配额进度只数 `aspect=0` 的条目。此刻两者都是 3，定义不同，不合并、不互相替代。
  4. **S9 扩到带签名条目**：约束对象改为「卡片 `predicate_writes` 条目整体」，裸名与带签名条目（如 `selection_context(DP, F, C)`）一视同仁——都只作名字存在性与命名空间校验，都不得据以反推参数位或取值域；签名只证明字面存在，推不出取值域。README S9、`manifest.yaml` DG-0003、`_template.yaml` 注释、设计稿第 10 章、`TECH-DEBT.md` 第 14 条同步；技术债里写明这正是 P3 的 18 卡投影不能从卡片自动生成的原因。
  5. **校验**：仓外临时脚本（`/tmp`，不入库）复算 24 条——0 错误；`by_aspect` 从 `cases[]` 重算与清单相等（`{4:6,5:6,9:6,process_record:3,0:3}`）；桶 21、`aspect=0` 的 `unqualified` 3、剩余 15＋1＝16、`expected_files` 40；`sampling_status` 仍 `pending`。仅保留「distinct names 19 < 20」进行中提示。
- **未改动**：母本、`SKILL.md` 判据、18 张卡、`validators/`、`dist/`；未写解析器／求值器／引擎、未重打包；0014–0022 逐字未动（`0022` 未推送，按例外规则本可就地合并，选择另开 `0023` 以保持「既往批次不改」；`0022` 中的旧配额数字由本批取代，以本批为准）。
- **关联 ADR**：无
- **备注**：单人标注，第 2 批抽检尚未执行，`sampling_status` 保持 `pending`，执行席未自抽检。只提交，不推送、不打标签。

## 批次 0024 — 2026-11-20

- **批次号**：0024
- **日期**：2026-11-20
- **事项**：黄金样本第 3 批 12 条（`GC-0025`–`GC-0036`，全部进桶）；同时做掉三项记账（抽检状态改为实际结论、覆盖进度落纸、0023 取代句补全）。
- **涉及文件**：
  - 新增：`pilot/predicate-ization/golden/cases/GC-0025.yaml`–`GC-0036.yaml`（12 条全部进桶：方面 4／5／9 各 4，无 `process_record`、无 `unqualified`）
  - 修改：`pilot/predicate-ization/golden/manifest.yaml`（`sampling_status` 与结论登记、覆盖进度注释、`counts`／`cases`／`uncovered`／`quotas.remaining_gap`、第 3 批无新增定义缺口注记与多方面取材观察）
  - 修改：`pilot/predicate-ization/golden/README.md`（顶部抽检状态、§4 批次与配额进度同步至 36 文件／33 桶／剩余 4 条、覆盖进度与批次要求）
  - 修改：`plans/predicate-ization-design.md`（第 11 章回改记录追加第 3 批，无判定口径变更）
- **变更摘要**：
  1. **第 3 批 12 条（全部进桶，方面 4／5／9 = 4／4／4）**：方面 4 = `GC-0025` `owner(order_db,"ops, data")`（引号内逗号＋空格是内容，不切分实参）／`GC-0026` `sensitivity(order_db,"pii \"masked\"")`（引号内 `\"` 不闭合引号）／`GC-0027` `invariant(order_db,ledger,nonneg(sum(a,b)))`（无引号嵌套括号按深度配对；源卡 G-TRUNK-CSL）／`GC-0028` `shared_write_exception(order_db,ledger_svc,exit_2026q4)`（原始写法 name 与 ( 之间 U+3000、其余结构位 U+0020，规范化后与基线同键，**no_op**）。方面 5 = `GC-0029` `saga(order_flow,reserve\,release)`（`\,` 不切分）／`GC-0030` `orchestrator(order_flow,"saga_coord")`（基线为单引号写法；引号不剥离、不做类型转换，判 new）／`GC-0031` `compensation(order_flow,undo\(charge\))`（`\(` `\)` 是字面内容，与基线真嵌套括号不同键）／`GC-0032` `interaction_flow(order_ui,checkout,"click\u00A0confirm")`（引号内 NBSP U+00A0 按原文保留，与基线普通空格不同键）。方面 9 = `GC-0033` `deploy_strategy(order_svc,blue_green,"C:\\temp",rollback_v2)`（`\\` 字面反斜杠）／`GC-0034` `strangler_sequence(legacy_order,route(api(v1,v2),legacy),30d)`（多层嵌套括号、内层逗号不切分）／`GC-0035` `canary_gate(order_svc,"phase 1",5pct)`（仅结构空白不同，跨批复用 `GC-0019` 增量原子，同键 **no_op**；基线两项逐项给出）／`GC-0036` `evolution_path(order_svc,'cutover \'big bang\'',lrm_2026q4,thresholds_v1)`（单引号内 `\'` 不闭合引号）。六类转义（`\\ \( \) \, \' \"`）全覆盖；`atom_key` 全部以 `printf '%s' '<atom>' | sha256sum` 实算写入（NBSP 条以 `printf '\xc2\xa0'` 构造字节），每条 trace 附计算命令与完整键值；`snapshot_before.atoms` 逐项 `{atom_key, atom}`、按 `atom_key` 升序去重；期望值按 T1.2／T2.1 与 S1–S9 手算。
  2. **覆盖**：本批新引入谓词名 8 个（批次要求 ≥2，取自原 `uncovered` 14 名）：`owner`／`sensitivity`／`invariant`／`shared_write_exception`／`saga`／`orchestrator`／`compensation`／`interaction_flow`。累计覆盖 **27／33**，`min_distinct_names: 20` 已满足；仍 `uncovered` 6 名：`cleanup_filed`／`exclusion_record`／`flag`／`quality_impact_card`／`selection_procedure`／`step_class`，未静默。
  3. **记账 1（抽检状态）**：`manifest.yaml` 的 `sampling_status` 由 `pending` 改为 `partial`，新取值含义在 `annotation_method` 注释中定义（pending＝无任何批次抽检结论登记；partial＝部分批次完成、其余待；complete＝全部批次完成）。`sampling_note` 与 README 顶部改为实际结论：第 1 批抽检 5 条一致、第 2 批抽检 6 条一致，合计 **11 条一致、0 不一致**；**抽检由独立复核席在仓外执行，仓内只登记结论**，不是仓内签署；第 3 批抽检尚未执行。κ 不可估计的口径不变。
  4. **记账 2（覆盖进度落纸）**：README §4 与 manifest 注释明确写出第 2 批后覆盖 19／33、距 `min_distinct_names: 20` 差 1；「第 3 批至少引入 2 个新名字」写入批次要求（不卡在 20 上）；第 3 批实际引入 8 个后覆盖 27／33。
  5. **记账 3（更正，引用批次 0023）**：0023「未改动」项的取代句只声明「`0022` 中的旧配额数字由本批取代」，未声明取代 0022 里 `GC-0015`／`GC-0018` 的方面归属（0022 第 1 条写作「`GC-0015` 记方面 4、`GC-0018` 记方面 5」）。按 0023 引入的三层口径，该归属表述亦被取代：`GC-0015`／`GC-0018` 一律 `aspect=0`、记入 `'0'` 桶、不占桶、只计入 `unqualified` 单列配额；其原指向的方面（4／5）只存于该两条 `notes`，不进任何统计。以本条更正为准；按只追加规则不改 0023 原文。
  6. **进度与计数**：`counts` 更新为 total 36、new 27、no_op 6、unqualified 3、undecidable 0；`by_aspect` 由 `cases[]` 重算为 `{4:10, 5:10, 9:10, process_record:3, 0:3}`，五项相加等于 total；桶数 = 33。`no_op_min: 6` 达标（`GC-0003`／`0007`／`0017`／`0022`／`0028`／`0035`）。`remaining_gap`：第 4 批 4 条＝`process_record` 3 ＋ `unqualified` 1；文件总数 36＋4＝40。
  7. **设计回改**：第 3 批**无判定口径变更**——六类转义、嵌套括号、引号内逗号／空白（含 NBSP）、结构空白（含 U+3000）、单双引号对照均可按 T1.2／T2.1 现行文本唯一定键，未新增定义缺口。留档三条观察：①「需要多个方面的名字」本批无法取材（33 名全部单方面，S3 禁止自造方面；取材观察、非定义缺口，留待首个多方面谓词）；② 卡片 `predicate_writes` 条目按 S9／TECH-DEBT 14 只作名字存在性与命名空间校验，不反推参数位／取值域；③ `GC-0035` 两个基线键与 `GC-0019` 逐一相同，跨批同一性按 T2.1「与历史写法无关」成立。
- **未改动**：母本、`SKILL.md` 判据、18 张卡、`validators/`、`dist/`；未写解析器／求值器／引擎、未重打包；不改 `pilot/schemas/narrative-step.schema.yaml`、不改《编译规范》T1.2／T2.1；未新增定义缺口与 `reject_code`；0014–0023 逐字未动。
- **关联 ADR**：无
- **备注**：单人标注，第 3 批抽检尚未执行；第 1–2 批抽检结论（11 条一致、0 不一致）为独立复核席仓外执行的登记，不是仓内签署。只提交，不推送、不打标签；不自评，不写「已复核」「已验证」。

## 批次 0025 — 2026-11-21

- **批次号**：0025
- **日期**：2026-11-21
- **事项**：黄金样本第 4 批（收尾批）4 条（`GC-0037`–`GC-0040`）；同时做掉三项记账（第 3 批抽检结论入仓、S8「键」用词观察登记、收尾记账 `remaining_gap` 归零）。40 文件齐、桶 36 满、`unqualified` 4 满。
- **涉及文件**：
  - 新增：`pilot/predicate-ization/golden/cases/GC-0037.yaml`–`GC-0040.yaml`（3 条 `process_record` ＋ 1 条 `unqualified`）
  - 修改：`pilot/predicate-ization/golden/manifest.yaml`（`sampling_status: complete` 与枚举含义、`sampling_note` 23 条结论、`counts`／`cases`／`uncovered`／`quotas.unqualified_progress`／`remaining_gap` 归零、第 4 批无新增定义缺口注记）
  - 修改：`pilot/predicate-ization/golden/README.md`（顶部状态、§1 目录注释、§4 批次与配额进度同步至 40 文件／36 桶／`unqualified` 4、覆盖 29／33）
  - 修改：`plans/predicate-ization-design.md`（第 11 章回改记录追加第 4 批，无判定口径变更）
- **变更摘要**：
  1. **第 4 批 4 条（收尾批）**：`GC-0037` `exclusion_record(DP-5.2,STP-004,applicability.problem_space)`（新名，`process_record`／`mapped`，new；排除记录只记「为何未选」，不是设计事实）／`GC-0038` `selection_procedure(DP-5.2,S6,C6)`（新名，`process_record`／`exempt`，new；规程完成记录覆盖 S0–S6，归任一方面都会重复计数）／`GC-0039` `step_log(DP-4.5,S1,order_db,verified,selected,C7,alice)`（`process_record`／`exempt`，**no_op**——复盘评审逐字重登 `GC-0011` 的增量原子，跨批复用同键；首个 `no_op` × `process_record` 交叉，压 R9 与 T2.1 的叠加，`advanced_keys` 必为 `[]`）／`GC-0040` `unqualified`（源卡 G-TRUNK-DPS 条款 9.5；决定不为报表服务单设灰度门禁、沿用既有检查单，无可写谓词原子；`expected` 只写 `verdict: unqualified` 与 `reject_code: no_predicate_atom`，`d3_disposition`／`d4_status` 不适用、两键不写；原指向方面 9 记于 notes，不进统计）。三条过程记录均按 S4 写明「为何不是设计事实」；`atom_key` 全部以 `printf '%s' '<atom>' | sha256sum` 实算写入，每条 trace 附计算命令与完整键值；`snapshot_before.atoms` 逐项 `{atom_key, atom}`、升序去重。
  2. **覆盖**：本批新引入谓词名 2 个（批次要求 ≥2，取自原 `uncovered` 6 名）：`exclusion_record`／`selection_procedure`。累计覆盖 **29／33**；仍 `uncovered` 4 名：`cleanup_filed`／`flag`／`quality_impact_card`／`step_class`，未静默。
  3. **记账 1（第 3 批抽检结论入仓）**：第 3 批抽检已由独立复核席**在仓外执行**：12 条全覆盖、12 条一致、0 不一致、0 条「无法判定」。`manifest.yaml` 的 `sampling_status` 由 `partial` 改为 `complete`，枚举含义同步定义（complete＝已执行抽检的全部批次结论均已登记、无悬置结果；该值不主张全部样本均已抽检——第 4 批抽检尚未执行，结论另行追加登记）。`sampling_note` 与 README 顶部改为：第 1 批 5 条一致＋第 2 批 6 条一致＋第 3 批 12 条一致＝**23 条一致、0 不一致**；仓内只登记结论，不是仓内签署。κ 不可估计的口径不变。
  4. **记账 2（S8「键」用词观察，不改口径）**：复核席指出 S8 的「键」可能被读成 `atom_key`。本批**不改 S8**：上下文已由字段名（`advanced_keys`）约束，收尾批改动定义的风险大于收益。仅登记观察（本条与设计稿第 11 章第 4 批回改记录），不为交差顺手改字；留待冻结后如有歧义实例再议。
  5. **记账 3（收尾记账）**：`remaining_gap` 归零——40 文件齐＝桶 36 满（4／5／9 = 10／10／10 ＋ `process_record` 6）＋ `aspect=0` 的 `unqualified` 4 满（`GC-0012`／`0015`／`0018`／`0040`）；`expected_files: 40` 标为已达成。`status` 仍 `in_progress`、`frozen_at` 仍 `null`——**冻结是人类门，执行方不自行冻结**，本批不写「P0 已通过」。
  6. **进度与计数**：`counts` 更新为 total 40、new 29、no_op 7、unqualified 4、undecidable 0；`by_aspect` 由 `cases[]` 重算为 `{4:10, 5:10, 9:10, process_record:6, 0:4}`，五项相加等于 total；桶数 = 36。`no_op_min: 6` 达标且超出（共 7：`GC-0003`／`0007`／`0017`／`0022`／`0028`／`0035`／`0039`）；`unqualified_progress: 4` 满。
  7. **设计回改**：第 4 批**无判定口径变更**——`no_op` × `process_record` 交叉可由 T2.1 与 S4 叠加唯一判定，`unqualified` 沿用 DG-0001 裁定；未新增定义缺口、未新开 `reject_code`。留档三条观察：① `GC-0039` 跨批复用 `GC-0011` 键，同一性与批次边界无关；② S8 用词观察不改口径（见记账 2）；③ `process_record` 与 `exempt` 是两个独立维度，`GC-0037`（mapped）与 `GC-0038`（exempt）对照落实。
- **未改动**：母本、`SKILL.md` 判据、18 张卡、`validators/`、`dist/`；未写解析器／求值器／引擎、未重打包；不改 `pilot/schemas/narrative-step.schema.yaml`、不改《编译规范》T1.2／T2.1、不改 S8 口径；未新增定义缺口与 `reject_code`；0014–0024 逐字未动。
- **关联 ADR**：无
- **备注**：单人标注，第 4 批抽检尚未执行；第 1–3 批抽检结论（23 条一致、0 不一致）为独立复核席仓外执行的登记，不是仓内签署。40 文件齐是收尾就绪的待验主张，不是「P0 完成」；冻结与出口验收留人类门。只提交，不推送、不打标签；不自评，不写「已复核」「已验证」「已冻结」。

## 批次 0026 — 2026-11-21

- **批次号**：0026
- **日期**：2026-11-21
- **事项**：治理补丁——新增「推送前安全审核」条款。该条款由人类 **2026-11-21 批准生效**（批准方式：人类在会话中对补丁全文拍板「本条消息即批准」）；批准前按草案对待的纪律已完成其使命，本批为批准后的落盘登记。
- **涉及文件**：
  - 修改：`AGENTS.MD`（第 20 条独立复核规程之后插入安全审核条款，全文照录补丁；文件无显式编号，其后条目位置顺延为第 22–26 条）
  - 新增：`review/security/SECURITY-CHECKLIST.md`（必查项的可执行版本：审核对象命令、①凭据②本机环境③私人内容三组扫描命令、判定与处置、审核记录字段、不可逆操作门）
- **变更摘要**：
  1. **条款要点**：任何推送／打标签／打包／发布／升版本之前，除独立复核外必须完成一次安全审核，两者互不替代；审核对象为待推送全部提交与差异＋全历史（`git log --all -S`）；必查项①私钥与凭据②本机环境信息③与任务无关的私人笔记／日志／截图／主机指纹；命中任一项即不得推送，确需保留的内容放仓外、仓内只留脱敏摘要；审核记录放 `review/security/`，无记录即视为未审核；改写历史／`push --force*`／删远端分支或标签须先取得人类明确授权并先做 `git bundle` 备份；公开仓库按「一旦进入远端即视为已泄露」处理，清除历史不等于收回凭据，密钥与 token 须轮换。
  2. **立法事实登记**：现行 25 条中原本没有推送前安全审核条款；`git log --all -S'安全审核'` 在全部历史命中 0 次，`安全审核`／`敏感信息` 在落盘前的当前树也搜不到——该条款是**新增**，不是恢复被删条款（待验主张，落盘前由执行席检索核实）。
  3. **与独立复核的边界**：第 20 条（独立复核规程，仍为草案、待人类批准）约束「未参与者在推送前只读复核」；新条款约束「敏感信息扫描」，审核可由执行方按检查单执行并留记录，但不得据审核记录声称「已复核」。两闸并列，任一缺失都不得推送。
  4. **编号顺延影响**：`AGENTS.MD` 为无编号 bullet 列表，插入后原第 21–25 条（adr／registry／技能包／dist／review）位置顺延；落盘前检索未发现树内对「第 21–25 条」的硬引用（待验主张）。第 25 条（现第 26 条）「review/ 只放复核者产出的只读记录」与安全审核记录、检查单同目录存放的关系：安全审核记录属审核者产出的只读记录，检查单为人类批准的规约附件，均不随包发布。
  5. **不随包发布**：打包源树为 `skills/software-engineering/`（`build_package.py` 的 ROOT），根部 `review/` 在源树之外，天然不入包；未改打包脚本与 `validators/`。
- **未改动**：母本、`SKILL.md` 判据、18 张卡、`validators/`、`dist/`、`独立复核规程.md`（仍草案）；0014–0025 逐字未动。
- **关联 ADR**：无
- **备注**：条款自本批批准起生效，**不溯及既往**——不得据其声称任何既有提交「已通过安全审核」；下一次推送前须按 `review/security/SECURITY-CHECKLIST.md` 完成审核并留记录。另登记一项观察：本批落盘前发现仓库历史在本会话第 4 批提交后被仓外操作重写（第 4 批提交 SHA 由 3e7bb2c 变为 0824cf0，差异含删除一份更新记录文件），该操作非本会话执行，其授权与备份情况须由操作方按新条款第 5 节补登记。本批只提交，不推送、不打标签。

## 批次 0027 — 2026-11-21

- **批次号**：0027
- **日期**：2026-11-21
- **事项**：历史重写后的 SHA 对照记账。登记 2026-11-21 全历史重写这一事实、旧 SHA 与新 SHA 的对应关系、受影响的仓内引用，以及残余风险实测结论。
- **涉及文件**：
  - 修改：`registry/release_manifest.yaml`（0.9.0 条目 `source_commit` 由旧 SHA `a1999810…` 改为新 SHA `273dde068f8fb9a8234a9081562e03c2257dd88a`；`note` 追加一句说明；`build_time`／`sha256`／`bytes` 未动）
  - 修改：`CHANGELOG.md`（本批次，仅追加）
- **事件**：公开仓库 `onlookor/skill-software-engineer` 含本机环境笔记 `[已移除]`。2026-11-21 经人类授权，对全部提交做历史重写以清除该文件，并 `push --force` 覆写远端。重写前已做 `git bundle` 备份，存于仓外私人目录（路径不登记），可 `git clone` 复核旧历史。
- **影响**：
  1. 全部提交 SHA 变化，凡按旧 SHA 引用的地方一律作废。
  2. `CHANGELOG.md` 0017 引用的 `da4b1d7`／`5608121`、0019 引用的 `a199981` 均属旧 SHA，**原文保留不改**（只追加规则），其对应关系以本批次对照表为准。
  3. `registry/release_manifest.yaml` 的 `source_commit` 原为旧 SHA，本批已改为新 SHA。
- **SHA 对照表**（对应关系按**提交主题**逐条核出，未用旧 SHA 直接映射）：

| 旧 SHA | 新 SHA | 说明 |
| --- | --- | --- |
| `a199981` | `273dde0` | 适用面收窄按 minor 并入 0.9.0（0.9.0 归档的源提交） |
| `da4b1d7` | `3901e53` | 谓词引擎技术路径选型（待裁定）与设计文档冻结口径 |
| `5608121` | `73631ac` | 谓词引擎选型裁定（ADR-PRED-ENG-01）与估算口径统一 |
| `045ee3c` | `1ba1093` | 补交三份前序文档（重写后该提交已不含本机笔记） |
| `e930095`（原远端 tip） | `773200b` | 第 3 批黄金样本 |
| tag `layer-skill-narrow-20261116`（旧指 `83d7f0d`） | `3311657` | 标签随历史重写改指 |

- **对照核验（待验主张）**：
  - 新 SHA 均存在，主题与上表逐条一致：`273dde0`「适用面收窄按 minor 并入 0.9.0，并在 SKILL/README 披露子进程与夹具类缺陷不适用」／`3901e53`「docs: 谓词引擎技术路径选型（待裁定）与设计文档冻结口径」／`73631ac`「docs: 谓词引擎选型裁定（ADR-PRED-ENG-01）与估算口径统一」／`1ba1093`「补交三份前序分析文档…」／`773200b`「feat(p0): 黄金样本第 3 批 12 条…」；标签 `layer-skill-narrow-20261116` 现指 `3311657`。
  - 三个旧 SHA 在本地**仍可被 `git cat-file -t` 解析为 commit**，这是重写后未 `gc` 的悬空对象（`git fsck --dangling` 可见 `e9300954…`，`refs/remotes/origin/main@{1}` 记有 forced-update）。它们**不再是 `main` 的祖先**，任何分支与远端跟踪引用都不包含它们——「本地已不存在」的准确表述是「本地已不在任何引用链上，仅剩悬空对象」。该情形不改变对照表结论，但说明本地仍可按旧 SHA 取到旧内容。
  - `[已移除]` 存在于旧 `045ee3c` 树、不存在于新 `1ba1093` 树，也不存在于当前树。
- **残余风险（本批实测，待验主张）**：
  1. GitHub 仍可按旧 SHA 返回旧对象。实测（2026-11-21，GitHub REST API，仓 `onlookor/skill-software-engineer`）：旧 `a1999810…` 与旧 tip `e9300954…` 均返回 `HTTP 200`，且旧提交信息内容可读出；以 `ref=<旧 SHA>` 取 `[已移除]` 亦返回 `HTTP 200`。新 SHA 同样返回 200，属正常。结论：**force push 未使旧对象立即不可访问**，公开仓库下应视为已泄露。
  2. 彻底清除需 GitHub Support 强制 GC（或删除并重建仓库）。在此之前，旧 SHA 与旧文件内容仍可从远端取回。
  3. 该文件名已在本次重写中从提交信息移除（提交主题不再包含该文件名），原「提交主题逐字保留」主张作废；旧对象仍可经旧 SHA 取回，该痕迹需随远端 GC 一并处理。
  4. 若该笔记含 SSH 私钥、口令或 token 线索，按 `AGENTS.MD` 安全审核条款「一旦进入远端即视为已泄露」，须轮换相关凭据并留审核记录；本批未取得笔记内容，无法判定是否含凭据（待验主张）。
- **未改动**：`dist/`、母本、`SKILL.md`、18 张卡、`validators/`、`AGENTS.MD`、`review/security/`；未重打包（`sha256`／`bytes`／`build_time` 保持原值）；0014–0026 逐字未动。不打标签、不推送。
- **关联 ADR**：无
- **备注**：本批次只登记事实与对照关系，不声称任何提交「已复核」「已通过」；对照表的正确性以独立复核席按提交主题复核为准。历史重写的授权、备份与凭据轮换责任属操作方，本仓内只留脱敏结论。

## 批次 0028 — 2026-11-21

- **批次号**：0028
- **日期**：2026-11-21
- **事项**：应答独立复核席对 `origin/main..HEAD` 判「不可推送」的整改（前两项）：① 0027 的本机环境信息脱敏更正；② 补本次待推送集的安全审核记录。另补两次会话授权的登记、两处可选小项。
- **涉及文件**：
  - 修改：`CHANGELOG.md`（本批次，仅追加）
  - 新增：`review/security/20261121-pending-set.md`（安全审核记录）
  - 新增：`review/approvals/20261121-authorizations.md`（两次会话授权登记）
  - 修改：`review/security/SECURITY-CHECKLIST.md`（文件末尾补换行符，原文件缺行尾换行；正文未动）
- **变更摘要**：
  1. **0027 脱敏更正**：0027 事件行登记的重写前备份路径，属**本机环境信息**（登录用户名＋目录结构），命中 `SECURITY-CHECKLIST.md` 必查项②，不得留在仓内。**更正为**：重写前备份 bundle 存于**仓外私人目录，路径与文件名均不登记**；备份的存在只作仓外旁证。该句已在本次整改中按 0017 例外规则就地删除（见第 7 条），未推送历史不含该路径。
  2. **安全审核记录**：新增 `review/security/20261121-pending-set.md`，审核对象为 `origin/main`（`773200b`）..本次待推送集四个提交＋全历史（0027/0028 合并前审核；合并后仅新增已复核内容）；含命令清单、三类必查项的命中统计与分类依据、整改项状态、判定与残余风险。统计结论（待验主张）：私钥／凭据前缀 0（工作树、待推送集新增行、全历史均为 0）；`(password|secret|token|api_key)[:=]` 35 行／36 处全为代码标识符与术语，无凭据值；本机家目录绝对路径 70 行／76 处，其中待推送集新增行 0 处（0027 原 1 处已就地删除，见第 7 条）、历史文档 67 行／73 处已在公开远端；`hostname|proxy|:NNNN` 187 行／296 处，`hostname`／`proxy` 为概念讨论、`:NNNN` 为 YAML 行号引用而非端口；内网 IP 0；文件名模式 1 处（`run-log.md`），该文件不含①类凭据但含②类本机路径 10 行，故「不含①②」不能确认。
  3. **统计口径差异登记**：复核席给出 54／101／371，本次以 `git grep` 测得 35／70／187（行）或 36／76／296（出现次数）。差异原因未查明，本仓以可复现命令测得值为准，复核席口径待对齐。
  4. **授权登记**：新增 `review/approvals/20261121-authorizations.md`，只登记实际发生的两次人类授权（安全审核条款批准；历史重写与 force push 授权），逐字引用原话，并写明**性质限定**：属会话内授权的转述与留痕、自述式登记，不是仓外签署、不是独立外部证据，真实性只能由人类本人在仓外确认；不得据其声称任何审批已取得「外部证据」。
  5. **判定与残余风险（如实登记，不作「可推送」结论）**：本集**不满足「零命中」**。0027 段落的绝对路径已在就地整改中删除；`origin/main` 已公开的历史文档含 73 处真实本机绝对路径；`run-log.md` 含 10 处；远端旧对象仍可按旧 SHA 取回（实测 `HTTP 200`，含已删笔记文件），全历史仍 7 处提及该笔记文件名；彻底清除需 GitHub Support 强制 GC。是否再改写历史、是否轮换凭据，均待人类裁定。
  6. **可选小项**：0027 对照表的 tag 行补充说明——`3311657` 是 **annotated tag 对象** SHA，peel 后指向提交 `7b3f1d5d9d1b215cabd4d9b5a21308032aee6a6d`（只追加，不改 0027）；`SECURITY-CHECKLIST.md` 末尾补换行符。
  7. **就地整改依据与范围**：0027 段落原登记了本机绝对路径，属未推送批次；按 0017 例外规则（未推送批次在推送前可合并整改）就地脱敏，不以「追加更正」代替删除。除该句外 0027 其余内容与语义未变。
- **未改动**：`0014`–`0026` 原文逐字未动（`0027` 仅按 0017 例外就地脱敏一句，见第 7 条）；`dist/`、母本、`SKILL.md`、18 张卡、`validators/`、`AGENTS.MD`；未重打包、不打标签、不推送。
- **关联 ADR**：无
- **备注**：本批次为整改登记，**不是**安全审核通过结论；审核由执行席自审，不是独立复核。不得据本批次声称任何提交「已通过安全审核」「已清除」或「泄露已收回」。全部结论为待验主张，待独立复核席复核与人类裁定。

## 批次 0029 — 2026-11-21

- **批次号**：0029
- **日期**：2026-11-21
- **事项**：待推送集的第二轮安全整改登记：① 全部可达提交与附注 tag 的作者身份统一；② 13 个 tag 重指；③ 0027 第 547 行失实陈述就地订正（0017 例外）。
- **涉及文件**：
  - 修改：`CHANGELOG.md`（第 547 行订正；本批次，仅追加）
- **变更摘要**：
  1. **作者身份统一**：423 条可达提交的 `author` 与 `committer`，以及 3 个附注 tag 的 `tagger`，统一为 `onlookor <onlookor@users.noreply.github.com>`。原有作者/提交时间与**时区偏移**逐条保留；拓扑、父链、树内容、提交信息正文逐字节不变。该等价**仅在身份重写轮内**（`731b3272` → `05109910`）成立；相对重写前 `6c9695e`，树与提交信息含脱敏替换。共改写身份行 846 条、tagger 行 3 条。
  2. **tag 重指**：13 个 tag 全部重指到身份重写后的对应提交；轻量/附注类型不变，附注 tag 的 tag 名与注解正文保留。
  3. **第 547 行订正**：0027「残余风险」第 3 条原称提交主题逐字保留了该文件名，与重写后事实不符，已就地订正为「该文件名已在本次重写中从提交信息移除，旧主张作废」。依据 0017 例外规则（未推送批次在推送前可就地整改）。
  4. **旧 SHA 指针保留**：0027 第 524／543／545 行的旧 SHA 指针本身按人类裁定原文保留；对应行内的笔记名已随脱敏替换，并非「整行未动」。本批不改动旧 SHA 指针。
  5. **新 tip**：身份重写与 tag 重指后为 `0510991`；本批自身提交使 tip 再前进一条，最终 tip 由执行报告与推送前审核记录登记（提交正文无法自指自身 SHA）。
- **验证（待验主张，执行席自测）**：423 对提交逐一比对，树 SHA 相同、提交信息逐字节相同、父链映射一致、时间与时区一致，差异仅出现在 `author`／`committer` 两行；13 个 tag 类型与注解正文不变、指向映射后提交；`git fsck` 无报错。
- **未改动**：`dist/`、母本、`SKILL.md`、18 张卡、`validators/`、`AGENTS.MD`；未重打包；未推送、未建新标签；未改 0027 第 524／543／545 行的旧 SHA 指针（行内笔记名已随脱敏替换）及 0028 正文。
- **关联 ADR**：无
- **备注**：本批为整改登记，**不是**安全审核或独立复核结论，不声称任何提交「已通过」。作者身份统一不改变历史事实与责任归属；全部结论为待验主张。

## 批次 0030 — 2026-11-21

- **批次号**：0030
- **日期**：2026-11-21
- **事项**：独立复核结论的落实登记：① 更新 0.9.0 归档条目的 `source_commit`；② 订正 0029 两处表述；③ 新增授权登记 A-003。
- **涉及文件**：
  - 修改：`registry/release_manifest.yaml`（0.9.0 条目 `source_commit` 与 `note`）
  - 修改：`CHANGELOG.md`（0029 两处表述；本批次追加）
  - 新增：`review/approvals/20261121-authorizations.md` 中的 A-003
- **变更摘要**：
  1. **`source_commit` 更新**：0.9.0 条目改记为当前新历史的对应提交 `a2e18613`。核验依据：该提交主题与旧记录唯一对应；`skills/` 子树零差异，包内 SKILL.md／README.md／PACKAGING.md／BACKFLOW.md 等包装物 blob 逐字节相同；归档未重打包，`sha256`／`bytes`／`build_time` 保持不变。
  2. **0029 表述订正（两处）**：① 为「树内容、提交信息正文逐字节不变」加限定，说明该等价仅在第二轮身份重写范围内成立，相对首轮脱敏前的历史，树与提交信息含脱敏替换；② 将「第 524／543／545 行原文保留、本批不改」改为「旧 SHA 指针本身原样保留，但行内笔记名已随脱敏替换」，并在「未改动」条目同步。依据 0017 例外规则（未推送批次可就地整改）。
  3. **授权登记 A-003**：新增于 `review/approvals/20261121-authorizations.md`，逐字引用两条人类原话，登记两轮实际动作范围，并把 `source_commit` 更新列为随附整改；明确 force push `main` 与 13 个 tag 的推送授权尚未取得，本登记不覆盖该动作。
- **验证（待验主张，执行席自测）**：`source_commit` 指向的提交在 `main` 祖先链上；`skills/` 包装物与旧记录逐字节相同；新历史对脱敏清单零命中；`git fsck` 无报错。
- **未改动**：`dist/`、母本、`SKILL.md`、18 张卡、`validators/`、`AGENTS.MD`；未重打包；未推送、未动远端、未建新标签。
- **关联 ADR**：无
- **备注**：本批为整改登记，**不是**安全审核或独立复核结论；A-003 为会话内授权的自述式留痕，不是仓外签署、不是独立外部证据；全部结论为待验主张。

## 批次 0031 — 2026-11-21

- **批次号**：0031
- **日期**：2026-11-21
- **事项**：登记 A-004 强推授权及本次推送范围。
- **涉及文件**：
  - 修改：`review/approvals/20261121-authorizations.md`（新增 A-004，文末性质限定同步）
  - 修改：`CHANGELOG.md`（本批次追加）
- **变更摘要**：
  1. **授权登记 A-004**：force push `main` 与 13 个 tag，以重写后的历史替换远端历史；原话逐字引用「可以执行。」。
  2. **推送范围**：仅 `refs/heads/main` 与 13 个 `refs/tags/*`（名称、类型不变）；不含对远端做 GC、不含轮换凭据、不含 GitHub 侧悬空对象清除。
- **验证（待验主张）**：推送前以 `git for-each-ref` 确认本地仅有 `main` 与 13 个 tag，无超出范围的 ref；`main` 用 `--force-with-lease`（租约取推送前实测 `origin/main`），tag 逐个显式 refspec force 更新；推后以 `git ls-remote` 逐一比对并核对 ref 总数。
- **未改动**：`dist/`、母本、`SKILL.md`、18 张卡、`validators/`、`AGENTS.MD`；未重打包；未建新 tag；未对远端做 GC；未轮换凭据。
- **关联 ADR**：无
- **备注**：本批只登记授权与推送范围，**不是**安全审核或独立复核结论；A-004 为会话内授权的自述式留痕，不是仓外签署、不是独立外部证据；全部结论为待验主张。
