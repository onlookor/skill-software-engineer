# ADR 索引

> 本目录收纳全部架构决策记录（ADR）。**本文件是收纳之后唯一需要人工维护的清单**：新增／变更状态／取代关系时逐条登记，其余字段随 ADR 正文走。
> 历史文档中的旧路径引用按 0.22 保持 as-of，其映射见 §4。

## 1. 位置与命名规约

**位置＝仓库根目录 `adr/`。** 理由：ADR 同时约束母本条款与 `registry/` 实现，服务对象跨两者；`adr/` 与 `软件工程元框架成文法.md`、`registry/` 平级，正确表达「跨域治理记录」的位阶。`registry/adr/` 会把 ADR 错误限定为注册表专属（如 ADR-M5-01 改的是母本条款，与注册表数据无关）；`docs/adr/` 需新引入本仓库不存在的 `docs/` 层级，与现有扁平布局不一致。

**文件名＝`{ADR 编号}-{状态}-{YYYYMMDD}-{短标题}.md`。**

| 段 | 取值 |
|---|---|
| ADR 编号 | **原编号逐字保留，作为主键**（`ADR-README-01`、`ADR-LC-01`、`ADR-R2-APPL-01`…）。不重排全序：重排会使已推送历史、changelog、台账 evidence、其他会话记录中的编号集体失效，且 13 份 ADR 的编号已带领域前缀（`LC`/`R2-APPL`/`README`/`SRC`/`VG09`/`STY-FIM`/`M5`），已有可读语义 |
| 状态 | `draft`（草案）／`approved`（已批准）／`rejected`（已否决）／`superseded`（已取代） |
| 日期 | 批准日期（draft 则为起草日期），`YYYYMMDD` |
| 短标题 | 去标点、不加空格的中文短语；与 H1 标题可不逐字相同 |

**候选方案对比**（择一已采纳，其余记录理由）：

| 方案 | 形态 | 取舍 |
|---|---|---|
| **A（采纳）** | `{原编号}-{状态}-{日期}-{短标题}.md` | 编号即主键；状态与日期可排序可检索；不破坏任何既有引用 |
| B | `ADR-{000}-{状态}-{日期}-{短标题}.md`（全局重排） | 序号连续好看，但全量重排编号＝全仓引用与历史记录失效，违反 0.22 编号不复用／锚点纪律 |
| C | `{日期}-{原编号}-{状态}-{短标题}.md`（日期前置） | 便于按时间浏览，但按编号检索退化，且与现有 `ADR-*` 前缀惯例断裂 |

**状态 token 的判定来源**：以 ADR 正文的批准记录／changelog 批次／台账 `closure.ruled_by` 为准；三者矛盾时以台账与 changelog 的执行证据为准，并在 §3 记明。

## 2. 索引

| 编号 | 标题 | 状态 | 批准日期 | 被取代 | 影响的母本条款／注册表区段 | 文件 |
|---|---|---|---|---|---|---|
| `ADR-INLINE-MARK-01` | T2 五项行内标记方案（VFM／CFG／SCH／RLP／STY-4） | approved | 2026-11-04 | — | 母本 1.5(@1467)／5.2.3(@2479)／5.2.4(@2485)／5.2.6(@2507-2510)／5.5(@2574)／8.2.1(@3322)；`project.py` row_id 解析与 META；gaps `G-VFM-1`／`G-CFG-1`／`G-SCH-1`／`G-RLP-1`／`G-STY-4` | `ADR-INLINE-MARK-01-approved-20261104-五项行内标记方案.md` |
| `ADR-STY-FIM-01` | 框架内生元方法与 `provenance.source_class` | approved | 2026-11-07 | — | 母本 0.12／0.13／0.17.2（@335 `source_class`、@462 `origin`）／0.17.6／0.22；`project.py` `ENUM_ORIGIN` 与 `source_class` 校验；条目 `STY-021`／`STY-024`；gaps `G-STY-5`／`G-GOV-2`；SO-3／SO-24 | `ADR-STY-FIM-01-approved-20261107-框架内生元方法与source_class.md` |
| `ADR-VG09-01` | 母本谓词表一次性扩容（VG-09 十七名） | approved | 2026-11-06 | — | 母本 9.5 谓词表；`registry/predicate_vocabulary.yaml` `VOCAB`；gap `VG-09`（另记 `cycle_scale` 残余） | `ADR-VG09-01-approved-20261106-谓词表一次性扩容.md` |
| `ADR-VGEX-01` | VG-01～VG-08 谓词表扩容（20 名入表） | approved | 2026-11-07 | — | 母本 5.5(@2579)／8.5(@3435)／9.5(@3711)；`registry/predicate_vocabulary.yaml` 20 名与 VG-01～08 resolution；`node_role` 后置 | `ADR-VGEX-01-approved-20261107-VG01-08谓词表扩容.md` |
| `ADR-G-OWN-CSL-01` | G-OWN-1／G-CSL-1 行内出处补写（零插行母本改写） | approved | 2026-11-04 | — | 母本 4.2.1(@2166-2171)／4.2.3(@2186-2194)／4.7(@2431/@2432/@2435)；gaps `G-OWN-1`／`G-CSL-1` | `ADR-G-OWN-CSL-01-approved-20261104-行内出处补写.md` |
| `ADR-G-PRJ-1-01` | G-PRJ-1 有意保留悬空 | approved | 2026-11-06 | — | 台账 gap `G-PRJ-1`（保留理由与关闭条件）；`project.py` `GAP_SO_WHITELIST` | `ADR-G-PRJ-1-01-approved-20261106-有意保留悬空.md` |
| `ADR-KP-G3-01` | GRD／PRJ／GOV 三 kind 剖面变更（KP-G3 的 R2 落地） | approved | 2026-11-03 | — | 母本 0.17.2 @387 末句；`registry/profiles.yaml` `GRD`／`PRJ`／`GOV` 三剖面；`project.py` C-ENV 读 `entry_level_exemptions`；gap `KP-G3` | `ADR-KP-G3-01-approved-20261103-GRD-PRJ-GOV剖面变更.md` |
| `ADR-G-STY-ENV-01` | 接地编译前两闸（G-STY-1 三空间条件／G-ENV-1 指标映射） | approved | 2026-11-04 | — | 母本 1.2.1–1.2.4／1.3／6.2.1；0.18.2 S1；0.18.6 M15；0.17.7 门槛 2；gaps `G-STY-1`／`G-ENV-1`；SO-1 | `ADR-G-STY-ENV-01-approved-20261104-接地编译前置两闸.md` |
| `ADR-PRJ-2-01` | PRJ 交付空间谓词槽纠正（G-PRJ-2） | approved | 2026-11-04 | — | 母本 0.17.2 @342；10.2.2；`method_registry.yaml` 条目 `PRJ-001…PRJ-011`；gap `G-PRJ-2` | `ADR-PRJ-2-01-approved-20261104-PRJ交付空间谓词槽纠正.md` |
| `ADR-SRC-01` | 方案③：以 SRC kind 承载 9.2.3 九信号源 | draft | 2026-11-05（起草；方向 R1.0–R1.7 已批准） | — | 母本 0.17.3 kind 表（SRC 行，I-A）／0.17.4（I-B）／9.2.3；0.18.2 S1；`registry/profiles.yaml` SRC 剖面；gap `G-GRD-1`／SO-17 | `ADR-SRC-01-draft-20261105-9.2.3九信号源方案③.md` |
| `ADR-SRC-02` | 方案 A：0.17.2 增 `signals` 字段 | approved | 2026-11-06 | — | 母本 0.17.2 `signals`；`registry/profiles.yaml` 全 18 剖面；条目 `SRC-001…SRC-008`；gaps `G-GRD-1`（closed）／`G-SRC-1`（open） | `ADR-SRC-02-approved-20261106-signals字段方案A.md` |
| `ADR-LC-01` | 0.17.5 增补 `seed→draft` 迁移权限 | approved | 2026-11-07 | — | 母本 0.17.5 L451（已增补 `seed→draft`，同行）；总纲单行本同步；0.17.6／0.17.7／0.17.8 M5／9.2.1；`registry/CHECK-SPEC.md` C1 C-ST 行（§2.5 回落依据）；`method_registry.yaml` `status_transitions` 迁移记录 schema；`project.py` `check_ledgers`／`check_cst` | `ADR-LC-01-approved-20261107-seed到draft迁移权限.md` |
| `ADR-R2-APPL-01` | applicability 项级事实槽与问句式判据 | approved | 2026-11-06 | — | 母本 0.17.2 `applicability_item`（+5 行）；`project.py` `check_r2_applicability`；`profiles.yaml` 开关；130 条 `problem_space` | `ADR-R2-APPL-01-approved-20261106-applicability事实槽.md` |
| `ADR-README-01` | 子目录自检矩阵的授权边界与 README §5 公式拆解 | approved | 2026-11-07 | — | `registry/README.md` §5（迁入 `registry/CHECK-SPEC.md` C1）；`project.py` `check_m2`／`check_cenv`／`check_cst`／`SEED_CHECKS`；母本配套文件说明表 L21；`AGENTS.MD` L15 | `ADR-README-01-approved-20261107-子目录自检矩阵授权边界.md` |
| `ADR-M5-01` | M5（`narrative_sync`）软硬冲突裁决 | approved | 2026-11-07 | — | 母本 0.17.8 L500 行内追加（同行）；总纲单行本 L475 同步；`CHECK-SPEC` C1 M5 行；`ST-STY-01.condition`；`project.py` `check_m5`／`SEED_CHECKS` | `ADR-M5-01-approved-20261107-M5软硬冲突裁决.md` |
| `ADR-GAP-01` | 登记面下探与 gap 闭合规则（三态） | approved | 2026-11-07 | — | 0.12／0.17.7 门槛 6／0.17.8 M6；`ADR-STY-FIM-01` §5.5；gaps `G-CRD-1`／`G-DEC-1`／`G-CTR-1`／`G-STP-1`／`G-DFL-1`（均 closed）；SO-7～SO-11（均 closed） | `ADR-GAP-01-approved-20261107-登记面下探与gap闭合规则.md` |
| `ADR-STY-3-01` | `G-STY-3`／STY-012 的 MVC 行级外部出处补登记 | approved | 2026-11-07 | — | 母本 0.12 @11／@1869（编号 81、增补区 10.8）；书目 81；`method_registry.yaml` `STY-012`；gap `G-STY-3`；SO-3 | `ADR-STY-3-01-approved-20261107-MVC行级外部出处补登记.md` |
| `ADR-VG03-NR-01` | 节点角色谓词单族扩容（`node_role`，1 名） | approved | 2026-11-07 | — | 母本 1.5 @1479（+2 行，4,461→4,463；闭合围栏 @1480）；`registry/predicate_vocabulary.yaml` `node_role`（arity 2）与 VG-03 resolution；`method_registry.yaml` `STY-019-AP1` 改写（1 方括号）／SO-4 未闭合项 6→4 | `ADR-VG03-NR-01-approved-20261107-节点角色谓词单族扩容.md` |
| `ADR-VG02VG04-01` | VG-02／VG-04 残余四词裁决（R0 零母本改动） | approved | 2026-11-07 | — | 母本 **0 行**（载体 1.2.1 行 1348／2.2.3 行 1638／2.5 行 1724、行 1729／3.2.1 行 1929）；`registry/predicate_vocabulary.yaml` `schema`／`error_handling`（`kind: term`，arity 1）与 VG-02／VG-04 resolution；`method_registry.yaml` `STY-016-AP2`／`STY-011-AP1`／`STY-013-AP2` 改写（共 4 方括号）；SO-4 未闭合项 4→0 | `ADR-VG02VG04-01-approved-20261107-VG02-VG04残余词条款补写评估.md` |
| `ADR-STY015-P0-01` | V1 严格逐字读收口与 `STY-015-AP1` 升 P0 | approved | 2026-11-08 | — | 母本 9.2.1（第 3600 行，**0 行增减**，围栏 216 不变）／1.5 第 1474 行三族、第 1485 行 V1；`method_registry.yaml` `STY-015-AP1`（P1→P0）／`MJ-4` P0 判据／`G-STY-4` `correction_2026_11_08`／`SO-4` `decision_basis`；`registry/CHECK-SPEC.md` C2.4／C5.17／C6.3 | `ADR-STY015-P0-01-approved-20261108-V1严格逐字读与STY-015-AP1升P0.md` |

**统计**：20 份；approved 19、draft 1（`ADR-SRC-01`）；无 rejected、无 superseded。

## 3. 状态存疑项（正文头部与执行证据不一致，已按证据裁定）

| 编号 | 正文头部写法 | 执行证据 | 裁定 |
|---|---|---|---|
| `ADR-G-OWN-CSL-01` | 「方向已获批准…落盘后执行」 | §5 记批准；changelog 2026-11-04 记执行；gaps `G-OWN-1`／`G-CSL-1` 已 closed | approved（2026-11-04） |
| `ADR-PRJ-2-01` | 「草案；条目未改写」 | changelog §4.18 记「人类批准…执行清单…本轮只改 method_registry.yaml」；gap `G-PRJ-2` 已 closed | approved（2026-11-04）；头部为执行前遗留 |
| `ADR-SRC-01` | 「草案；R1.0–R1.7 方向已批准；仍未落盘」 | 方向已批准；I-A（kind 行）／I-B 两行已落盘；其余待续 | **维持 draft**：文档未转 approved，批准仅及于方向 |
| `ADR-SRC-02` | 「草案；2026-11-06 已获人类责任方批准」 | §11 记批准并执行；`SRC-001…008` 已落地 | approved（2026-11-06） |

> 以上头部文本按 0.22 不改写；本表为状态权威读法。若将来统一正文头部，须另立变更批次。

## 4. 旧路径 → 现路径映射

迁移前的文件名（根目录平铺）与现名对照。历史文档（changelog、`todo.md`、`R2提案-*`、`adr/` 内 FROZEN 文件的 as-of 引用）保留旧名，按本表解析。

| 旧文件名 | 现文件名 |
|---|---|
| `ADR草案-行内标记方案-五项gap.md` | `ADR-INLINE-MARK-01-approved-20261104-五项行内标记方案.md` |
| `ADR草案-框架内生元方法-STY-021-024.md` | `ADR-STY-FIM-01-approved-20261107-框架内生元方法与source_class.md` |
| `ADR草案-谓词表一次性扩容-VG-09.md` | `ADR-VG09-01-approved-20261106-谓词表一次性扩容.md` |
| `ADR草案-G-OWN-CSL-行内出处.md` | `ADR-G-OWN-CSL-01-approved-20261104-行内出处补写.md` |
| `ADR草案-G-PRJ-1-悬空保留.md` | `ADR-G-PRJ-1-01-approved-20261106-有意保留悬空.md` |
| `ADR草案-GRD-PRJ-GOV-剖面变更.md` | `ADR-KP-G3-01-approved-20261103-GRD-PRJ-GOV剖面变更.md` |
| `ADR草案-G-STY-1-G-ENV-1-接地编译前置.md` | `ADR-G-STY-ENV-01-approved-20261104-接地编译前置两闸.md` |
| `ADR草案-PRJ交付空间-谓词槽纠正.md` | `ADR-PRJ-2-01-approved-20261104-PRJ交付空间谓词槽纠正.md` |
| `ADR草案-SRC-9.2.3九信号源-方案③.md` | `ADR-SRC-01-draft-20261105-9.2.3九信号源方案③.md` |
| `ADR草案-SRC-signals字段-方案A.md` | `ADR-SRC-02-approved-20261106-signals字段方案A.md` |
| `ADR-LC-01-seed到draft迁移权限.md` | `ADR-LC-01-approved-20261107-seed到draft迁移权限.md` |
| `ADR-R2-APPL-01-applicability事实槽.md` | `ADR-R2-APPL-01-approved-20261106-applicability事实槽.md` |
| `ADR-README-01-子目录自检矩阵授权边界.md` | `ADR-README-01-approved-20261107-子目录自检矩阵授权边界.md` |
| `ADR-GAP-01-draft-20261107-登记面下探与gap闭合规则.md` | `ADR-GAP-01-approved-20261107-登记面下探与gap闭合规则.md` |
| `决策建议-M5-软硬冲突-2026-11-07.md` | `ADR-M5-01-approved-20261107-M5软硬冲突裁决.md`（原件已删除） |

## 5. 维护规则

1. **新增 ADR**：按 §1 命名，登记 §2 一行；若取代既有 ADR，被取代者文件名状态改为 `superseded` 并在其「被取代」列填后继编号。
2. **状态变更**：改文件名状态 token ＋ 改本表状态列；`draft` → `approved` 必须有批准记录（changelog 或台账 `closure.ruled_by`）。
3. **编号不复用**（0.22）：废弃编号永久保留于本表，不得回收。
4. 本文件是索引，不是规约；ADR 的效力以各自正文为准。
