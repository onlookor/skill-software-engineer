// ============================================================================
// 软件工程元框架 · PACT 适配结构 · 档 II（小团队 / 单产品）
// ----------------------------------------------------------------------------
// 范式      ：PACT v1 rev2（Precondition-governed Autonomous Counter-based Token）
// 文法依据  ：docs/pactv1_rev2.md §3.1
//             Domain ::= TypeSchema PreconditionGraph GateMatrix SeedAuthorityDecl
// 母本      ：软件工程元框架成文法.md（下列条款指针均指该文件）
// 裁剪依据  ：软件工程元框架-部署规模裁剪模板.md §1.1（红线 R1–R6）、§1.2（三合法轴）、
//             §2.1–§2.6（参数包）、§3「档 II：小团队 / 单产品」
// 同族文件  ：se_tier1_solo.pact（档 I）、se_tier3_multi_team.pact（档 III）
//             三档**类型集与前置图基本一致**，差异只在参与者名册与 count 阈值参数；
//             详见 docs/skill-adaptation.md 的「三档粒度差异矩阵」。
//
// 【档位性质声明】（裁剪模板 §3 引言，照引不减）
//   档 II 是**装配形态示例**，不是规范分级，更不是人数门槛。"2～8 人"是常见画像
//   而非判据；母本的可行性过滤器是三空间承载能力（§1.3 交付空间硬过滤器 / §2.3；
//   §5.3/§9.3 on-call 与观测；§8.3 CI 成熟度）。对档入座前必须以有出处的三空间
//   勘察事实为准，并经裁剪模板 §1.3 裁剪 ADR 登记。事实跨档时按事实逐项取档。
//
// 【本档三空间事实前提】（裁剪模板 §3 档 II，须勘察在案，非假定）
//   小团队、单一产品；存在轻量 CI（承载单元/契约测试、静态检查）；有基本 on-call
//   轮值；高影响决策由团队技术负责人批准，备选链为组长/外部架构责任人；
//   五类评审点独立排期（可与迭代仪式并轨，但分别留痕）。
//
// 【本档参数取值】（裁剪模板 §2.1）
//   批准链总级数 m = 2（主批准人 + 一级备选；`count approval_escalation >= 2` 判不可达）
//   消解链递归深度 N = 2（§0.19.5 第 3 条默认 3；本档取 2）
//   评审点集合 = 五类全保留且**独立排期、分别留痕**（§8.2.7 T8）
//   验证形态 = CI 承载（§8.3），非档 I 的人工执行检查单
//
// 【与档 I 的形式层差异】（只有这三项，其余全部同构）
//   D-1 参与者名册 +3：approver_backup（§0.5 有序备选链第一级）、
//       contract_owner（§0.21.2 SM-CT 契约确认）、oncall_responder
//       （§9.3 on-call 轮值 / §10.2.5 判据 6，档 I 由 responsible_human 兼任）。
//   D-2 类型集 +1：contract_confirmation（SM-CT）。档 I 单人无跨方契约，
//       该状态机不激活——这是**实例化判断**，须由人类责任方复核，不是母本删减。
//   D-3 count 阈值：m 1→2、N 1→2。
//   注：guard_signal → waiver_request 的处置口从 responsible_human 移交
//       oncall_responder（值守与决策分离，避免"自己批准自己的豁免请求"）。
//
// 【关键建模纪律：参与者 = 角色位，不是自然人】
//   档 II 由 2～8 名自然人填充下列 18 个角色位；一人可填多个角色位（如技术负责人
//   兼 review_design），但**不得**由同一人同时填充 approver_primary 与
//   review_waiver 之外又填充 external_arbiter（利益无关方要求，§9.2.2）。
//   角色位不合并的理由同档 I：R1（§0.10）、T8（§8.2.7）、§0.5。
//
// 【本文件不表达的维度】（禁止造语法，一律落配套内容层）
//   1. 频次与时限：评审排期与迭代仪式并轨方式、简记包复查周期（§7.2.3）、
//      批准时限（§0.5）、Waiver 期限与到期升 P0（§9.2.2）、on-call 轮值周期
//      （§9.3）、CI 触发节奏（§8.3）——PACT 无时间词汇。
//   2. 多路由 OR：FM-0～FM-15（§0.20.2）、D1–D6 有序首命中（§0.19.4）、
//      S6 高/低影响二路由（§0.18.2 S6(ii)）。见"已知表达边界 E1"。
//   3. 图结构判据：冲突图成环（§0.19.5）、决策血缘下游逐一目检（§0.19.2 规则 1(ii)）。
//   4. 三值语义与 unknown 传播：M15、§0.19.3。未闭合勘察义务 = 未消费的
//      survey_obligation 常驻 Counter = 可见的债，由 consumption_reachability 报出。
//   5. 概率、成本数值、SLO 阈值、包络界表达式（§6.2.4 / §8.2.5）、
//      Saga 补偿步数上限（裁剪模板 §2.2 取 ≤4）、Z4/Z5 预算与深度。
//
// 【已知表达边界】（与档 I 同；E6 为本档新增）
//   E1. RHS Uniqueness 禁止 selected_entry 经"完整 ADR"与"简记包"两路汇聚到同一
//       decision_landing，故建成两条不相交 Token 流；择一由 §7.2.2 谓词在配套层
//       裁决。互斥性部分编码为 responsible_human 的
//       `reads selected_entry when not exists adr_package`；反向不阻塞，正好承载
//       §7.2.4"复查发现越级 → 摘出补全流程 + P2"。两路由分属不同角色位
//       （adr_package ← agent_preparer 备料；shorthand_pack ← responsible_human），
//       同时规避 DomainError::DuplicateGateClause。
//   E2. produces 不得携带条件（DomainError::ProduceWithCondition），故阈值/存在性
//       判据只能挂 reads/consumes：N 挂 `consumes conflict_instance`、
//       m 挂 `reads approval_escalation`、§10.2.5 判据 2 挂 `consumes compilation_artifact`。
//   E3. A0–A5 权威六级全序（§0.19.2）中只有 A0 有对应 Token（external_mandate）；
//       A1–A5 比较（T1/T2/T3）是配套层谓词求值。
//   E4. 让步记录的三个强制消费端在形式层是 reads（Rule-R 非破坏）+ Archive 审计链。
//   E5. PACT 无时序词汇；"会签先于批准"编码为 Counter 在场性（external_arbiter 对
//       waiver_request 的读在该 Token 被消费后自然失效）。
//   E6.（本档新增）approval_escalation **只读不消费**，是 m 阈值可数的前提。
//       若备选批准人消费掉升级事件，`count approval_escalation >= m` 将永远无法
//       累积到 m，链耗尽判定失效。故 approver_backup 持 `reads approval_escalation`
//       而非 consumes——升级台账必须常驻，其"未被消费"是设计意图而非技术债。
//
// 【红线自检】（裁剪模板 §1.1 六项 + 两项结构性必备）
//   R1 §0.10 权力条款   ：approver_primary / approver_backup / 五个 review_* /
//                         responsible_human / external_arbiter / contract_owner /
//                         oncall_responder 全部是人类角色位；agent_preparer 与
//                         system_automaton 无 produces approval_record /
//                         decision_landing / selected_entry / human_ruling /
//                         waiver_grant / grounding_status 的 gate。
//                         批准不可达 → unreachable_event → provisional_ruling，
//                         **不存在"默认通过"的产生式**。
//   R2 §0.4 出处门槛    ：tri_space_fact / new_fact 为源类型，只能经 Rule-S 注入。
//   R3 §0.6 接续处置协议 ：conflict_instance 两个出口；自动出口受 N=2 限制，
//                         超限即只剩人类出口。
//   R4 高影响批准路径    ：decision_landing ← {adr_package + approval_record} ←
//                         approval_registry_entry；注册表未声明即全阻塞（§0.5）。
//   R5 硬性质与 P0 响应  ：guard_signal → waiver_request → waiver_grant 唯一豁免通道，
//                         由 oncall_responder 发起、review_waiver 批准、
//                         external_arbiter 独立性见证；无"静默消失"出口。
//   R6 接地六判据        ：grounding_status 受 `exists` × 5 守护；五注册表条目全为
//                         源类型且无 produces gate（Source-Production Constraint）。
//   结构性必备一：approval_registry_entry 必须 seed，否则高影响决策全阻塞。
//   结构性必备二：五注册表装配的是**子集**（裁剪模板 §2.6），不是空集。
//
// 【组合接口】（与 requirements-engineering/pact/re_fragment.pact）
//   re_baseline 是唯一跨片段共享类型。本文件只声明类型、不声明其前置规则、
//   不持有 produces re_baseline 的 gate（§1.8 D18 单侧声明语义）。组合后
//   re_baseline 的前置由 RE 侧提供（validation_report → re_baseline）；
//   本文件保留 seed 权威作为"外部基线导入"通道（Rule-S 记入审计链）。
//   参与者名不重叠 ⇒ §1.8 C3 空满足；seed 与 produce 分属不同参与者 ⇒
//   不触发 A.5 SEED_PRODUCE_OVERLAP。
//   本档另将 re_baseline 用于 contract_confirmation 的前置（SM-CT：契约确认须
//   对齐需求基线），这是档 II/III 相对档 I 的唯一新增跨片段耦合点。
// ============================================================================

types {
    // ---- 源类型（Precond 为空集，只能经 SeedAuthority / Rule-S 注入）----
    tri_space_fact;            // §1.3/§2.3 三空间勘察事实，每条过 §0.4 出处门槛
    external_mandate;          // §0.19.2 A0 外部显式指定（合同 SLA / 监管条文 / 法定要求）；§0.11
    new_fact;                  // §7.2.4 三空间新事实（R2 重审门槛的唯一合法触发源）
    method_registry_entry;     // §0.17.2 方法注册表条目
    approval_registry_entry;   // §0.5 / §7.2.5 批准角色注册表条目（主批准人＋有序备选链＋时限）
    guard_rule_entry;          // §9.2.2 守护规则注册表条目
    fvr_entry;                 // §10.2.4 FVR 条目（本档由 CI 承载执行，§8.3）
    projection_rule_entry;     // §10.2.1/§10.2.2 投影规则条目（本档图形/表格混用，§10.3）
    re_baseline;               // 组合接口类型：需求基线（见文件头【组合接口】）

    // ---- 选型规程 S0–S6（§0.18.2 七步）----
    selection_context;         // S0 输出：selection_context(DP, F, C)
    candidate_set;             // S1 输出：候选集 + 逐候选 applicability 求值记录
    survey_obligation;         // S1 unknown → 勘察义务登记（M15）
    survey_record;             // 勘察闭合记录（CH-B 可推翻指标达成）
    survivor_set;              // S2 输出：存活集 + 排除记录
    feasible_set;              // S3 输出：三空间过滤后的可行集 + 过滤记录
    verdict_table;             // S4 输出：逐候选三值判定表
    cost_ledger;               // S4 输出：代价账本（§6.2.4 itemwise 聚合）
    selected_entry;            // S5 输出：选定条目 + selection_rationale
    adr_package;               // S6 高影响路：完整 ADR
    shorthand_pack;            // S6 低影响路：简记五字段（§7.2.3）／快速通道（§0.18.5）
    approval_record;           // §0.5 R1 批准记录（署名 + 时限内；主批准人或备选链）
    decision_landing;          // S6(iii) 谓词写入（§10.2.3bis），常驻不消费

    // ---- 批准不可达路径（§0.5 时限 + 有序备选链；FM-2；§0.10 第三条）----
    approval_deadline_breach;  // 批准时限逾越事件
    approval_escalation;       // 备选链上移一级（**只读不消费**，见 E6：m 阈值可数的前提）
    unreachable_event;         // FM-2：备选链耗尽仍不可达
    provisional_ruling;        // §0.10 第三条：临时保守裁决（人类权力，非默认通过）

    // ---- 冲突消解（§0.6 CH-A～CH-E；§0.19）----
    conflict_instance;         // §0.19.6 冲突实例（按阻塞事件为粒度）
    mandate_intake;            // §0.6 CH-A：外部指令注入的范围解包（D6 intake）
    concession_record;         // §0.19.2 消解规则 1：败方让步记录
    human_ruling;              // §0.19.2 T4 / FM-7 / FM-6 → CH-C 人类裁决

    // ---- 验证与守护（§8.2；§9.2）----
    verification_plan;         // §8.2.1 验证计划（计划矩阵）
    plan_review;               // §8.2.7 评审点四：验证计划评审通过记录
    evidence_artifact;         // §8.2.6 证据保全（T-F3 七要素）/ §10.2.4 FVR 执行证据
    guard_signal;              // §9.2.2 守护信号（P0/P1/P2 分级为条目字段）
    waiver_request;            // §9.2.2 Waiver 请求（五要素齐备，缺一驳回）
    waiver_grant;              // §9.2.2 限期限范围豁免（评审点五批准；不允许静默展期）

    // ---- 契约确认（§0.21.2 SM-CT；档 II/III 专有，见 D-2）----
    contract_confirmation;     // 跨方契约确认记录：决策落地与需求基线的一致性签认

    // ---- 重审、表达双通道、接地验收 ----
    reopen_proposal;           // §7.2.4/§7.5 R2：三空间新事实触发的重审提案
    view_instance;             // §10.2.1 E1：人类层视图（纯函数、可重放）
    compilation_artifact;      // §10.2.3bis/E4：卡片/注册表编译产物（版本须与注册表一致）
    grounding_status;          // §10.2.5 接地六判据验收结论（未过 → 决策一律 provisional）
}

preconditions {
    // ---- S0–S6 主链（§0.18.2；§0.18.3 纪律一"禁即兴"＝不得增步/跳步/改序）----
    {tri_space_fact + re_baseline} → selection_context;   // S0：事实集 + 生效约束集（血缘查询 §7.2.1）
    selection_context → candidate_set;                     // S1：注册表剖面装配（§0.17.4）
    candidate_set → survey_obligation;                     // S1 unknown ≠ false → 勘察义务（M15）
    survey_obligation → survey_record;                     // 勘察闭合（CH-B 可推翻指标达成）
    candidate_set → survivor_set;                          // S2：硬约束排除 + hard_conflict 检验
    survivor_set → feasible_set;                           // S3：交付空间能力过滤 + §0.11 现状锁定
    feasible_set → verdict_table;                          // S4：逐候选 × 逐硬目标包络判定
    feasible_set → cost_ledger;                            // S4：cost_profile 聚合
    {verdict_table + cost_ledger} → selected_entry;        // S5：加权得分 + 不可区分处置（禁按名义分择一，M-Q2）
    selected_entry → adr_package;                          // S6(ii) 高影响 → 完整 ADR
    selected_entry → shorthand_pack;                       // S6(ii) 低影响 → 简记条目/快速通道

    // ---- 批准与落地（§0.5；§7.5 R1）----
    {adr_package + approval_registry_entry} → approval_record;  // §0.5：注册表条目 + ADR 包 → 批准
    {adr_package + approval_record} → decision_landing;         // §7.5 R1：批准后方可生效

    // ---- 批准不可达（§0.5 时限 + 有序备选链；FM-2；§0.10 第三条）----
    adr_package → approval_deadline_breach;
    approval_deadline_breach → approval_escalation;
    approval_escalation → unreachable_event;
    unreachable_event → provisional_ruling;

    // ---- 冲突消解（§0.19）----
    selection_context → conflict_instance;                 // §0.19.6
    external_mandate → mandate_intake;                     // §0.6 CH-A：范围解包
    conflict_instance → concession_record;                 // §0.19.2 规则 1
    conflict_instance → human_ruling;                      // §0.19.2 规则 2 T4 / 规则 3 FM-7 / 规则 4 FM-6 → CH-C

    // ---- 验证与守护（§8.2；§9.2）----
    decision_landing → verification_plan;                  // §8.2.1
    verification_plan → plan_review;                       // §8.2.7 评审点四
    plan_review → evidence_artifact;                       // §8.2.6/§10.2.4
    decision_landing → guard_signal;                       // §9.2.2
    guard_signal → waiver_request;                         // §9.2.2：豁免唯一合法通道（R5）
    waiver_request → waiver_grant;                         // §9.2.2：评审点五批准

    // ---- 契约确认（§0.21.2 SM-CT；档 II/III 专有）----
    {decision_landing + re_baseline} → contract_confirmation;   // 契约确认须同时对齐已落地决策与需求基线

    // ---- 重审、双通道表达、编译、接地（§7.2.4；§10.2）----
    {decision_landing + new_fact} → reopen_proposal;       // §7.2.4 R2 三条件重审门槛
    {decision_landing + projection_rule_entry} → view_instance;   // §10.2.1 E1
    {selected_entry + method_registry_entry} → compilation_artifact;  // §10.2.3bis
    {compilation_artifact + evidence_artifact} → grounding_status;    // §10.2.5：六判据验收
}

gates {
    // ==== 人类责任方（§0.10 第一条：裁决/批准权不可让渡给自动化）====
    // 档 II ＝ 团队技术负责人（可同时填充 review_* 若干角色位）。
    responsible_human:
        reads tri_space_fact, reads re_baseline, reads new_fact,
        reads external_mandate, reads mandate_intake,
        reads method_registry_entry, reads approval_registry_entry,
        reads guard_rule_entry, reads fvr_entry, reads projection_rule_entry,
        // §0.19.2 规则 2 T4 / 规则 3 A0×A0 (FM-7) → CH-C：无条件人类出口（R3）。
        reads conflict_instance, consumes conflict_instance, produces human_ruling,
        // §0.10 第三条：临时保守裁决。**不是**默认通过——provisional_ruling 不产生
        // decision_landing（见前置图），高影响决策仍阻塞。
        reads unreachable_event, consumes unreachable_event, produces provisional_ruling,
        // §0.18.2 S6(iii) 谓词写入（§10.2.3bis）：批准后由责任人落地生效（R1）。
        reads adr_package, reads approval_record, produces decision_landing,
        // §7.2.3 简记五字段／§0.18.5 快速通道：低影响路由的人类记录端。
        // `when not exists adr_package` 是 E1 的互斥编码（防越级降级）。
        reads selected_entry when not exists adr_package, produces shorthand_pack,
        // §7.2.4/§7.5 R2：重审只能由三空间新事实触发，材料性由人类判定。
        reads decision_landing, consumes new_fact, produces reopen_proposal,
        // §10.2.5 判据 2：五注册表不得为空（见 E2：判据只能挂 reads/consumes）。
        reads compilation_artifact, reads evidence_artifact,
        consumes compilation_artifact when exists method_registry_entry and exists approval_registry_entry and exists guard_rule_entry and exists fvr_entry and exists projection_rule_entry,
        consumes evidence_artifact,
        produces grounding_status,
        // §0.19.2 消解规则 1：让步记录三个强制消费端之一（Rule-R 非破坏，见 E4）。
        reads concession_record, reads human_ruling,
        // 档 II：guard_signal 的处置口已移交 oncall_responder（见 D-1 注），
        // 本角色位保留只读监督权，不再自行发起 Waiver（值守与决策分离）。
        reads guard_signal, reads waiver_grant;

    // ==== 主批准人（档 II ＝ 团队技术负责人；裁剪模板 §3 档 II「批准链」行）====
    // via selected_entry：批准相关性见证，防止"批准漂移"到别的决策上。
    // selected_entry 全程不被消费 ⇒ 见证不会被抽走（A.6 滞留风险为零）。
    approver_primary:
        reads approval_registry_entry,
        reads adr_package via selected_entry,
        produces approval_record;

    // ==== 备选批准人（§0.5 有序备选链第一级；档 II ＝ 组长/外部架构责任人）====
    // 见 E6：reads 而非 consumes approval_escalation —— 升级台账必须常驻，
    // 否则 `count approval_escalation >= 2` 永远无法累积，链耗尽判定失效。
    // 备选链顺序（谁第二级、时限各多少）是 approval_registry_entry 的条目字段，
    // 属配套层；形式层只保证"存在一个独立的备选批准角色位且其权力来自主批准链"。
    approver_backup:
        reads approval_registry_entry,
        reads adr_package via selected_entry,
        reads approval_escalation,
        produces approval_record;

    // ==== 评审点一：设计/选型定案评审（§8.2.7；T8 类型存在性不可删）====
    // selected_entry 的唯一 producer 是本角色位（Agent 无此 gate，R1）。
    // verdict_table / cost_ledger 只读不消费：§8.2.6 证据保全对象须常驻供审计。
    review_design:
        reads verdict_table, reads cost_ledger, reads survey_obligation,
        produces selected_entry;

    // ==== 评审点二：简记包抽查（§7.2.3；档 II 独立排期，可与迭代仪式并轨）====
    review_shorthand:
        reads shorthand_pack;

    // ==== 评审点三：材料性与重审判定（§7.2.4）====
    // reopen_proposal 在形式层是终态：重审的实质动作是重新进入 S0
    // （注入新的 tri_space_fact / 重新发起选型），§0.18.3 纪律一禁即兴。
    review_materiality:
        reads shorthand_pack, reads decision_landing, reads reopen_proposal;

    // ==== 评审点四：验证计划评审（§8.2.7）====
    // consumes verification_plan：计划定案后移入不可变 Archive，plan_review 是唯一
    // 后继凭证——"未过评审的计划不得据以取证"由前置图（plan_review → evidence_artifact）保证。
    review_verif_plan:
        reads verification_plan, reads fvr_entry,
        consumes verification_plan, produces plan_review;

    // ==== 评审点五：Waiver 批准（§9.2.2）====
    // 档 II 起，本角色位不得由 oncall_responder 兼任（发起方与批准方分离）。
    review_waiver:
        reads waiver_request, consumes waiver_request, produces waiver_grant;

    // ==== Waiver 独立性见证（§9.2.2：评审点五须利益无关方）====
    // 纯只读、无 produces。见 E5：对 waiver_request 的读在被消费后自然失效。
    external_arbiter:
        reads guard_signal, reads waiver_request, reads waiver_grant;

    // ==== 值守响应（§9.3 on-call 轮值 / §10.2.5 判据 6；档 I 由责任人兼任）====
    // consumes guard_signal：信号必须被处置（修复或申请豁免），无"静默消失"出口（R5）。
    // 轮值表、响应时限、升级路径是 guard_rule_entry 条目字段与排期事实（配套层）。
    oncall_responder:
        reads guard_rule_entry, reads guard_signal,
        consumes guard_signal, produces waiver_request;

    // ==== 契约所有者（§0.21.2 SM-CT；档 II 起存在跨方契约）====
    // 契约确认须同时对齐 decision_landing 与 re_baseline（见前置图），
    // 因此本角色位是 SE 片段中唯一直接消费 RE 侧产物的 gate——跨片段耦合点。
    contract_owner:
        reads decision_landing, reads re_baseline, produces contract_confirmation;

    // ==== Agent 备料（§0.10 第二条：备料至"只需裁决"，无裁决权）====
    // 不持有 approval_record / decision_landing / selected_entry / human_ruling /
    // waiver_grant / grounding_status / contract_confirmation 的 produces gate（R1）。
    // 同一 (action, T) 只声明一次，多个 produces 并列（DomainError::DuplicateGateClause）。
    agent_preparer:
        reads tri_space_fact, reads re_baseline, produces selection_context,
        reads selection_context, reads method_registry_entry,
        produces candidate_set, produces conflict_instance,
        // M15：勘察义务登记与闭合。未闭合者常驻 Counter ＝ 可见的债。
        reads candidate_set, produces survey_obligation, produces survivor_set,
        reads survey_obligation, consumes survey_obligation, produces survey_record,
        reads external_mandate, produces mandate_intake,
        reads survivor_set, produces feasible_set,
        reads feasible_set, produces verdict_table, produces cost_ledger,
        // S6(ii) 高影响路 ADR 包装配（含被拒候选节、步骤日志指针 §0.18.3 纪律二）。
        reads selected_entry, produces adr_package;

    // ==== 时限与备选链自动机（§0.5）====
    // 只做事实检测与上报，不做裁决（R1）。m = 2 / N = 2（本档取值）。
    system_automaton:
        reads adr_package, reads approval_registry_entry, produces approval_deadline_breach,
        reads approval_deadline_breach, consumes approval_deadline_breach, produces approval_escalation,
        reads approval_escalation when count approval_escalation >= 2, produces unreachable_event,
        // N = 2：自动让步至多两次；此后 concession_record 计数达阈，本消费口关闭，
        // 只剩 responsible_human 的人类出口（§0.19.5 良基性终止：更早升级人类）。
        reads conflict_instance,
        consumes conflict_instance when not count concession_record >= 2,
        produces concession_record;

    // ==== 守护（§9.2.1/§9.2.2；档 II 检测手段进 CI + 轻量监测，裁剪模板 §2.5）====
    guardian:
        reads guard_rule_entry, reads decision_landing, produces guard_signal;

    // ==== 验证执行（§8.2.1/§8.2.6/§10.2.4；档 II 由 CI 承载，§8.3）====
    // 计划起草与取证执行同属验证角色位；二者之间隔着人类的 review_verif_plan，
    // 故不构成"自审自证"（§8.2.7 T8）。
    verifier:
        reads decision_landing, reads fvr_entry, produces verification_plan,
        reads plan_review, produces evidence_artifact;

    // ==== 投影（§10.2.1 E1；档 II 视图形态图形/表格混用，§10.3）====
    projector:
        reads decision_landing, reads projection_rule_entry, produces view_instance;

    // ==== 编译（§10.2.3bis/E4；档 II 编排形态为同步链/编排为主，裁剪模板 §2.4）====
    compiler:
        reads selected_entry, reads method_registry_entry, produces compilation_artifact;

    // ==== 审计只读（§8.2.6 证据保全）====
    // 纯只读、无 produces、无 consumes——审计不得改变被审计对象的状态。
    // 已被消费的 Token（verification_plan / waiver_request / evidence_artifact /
    // compilation_artifact）其不可变副本在 Archive；Archive 检索属配套层能力。
    auditor:
        reads selection_context, reads verdict_table, reads cost_ledger,
        reads selected_entry, reads adr_package, reads shorthand_pack,
        reads decision_landing, reads concession_record, reads human_ruling,
        reads survey_obligation, reads evidence_artifact, reads view_instance,
        reads compilation_artifact, reads grounding_status,
        reads contract_confirmation, reads approval_escalation;
}

seed_authority {
    responsible_human: seeds tri_space_fact;
    responsible_human: seeds external_mandate;
    responsible_human: seeds new_fact;
    responsible_human: seeds method_registry_entry;
    responsible_human: seeds approval_registry_entry;
    responsible_human: seeds guard_rule_entry;
    responsible_human: seeds fvr_entry;
    responsible_human: seeds projection_rule_entry;
    // 见文件头【组合接口】：与 RE 片段组合后该类型由 release_manager 生产，
    // seed 权威保留为"外部基线导入"通道（Rule-S 记入审计链）。
    responsible_human: seeds re_baseline
}
