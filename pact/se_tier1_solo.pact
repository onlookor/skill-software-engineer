// ============================================================================
// 软件工程元框架 · PACT 适配结构 · 档 I（单人 / 探索原型）
// ----------------------------------------------------------------------------
// 范式      ：PACT v1 rev2（Precondition-governed Autonomous Counter-based Token）
// 文法依据  ：docs/pactv1_rev2.md §3.1
//             Domain ::= TypeSchema PreconditionGraph GateMatrix SeedAuthorityDecl
// 母本      ：软件工程元框架成文法.md（下列条款指针均指该文件）
// 裁剪依据  ：软件工程元框架-部署规模裁剪模板.md §1.1（红线 R1–R6）、§1.2（三合法轴）、
//             §2.1（评审与决策通道参数）、§3「档 I：单人 / 探索原型」
//
// 【档位性质声明】（裁剪模板 §3 引言，照引不减）
//   档 I 是**装配形态示例**，不是规范分级，更不是人数门槛。母本的可行性过滤器是
//   三空间承载能力（§1.3 交付空间硬过滤器 / §2.3 S6 退化；§5.3/§9.3 on-call 与观测；
//   §8.3 CI 成熟度）。对档入座前必须以有出处的三空间勘察事实为准，并经裁剪模板
//   §1.3 裁剪 ADR 登记。本文件是"档 I 装配形态"的形式层骨架，不替代该 ADR。
//
// 【本档三空间事实前提】（裁剪模板 §3 档 I，须勘察在案，非假定）
//   单一责任人承担分析/批准/运维；无团队边界（S6 退化适用，§2.3 + §0.10 第二条）；
//   无 CI 或仅脚本化构建；无生产监测平台；问题空间目标不稳定或缺失（§6.3 探索型）；
//   系统尚未承载不可逆外部事实。
//
// 【本档参数取值】（裁剪模板 §2.1）
//   批准链总级数 m = 1（主批准人＝责任人本人；备选链＝外部干系人/空缺并知阻塞后果）
//   消解链递归深度 N = 1（§0.19.5 第 3 条默认 3；小部署取更小值＝更早升级人类）
//   评审点集合 = 五类全保留（§8.2.7 T8：类型存在性不可自动化删减），
//                可合并为同一评审节拍（"评审日"五会连开），均排期、均有责任人。
//
// 【关键建模纪律：参与者 = 角色位，不是自然人】
//   档 I 由单一自然人填充下列 15 个角色位（含 approver_primary 与 responsible_human
//   同为一人，裁剪模板 §3 档 I「决策通道」行：责任人自审自批，**完整 ADR 包与署名
//   不减**）。角色位不合并，因为：
//     R1（§0.10 第一/二条）——批准权不可让渡给自动化，Agent 不得自任批准人/评审人；
//     T8（§8.2.7）——五类评审点的类型存在性不可删；
//     §0.5——批准角色注册表必须显式声明，未声明则全部高影响决策走阻塞路径。
//   "一个人填多个角色位"是配套内容层的排期与署名事实，不是形式层的角色位删减。
//
// 【本文件不表达的维度】（禁止造语法，一律落配套内容层）
//   1. 频次与时限：评审节拍、简记包复查周期（§7.2.3）、批准时限（§0.5）、
//      Waiver 期限与到期升 P0（§9.2.2）、守护周期勘察周期（§9.2.2）——
//      PACT 无时间词汇，全部为注册表条目/排期事实。
//   2. 多路由 OR：FM-0～FM-15 封闭失败目录（§0.20.2）是 16 路互斥路由；
//      §0.19.4 D1–D6 诊断序是"首个命中即路由"的有序 OR；S6 的高影响/低影响
//      二路由（§0.18.2 S6(ii)）。PACT 的前置图是 AND 合取，RHS 唯一性禁止
//      同一凭证类型有多条产生式，故 OR 不可表达——见下方"已知表达边界 E1"。
//   3. 图结构判据：冲突图成环检测（§0.19.5）、决策血缘下游逐一目检
//      （§0.19.2 消解规则 1(ii)，R8 联动）——非 Token 计数可判。
//   4. 三值语义与 unknown 传播：M15（§0.18.2 S1「未知 ≠ 假」）、§0.19.3
//      条件硬 unknown → 保守激活。PACT 只有"在/不在 Counter"两值。
//      本结构的处理方式：未闭合的勘察义务 = 未消费的 survey_obligation Token
//      常驻 Counter = **可见的债**（论文 Part II「Technical Debt as Unconsumed
//      Tokens」），由 `pact analyze` 的 consumption_reachability 直接报出。
//   5. 概率、成本数值、SLO 阈值、包络界表达式（§6.2.4 / §8.2.5）。
//
// 【已知表达边界】（rev2 前置唯一性约束下的诚实记录，不得静默绕过）
//   E1. RHS Uniqueness（§3.1 约束 1）禁止 `selected_entry` 同时经"完整 ADR"与
//       "简记包"两条路汇聚到同一个 decision_landing。故本结构把两条路建成**两条
//       不相交的 Token 流**：高影响路（adr_package → approval_record →
//       decision_landing）与低影响路（shorthand_pack，终态记录）。二者的**择一**
//       由 §7.2.2 决策分级谓词（impact_scope × reversibility）在配套层裁决。
//       互斥性在形式层部分编码为 responsible_human 的
//       `reads selected_entry when not exists adr_package`（已装配完整 ADR 包时
//       不得再走简记），反向不阻塞——这正好承载 §7.2.4"复查中发现越级 → 摘出
//       补全流程 + P2"：补全流程＝重新发起高影响路，原简记包留在 Counter 作为
//       P2 漂移证据。
//       注：两条路由由**不同角色位**持有（adr_package ← agent_preparer 备料；
//       shorthand_pack ← responsible_human 记录），这既是 §0.10 第二条"Agent 备料
//       至只需裁决"与 §7.2.3"简记是责任人自己的轻量记录"的分工，也规避了
//       DomainError::DuplicateGateClause（同一参与者对同一 (action, T) 只能声明
//       一次，无法并存有条件与无条件两个 `reads selected_entry`）。
//   E2. `produces` 子句不得携带条件（§3.1 Note / DomainError::ProduceWithCondition：
//       生产合法性只由前置图决定）。故一切"阈值/存在性"判据只能挂在 reads/consumes
//       子句上。本文件据此把 §0.19.5 深度上限 N 挂在 `consumes conflict_instance`、
//       把 §0.5 备选链级数 m 挂在 `reads approval_escalation`、把 §10.2.5 判据 2
//       "五注册表不得为空"挂在 `consumes compilation_artifact`。
//   E3. 权威六级全序 A0–A5（§0.19.2）在 PACT 中只有 A0 有对应 Token
//       （external_mandate）。A1–A5 的比较（含 T1 范围特指度、T2 出处权威细分、
//       T3 时间新近性附知情前提）是配套层谓词求值，形式层不表达。
//   E4. 让步记录的三个强制消费端（§0.19.2 消解规则 1）在形式层是 reads（Rule-R
//       非破坏）＋ Archive 审计链，不是 Rule-E 消费；未消费的让步记录 Token 常驻
//       Counter，与维度 4 同型（可见的债）。
//   E5. PACT 无时序词汇。形如"会签须发生在批准之前"的次序，只能编码为
//       **Counter 在场性**：external_arbiter 对 waiver_request 的 reads 在该 Token
//       被 review_waiver 消费（移入 Archive）后自然失效，因此"利益无关方必须在
//       请求尚存活时读取"是结构性成立的，而"何时读"仍属配套层排期事实。
//
// 【红线自检】（裁剪模板 §1.1 六项 + 两项结构性必备，逐项确认未触碰）
//   R1 §0.10 权力条款   ：approver_primary / 五个 review_* / responsible_human /
//                         external_arbiter 全部是人类角色位；agent_preparer 无
//                         produces approval_record / decision_landing / selected_entry
//                         / human_ruling / waiver_grant / grounding_status 的 gate。
//                         批准不可达 → unreachable_event → provisional_ruling
//                         （§0.10 第三条临时保守裁决），**不存在"默认通过"的产生式**。
//   R2 §0.4 出处门槛    ：tri_space_fact / new_fact 为源类型，只能经 Rule-S 由
//                         responsible_human 注入——形式层保证"无出处的事实无法
//                         进入 Token 流"；注入行为本身即署名登记。
//   R3 §0.6 接续处置协议 ：conflict_instance 有两个出口（concession_record /
//                         human_ruling），system_automaton 的自动出口受 N=1 限制，
//                         超限即只剩人类出口；不存在"自行消解或假装合规"的第三路。
//   R4 高影响批准路径    ：decision_landing 的前置集含 approval_record，而
//                         approval_record 的前置集含 approval_registry_entry——
//                         批准注册表未声明 ⇒ 无 approval_record ⇒ 无 decision_landing
//                         ⇒ 高影响决策结构性阻塞（§0.5 精确编码）。
//   R5 硬性质与 P0 响应  ：guard_signal → waiver_request → waiver_grant 是唯一豁免
//                         通道，且 waiver_grant 由人类 review_waiver 消费 waiver_request
//                         后产生；不存在"guard_signal 直接消失"的产生式或消费口。
//   R6 接地六判据        ：grounding_status 的产生受 `exists` × 5 守护（判据 2）；
//                         五注册表条目全为源类型且无任何 produces gate
//                         （Source-Production Constraint 结构性保证），
//                         即"只能装配子集，不能凭空生产"。
//   结构性必备一（批准角色注册表必须声明）：approval_registry_entry 是
//                         approval_record 的前置，未 seed 即全阻塞。
//   结构性必备二（五注册表不得为空）：见 R6；装配的是**子集**，不是空集。
//
// 【组合接口】（与 requirements-engineering/pact/re_fragment.pact）
//   re_baseline 是唯一的跨片段共享类型。本文件**只声明类型、不声明其前置规则、
//   不持有任何 produces re_baseline 的 gate**（§1.8 D18 单侧声明语义：单侧缺席
//   不构成冲突，合并取并）。组合后：
//     - re_baseline 的前置规则由 RE 片段单方提供（validation_report → re_baseline）；
//     - 本文件保留 `responsible_human: seeds re_baseline`，语义是"需求基线在 PACT
//       之外既已存在，由责任人引入并署名"——这是 SE 单独部署（档 I 常见形态）的
//       合法启动路径，不是绕过 RE 的后门（seed 注入按 Rule-S 记入审计链）；
//     - 二者参与者名不重叠，故 §1.8 C3（共享 gate 条件语法同一）空满足；
//     - re_baseline 在 RE 侧由 release_manager 生产、在本侧被 seed，参与者不同，
//       故不触发 A.5 的 SEED_PRODUCE_OVERLAP 咨询性警告。
//   校验命令：pact compose <RE 片段> <本文件> ；pact analyze 逐档。
// ============================================================================

types {
    // ---- 源类型（Precond 为空集，只能经 SeedAuthority / Rule-S 注入）----
    tri_space_fact;            // §1.3/§2.3 三空间勘察事实（问题/系统/交付），每条过 §0.4 出处门槛
    external_mandate;          // §0.19.2 A0 外部显式指定（合同 SLA / 监管条文 / 法定要求）；§0.11 现状锁定
    new_fact;                  // §7.2.4 "三空间新事实"（R2 重审门槛的唯一合法触发源）
    method_registry_entry;     // §0.17.2 方法注册表条目（§0.17.6 人工种子通道启动）
    approval_registry_entry;   // §0.5 / §7.2.5 批准角色注册表条目（主批准人＋有序备选链＋时限）
    guard_rule_entry;          // §9.2.2 守护规则注册表条目（级别/检测手段/阈值窗口/响应义务/出处）
    fvr_entry;                 // §10.2.4 FVR 条目（已激活硬性质的验证检查程序，可为人工执行形态）
    projection_rule_entry;     // §10.2.1/§10.2.2 投影规则条目（表格形态规则合法，§10.3）
    re_baseline;               // 组合接口类型：需求基线（见文件头【组合接口】）

    // ---- 选型规程 S0–S6（§0.18.2 七步）----
    selection_context;         // S0 输出：selection_context(DP, F, C)
    candidate_set;             // S1 输出：候选集 + 逐候选 applicability 求值记录
    survey_obligation;         // S1 unknown → 勘察义务登记（M15：候选保留但附义务）
    survey_record;             // 勘察闭合记录（CH-B 可推翻指标达成）
    survivor_set;              // S2 输出：存活集 + 排除记录（被拒候选登记是 ADR 必备节）
    feasible_set;              // S3 输出：三空间过滤后的可行集 + 过滤记录
    verdict_table;             // S4 输出：逐候选三值判定表
    cost_ledger;               // S4 输出：代价账本（§6.2.4 itemwise 聚合，不稀释极端值）
    selected_entry;            // S5 输出：选定条目 + selection_rationale
    adr_package;               // S6 高影响路：完整 ADR（含被拒候选节、证据集、步骤日志指针）
    shorthand_pack;            // S6 低影响路：简记五字段（§7.2.3）／快速通道（§0.18.5）
    approval_record;           // §0.5 R1 批准记录（署名 + 时限内）
    decision_landing;          // S6(iii) 谓词写入 = 决策的存在形态（§10.2.3bis），常驻不消费

    // ---- 批准不可达路径（§0.5 时限 + 有序备选链；FM-2；§0.10 第三条）----
    approval_deadline_breach;  // 批准时限逾越事件
    approval_escalation;       // 备选链上移一级
    unreachable_event;         // FM-2：备选链耗尽仍不可达
    provisional_ruling;        // §0.10 第三条：临时保守裁决（人类权力，非默认通过）

    // ---- 冲突消解（§0.6 CH-A～CH-E；§0.19.2/§0.19.4/§0.19.5/§0.19.6）----
    conflict_instance;         // §0.19.6 冲突实例（按阻塞事件为粒度，非按决策点生命周期）
    mandate_intake;            // §0.6 CH-A：外部指令注入的范围解包（D6 intake，本身不消解）
    concession_record;         // §0.19.2 消解规则 1：跨级冲突高层胜，败方登记让步记录
    human_ruling;              // §0.19.2 T4 / A0×A0 (FM-7) / A1×A1 (FM-6) → CH-C 人类裁决

    // ---- 验证与守护（§8.2.1/§8.2.6/§8.2.7 评审点四；§9.2.1/§9.2.2 评审点五）----
    verification_plan;         // §8.2.1 验证计划（计划矩阵）
    plan_review;               // §8.2.7 评审点四：验证计划评审通过记录
    evidence_artifact;         // §8.2.6 证据保全（T-F3 七要素）/ §10.2.4 FVR 首轮全量执行证据
    guard_signal;              // §9.2.2 守护信号（P0/P1/P2 分级为条目字段，配套层）
    waiver_request;            // §9.2.2 Waiver 请求（五要素齐备，缺一驳回＝不产生 Token）
    waiver_grant;              // §9.2.2 限期限范围豁免（评审点五批准；不允许静默展期）

    // ---- 重审、表达双通道、接地验收 ----
    reopen_proposal;           // §7.2.4/§7.5 R2：三空间新事实触发的重审提案
    view_instance;             // §10.2.1 E1：人类层视图（纯函数、可重放；表格形态合法）
    compilation_artifact;      // §10.2.3bis/E4：卡片/注册表编译产物（版本须与注册表一致）
    grounding_status;          // §10.2.5 接地六判据验收结论（未过 → 决策一律 provisional）
}

preconditions {
    // ---- S0–S6 主链（§0.18.2；§0.18.3 纪律一"禁即兴"＝不得增步/跳步/改序，
    //      在形式层表现为：链条中每一步的后继都以前一步的产物为前置，无法绕过）----
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
    selection_context → conflict_instance;                 // §0.19.6：冲突在选型上下文中被识别
    external_mandate → mandate_intake;                     // §0.6 CH-A：范围解包（禁过度泛化/过度反抗）
    conflict_instance → concession_record;                 // §0.19.2 规则 1：跨级高层胜，登记让步
    conflict_instance → human_ruling;                      // §0.19.2 规则 2 T4 / 规则 3 FM-7 / 规则 4 FM-6 → CH-C

    // ---- 验证与守护（§8.2；§9.2）----
    decision_landing → verification_plan;                  // §8.2.1：决策落地触发验证计划生成
    verification_plan → plan_review;                       // §8.2.7 评审点四：计划矩阵发布节点评审
    plan_review → evidence_artifact;                       // §8.2.6/§10.2.4：评审通过后方可执行 FVR 取证
    decision_landing → guard_signal;                       // §9.2.2：已部署机制产生守护信号
    guard_signal → waiver_request;                         // §9.2.2：豁免唯一合法通道（R5）
    waiver_request → waiver_grant;                         // §9.2.2：评审点五批准（五要素缺一驳回）

    // ---- 重审、双通道表达、编译、接地（§7.2.4；§10.2）----
    {decision_landing + new_fact} → reopen_proposal;       // §7.2.4 R2 三条件重审门槛
    {decision_landing + projection_rule_entry} → view_instance;   // §10.2.1 E1：投影规则纯函数生成
    {selected_entry + method_registry_entry} → compilation_artifact;  // §10.2.3bis：卡片按注册表版本编译
    {compilation_artifact + evidence_artifact} → grounding_status;    // §10.2.5：六判据验收
}

gates {
    // ==== 人类责任方（§0.10 第一条：裁决/批准权不可让渡给自动化）====
    // 档 I 由单一自然人填充；seed 注入即署名登记（R2 出处门槛的形式层落点）。
    responsible_human:
        reads tri_space_fact, reads re_baseline, reads new_fact,
        reads external_mandate, reads mandate_intake,
        reads method_registry_entry, reads approval_registry_entry,
        reads guard_rule_entry, reads fvr_entry, reads projection_rule_entry,
        // §0.19.2 规则 2 T4 / 规则 3 A0×A0 (FM-7) → CH-C：无条件人类出口，
        // 保证消解链深度超限（N=1）后仍有可走的路（R3）。
        reads conflict_instance, consumes conflict_instance, produces human_ruling,
        // §0.10 第三条：批准不可达时的临时保守裁决。**不是**默认通过——
        // provisional_ruling 不产生 decision_landing（见前置图），高影响决策仍阻塞。
        reads unreachable_event, consumes unreachable_event, produces provisional_ruling,
        // §0.18.2 S6(iii) 谓词写入（§10.2.3bis）：批准记录到位后由责任人落地生效。
        // Agent 无此 gate（R1）；落地是权力行为，不是备料行为。
        reads adr_package, reads approval_record, produces decision_landing,
        // §7.2.3 简记五字段／§0.18.5 快速通道：低影响路由的人类记录端。
        // `when not exists adr_package` 是 E1 的互斥编码：已装配完整 ADR 包者不得
        // 改走简记（防越级降级）；反向不阻塞，承载 §7.2.4"摘出补全流程 + P2"。
        reads selected_entry when not exists adr_package, produces shorthand_pack,
        // §7.2.4/§7.5 R2：重审只能由三空间新事实触发，且由人类判定材料性。
        // new_fact 被消费（Rule-E）＝一个事实只能开一次重审，防重复触发。
        reads decision_landing, consumes new_fact, produces reopen_proposal,
        // §9.2.2：档 I 无独立值守角色位，P0 响应义务由责任人本人闭合（R5）。
        // 修复或走 Waiver，二者必居其一；guard_signal 无"静默消失"的出口。
        reads guard_signal, consumes guard_signal, produces waiver_request,
        // §10.2.5 判据 2：五注册表不得为空——挂在本消费口上（见文件头 E2：
        // produces 不得带条件，故判据只能挂在 reads/consumes）。
        // 装配的是**子集**（裁剪模板 §2.6），不是空集；空集 ⇒ 验收不可产生 ⇒
        // 未接地 ⇒ 全部决策标 provisional（R6）。
        reads compilation_artifact, reads evidence_artifact,
        consumes compilation_artifact when exists method_registry_entry and exists approval_registry_entry and exists guard_rule_entry and exists fvr_entry and exists projection_rule_entry,
        consumes evidence_artifact,
        produces grounding_status,
        // §0.19.2 消解规则 1：让步记录的三个强制消费端之一（张力承认 ADR 材料）；
        // 形式层为 reads（Rule-R 非破坏），见文件头 E4。
        reads concession_record, reads human_ruling;

    // ==== 主批准人（档 I ＝责任人本人，角色位不合并；裁剪模板 §3 档 I「决策通道」）====
    // via selected_entry：批准相关性见证（论文 Part II「Approval Correlation」模式）——
    // 批准必须能指回它所批准的那个选型定案，防止"批准漂移"到别的决策上。
    // selected_entry 全程不被消费，故见证不会被抽走（A.6 滞留风险为零）。
    approver_primary:
        reads approval_registry_entry,
        reads adr_package via selected_entry,
        produces approval_record;

    // ==== 评审点一：设计/选型定案评审（§8.2.7；T8 类型存在性不可删）====
    // S5 的定案权在人类评审，不在 Agent：selected_entry 的唯一 producer 是本角色位。
    // verdict_table / cost_ledger **只读不消费**——它们是 §8.2.6 证据保全对象，
    // 定案后须常驻 Counter 供 auditor 与后续重审复查（消费即移入 Archive，会切断
    // 审计只读口）。reads survey_obligation 使评审人必须面对未闭合的勘察义务（M15）。
    review_design:
        reads verdict_table, reads cost_ledger, reads survey_obligation,
        produces selected_entry;

    // ==== 评审点二：简记包抽查（§7.2.3）====
    // 只读角色位：抽查不改状态。复查周期（默认一迭代/一周，裁剪模板 §2.1）是
    // 配套层排期事实，形式层不表达。
    review_shorthand:
        reads shorthand_pack;

    // ==== 评审点三：材料性与重审判定（§7.2.4）====
    // 只读角色位。reopen_proposal 在形式层是终态：重审的实质动作是**重新进入 S0**
    // （由责任人注入新的 tri_space_fact / 重新发起选型），不是从 reopen_proposal
    // 派生 Token——因为"重审"与"新选型"在母本里是同一个规程（§0.18.3 纪律一禁即兴）。
    review_materiality:
        reads shorthand_pack, reads decision_landing, reads reopen_proposal;

    // ==== 评审点四：验证计划评审（§8.2.7）====
    // consumes verification_plan：计划经评审定案后移入不可变 Archive，
    // plan_review 是其唯一后继凭证——"未过评审的计划不得据以取证"由前置图保证
    // （plan_review → evidence_artifact）。
    review_verif_plan:
        reads verification_plan, reads fvr_entry,
        consumes verification_plan, produces plan_review;

    // ==== 评审点五：Waiver 批准（§9.2.2）====
    // consumes waiver_request：请求被处置（批准）即消耗；驳回＝不产生 Token，
    // 请求留在 Counter 作为未处置的可见债。不允许静默展期（无 waiver_grant 自环）。
    review_waiver:
        reads waiver_request, consumes waiver_request, produces waiver_grant;

    // ==== Waiver 独立性见证（§9.2.2：评审点五须利益无关方）====
    // 纯只读角色位，无任何 produces——独立性体现在"有权看、无权改"。
    // 见文件头 E5：对 waiver_request 的读在该 Token 被消费后自然失效，
    // 因此"会签在批准前"是结构性成立的。
    external_arbiter:
        reads guard_signal, reads waiver_request, reads waiver_grant;

    // ==== Agent 备料（§0.10 第二条：备料至"只需裁决"，无裁决权）====
    // 本参与者不持有任何 approval_record / decision_landing / selected_entry /
    // human_ruling / waiver_grant / grounding_status 的 produces gate（R1 的结构性落点）。
    // 同一 (action, T) 只声明一次，多个 produces 并列（DomainError::DuplicateGateClause）。
    agent_preparer:
        reads tri_space_fact, reads re_baseline, produces selection_context,
        reads selection_context, reads method_registry_entry,
        produces candidate_set, produces conflict_instance,
        // M15：勘察义务的登记与闭合。未闭合者常驻 Counter ＝ 可见的债。
        reads candidate_set, produces survey_obligation, produces survivor_set,
        reads survey_obligation, consumes survey_obligation, produces survey_record,
        reads external_mandate, produces mandate_intake,
        reads survivor_set, produces feasible_set,
        reads feasible_set, produces verdict_table, produces cost_ledger,
        // S6(ii) 高影响路的 ADR 包装配（含被拒候选节、步骤日志指针 §0.18.3 纪律二）。
        reads selected_entry, produces adr_package;

    // ==== 时限与备选链自动机（§0.5）====
    // 只做**事实检测与上报**，不做裁决：产出的是 breach / escalation / unreachable
    // 三个事件 Token，处置权分别在 approver_* 与 responsible_human（R1）。
    // m = 1（本档取值）：主批准人一级即全链，故 `count approval_escalation >= 1`
    // 就可判 unreachable_event。档 II 取 2、档 III 取 3。
    system_automaton:
        reads adr_package, reads approval_registry_entry, produces approval_deadline_breach,
        reads approval_deadline_breach, consumes approval_deadline_breach, produces approval_escalation,
        reads approval_escalation when count approval_escalation >= 1, produces unreachable_event,
        // N = 1（本档取值）：自动让步只允许一次；此后 concession_record 在场，
        // 本消费口被 `not count ... >= 1` 关闭，只剩 responsible_human 的人类出口（R3）。
        reads conflict_instance,
        consumes conflict_instance when not count concession_record >= 1,
        produces concession_record;

    // ==== 守护（§9.2.1/§9.2.2；档 I 检测手段为封闭三形态中的人工执行形态）====
    guardian:
        reads guard_rule_entry, reads decision_landing, produces guard_signal;

    // ==== 验证执行（§8.2.1/§8.2.6/§10.2.4；档 I 为人工执行检查单 + 人工证据保全）====
    // 计划起草与取证执行同属验证角色位；二者之间隔着人类的 review_verif_plan，
    // 故不构成"自审自证"（§8.2.7 T8）。
    verifier:
        reads decision_landing, reads fvr_entry, produces verification_plan,
        reads plan_review, produces evidence_artifact;

    // ==== 投影（§10.2.1 E1；档 I 视图形态为表格/Markdown，§10.3 合法）====
    projector:
        reads decision_landing, reads projection_rule_entry, produces view_instance;

    // ==== 编译（§10.2.3bis/E4；档 I 编排形态为代码优先编排库，裁剪模板 §2.4）====
    compiler:
        reads selected_entry, reads method_registry_entry, produces compilation_artifact;

    // ==== 审计只读（§8.2.6 证据保全 + 论文 Part II「Audit Trail」）====
    // 纯只读、无 produces、无 consumes——审计不得改变被审计对象的状态。
    // 对已被消费的 Token（verification_plan / waiver_request / evidence_artifact /
    // compilation_artifact）的读只在消费前有效，消费后其不可变副本在 Archive 中，
    // Archive 检索属配套层能力（PACT 形式层不建模 Archive 查询）。
    auditor:
        reads selection_context, reads verdict_table, reads cost_ledger,
        reads selected_entry, reads adr_package, reads shorthand_pack,
        reads decision_landing, reads concession_record, reads human_ruling,
        reads survey_obligation, reads evidence_artifact, reads view_instance,
        reads compilation_artifact, reads grounding_status;
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
    // 见文件头【组合接口】：单独部署时引入既有需求基线；与 RE 片段组合后
    // 该类型由 release_manager 生产，seed 权威保留为"外部基线导入"通道。
    responsible_human: seeds re_baseline
}
