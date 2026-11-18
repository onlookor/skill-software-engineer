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
