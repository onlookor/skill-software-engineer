# E3 Waiver 内容草案（PRJ／GOV／GRD 三份）

| 项 | 值 |
|---|---|
| 状态 | **draft（仅内容草案；未获批准、未写入 `method_registry.yaml`）** |
| 日期 | 2026-11-06 |
| 性质 | 9.2.2 五要素的备材；批准与否由人类裁决（0.10 第一条） |
| 依据 | E3（母本 10.5，FVR 全覆盖 —— 硬）；0.17.6(2) 制度性豁免通道；G1（P0 即时阻塞 —— 硬）；G5（豁免不静默展期 —— 硬）；`WV-STY-E3-01` 已裁定的边界结论（制度性豁免 ≠ 裁量豁免，`external_cause: false` 不构成驳回理由）；防扩宽条款 (ii)「各 kind 各自单独申请」 |
| 未动项 | `method_registry.yaml` 的 `waivers` 段零改动；`G-GOV-1`／`SO-19` 零改动；母本零改动；条目零改动 |

## 0. 三份的一行转述版（供拍板）

| Waiver | scope 一句 | 闭合条件一句 |
|---|---|---|
| `WV-PRJ-E3-01` | 仅覆盖 PRJ-001…PRJ-011（11 条 seed）`formal_anchor` 引用的 **E1 implements 11 个实例**；不含其它 kind、不含 active 条目、不含 E1 以外的性质。 | 编译器首次成功运行且 E1 已建 FVR 条目、接线完成、`first_full_run` 留证时闭合（事件型，无日历期限）。 |
| `WV-GOV-E3-01` | 仅覆盖 GOV-001…GOV-006（6 条 seed）引用的 **5 项 8 实例**（R7 implements 3／R1 1／R2 implements 1＋triggers 1／R6 1／R8 1）；不含其它 kind、不含 active 条目。 | 同上事件型：R1／R2／R6／R7／R8 五项各建 FVR 条目并接线、首次全量运行留证时闭合。 |
| `WV-GRD-E3-01` | 仅覆盖 GRD-001…GRD-003（3 条 seed）引用的 **G1／G5／G7 各 1 个 implements 实例**（共 3 实例）；**不含** SRC 侧 G1 `triggers` 3 实例（见 §4）。 | 同上事件型：G1／G5／G7 三项建 FVR 条目并接线、首次全量运行留证时闭合。 |

> 三份均 `independent_effect: true`（各自独立生效、独立闭合、互不援引）；均**不**使对应条目的 `seed` 资格以本豁免为前提（C-ST 只查硬检查，E3 属 FVR 接线面，与 `draft→seed` 条件不同轴）。

## 1. `WV-PRJ-E3-01`

```yaml
waiver_id: WV-PRJ-E3-01
rule: 'E3（母本 10.5）：∀ property(hard): ∃ fvr_entry ∧ wired ∧ first_full_run has evidence —— FVR 全覆盖，硬'
violation_fact: >-
  PRJ 批 11 条（PRJ-001…PRJ-011，覆盖 1.4／2.4／4.4／5.4／8.4／9.4 六个评审入口与 8.2.7 的五个评审点）
  经人工种子通道（0.17.6(1)）迁移为 seed；其 formal_anchor 一律为 E1 implements（11 条各 1），
  而 project.py 只做注册表静态自检、不是 FVR 运行器，E1 尚无 FVR 条目与检查程序接线 →
  『引用 seed 条目的性质』不满足 E3 的 existence ∧ wired ∧ first_full_run has evidence。
  合法性出处：0.17.6(2)（母本明文设立 seed 期 E3 豁免通道），并须符合防扩宽条款 (ii) 的单独申请。
scope: >-
  精确范围：method_registry.yaml 中 status=seed 的 PRJ-001…PRJ-011 十一条的 formal_anchor
  所引用的性质实例，共 1 项 11 实例——E1『表达无缺口 —— 硬』implements 11（11 条各 1，YAML 解析逐条统计 property_id×role）。
  不含 active 条目；不含其它 17 个 kind（各由其自身 Waiver 或另批申请承担）；不含 E1 以外的性质
  （E2 同源生成／E3 本体／E4 版本一致／E5 均不在本 Waiver 范围）；不含 PRJ 条目的 applicability／anti_patterns 所引方向性事实。
deadline:
  type: event
  lrm: 编译器首次成功运行（0.17.6(2) 指定的 LRM）
  calendar_date: null
  note: 不虚构日历期限（0.4 禁假精确）；超期按 9.2.2 自动升 P0＋CH-C(2)，延续＝新 Waiver，不许静默展期。
closing_condition: >-
  编译器首次成功运行 ∧ E1 已建 FVR 条目 ∧ 接线完成 ∧ first_full_run 留证 ∧ 逐条 seed→active
  （diff 为空＝低影响简记；diff 非空按 0.17.6(3) 三分类定级）。
remediation_plan: '(1) project.py 自检全过 → (2) 编译器对 seed 条目重验证（人工条目 vs 编译条目，差异按 0.17.6(3) 三分类）→ (3) 为 E1 建 FVR 条目并接线、首次全量运行留证 → (4) 逐条 seed→active。本 Waiver 在 (3) 完成时闭合。'
risk_quantification: >-
  触及面 11 实例。利息形态：E1「表达无缺口」的检出时机由编译期自动检出退化为评审期人工核验，延迟＝一个决策周期；
  漏检后果＝评审点引用的谓词子集无 view_instance 覆盖（表达缺口）进入实现。缓解：(i) 0.17.5 强制 ADR 附注「依据种子条目，待重验证」；
  (ii) PRJ 条目的 anti_patterns 信号级判读带母本指针，可逐条人工复核；(iii) project.py 的 M/M2–M9/C 系列静态自检覆盖可机器判定面。
independent_effect: true
approval:
  category: 批准注册表类目 + 8.2.7 评审点五（例外评审）
  external_cause: false
  status: pending
  note: 本轮只备内容、不写台账；批准后才在 waivers 段追加并写 approved_by／approved_date／ruling。
```

## 2. `WV-GOV-E3-01`

```yaml
waiver_id: WV-GOV-E3-01
rule: 'E3（母本 10.5）：∀ property(hard): ∃ fvr_entry ∧ wired ∧ first_full_run has evidence —— FVR 全覆盖，硬'
violation_fact: >-
  GOV 批 6 条（GOV-001…GOV-006：完整 ADR／接受约束 ADR／张力承认 ADR／保守假设 ADR／权衡承认 ADR／重审提议）
  经人工种子通道迁移为 seed；其 formal_anchor 引用 R 系列五项硬性质（R1／R2／R6／R7／R8），
  其中 GOV-001 同时引 R1 与 R7、GOV-004 引 R2 triggers、GOV-006 同引 R2 implements 与 R8；
  上述性质均无 FVR 条目与接线 → E3 三支一律未满足。合法性出处同上（0.17.6(2)＋防扩宽条款 (ii)）。
scope: >-
  精确范围：status=seed 的 GOV-001…GOV-006 六条的 formal_anchor 所引性质实例，共 5 项 8 实例——
  R7『公理 A2 逐决策执行 —— 硬』implements 3（GOV-001／002／005）；R1『批准闭环、执行者不可自批 —— 硬』implements 1（GOV-001）；
  R2『重审门槛三条件 —— 硬』implements 1（GOV-006）＋triggers 1（GOV-004）；R6『临时决策不得硬化传播 —— 硬』implements 1（GOV-003）；
  R8『重审后的下游血缘逐一目检 —— 硬』implements 1（GOV-006）。
  不含 active 条目；不含其它 kind（含 PRJ／GRD 侧同系列性质的不同实例，各自单独申请）；不含 R 系列以外性质。
deadline:
  type: event
  lrm: 编译器首次成功运行（0.17.6(2) 指定的 LRM）
  calendar_date: null
  note: 同 WV-PRJ-E3-01；超期自动升 P0＋CH-C(2)，延续＝新 Waiver。
closing_condition: >-
  编译器首次成功运行 ∧ R1／R2／R6／R7／R8 五项各建 FVR 条目 ∧ 接线完成 ∧ first_full_run 留证 ∧ 逐条 seed→active。
remediation_plan: '(1) project.py 自检全过 → (2) 编译器重验证（0.17.6(3) 三分类）→ (3) 为 R1／R2／R6／R7／R8 建 FVR 条目并接线、首次全量运行留证 → (4) 逐条 seed→active。本 Waiver 在 (3) 完成时闭合。'
risk_quantification: >-
  触及面 8 实例。利息形态：治理性质（批准闭环、重审门槛、临时决策软化传播、证据溯源、重审影响传播）由机器检出退化为人工核验，
  延迟＝一个决策周期；漏检后果分性质——R1 漏检＝执行者自批进入台账（P0 面）；R2 漏检＝未过三条件的重审被受理；
  R6 漏检＝临时决策被当硬约束传播；R7 漏检＝无出处证据进入决策；R8 漏检＝重审后下游血缘失检。
  缓解：(i) 0.17.5 ADR 附注「依据种子条目，待重验证」；(ii) GOV 六条的 anti_patterns／signals 判读带母本指针；
  (iii) project.py 的 M 系列与 C-ST／C-ID 静态检查覆盖可机器判定面。
independent_effect: true
approval:
  category: 批准注册表类目 + 8.2.7 评审点五（例外评审）
  external_cause: false
  status: pending
  note: 本轮只备内容、不写台账。本项与 `G-GOV-1`／`SO-19` 无关：`G-GOV-1` 记录的是「三 kind E3 Waiver 未起草」，本项落盘后才由其收口，不得先行关闭。
```

## 3. `WV-GRD-E3-01`

```yaml
waiver_id: WV-GRD-E3-01
rule: 'E3（母本 10.5）：∀ property(hard): ∃ fvr_entry ∧ wired ∧ first_full_run has evidence —— FVR 全覆盖，硬'
violation_fact: >-
  GRD 批 3 条（GRD-001 P0 阻塞级／GRD-002 P1 限期级／GRD-003 P2 监测级）经人工种子通道迁移为 seed；
  其 formal_anchor 为 G1／G5／G7 各 1 个 implements，而 G 系列在 FVR 侧尚无条目与接线（批前全库 G 系列本无实例，
  本批系 G1／G5／G7 的首次计息面）→ E3 三支一律未满足。合法性出处同上。
  前置：G-GRD-1 已于 2026-11-06 closed；G1／G5 的级别由母本 9.5 明文标注「P0 即时阻塞 —— 硬」「豁免不静默展期 —— 硬」，
  无待裁空间（原冻结点「G1／G5 硬软级别未定」已随之消失）。
scope: >-
  精确范围：status=seed 的 GRD-001…GRD-003 三条的 formal_anchor 所引性质实例，共 3 项 3 实例——
  G1『P0 即时阻塞 —— 硬』implements 1（GRD-001）；G5『豁免不静默展期 —— 硬』implements 1（GRD-002）；
  G7『P2 双判据告警治理 —— 硬』implements 1（GRD-003）。
  不含 active 条目；不含其它 kind（含 SRC 侧 G1 的 triggers 3 实例，见 §4）；不含 G 系列以外性质。
deadline:
  type: event
  lrm: 编译器首次成功运行（0.17.6(2) 指定的 LRM）
  calendar_date: null
  note: 同前两份；超期自动升 P0＋CH-C(2)，延续＝新 Waiver；G5 对「静默展期」的禁止同样适用于本项自身。
closing_condition: >-
  编译器首次成功运行 ∧ G1／G5／G7 三项各建 FVR 条目 ∧ 接线完成 ∧ first_full_run 留证 ∧ 逐条 seed→active。
remediation_plan: '(1) project.py 自检全过 → (2) 编译器重验证（0.17.6(3) 三分类）→ (3) 为 G1／G5／G7 建 FVR 条目并接线、首次全量运行留证 → (4) 逐条 seed→active。本 Waiver 在 (3) 完成时闭合。'
risk_quantification: >-
  触及面 3 实例。利息形态：守护规则三级的机器判定（P0 阻塞、豁免到期自动升级、P2 双判据告警）退化为人工核验；
  漏检后果——G1 漏检＝P0 无整改/无批准豁免即部署进入实现；G5 漏检＝到期豁免被静默展期（正是 9.2.2 明令禁止的侵蚀形态）；
  G7 漏检＝单点越阈被当作告警。缓解：(i) GRD 三条的 anti_patterns／signals 判读带母本指针；
  (ii) project.py 静态自检覆盖可机器判定面；(iii) 0.17.5 ADR 附注。
independent_effect: true
approval:
  category: 批准注册表类目 + 8.2.7 评审点五（例外评审）
  external_cause: false
  status: pending
  note: 本轮只备内容、不写台账。G1 的「内部原因 P0 不可豁免」只约束**裁量豁免**；本项属 0.17.6(2) 明文的制度性豁免（同 WV-STY-E3-01 已裁定边界），边界表述沿用，不新增先例。
```

## 4. 覆盖缺口与待决

- **SRC 批的 G1 `triggers` 3 实例（SRC-002／003／004）无任何在册 Waiver 覆盖**：14 份在册 Waiver 均不含 SRC；本草案按用户指定只覆盖 PRJ／GOV／GRD 三 kind，故 SRC 3 实例仍悬空。两条出路，须用户选一：
  1. 另起第 4 份 `WV-SRC-E3-01`（scope＝G1 triggers 3 实例，其余同本文件模板）；
  2. 明确裁定「SRC 只触发 G1、不独立计息，G1 的 FVR 条目由 `WV-GRD-E3-01` 首建后一并覆盖」，并在 `WV-GRD-E3-01.scope` 显式登记该 3 实例的**引用面**（不等于扩宽豁免面）。
- 三份均未解决「E3 的守护规则条目未建立、级别未定」——该项按既有先例不预设。

## 5. 落盘与批准口径（批准后才做）

1. 仅在 `registry/method_registry.yaml` 的 `waivers` 段末尾追加三条（顺序 PRJ → GOV → GRD，编号不复用）。
2. `approval.status` 先写 `pending`；人类裁决后补 `approved_by`／`approved_date`／`ruling` 三键，不得预置空键。
3. 同日批准可只记日历日，不写时点（0.4 禁假精确）。
4. `G-GOV-1`／`SO-19` 的关闭**不在本批**：须待三条落盘后再单独处置，且不限本笔。
