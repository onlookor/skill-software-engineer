# STATE：文件当前状态

> 本文件只登记**文件／目录的当前状态**（schedule 纪律见 [AGENTS.MD](AGENTS.MD) 第 3 条）。
> 不登记：里程碑与出口条件（归 `ROADMAP.md`）、单点工作项状态（归 `todo.md`）、已发生的变更（归 `CHANGELOG.md`）。
> 新增、删除或状态变化时由任何执行者更新，不需 ADR。

状态取值：`active`（在用，可维护）｜`generated`（生成物，不得手改）｜`append-only`（只追加，不改写）｜`internal`（仓内使用，不随包分发）｜`draft`（草案，待批准）｜`archived`（归档，只读）｜`ignored`（不入库）。

| 路径 | 状态 | 说明 | 维护责任 |
|---|---|---|---|
| `软件工程元框架成文法.md` | active | 母本；条款与判据权威 | 人类责任方（ADR） |
| `软件工程元框架成文法-changlog.md` | append-only | 母本语义裁决与批次登记 | 任何执行者 |
| `编译规范.md` | active | 编译源 → 产物的映射规程；状态不在文件头维护，缺口见 `todo.md` 3.7 | 人类责任方（E7 修订权） |
| `编译规范-changlog.md` | append-only | 编译规范批次登记 | 任何执行者 |
| `README.md` | active | 目录导览、文件依赖、阶段释义指针 | 交付方 |
| `AGENTS.MD` | active | 执行约定、目录结构权威、schedule 纪律 | 交付方 |
| `ROADMAP.md` | active | 计划与验收唯一登记处（M0–M7） | 交付方 |
| `todo.md` | active | 单点工作项台账；顶部状态块由 `project.py` 生成 | 任何执行者 |
| `CHANGELOG.md` | append-only | 变更历史唯一登记处 | 任何执行者 |
| `STATE.md` | active | 本文件：文件当前状态 | 任何执行者 |
| `独立复核规程.md` | draft | 独立复核制度；**草案，待人类批准后生效** | 人类批准人 |
| `adr/` | active | 同时约束母本与 `registry/` 的架构决策记录 | 任何执行者 |
| `registry/` | active | 方法注册表机器层权威源（YAML）；矛盾时以 YAML 为准 | 交付方 |
| `registry/projections/` | generated | `registry/scripts/project.py` 生成的人类可读投影，**不得手改** | 生成物 |
| `registry/scripts/` | internal | 自检、投影与状态块生成脚本 | 交付方 |
| `pilot/` | internal | 纵向切片试点与 10.2.5 判定记录；不随包分发 | 交付方 |
| `pact/` | active | 形式层结构位（`.pact`），母本的下游投影 | 交付方 |
| `archieve/` | archived | 历轮讨论记录，只读 | 只读 |
| `skills/software-engineering/` | active | 技能包源（`SKILL.md`、`stages/`、`schemas/`、`validators/`、`examples/`、内部 `tests/`、`scripts/`） | 交付方 |
| `dist/` | generated | 打包产物（目录、`.tar.gz`、`.sha256`）；由 `build_package.py` 生成，不手工放入 | 生成物 |
| `review/` | internal | 独立复核记录；**当前未启用**（尚无复核记录），不随包发布 | 复核者／执行者 |
| `resources/` | ignored | 本地参考资料，不入库（`.gitignore`） | 只读 |

**边界**：本文件不判断文件内容是否正确，只登记状态；内容冲突由 `CHANGELOG.md` 的批次与 `todo.md` 的条目承载。
