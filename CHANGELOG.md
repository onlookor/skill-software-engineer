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
