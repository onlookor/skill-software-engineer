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
