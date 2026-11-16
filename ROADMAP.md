# ROADMAP：计划与验收

> 本文件是**计划与验收的唯一登记处**（schedule 纪律见 [AGENTS.MD](AGENTS.MD) 第 3 条）。
> 不登记：单点工作项状态（归 `todo.md`）、文件当前状态（归 `STATE.md`）、已发生的变更（归 `CHANGELOG.md`）。
> 每个里程碑的出口条件必须能由**命令、文件或计数**核对；关闭里程碑须附出口证据。
> 里程碑的运行状态不在本文件维护：它由 `todo.md` 顶部状态块的「阶段」字段承载，由 `registry/scripts/project.py` 从事实生成。本文件只定义「做到什么算完」。

## 一、阶段释义（A–D：接地编译流程）

以下四个阶段描述「把成文法编译成某部署可执行、可验证产物」的端到端流程。判定权威是母本 10.2.5 六判据。

| 阶段 | 指什么工作 | 判据 | 产物 |
|---|---|---|---|
| **A 编译准备** | 读目录文档、确认本地参考资源在位；按《部署规模裁剪模板》对档；建立五注册表接地最小集 | 资源缺失即暂停；五注册表非空；档位与 `pact/se_tier{1,2,3}_*.pact` 对应 | 五注册表最小集、档位结构位基线 |
| **B 种子引导** | 按成文法 0.17.6 人工种子通道整理方法注册表初始条目；E3 bootstrap 豁免按 Waiver 登记；LRM＝编译器首次成功运行 | 四层来源逐条标注；未标 `compile_usage` 的文献不得填充字段；条目先入 `seed`，编译器就绪后逐条重验证 | 种子条目（`seed`）、Waiver 登记 |
| **C 编译执行** | 按《编译规范》第五章执行编译：源锚定 → 参考资料映射 → 产物生成；忠实性检查与 FVR 接线；多 Agent 前置门 #9 | 第六章三判据；失败按第九章 FM 目录归类；首个多写入方部署决策前补齐 11.4 并发协议 | 编译产物（artifact 标签）、忠实性检查、FVR 接线 |
| **D 接地验收与运行** | 按 10.2.5 六判据验收；真实项目试点（`todo.md` 3.5）；通道终止（首次成功编译通过对齐验证＝LRM） | 10.2.5 六判据全过；试点收集忠实性缺陷与卡片可用性问题；能力缺口不得豁免硬性质 | 10.2.5 判定、试点记录 |

**与后来三件事的关系**：

- **接地编译（母本／判据／`.10`–`.14` 重编译链）**：A–D 就是这条链本身。`.10`–`.14` 是 C 阶段的产物标签，10.2.5 是 D 阶段的验收判据。
- **技能层（开发侧／部署侧／回流三层）**：不是 A–D 的下一阶段，而是把「人能执行的编译流程」压缩成「agent 可执行的技能包」的**并行线**，记为 M4。它消费 A–D 的产物与判据，但不以 D 关闭为前提。
- **分发件**：把技能包变成可下载、可校验、可安装的归档，也是**并行线**，记为 M5；出口只由分发件自身的事实决定。

## 二、里程碑 M0–M7

| 里程碑 | 对应 | 出口条件（可核对） | 产出 | 前置依赖 | 与既有排期项的关系 |
|---|---|---|---|---|---|
| **M0** | 阶段 A | `registry/profiles.yaml`、`method_registry.yaml`、`guard_registry.yaml`、`fvr_registry.yaml`、`projection_registry.yaml` 五文件存在；`pact/` 至少 3 个 `se_tier*_*.pact` | 五注册表最小集、档位结构位基线 | 无 | `todo.md` 3.10 |
| **M1** | 阶段 B | `registry/method_registry.yaml` 的 `meta.entry_count` ≥ 1；`pilot/vertical-slice-20261112/artifact.yaml` 的 `compilation_artifact.version.label` 非空（LRM 已越） | 种子条目、Waiver 登记 | M0 | `todo.md` 3.8 |
| **M2** | 阶段 C | `artifact.yaml` 的 `compilation_artifact.version.label` 非空；`编译规范.md` 正文在位 | 编译产物、忠实性检查、FVR 接线 | M1 | `todo.md` 3.1／3.2／3.3／3.4／3.6／3.7／3.9 |
| **M3** | 阶段 D | `pilot/vertical-slice-20261112/10.2.5-verdict-pact-dsh.yaml` 的 `grounding_acceptance.summary.pass = 6` 且 `fail = 0`；`todo.md` 3.5／3.8 关闭 | 10.2.5 判定、试点记录 | M2 | `todo.md` 3.5 |
| **M4** | 技能层（开发侧／部署侧／回流三层） | `skills/software-engineering/validators/validate.py` 提供 V01–V08 可执行检查；`skills/software-engineering/tests/negative/run_negative.py` 全部用例拦截；包内示例 `examples/defect-repro-fix/run.py` 退出 0 | 技能包（`SKILL.md`、`stages/`、`schemas/`、`validators/`、`examples/`）、回流说明 | 与 M3 **并行**，不以其关闭为前提 | 新增里程碑；不并入 C／D 出口 |
| **M5** | 分发件 | `python3 skills/software-engineering/scripts/build_package.py` 退出 0；`dist/software-engineering-<version>.tar.gz` 与 `.sha256` 存在；解包后包内示例退出 0 | 归档、摘要、随包 README／PACKAGING | 与 M3 **并行**；出口**不绑定** M6 批准或第三轮复核 | 新增里程碑；不并入 C／D 出口 |
| **M6** | 独立复核制度 | `独立复核规程.md` 经人类批准；`review/` 下的复核记录与批次对应 | 复核规程、复核记录 | 人类批准；与 M3／M4／M5 并行 | 新增里程碑；复核制度批准状态归本项，不串入 M5 |
| **M7** | 发布点 | annotated tag 指向 `HEAD`，且 tag 名为 `release-*` 或 `vX.Y.Z`；未满足时不打标签 | annotated tag、发布说明 | M3–M6 各自出口；由人类决定是否打标签 | 发布动作 |

**并行关系（人类裁定，2026-11-16）**：M4、M5 是与 M3 并行的独立线，不因 M3 未闭合而阻塞；M4、M5 是新增里程碑，不并入 C／D 的出口；M5 的关闭条件不绑定「人类批准复核制度」和「第三轮复核通过」。

## 三、现状与冲突（原样登记，不改写阶段语义）

1. 根 `README.md` 原 §5「阶段 B：种子引导（单 Agent/人工种子阶段，**当前所处阶段**）」与事实不符：`artifact.yaml` 已到 `pilot-20261112.14`，10.2.5 判定文件为 `pass 6 / fail 0`，LRM 已越过。**人类裁定（2026-11-16）**：该「当前所处阶段」判为**过时**，改写为「已越过 LRM、待补阶段记录」。这是语义变更，不是笔误修正或文字澄清。
2. 根 `README.md` 原 §6「状态、计数与版本不在本文件维护：以 `todo.md` 顶部「当前状态」块为准」在 2026-11-16 之前不成立：`todo.md` 的状态块没有阶段字段。现已补入「阶段」字段并由 `project.py` 生成，本文件与 `todo.md` 的分工才成立。
3. `todo.md` 3.5 的进展段写「10.2.5 一过五 fail」（首次纵向切片，2026-11-12），而 `10.2.5-verdict-pact-dsh.yaml` 当前 `summary` 为 `pass 6 / fail 0`（2026-11-15，artifact `.14`）。两处读数属于不同时点，**未在此处裁定哪个代表「当前」**；阶段字段只显示判定文件的事实读数 `6/6`。
4. `todo.md` 状态块（2026-11-16 之前）记 `tag 12 个`（截至 `layer-close-20261111`），`git tag -l` 实为 13 个（多 `layer-skill-narrow-20261116`）。状态块由 `project.py --project` 按事实重写后以事实为准。
5. `编译规范.md` 文件头原有一句「当前状态：第一～十章、第十二～十三章已定稿……唯一未闭合项＝#9 并发协议」。该「当前状态」与 `todo.md` 3.7 的缺口登记是两份状态来源；已按 A 类文档同步要求删去文件头状态，只留指向 `todo.md` 3.7 的登记指针。
6. 根 `README.md` 原 §5 同时把「LRM＝编译器首次成功运行」写在阶段 B，又在阶段 D 第 11 条写「第一次成功编译通过对齐验证＝人工种子通道 LRM」。两处措辞不完全一致（「首次运行」vs「通过对齐验证」）；此处原样登记，不改写。

## 四、关闭纪律

- 关闭里程碑须附出口证据：命令与结论、文件路径或计数。
- 里程碑增删与顺序变更追加 `CHANGELOG.md` 后生效；里程碑内部的进度更新不记 `CHANGELOG.md`。
- 不得静默删除里程碑；取消的里程碑标 `dropped` 并写明理由。
- 本文件不承载版本号；发布点以 annotated tag 为准。
