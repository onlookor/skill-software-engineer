// ============================================================================
// 软件工程元框架 · PACT 适配结构 · 档 III（中大型 / 多团队多服务）
// ----------------------------------------------------------------------------
// 范式      ：PACT v1 rev2（Precondition-governed Autonomous Counter-based Token）
// 文法依据  ：docs/pactv1_rev2.md §3.1
//             Domain ::= TypeSchema PreconditionGraph GateMatrix SeedAuthorityDecl
// 母本      ：软件工程元框架成文法.md（下列条款指针均指该文件）
// 裁剪依据  ：软件工程元框架-部署规模裁剪模板.md §1.1（红线 R1–R6）、§1.2（三合法轴）、
//             §2.1–§2.6（参数包）、§3「档 III：中大型 / 多团队多服务」
// 同族文件  ：se_tier1_solo.pact（档 I）、se_tier2_small_team.pact（档 II）
//
// 【本档的特殊地位：不裁剪，但"不裁剪"本身须登记】（裁剪模板 §3 档 III）
//   档 III 是母本默认形态的全量启用，本档**无需裁剪 ADR**；但"本部署按母本默认
//   形态全量装配、未做任何裁剪"这一事实仍须按裁剪模板 §1.3 登记为一条事实记录
//   （否则后续任何局部省略都无基线可比，等同隐性裁剪，落入 §4 违例清单）。
//
// 【档位性质声明】（裁剪模板 §3 引言，照引不减）
//   档 III 是**装配形态示例**，不是规范分级，更不是人数门槛。母本的可行性过滤器是
//   三空间承载能力（§1.3 交付空间硬过滤器 / §2.3；§5.3/§9.3 on-call 与观测；
//   §8.3 CI 成熟度）。对档入座前必须以有出处的三空间勘察事实为准。事实跨档时
//   按事实逐项取档——例如"多团队但无生产监测平台"应按事实把守护检测手段逐项
//   降为人工形态，而不是整体降到档 II。
//
// 【本档三空间事实前提】（裁剪模板 §3 档 III，须勘察在案，非假定）
//   多团队、多服务；完整 CI/CD 与生产监测平台；存在跨方契约与多所有权主体；
//   多 Agent 参与生产阶段（另须完成《编译规范》#9 并发协议，属配套层义务）；
//   系统承载不可逆外部事实（§0.11 现状锁定生效）。
//
// 【本档参数取值】
//   批准链总级数 m = 3（主批准人 + 两级有序备选；`count approval_escalation >= 3` 判不可达）
//     ※ m = 3 是**本适配结构的参数包取值**，母本 §0.5 只规定"完整有序备选链"
//       而未定级数；级数由 approval_registry_entry 条目字段决定。若某部署的链长
//       不为 3，改的是本文件的 count 字面量与注册表条目，母本条款不变——
//       该改动本身是高影响决策，须走 §0.13 注册表变更 + §8.2.7 评审点一。
//   消解链递归深度 N = 3（§0.19.5 第 3 条母本默认值，本档不裁剪）
//   评审点集合 = 五类全保留、独立排期、分别留痕（§8.2.7 T8）
//   五注册表 = 全量装配（§10.2.5 判据 2；子集/全量之别只在条目数，不在表数）
//   检测手段 = 封闭三形态中的自动化形态为主（裁剪模板 §2.5）
//   视图形态 = 图形视图为主（§10.3；投影规则纯函数、可重放）
//   编排形态 = 工作流引擎承载 CH-B（裁剪模板 §2.4）
//
// 【与档 II 的形式层差异】（只有这两项，其余全部同构）
//   D-1 参与者名册 +2：approver_external（§0.5 有序备选链第二级，链外/跨团队
//       批准责任人）、service_owner（方面 3 所有权：多服务下每个服务有独立所有权
//       主体，各自对其服务发出守护信号）。角色位总数 18 → 20。
//   D-2 count 阈值：m 2→3、N 2→3。
//   类型集与前置图**与档 II 完全一致**（41 类型 / 33 规则），无任何增删。
//   这正是裁剪模板 §1.2 三合法轴的结论在形式层的投影：三轴中只有"粒度"能进
//   `.pact`（表现为参与者名册细分与 count 阈值），"频次"与"工具形态"必须落
//   配套内容层——因为 PACT 无时间词汇、无工具词汇。
//
// 【guard_signal 的多生产者语义】（本档特有）
//   guardian（平台级守护）与 service_owner（服务级守护）**同为 guard_signal 的
//   producer**。这不是冗余，而是多服务部署下"守护义务按所有权分片"的形式表达：
//   PACT 允许多个参与者持有同一类型的 produces gate（RHS Uniqueness 约束的是
//   前置图的 RHS，不是 Gate Matrix 的生产者数量），因此每个所有权主体都能独立
//   就其服务发出信号，而下游处置链（waiver_request → waiver_grant）保持单一。
//   服务与所有权主体的对应关系是 guard_rule_entry 的条目字段（配套层）。
//
// 【关键建模纪律：参与者 = 角色位，不是自然人】
//   档 III 下 20 个角色位应由不同自然人/不同团队填充，且必须满足：
//     - approver_primary / approver_backup / approver_external 三级互不兼任
//       （§0.5 有序备选链的意义在于主批准人不可达时链仍可走）；
//     - external_arbiter 与 review_waiver、oncall_responder 互不兼任
//       （§9.2.2 利益无关方）；
//     - review_* 五个角色位不得由 agent_preparer 或 system_automaton 填充
//       （§8.2.7 T8 / §0.10 第一条）。
//   这些"互不兼任"约束是**配套层的注册表条目约束**，PACT 形式层无法表达
//   （参与者是角色位标识，不携带自然人身份）——记为已知表达边界 E7。
//
// 【本文件不表达的维度】（禁止造语法，一律落配套内容层）
//   1. 频次与时限：评审排期、批准时限、Waiver 期限与到期升 P0、on-call 轮值、
//      守护/勘察周期、CI 触发节奏、视图刷新节奏。
//   2. 多路由 OR：FM-0～FM-15（§0.20.2）、D1–D6 有序首命中（§0.19.4）、
//      S6 高/低影响二路由（§0.18.2 S6(ii)）。见 E1。
//   3. 图结构判据：冲突图成环（§0.19.5）、决策血缘下游逐一目检（§0.19.2 规则 1(ii)，
//      R8 联动）——档 III 决策血缘规模大，此项尤为关键，但形式层不可判。
//   4. 三值语义与 unknown 传播：M15、§0.19.3。未闭合勘察义务 = 未消费的
//      survey_obligation 常驻 Counter = 可见的债。
//   5. 概率、成本数值、SLO 阈值、包络界表达式（§6.2.4 / §8.2.5）、
//      Saga 补偿步数、Z4 超时预算、Z5 registered_max_depth。
//   6. 多 Agent 并发协议（《编译规范》#9）：PACT 的 Counter 语义本身是并发安全的
//      （Token 不可变 + 前置图门控），但**多 Agent 之间的任务分配、锁与重试策略**
//      不在域声明范围内，属编译层义务。
//
// 【已知表达边界】（E1–E6 与档 I/II 同；E7 为本档新增）
//   E1. RHS Uniqueness 禁止 selected_entry 经"完整 ADR"与"简记包"两路汇聚到同一
//       decision_landing，故建成两条不相交 Token 流；择一由 §7.2.2 谓词在配套层
//       裁决。互斥性部分编码为 `reads selected_entry when not exists adr_package`；
//       反向不阻塞，承载 §7.2.4"越级 → 摘出补全流程 + P2"。
//   E2. produces 不得携带条件（DomainError::ProduceWithCondition），故阈值/存在性
//       判据只能挂 reads/consumes。
//   E3. A0–A5 权威六级全序中只有 A0 有对应 Token；A1–A5 比较是配套层谓词求值。
//       档 III 冲突密度高，此项表达缺口影响最大（T1/T2/T3 平票序列全在配套层）。
//   E4. 让步记录的三个强制消费端在形式层是 reads（Rule-R 非破坏）+ Archive 审计链。
//   E5. PACT 无时序词汇；"会签先于批准"编码为 Counter 在场性。
//   E6. approval_escalation 只读不消费，是 m 阈值可数的前提（消费即计数归零，
//       链耗尽判定失效）。升级台账常驻是设计意图，非技术债。
//   E7.（本档新增）"角色位互不兼任"不可表达：PACT 参与者是不透明标识，
//       无自然人身份、无互斥约束词汇。三级批准链的独立性、Waiver 的利益无关性
//       在形式层只体现为**角色位分离**（存在三个独立的 produces approval_record
//       的 gate），实际是否由不同人填充须由 approval_registry_entry 条目与
//       部署前检查单保证。这是档 III 最需要人类复核的表达缺口。
//
// 【红线自检】（裁剪模板 §1.1 六项 + 两项结构性必备）
//   R1 §0.10 权力条款   ：三级 approver_* / 五个 review_* / responsible_human /
//                         external_arbiter / contract_owner / oncall_responder /
//                         service_owner 全部是人类角色位；agent_preparer 与
//                         system_automaton 无 produces approval_record /
//                         decision_landing / selected_entry / human_ruling /
//                         waiver_grant / grounding_status / contract_confirmation 的 gate。
//                         批准不可达 → unreachable_event → provisional_ruling，
//                         **不存在"默认通过"的产生式**。
//   R2 §0.4 出处门槛    ：tri_space_fact / new_fact 为源类型，只能经 Rule-S 注入；
//                         档 III 下注入者须为具名责任人（署名登记在配套层）。
//   R3 §0.6 接续处置协议 ：conflict_instance 两个出口；自动出口受 N=3（母本默认）
//                         限制，超限即只剩人类出口；不存在第三路。
//   R4 高影响批准路径    ：decision_landing ← {adr_package + approval_record} ←
//                         approval_registry_entry；注册表未声明即全阻塞。
//                         档 III 下该阻塞会跨团队传播，故注册表全量装配是启动前提。
//   R5 硬性质与 P0 响应  ：guard_signal → waiver_request → waiver_grant 唯一豁免通道；
//                         guard_signal 有两个 producer（平台级 + 服务级）但只有
//                         oncall_responder 一个消费口，处置责任不被所有权分片稀释。
//   R6 接地六判据        ：grounding_status 受 `exists` × 5 守护；五注册表条目全为
//                         源类型且无 produces gate（Source-Production Constraint）。
//   结构性必备一：approval_registry_entry 必须 seed 且三级链齐备。
//   结构性必备二：五注册表全量装配（本档不取子集）。
//
// 【组合接口】（与 requirements-engineering/pact/re_fragment.pact）
//   re_baseline 是唯一跨片段共享类型；本文件只声明类型、不声明其前置规则、
//   不持有 produces re_baseline 的 gate（§1.8 D18 单侧声明语义）。组合后：
//     - re_baseline 的前置由 RE 侧提供（validation_report → re_baseline）；
//     - 本文件保留 seed 权威作为"外部基线导入"通道；
//     - contract_owner 与 agent_preparer 均 reads re_baseline，是 SE 侧对 RE 产物
//       的两个消费点（选型上下文装配 + 契约确认）；
//     - 参与者名不重叠 ⇒ §1.8 C3 空满足；seed 与 produce 分属不同参与者 ⇒
//       不触发 A.5 SEED_PRODUCE_OVERLAP。
//   档 III 是 RE 与 SE **同时部署**的典型形态（多团队下需求基线必须由 RE 片段
//   生产而非导入），故本档的组合校验是必做项，不是可选项。
// ============================================================================

types {
    // ---- 源类型（Precond 为空集，只能经 SeedAuthority / Rule-S 注入）----
    tri_space_fact;            // §1.3/§2.3 三空间勘察事实，每条过 §0.4 出处门槛
    external_mandate;          // §0.19.2 A0 外部显式指定（合同 SLA / 监管条文 / 法定要求）；§0.11
    new_fact;                  // §7.2.4 三空间新事实（R2 重审门槛的唯一合法触发源）
    method_registry_entry;     // §0.17.2 方法注册表条目（本档全量装配）
    approval_registry_entry;   // §0.5 / §7.2.5 批准角色注册表条目（三级有序备选链 + 时限）
    guard_rule_entry;          // §9.2.2 守护规则注册表条目（含服务↔所有权主体对应字段）
    fvr_entry;                 // §10.2.4 FVR 条目（本档由 CI/CD 自动化执行，§8.3）
    projection_rule_entry;     // §10.2.1/§10.2.2 投影规则条目（本档图形视图为主，§10.3）
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
    approval_record;           // §0.5 R1 批准记录（三级链中任一级署名，时限内）
    decision_landing;          // S6(iii) 谓词写入（§10.2.3bis），常驻不消费

    // ---- 批准不可达路径（§0.5 时限 + 有序备选链；FM-2；§0.10 第三条）----
    approval_deadline_breach;  // 批准时限逾越事件
    approval_escalation;       // 备选链上移一级（**只读不消费**，见 E6）
    unreachable_event;         // FM-2：三级链耗尽仍不可达
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
    guard_signal;              // §9.2.2 守护信号（平台级 + 服务级两个 producer，见文件头）
    waiver_request;            // §9.2.2 Waiver 请求（五要素齐备，缺一驳回）
    waiver_grant;              // §9.2.2 限期限范围豁免（评审点五批准；不允许静默展期）

    // ---- 契约确认（§0.21.2 SM-CT）----
    contract_confirmation;     // 跨方契约确认记录：决策落地与需求基线的一致性签认

    // ---- 重审、表达双通道、接地验收 ----
    reopen_proposal;           // §7.2.4/§7.5 R2：三空间新事实触发的重审提案
    view_instance;             // §10.2.1 E1：人类层视图（纯函数、可重放；本档图形形态）
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

    // ---- 批准不可达（§0.5 时限 + 三级有序备选链；FM-2；§0.10 第三条）----
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

    // ---- 契约确认（§0.21.2 SM-CT）----
    {decision_landing + re_baseline} → contract_confirmation;   // 契约确认须同时对齐已落地决策与需求基线

    // ---- 重审、双通道表达、编译、接地（§7.2.4；§10.2）----
    {decision_landing + new_fact} → reopen_proposal;       // §7.2.4 R2 三条件重审门槛
    {decision_landing + projection_rule_entry} → view_instance;   // §10.2.1 E1
    {selected_entry + method_registry_entry} → compilation_artifact;  // §10.2.3bis
    {compilation_artifact + evidence_artifact} → grounding_status;    // §10.2.5：六判据验收
}

gates {
    // ==== 人类责任方（§0.10 第一条：裁决/批准权不可让渡给自动化）====
    responsible_human:
        reads tri_space_fact, reads re_baseline, reads new_fact,
        reads external_mandate, reads mandate_intake,
        reads method_registry_entry, reads approval_registry_entry,
        reads guard_rule_entry, reads fvr_entry, reads projection_rule_entry,
        // §0.19.2 规则 2 T4 / 规则 3 A0×A0 (FM-7) → CH-C：无条件人类出口（R3）。
        reads conflict_instance, consumes conflict_instance, produces human_ruling,
        // §0.10 第三条：临时保守裁决。**不是**默认通过（provisional_ruling 不产生
        // decision_landing）；档 III 下该裁决须同时通知全部受影响服务所有权主体。
        reads unreachable_event, consumes unreachable_event, produces provisional_ruling,
        // §0.18.2 S6(iii) 谓词写入（§10.2.3bis）：批准后落地生效（R1）。
        reads adr_package, reads approval_record, produces decision_landing,
        // §7.2.3 简记／§0.18.5 快速通道：低影响路由的人类记录端。
        // 档 III 下快速通道准入谓词（impact_scope≤1 ∧ 可逆性∈{free,bounded} ∧
        // S2-lite 无 hard_conflict，裁剪模板 §2.1）由配套层求值，形式层只保留互斥编码。
        reads selected_entry when not exists adr_package, produces shorthand_pack,
        // §7.2.4/§7.5 R2：重审只能由三空间新事实触发，材料性由人类判定。
        reads decision_landing, consumes new_fact, produces reopen_proposal,
        // §10.2.5 判据 2：五注册表不得为空（本档全量装配，见 E2：判据挂 consumes）。
        reads compilation_artifact, reads evidence_artifact,
        consumes compilation_artifact when exists method_registry_entry and exists approval_registry_entry and exists guard_rule_entry and exists fvr_entry and exists projection_rule_entry,
        consumes evidence_artifact,
        produces grounding_status,
        // §0.19.2 消解规则 1：让步记录三个强制消费端之一（Rule-R 非破坏，见 E4）。
        // 档 III 下另两个消费端（A2 败方时血缘下游逐一目检 R8、冲突图的边）
        // 属图结构判据，形式层不可表达（见"不表达的维度"3）。
        reads concession_record, reads human_ruling,
        reads guard_signal, reads waiver_grant;

    // ==== 主批准人（第一级）====
    // via selected_entry：批准相关性见证，防止"批准漂移"。selected_entry 全程不被
    // 消费 ⇒ 见证不会被抽走（A.6 滞留风险为零）。
    approver_primary:
        reads approval_registry_entry,
        reads adr_package via selected_entry,
        produces approval_record;

    // ==== 备选批准人（第二级；§0.5 有序备选链）====
    // 见 E6：reads 而非 consumes approval_escalation，否则 m 阈值不可累积。
    approver_backup:
        reads approval_registry_entry,
        reads adr_package via selected_entry,
        reads approval_escalation,
        produces approval_record;

    // ==== 外部/跨团队批准责任人（第三级；档 III 特有）====
    // 母本 §0.5 只规定"完整有序备选链"未定级数，第三级是本适配结构的参数包取值
    // （见文件头【本档参数取值】※ 注）。三级互不兼任是配套层注册表约束（E7）。
    approver_external:
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

    // ==== 评审点二：简记包抽查（§7.2.3；本档独立排期，抽查比例属配套层）====
    review_shorthand:
        reads shorthand_pack;

    // ==== 评审点三：材料性与重审判定（§7.2.4）====
    // reopen_proposal 在形式层是终态：重审实质是重新进入 S0（§0.18.3 纪律一禁即兴）。
    review_materiality:
        reads shorthand_pack, reads decision_landing, reads reopen_proposal;

    // ==== 评审点四：验证计划评审（§8.2.7）====
    review_verif_plan:
        reads verification_plan, reads fvr_entry,
        consumes verification_plan, produces plan_review;

    // ==== 评审点五：Waiver 批准（§9.2.2）====
    // 不得由 oncall_responder 或 service_owner 兼任（发起方/受影响方与批准方分离）。
    review_waiver:
        reads waiver_request, consumes waiver_request, produces waiver_grant;

    // ==== Waiver 独立性见证（§9.2.2：利益无关方）====
    // 纯只读、无 produces。见 E5：对 waiver_request 的读在被消费后自然失效。
    external_arbiter:
        reads guard_signal, reads waiver_request, reads waiver_grant;

    // ==== 值守响应（§9.3 on-call 轮值 / §10.2.5 判据 6）====
    // guard_signal 的**唯一**消费口：无论信号来自平台级 guardian 还是服务级
    // service_owner，处置责任都汇聚到值守角色位，不被所有权分片稀释（R5）。
    oncall_responder:
        reads guard_rule_entry, reads guard_signal,
        consumes guard_signal, produces waiver_request;

    // ==== 契约所有者（§0.21.2 SM-CT）====
    // 跨方契约确认须同时对齐 decision_landing 与 re_baseline；本角色位是 SE 片段
    // 中直接消费 RE 侧产物的 gate——跨片段耦合点。
    contract_owner:
        reads decision_landing, reads re_baseline, produces contract_confirmation;

    // ==== 服务所有权主体（方面 3 所有权；档 III 特有）====
    // 与 guardian 同为 guard_signal 的 producer：守护义务按所有权分片
    // （见文件头【guard_signal 的多生产者语义】）。多服务下同一部署会有多个
    // service_owner 实例填充本角色位，各自的服务范围由 guard_rule_entry 条目界定。
    // 不持有 waiver_request 的 produces gate——服务所有者是受影响方，不得自请豁免。
    service_owner:
        reads decision_landing, reads guard_rule_entry, produces guard_signal,
        reads contract_confirmation, reads view_instance, reads reopen_proposal;

    // ==== Agent 备料（§0.10 第二条：备料至"只需裁决"，无裁决权）====
    // 档 III 下可有多个 Agent 填充本角色位并发备料；Counter 语义本身并发安全
    // （Token 不可变 + 前置图门控），但任务分配/锁/重试属《编译规范》#9 义务。
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
        reads selected_entry, produces adr_package;

    // ==== 时限与备选链自动机（§0.5）====
    // 只做事实检测与上报，不做裁决（R1）。m = 3 / N = 3（母本默认，本档不裁剪）。
    system_automaton:
        reads adr_package, reads approval_registry_entry, produces approval_deadline_breach,
        reads approval_deadline_breach, consumes approval_deadline_breach, produces approval_escalation,
        reads approval_escalation when count approval_escalation >= 3, produces unreachable_event,
        // N = 3（§0.19.5 第 3 条母本默认值）：自动让步至多三次，此后本消费口关闭，
        // 只剩 responsible_human 的人类出口（良基性终止）。
        reads conflict_instance,
        consumes conflict_instance when not count concession_record >= 3,
        produces concession_record;

    // ==== 平台级守护（§9.2.1/§9.2.2；本档检测手段为自动化形态，裁剪模板 §2.5）====
    guardian:
        reads guard_rule_entry, reads decision_landing, produces guard_signal;

    // ==== 验证执行（§8.2.1/§8.2.6/§10.2.4；本档由 CI/CD 自动化承载，§8.3）====
    // 计划起草与取证执行同属验证角色位；二者之间隔着人类的 review_verif_plan，
    // 故不构成"自审自证"（§8.2.7 T8）。
    verifier:
        reads decision_landing, reads fvr_entry, produces verification_plan,
        reads plan_review, produces evidence_artifact;

    // ==== 投影（§10.2.1 E1；本档图形视图为主，§10.3）====
    projector:
        reads decision_landing, reads projection_rule_entry, produces view_instance;

    // ==== 编译（§10.2.3bis/E4；本档编排由工作流引擎承载 CH-B，裁剪模板 §2.4）====
    compiler:
        reads selected_entry, reads method_registry_entry, produces compilation_artifact;

    // ==== 审计只读（§8.2.6 证据保全）====
    // 纯只读、无 produces、无 consumes——审计不得改变被审计对象的状态。
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
    // 档 III 是 RE 与 SE 同时部署的典型形态：re_baseline 通常由 RE 侧
    // release_manager 生产，本 seed 权威仅在"既有基线导入"时使用（Rule-S 记入审计链）。
    responsible_human: seeds re_baseline
}
