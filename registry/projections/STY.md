# 方法条目卡片（人类层投影）

> 本文件由 `scripts/project.py` 自动生成（机器层→人类层同源投影，母本 0.9／编译规范 E2），**禁止手改**；修改 registry/ 任一源后重跑 `python3 scripts/project.py --project`。

- 批次：种子批次一：STY（kind 前缀见 0.17.3 首行）＋种子批次二：OWN（kind 前缀见 0.17.3）＋种子批次三：CSL（kind 前缀见 0.17.3）＋种子批次四：CRD（kind 前缀见 0.17.3）＋种子批次五：DEC（kind 前缀见 0.17.3）＋种子批次六：CTR（kind 前缀见 0.17.3）＋种子批次七：STP（kind 前缀见 0.17.3）＋种子批次八：DFL（kind 前缀见 0.17.3）＋种子批次九：RLP（kind 前缀见 0.17.3）＋种子批次十：SCH（kind 前缀见 0.17.3）＋种子批次十一：CFG（kind 前缀见 0.17.3）＋种子批次十二：QAT（kind 前缀见 0.17.3）＋种子批次十三：VFM（kind 前缀见 0.17.3）＋种子批次十四：DPS（kind 前缀见 0.17.3）＋种子批次十五：GRD（kind 前缀见 0.17.3；s5e-10 M2）＋种子批次十六：PRJ（kind 前缀见 0.17.3；s5e-10 M2）＋种子批次十七：GOV（kind 前缀见 0.17.3；s5e-10 M2）＋种子批次十八：SRC（kind 前缀见 0.17.3；ADR-SRC-02，2026-11-06）
- 版本：registry_version 1.0.0
- 条目：合计 138 条＝STY 24 条＋OWN 4 条＋CSL 5 条＋CRD 8 条＋DEC 8 条＋CTR 12 条＋STP 4 条＋DFL 5 条＋RLP 7 条＋SCH 3 条＋CFG 4 条＋QAT 15 条＋VFM 6 条＋DPS 5 条＋GRD 3 条＋PRJ 11 条＋GOV 6 条＋SRC 8 条
- kind 覆盖：STY 全覆盖（1.2.1/1.2.2/1.2.3/1.2.4 四表全部行）＋ OWN 全覆盖（4.2.1 全部 4 行）＋ CSL 全覆盖（4.2.3 全部 5 行）＋ CRD 全覆盖（5.2.1 全部 4 行＋5.2.2 全部 4 行）＋ DEC 全覆盖（2.2.1 全部 8 行）＋ CTR 全覆盖（3.2.1 全部 6 行＋3.2.2 全部 6 行）＋ STP 全覆盖（4.2.2 全部 4 行）＋ DFL 全覆盖（4.2.4 全部 5 行）＋ RLP 全覆盖（5.2.3 清单全部 7 项，非表格源，逐表行数不适用）＋ SCH 全覆盖（5.2.4 单段落全部 3 个分号子命题，非表格源，逐表行数不适用）＋ CFG 全覆盖（5.2.6 行内加粗清单全部 4 项，非表格源，逐表行数不适用）＋ QAT 全覆盖（6.2.5 四属性行内清单全部 15 项战术：性能 5／可用性 3／可修改性 4／安全 3，非表格源，逐表行数不适用；6.2.1 七族中可伸缩性／合规／可观测性三族在 6.2.5 无战术 → 缺口登记为 G-QAT-1，不得本地发明）＋ VFM 全覆盖（8.2.1 @3329 手段映射注册表六类全部 6 项：静态分析／可执行检查程序／模型检查／测试／人工评审／生产监测，非表格源，逐表行数不适用；「测试」一类的五个括注子项（单元/集成/契约/行为注入/端到端）不拆条、8.2.2–8.2.7 其余子节降入六条字段，粒度裁决判读登记为 MJ-28 (i)；@3329 的**计划矩阵本身**（五元组形态）在六类粒度下无承载条目 → 缺口登记为 G-VFM-1，不得本地增设第七条）＋ DPS 全覆盖（9.2.5 @3653-3659 单表全部 5 行，表行序 @3655-3659：滚动发布／蓝绿发布／金丝雀发布／功能开关驱动发布／回滚规程；回滚规程 @3659 在语义上是跨策略义务而非独立策略，但母本置其于「策略」列且 DPS kind 由 9.2.5 整节承载 → 按表行序取 DPS-005、不跳过不改序，判读登记于 ST-DPS-01 与 README §4.11）＋ GRD 全覆盖（9.2.1 主表 @3598-3602 全部 3 行：P0 阻塞级／P1 限期级／P2 监测级；9.2.3 @m:9.2.3 九信号源本期不收 → 缺口 G-GRD-1 与 SO-17）＋ PRJ 全覆盖（10.2.2 义务表 @3903-3913 全部 11 行：1.4／2.4／4.4／5.4／8.4／9.4 ＋ 8.2.7 评审点一–五；C4／arc42 16 行实例表 @3921-3932 按母本「实例级，非规范」不作种子）＋ GOV 全覆盖（0.5 表 @117-122 全部 6 行：完整 ADR／接受约束 ADR／张力承认 ADR／保守假设 ADR／权衡承认 ADR／重审提议；7.2.3 @3054-3061 简记格式不单列条目，登记为 GOV 块头格式约束）＋ SRC 全覆盖（9.2.3 @m:9.2.3 信号源表 9 数据行：8 行非部署各立 SRC-001…SRC-008（14 子信号逐条进 signals），1 行部署（部署失败率／回滚率／变更前置时间三指标）归 DPS 不立 SRC；四数对齐 9＝8＋1，见 G-GRD-1 closure 与 README §4.26）；0.17.3 表 @m:0.17.3 共 18 行，已入库 18 kind 全覆盖
- 文件名沿用 CHECK-SPEC C3.3 既定产物名 `STY.md`（该产物首块 kind 为 STY 时的历史命名）；改文件名属规范面变更，须走 ADR＋人工批准，本投影不自行改名。
- 编号：STY 块内分块序为 DATA-SPEC D4.2 裁决，锚定 STY-004（母本反例 18-A 既有引用一致，MJ-1）；母本零改动。
- 卡片仅为紧凑投影；字段全量与逐字措辞以 method_registry.yaml 为准。

## 子维度三：通信/协调风格

（STY-001–STY-006，共 6 条；kind_profile_STY status=seed）

### STY-001｜同步请求-响应

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.3-同步请求-响应
- **envelope** 延迟分位数 P99：`P99(path) = Σ_{i ∈ path} latency_i；depth(path) ↑ → P99(path) 单调不减`
- **envelope** 可用性目标（SLO）：`availability(path) ≤ Π_{i ∈ path} availability_i（串联上界）；depth(path) ↑ → 可达 SLO 上界单调不增`
- **envelope** 可修改性：变更前置时间：`lead_time(change) ≥ max_{i ∈ path} lead_time_i（时间耦合：链上单元须协同发布）`
- **成本**：ops_cost＝随同步链深度与端点数量上升；无独立中介运维项｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：STY-001-AP1 深层同步调用链（链深超出超时预算可容纳层级）；STY-001-AP2 同步链上的跨团队耦合部署
- **兼容性**：STY-004(tension)
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：同步链上的单元边界即调用契约边界；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集（connects/style）
- **formal_anchor**：V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction、bib 5 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：语义简单、易推理、无需处理乱序与重复投递
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源/人工判断；cost_profile: 骨架源/人工判断；compatibility: 交叉表源/人工判断；constraints_imposed: 交叉表源；anti_patterns: 骨架源/交叉表源；formal_anchor: 交叉表源

### STY-002｜异步消息

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.3-异步消息
- **envelope** 延迟分位数 P99：`P99(e2e) ≥ P99_sync_equivalent + queue_delay(load)；queue_delay 随到达率/处理率之比 ↑`
- **envelope** 可伸缩性：单位资源容量增量：`capacity(consumers) 随消费者实例数单调不减（削峰：突发由队列吸收，处理速率由消费者规模决定）`
- **envelope** 可用性目标（SLO）：`delivery_guarantee ∈ {at-most-once, at-least-once, exactly-once}；选 at-least-once → 消费侧必须 idempotency(·, ·) 成立方可保证业务级 SLO`
- **成本**：ops_cost＝消息中间件集群运维 + 积压告警值守；随吞吐与分区数上升｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-002-AP1 用异步消息实现需要同步语义的查询
- **施加约束** 4 项：方面 3←契约须表达投递语义与消息 schema（异步端点不得以进程内调用契约替代…；方面 5←协调须处置重复/乱序/补偿（分布式协调成为必答题）；方面 6←本条目 envelope = 质量目标可达性上界；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction、bib 5 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：时间解耦、削峰、消费者可独立伸缩
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；envelope: 人工判断/交叉表源；cost_profile: 骨架源/人工判断；constraints_imposed: 人工判断

### STY-003｜事件驱动（发布订阅）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.3-事件驱动（发布订阅）
- **envelope** 可修改性：跨边界契约变更数：`新增消费者时 touched_contracts(change) = 0（生产者不改）；变更事件 schema 时 touched_contracts = |subscribers(event)|`
- **envelope** 可伸缩性：单位资源容量增量：`capacity 随消费者组数单调不减；生产者吞吐与消费者数解耦`
- **envelope** 可用性目标（SLO）：`consistency_default = eventual；对强一致目标的可达性 = 不可达（除非引入额外协调，代价单列）`
- **envelope** 可观测性：追踪覆盖率：`causal_trace_coverage ≤ 1 − implicit_hops/total_hops；因果链追踪难度随订阅方数 ↑（母本：因果链追踪难）`
- **成本**：ops_cost＝事件基础设施运维 + 契约治理流程；随订阅方数上升｜聚合语义=itemwise
- **反模式** 3 项（P1×2／P2×1）：STY-003-AP1 事件变成隐式 RPC（PleaseDoX 事件：命令语义伪装为领域事件）；STY-003-AP2 事件契约无版本治理；STY-003-AP3 事件 schema 漂移趋势（消费者兼容性劣化）
- **兼容性**：STY-016(composable)、STY-004(composable)
- **施加约束** 6 项：方面 3←异步消息/事件流必选其一（跨单元契约不得以进程内调用为主手段）；方面 4←事件日志为一等数据模型；方面 5←协同式（choreography）行为为默认；方面 6←本条目 envelope = 质量目标可达性上界…
- **formal_anchor**：V2(implements)、V3(triggers)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 5 [已核验]·metadata_extraction、bib 3 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：新消费者零改动接入、时间解耦、可扩展性最高
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；envelope: 人工判断/骨架源；compatibility: 交叉表源/骨架源/人工判断；constraints_imposed: 交叉表源

### STY-004｜事件溯源 + CQRS

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.3-事件溯源 + CQRS
- **envelope** 可修改性：变更前置时间：`history_completeness = 全量（自溯源起点）；读模型可独立优化 → read_latency 上界由读模型存储决定，与写路径解耦`
- **envelope** 延迟分位数 P99：`read_consistency_lag ≥ 0 且无零上界保证（读模型最终一致）；对强同步查询语义目标：不可达`
- **envelope** 可修改性：跨边界契约变更数：`event_schema_evolution_cost 随已发布事件版本数单调不减（母本：事件 schema 演化难、复杂度↑↑）`
- **成本**：ops_cost＝事件存储 + 投影管道 + 读模型存储三套运维面；复杂度↑↑（骨架源）｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：STY-004-AP1 把 CQRS 当作默认选择用在不需要的场景（无审计要求、读写负载特征相近…；STY-004-AP2 在事件溯源读模型上提供强同步查询语义而未登记批准例外
- **兼容性**：STY-001(tension)、STY-003(composable)
- **施加约束** 5 项：方面 4←事件日志为一等数据模型；方面 3←事件契约必须版本化（读写两侧独立演化）；方面 6←本条目 envelope = 质量目标可达性上界；方面 8←事件回放验证必备（重放即回归手段）…
- **formal_anchor**：V3(triggers)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 5 [已核验]·metadata_extraction、bib 3 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：完整历史（审计、时间旅行调试）、读写模型各自自由优化
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源/交叉表源/人工判断；compatibility: 交叉表源；constraints_imposed: 交叉表源；anti_patterns: 交叉表源

### STY-005｜Broker 中介

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：1.2.3-Broker 中介
- **envelope** 可修改性：跨边界契约变更数：`新增/替换参与方时 touched_contracts = 1（仅对中介）；集中治理 → 策略变更触达单元数 = 1`
- **envelope** 可用性目标（SLO）：`availability(system) ≤ availability(broker)（中介为单点时系统可用性以其为上界）`
- **envelope** 吞吐量：`throughput(system) ≤ throughput(broker)（瓶颈上界）`
- **成本**：ops_cost＝中介集群高可用运维 + 策略治理；集中式 → 单点运维压力高｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-005-AP1 业务逻辑沉积在中介里
- **兼容性**：STY-017(composable)
- **施加约束** 4 项：方面 3←跨中介契约须与中介路由/转换能力自洽（V2）；方面 6←本条目 envelope = 质量目标可达性上界（中介单点上界尤其约束可…；方面 9←中介承载业务逻辑属守护对象（反模式 → G 规则播种）；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 1 [已核验]·metadata_extraction、bib 3 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：异构集成、集中策略点、参与方解耦（契约变更只触达中介）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；envelope: 骨架源/人工判断；compatibility: 骨架源/人工判断

### STY-006｜共享数据

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.3-共享数据
- **envelope** 延迟分位数 P99：`P99 以共享存储访问延迟为下界项；无中介跳，延迟低于跨单元 RPC 形态`
- **envelope** 可修改性：跨边界契约变更数：`touched_contracts(schema_change) = |readers(store)| ∪ |writers(store)|（隐式契约：schema 变更触达全部共享方）`
- **envelope** 可修改性：变更前置时间：`lead_time(change) ≥ max_{p ∈ sharers} lead_time_p（时间耦合：须与全部共享方协同）`
- **成本**：ops_cost＝共享存储运维 + 跨方变更协调成本（随共享方数上升）｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-006-AP1 以共享数据库实现服务间集成（分布式单体信号）
- **兼容性**：STY-016(tension)、STY-014(composable)
- **施加约束** 4 项：方面 3←共享数据的适用条件须由方面 3 已定结论确认并显式记录；方面 4←共享存储的写方与所有权须明确（否则违反数据单一所有者，W4 联动）；方面 6←本条目 envelope = 质量目标可达性上界；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V2(implements)、V3(triggers)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：实现简单、无中介跳、同一存储内可达强一致
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；compatibility: 骨架源；constraints_imposed: 骨架源；anti_patterns: 交叉表源

## 子维度一：抽象/代码结构风格

（STY-007–STY-013，共 7 条；kind_profile_STY status=seed）

### STY-007｜分层

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.1-分层
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`change 限于层 L → touched_units ≤ |units(L)|（层内替换）；跨层变更 → touched_units = Σ_{L ∈ path} touched_units(L)；层间抽象泄漏时该项失去层内上界（见 STY-007-AP3）`
- **envelope** 延迟分位数 P99：`P99(req) ≥ P99_core(req) + Σ_{L ∈ traversed} overhead_L（穿越层的开销：每穿越一层一项；overhead_L 由转发/校验/适配的实现形态决定，为参数）`
- **成本**：ops_cost＝无独立运维面；成本落在结构治理侧（依赖规则校验工具与 CI 门禁）｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：STY-007-AP1 层跳跃调用（跨越相邻层直接依赖）；STY-007-AP2 下层反向依赖上层；STY-007-AP3 「万能工具层」（被全体上层依赖的公共层膨胀为全局耦合点）
- **兼容性**：STY-008(composable)、STY-016(composable)、STY-003(composable)
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：分解单元须归属唯一层级（layer_of 全定义…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集（layer_of/dependency_ru…
- **formal_anchor**：V1(implements)、V3(triggers)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 1 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：层内替换使变更触达面被层边界收敛，抽象级别与关注点对齐
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/交叉表源/人工判断；compatibility: 骨架源；constraints_imposed: 交叉表源/人工判断；anti_patterns: 骨架源/交叉表源/人工判断；formal_anchor: 交叉表源

### STY-008｜六边形（端口-适配器）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.1-六边形（端口-适配器）
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`外部技术替换 → touched_units = |adapters(port)| 且 touched_units(core) = 0（核心不依赖任何外部技术）；成本项 = +|ports| 的接口定义与维护量（间接层成本）`
- **envelope** 可修改性：变更前置时间：`lead_time(核心变更) ≤ verify(core) + regression(adapters)，且 verify(core) 可脱离适配器执行（可测试性↑↑ 的量化落点：核心单测不需要外部设施就绪）`
- **成本**：ops_cost＝无独立运维面；成本落在端口契约维护与适配器测试替身建设｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：STY-008-AP1 端口退化为框架接口的转发（端口未承担翻译职责，核心经端口直接暴露框架语义…；STY-008-AP2 适配器泄漏进核心（核心依赖外部技术类型/异常/设施）
- **兼容性**：STY-016(composable)、STY-014(composable)、STY-015(composable)、STY-007(composable)
- **施加约束** 4 项：方面 2←风格收窄分解策略可行集：核心与外部的边界即分解单元边界候选，端口为 hi…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 8←验证策略适配：核心须存在可脱离适配器执行的测试路径（seam 即端口，0…；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V1(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 20 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：核心可脱离适配器单测（可测试性↑↑）、外部技术可替换（可替换性↑），替换的触达单元数被端口边界收敛
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；compatibility: 骨架源；constraints_imposed: 交叉表源/人工判断；anti_patterns: 人工判断

### STY-009｜整洁/洋葱架构

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.1-整洁/洋葱架构
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`外层技术替换 → touched_units = |外层环上的实现单元| 且 touched_units(内层) = 0（依赖只能指向内层，内层不知道外层）；成本项 = +|环间接口| 的契约维护量`
- **envelope** 可修改性：变更前置时间：`lead_time(领域模型变更) ≤ verify(内层) + regression(外层环)，且 verify(内层) 可脱离外层设施执行（同六边形：核心可独立验证）`
- **成本**：ops_cost＝无独立运维面；成本落在环间契约维护与依赖方向门禁｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：STY-009-AP1 环间接口退化为外层框架接口的转发（内层接口未承担语义翻译）；STY-009-AP2 外层泄漏进内层（内层依赖外层技术类型/设施）
- **兼容性**：STY-016(composable)、STY-014(composable)、STY-015(composable)、STY-007(composable)
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：环边界即分解单元边界候选，依赖方向为单向向内（分…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V1(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 6 [已核验]·metadata_extraction、bib 21 [已核验]·metadata_extraction、bib 22 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：与六边形同族的依赖方向控制收益（内层可独立验证、外层可替换），并以领域模型为中心组织环序
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/人工判断；envelope: 骨架源；cost_profile: 骨架源/人工判断；compatibility: 骨架源；anti_patterns: 骨架源/人工判断

### STY-010｜微内核-插件

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.1-微内核-插件
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`新增扩展 → touched_units = |新增插件单元| + |注册点|，且 touched_units(core) = 0（最小核心不因扩展而变更）；前提：扩展点契约不变——契约变更时该上界失效，改由下一项承载`
- **envelope** 可修改性：典型变更的实现成本（跨边界契约变更数）：`扩展点契约变更 e → contract_changes(e) 的波及面 = |registered_plugins(e)|（「插件全灭」的参数化形态）；核心稳定性 ⇒ contract_changes(extension_point) 须受版本化/兼容策略约束，无策略声明时波及面无上界`
- **成本**：ops_cost＝无独立运维面；成本落在扩展点契约的版本治理与插件兼容性回归｜聚合语义=itemwise
- **反模式** 2 项（P2×2）：STY-010-AP1 扩展点契约不稳定导致插件全灭（契约破坏性变更无版本化/兼容策略）；STY-010-AP2 核心膨胀吞并插件职责
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：核心与插件为两类分解单元，插件职责不得回流核心（…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V4(consumed_by)、V5(implements)
- **参考文献**：bib 1 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：扩展方向的变更被注册机制收敛为『新增插件 + 注册』，核心不动，故 touched_units(core)=0
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；constraints_imposed: 交叉表源/人工判断；anti_patterns: 骨架源；formal_anchor: 交叉表源

### STY-011｜黑板

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.1-黑板
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`新增知识源 ks → touched_units = 1（ks 自身）+ |黑板 schema 登记项|，且 touched_units(既有知识源) = 0（控制由黑板状态驱动，无需改编排方）；前提：知识源间无隐式协议——AP2 成立时该上界失效`
- **envelope** 可观测性：追踪覆盖率：`trace_coverage ≤ 1 − |状态驱动的非确定转移| / |全部控制流转移|（控制流非确定 → 覆盖上界由黑板状态空间规模与知识源触发条件数决定，二者为参数）；可预测性下降的量化落点即该上界`
- **成本**：ops_cost＝无独立运维面；成本落在状态回放设施与触发条件治理｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：STY-011-AP1 黑板变成无结构的垃圾场（写入项无 schema 声明）；STY-011-AP2 知识源间隐式协议（未经黑板 schema 声明的相互假设）
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：分解单元为知识源，其职责须以黑板 schema …；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V4(consumed_by)、V5(implements)
- **参考文献**：bib 1 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：知识源可机会主义增删而无需改动既有知识源（灵活性↑ 的落点 = 变更触达面收敛到 1 个单元 + schema 登记）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 人工判断/骨架源；anti_patterns: 骨架源/人工判断

### STY-012｜MVC 及变体（MVP/MVVM）

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：1.2.1-MVC 及变体（MVP/MVVM）
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`表现层替换 → touched_units = |表现层单元|，且 touched_units(领域) = 0（表现-领域-交互三分 + 单向数据流）；领域逻辑渗入控制器/视图时该上界失效（见 STY-012-AP1）`
- **成本**：ops_cost＝无独立运维面；成本落在表现层构建与前端交付管道｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-012-AP1 领域逻辑渗入控制器/视图
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：表现/领域/交互为三类分解单元，领域规则不得以表…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V1(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 81 [已核验（在线在位：2026-11-07 全文抓取；标题、日期、目录与正文一致；Presentation Model 节覆盖「表现状态外置为可测试模型」、MVP／Passive View 节在正文；作者自述 draft form，仅作模式谱系与结构区分）]·metadata_extraction
- **叙事（收益-成本）**：收益：表现层可替换（触达面收敛到表现单元，领域零触达），交互式界面与领域逻辑的变更率差异被结构吸收
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；anti_patterns: 骨架源；formal_anchor: 人工判断

### STY-013｜管道-过滤器

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.1-管道-过滤器
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`单步变换替换 → touched_units = 1（该过滤器），且 touched_units(其余过滤器) = 0（过滤器无状态、仅经声明的数据流交互）；前提：过滤器间无隐式共享状态——AP1 成立时该上界失效`
- **envelope** 可伸缩性：单位资源增量带来的容量增量：`capacity(r + Δr) − capacity(r) ∝ |可并行的过滤器段|（「可并行↑」的参数化形态：并行度上界 = 管道图中可并行段数）；串行依赖段不随 Δr 增长`
- **成本**：ops_cost＝无独立运维面；成本落在管道调度与批/流作业治理（重跑、补数、背压）｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：STY-013-AP1 过滤器间隐式共享状态；STY-013-AP2 管道内全局错误处理缺失
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：分解单元为过滤器，须无状态且以数据契约（而非共享…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V1(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 1 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：过滤器可独立替换与重用（变更触达面收敛到单个过滤器），无状态假设使可并行段的容量随资源增量线性增长
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；anti_patterns: 骨架源/人工判断；narrative: 人工判断

## 子维度二：部署/运行单元风格

（STY-014–STY-019，共 6 条；kind_profile_STY status=seed）

### STY-014｜单体

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：1.2.2-单体
- **envelope** 延迟分位数 P99：`P99(req) = Σ 单元内调用开销，跨单元网络跳数 = 0（母本：进程内调用，延迟最低）；与 STY-016 的 0.8 下界（跨单元调用约为同进程调用的 10–100 倍）构成对照项；参数：单元内调用路径长度、共享资源竞争`
- **envelope** 可伸缩性：单位资源增量带来的容量增量：`capacity(r + Δr) − capacity(r) 的实现粒度 = 整个部署单元（母本：无独立伸缩）——不存在按单元子集伸缩的容量增量通道；参数：单元副本数、单副本容量、负载分布`
- **envelope** 可用性目标（SLO）：`单个单元级故障的影响面比例 = 1（母本：一次故障全局倒）；SLO 提升通道限于单元级冗余，不含单元内隔离通道；参数：副本数 n、故障域分布、恢复策略（MTTR）`
- **成本**：ops_cost＝单一制品、单一发布通道 → 运维面最小；成本随单元规模上升而在发布编排与故障隔离侧增长｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-014-AP1 单体内部无模块化（大泥球）
- **兼容性**：STY-007(composable)、STY-015(composable)
- **施加约束** 6 项：方面 2←分解可纯逻辑边界（1.4 施→2 单体行）：分解单元不必映射部署单元；方面 3←进程内调用可用（1.4 施→3 单体行）：跨单元契约规则不适用于本风格内…；方面 4←共享数据库可用（1.4 施→4 单体行）：本地事务与 ACID 为默认一…；方面 5←进程内编排、本地事务可用（1.4 施→5 单体行）：不触发分布式协调必答……
- **formal_anchor**：V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction、bib 2 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：进程内调用使延迟项最小、ACID 本地事务可用（一致性成本最低），单一制品使运维面与发布通道最小
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/人工判断；envelope: 骨架源；cost_profile: 骨架源/人工判断；compatibility: 骨架源/人工判断；constraints_imposed: 交叉表源；anti_patterns: 骨架源/人工判断；formal_anchor: 交叉表源

### STY-015｜模块化单体

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：1.2.2-模块化单体
- **envelope** 延迟分位数 P99：`P99(req) = Σ 单元内调用开销，跨单元网络跳数 = 0（「单体的性能优势」：与 STY-014 同型，模块边界不引入网络项）；参数：模块间调用路径长度、边界契约的转发开销`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`模块内变更 → touched_units ≤ |units(m)| + |boundary_contracts(m)|（「接近微服务的可修改性」的参数化落点）；前提：模块边界经 boundary_type 登记且穿透受门禁约束——AP1 成立时该上界退化为 STY-014 形态（无边界收敛）`
- **envelope** 可修改性：典型变更的实现成本（跨边界契约变更数）：`模块 → 部署单元的迁移成本上界 = |boundary_contracts(m)|（「保留未来拆分选项」的参数化落点：拆分红利取决于既有边界契约面，内部无需重切分）；参数：模块间穿透依赖数（AP1 成立时该项发散）`
- **成本**：ops_cost＝单一制品、单一发布通道（与 STY-014 同型）；额外成本落在边界门禁工具与模块级度量建设｜聚合语义=itemwise
- **反模式** 1 项（P0×1）：STY-015-AP1 模块边界只在文档里，代码里随意穿透
- **兼容性**：STY-014(composable)、STY-023(composable)
- **施加约束** 6 项：方面 2←分解可纯逻辑边界（1.4 施→2 单体行），且内部模块边界须强制：模块为…；方面 3←进程内调用可用（1.4 施→3 单体行）；方面 4←共享数据库可用（1.4 施→4 单体行）；方面 5←进程内编排、本地事务可用（1.4 施→5 单体行）…
- **formal_anchor**：V1(implements)、V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction、bib 2 [已核验]·metadata_extraction、bib 23 [已核验]·narrative_only
- **叙事（收益-成本）**：收益：以单体的性能/事务优势（网络跳数 = 0、ACID 可用）换取接近微服务的可修改性（变更触达面被模块边界收敛），并保留未来拆分选项（迁移成本上界 = 边界契约面）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；compatibility: 骨架源；constraints_imposed: 交叉表源/骨架源/人工判断；anti_patterns: 骨架源

### STY-016｜微服务

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.2-微服务
- **envelope** 延迟分位数 P99：`P99(req) ≥ P99_inproc(req) + Σ_{hops ∈ 跨单元路径} network_hop，其中跨单元调用引入的网络延迟项下界约为同进程调用的 10–100 倍（0.8 唯一给定的参数化数值）；参数：调用链跳数、协议、序列化形态`
- **envelope** 可伸缩性：单位资源增量带来的容量增量：`capacity(r + Δr) − capacity(r) 的实现粒度 = 单个服务（0.8：单元可独立伸缩，增益项）；上界 ∝ |可独立伸缩的服务数|；前提：服务间无共享伸缩约束（共享数据库/共享配额时该上界退化为整体粒度）`
- **envelope** 可修改性：变更前置时间：`lead_time(服务内变更) ≤ verify(svc) + deploy(svc)，与其他服务的发布解耦（「独立伸缩/部署↑」的部署侧落点）；跨服务契约变更 → lead_time = Σ_{受影响服务} (verify + deploy)；参数：契约扇出数、消费者驱动契约测试覆盖`
- **成本**：ops_cost＝运维复杂度↑↑（母本原文）：每服务独立发布通道、容量治理、故障演练与基础设施自动化；成本随服务数上升，且 1.3 预算条为分布式基础设施与可…｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：STY-016-AP1 分布式单体（服务间强耦合必须同步部署）；STY-016-AP2 纳米服务（拆分过细）
- **兼容性**：CSL-001(hard_conflict)
- **施加约束** 7 项：方面 2←分解单元必须一一映射部署单元（1.4 施→2 微服务行）；方面 3←跨单元禁止以进程内调用为主手段（1.4 施→3 微服务行）；方面 4←每服务自有数据库为默认（1.4 施→4 微服务行）；方面 5←分布式协调是必答题（1.4 施→5 微服务行）：协调机制须显式选型（编排……
- **formal_anchor**：V2(implements)、V3(triggers)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 4 [已核验]·metadata_extraction、bib 3 [已核验]·metadata_extraction、bib 5 [已核验]·metadata_extraction、bib 9 [已核验]·metadata_extraction、bib 19 [已核验]·case_study、bib 17 [已核验]·narrative_only
- **叙事（收益-成本）**：收益：单元可独立伸缩与独立部署（容量增量粒度 = 单服务，变更前置时间与其他服务解耦）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/交叉表源/人工判断；constraints_imposed: 交叉表源；anti_patterns: 骨架源/人工判断

### STY-017｜SOA

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.2-SOA
- **envelope** 可修改性：典型变更的实现成本（跨边界契约变更数）：`新增/替换参与方 → 跨边界契约变更数 ≤ 1（中介侧路由/转换策略）+ |该参与方自身契约面|，既有参与方内部变更数 = 0（「互操作性↑」的参数化落点：集成点集中于中介）；参数：参与方数、中介路由/转换规则数`
- **envelope** 吞吐量：`throughput(system) ≤ throughput(中介集群)（「中介成为瓶颈」：集中式消息路由/转换使全局吞吐上界由中介容量决定）；参数：中介节点数、消息体量、路由/转换规则复杂度`
- **envelope** 可用性目标（SLO）：`中介单点故障的影响面比例 = 经中介的流量占比（「中介成为单点」）；SLO 提升通道 = 中介集群冗余与故障域分布；参数：中介冗余配置、参与方降级路径`
- **成本**：ops_cost＝中介集群高可用运维 + 集中策略点治理；集中式 → 单点运维压力高（与 STY-005 同型）｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-017-AP1 ESB 承载业务逻辑
- **兼容性**：STY-005(composable)
- **施加约束** 5 项：方面 2←分解单元为服务，服务间交互经中介路由（本行定义「服务化 + ESB/中介…；方面 3←跨单元契约须与中介的路由/转换能力自洽（V2 消费面）；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 9←ESB 承载业务逻辑属守护对象（反模式 → G 规则播种）…
- **formal_anchor**：V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction、bib 2 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：异构系统集成的契约转换集中于中介，新增参与方的跨边界契约变更数被收敛（互操作性↑）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；compatibility: 骨架源/人工判断；constraints_imposed: 交叉表源；anti_patterns: 骨架源/人工判断

### STY-018｜Serverless / FaaS

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.2-Serverless / FaaS
- **envelope** 可伸缩性：单位资源增量带来的容量增量：`capacity 增量由平台自动伸缩承担（无需预留容量）；上界 ∝ 平台伸缩速率与并发配额，伸缩操作时长由平台决定而非本地决策；参数：请求到达率、并发配额、冷启动时长`
- **envelope** 延迟分位数 P99：`P99 ≥ P99_warm + P(cold_start) × cold_start_latency（「冷启动延迟」进入尾延迟）；参数：调用稀疏度、平台预热策略、运行时初始化量`
- **envelope** 性能：资源占用：`闲置期资源占用 = 0（「零闲置成本」的参数化形态）；单次执行时长 ≤ [平台执行时长上界]、并发 ≤ [平台并发配额]（方括号为待勘察平台参数，VG-02/M15）；超限流程不可承载 → 1.2.5 硬冲突（STY-018-AP1）`
- **成本**：ops_cost＝基础设施运维由平台托管（无集群运维面）；成本转移到配额治理、冷启动优化、平台锁定评估与账单侧可观测性｜聚合语义=itemwise
- **反模式** 1 项（P0×1）：STY-018-AP1 长时运行有状态流程
- **兼容性**：STY-003(composable)、CRD-007(hard_conflict)
- **施加约束** 5 项：方面 2←分解单元为函数粒度、以事件触发为入口（本行定义「函数粒度、事件触发」的实…；方面 4←状态外置强制：函数实例不得承载跨调用状态，状态须外置到托管存储/事件日志；方面 5←长时运行有状态流程不可由本风格承载（1.2.5 硬冲突行）→ 须改用其他…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）…
- **formal_anchor**：V2(implements)、V3(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：闲置期资源占用为零、容量增量由平台自动伸缩承担（无需预留与集群运维），事件触发形态与事件驱动通信天然契合
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；compatibility: 骨架源/人工判断；constraints_imposed: 交叉表源/骨架源；anti_patterns: 骨架源/交叉表源

### STY-019｜边缘-中心混合

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：1.2.2-边缘-中心混合
- **envelope** 延迟分位数 P99：`边缘承载的请求：P99 ≥ P99_edge 且不含回源网络项；需回源的请求：P99 ≥ P99_edge + network_hop(edge→center)；整体上界由回源比例决定（「延迟↓」的参数化落点）；参数：边缘节点覆盖、回源比例、边缘侧处理能力`
- **envelope** 性能：资源占用：`回源带宽 = 总流量 × 回源比例（「带宽↓」的参数化落点：边缘处理/聚合把带宽消耗压到回源侧）；参数：边缘聚合率、数据新鲜度要求、缓存策略`
- **成本**：ops_cost＝边缘运维可达性差（母本原文）：节点分散、物理可达性低、更新与故障恢复须远程批量执行；成本随边缘节点数上升｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-019-AP1 边缘节点承担需要全局视图的决策
- **施加约束** 4 项：方面 2←单元到节点映射属本子维度决策面（1.2.2 切分线规则：决策改变部署单元…；方面 4←数据放置须满足合规/数据主权要求（本行定义「按…合规要求…分布」+ 适用…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集（deployed_on 为核心登记面，节点角…
- **formal_anchor**：V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：把响应路径与数据聚合压到边缘，延迟上界不含回源项、回源带宽按回源比例收敛，并满足数据主权类合规要求
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；constraints_imposed: 交叉表源；anti_patterns: 骨架源/人工判断；narrative: 骨架源/人工判断

## 子维度四：风格选择元方法

（STY-020–STY-024，共 5 条；kind_profile_STY status=seed）

### STY-020｜质量属性驱动（风格选择元方法）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：1.2.4-质量属性驱动
- **成本**：ops_cost＝无独立运维面；成本落在属性量化（6.2 六要素场景编写）与映射表的维护/复核｜聚合语义=itemwise
- **兼容性**：STY-021(composable)、STY-024(composable)
- **施加约束** 3 项：方面 6←属性映射与求交结果构成 S4 包络校验的候选集输入；方面 1←产出的四子维度组合须经 1.2.5 冲突矩阵自洽性检查（V3）并走批准路…；方面 10←机器层：映射、求交与 verdict 表入 selection_log …
- **formal_anchor**：V4(triggers)、V5(triggers)
- **参考文献**：bib 12 [已核验（联网核验时间 2026-09-13，Pearson 官方页面）]·metadata_extraction
- **叙事（收益-成本）**：收益：把风格选择从『流行度驱动』转为『目标可达性驱动』——每个质量属性映射到使其可达/受损的风格特征后求交，可行集的每个成员都有属性层面的辩护理由，且产出直接供给 S4 包络校验与 V4
- **数据来源层**（yaml 行内注释）：provenance: 人工判断；typical_reversibility: 人工判断；applicability: 骨架源/人工判断；cost_profile: 人工判断；compatibility: 骨架源；anti_patterns: 骨架源

### STY-021｜约束排除法（风格选择元方法）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：1.2.4-约束排除法
- **成本**：ops_cost＝无独立运维面；成本落在硬约束清单的维护、出处核验与外部强加决策的登记跟踪｜聚合语义=itemwise
- **兼容性**：STY-020(composable)
- **施加约束** 3 项：方面 1←排除以硬约束为限；方面 9←守护规则（P0/P1）属硬约束来源（1.4 接收表方面 9 行，级别硬）…；方面 10←机器层：排除记录入 selection_log（step_log + e…
- **formal_anchor**：V3(implements)、V5(triggers)
- **叙事（收益-成本）**：收益：在硬约束密集的场景下最省认知成本——不必先量化全部质量属性，只需把合规、现状平台、团队能力三类硬约束逐条过筛，剩余即候选
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；cost_profile: 人工判断；formal_anchor: 人工判断

### STY-022｜领域驱动（风格选择元方法）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：1.2.4-领域驱动
- **成本**：ops_cost＝无独立运维面；成本落在领域分解边界的维护与上下文映射的复核（方面 2 变更须触发本方法产出重审）｜聚合语义=itemwise
- **施加约束** 3 项：方面 2←部署与通信结构从方面 2 的领域分解边界导出；方面 1←部署切分线仍按 1.2.2 判定规则（决策改变部署单元数量/单元边界/单…；方面 10←机器层：上下文 → 部署单元候选映射与导出依据入 selection_l…
- **formal_anchor**：V5(triggers)
- **参考文献**：bib 7 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：当领域复杂且方面 2 已给出可信的分解边界时，本方法把风格选择锚定在语义边界上——部署单元与限界上下文对齐可避免跨单元协调成本爆炸（1.4 接收表方面 2 行的理由），且通信结构随上下文映射自然…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；cost_profile: 人工判断

### STY-023｜演进式（风格选择元方法）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：1.2.4-演进式
- **成本**：ops_cost＝切换点重审与迁移执行成本：推迟不等于免除，迁移代价随既成结构固化上升（参数：切换点数量、间隔时长、期间累积的结构耦合）｜聚合语义=itemwise
- **兼容性**：STY-024(composable)、STY-015(composable)
- **施加约束** 3 项：方面 1←默认起点「模块化单体」是 0.10 临时保守通道条件 (i) 的登记默认…；方面 1←被推迟的不可逆决定须附参数化切换点 + LRM + 可推翻指标（CH-B…；方面 10←机器层：切换点、推迟项与可推翻指标入 selection_log（ste…
- **formal_anchor**：V5(triggers)
- **参考文献**：bib 13 [已核验]·metadata_extraction、bib 23 [已核验]·narrative_only
- **叙事（收益-成本）**：收益：在需求不确定性高、团队规模小的场景下，把『错误代价最高、最难逆转』的风格决策（1.1）拆成可回退的小步——从最小可行架构出发，显式预留演化路径与切换点，推迟不可逆决定
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；cost_profile: 人工判断

### STY-024｜模式匹配（风格选择元方法）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：1.2.4-模式匹配
- **成本**：ops_cost＝无独立运维面；成本落在问题特征向量的装配与出处核验、适用条件谓词的求值记录维护｜聚合语义=itemwise
- **兼容性**：STY-020(composable)、STY-023(composable)
- **施加约束** 3 项：方面 1←对 Agent 为强制步骤（纪律一，第 1312 行）：每一个候选必须来…；方面 1←匹配度排序不得替代规程其余步骤：不得增步、跳步、改序、在步骤内引入规程外…；方面 10←机器层：逐候选求值记录与得分入 selection_log / step…
- **formal_anchor**：V5(triggers)
- **叙事（收益-成本）**：收益：把风格选择变成可机器执行的匹配问题——问题特征向量 × 各风格条目的适用条件谓词 → 匹配度排序，使『候选从何而来』有唯一合法答案（注册表条目），从而封死 Agent 凭训练语料流行度自由提案的…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；cost_profile: 人工判断

## kind OWN（源表 4.2.1）

（OWN-001–OWN-004，共 4 条；kind_profile_OWN status=seed；块内按 entry_id 升序）

### OWN-001｜单一所有者（single writer）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：4.2.1-单一所有者（single writer）
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`Δconsumer_set ⊆ consumers(D)：他者经所有者契约访问 → 变更触达单元数上界 |consumers(D)|`
- **envelope** 延迟分位数 P99：`P99_direct(D) ≤ P99_via_repl(D)：直读所有者为最短访问路径，经副本的读路径延迟不优于直读`
- **envelope** 可用性目标（SLO）：`SLO_undocumented → SLO_documented：访问路径契约化（Y2）→ 服务质量承诺可登记可计量`
- **成本**：ops_cost＝随数据集合数量与访问路径契约数上升；无副本一致性运维项，四行中最低｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：OWN-001-AP1 所有权含糊：数据集合的写入责任单元未定案即存在写路径
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y1(implements)、Y2(implements)、W4(consumed_by)
- **叙事（收益-成本）**：收益：语义最简单的所有权形态——写权唯一，一致性协调与访问控制都收敛到所有者单元
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源/人工判断；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### OWN-002｜所有者 + 授权读副本

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：4.2.1-所有者 + 授权读副本
- **envelope** 延迟分位数 P99：`P99_replica(D) ≤ P99_direct(D)：授权读副本为读负载分流 → 读路径延迟不劣于直读所有者`
- **envelope** 可用性目标（SLO）：`freshness_window ≤ Δ_read：副本新鲜度窗口写入数据契约（4.2.1 备注）→ 消费方按声明窗口容忍旧值`
- **envelope** 可修改性：变更前置时间：`read_load_owner ↓：引入副本后所有者单元读负载单调不增 → 变更排期不受读峰值挤压`
- **成本**：ops_cost＝较单一所有者增加副本同步与新鲜度监控运维项；写权仍单点故无跨单元协调项｜聚合语义=itemwise
- **反模式** 1 项（P0×1）：OWN-002-AP1 写权旁落：经授权读副本/物化视图的直写流量
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y1(implements)、Y2(implements)、Y7(triggers)、W4(consumed_by)
- **叙事（收益-成本）**：收益：读负载分流而写权仍单点——一致性协调成本不增，只增副本新鲜度一项契约条款
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### OWN-003｜数据产品

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.1-数据产品
- **envelope** 可用性目标（SLO）：`SLO_declared(D) ∧ monitored(D)：4.2.1 行定义含「SLO」→ SLO 已声明且可计量（未声明 = Y3 同型违例）`
- **envelope** 可修改性：跨边界契约变更数：`|Δcontract_count| ≥ 1：任一语义条款变更须以消费契约变更形态过全部消费方边界 → 变更成本随消费方数放大`
- **成本**：ops_cost＝随消费契约数与消费方数量上升；含发现元数据与 SLO 运营项，4.2.1 四行中最高｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：OWN-003-AP1 空壳产品化：无组织前提的数据产品宣告
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y3(implements)、Y2(implements)、Y7(consumed_by)
- **参考文献**：bib 41 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：把数据集合升级为带所有者团队、SLO、发现元数据与消费契约的产品，异构消费方（分析/ML/运营）可自助接入而不逐一谈判
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源/参考资料源；typical_reversibility: 人工判断；applicability: 骨架源/人工判断/交叉表源；constraints_imposed: 交叉表源；references: 参考资料源

### OWN-004｜共享写（治理例外）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：4.2.1-共享写（治理例外）
- **envelope** 可修改性：变更前置时间：`lead_time_exit ≤ deadline：退出计划的执行前置时间不晚于最后负责时刻（CH-B 参数化切换点）`
- **envelope** 可用性目标（SLO）：`now ≤ deadline ∨ escalation_filed：到期未迁移 → 升级裁决（Y8 原文界形）`
- **成本**：ops_cost＝随共享写单元数与过渡期时长上升；含升级裁决通道与到期告警维护｜聚合语义=itemwise
- **反模式** 2 项（P0×2）：OWN-004-AP1 常态化共享写：过渡期外的多单元写同一存储；OWN-004-AP2 共享写例外超期：到期未迁移且未升级裁决
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y1(consumed_by)、Y8(implements)、W4(consumed_by)
- **叙事（收益-成本）**：收益：遗留迁移过渡期内唯一合法的多写形态，为物理迁移换取时间（0.11 现状锁定 + 4.6 示例一：逻辑所有权先行、物理迁移推迟）
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源；typical_reversibility: 人工判断；applicability: 骨架源/人工判断/交叉表源；constraints_imposed: 交叉表源；narrative: 骨架源

## kind CSL（源表 4.2.3）

（CSL-001–CSL-005，共 5 条；kind_profile_CSL status=seed；块内按 entry_id 升序）

### CSL-001｜强一致

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：4.2.3-强一致
- **envelope** 可修改性：变更前置时间：`lead_time(跨单元强一致需求) ≥ lead_time(saga_candidate) ∨ lead_time(reopen(aspect1))：Y6 冲突信号的两条处置路径（Saga + 业务补偿，或回溯方面 1 重审部署风格）→ 变更前置时间以两路径较长者为下界，不设默认协调轮次`
- **envelope** 可用性目标（SLO）：`declared(consistency_level(D)) ∧ declared(consistency_rationale(D)) → SLO 判定面完整：级别与业务语义论证写入数据契约语义条款（4.2.3 降级纪律）→ 一致性目标可计量可校验（Y3 三合取项的落点）`
- **成本**：ops_cost＝随参与协调的单元数上升；跨单元形态为五行中最高——Y6 冲突信号即其代价的形式化表达｜聚合语义=itemwise
- **反模式** 1 项（P0×1）：CSL-001-AP1 跨单元强一致作为默认一致性手段（4.2.3 降级纪律禁项 (i) 全局强…
- **兼容性**：STY-016(hard_conflict)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y3(implements)、Y6(triggers)、V3(consumed_by)、W4(consumed_by)
- **叙事（收益-成本）**：收益：语义最强——线性化与写后读保证使并发推理退化为顺序推理，业务硬规则可在存储层直接成立（4.6 示例二：预扣使超卖在存储层不可能）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源/人工判断；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### CSL-002｜会话一致

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.3-会话一致
- **envelope** 延迟分位数 P99：`P99_ryw(D) ≤ P99_write(D) + Δ_route：写后读路由主副本 → read-your-writes 的读路径延迟界＝写确认延迟加路由开销，无全序广播项`
- **envelope** 可修改性：变更前置时间：`lead_time(级别争议返工) ↓：业务语义论证在声明时点前置完成并写入数据契约语义条款 → 窗口期语义争议不在实现期返工（4.2.3 降级纪律的论证义务落点）`
- **成本**：ops_cost＝随实现手段上升：粘性会话 < 写后读路由主副本 < 版本向量（4.3 交付空间驱动：DBA 能力限定版本向量类机制的可行集）｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：CSL-002-AP1 实现手段缺位：声明会话一致但三种手段（粘性会话/版本向量/写后读路由主副…
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y3(implements)
- **叙事（收益-成本）**：收益：以最小机制满足『客户端读到自己刚写的值』——交互体验硬需求处的最小充分级别（4.2.3 选择条件列），无须全序广播或跨单元协调，读路径延迟界＝写确认延迟加路由开销
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### CSL-003｜因果一致

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.3-因果一致
- **envelope** 可修改性：变更前置时间：`lead_time(消费者接入) ≤ lead_time(基线)：因果序元数据（逻辑时钟）与流分区键设计在写路径一次建成 → 后续消费者接入不追加写路径改造，变更触达单元数不增`
- **envelope** 可用性目标（SLO）：`顺序保证覆盖全部有因果序的写对 → 协作/社交类语义的可用界由偏序一致性承载，无全序协调项（SLO 判定面＝乱序可检出）`
- **成本**：ops_cost＝随写路径元数据与分区键设计复杂度上升；读侧无协调项；4.3 交付空间驱动：DBA 能力限定其可行集｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：CSL-003-AP1 因果序元数据未随写路径登记（声明因果一致而实现手段缺位）
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y3(implements)
- **叙事（收益-成本）**：收益：有因果序的写对所有观察者顺序一致——协作/社交类语义的最小充分级别（4.2.3 选择条件列），比强一致便宜（只需偏序追踪，无需全序协调），比会话一致强（覆盖跨观察者顺序）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### CSL-004｜最终一致

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.3-最终一致
- **envelope** 可用性目标（SLO）：`窗口时长 ∈ 数据契约新鲜度字段 → 收敛窗口可计量：消费者按声明窗口容忍旧值，SLO 判定面＝窗口违约可检出（无协调收敛的服务质量界）`
- **envelope** 可修改性：变更前置时间：`lead_time(级别争议返工) ↓：业务语义论证（消费者窗口期读到旧值的业务后果）在声明时点前置完成并写入数据契约语义条款 → 窗口期争议不在实现期返工`
- **成本**：ops_cost＝五行中最低（无协调项）；但须承担对账与补偿设计成本（缺此即为 STY-016 的第三项失效形态）｜聚合语义=itemwise
- **反模式** 1 项（P0×1）：CSL-004-AP1 最终一致万能幻觉：声明最终一致而无业务语义论证（窗口时长亦未入新鲜度条款…
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y3(implements)
- **参考文献**：bib 39 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：无协调收敛——跨单元默认级别（4.2.3 选择条件列），可用性与分区容忍最好，异步复制与事件传播的实现面最轻，ops_cost 为五行最低
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CSL-005｜补偿一致（业务级）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：4.2.3-补偿一致（业务级）
- **envelope** 可用性目标（SLO）：`终态可达界 = ∧_{补偿步} 可执行补偿：∀ 补偿步有出路（Z3 同型）→ 长流程终态正确的服务质量界；预扣超时自动释放使可见性损失有界（4.6 示例二的下限合法性来源）`
- **envelope** 可修改性：变更前置时间：`lead_time(长流程变更) ≥ lead_time(补偿步重验)：补偿语义一经流程消费即形成业务依赖 → 变更须逐步重验补偿动作与幂等性（Z3），前置时间以补偿步数为下界`
- **成本**：ops_cost＝随补偿步数与参与单元数上升；须承担补偿编排正确性的验证成本（Z3 每步有出路）｜聚合语义=itemwise
- **反模式** 1 项（P0×1）：CSL-005-AP1 补偿步无幂等设计（可补偿步缺幂等 → 重试放大）
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y3(implements)、Y6(implements)、Z3(consumed_by)
- **参考文献**：bib 36 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：全局原子性不可得时唯一能达成终态正确的形态（4.2.3 定义列）——以 Saga（方面 5）与预扣/预留模式把原子性从存储层移到业务层，同时是 Y6 冲突信号的正向出路（saga_candida…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

## kind CRD（源表 5.2.1、5.2.2）

（CRD-001–CRD-008，共 8 条；kind_profile_CRD status=seed；块内按 entry_id 升序）

### CRD-001｜编排（orchestration）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：5.2.1-编排（orchestration）
- **envelope** 可观测性：追踪覆盖率：`追踪覆盖率（编排流程） ≥ 追踪覆盖率（无中央协调形态） → 编排者提供单一集中观测点（5.2.1 质量影响列「可观测性集中」），覆盖率单调优于协同形态`
- **envelope** 延迟分位数 P99：`P99（流程） = Σ 各步骤卡片 latency_budget_delta + 步骤自身业务耗时 + 编排者跳数开销（5.2.5 Σ 消费路径）→ 每跳经编排者中转，延迟随步骤数单调不增下界为直连形态`
- **envelope** 可用性目标（SLO）：`可用性（流程） ≤ min（编排者可用性, ∧ 各参与者可用性） → 编排者是新增单点，其可用性构成流程可用性的上界（Z8 要求状态持久化 ∧ 崩溃可恢复以缓解）`
- **成本**：ops_cost＝随编排者实例数与流程步骤数上升；须承担编排者单点的高可用部署与状态持久化运维成本（Z8）｜聚合语义=additive
- **反模式** 2 项（P0×1／P1×1）：CRD-001-AP1 协调者状态未持久化即承载长流程（崩溃即流程丢失）；CRD-001-AP2 以编排承载步骤少而稳定的流程（无谓引入中央组件）
- **兼容性**：STY-014(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z1(implements)、Z8(implements)、X1(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 44 [已核验]·metadata_extraction、bib 45 [已核验]（2026-09-20 在线复核在位；本文本地无存档，二分内容由书目 4《Building Microservices》第 2 版第 4 章本地承载，编译提取以书目 4 为本地来源——母本 5.7 逐字，不得在注册表侧降级为存疑/narrative_only）·metadata_extraction
- **叙事（收益-成本）**：收益：步骤多且需集中留痕的流程获得单一集中观测点（5.2.1 质量影响列「可观测性集中」），追踪覆盖率单调优于协同形态
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CRD-002｜协同（choreography）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：5.2.1-协同（choreography）
- **envelope** 可修改性：跨边界契约变更数：`跨边界契约变更数（协同） ≥ min（各单元事件契约变更数） → 无中央协调点可吸收变更，各方事件契约独立演进但互相构成下界（5.2.1 质量影响列「耦合度低」的代价面）`
- **envelope** 可观测性：追踪覆盖率：`追踪覆盖率（协同流程） ≤ 追踪覆盖率（中央协调形态） → 可观测性分散（5.2.1 质量影响列），覆盖率上界受限于跨单元追踪链的可拼接性`
- **envelope** 可用性目标（SLO）：`可用性（协同流程） 单调不增于中央协调形态 → 无编排者单点，可用性界由 ∧ 各参与者可用性给出，单调优于编排形态`
- **成本**：ops_cost＝随订阅方数量上升；须承担事件回放与乱序注入的常态化验证成本（5.4 施→8：事件驱动 → 必备）｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：CRD-002-AP1 异步交互未声明投递语义，或投递语义非至多一次而消费端未声明幂等；CRD-002-AP2 以协同承载步骤多或需集中留痕的流程（流程隐式化不可维护）
- **兼容性**：STY-003(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z1(implements)、Z2(implements)、X1(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 44 [已核验]·metadata_extraction、bib 45 [已核验]（2026-09-20 在线复核在位；本文本地无存档，二分内容由书目 4《Building Microservices》第 2 版第 4 章本地承载，编译提取以书目 4 为本地来源——母本 5.7 逐字，不得在注册表侧降级为存疑/narrative_only）·metadata_extraction
- **叙事（收益-成本）**：收益：各单元自治演进、无中央单点，可用性界由 ∧ 参与者给出而单调优于编排形态（5.2.1 质量影响列「耦合度低」）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CRD-003｜同步调用链

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.1-同步调用链
- **envelope** 延迟分位数 P99：`Σ timeout_budget（path） ≤ sla_bound（path） ∧ ∀ 相邻级: t_downstream < t_upstream − propagation（Z4 逐字界形）→ 链延迟按跳加和，超时预算必须闭合且不得倒挂`
- **envelope** 可用性目标（SLO）：`可用性（链） = Π 各跳可用性 → 单调不增于链深（每增一跳乘一因子），链深是可用性的直接决定量`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`sync_chain_depth（F） ≤ registered_max_depth（Z5 软界） → 链深越阈为 P2 漂移信号，越阈 + 趋势上升双判据方告警`
- **成本**：ops_cost＝随链深上升；须承担超时值治理与链深漂移观测的常态成本（Z4/Z5）｜聚合语义=additive
- **反模式** 2 项（P1×1／P2×1）：CRD-003-AP1 链深超注册上限而无漂移观测（越阈 + 趋势双判据缺失）；CRD-003-AP2 超时预算不闭合或相邻级超时倒挂
- **兼容性**：STY-001(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z5(implements)、Z1(implements)、Z4(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 44 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：调用方获得即时结果，语义最简、无需引入中央协调组件或事件基础设施
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CRD-004｜混合（宏观编排 + 微观协同）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：5.2.1-混合（宏观编排 + 微观协同）
- **envelope** 可观测性：追踪覆盖率：`追踪覆盖率（混合流程） = min（宏观编排侧覆盖率, 微观协同侧覆盖率） + 边界项 → 并集口径下覆盖率由较弱一侧决定（5.2.1 质量影响列「两种卡片的并集」）`
- **envelope** 可修改性：跨边界契约变更数：`跨边界契约变更数（混合） ≥ 跨边界契约变更数（宏观侧） + 跨边界契约变更数（边界处） → 边界划分新增契约登记面（5.4 施→3：编排者与参与者间的命令契约、事件契约）`
- **envelope** 延迟分位数 P99：`P99（混合流程） = Σ 宏观侧步骤卡片 latency_budget_delta + Σ 微观侧事件投递延迟 → 两侧按各自聚合语义加和（5.2.5 Σ 消费路径）`
- **成本**：ops_cost＝为两种形态运维成本之和并加边界治理成本；须同时承担编排者高可用（Z8）与事件回放/乱序注入验证（5.4 施→8）｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：CRD-004-AP1 跨域主流程未集中留痕（合规域落在微观协同侧）；CRD-004-AP2 边界处契约密度不足（隐式跨域时序假设）
- **兼容性**：STY-003(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z1(implements)、Z8(implements)、X1(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 44 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：合规域的集中留痕与开放域的单元自治可同时满足（5.2.1 适用条件列），避免为全域统一形态而在某一侧付出过高代价
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CRD-005｜Saga（编排式）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：5.2.2-Saga（编排式）
- **envelope** 可用性目标（SLO）：`终态可达界 = ∧_{步骤} 有出路：∀ saga step: step_class ∈ {compensable, retriable, pivot} ∧ (compensable → ∃ compensation ∧ idempotent) ∧ pivot_ordering_valid（Z3 逐字界形）→ 长流程终态正确的服务质量界`
- **envelope** 延迟分位数 P99：`P99（Saga） = Σ 各步骤卡片 latency_budget_delta + 步骤自身业务耗时 + 逆序补偿上界（∃ 失败时按 pivot 逆序逐步补偿）→ 补偿路径的延迟不劣于正向路径（5.2.5 Σ 消费路径）`
- **envelope** 可修改性：变更前置时间：`lead_time（流程变更） ≥ lead_time（需重判步骤的重分类） → 步骤三分类一经定案即约束补偿动作与关键步排序（Z3），变更前置时间以需重判步骤数为下界`
- **成本**：ops_cost＝随步骤数与补偿分支数上升；须承担补偿编排正确性的验证成本与 Saga 日志的对账运维（Z3 每步有出路）｜聚合语义=additive
- **反模式** 3 项（P0×3）：CRD-005-AP1 步骤三分类不明即上线（compensable/retriable/piv…；CRD-005-AP2 可补偿步缺补偿动作，或补偿动作非幂等；CRD-005-AP3 编排器状态或 Saga 日志未持久化
- **兼容性**：CSL-005(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z3(implements)、Z8(implements)、Y6(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 47 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：跨单元长流程在全局原子性不可得时达成终态正确（4.2.3 定义列），是 Y6 冲突信号的正向出路（saga_candidate）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CRD-006｜Saga（协同式）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：5.2.2-Saga（协同式）
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`步骤数（Saga） ≤ 注册上限（5.2.2 关键设计规则列，默认 ≤4） → 越阈即流程隐式化不可维护；与 Z5 registered_max_depth 同源词汇、不同谓词面（MJ-19）`
- **envelope** 可用性目标（SLO）：`终态可达界 = ∧_{步骤} 有出路：∀ saga step: step_class ∈ {compensable, retriable, pivot} ∧ (compensable → ∃ compensation ∧ idempotent) ∧ pivot_ordering_valid（Z3 逐字界形）→ 无中央协调者，终态可达由各单元补偿事件的合取给出`
- **envelope** 可观测性：追踪覆盖率：`追踪覆盖率（协同式 Saga） ≤ 追踪覆盖率（编排式 Saga） → 无集中留痕（5.2.2 关键设计规则列），覆盖率上界受跨单元事件链可拼接性限制`
- **成本**：ops_cost＝随参与单元数上升；须承担事件回放与乱序/重复/丢失注入的常态化验证成本（5.4 施→8：事件驱动 → 必备），且无集中留痕使故障定位成本高于…｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：CRD-006-AP1 以协同式承载步骤多或需集中留痕的流程（流程隐式化不可维护）；CRD-006-AP2 补偿事件未声明投递语义，或消费端未声明幂等
- **兼容性**：STY-003(requires)、CSL-005(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z3(implements)、Z2(implements)、Z5(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 47 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：各单元自治推进补偿、无中央协调者单点，可用性界由各单元合取给出
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CRD-007｜流程管理器（process manager）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：5.2.2-流程管理器（process manager）
- **envelope** 延迟分位数 P99：`P99（流程） = Σ 各步骤卡片 latency_budget_delta + 人工步骤超时上界 → 人工步骤的超时值构成延迟预算的主导项；并行分支的聚合式母本未给（5.2.5 只给 Σ 语义）→ 本条目不本地补充（MJ-19）`
- **envelope** 可修改性：变更前置时间：`lead_time（流程变更） ≥ lead_time（状态机状态数变更的重验） → 状态机显式建模使变更触达面可数，前置时间以状态数为下界（含在途实例迁移）`
- **envelope** 可用性目标（SLO）：`Σ timeout_budget（path） ≤ sla_bound（path） ∧ ∀ 相邻级: t_downstream < t_upstream − propagation（Z4 逐字界形）→ 人工步骤超时值必须纳入预算闭合，不得倒挂`
- **成本**：ops_cost＝为编排式之上再加人工步骤治理成本（超时值、代理规则、值班升级通道）；在途实例迁移使版本升级成本高于 CRD-001｜聚合语义=additive
- **反模式** 3 项（P0×1／P1×2）：CRD-007-AP1 长时运行有状态流程落在函数粒度的平台托管单元（STY-018-AP1 的…；CRD-007-AP2 人工步骤无超时值与代理规则（流程无限期挂起）；CRD-007-AP3 状态机未显式建模即承载分支/并行流程
- **兼容性**：STY-018(hard_conflict)、CRD-005(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z3(implements)、Z8(implements)、Z4(consumed_by)、V3(consumed_by)、Z7(consumed_by)
- **叙事（收益-成本）**：收益：编排式 Saga 的泛化（5.2.2 定义列），把人工步骤、分支与并行纳入同一状态机，流程状态集中且可验证（Z1 显式建模的落点）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源；anti_patterns: 交叉表源

### CRD-008｜预扣/预留（reservation）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.2-预扣/预留（reservation）
- **envelope** 可观测性：追踪覆盖率：`可见性损失窗口 ≤ 预扣超时值 → 超时自动释放使窗口有界（4.6 示例二的下限合法性来源：预扣使超卖在存储层不可能 ∧ 可见性损失有界）`
- **envelope** 延迟分位数 P99：`P99（预扣 + 确认/释放） = 两次本地原子操作之和 → 无跨单元事务协调开销，延迟界优于分布式提交形态（5.2.5 Σ 消费路径的两步特例）`
- **envelope** 可修改性：跨边界契约变更数：`预扣超时值变更 ≥ 1 项跨边界契约变更 → 超时值是契约条款而非实现细节（4.6 示例二），变更须触及资源消费方`
- **成本**：ops_cost＝随预扣资源种类上升；须承担泄漏巡检与对账的常态成本（5.2.2 关键设计规则列「防泄漏」）｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：CRD-008-AP1 预扣无超时自动释放（资源泄漏）；CRD-008-AP2 预扣超时值留在实现里而不入契约条款
- **兼容性**：CSL-005(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z3(implements)、Y6(consumed_by)、Z4(consumed_by)、Z7(consumed_by)
- **叙事（收益-成本）**：收益：在存储层排除超卖而不需跨单元原子提交（4.6 示例二的下限合法性来源：预扣使超卖在存储层不可能 ∧ 可见性损失有界），延迟界为两次本地原子操作之和，优于分布式提交形态
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

## kind DEC（源表 2.2.1）

（DEC-001–DEC-008，共 8 条；kind_profile_DEC status=seed；块内按 entry_id 升序）

### DEC-001｜S1 按业务领域

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：2.2.1-S1 按业务领域
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`触达单元数（典型领域变更） ≤ 1 → 限界上下文内聚使单侧领域变更不跨单元传播；> 1 即语义边界划错的反向信号（2.2.2 语义边界判据）`
- **envelope** 可修改性：DSM 密度（2.2.4 通道二的消费端之一）：`cross_density（DSM） ≤ 注册阈值 → 阈值是 2.2.4 的注册参数（2.6 示例一消费字段『DSM.cross_density 阈值』）；越阈则按 2.6 示例一走组合冲突处置，单调越阈即界外`
- **envelope** 可修改性：变更前置时间：`变更前置时间 随跨边界契约变更数单调不减 → 上下文映射（2.4 施→3 硬）是前置时间的支配项，下界为单上下文内变更`
- **成本**：ops_cost＝随限界上下文数上升：每上下文的独立验证与部署面带来运维单元数增长；单元数与认知负荷上限的联合可行性须先校验（2.6 示例三）｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：DEC-001-AP1 语义边界不清即以 S1 切分（切出的『上下文』不能独立陈述领域语义）；DEC-001-AP2 按流程步骤而非『什么会变』切分（信息隐藏判据违例）
- **兼容性**：DEC-006(tension)、DEC-002(tension)
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W1(consumed_by)、W2(consumed_by)、W3(consumed_by)、W7(consumed_by)、W5(consumed_by)、X1(consumed_by)
- **参考文献**：bib 7 [已核验]·metadata_extraction、bib 24 [已核验（联网核验时间 2026-09-13）；出版形态澄清：Leanpub 迭代出版无单一出版年——官方页面最新更新 2021-08-26（416 页），著录出版年以引用时所据版本为准；本地资源＝resources/se《Introducing EventStorming - Alberto Brandolini - 20190823.pdf》345 页，2026-09-15 内容核验]·metadata_extraction
- **叙事（收益-成本）**：收益：领域复杂度高的系统获得与业务语言对齐的语义边界（2.2.1 定义列），典型领域变更的触达单元数上界为 1，跨边界契约变更数随之收敛
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### DEC-002｜S2 按技术层次

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：2.2.1-S2 按技术层次
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`触达单元数（典型业务变更） ≥ 2 → 纯技术分层使单个业务变更纵切多层，触达单元数下界高于语义边界形态（2.2.2 语义边界判据的对比结论），单调高于 S1/S3`
- **envelope** 可修改性：变更前置时间：`变更前置时间 随跨边界契约变更数单调不减 → 层间契约变更须各层同步，上界由跨层协调节奏决定（6.2.1 可修改性行度量方式）`
- **成本**：ops_cost＝风格为单体时 S7 退化、分解可纯逻辑（2.4 接收约束方面 1 行）→ 层次单元通常合并于同一部署单元，运维单元数增量低于按部署边界切分的…｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：DEC-002-AP1 领域复杂度高时以技术分层为唯一主策略（纵切变更放大）；DEC-002-AP2 层间边界未即契约边界（切割既有契约）
- **兼容性**：DEC-001(tension)
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W1(consumed_by)、W2(consumed_by)、W3(consumed_by)、W7(consumed_by)、X1(consumed_by)
- **叙事（收益-成本）**：收益：关注点分离直接落地为单元边界（2.2.1 主导驱动空间列），层间依赖规则可由 dependency_rule / layer_of 谓词机器判定（2.5），守护成本低
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### DEC-003｜S3 按业务能力

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：2.2.1-S3 按业务能力
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`触达单元数（典型能力变更） ≤ 1 → 能力项内聚；> 1 时以 2.2.3 准则三判定粒度（interface_cost(M) > cohesion_gain(M) → tech_debt_flag(M)，W6 软），单调越阈即粒度失当`
- **envelope** 可修改性：DSM 密度（2.2.4 通道二的消费端之一）：`cross_density（DSM） ≤ 注册阈值 → 越阈即能力项划分与真实依赖结构错位（2.2.4 通道二消费端），按 2.6 示例一同型处置组合冲突`
- **成本**：ops_cost＝定义列『粒度可粗可细』是运维单元数不确定的主要来源 → 须先以 2.2.3 停止准则（W2 硬 / W3 条件硬 / W6 软）收敛，再估运…｜聚合语义=itemwise
- **反模式** 2 项（P0×2）：DEC-003-AP1 以能力项包含关系替代能力编排（跨单元协调隐式化）；DEC-003-AP2 业务能力地图粒度不一致即切分（单元无可测试接口）
- **兼容性**：DEC-004(tension)
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W1(consumed_by)、W2(consumed_by)、W3(consumed_by)、W7(consumed_by)、W4(consumed_by)、W6(consumed_by)、X1(consumed_by)、Z1(consumed_by)
- **叙事（收益-成本）**：收益：单元边界直接使用业务语言（2.2.1 定义列「比 S1 更贴业务语言」），与业务方书面目标（6.2.1 四类合法出处之一）天然对齐，目标值出处门槛易过
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### DEC-004｜S4 按数据归属

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：2.2.1-S4 按数据归属
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`|{M : owned_by(M, d)}| = 1（W4，∀ data d）→ 数据变更的触达单元数上界为 1（所有者单元）；≥ 2 即 W4 违例，触达单元数无上界`
- **envelope** 可修改性：DSM 密度（2.2.4 通道二的消费端之一）：`cross_density（DSM） 随跨所有者数据访问数单调不减 → 归属定案后跨边界数据依赖应单调不增；不降即归属划错（2.4 施→4）`
- **成本**：ops_cost＝数据迁移是主要运维成本项：拆分序列须按数据迁移可行性排序（2.4 接收约束方面 4 行），迁移窗口内须承担双写与对账；归属定案后运维面按所有…｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：DEC-004-AP1 同一数据集合出现两个所有者单元；DEC-004-AP2 现状数据不可干净归属时仍按 S4 强切（拆分序列不按迁移可行性排序）
- **兼容性**：DEC-003(tension)
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W4(implements)、W1(consumed_by)、W2(consumed_by)、W3(consumed_by)、W7(consumed_by)、Y1(consumed_by)
- **叙事（收益-成本）**：收益：唯一直接操作化 W4 的策略（2.4 施→4 明文「即 W4」），数据变更的触达单元数上界为 1，跨边界数据依赖单调不增
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### DEC-005｜S5 按变更频率

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：2.2.1-S5 按变更频率
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`触达单元数（高频变更） ≤ 1 → 高频逻辑已隔离；≥ 2 即分离失效，且触达单元数随易变点扩散单调不增方为合格`
- **envelope** 可修改性：变更前置时间：`稳定单元的变更前置时间 单调不增于分离前 → 分离不得把易变性成本转嫁给稳定单元（2.2.2 信息隐藏判据的反面）；下界为单一易变点内变更`
- **成本**：ops_cost＝易变性分离的运维成本主要是可推翻指标的持续治理：注册假设值、按窗口观测漂移、越阈即立案重审（2.6 示例二）；母本未给成本量化式 → 方括号…｜聚合语义=itemwise
- **反模式** 2 项（P1×1／P2×1）：DEC-005-AP1 易变性评估缺失或无出处仍按 S5 切分（把 unknown 当作 fal…；DEC-005-AP2 保守界假设被实测推翻但未立案重审（可推翻指标失效）
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W1(consumed_by)、W2(consumed_by)、W3(consumed_by)、W7(consumed_by)
- **参考文献**：bib 15 [已核验]·metadata_extraction、bib 14 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：八策略中唯一以『什么会变』为主驱动的策略（2.2.2 信息隐藏行明文「S5 正是此判据的操作化」），高频变更的触达单元数上界为 1，稳定单元免于易变性波及
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### DEC-006｜S6 按团队认知负荷

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：2.2.1-S6 按团队认知负荷
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`cognitive_load(M) ≤ capacity(team(M))（W3，容量证据充分时为硬）→ 单元规模上界由承载团队容量给出；证据不足时上界为注册表登记的保守上限（2.2.3 准则二 CH-B1：单元对外接口数与职责陈述数不超过注册的保守上限）`
- **envelope** 可修改性：变更前置时间：`变更前置时间 随跨团队协调数单调不减 → 单元边界对齐团队边界时跨团队协调数取下界；未对齐即前置时间的支配项转为组织协同（G-ENV-1 映射理由：认知负荷在 6.2.1 无独立指标族，其可观测落点为前置时间的支配项＝跨团队协调数，DSM 依赖种类含 team，2.2.4）`
- **成本**：ops_cost＝单元数与团队数强绑定 → 组织变动即架构变动（Conway 面）；2.6 示例三明示联合不可行时的三个出路（增团队/合并上下文/豁免物理隔离…｜聚合语义=itemwise
- **反模式** 2 项（P1×2）：DEC-006-AP1 容量证据充分时单元规模超出承载团队认知负荷（W3 硬化分支违例）；DEC-006-AP2 单元数与团队容量联合不可行仍推进（未在方面 8 可行性校验发阻塞声明）
- **兼容性**：DEC-001(tension)
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W3(implements)、W1(consumed_by)、W2(consumed_by)、W7(consumed_by)
- **参考文献**：bib 9 [已核验]·metadata_extraction、bib 17 [已核验]·narrative_only
- **叙事（收益-成本）**：收益：唯一以交付空间为主导驱动的策略（2.2.1 主导驱动空间列），且是所有策略的过滤器（2.3 交付空间驱动第一行）——任何策略产出的单元规模都须过本条
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### DEC-007｜S7 按部署边界

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：2.2.1-S7 按部署边界
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`部署单元数 = 分解单元数（一一映射，2.4 接收约束方面 1 行）→ 触达单元数（典型变更） ≤ 1 时不产生跨部署单元的契约变更；≥ 2 即映射错位，跨边界契约变更数随错位面单调不减`
- **envelope** 可修改性：DSM 密度（2.2.4 通道二的消费端之一）：`cross_density（DSM，deploy 类依赖） ≤ 注册阈值 → 部署单元间的双向依赖（反馈环）暴露跨单元耦合（2.2.4：非对角区块暴露反馈环；依赖种类含 deploy），一一映射下应单调不增`
- **成本**：ops_cost＝运维单元数 = 部署单元数（一一映射）→ 每单元的独立发布、回滚与监控面为固定成本项；单元数增长须与团队容量联合校验（2.6 示例三：团队容…｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：DEC-007-AP1 微服务风格下分解单元与部署单元错位（分布式单体/纳米服务）；DEC-007-AP2 单体风格下仍强制物理拆分（S7 退化分支被误用为强制）
- **兼容性**：STY-016(composable)
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W1(consumed_by)、W2(consumed_by)、W3(consumed_by)、W7(consumed_by)
- **叙事（收益-成本）**：收益：单元与部署单元一一映射，消除部署单元与语义单元错位（2.4 接收约束方面 1 行理由列：错位是分布式单体/纳米服务的根源），独立部署与独立发布的边界天然清晰
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### DEC-008｜S8 按风险

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：2.2.1-S8 按风险
- **envelope** 合规：监管条款 → 可判定谓词的映射覆盖率：`隔离单元的未映射监管条款数 = 0（全量映射为可判定谓词，6.2.1 合规族指标）；> 0 即更强验证面不完整，且映射覆盖率单调不减（不得以豁免降低）`
- **envelope** 安全：攻击面清单闭合率、漏洞修复时限、敏感数据访问路径合规率：`敏感数据访问路径合规率 上界为 1（全量合规，Y5 联动）；攻击面清单闭合率单调不减 → 隔离后攻击面不得跨单元扩散（6.2.1 安全族度量方式：静态扫描、渗透测试、Y5 联动）`
- **成本**：ops_cost＝独立隔离单元带来独立验证、独立发布与独立运维面 → 运维单元数增长；2.6 示例三明示单元数与团队容量的联合可行性须先校验，不可行时发 CH…｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：DEC-008-AP1 高风险/合规关键子系统未隔离成独立单元，致更强验证无独立执行面；DEC-008-AP2 合规条款未映射为可判定谓词即以『已合规』结案
- **施加约束** 7 项：方面 1←分解边界候选 → 部署单元风格可行集（对偶回馈：语义边界不清晰时分布式风…；方面 3←分解边界 = 契约边界；方面 4←分解边界 = 数据所有权边界（每个数据集合有且仅有一个所有者单元，即 W…；方面 5←单元内编排自由…
- **formal_anchor**：W1(consumed_by)、W2(consumed_by)、W3(consumed_by)、W7(consumed_by)
- **叙事（收益-成本）**：收益：唯一以风险画像为主导驱动的策略（2.2.1 主导驱动空间列），高风险/高保障子系统获得独立验证面与更强验证（2.3 问题空间驱动第三行明文「S8 强制隔离 + 强化验证（与方面 8 联动）」）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

## kind CTR（源表 3.2.1、3.2.2）

（CTR-001–CTR-012，共 12 条；kind_profile_CTR status=seed；块内按 entry_id 升序）

### CTR-001｜进程内接口

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：3.2.1-进程内接口
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`接口变更触达的调用方单元数 上界 = 该接口内部调用方集合的基数；跨边界契约变更数 = 0（3.2.1 适用条件列限定于模块边界与单元内部）→ > 0 即本形态被越界使用（3.4 接收约束方面 1 行：微服务 → 跨单元禁止以进程内调用为主手段）`
- **envelope** 性能：延迟分位数（P50/P99，P99 = 延迟分布第 99 百分位数）：`进程内调用的延迟增量 下界为 0（无网络往返与跨进程序列化项）；同接口 P99 随调用方数量单调不减 → 跨单元延迟预算项归属方面 1 风格包络，本条不重复计入（0.8）`
- **成本**：ops_cost＝无独立运维面——进程内接口不产生独立部署/独立监控单元，运维成本随所属单元计入（0.8 包络不重复计项）｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：CTR-001-AP1 跨单元以进程内调用为主手段（分布式单体信号）；CTR-001-AP2 接口面未经静态分析提取即声称无契约面（机器层盲区充作不存在）
- **兼容性**：STY-016(hard_conflict)、STY-014(composable)、STY-015(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：W1(implements)、X1(consumed_by)、X2(consumed_by)、X6(consumed_by)
- **叙事（收益-成本）**：收益：延迟增量下界为 0（无网络往返与跨进程序列化），机器层可由静态分析直接提取，且与方面 2 的 seam 谓词同源（3.2.1 定义列）→ 0.9 双层表达无需双重维护
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-002｜同步 API 契约

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：3.2.1-同步 API 契约
- **envelope** 性能：延迟分位数（P50/P99，P99 = 延迟分布第 99 百分位数）：`契约 SLA 条款登记的 P99 上界 ≤ 方面 6 目标值（3.4 接收约束方面 6 行：延迟/可用性目标 → 契约 SLA 条款 P99、错误预算）；端到端 P99 随调用链深度单调不减（每次交互引入一次网络往返 + 编解码项）→ 不可达即须换形态或重审风格（3.6 示例一：延迟预算量化证据）`
- **envelope** 可用性/可靠性：可用性目标（SLO）、错误预算〔error budget：1 − SLO〕：`错误预算 = 1 − SLO（6.2.1 定义式）；对外 API 场合错误预算 上界由合同 SLA 或监管条文给定（3.3 问题空间驱动第一行：第三方开放 → 对外 SLA 条款）→ 四类合法出处之外不得填值（6.2.1 量化纪律＋0.4 证据门槛）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`破坏性变更触达的消费者数 上界 = consumer_set 基数；弃用窗口时长 ≥ 最慢消费者迁移时长（X3，条件硬）→ 窗口短于该下界即越界，估计无出处时按 0.4 降级为软＋保守假设 ADR`
- **成本**：ops_cost＝API 网关（南北向）与服务目录（内部检索）的注册与运维面（3.2.2 发现与注册）→ 运维项随对外 API 数上升；母本未给单位运维成本 …｜聚合语义=itemwise
- **反模式** 2 项（P0×2）：CTR-002-AP1 把强加决策过度泛化（南北向标准被套用到东西向），致延迟预算不可达仍强行沿…；CTR-002-AP2 对外 API 未登记 full 兼容与弃用窗口即以 published …
- **兼容性**：STY-001(requires)、CTR-007(composable)、CTR-008(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X1(implements)、X2(consumed_by)、X3(consumed_by)、X5(consumed_by)
- **参考文献**：bib 30 [已核验]·metadata_extraction、bib 32 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：机器层天然性为『高』——IDL/OpenAPI 文档本身即谓词（3.2.1 定义列/机器层天然性列），0.9 同源生成在契约域最强适用（3.4 施→10 硬），禁止双重维护
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-003｜异步消息契约

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：3.2.1-异步消息契约
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`关联 ID 覆盖率 上界为 1（3.2.1 定义列明文消息元数据约定含关联 ID）；追踪覆盖率 单调不减 → 缺关联 ID 即跨单元因果链断裂，覆盖率 < 1 时为可观测性缺口而非可接受状态（6.2.1 可观测性族）`
- **envelope** 性能：延迟分位数（P50/P99，P99 = 延迟分布第 99 百分位数）：`端到端延迟增量 = 网络往返 + broker 驻留 + 编解码 → 随队列深度单调不减；本形态不承诺即时结果（3.2.1 适用条件列的反面）→ 需即时结果的交互不得以本形态承载，P99 上界须由方面 6 目标值给定（3.4 接收约束方面 6 行）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`schema 变更触达的消费者数 上界 = consumer_set 基数（命令类交互默认 = 1，3.2.1 判别规则）；> 1 即本形态被当作事件契约使用 → X7 交叉一致性检查可捕获（命名模式 × 消费者数）`
- **成本**：ops_cost＝broker 与 schema registry（事件/消息）的运维面（3.2.2 发现与注册）→ 运维项随消息主题数上升；母本未给单位运维…｜聚合语义=itemwise
- **反模式** 2 项（P1×1／P2×1）：CTR-003-AP1 命令类交互以事件契约承载（『PleaseDoX 事件』反模式）；CTR-003-AP2 消息元数据约定缺项（消息 ID/时间戳/关联 ID/投递语义声明任一缺失…
- **兼容性**：STY-002(requires)、STY-003(composable)、CTR-004(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X1(implements)、X7(consumed_by)、X2(consumed_by)、Z1(consumed_by)
- **叙事（收益-成本）**：收益：调用方不等待结果 → 削峰与解耦，单跳延迟预算由往返改为投递/驻留/消费三段
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-004｜事件契约

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：3.2.1-事件契约、3.2.2-版本化策略、3.2.2-兼容性规则、3.2.2-破坏性变更流程
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`additive-only 下既有字段的改动数 = 0 且新增字段均为可选（3.2.2 版本化策略内容列明文）→ 改动数 > 0 即为破坏性变更，须走 X3 弃用窗口；schema 变更触达的消费者数 = consumer_set 基数，一对多消费者使该基数 单调不减`
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`事件信封元数据规范覆盖率 上界为 1；追踪覆盖率 单调不减 → 信封缺项即跨消费方因果链断裂，覆盖率 < 1 时为可观测性缺口而非可接受状态（3.2.1 定义列将事件信封列为构成项；6.2.1 可观测性族）`
- **envelope** 可用性/可靠性：可用性目标（SLO）、错误预算〔error budget：1 − SLO〕：`错误预算 = 1 − SLO（6.2.1 定义式）；一对多扇出使单事件的投递失败影响面 ≥ 单个消费方 → 错误预算消耗速率 随 consumer_set 基数单调不减；目标值只能取四类合法出处（6.2.1 量化纪律＋0.4 证据门槛）`
- **成本**：ops_cost＝schema registry（事件/消息）与事件总线的运维面（3.2.2 发现与注册）→ 运维项随事件类型数与订阅方数上升；母本未给单位运…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：CTR-004-AP1 事件契约以祈使语义命名，或消费者数为一对一（『PleaseDoX 事件』…；CTR-004-AP2 事件契约以 published 发布而缺 version 或 compa…；CTR-004-AP3 已发布事件契约做非 additive-only 变更而未走破坏性变更流程…
- **兼容性**：STY-003(requires)、CTR-003(composable)、CTR-007(composable)、CTR-008(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X1(implements)、X7(implements)、X2(consumed_by)
- **参考文献**：bib 31 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：一方发布、多方响应 → 发布方与消费方在时间与拓扑上双重解耦，新增消费方无需发布方改动（additive-only 下新增可选字段即可扩展）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-005｜数据契约

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：3.2.1-数据契约
- **envelope** 安全：攻击面清单闭合率、漏洞修复时限、敏感数据访问路径合规率：`敏感数据访问路径合规率 上界为 1（3.2.1 定义列将『敏感性标注』列为语义条款构成项；6.2.1 安全族）→ 存在未经数据契约暴露的敏感数据访问路径即 < 1，为越界而非可接受状态`
- **envelope** 合规：监管条款 → 可判定谓词的映射覆盖率：`监管条款 → 可判定谓词的映射覆盖率 单调不减；语义条款中的敏感性标注与所有权声明是映射的输入面 → 缺项即覆盖率上界受限于缺项数（6.2.1 合规族；3.2.1 定义列）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`语义条款变更触达的访问路径数 上界 = access_path 中以本契约为第四实参的路径数；3.4 施→4『唯一合法路径定义』使该上界同时是全部合法数据流动的触达面 → 上界随消费方增加单调不减`
- **成本**：ops_cost＝服务目录（内部检索）与数据契约注册面的运维项（3.2.2 发现与注册）→ 运维项随数据集数与消费方数上升；母本未给单位运维成本 → 方括号占…｜聚合语义=itemwise
- **反模式** 4 项（P0×3／P1×1）：CTR-005-AP1 直连物理表/存储引擎绕过数据契约（共享数据接入的条件 4 违例）；CTR-005-AP2 共享数据接入四条件的满足情况未显式记录，或四条件任一违反而未触发向方面 …；CTR-005-AP3 语义条款缺项（单位/值域/空值语义/敏感性标注/所有权声明任一缺失）；CTR-005-AP4 数据访问路径未经所有者单元暴露（所有权绕过的契约面投影）
- **兼容性**：STY-006(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X6(implements)、X1(implements)、Y1(consumed_by)、W4(consumed_by)
- **叙事（收益-成本）**：收益：语义条款五项（单位、值域、空值语义、敏感性标注、所有权声明）把数据流动的解释面从代码与口头约定收回到注册表，使 3.4 施→4『唯一合法路径定义』可判定
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-006｜UI/端契约

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：3.2.1-UI/端契约
- **envelope** 性能：延迟分位数（P50/P99，P99 = 延迟分布第 99 百分位数）：`前端可见延迟 = 端渲染项 + 网络项 + 聚合层项 → 随聚合层引入的后端调用数单调不减；P99 上界须由方面 6 目标值给定（3.4 接收约束方面 6 行：延迟/可用性目标 → 契约 SLA 条款）→ 四类合法出处之外不得填值（6.2.1 量化纪律＋0.4 证据门槛）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`跨边界契约变更数 = 端形态数 × 该端契约面数；BFF 作为『面向特定前端形态定制的聚合服务层』（3.2.1 定义列）使每端各持一份契约面 → 端形态数增加时该乘积 单调不减`
- **成本**：ops_cost＝API 网关（南北向）与按端形态定制的聚合服务层的部署与运维面（3.2.2 发现与注册；3.2.1 定义列 BFF）→ 运维项随端形态数上升…｜聚合语义=itemwise
- **反模式** 2 项（P0×1／P1×1）：CTR-006-AP1 前端与后端间的约定未登记为契约（端侧隐式契约）；CTR-006-AP2 同一语义条款在聚合层（BFF）与后端契约两处维护（双重维护）
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X1(consumed_by)、X2(consumed_by)
- **叙事（收益-成本）**：收益：把前端与后端间的约定从端代码与口头惯例收回到注册表，使 X1『无未登记跨单元交互』在端侧同样可判定
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-007｜版本化策略

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：3.2.2-版本化策略
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`additive-only 演化下既有字段的改动数 = 0 → 单次演化的跨边界契约变更数 上界 = 新增可选字段数；非 additive-only 演化的变更数 随 consumer_set 基数 单调不减（每个消费者各需一次适配，3.2.2 内容列的推荐项即为此设）`
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`已登记版本载体的 published 契约数 / published 契约总数 上界为 1（X2：∀C(lifecycle_state=published): has(version) ∧ has(compat_policy) —— 硬）→ 缺口 = 未登记者数，随 published 契约数增加 单调不减`
- **成本**：ops_cost＝schema registry / API 网关版本路由 / 服务目录三类注册面的部署与运维项（3.2.2 发现与注册行）→ 运维项随契约数…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×2）：CTR-007-AP1 published 态契约未登记版本载体（缺 version 或缺 co…；CTR-007-AP2 事件契约改动或删除既有字段（违反 additive-only 推荐）而未…；CTR-007-AP3 同一契约在 URI 与头部两处各持一个版本载体（版本载体双重维护）
- **兼容性**：CTR-002(composable)、CTR-004(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X2(implements)、X3(consumed_by)
- **参考文献**：bib 33 [已核验（在线在位：2026-09-18 复核，Platform 8.3 当前文档可获取）]·metadata_extraction
- **叙事（收益-成本）**：收益：把版本载体的选择从口头惯例收回到注册表，使 X2『发布态版本与兼容策略齐备』可逐契约判定
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-008｜兼容性规则

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：3.2.2-兼容性规则
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`compat_policy = none 时单次变更的跨边界契约变更数 上界 = consumer_set 基数（每个消费者各需一次适配）；= full 时该上界降为 0（变更须对新旧两侧同时可读 → 只允许 additive 演化）；任一取值下该上界 随 consumer_set 基数 单调不减`
- **envelope** 可用性可靠性：SLO、错误预算〔1 − SLO〕、MTTR、RPO/RTO：`兼容性失配导致的消费者解析失败所占错误预算份额 上界为 1（错误预算 = 1 − SLO，3.4 接收约束方面 6 行：可用性目标 → 契约 SLA 条款）→ 该份额随弃用窗口内并存版本数 单调不减；对外 API 取 full + 弃用窗口（3.2.2 默认值列）以压低该份额`
- **成本**：ops_cost＝兼容性检查在 CI 中的执行面与 schema registry 的 per-subject 兼容性配置面（3.2.2 发现与注册行；书目 …｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×2）：CTR-008-AP1 published 态契约未登记兼容性规则（缺 compat_polic…；CTR-008-AP2 对外 API 按内部 API 放宽兼容性（未取 full + 弃用窗口）；CTR-008-AP3 多契约共用一条全局兼容性声明（未每契约登记其一）
- **兼容性**：CTR-002(composable)、CTR-004(composable)、CTR-011(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X2(implements)、X3(consumed_by)
- **参考文献**：bib 33 [已核验（在线在位：2026-09-18 复核，Platform 8.3 当前文档可获取）]·metadata_extraction
- **叙事（收益-成本）**：收益：兼容性规则把『谁能读谁』从口头承诺变成逐契约登记的可判定字段，使 X2 的 has(compat_policy) 有确定取值域（backward / forward / full / none）
- **数据来源层**（yaml 行内注释）：applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-009｜消费者驱动契约测试（CDC）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：3.2.2-消费者驱动契约测试（CDC）
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`高风险契约的 CDC 覆盖率 = 已建 cdc_suite 的高风险契约数 / 高风险契约总数 上界为 1（X4：∀C ∈ high_risk: cdc_suite(C)）→ 缺口 = 未覆盖者数；变更前置时间随 CDC 在提供者 CI 中的执行时长 单调不减，母本未给该时长数值（0.4 证据门槛 → 不填）`
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`『提供者自认为兼容』幻觉的检出率 = CDC 在提供者 CI 中拦截的兼容性回归数 / 兼容性回归总数 上界为 1；未纳入 CI 的契约其检出率 下界为 0（3.2.2 内容列：消费者定义期望 → 提供者 CI 中验证）`
- **成本**：ops_cost＝CDC 套件在提供者 CI 中的执行与维护面＋消费者期望工件的存放与同步面（3.2.2 内容列）→ 运维项随高风险契约数与 consumer…｜聚合语义=itemwise
- **反模式** 3 项（P1×3）：CTR-009-AP1 高风险契约无 CDC 套件；CTR-009-AP2 消费者期望由提供者单方定义（期望来源倒置）；CTR-009-AP3 CDC 未纳入提供者 CI（仅本地或人工执行）
- **兼容性**：STY-016(composable)、STY-003(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X4(implements)
- **参考文献**：bib 28 [已核验]·metadata_extraction、bib 29 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：CDC 把兼容性承诺的验证权交给消费者——期望由消费者定义、在提供者 CI 中验证，直接消除 3.2.2 内容列点名的『提供者自认为兼容』幻觉
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-010｜契约生命周期

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：3.2.2-契约生命周期
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`lifecycle_state 已写入共享白板决策记录的契约数 / 契约总数 上界为 1（3.2.2 内容列：状态字段写入共享白板决策记录）→ 缺口 = 未写入者数，随契约总数增加 单调不减`
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`published 与 deprecated 并存版本数 上界 = 弃用窗口内允许并存数；迁移完成度 = 已迁移消费者数 / consumer_set 基数 上界为 1 → 随窗口推进 单调不减（3.2.2 破坏性变更流程默认值列：弃用窗口 ≥ 最慢消费者的迁移时长估计）`
- **成本**：ops_cost＝五态链的状态流转管理面＋白板决策记录的写入与查询面（3.2.2 内容列）→ 运维项随契约数与并存版本数上升；母本未给单位运维成本（默认值列为…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×2）：CTR-010-AP1 契约未经批准即迁入 published（或已迁入 deprecated …；CTR-010-AP2 状态字段未写入共享白板决策记录（生命周期状态只存于文档或代码）；CTR-010-AP3 契约迁入 deprecated 而未登记弃用窗口终点（until 缺失）
- **兼容性**：CTR-011(composable)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X5(implements)、X2(consumed_by)
- **叙事（收益-成本）**：收益：五态链把契约的存在状态从口头共识变成白板谓词 lifecycle_state，使 X5『发布即批准』与 X2『发布态版本与兼容策略齐备』都有确定的量词范围
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-011｜破坏性变更流程

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：3.2.2-破坏性变更流程
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`迁移支持成本 上界 = consumer_set 基数 × 单消费者迁移项数（3.2.2 内容列：影响全部消费者）→ 随 consumer_set 基数 单调不减；触达单元数含拆分后新建契约数（3.6 示例三：契约 v2 = 拆分后的两条新契约）`
- **envelope** 可用性可靠性：SLO、错误预算〔1 − SLO〕、MTTR、RPO/RTO：`弃用窗口 t ≥ slowest_consumer_migration(C)（X3）→ 窗口内旧版本须持续可用，并存版本所占错误预算份额（错误预算 = 1 − SLO）上界为 1；窗口缩短使未按期迁移的消费者失配概率 单调不减，母本未给该概率数值（0.4 证据门槛 → 不填）`
- **成本**：ops_cost＝弃用窗口内新旧版本并存的运维面＋迁移支持的工程面＋绞杀者迁移序列的切换运维面（3.2.2 内容列；3.4 施→2；书目 34）→ 运维项随 …｜聚合语义=itemwise
- **反模式** 4 项（P0×3／P1×1）：CTR-011-AP1 破坏性变更无弃用窗口，或窗口短于最慢消费者迁移时长；CTR-011-AP2 破坏性变更缺完整 ADR 或未经批准即执行；CTR-011-AP3 以无出处的消费者迁移承诺作为弃用窗口依据（未剔除即使用）；CTR-011-AP4 切割已发布契约而不走本流程（分解直接跨越契约边界）
- **兼容性**：CTR-010(composable)、CTR-008(composable)、DEC-005(tension)
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X3(implements)、X5(consumed_by)
- **参考文献**：bib 34 [已核验（2026-09-15 年份更正，见附录一第 16 行）]·metadata_extraction
- **叙事（收益-成本）**：收益：把破坏性变更从『改了就发』收回到四要件流程（完整 ADR + 批准 + 弃用窗口 + 迁移支持），使 X3『迁移窗口闭合』与 X5『发布即批准』在契约域可判定
- **数据来源层**（yaml 行内注释）：applicability: 骨架源；constraints_imposed: 交叉表源

### CTR-012｜发现与注册

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：3.2.2-发现与注册
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`注册面覆盖率 = 已登记于 API 网关 ∨ schema registry ∨ 服务目录 三者之一的契约数 / 契约总数 上界为 1（3.2.2 内容列；X1：∀ interaction(u1,u2) ∈ connects: ∃C ∈ registry: covers(C,u1,u2)）→ 缺口 = 未登记者数，随契约总数增加 单调不减`
- **envelope** 性能：延迟分位数（P50/P99，P99 = 延迟分布第 99 百分位数）：`API 网关（南北向）作为注册与发现面引入额外一跳 → 外部可见延迟 随网关串联跳数 单调不减；P99 上界须由方面 6 目标值给定（3.4 接收约束方面 6 行：延迟/可用性目标 → 契约 SLA 条款）→ 四类合法出处之外不得填值（6.2.1 量化纪律＋0.4 证据门槛）`
- **成本**：ops_cost＝API 网关（南北向）＋schema registry（事件/消息）＋服务目录（内部检索）三类注册面的部署与运维项（3.2.2 内容列）→ …｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×2）：CTR-012-AP1 契约未在任何注册面登记（网关、schema registry、服务目录三…；CTR-012-AP2 注册面选择与方面 1 风格不符（事件/消息契约仅登记于南北向 API 网…；CTR-012-AP3 同一契约在两个注册面各持一份不同步的登记（注册面双重维护）
- **施加约束** 6 项：方面 2←已发布契约的边界冻结——分解不得切割既有契约（切割需求 → 走弃用窗口 …；方面 4←数据契约的 schema 与语义条款是数据流动的唯一合法路径定义；方面 5←协调模式中的每条跨单元交互必须有注册契约（Z1 的契约来源）；方面 8←契约测试是验证计划的组成部分…
- **formal_anchor**：X1(consumed_by)
- **参考文献**：bib 33 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：三类注册面把 X1 中的抽象 registry 落成可运维工件——南北向经 API 网关、事件/消息经 schema registry、内部检索经服务目录，使『无未登记跨单元交互』有确定的查证入…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；constraints_imposed: 交叉表源；narrative: 人工判断

## kind STP（源表 4.2.2）

（STP-001–STP-004，共 4 条；kind_profile_STP status=seed；块内按 entry_id 升序）

### STP-001｜每服务自有数据库

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：4.2.2-每服务自有数据库
- **envelope** 延迟分位数 P99：`P99_cross_unit(D) ≥ P99_in_unit(D)：一一绑定后他者访问须经所有者路径（网络跳数 ≥ 1），延迟不优于单元内直访；且随访问路径跳数单调不减`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ schema of D) ≤ 1：schema 变更影响面收敛到所有者单元（4.2.2 第二列「一一绑定」的可修改性上界）；越界即所有权违例`
- **envelope** 可用性目标（SLO）：`故障域上界(D) = 故障域(其绑定存储实例)：单实例故障不外溢到无关单元 → SLO 可逐单元承诺（对照 STP-002 的全局故障域）`
- **成本**：ops_cost＝随数据集合数与部署单元数同阶上升：每单元一套实例的备份、升级、容量与连接治理；四行中高于共享数据库、低于多语言持久化与事件日志权威状态｜聚合语义=itemwise
- **反模式** 3 项（P0×3）：STP-001-AP1 名义上每服务自有数据库，实际访问路径不经所有者（跨单元直访他者存储）；STP-001-AP2 私有 schema 形态退化为多单元共写同一数据集合（无共享写例外登记）；STP-001-AP3 以跨单元 2PC 作为默认一致性手段
- **兼容性**：STY-016(composable)、OWN-001(requires)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y1(implements)、Y2(implements)、Y6(consumed_by)、W4(consumed_by)
- **叙事（收益-成本）**：收益：微服务风格的存储面默认形态，把「独立部署、独立数据」（1.2.2 微服务行定义列）落到存储实例层——变更影响面收敛到所有者单元、故障域不互相外溢、跨单元强一致需求在选型期即显形为 Y6 冲突信号…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源/人工判断；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### STP-002｜共享数据库

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.2-共享数据库
- **envelope** 延迟分位数 P99：`P99_shared(D) ≤ P99_cross_unit(D)：单元与数据同处一实例，访问路径无网络跳 → 延迟不劣于跨单元访问（此项为负向节约，不构成质量收益：1.2.3 共享数据行「时间耦合与隐式契约是默认代价」）`
- **envelope** 可用性目标（SLO）：`故障域(D) ⊇ {u : u 访问该存储实例}：单实例故障即全部访问单元不可用（1.2.2 单体行「一次故障全局倒」的存储域对应）→ SLO 上界受单实例可用性约束`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ schema of D) ≤ |{u : u 访问被改 schema}|：schema 级隔离把上界压到隔离域内；隔离缺失时上界退化为全体访问单元（1.2.2 模块化单体行反模式「模块边界只在文档里，代码里随意穿透」的存储面形态）`
- **成本**：ops_cost＝四行中最低：单一实例的备份、升级、容量与连接治理；代价转移到变更协调成本与拆分难度（此二项不进入运维面计数，须由 S4 的 ops_cost…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：STP-002-AP1 以共享数据库实现服务间集成（分布式单体信号）；STP-002-AP2 schema 级隔离缺失或穿透（多模块直访同一 schema）；STP-002-AP3 拆分缝逐版本固化：跨 schema 依赖上升而无收敛计划
- **兼容性**：STY-014(composable)、STY-015(composable)、STY-006(tension)、STY-016(tension)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y1(consumed_by)、Y6(consumed_by)、W4(consumed_by)
- **叙事（收益-成本）**：收益：运维面最小（单一实例）、访问路径无网络跳、本地事务使强一致在技术上可得，是单体风格的自然存储形态
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源/人工判断；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### STP-003｜事件日志为权威状态

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：4.2.2-事件日志为权威状态
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 读模型) ≤ 1 ∧ 触达单元数(Δ 事件 schema) ≥ |{已持久化事件版本}|：读写分离使读侧变更收敛到单一派生视图，而事件 schema 变更触达全部历史版本 → 两向界不对称（1.2.3 包络列「事件 schema 演化难」）`
- **envelope** 延迟分位数 P99：`P99_read(派生视图) 与写后立即可读不可同时成立：读模型自由优化（1.2.3 包络列）压低读侧 P99，但读侧相对权威日志存在投影延迟窗口 → 强同步查询语义不可得（1.2.5 张力行「事件溯源 × 强同步查询语义 → 张力（读模型最终一致）」）`
- **envelope** 可用性目标（SLO）：`RPO(派生视图) ≥ RPO(事件日志)：权威状态在日志侧，日志持久化即业务状态不丢；派生视图可按 Y7 重算 → 其 SLO 承诺可低于日志侧（4.2.4 物化视图行「视图是派生物不是所有者」）`
- **成本**：ops_cost＝四行中最高：事件基础设施（日志存储、流处理、投影作业、快照与重放）＋完整历史保留（1.2.3 包络列「复杂度↑↑」；1.3 交付空间驱动将其…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：STP-003-AP1 派生视图反客为主：向物化视图直写，或把视图当权威源；STP-003-AP2 派生数据无可重建血缘（重建能力未登记）；STP-003-AP3 事件契约无版本治理（以隐式约定演化事件 schema）
- **兼容性**：STY-004(requires)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y1(implements)、Y7(implements)、Y3(consumed_by)
- **参考文献**：bib 37 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：权威状态即完整变更历史，审计与时间旅行调试由存储形态直接提供而无需附加设施（1.2.3 适用条件列）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### STP-004｜多语言持久化

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：4.2.2-多语言持久化
- **envelope** 延迟分位数 P99：`∀ q ∈ query_classes: P99_measured(q) ≤ P99_registered(q)：逐查询类的实测分位数不得超过注册表登记阈值（4.6 示例三消费字段「STP/R 阈值注册表（P99）」；越界即可推翻指标的触发面）`
- **envelope** 性能：资源占用：`运维面(engine_set) 随 |engine_set| 单调不减：每增加一种引擎 = 运维面扩大（4.2.2 第三列原文）→ 资源占用与治理成本的下界随引擎数上升`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 存储引擎) ≤ |{u : u 直依该引擎原生接口}|：访问层参数化（4.6 示例三 CH-B 保守界「repository 参数化存储访问」）把上界压到抽象层内；未参数化时上界为全部直依单元`
- **成本**：ops_cost＝随引擎数线性累积且为四行中最高之一：每种引擎独立的备份、升级、容量、监控与专家知识（4.2.2 第三列「每增加一种引擎 = 运维面扩大」）；…｜聚合语义=itemwise
- **反模式** 3 项（P0×2／P2×1）：STP-004-AP1 无负载证据的多语选型（以技术偏好替代访问模式勘察）；STP-004-AP2 引擎集合超出交付空间登记的运维能力；STP-004-AP3 存储访问层未参数化（引擎选择固化进业务代码）
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y3(consumed_by)、Y4(consumed_by)、Y6(consumed_by)
- **参考文献**：bib 38 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：访问模式与存储引擎匹配时，单类查询的延迟/吞吐可显著优于通用关系库（4.2.2 第二列）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源；narrative: 人工判断

## kind DFL（源表 4.2.4）

（DFL-001–DFL-005，共 5 条；kind_profile_DFL status=seed；块内按 entry_id 升序）

### DFL-001｜事务性发件箱（outbox）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.4-事务性发件箱（outbox）
- **envelope** 延迟分位数 P99：`P99_event_visible(consumer) ≥ P99_business_commit + Δrelay：业务写在本地事务提交即持久（本机制不劣化写路径），事件对消费者可见须经异步中继 → 可见延迟不小于中继投递间隔；且随中继堆积深度单调不减`
- **envelope** 可用性目标（SLO）：`业务写可用性 ⊥ 消息中间件可用性（发件箱表与业务表同事务 → 中间件故障期业务写不受阻）；事件投递可用性 = 中继可用性 ∧ 中间件可用性，且故障期事件只累积不丢失（at-least-once 的可用性收益面）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(新增消费者) = 0（生产者侧）：1.2.3 事件驱动行『扩展新消费者不改生产者』的生产侧前提；触达单元数(Δ 事件 schema) ≤ 生产者单元 + 中继`
- **envelope** 性能：资源占用：`资源占用(发布点) = 业务表 + 1 张发件箱表 + 1 个常驻中继作业（轮询或日志读取）→ 存储与调度资源随发布数据集合数同阶增长；发件箱表深度上界由清理策略给出（未登记清理策略即无上界）`
- **成本**：ops_cost＝随发布数据集合数同阶上升：每处发件箱表 + 一个常驻中继作业的部署、监控、堆积告警与清理治理；高于纯同步发布（多一类常驻作业与一张表），低于…｜聚合语义=itemwise
- **反模式** 4 项（P0×3／P2×1）：DFL-001-AP1 业务写与事件发布分离为两次写（应用层双写），以重试替代同一本地事务的原子…；DFL-001-AP2 投递语义未显式声明即上线（假设中间件提供恰好一次）；DFL-001-AP3 消费者未声明幂等机制而依赖 at-least-once 投递；DFL-001-AP4 发件箱表无清理策略与堆积告警（表深度与最旧记录时龄不可观测）
- **兼容性**：STY-003(composable)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Z2(implements)、Y4(consumed_by)
- **参考文献**：bib 42 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：4.2.4 第三列把本机制定性为事件驱动风格下『业务成功但事件丢失』问题的**标准解**——业务写与事件发布在同一本地事务内原子提交，把双写不一致消解为单库事务问题
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源/人工判断；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### DFL-002｜变更数据捕获（CDC）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.4-变更数据捕获（CDC）
- **envelope** 延迟分位数 P99：`P99_change_visible(下游) ≥ P99_commit(源库) + Δcapture + Δrelay：变更须先落源库事务日志、再由捕获器读取并外发 → 可见延迟严格大于源库提交延迟；且随日志位点滞后（lag）单调不减。6.6 示例四要求此类刷新延迟界必须**补出处**（现状基线测量），不得编造精确值`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 源库 schema) ≥ 捕获管道 + 全体下游消费者：日志格式与表结构耦合 → schema 变更沿事件流传播（4.2.4 第四列『日志格式耦合存储引擎』的可修改性下界）；触达单元数(Δ 存储引擎) ≥ 1 管道重建（引擎更换即重建）`
- **envelope** 性能：资源占用：`资源占用(源库) ≥ 日志读取连接 + 位点存储：捕获为常驻读取负载，源库侧新增连接与 I/O 面；非侵入路径的代价是把负载从应用代码移到数据库层`
- **envelope** 可用性目标（SLO）：`下游派生数据的可用性上界 = min(源库可用性, 捕获器可用性, 事件流可用性)：任一环节故障期下游只陈旧不丢失（日志位点可续读），但陈旧窗口无上界除非位点滞后已登记告警阈值`
- **成本**：ops_cost＝随捕获源库数同阶上升：每源一套连接器部署、日志位点管理、schema 跟随与滞后告警；高于发件箱（耦合存储引擎日志格式、引擎更换即重建），四…｜聚合语义=itemwise
- **反模式** 4 项（P0×3／P2×1）：DFL-002-AP1 事务日志可访问性未勘察即把 CDC 列入候选（勘察必答项缺答）；DFL-002-AP2 以 CDC 非侵入为名绕过所有者契约直取他者数据；DFL-002-AP3 外发事件流未声明投递语义与消费者幂等；DFL-002-AP4 日志位点滞后无告警阈值（下游陈旧窗口不可观测）
- **兼容性**：STY-014(tension)、DFL-005(composable)、DFL-003(composable)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Z2(consumed_by)、Y2(consumed_by)、Y4(consumed_by)
- **参考文献**：bib 43 [已核验（工具存在）]·narrative_only
- **叙事（收益-成本）**：收益：4.2.4 第三列把本机制定性为遗留库集成中「无法改造应用代码时的**唯一非侵入路径**」——不改一行业务代码即可把既有库的变更外发为事件流，是 4.6 示例一棕地过渡（逻辑所有权先行、物理拆分…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### DFL-003｜流处理

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.4-流处理
- **envelope** 延迟分位数 P99：`P99_derived_visible ≥ P99_event_arrival + Δwindow + Δstate_emit：派生结果的可见延迟受窗口/水位线推进节奏的下界约束；事件时间语义下随水位线滞后（乱序容忍度）单调不减，处理时间语义下随链路处理耗时单调不减（5.2.4 语义分岔点的界形后果）。具体数值母本未给（0.4）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 变换/聚合逻辑) ≤ 1 流作业 + 其结果的消费者：连续变换/聚合收敛于流作业内，不改上游生产者（4.2.4 第二列；1.2.3 事件驱动行『扩展新消费者不改生产者』）；触达单元数(Δ 时间语义) ≥ 1 流作业 + 全体依赖其结果时基的下游（事件时间↔处理时间切换改变结果语义，非局部改动）`
- **envelope** 性能：资源占用：`资源占用 ≥ 常驻计算 + 状态后端存储，且状态后端占用随键基数与窗口长度单调增长（无界流的连续聚合须持有中间状态）；4.2.4 未给量化界 → 只登记构成项与单调方向（0.4）`
- **envelope** 可用性目标（SLO）：`派生结果的可用性上界 = min(上游事件流可用性, 流作业可用性, 状态后端可用性)；作业重启期须回放，回放完成前派生结果不满足新鲜度界（水位线须重新推进，5.2.4）`
- **成本**：ops_cost＝随流作业数与状态后端规模上升：常驻计算集群、状态后端容量与快照/恢复、水位线与滞后告警；高于批式 ETL（常驻 vs 周期），与 CDC 管…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：DFL-003-AP1 事件时间 vs 处理时间语义未显式选择（或乱序容忍度未以水位线表达）；DFL-003-AP2 上游事件流未声明投递语义，或流作业消费非幂等；DFL-003-AP3 水位线策略缺失或过紧（迟到事件被静默丢弃）；DFL-003-AP4 状态后端无界增长（键基数或窗口长度失控，无容量阈值告警）
- **兼容性**：STY-014(tension)、DFL-002(composable)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Z2(consumed_by)、Y4(consumed_by)
- **叙事（收益-成本）**：收益：4.2.4 第三列把本机制的适用面定为「实时派生视图、监控指标」——对无界事件流做连续变换/聚合，使派生结果随事实到达即更新，而不必等批窗口闭合
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；anti_patterns: 人工判断；formal_anchor: 交叉表源

### DFL-004｜ETL/ELT 批

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.4-ETL/ELT 批
- **envelope** 延迟分位数 P99：`P99_data_visible ≥ [batch_window]：变更在窗口闭合并完成抽取-变换-装载前不可见 → 可见延迟以批窗口长度为下界（4.2.4 第四列『批窗口 = 新鲜度条款』的界形）；供给为批式而非连续 → 窗口内延迟分布不连续，不适用流式的单调滞后表述。窗口长度母本未给（0.4）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 变换逻辑) ≤ 1 批作业（ELT 形态下收敛于目标端变换，不改源端）；触达单元数(Δ 源端 schema) ≥ 1 抽取通道 + 1 变换 + 目标端结构（4.4 施→9 schema 漂移守护对象）`
- **envelope** 性能：资源占用：`资源占用呈周期性峰值（窗口内集中抽取/变换/装载）而非常驻占用；峰值随抽取数据量与窗口内并发变换单调上升；4.2.4 未给量化界 → 只登记形态与单调方向（0.4）`
- **envelope** 可用性目标（SLO）：`目标端数据的可用性上界 = min(源端可读性, 调度器可用性, 目标端可用性)；单个窗口失败即令新鲜度条款违约一个窗口长度 → SLO 承诺须以窗口数为单位表述（4.2.4 第四列）`
- **成本**：ops_cost＝随批作业数与目标端规模上升：调度器与窗口监控、失败重跑与幂等装载、目标端容量与结构治理；无常驻计算面（周期性执行）→ 常驻成本低于流处理与 …｜聚合语义=itemwise
- **反模式** 5 项（P0×2／P1×2／P2×1）：DFL-004-AP1 以批式 ETL 承载实时/高新鲜度需求（批窗口下界与业务新鲜度要求不匹配…；DFL-004-AP2 新鲜度条款未写入数据契约（批窗口只存在于调度配置里）；DFL-004-AP3 抽取绕过所有者契约直取源库；DFL-004-AP4 装载非幂等（窗口重跑产生重复数据）；DFL-004-AP5 窗口失败未重跑且无告警（下游静默读到陈旧数据）
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y4(consumed_by)
- **叙事（收益-成本）**：收益：4.2.4 第三列把本机制的适用面定为「分析域、报表
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；anti_patterns: 人工判断；formal_anchor: 交叉表源

### DFL-005｜物化视图

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：4.2.4-物化视图
- **envelope** 延迟分位数 P99：`P99_view_fresh ≥ Δrefresh > 0：视图为派生物 → 变更可见延迟以刷新延迟为下界（4.2.4 第二列『由权威数据派生』的界形）。6.6 示例四给出该界的既有书写实例（『事件投影读模型：刷新延迟 P99 界』并明记『出处＝现状消息基础设施基线测量，非编造精确值』）；其实例数值不入本字段（M3 假精确门槛）→ 本条只登记界形、符号与出处要求，数值须由现状基线测量补入（0.4＋6.2.1）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 读模型口径) ≤ 1 视图定义 + 1 刷新路径（读侧自由优化，1.2.3「事件溯源 + CQRS」行第四列）；触达单元数(Δ 权威 schema) ≥ 1 视图定义 + 1 刷新路径 + 全体消费方（派生面随源变更传播，4.4 施→9 schema 漂移守护对象）`
- **envelope** 性能：资源占用：`存储占用随视图数据量单调上升（本地化读模型 = 数据复制面，与 4.2.2『所有者 + 授权读副本』行同阶）；读侧查询开销下降为该复制面的对价；4.2.4 未给量化界 → 只登记形态与单调方向（0.4）`
- **envelope** 可用性目标（SLO）：`视图读可用性上界 = min(刷新链路可用性, 视图存储可用性)；权威源不可用时视图仍可读（本地化读模型的可用性收益面）但新鲜度随之退化 → 陈旧读窗口须与可用性一并写入 SLO（6.6 示例四把陈旧读窗口界与读取可用性界作为联合目标同时判定，二者不可只承诺其一；其实例数值不入本字段——M3 假精确门槛）`
- **成本**：ops_cost＝随视图数与刷新链路规模上升：全量重建与增量回填能力、刷新滞后告警、与权威源的对账；存储面为数据复制成本（与授权读副本同阶）；无常驻计算集群时…｜聚合语义=itemwise
- **反模式** 5 项（P0×2／P1×1／P2×2）：DFL-005-AP1 向物化视图直写，或把视图当作权威状态源（派生物反客为主）；DFL-005-AP2 重建能力与血缘未登记（视图不可重建，或 source_set 不明）；DFL-005-AP3 视图访问路径未经所有者授权与契约登记即对消费方开放；DFL-005-AP4 刷新延迟界无出处即写入 SLO/包络，或以编造精确值充当现状基线；DFL-005-AP5 刷新链路滞后无告警阈值（陈旧读窗口不可观测）
- **兼容性**：DFL-002(composable)、STP-003(composable)、STP-001(composable)、STY-004(composable)
- **施加约束** 7 项：方面 2←数据归属现状回馈分解：现状数据不可干净归属时，S4 策略受约束、拆分序列…；方面 3←数据契约的 schema 与语义条款（单位/值域/空值/敏感性/新鲜度）…；方面 5←一致性模型 → 协调模式可行集：跨所有者强一致需求 → Saga + 业…；方面 6←一致性级别声明与新鲜度条款 → 质量判定的代价计入项…
- **formal_anchor**：Y1(implements)、Y2(consumed_by)、Y7(implements)、Y4(consumed_by)
- **参考文献**：bib 40 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：4.2.4 第二列把本机制定性为「由权威数据派生、可重建的本地化读模型」——读侧可按查询形态自由优化（1.2.3「事件溯源 + CQRS」行第四列『读模型自由优化』），跨单元查询聚合得以在不引入…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

## kind RLP（源表 5.2.3）

（RLP-001–RLP-007，共 7 条；kind_profile_RLP status=seed；块内按 entry_id 升序）

### RLP-001｜幂等

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.3-R-01
- **envelope** 延迟分位数 P99：`P99(处理) ≥ P99(无幂等面) + Δdedup：业务效果生效前须完成幂等键计算与去重状态查询（一次额外存储读写）→ 附加项恒 ≥ 0，且随去重状态规模单调不减；母本未给量化增量 → 只登记界形、符号与单调性（0.4）`
- **envelope** 可用性目标（SLO）：`可用性(有效恰好一次效果) = min(消费者可用性, 去重状态存储可用性) → 去重状态不可用时幂等判定不可得，at-least-once 的重复投递不再被吸收（5.5 Z2 的后果面；@2488『非中间件魔法』）`
- **envelope** 性能：资源占用：`资源占用 = 每消费者 1 份去重状态（去重表或去重窗口）+ 每请求 1 次键计算与查询 → 存储随被去重的业务事实数同阶增长；去重窗口长度给出状态上界（未登记窗口或清理策略即无上界）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 幂等键口径) ≥ 生产者单元 + 全体消费者单元：键口径是跨单元契约条款（5.4 接收约束方面 3 行『投递语义是契约条款』同型）→ 随消费者数单调不减`
- **成本**：ops_cost＝随消费者数与被去重的业务事实数上升：每处消费者一份去重状态的部署、清理与告警；高于无幂等面（多一类状态存储与清理治理），低于 RLP-002…｜聚合语义=itemwise
- **反模式** 4 项（P0×2／P1×1／P2×1）：RLP-001-AP1 投递语义 ≠ at-most-once 而消费者未声明幂等机制（含以中间…；RLP-001-AP2 幂等键不由业务事实稳定导出（以消息 ID／投递序号充当键，重投递携新 I…；RLP-001-AP3 去重窗口短于上游最坏重投递间隔，或去重判定与业务写跨事务；RLP-001-AP4 去重表无清理策略与堆积告警（深度与最旧记录时龄不可观测）
- **兼容性**：RLP-002(composable)、RLP-004(composable)、RLP-003(composable)、CRD-005(composable)、STY-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z2(implements)、Z7(consumed_by)、X1(consumed_by)
- **参考文献**：bib 44 [已核验]（2026-10-04 在线复核：作者官网记 with Bobby Woolf／ISBN 0321200683〔ISBN-10 形态〕／2003, Addison-Wesley，数字串与母本著录 978-0-321-20068-6 一致；本地 EPUB 自述 isbn13 9780133065091 的差异仍归 G-DFL-1.route 裁决口④／SO-11，开放，本批不裁决）·metadata_extraction、bib 51 [已核验]（2026-10-04 在线复核在位，页面标注 Last updated on 06/04/2026；母本 5.7 逐字『Retry/Circuit Breaker/Bulkhead 的机制内容以书目 46《Release It!》第 2 版为提取锚点』→ 本条（幂等）的机制内容以 @2486 母本明文与书目 44 词汇面为提取锚点，51 只作工程参照；compile_usage 依 5.7 逐字为 metadata_extraction，不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：把 at-least-once 投递的重复副作用消解为可判定的去重问题——@2488 明文的『有效恰好一次』（幂等消费达成的效果等价）只能由本模式达成，中间件配置不提供（『非中间件魔法』）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源/人工判断；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### RLP-002｜收件箱（inbox）

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.3-R-02
- **envelope** 延迟分位数 P99：`P99(消费处理) ≥ P99(业务写单独) + Δinbox：去重判定与业务写在同一本地事务内 → 事务持锁时长增加，附加项恒 ≥ 0 且随收件箱表深度单调不减；母本未给量化增量 → 只登记界形与单调性（0.4）`
- **envelope** 可用性目标（SLO）：`可用性(消费处理) = 业务表可用性 ∧ 收件箱表可用性（同事务 → 任一侧不可用即处理失败）→ 可用性上界不优于业务写单独形态；换取的收益是重复副作用被原子吸收（Z2 的效果面）`
- **envelope** 性能：资源占用：`资源占用 = 每消费者 1 张收件箱表 + 每消息 1 次事务内读写 → 存储随已处理消息数同阶增长；清理策略给出表深度上界（未登记清理策略即无上界）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 去重口径) = 消费者单元内 1（同事务内闭合，不外溢至生产侧）→ 优于 RLP-001 的跨单元键口径变更（后者的触达单元数随消费者数单调不减）`
- **成本**：ops_cost＝随消费者数与消息量上升：每处消费者一张收件箱表的部署、清理作业与堆积告警；高于 RLP-001（多一类事务内写路径与清理作业），低于生产侧发…｜聚合语义=itemwise
- **反模式** 4 项（P0×2／P1×1／P2×1）：RLP-002-AP1 收件箱表与业务写不在同一本地事务（跨库或跨服务），却声称达成有效恰好一次；RLP-002-AP2 以收件箱机制替代投递语义声明（未在注册表登记 delivery_sema…；RLP-002-AP3 在收件箱事务内引入跨单元远程调用（持锁时长受下游延迟支配）；RLP-002-AP4 收件箱表无清理策略与保留期核定（表深度与最旧记录时龄不可观测）
- **兼容性**：RLP-001(composable)、RLP-003(composable)、DFL-001(composable)、STY-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z2(implements)、Y1(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 44 [已核验]（2026-10-04 在线复核：作者官网记 ISBN 0321200683〔ISBN-10 形态〕，数字串与母本著录一致；本地 EPUB 自述 isbn13 9780133065091 的差异仍归 G-DFL-1.route 裁决口④／SO-11，开放，本批不裁决）·metadata_extraction、bib 51 [已核验]（2026-10-04 在线复核在位；母本 5.7 逐字载明 Retry/Circuit Breaker/Bulkhead 的机制内容以书目 46 为提取锚点 → 本条机制内容以 @2486 母本明文为提取锚点，51 只作工程参照，compile_usage 不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：把去重判定与业务写收束进同一本地事务，消除 RLP-001 跨事务形态的崩溃窗口（『业务已写、去重未记』或反向）——@2488 的『有效恰好一次』因此在单库事务内可证成
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### RLP-003｜发件箱（outbox）

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.3-R-03
- **envelope** 延迟分位数 P99：`P99(端到端) = Δrelay（定义面，见 DFL-001）+ Σ 消费侧卡片 latency_budget_delta（去重判定等，RLP-001/002）+ 消费处理耗时 → 按 5.2.5 Σ 消费路径加和；本条目只登记消费侧附加项，不重复登记 Δrelay（0.17.1 条目为准）`
- **envelope** 可用性目标（SLO）：`可用性(有效恰好一次效果) = min(生产侧中继可用性, 消费侧幂等面可用性) → 任一侧缺失即 at-least-once 退化为可重复副作用（5.5 Z2 硬）；生产侧业务写可用性 ⊥ 中间件可用性属定义面（DFL-001），本条目不重复登记`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 投递语义声明) ≥ 生产者单元 + 全体消费者单元：投递语义是契约条款（5.4 接收约束方面 3 行『投递语义是契约条款』）→ 变更须同步至消费侧幂等面，随消费者数单调不减`
- **成本**：ops_cost＝行为面运维增量 = 消费侧去重状态的部署与清理（RLP-001/002）+ 投递语义与卡片的登记治理；生产侧发件箱表与常驻中继作业的运维成本…｜聚合语义=itemwise
- **反模式** 4 项（P0×2／P1×2）：RLP-003-AP1 生产侧采用发件箱而消费侧未声明幂等机制（行为面义务缺失）；RLP-003-AP2 投递语义未显式声明即上线，或以中间件 exactly-once 声称替代…；RLP-003-AP3 行为面与定义面分裂登记（卡片缺项，方面 6 无从校验）；RLP-003-AP4 把发件箱的投递语义读作跨单元一致性保证（以 outbox 承担强一致）
- **兼容性**：DFL-001(requires)、RLP-002(composable)、RLP-001(composable)、STY-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z2(implements)、Z7(consumed_by)、X1(consumed_by)
- **参考文献**：bib 44 [已核验]（2026-10-04 在线复核：作者官网记 ISBN 0321200683〔ISBN-10 形态〕，数字串与母本著录一致；本地 EPUB 自述 isbn13 9780133065091 的差异仍归 G-DFL-1.route 裁决口④／SO-11，开放，本批不裁决）·metadata_extraction、bib 51 [已核验]（2026-10-04 在线复核在位；本条机制内容的提取锚点是母本 4.2.4 与 @2486 明文，51 只作工程参照，compile_usage 不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：把『业务状态已提交』与『事件待投递』收束进同一本地事务，消除生产侧的丢失窗口与双写不一致（业务写成功而消息未发，或反之）——@2486 逐字将其定位为『生产侧，4.2.4 已定义，行为面消费其投…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### RLP-004｜重试 + 指数退避 + 抖动

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.3-R-04
- **envelope** 延迟分位数 P99：`P99(带重试) 的上界 = Σ_{k=1..N}（第 k 次尝试耗时 + backoff_k），N = 登记的重试上限次数 → 最坏时长随 N 与退避基数单调不减；5.6 示例一逐字将其作为 Z4 预算不闭合的成因（『SLA 要求的用户等待上界 < 捕获重试的最坏时长』）；母本未给量化值 → 只登记界形与单调性（0.4）`
- **envelope** 可用性目标（SLO）：`可用性(交互) 的上界受『暂时性失败假设』支配：假设成立时随尝试次数单调不减；假设不成立（确定性失败）时可用性无提升而延迟与负载全额付出 → 收益非无条件，须以失败分类可观测为前提`
- **envelope** 性能：资源占用：`资源占用 = 每次在途尝试一份占用（连接/线程/队列位）+ 退避等待期的状态保持 → 随 N 与并发交互数同阶增长；抖动缺失时多实例重试同步化 → 瞬时占用出现尖峰（@2486 逐字列出『抖动』即为此项的封堵）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 重试参数) = 调用方单元内 1（策略配置面）；但 Δ 最坏重试时长须同步至路径超时预算与 SLA 论证（RLP-005／Z4）→ 有效触达面 = 调用方 + 路径预算登记处`
- **成本**：ops_cost＝随重试上限次数与交互数上升：下游容量须按放大后的峰值负载核定（含重试风暴余量）、失败分类与告警须维护、最坏时长须纳入 SLA 论证；低于断路…｜聚合语义=additive
- **反模式** 5 项（P0×2／P1×2／P2×1）：RLP-004-AP1 对未声明幂等的操作重试（含对关键步 pivot 重试）；RLP-004-AP2 无上限次数或无退避的重试（含固定间隔紧密重试）；RLP-004-AP3 最坏重试时长未纳入上游超时预算／SLA 论证（Z4 预算不闭合）；RLP-004-AP4 对确定性失败重试（失败原因不可分类即一律重试）；RLP-004-AP5 退避无抖动导致多实例重试同步化（重试尖峰）
- **兼容性**：RLP-001(requires)、RLP-005(composable)、RLP-006(composable)、RLP-007(composable)、CRD-005(composable)、CRD-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z3(consumed_by)、Z4(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 46 [已核验]（2026-10-04 在线复核：官方 PDF 抽取页记 ISBN-13 978-1-68050-239-8／Book version P1.0—January 2018／作者 Michael T. Nygard，数字串与母本著录 978-1-680-50239-8 相同而连字符分组位置不同；书商页数两说 350 vs 376。差异据实登记入 MJ-24，不改写母本）·metadata_extraction、bib 51 [已核验]（2026-10-04 在线复核在位，页面标注 Last updated on 06/04/2026；母本 5.7 逐字『Retry/Circuit Breaker/Bulkhead 的机制内容以书目 46《Release It!》第 2 版为提取锚点』→ 本条机制内容以书目 46 为提取锚点，51 只作工程参照；compile_usage 依 5.7 逐字为 metadata_extraction，不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：把暂时性失败从『交互失败』转化为『延迟增加』——5.2.2 @2482 的 retriable 类因此有执行手段，关键步之后的步骤全部可重试（Z3 的 pivot_ordering_valid）…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### RLP-005｜超时预算

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.3-R-05
- **envelope** 延迟分位数 P99：`Σ timeout_budget(path) ≤ sla_bound(path) ∧ ∀ 相邻级: t_downstream < t_upstream − propagation（5.5 Z4 逐字）→ P99(路径) 的上界由 SLA 上界给出，任一跳超时值上调须由其他跳下调或 SLA 上界放宽补偿（预算守恒）；母本未给数值 → 只登记界形与守恒关系（0.4）`
- **envelope** 可用性目标（SLO）：`可用性(路径) 随超时值非单调：过短 → 正常长尾被误杀为失败（可用性下降）；过长 → 故障传播窗口拉长、在途占用累积（上游先耗尽资源）→ 存在使可用性最大的区间，其位置由实测传播延迟与长尾分布决定，母本未给 → 不填数值（0.4）`
- **envelope** 性能：资源占用：`资源占用(等待期) = 并发在途请求数 × 超时时长 → 随超时时长线性不减；级联路径上各级同时持有等待占用 → 总占用随跳数（5.5 Z5 的 sync_chain_depth）单调不减`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 任一级超时) ≥ 该级上游全体跳（预算守恒要求上游重算）+ SLA 论证登记处 → 随路径跳数单调不减；路径拓扑变更（增/减跳）触达面 = 全路径`
- **成本**：ops_cost＝随路径跳数与拓扑变更频率上升：每级超时值须实测核定、拓扑变更须重算全路径预算、超时告警须按级分列；高于重试（多一层路径级核算），低于舱壁（不…｜聚合语义=additive
- **反模式** 5 项（P0×1／P1×3／P2×1）：RLP-005-AP1 下游超时 ≥ 上游超时 − 传播开销（逐级分配界形违例）；RLP-005-AP2 全链预算不闭合（Σ timeout_budget(path) > sla…；RLP-005-AP3 传播开销与 SLA 上界无实测/无出处即取便利常数（Z4 被迫降软）；RLP-005-AP4 超时后无处置面（无快速失败/降级/断路，调用方行为未定义）；RLP-005-AP5 路径拓扑变更而预算未重算（僵尸超时配置）
- **兼容性**：RLP-004(composable)、RLP-006(composable)、RLP-007(composable)、CRD-003(composable)、CRD-008(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z4(implements)、Z5(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 46 [已核验]（2026-10-04 在线复核：官方 PDF 抽取页记 ISBN-13 978-1-68050-239-8／Book version P1.0—January 2018／作者 Michael T. Nygard，数字串与母本著录 978-1-680-50239-8 相同而连字符分组位置不同；书商页数两说 350 vs 376。差异据实登记入 MJ-24，不改写母本）·metadata_extraction、bib 51 [已核验]（2026-10-04 在线复核在位，页面标注 Last updated on 06/04/2026；母本 5.7 逐字『Retry/Circuit Breaker/Bulkhead 的机制内容以书目 46《Release It!》第 2 版为提取锚点』→ 本条机制内容以 @2486 明文与书目 46 为提取锚点，51 只作工程参照；compile_usage 依 5.7 逐字为 metadata_extraction，不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：把『各跳自行取超时默认值』的隐式假设变为显式的预算分配问题，使 Z4 可机器求值（timeout_budget(path, allocations) 在册）——@2486 括号内给出两条界形：逐…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### RLP-006｜断路器

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.3-R-06
- **envelope** 延迟分位数 P99：`断路开启时 P99(调用点) 的上界 = 断路判定开销（快速失败）→ 显著低于等待超时形态（RLP-005 的 t_timeout）；关闭态 P99 不变（仅增一次状态判定）→ 附加项恒 ≥ 0 且有界；母本未给数值 → 只登记界形与两态差异（0.4）`
- **envelope** 可用性目标（SLO）：`可用性(上游) 不再被下游可用性支配（故障扩散被截断）→ 上游可用性上界提升；代价：被断路的下游功能可用性 = 0（无降级面时）或 = 降级面可用性 → 全局 SLO 的达成取决于降级面是否覆盖该功能的必要性`
- **envelope** 性能：资源占用：`资源占用(等待期) 在断路开启时归零（不再持有在途等待）→ 占用上界由『阈值 × 统计窗口内的失败请求数』给出；关闭态增一份状态与计数占用（常数阶）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 阈值/窗口) = 调用方单元内 1（策略配置面）；触达单元数(Δ 降级面语义) ≥ 全体消费者单元（降级结果是对外可见行为，属契约面）→ 两类变更的触达面不同阶，须分别登记`
- **成本**：ops_cost＝随被保护的调用点数上升：每处须核定失败口径、阈值、窗口与降级面，并维护状态告警与恢复核定；高于重试与超时预算（多一层状态机与降级面），与舱壁…｜聚合语义=itemwise
- **反模式** 5 项（P0×1／P1×2／P2×2）：RLP-006-AP1 无半开探测（断路后不自动恢复，或恢复须人工重启）；RLP-006-AP2 无降级面即启用断路（快速失败成为对消费者的裸失败）；RLP-006-AP3 失败率阈值与统计窗口无实测出处（或失败判定口径混计）；RLP-006-AP4 断路长期开启而无 expiry 与清理登记（功能永久降级成为既成事实）；RLP-006-AP5 断路状态与转换不可观测（无告警，恢复无从核定）
- **兼容性**：RLP-007(composable)、RLP-005(composable)、RLP-004(composable)、CRD-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z4(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 46 [已核验]（2026-10-04 在线复核：官方 PDF 抽取页记 ISBN-13 978-1-68050-239-8／Book version P1.0—January 2018／作者 Michael T. Nygard，数字串与母本著录 978-1-680-50239-8 相同而连字符分组位置不同；书商页数两说 350 vs 376。差异据实登记入 MJ-24，不改写母本）·metadata_extraction、bib 51 [已核验]（2026-10-04 在线复核在位，页面标注 Last updated on 06/04/2026；母本 5.7 逐字『Retry/Circuit Breaker/Bulkhead 的机制内容以书目 46《Release It!》第 2 版为提取锚点』→ 本条机制内容以书目 46 为提取锚点，51 只作工程参照；compile_usage 依 5.7 逐字为 metadata_extraction，不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：把『下游故障 → 上游等待耗尽 → 全局拖垮』的传播链在调用点截断——@2486 逐字给出两个机制要件：失败率越阈时快速失败、半开探测恢复
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源

### RLP-007｜舱壁

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.3-R-07
- **envelope** 延迟分位数 P99：`P99(消费者 i) 的上界 = 该池排队等待 + 服务时长，且排队等待受该池排队上限约束（有界）→ 局部 P99 随该池饱和度上升；其余消费者的 P99 不受该池故障影响（外溢被阻止）→ 隔离使局部 P99 恶化而全局 P99 上界改善，非单调；母本未给数值 → 只登记界形与非单调性（0.4）`
- **envelope** 可用性目标（SLO）：`单点故障被限制在其所属池内（@2486『防单点拖垮全局』）→ 全局可用性上界不再被最弱消费者支配；代价：被隔离消费者的可用性上界 = 其池容量可承载的吞吐上限（池满即拒绝）→ 全局 SLO 的达成取决于池划分与各池容量核定是否覆盖该消费者的必要性`
- **envelope** 性能：资源占用：`每池独立预留 → 总预留 = Σ_i 池容量_i ≥ 共享池形态下的峰值需求（碎片化对价），且空闲池的预留不产生吞吐 → 资源占用上界由池划分给出而非由实际负载给出，整体利用率下降；占用随被隔离消费者数单调上升`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 池容量/排队上限) = 该池配置面 1；触达单元数(Δ 池划分：新增或合并消费者) ≥ 容量核定处 + 部署与资源预留配置处 + 该消费者的调用方单元 → 划分变更与容量变更不同阶，须分别登记`
- **成本**：ops_cost＝随被隔离的消费者数上升：每池须核定容量、排队上限与拒绝策略，并维护饱和度告警与容量复核定；与断路器同级（后者多一层状态机与降级面，本条多一层…｜聚合语义=itemwise
- **反模式** 5 项（P0×1／P1×2／P2×2）：RLP-007-AP1 以逻辑命名区分消费者而物理共享同一线程/连接池（隔离面不成立）；RLP-007-AP2 池饱和后无拒绝策略（无界排队）；RLP-007-AP3 池容量与排队上限无实测出处（或消费者划分与实际故障域不一致）；RLP-007-AP4 池划分与部署/容量核定脱钩，流量配比或拓扑变更后未重算（长期漂移）；RLP-007-AP5 池利用率、排队深度与拒绝次数不可观测（容量核定与饱和告警无从取证）
- **兼容性**：RLP-006(composable)、RLP-005(composable)、RLP-004(composable)、CRD-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z1(consumed_by)、Z4(consumed_by)、Z7(consumed_by)
- **参考文献**：bib 46 [已核验]（2026-10-04 在线复核：官方 PDF 抽取页记 ISBN-13 978-1-68050-239-8／Book version P1.0—January 2018／作者 Michael T. Nygard，数字串与母本著录 978-1-680-50239-8 相同而连字符分组位置不同；书商页数两说 350 vs 376。差异据实登记入 MJ-24，不改写母本）·metadata_extraction、bib 51 [已核验]（2026-10-04 在线复核在位，页面标注 Last updated on 06/04/2026；母本 5.7 逐字『Retry/Circuit Breaker/Bulkhead 的机制内容以书目 46《Release It!》第 2 版为提取锚点』→ 本条机制内容以书目 46 为提取锚点，51 只作工程参照；compile_usage 依 5.7 逐字为 metadata_extraction，不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：把『单个消费者的慢响应或故障耗尽共享线程/连接池 → 拖垮其余全部消费者』的传播路径在资源层截断——@2486 逐字给出机制要件（线程/连接池按消费者隔离）与其目的（防单点拖垮全局）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源；narrative: 交叉表源

## kind SCH（源表 5.2.4）

（SCH-001–SCH-003，共 3 条；kind_profile_SCH status=seed；块内按 entry_id 升序）

### SCH-001｜定时器/截止期/cron 的登记

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.4-SCH-01
- **envelope** 延迟分位数 P99：`P99(触发 → 完成) ≤ 周期长度 − [调度排队与资源竞争余量]；截止期形态下 截止期 − 触发时刻 ≥ Σ timeout_budget(path)（与 RLP-005 的 Z4 共用同一上界源，两处各自取值即两处真相，0.9）→ 母本未给任何数值，只登记界形与守恒方向（0.4）`
- **envelope** 可用性目标（SLO）：`可用性(流程) 随周期长度非单调：周期过短 → 单次执行未毕即触发下次（重叠执行与资源竞争，5.3 @2530『定时任务互相踩』）；周期过长 → 新鲜度条款被违背（4.2.4 @2210）→ 存在同时满足新鲜度且不重叠的区间，其位置由单次执行时长分布决定，母本未给 → 不填数值（0.4）`
- **envelope** 性能：资源占用：`同一时间窗内的并发触发数 ≤ [共享执行资源的预留容量]（超出即排队，排队时长计入 P99 上界）；调度器自身占用随已登记定时任务数单调不减 → 任务数增加而不增预留等价于池容量下调（与 RLP-007 的池守恒同型）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 任一 cron 表达式或截止期) ≥ 依赖该任务产出的下游全体（新鲜度条款的消费方）+ 调度权归属登记处（Y1 同型，@2492 第三子命题）→ 随下游数单调不减；若周期变更改变对外新鲜度承诺，触达面另含契约登记处（5.4 施→3，@2557）`
- **成本**：ops_cost＝随已登记定时任务数与周期变更频率上升：每任务须核定周期与截止期、变更须重算下游新鲜度条款、告警须按任务分列；人工判断的相对序为『高于舱壁（多…｜聚合语义=additive
- **反模式** 5 项（P0×1／P1×3／P2×1）：SCH-001-AP1 定时任务/cron 表达式在用而未登记（登记表外触发面）；SCH-001-AP2 重叠执行而无互斥或归属声明（同一数据集事实上出现两个写入者）；SCH-001-AP3 周期长度与截止期取便利常数（无实测执行时长分布、无新鲜度条款出处）；SCH-001-AP4 错过触发（misfire）无处置面（跳过／顺延／补偿未选边即启用）；SCH-001-AP5 cron/定时器变更而下游新鲜度条款与归属登记未同步（僵尸配置）
- **兼容性**：SCH-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **叙事（收益-成本）**：收益：把『谁在什么时候被触发』从散落于代码与部署脚本的常量变为注册表内的显式清单，使 5.3 @2530 的现状勘察有对象——@2492 把定时器／截止期／cron 三者并列为同一登记义务，因为它们同…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### SCH-002｜事件时间 vs 处理时间的显式选择

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.4-SCH-02
- **envelope** 延迟分位数 P99：`P99(事件发生 → 结果可见) = 水位线滞后 + 处理时延；事件时间语义下该上界由 watermark_policy 的乱序容忍度给出（容忍度 ↑ → P99 ↑），处理时间语义下该上界即处理时延（不含容忍度项）→ 两种语义的 P99 上界不可互换比较（@2492 逐字『语义分岔点』）；母本未给容忍度数值 → 只登记界形与单调方向（0.4）`
- **envelope** 可用性目标（SLO）：`结果完整性口径下的可用性随乱序容忍度非单调：容忍度过小 → 迟到事件被丢弃，结果对事件时间口径不完整（正确性下降）；容忍度过大 → 结果可见延迟拉长，SLO 的延迟项失守 → 存在使两项同时可满足的区间，其位置由实测乱序分布决定，母本未给 → 不填数值（0.4）`
- **envelope** 性能：资源占用：`资源占用(乱序缓冲) 随乱序容忍度单调不减（须为迟到事件保留状态窗口）；处理时间语义下该项趋于下界（不保留事件时间窗口）而以结果口径为代价 → 两种语义的占用不可同表比较（@2492 分岔点）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 时间语义) ≥ 该流全体下游消费者（结果口径随之改变）+ 卡片 observability_requires 登记处 + 回放与乱序注入的验证用例（5.4 施→8 @2560）→ 为全流触达面（单调不减）；语义一经选定即成口径承诺，回改等价于重建历史结果`
- **成本**：ops_cost＝随流数量与乱序程度上升：每流须核定容忍度、须分别采集两条时间轴、迟到事件须对账；人工判断的相对序为『高于 SCH-001（多一层时间轴观测与…｜聚合语义=additive
- **反模式** 5 项（P0×1／P1×4）：SCH-002-AP1 时间语义未显式声明（流处理/事件驱动分析未选边）；SCH-002-AP2 事件时间语义下无水位线策略（乱序容忍度未表达）；SCH-002-AP3 迟到事件无处置面（丢弃／侧输出／重算未选边）；SCH-002-AP4 以处理时间语义承载事件时间口径的正确性要求（口径错配）；SCH-002-AP5 语义选定后无事件回放与乱序注入验证
- **兼容性**：DFL-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **参考文献**：bib 49 [已核验]（2026-10-06 在线复核：VLDB 官方 PDF 抽取成功，题名标题式大写与母本著录逐字一致；作者 11 位、机构 Google；页脚 Proceedings of the VLDB Endowment, Vol. 8, No. 12 Copyright 2015 VLDB Endowment 2150-8097/15/08；页码 1792 起；CC BY-NC-ND 3.0；41st VLDB, Aug 31–Sep 4 2015, Kohala Coast, Hawaii。§1.3 Time Domains 逐字『Event Time = the time at which the event itself actually occurred』『Processing Time = the time at which an event is observed at any given point during processing within the pipeline』→ 与 @2492 中文压缩转写（事件时间 = 事实发生时刻，处理时间 = 系统见到时刻）对应无失真。著录差异据实登记：ACM DL 页题名为句首大写规范化形态（MJ-25 (ix)，不改写母本）。母本原记的本地资源面与专著展开（Streaming Systems, O'Reilly 2018, ISBN 978-1-491-98384-3）本批不重复核验。compile_usage 依 5.7 逐字为 metadata_extraction，不得在注册表侧降级）·metadata_extraction
- **叙事（收益-成本）**：收益：@2492 把时间语义定为『流处理与事件驱动分析的语义分岔点』——分岔点意味着两条路径的结果不可互换，未显式选边即把口径交给实现默认值（多数在役实现隐式采用处理时间，5.3 @2530『隐式协调…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；anti_patterns: 人工判断

### SCH-003｜调度冲突与资源竞争的归属声明

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.4-SCH-03
- **envelope** 延迟分位数 P99：`P99(争用流程) ≤ [该流程被授权的调度窗上界]；无归属声明时该上界不可判定（触发顺序偶然）→ 归属声明把偶然序变为可核算上界；调度窗上界与 5.5 @2575 timeout_budget 必须同参数（0.9）。母本未给数值 → 只登记界形与可判定性的转变（0.4）`
- **envelope** 可用性目标（SLO）：`可用性(被争用资源) 随争用方数单调不增（无裁决时每方触发都可能被另一方挤占）；声明后冲突退化为已授权的排他或优先级序 → 可用性下界由被授权方的预留给出而非由争用方数给出（Z4 @2595 超时预算闭合同型：上界须可核算）`
- **envelope** 性能：资源占用：`峰值占用 ≤ Σ 各被授权调度方的预留（可预留的前提是调度方集合已封闭）；无归属声明时峰值 = 全体争用方同时触发的叠加且叠加项不可枚举 → 不可预留（与 RLP-007 的池守恒同型：容量守恒只在成员封闭时成立）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 调度权归属) ≥ 被调度流程全体 + 其他被授权方 + 所有权登记处（Y1 例外须批准＋退出计划，4.5 @2288-2289）→ 跨单元触达面（单调不减）；归属变更未同步例外的最后负责时刻即触发 Y8 @2303 超期升级（CH-C(2)）`
- **成本**：ops_cost＝随争用方数与归属变更频率上升：每流程须核定归属与裁决路径、每次变更须重算下游新鲜度条款并同步所有权登记处、争用须常态告警；人工判断的相对序为…｜聚合语义=additive
- **反模式** 5 项（P0×1／P1×3／P2×1）：SCH-003-AP1 多方调度同一流程/数据集而无归属声明（事实上共享写）；SCH-003-AP2 归属声明与实际触发权不符（声明者不触发、触发者未声明）；SCH-003-AP3 以 shared_write_exception 长期化替代归属裁决（例…；SCH-003-AP4 争用资源无预留即启用多方调度（峰值不可核算）；SCH-003-AP5 归属变更而下游新鲜度条款与所有权登记处未同步（僵尸归属）
- **兼容性**：SCH-001(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Y1(consumed_by)
- **叙事（收益-成本）**：收益：@2492 把调度冲突与资源竞争的处置定为『归属声明』而非『机制选型』，并给出其法源——逐字『调度权也是所有权的一种，受 Y1 同型约束』
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；anti_patterns: 人工判断；narrative: 交叉表源/骨架源

## kind CFG（源表 5.2.6）

（CFG-001–CFG-004，共 4 条；kind_profile_CFG status=seed；块内按 entry_id 升序）

### CFG-001｜配置 schema 注册

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.6-CFG-01
- **envelope** 延迟分位数 P99：`P99(请求) 随配置求值路径的远端化单调不减：本地常量求值 → 该项趋于下界；远端配置中心拉取或运行时开关求值 → P99 增加 [配置求值时延] 一项，随求值次数与缓存缺失率不减。本条只登记五槽而不确定求值实现 → 母本未给任何数值，只登记界形与单调方向（0.4）；该延迟项不以 cost_profile.latency_budget_delta 双写（@p:CFG#optional）`
- **envelope** 可用性目标（SLO）：`注册表覆盖率 = 已登记项 / 实际行为相关项；覆盖率下降 → 行为漂移的可归因性单调不增（@2512『纪律的潜在旁路』的量化面：未登记项即无判别基准的旁路），事故定位触达面单调不减；母本未给覆盖率下界数值 → 不填数值（0.4）`
- **envelope** 性能：资源占用：`注册表自身占用随已登记配置项数单调不减（五槽 × 项数）；该占用与配置项所控制的运行时资源占用（如池大小）不同轴 → 不得合并计（0.9：池大小的实际取值是登记对象，不是注册表开销）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 任一已登记键的值域) ≥ 该键全体读取方 + 判别谓词的登记处（CFG-002；@2515『仅在登记值域内调参』的边界即本条登记面）→ 随读取方数单调不减；收窄值域另触达在役取值的合法性复核面（等价于把在役取值推为行为级变更，须记 ADR + 批准）`
- **成本**：ops_cost＝随已登记配置项数与变更频率上升：每项须核定五槽、每次变更须判别级别、比对须双侧常态化执行（8.2.4 @3357）；人工判断的相对序为『高于…｜聚合语义=itemwise
- **反模式** 5 项（P0×2／P1×2／P2×1）：CFG-001-AP1 行为相关配置项在用而未登记入注册表（登记表外配置面）；CFG-001-AP2 五槽缺项（键、值域、作用域、级别、生命周期任一为空即计为已登记）；CFG-001-AP3 级别槽一律填 parameter（以级别错填规避行为级判定，使 Z6 的…；CFG-001-AP4 注册表与实际配置长期不比对（8.2.4 @3357 的静态验证未常态化）；CFG-001-AP5 同一逻辑键多形态并存且各自取值（无唯一真相源）
- **兼容性**：CFG-003(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **叙事（收益-成本）**：收益：把『哪些旋钮能改运行时行为』从散落于代码、部署脚本与配置中心的常量变为注册表内的显式清单，使 @2512 所称的『准决策通道』重新受决策纪律约束——@2514 之所以把开关、阈值、路由规则、池大…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### CFG-002｜决策/参数判别谓词

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：5.2.6-CFG-02
- **envelope** 延迟分位数 P99：`判据在变更期/CI 期求值，不在请求路径上 → P99 不随判别次数变化（该项趋于下界）；若 Z 谓词快照采集内嵌于运行时路径（如逐请求求值 interaction_flow.kind）→ P99 增加 [快照采集时延] 一项，随采集频次与被采集谓词数单调不减 → 采集面应置于变更期而非请求期`
- **envelope** 可用性目标（SLO）：`误判率 = 记为 parameter 而快照比对不一致的变更数 / 全部已判别变更数；误判率上升 → 未走 ADR 的行为级变更数单调不减 → 事故的可归因性单调不增（@2512『纪律的潜在旁路』的量化面）；误判率下界为 0（@2517『按硬约束阻塞』即 0 容忍），上界不设数值（0.4 禁假精确 → 按实例核定）`
- **envelope** 性能：资源占用：`快照存储占用随被比对谓词数 × 保留窗口长度单调不减；该占用与配置注册表自身占用（CFG-001 envelope 第三项）不同轴 → 不得合并计（0.9：两者各有唯一真相源）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 判据) ≥ 全体依该判据作出的级别结论 + flag 谓词 level 槽的取值面（@2576）→ 随历史判别数单调不减；判据收窄使既有 parameter 结论须重判为 behavior → 触达面另含补记 ADR 的决策面（成本形态见 typical_reversibility: costly）`
- **成本**：ops_cost＝随变更频率与被比对 Z 谓词数上升：每次变更须取双侧快照并比对、每次结论须落留痕、判据变更须重判存量结论；人工判断的相对序为『高于 CFG-…｜聚合语义=itemwise
- **反模式** 5 项（P0×2／P1×2／P2×1）：CFG-002-AP1 级别判别不经在册判据而由变更者当场作出（运行时即兴判断）；CFG-002-AP2 以参数级变更之名行行为级变更之实（快照比对不一致却记为 paramete…；CFG-002-AP3 判据在册但不可求值（Z 谓词无采集面或无快照，判别退化为人工声称）；CFG-002-AP4 超时值变更未复核 Z4 预算闭合（@2515 括注的升格条件未执行）；CFG-002-AP5 参数级变更未留痕（@2515 义务下限『记录留痕即可』未履行）
- **兼容性**：CFG-001(requires)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z4(consumed_by)
- **叙事（收益-成本）**：收益：把『这次配置改动算不算决策』从变更者的自述变为可求值的判据——@2512 之所以称配置与开关为『准决策通道』，正因其能在不走 ADR 的情况下改变运行时行为
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### CFG-003｜开关生命周期

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.6-CFG-03
- **envelope** 延迟分位数 P99：`生命周期治理在 CI/周期勘察期求值，不在请求路径上 → 该项趋于下界；但本条确引入运行时开关求值界形：flag 谓词逐请求求值时 P99 随活跃开关数单调不减（块头 @6795：按 kind_profile_CFG.optional.reason 但书在此登记界形，不以 latency_budget_delta 双写，避免两处真相 0.9）；且僵尸开关的分支累积使可达路径数单调不减 → 长期上界随之上升（@2516 括注「隐式架构分支」）`
- **envelope** 可用性目标（SLO）：`超期未清理的行为级开关数 → 隐式架构分支数 → 单次变更的意外影响面单调不减 → 事故可归因性单调不增；@3633 明文把「僵尸开关（expiry 超期）」列为汇聚信号源且 Z6 违例在行为级开关上升 P0（@3600「不允许带病发布」）→ SLO 的可达性以 Z6 闭合为上界条件；清理动作自身亦改变可用性（删除一条在用分支 = 行为级变更）→ 清理须过包络校验，不因「只是删开关」而免检`
- **envelope** 性能：资源占用：`开关占用（注册表条目 + 代码分支 + 覆盖两侧路径的测试组合）随未清理开关数单调不减；路径组合数随并发活跃开关数按乘法上升（组合爆炸面，9.2.5 @3658 列为 P2 监测项）→ 资源占用与该乘积同向；本项与 CFG-001 envelope 第三项（注册表自身占用）、CFG-002 envelope 第三项（Z 谓词快照存储占用）三者不同轴 → 不得合并计（0.9：三者各有唯一真相源）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(拆除一个僵尸开关) ≥ 该开关的全部消费路径 + 依赖其分支形态的既有变更 + 覆盖两侧的测试 → 随超期时长单调不减（超期越久，分支被后续变更当作既成结构依赖的概率越高，@2516 逐字「腐化源」）；在 expiry 内拆除的触达单元数以下界为「该开关的直接消费点集」→ 到期纪律的可修改性收益即把该下界锁住，不使其随时间上浮`
- **成本**：ops_cost＝随行为级开关数与超期滞留时长上升：每个开关诞生须写入并核对 expiry、每次勘察须比对全量在册开关、每次到期须作清理或立案的裁决、每次清理…｜聚合语义=itemwise
- **反模式** 5 项（P0×3／P1×1／P2×1）：CFG-003-AP1 行为级开关诞生未带审查期/到期日（expiry 字段缺失）；CFG-003-AP2 行为级开关 expiry 超期且无清理立案（僵尸开关成形）；CFG-003-AP3 行为级开关无 ADR 批准（开关成为不走批准路径的行为变更载体）；CFG-003-AP4 非行为级开关长期滞留未清理（僵尸开关的泛指面：参数级/实验类/灰度类）；CFG-003-AP5 反复顺延 expiry 以规避清理（改期不改物，且顺延未走注册表变更）
- **兼容性**：CFG-001(composable)
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z6(implements)
- **参考文献**：bib 48 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：给『开关终将被拆除』这句意图一个可执行的载体
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；references: 骨架源

### CFG-004｜与 0.10 权力条款的联动

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：5.2.6-CFG-04
- **envelope** 延迟分位数 P99：`联动面在变更期/CI 期求值，不在请求路径上 → 该项趋于下界；『按硬约束阻塞』一旦触发即冻结相关变更 → 变更通过速率单调不增（阻塞面改的是通过速率而非请求延迟）；若快照比对内嵌运行时逐请求求值 → 增加 [快照采集时延]，P99 单调不减，该界形与 CFG-002 envelope 第一项**同轴** → 真相源在 CFG-002，本处不双计（0.9）`
- **envelope** 可用性目标（SLO）：`规避检出率 = 被机器判据捕获的规避数 / 全部规避数；检出率下降 → 未走 ADR 的行为级变更数单调不减 → 事故可归因性单调不增（@2512 的旁路重新打开）；本项的上界条件是快照比对可自动执行（AP3），不可自动执行则检出率的下界为 0 → SLO 的可达性失去该面的保障；@m:235 的批准面不改变该界形（批准是人的裁决，其通过率不作数值登记，0.4）`
- **envelope** 性能：资源占用：`快照采集与比对占用随被比对 Z 谓词数 × 变更频率单调不减——该项与 CFG-002 envelope 第三项（快照存储占用）**同轴**，真相源在 CFG-002 → 本处只登界形不重复计数（0.9）；本条独有的占用面是违例登记与升级裁决材料（候选、依据、包络校验结果、张力，@m:235 逐字的四件结构化材料）→ 随违例数单调不减，与快照占用不同轴`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 联动面) ≥ 全部依快照比对作出的级别结论 + 阻塞通道的门禁配置面 + 违例登记的响应义务面 → 随历史判别数单调不减；撤销机器可查面使其后全部结论失去可复核证据 → 须在窗口内人工重核（typical_reversibility 取 bounded 的界形依据）；改『何为规避』的定义即改 CFG-002 判据 → 回退面并入该条（costly），不在本条重复登记`
- **成本**：ops_cost＝随变更频率与被比对 Z 谓词数上升：每次变更须取双侧快照、比对、落结论，每处差异须走登记与裁决；人工判断的相对序为『高于 CFG-003』（…｜聚合语义=itemwise
- **反模式** 5 项（P0×2／P1×2／P2×1）：CFG-004-AP1 以参数级变更之名行行为级变更之实，且未被硬约束阻塞（规避行为成形）；CFG-004-AP2 Agent 自行批准行为级配置变更（批准闭环由被约束方自身闭合）；CFG-004-AP3 判据在册而快照比对不可自动执行（『机器可查』不成立，联动退化为自述）；CFG-004-AP4 阻塞通道存在但不生效（违例已判定而相关变更未冻结，带病发布）；CFG-004-AP5 以人工复核替代机器可查面，或喂养检查器使比对恒通过（20-A 形态）
- **施加约束** 7 项：方面 1←协调需求在既定风格下不可行 → 回溯约束声明（CH-E 原型通道，阻塞式…；方面 3←协调模式产生的新交互 → 契约登记需求（编排者与参与者间的命令契约、事件…；方面 4←流程状态（协调者状态机、Saga 日志、预扣记录）是数据集合，受 Y1–…；方面 6←质量影响卡片 → 行为级包络校验输入…
- **formal_anchor**：Z6(consumed_by)
- **叙事（收益-成本）**：收益：把 0.10 的权力条款从**声明**变为**可执行面**
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；narrative: 交叉表源/人工判断

## kind QAT（源表 6.2.5）

（QAT-001–QAT-015，共 15 条；kind_profile_QAT status=seed；块内按 entry_id 升序）

### QAT-001｜引入并发

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-01
- **envelope** 延迟分位数 P99：`P99(并发化后) ≤ max［P99(串行基线), 各并行分支 P99 的最大者 + 汇合与同步开销项］；分支数↑ 而分支耗时不均 → 尾延迟受最慢分支支配（max 语义），故 P99 不必然单调下降；母本未给任何数值 → 只登记界形与单调方向（0.4 禁假精确＋6.2.1 @2801 量化纪律）`
- **envelope** 吞吐量：`吞吐量(并发化后) ≤ min［Σ 各分支服务能力, 共享资源上界（锁、连接池、IO 通道）］；分支数↑ 而共享资源上界不变 → 吞吐量趋于上界后不增；母本未给该上界的公式 → 不本地造法（MJ-19 同型），只登记上界存在性与单调方向`
- **envelope** 性能：资源占用：`资源占用 随并行度单调不减：每分支的栈、上下文与缓冲各计一份，另加同步原语开销项；并行度 → 上界时占用进入线性增长段，故本条与 QAT-003（增加资源）在资源轴上同向叠加而不互相替代`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 并发相关逻辑) ≥ 全体读写同一共享状态的单元数 + 竞态回归验证面；并发化把该集合从「串行序的单元」扩展为「交错序的单元对」→ 触达面单调不减（6.4 @2875 可测试性冻结约束的消费端）`
- **成本**：ops_cost＝随并行度与共享状态面同时上升：调试成本非线性（竞态不可复现）、观测面从单路径扩展为分支矩阵、变更回归面按单元对计；人工判断的相对序为『高于 …｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-001-AP1 无基线即并发化（以手段替代目标可达性判定，宣称的改善无对照）；QAT-001-AP2 并发化后新增失败模式未入卡片（卡片存在而 failure_modes 缺…；QAT-001-AP3 以并行度提升替代共享资源上界核定（吞吐量宣称无参数化据）；QAT-001-AP4 竞态缺陷长期不可复现且无取证面（缺陷挂起，观测面缺位被当作无缺陷）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 性能族列举序的首项，也是唯一不改变资源总量与副本拓扑即可换取延迟/吞吐改善的手段——@2839 之所以把达成手段限定在战术注册表内，正是要让「改善性能」这句愿望落到可核查的映…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源/交叉表源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-002｜维持多副本

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-02
- **envelope** 延迟分位数 P99：`读路径：P99(多副本) ≤ P99(单副本) −［就近副本带来的传输时延项］，前提为副本内容满足已声明的一致性级别；写路径：P99 随须同步确认的副本数单调不减（确认面 = 上界）；母本未给任何数值 → 只登记界形与两路径的不同单调方向`
- **envelope** 可用性/可靠性：可用性目标（SLO）、错误预算〔error budget：1 − SLO〕：`SLO(多副本) ≥ SLO(单副本)，且提升幅度随副本间故障独立性单调不减；副本同故障域 → 该项趋于不变（形式冗余）；错误预算的消耗率因单副本失效不再等同服务失效而下降，但复制滞后引发的陈旧读计入预算消耗（6.4 @2880 施加于方面 9 的守护信号参数）`
- **envelope** 性能：资源占用：`资源占用 = 单副本占用 × 副本数 + 复制通道开销项，随副本数单调不减且为线性下界；该线性下界即 @2846 明文代价「成本」的界形（母本未给系数 → 不填数值，0.4）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 数据模型或复制语义) ≥ 全体副本实例 + 复制通道实现 + 冲突解决面；副本数↑ → 变更的验证面按副本数与故障域组合单调不减（6.4 @2877 施加于方面 4 的预算上界的消费端）`
- **成本**：ops_cost＝随副本数与故障域数上升：日常操作面（扩缩、修复、再平衡、脑裂处置）按副本数计，验证面按副本数 × 故障域组合计；人工判断的相对序为『高于 Q…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-002-AP1 副本共享故障域而宣称可用性提升（形式冗余）；QAT-002-AP2 多副本已上线而一致性级别声明未复核（@2846 明文代价未入账）；QAT-002-AP3 有代价可达而代价未量化未入 ADR（以副本数换 SLO 而不记账单）；QAT-002-AP4 复制滞后无观测面（陈旧读不可归因，滞后长期累积）
- **兼容性**：CSL-001(tension)
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)、Q4(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 中唯一同时服务性能族与可用性族的手段——@2841 把它列于性能族（就近副本降低读延迟、副本分担读容量），@2842 的恢复战术（主动冗余/被动冗余/ spare）又以副本底…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-003｜增加资源

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** free｜**origin** hybrid
- **源行**：6.2.5-Q-03
- **envelope** 吞吐量：`吞吐量(增加资源后) ≤ Σ(各资源轴可增区间上限)；上界由最紧轴支配（min 语义）→ 瓶颈轴之外的资源增量对该上界无贡献；母本未给系数 → 只登记界形与支配关系（6.2.1 @2801 量化纪律＋0.4 禁假精确）`
- **envelope** 性能：资源占用：`资源占用 ↑ 单调于吞吐量上界的达成——本条的定义性后果（以资源换指标）；占用与产出的比值（单位资源成本）母本未给系数 → 只登记单调方向，不填数值（0.4）`
- **envelope** 延迟分位数 P99：`P99 ↓ 仅在瓶颈为资源饱和时成立（等待队列长度随水位上升 → 增容即降排队）；瓶颈为串行依赖或远端往返时资源增量对 P99 无改善上界（该场合归 QAT-001 引入并发或 QAT-004 减少开销）→ 方向条件化，不得裸写下降（@2801 禁止裸陈述）`
- **envelope** 可伸缩性：单位资源增量带来的容量增量：`容量增量 ÷ 资源增量 ∈ [实测下界, 实测上界]——@2796 逐字指标名，为本条的唯一收益判据；母本未给该系数取值 → 按实例勘察（SO-15）；系数趋于零即本条对目标不可达，判定回馈走 6.4 @2874「不可达 → 候选重审或升级」`
- **成本**：ops_cost＝随资源规模上升而语义复杂度不升：无新增交错语义、无跨副本一致性负担，日常操作面为供给与回收；人工判断的相对序为『低于 QAT-001（引入并…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-003-AP1 未做瓶颈归因即扩容（以资源增量替代目标可达性判定）；QAT-003-AP2 有状态服务直接横向扩容（会话与状态未外置即增实例）；QAT-003-AP3 扩容后瓶颈迁移而未复核上界（宣称的容量增量不可复现）；QAT-003-AP4 资源长期闲置而无回收路径（成本沉没，预算出处未复核）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 性能族列举序中唯一不改变程序结构即可换取容量与延迟改善的手段——@2839 之所以要求达成手段从战术注册表选择，正是要让「加机器」这类愿望也落到可核查的映射上（Q6 @2913…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-004｜减少开销

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-04
- **envelope** 延迟分位数 P99：`P99(命中路径) ≤ P99(基线) −［被消除的开销项］；P99(未命中路径) ≥ P99(基线)（另加查找与回填项）→ 整体分位数由命中率支配，命中率 → 下界时本项无改善；母本未给命中率取值 → 只登记两路径的不同单调方向（0.4＋@2801）`
- **envelope** 吞吐量：`吞吐量 ≤ min［Σ 后端服务能力, 命中率决定的等效放大上界］；批处理形态下另受批量大小与等待窗口制约（批量 ↑ → 单请求排队时延 ↑）→ 吞吐与延迟在本条内存在方向冲突，不得同时裸写两者改善（@2801）`
- **envelope** 性能：资源占用：`资源占用 ↑ 单调于缓存容量与批量缓冲：缓存本身占用内存或存储，批处理占用缓冲与等待窗口 → 本条以资源换开销，与 QAT-003 在资源轴上同向叠加；母本未给容量系数 → 不填数值（0.4）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数(Δ 被缓存的数据模型或批量边界) ≥ 全体读写该数据的单元 + 失效路径实现 + 陈旧窗口的消费端；缓存把「一处取数」扩展为「取数 + 失效 + 陈旧判定」三面 → 触达面单调不减（6.4 @2875 可测试性冻结约束的消费端）`
- **成本**：ops_cost＝随缓存层数与失效路径复杂度上升：日常操作面为容量管理、预热与失效处置，验证面按「取数 + 失效 + 陈旧判定」三面计；人工判断的相对序为『高…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-004-AP1 缓存无新鲜度条款即上线（陈旧窗口未声明，@2846 明文代价未入账）；QAT-004-AP2 缓存无失效路径（陈旧不可界，与权威源的分歧不可检测）；QAT-004-AP3 以宣称的命中率替代实测（收益无参数化据）；QAT-004-AP4 命中率长期下降而无告警（收益消失不可归因）
- **兼容性**：CSL-004(tension)
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)、Q4(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 性能族列举序中唯一以**消除或摊薄既有开销**为手段的战术（前四条分别改结构、改拓扑、改资源、改并行度），故其收益上界由现状开销占比直接决定——占比高则收益大，占比低则本条不…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-005｜限制排队

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** free｜**origin** hybrid
- **源行**：6.2.5-Q-05
- **envelope** 延迟分位数 P99：`P99 ≤ max［队列上界对应的等待时延, 后端服务时延］——上界把尾延迟从「无界排队支配」转为「上界支配」，本项为本条的**主收益面**；母本未给上界取值 → 只登记支配关系与 max 语义（0.4＋@2801）`
- **envelope** 可用性/可靠性：可用性目标（SLO）、错误预算〔error budget：1 − SLO〕：`SLO ↑ 于过载场合（拒绝部分请求以保全整体），同时错误预算消耗率 ↑ 于拒绝率（二者同向变化而方向相反于目标）→ 不得裸写 SLO 改善而不入账拒绝（6.4 @2880 施加于方面 9 的守护信号参数）`
- **envelope** 吞吐量：`吞吐量 ≤ 后端可持续服务能力——本条不抬高该上界，只**截断崩溃段**（超越上界后吞吐量随排队深度下降的区段）；故本条与 QAT-003 增加资源在吞吐轴上不同据：彼条抬高上界，本条防止越过上界后的劣化`
- **envelope** 性能：资源占用：`资源占用 ≤ 队列上界对应的缓冲占用（有界即占用有上界）；无界排队下占用单调不减直至耗尽 → 本项为本条的第二收益面（耗尽防护），与 envelope 第一项共用同一上界参数（一处真相，0.9）`
- **成本**：ops_cost＝随排队点数量上升：每个排队点各需一套上界参数与观测面；语义复杂度低（无交错、无陈旧），但参数须随负载形态变化持续复核 → 属**持续运维**…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-005-AP1 无界排队而宣称可用性目标（资源耗尽显效前的宣称无据）；QAT-005-AP2 拒绝无计数（错误预算不入账，代价不可见）；QAT-005-AP3 上界取值无实测据（裸数值或由愿望推得）；QAT-005-AP4 上界命中频次无趋势监测（取值过低长期不被发现）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 性能族列举序中唯一**不提升能力**的战术——前四条都在扩大系统能做的事，本条限定系统该承受多少
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-006｜故障检测

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：6.2.5-Q-06
- **envelope** 可用性可靠性：SLO、错误预算〔1 − SLO〕、MTTR、RPO/RTO：`MTTR ≥ 检测时延 + 判定与接管时延 + 恢复动作时延——检测时延为 MTTR 的**首项下界**，本条只压缩首项，故改善上界由现状首项占比决定（可实测，@2852）；母本未给任何时延数值 → 只登记构成项与下界语义（0.4＋@2801）`
- **envelope** 可用性目标（SLO）：`SLO ↑ 于失效可被及时检出的场合（未检出的失效期全额计入不可用时长），同时错误预算消耗率 ↓ 于检测时延（二者反向）→ 不得裸写 SLO 改善而不入账误报与接管代价（6.4 @2880 施加于方面 9 的守护信号参数）`
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`满足率 ↑（本条即若干 observability_requires 项的供给面：健康信号、失效判定信号）；追踪覆盖率 → 检测覆盖率的相邻据（未纳入追踪的单元亦难纳入检测，AP2）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于探针与信号汇聚开销（与探测频率同向、单调不减）；该增量须入包络预算而非视为免费（5.2.5 @2508 卡片不豁免质量预算，Z7 对偶）`
- **成本**：ops_cost＝随被检测单元数与探测频率上升：告警面按单元计、阈值维护按失效形态计；语义复杂度中（须处置假阳性与 flapping，属持续调参而非一次性投入…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-006-AP1 无检测信号而宣称可用性目标或 MTTR（首项不可核算即目标值无出处）；QAT-006-AP2 检测覆盖不全而按全覆盖宣称（部分单元无心跳或看门狗纳管）；QAT-006-AP3 检测阈值与去抖动窗口无实测据（裸数值或由愿望推得）；QAT-006-AP4 误报率与检测时延无趋势监测（假阳性长期不被归因，flapping 不可见…
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 可用性族列举序的**首项**，其收益不表现为能力提升而表现为「不可用时长变得可核算且可压缩」——MTTR 的首项即检测时延（envelope 第一项的下界语义），故本条是后两…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-007｜恢复

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-07
- **envelope** 可用性可靠性：SLO、错误预算〔1 − SLO〕、MTTR、RPO/RTO：`RTO ≥ 检测时延 + 切换编排时延 + 状态重建时延（三形态的差别在第二、三项：主动冗余 ≈ 0、被动冗余含激活项、spare 含装配与加载项）；RPO ≥ 复制滞后上界（异步形态下非零，同步形态下趋零而其延迟代价入 envelope 第四项）→ 二者构成 6.4 @2877 施加于方面 4 的预算上界；母本未给任何数值 → 只登记构成项与下界语义（0.4＋@2801）`
- **envelope** 可用性目标（SLO）：`SLO ↑ 于失效后可恢复的场合（不可用时长由 RTO 支配而非由修复时长支配）；同时错误预算消耗率 ↓ 于 RTO（反向）→ 不得裸写 SLO 改善而不入账切换期失败与数据丢失窗口（6.4 @2880 施加于方面 9）`
- **envelope** 延迟分位数 P99：`P99 ↑ 于切换期（尖峰，其宽度由 RTO 支配）；主动冗余与同步形态下 P99 ↑ 于常态写路径（跨副本协调开销，与 QAT-002 @7421 的 consistency_impact 同据）→ 本项为本条的常态代价面，不得只登记切换期收益`
- **envelope** 性能：资源占用：`资源占用 ↑ 于冗余度（三形态递减序：主动冗余 > 被动冗余 > spare，单调关系而非数值）；该增量为**常驻**而非条件项 → 与 QAT-006 的探测开销不同轴（彼为频率项、此为容量项），须分列登记（一处真相，0.9）`
- **成本**：ops_cost＝随冗余度与故障域数上升：演练面按切换路径计、仲裁与 fencing 面按副本组计、资源面为常驻；语义复杂度高（脑裂处置、数据水位对齐、切换后…｜聚合语义=itemwise
- **反模式** 4 项（P0×2／P1×1／P2×1）：QAT-007-AP1 无恢复路径而声明 RTO/RPO（宣称无承载面）；QAT-007-AP2 RTO/RPO 宣称值未经切换演练实证（愿望值充当目标值）；QAT-007-AP3 切换无 fencing（双主双写，数据分歧不可自愈）；QAT-007-AP4 演练频次与冗余容量无趋势监测（恢复能力静默退化）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条把「失效后多久恢复、丢多少数据」从不可控变为可声明且可实证——RTO 与 RPO 是 4.4 @2253 母本定义的两个可容忍窗口，本条是其在战术面的唯一承载者
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-008｜故障预防

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-08
- **envelope** 可用性目标（SLO）：`SLO ↑ 于失效发生率下降（本条的**主收益面**：错误预算消耗率 ↓ 于失效率，二者反向）；不得裸写 SLO 改善而不入账常态开销与重启代价（6.4 @2880 施加于方面 9 的守护信号参数）`
- **envelope** 可用性可靠性：SLO、错误预算〔1 − SLO〕、MTTR、RPO/RTO：`失效率 ↓ → MTTR 的期望贡献 ↓（发生率与时长二者相乘构成不可用时长）；事务形态下 RPO → 0（提交点即恢复点，无丢失窗口）；本条与 QAT-007 在该式上互补而非替代（彼压时长、此压发生率）；母本未给任何数值 → 只登记构成关系（0.4＋@2801）`
- **envelope** 延迟分位数 P99：`P99 ↑ 于事务协调与提交开销（常驻项，与事务范围同向、单调不减）；过程监视器形态下 P99 ↑ 于重启期尖峰（条件项）→ 本项为本条的常态代价面，须与 envelope 第一项的收益同表登记（不得只登收益，5.2.5 @2508 Z7 对偶）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数 ↑ 于事务边界侵入（提交点、回滚路径、锁范围三面均须随业务变更同步修改）；该增量为 6.4 @2875 施加于方面 2 的可测试性冻结约束的直接消费端 → 不得视为一次性投入`
- **成本**：ops_cost＝事务形态：随事务范围与竞争面上升（死锁处置、长事务治理、回滚路径维护），属**持续运维**；过程监视器形态：随被监视单元数上升（阈值与重启上…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-008-AP1 宣称状态不半写而无事务边界登记（原子性宣称无承载面）；QAT-008-AP2 过程监视器无重启上限（flapping：反复重启放大不可用时长）；QAT-008-AP3 事务范围无实测据（范围由偏好推得，长事务与锁竞争不可归因）；QAT-008-AP4 失效率无趋势监测（预防效果不可判定，收益宣称长期不被证伪）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 可用性族列举序的**末项**，其收益轴与前两项不同——QAT-006 让失效可见、QAT-007 让失效可恢复，本条让失效**不发生**
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-009｜语义内聚

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-09
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数 ↓ 于典型变更（本条的**主收益面**：同一业务语义收敛到单一单元 → 触达面由「散落处数」降为「一处」）；下界为 1（不可为零，变更必触达承载单元）；母本未给任何数值 → 只登记方向与下界语义（0.4＋@2801）`
- **envelope** 可修改性：变更前置时间：`变更前置时间 ↓ 于触达单元数（同向，二者构成因果链：触达面收窄 → 协调与验证面收窄 → 前置时间下降）；该链的每一环须可实测，否则前置时间改善不可归因于本条（AP2）`
- **envelope** 可修改性：DSM 密度（2.2.4 通道二的消费端之一）：`DSM 密度 ↓ 于重排（块对角化：同语义单元间的依赖集中于对角块，跨块依赖减少）；密度为本条的**可判定代理面**（内聚本身不可直接度量）→ 无密度实测即内聚宣称无据（AP1）`
- **envelope** 可修改性：跨边界契约变更数：`跨边界契约变更数 ↑ 于重排期（一次性代价：边界移动即契约变更，须走 CTR 批的兼容性规则与破坏性变更流程）；重排完成后 ↑ 或 ↓ 取决于新边界与语义的对齐度 → 本项为本条的**过渡代价面**，不得只登记稳态收益`
- **成本**：ops_cost＝运行时运维面近似无增量（无新组件、无新告警面）；**变更期**成本高：重排为结构级变更，须一次性承担契约迁移、回归验证与所有权调整；重排后须…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-009-AP1 宣称内聚而无 DSM 密度与变更案例回溯实测据（内聚沦为形容词）；QAT-009-AP2 重排而所有权与 seam 未同步（结构改了而认知负荷与可测试性未改）；QAT-009-AP3 重排期跨边界契约变更未登记（破坏性变更扩散到消费方）；QAT-009-AP4 DSM 密度无持续核算（重排后依赖再度蔓延，收益静默退化）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 可修改性族列举序的**首项**，其收益机制是把「一起变更的东西放在一起」——判据来自变更案例回溯而非开发者的语义直觉（6.2.1 @2795 度量方式），代理面来自 DSM …
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-010｜限制依赖

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-10
- **envelope** 可修改性：跨边界契约变更数：`跨边界契约变更数 ↓ 于依赖收敛（本条的**主收益面**：契约变更的传播面由「全部依赖方」收窄为「规则允许的依赖方」，界形为受依赖规则约束的上界）；下界为 1（契约变更必触达其直接消费方）；母本未给任何数值 → 只登记方向与下界语义（0.4＋@2801）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数 ↓ 于依赖收敛（同向：传播面收窄即触达面收窄）；但**引入期 ↑**（既有违例的整改为一次性结构变更）→ 本项须分「引入期」与「稳态期」两段登记，不得只登稳态收益`
- **envelope** 可修改性：DSM 密度（2.2.4 通道二的消费端之一）：`DSM 密度 ↓ 于规则执行（跨块依赖与环形依赖减少）；密度与违例数为本条的**可判定代理面**（「依赖受控」本身不可直接度量）→ 无实测即受控宣称无据（AP1）`
- **envelope** 延迟分位数 P99：`P99 ≥ 基线值 于依赖收敛（代价面：规则若强制经由契约层或中介层调用，则路径跳数不减 → 延迟单调不减；本项**不含改善主张**，改善归 QAT-001…005）；母本未给数值 → 只登记方向（0.4＋@2801）`
- **成本**：ops_cost＝运行时运维面近似无增量（无新组件，除静态分析闸口的构建期成本）；**引入期**成本高：既有违例整改为结构级变更，须一次性承担迁移与回归验证；…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-010-AP1 宣称依赖受控而无机器可查的规则与违例实测（受控沦为口号）；QAT-010-AP2 规则在册而无执行闸口（违例持续引入，规则随时间失效）；QAT-010-AP3 依赖被压入隐式通道（反射、共享库、共享数据库、配置注入绕过规则）；QAT-010-AP4 违例数与 DSM 密度无持续核算（规则执行后依赖再度蔓延，收益静默退化）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 可修改性族列举序的**第二项**，其收益机制不是搬动代码而是**约束变更的传播路径**——把「谁能依赖谁、经由何种契约」定为可机器查的规则，使一次契约变更的触达面由「全部依赖…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-011｜参数化配置

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：6.2.5-Q-11
- **envelope** 可修改性：变更前置时间：`变更前置时间 ↓ 于参数化（本条的**主收益面**：该取值的变更由「代码改动 + 发布」降为「配置变更 + 分发」，界形为两条路径前置时间之差）；下界为配置分发与生效确认的时延（不可为零）；母本未给任何数值 → 只登记方向与下界语义（0.4＋@2801）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数 ↓ 于参数化，且**下界为 0**（配置变更可不触达任何代码单元；与 QAT-009 @8038 的下界 1 不同——彼条变更必触达承载单元，本条的承载单元为配置项而非代码）；但配置点数 ↑ → 组合与测试面 ↑（代价面，见 failure_modes 第一项）`
- **envelope** 可修改性：跨边界契约变更数：`跨边界契约变更数 ↑ 于配置面扩张（代价面：配置 schema 即契约——5.2.6 @2514 的 {键, 值域, 作用域, 级别, 生命周期} 五元组为消费方所依赖，schema 变更须走契约的兼容性处置）→ 本项为本条的**代价面**，不得只登记稳态收益`
- **envelope** 可用性目标（SLO）：`SLO ↓ 于误配置（风险面：配置错误即失效注入点，其消耗计入错误预算〔1 − SLO，6.2.1 @2794〕）；界形为「值域校验覆盖率 → 误配置失效率的上界收敛项」，母本未给数值 → 只登记方向（0.4＋@2801）`
- **成本**：ops_cost＝运行时运维面**高于** QAT-009／QAT-010：本条引入新的持续运维对象——配置分发面、生效核对面、审计面与到期清理面（属持续运维…｜聚合语义=itemwise
- **反模式** 4 项（P0×2／P1×1／P2×1）：QAT-011-AP1 宣称变更无需发布而配置项未入 schema 注册（收益与治理双失据）；QAT-011-AP2 无值域校验即上线配置点（非法值直达运行时，配置成为失效注入点）；QAT-011-AP3 配置面膨胀（预期变动面之外的取值也被参数化，组合爆炸）；QAT-011-AP4 行为级开关无 expiry 或到期未清理（僵尸开关 = 隐式架构分支）
- **兼容性**：CFG-001(requires)
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 可修改性族列举序的**第三项**，其收益机制是把预期会变的取值从代码中抽出，使该取值的变更由「代码改动 + 发布」降为「配置变更 + 分发」——收益量即两条路径的前置时间差（…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-012｜抽象中介

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-12
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数 ↓ 于中介化（本条的**主收益面**：实现替换的触达面由「全部调用点」收窄为「中介的实现侧」），且**下界为 1**（中介本身即承载单元，与 QAT-011 @8215 的下界 0 构成结构差别——彼条的承载单元为配置项而非代码）；但**引入期 ↑**（全部调用点改经中介为一次性结构变更，其范围与调用点数成正比）→ 本项须分「引入期」与「稳态期」两段登记，不得只登稳态收益`
- **envelope** 可修改性：跨边界契约变更数：`跨边界契约变更数 ↓ 于中介化（收益面：实现替换不外溢为契约变更，前提是中介契约稳定），**下界为 0**（中介契约不变时实现替换不产生契约变更）；但中介契约自身的变更即契约变更，且其传播面为**全部调用点**（代价面，见 failure_modes 第三项）→ 本项两面并存，不得只登记收益方向`
- **envelope** 延迟分位数 P99：`P99 ≥ 基线值 于中介化（代价面：每次调用增加一跳，其序列化与转发项单调不减；本项**不含改善主张**，改善归 QAT-001…005）；本条为可修改性族四条中唯一其运行时项在每次调用上皆非零者 → 母本未给数值，只登记方向与单调性（0.4＋@2801）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于中介化（代价面：中介层的实例、内存与连接池为新增占用；中介若为独立部署单元则增量为整实例级）；母本未给数值 → 只登记方向与增量形态（0.4＋@2801）`
- **成本**：ops_cost＝**变更期**成本低于 QAT-009／QAT-010（增量引入而非结构重排，与 QAT-009 @8064 已登记的相对序一致）而高于 Q…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-012-AP1 宣称实现可替换而中介无 seam（替换不可验证，抽象沦为声明）；QAT-012-AP2 抽象泄漏（调用方仍依赖被抽象实现的行为细节）；QAT-012-AP3 为单一实现引入中介（无第二实现且无预期变动面，净增跳数与复杂度）；QAT-012-AP4 跳数增量与触达单元数无持续核算（收益宣称失据，代价静默累积）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 可修改性族列举序的**第四项（末项）**，其收益机制是在调用方与实现之间插入中介，使「替换实现」的触达面由全部调用点收窄为中介的实现侧（envelope 第一项），并使替换不…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-013｜抵抗攻击

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** irreversible｜**origin** hybrid
- **源行**：6.2.5-Q-13
- **envelope** 安全：攻击面清单闭合率、漏洞修复时限、敏感数据访问路径合规率：`攻击面清单闭合率 ↑ 于本条（**主收益面**：认证/授权/加密三机制分别闭合「身份不可信」「访问越权」「数据明文」三类攻击面），界形为「闭合率 → 1 的上界收敛项，其分母为在册攻击面清单的全集」；敏感数据访问路径合规率同向 ↑（Y5 @2297 的判定面）；漏洞修复时限 ↓（@2797 在册指标，其目标值须由监管条文或合同 SLA 给出）；母本未给任何数值与目标值 → 只登记方向与分母语义（0.4＋@2801：目标值四者之外无合法来源）`
- **envelope** 延迟分位数 P99：`P99 ↑ 于本条（代价面：认证校验、授权判定与加解密三项均在请求路径或数据路径上，其项单调不减；本项**不含改善主张**）；母本未给数值 → 只登记方向与三项的可分离性（0.4＋@2801）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（代价面：加解密的 CPU 项与数据量成正比、密钥与凭据的存储项、授权判定缓存的内存项）；母本未给数值 → 只登记方向与增量形态（0.4＋@2801）`
- **envelope** 可用性目标（SLO）：`SLO ↓ 于本条（风险面：认证与授权服务成为新的关键依赖，其不可用即全路径不可用；密钥丢失即数据不可恢复而 RPO 失效）；其消耗计入错误预算〔1 − SLO，@2794〕；母本未给数值 → 只登记方向（0.4＋@2801）`
- **成本**：ops_cost＝运行时运维面**高于**可修改性族四条：本条引入四类持续运维对象——密钥托管与轮换、凭据与令牌服务、授权策略的集中治理、漏洞修复的时限跟踪（…｜聚合语义=itemwise
- **反模式** 4 项（P0×2／P1×1／P2×1）：QAT-013-AP1 宣称已加密而密钥无独立托管与轮换（密钥与密文同存，加密名存实亡）；QAT-013-AP2 以传输加密替代存储加密（数据落盘仍明文，存储面未覆盖）；QAT-013-AP3 授权判定分散于各单元（策略不一致，攻击面清单的分母不可枚举）；QAT-013-AP4 漏洞修复时限无持续核算（在册指标未测量，修复积压不可见）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 安全族列举序的**第一项**，其括注「认证/授权/加密」为三个手段面而非三条战术（母本未分列 → 不本地拆分），三者分别闭合「身份不可信」「访问越权」「数据明文」三类攻击面，…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### QAT-014｜检测攻击

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：6.2.5-Q-14
- **envelope** 安全：攻击面清单闭合率、漏洞修复时限、敏感数据访问路径合规率：`敏感数据访问路径合规率 ↑ 于本条（**主收益面**：Y5 @2297 的 lineage_complete 合取项以审计记录为核算源，无记录即合规率不可判定）；攻击面清单闭合率同向 ↑（检测使未闭合项可见，其增量为**可见性**而非抵抗面，抵抗面归 QAT-013 → 不得双计）；漏洞修复时限 ↓（检测发现的漏洞进入修复跟踪，@2797 在册指标）；母本未给任何数值与目标值 → 只登记方向与分母语义（0.4＋@2801：目标值四者之外无合法来源）`
- **envelope** 可观测性：卡片 observability_requires（5.2.5）满足率、追踪覆盖率：`满足率 ↑ 与追踪覆盖率 ↑ 于本条（本条为 @2799 两项指标的**直接生产面**，全批十五条中唯一：其余各条只是该两项指标的消费端）；界形为「满足率 → 1 的上界收敛项，其分母为在册卡片 observability_requires 项数之和；覆盖率 → 1 的上界收敛项，其分母为已枚举访问路径全集」；母本未给数值 → 只登记界形与分母语义（0.4＋@2801）`
- **envelope** 可用性目标（SLO）：`SLO ↓ 于本条（代价面：审计记录写入在请求路径上，同步写失败可致请求失败；日志载体成为新的集中单点，其不可用即检测面全失）；其消耗计入错误预算〔1 − SLO，@2794〕；母本未给数值 → 只登记方向（0.4＋@2801）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（代价面：日志写入的 I/O 项与存储项皆与访问次数成正比、留存期越长占用越高，关联分析的周期性计算项）；母本未给数值 → 只登记方向与增量形态（0.4＋@2801）`
- **成本**：ops_cost＝稳态运维面**与 QAT-013 同级而高于 QAT-015、高于可修改性族四条**：本条引入四类持续运维对象——日志载体的容量与留存期治理…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：QAT-014-AP1 宣称已检测而敏感数据访问路径无审计记录（Y5 的 lineage_com…；QAT-014-AP2 审计记录可被当事方删改，或留存期未登记（检测面在事后失效）；QAT-014-AP3 只采集不告警（无检测规则与响应路径，日志堆积而攻击仍不可见）；QAT-014-AP4 追踪覆盖率无持续核算（@2799 在册指标未测量，覆盖面漂移不可见）
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)、Y5(consumed_by)
- **叙事（收益-成本）**：收益：本条是 6.2.5 安全族列举序的**第二项**，其括注为「手段＋联动面」双成分（手段＝审计日志，联动面＝Y 域血缘），故与 QAT-013 的「手段列举」型括注不同——本条的联动面唯一可定，是…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；anti_patterns: 人工判断

### QAT-015｜从攻击恢复

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：6.2.5-Q-15
- **envelope** 安全：攻击面清单闭合率、漏洞修复时限、敏感数据访问路径合规率：`攻击面清单闭合率 ↑ 于本条（**主收益面**：限流与熔断使「资源耗尽」与「级联失败」两类攻击面闭合）；界形为「越阈流量的拒绝率 → 1 的上界收敛项，其阈值为参数化项而非定值（出处须为现状基线测量，@2801 四者之一）」；漏洞修复时限与敏感数据访问路径合规率**不因本条直接改善**（本条为事后止损，不消除漏洞本身、不改变访问路径的血缘面）→ 只登记闭合率一项的方向，不据此宣称全行改善（0.4）`
- **envelope** 可用性目标（SLO）：`SLO 双向于本条：正向 ↑（级联失败被切断，单点过载不拖垮全局，@2486 断路器与舱壁的保全面）；反向 ↓（**误伤面**：阈值过严或来源标识不准时正常请求被拒）→ 两面并存，须以错误预算〔1 − SLO，@2794〕统一核算，不得只登收益面；MTTR 同向 ↓（止损使恢复时点提前，@2794 在册指标）；母本未给数值 → 只登记双向性（0.4＋@2801）`
- **envelope** 延迟分位数 P99：`P99 双向：常态下 ↑（计量与阈值判定的请求路径项，量级为安全族三条中最低）；过载下 ↓（快速失败替代排队等待）——其后一面与 QAT-005 限制排队的手段面重叠，该重叠归 QAT-005 而本条不双计（latency_budget_delta 已明文）；本项**不含单向改善主张**；母本未给数值 → 只登记双向性与可分离性（0.4＋@2801）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（代价面：计量与滑动窗口的内存项、阈值判定的每请求计算项、半开探测的周期性项）；母本未给数值 → 只登记方向与增量形态（0.4＋@2801）`
- **成本**：ops_cost＝稳态运维面**低于 QAT-013／QAT-014 而高于 QAT-011**：本条引入三类持续运维对象——阈值的周期性重标定（流量基线漂移…｜聚合语义=itemwise
- **反模式** 4 项（P1×3／P2×1）：QAT-015-AP1 以止损替代抵抗与检测（限流/熔断在册而漏洞仍在、攻击仍不可见）；QAT-015-AP2 阈值无出处（由假定而非基线测量推得）；QAT-015-AP3 熔断后无半开探测（熔断不可自愈，须人工复位）；QAT-015-AP4 静默降级（止损已发生而无告警与归因）
- **兼容性**：RLP-006(requires)
- **施加约束** 8 项：方面 1←三值判定回馈候选集：不可达 → 候选重审或升级；方面 2←可测试性冻结约束：每单元必有 seam（0.15 → W1，双方不得单方…；方面 3←延迟/可用性目标与错误预算 → 已发布契约的 SLA 条款（P99 等）；方面 4←RPO/RTO 与一致性目标 → 存储拓扑与流动机制的预算上界…
- **formal_anchor**：Q6(implements)、Q5(triggers)
- **叙事（收益-成本）**：收益：本条是 6.2.5 安全族列举序的**第三项**，其括注为「手段＋联动面」双成分（手段＝限流与熔断，联动面明文指向 5.2.3），故本条是本批安全族三条中唯一有可登记 peer 者（requir…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；narrative: 骨架源/交叉表源

## kind VFM（源表 8.2.1）

（VFM-001–VFM-006，共 6 条；kind_profile_VFM status=seed；块内按 entry_id 升序）

### VFM-001｜静态分析

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** free｜**origin** hybrid
- **源行**：8.2.1-T-01
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`触达单元数 ↓ 于本条（**主收益面**：@3354 的依赖规则检查使 V1/W4/X1 类结构性违例在提交时即被检出，违例不被累积 → 后续变更的触达单元数以下界为「合规结构下的最小触达集」；界形为**下界收敛项**，其阈值为参数化项而非定值，出处须为现状基线测量，@2801 四者之一）。就近族映射理由：本条守护的是结构性性质，其失守的直接后果是变更触达面膨胀 → 落 @2795 可修改性族（6.2.1 无 kind_profile_VFM note（@d:registry/profiles.yaml#key-profiles[12].entry_level_exemptions）期望的「检出能力/覆盖/误报率」在册形态，该期望面差异登 G-VFM-1）`
- **envelope** 可修改性：DSM 密度（2.2.4 通道二的消费端之一）：`DSM 密度 ↓ 于本条（@3355 逐字「DSM 通道二全量消费（2.2.4）：发布节点的全量 DSM + 聚类 + W5 语义对照，结果入证据库」——本条是该消费端的执行手段，聚类结果的语义对照使非预期耦合可见 → 密度单调不增；界形为**不减项的反向**，即密度上界由发布节点的聚类阈值参数化，阈值为参数化项，出处须为现状基线测量）。就近族映射理由：@3355 明文把 DSM 通道二归入本条 → 直接取 @2795 族的 DSM 密度形态，无须映射推断`
- **envelope** 合规：监管条款 → 可判定谓词的映射覆盖率：`映射覆盖率 ↑ 于本条（@3390 逐字「合规验证要求（监管条文 → 强制验证项与证据留存期，**外部显式指定**）」——本条把可静态判定的条文映射为依赖或暴露面约束，映射面越大则须由人工评审（VFM-005）兜底的条文越少；界形为 **→ 1 的上界收敛项**，其上界为「可静态判定条文占全部强制验证项之比」，该比值是参数化项而非定值，出处须为监管条文清单与现状基线测量）。就近族映射理由：合规族（@2798）是本条唯一有**外部显式指定**权威的收益面，映射覆盖率即其可参数化形态`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（**代价面**：静态分析工具在 CI 上的计算与内存项，量级随被检代码规模与规则数单调不减；界形为**不减项**，其上界由 CI 资源预算参数化——@3483 逐字「执行成本超出交付空间预算（CI 时长上限有出处：发布节奏要求）」即该预算的出处形态，出处为业务方书面目标或现状基线测量）。就近族映射理由：本条不进入运行时请求路径（latency_budget_delta 据此省略），其代价只落在 CI 侧 → 取 @2793 性能族的资源占用形态而非延迟形态`
- **成本**：ops_cost＝稳态运维面**低于 VFM-004 而高于 VFM-003**：本条无运行时开销（不进入请求路径）、无测试资产管理面，但有**规则集维护面*…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×2／P2×1）：VFM-001-AP1 结构性硬性质只有叙事性结论、无静态检查程序（「架构我们看过了没问题」而在…；VFM-001-AP2 适应度函数在册而未接线到 CI（规则写就但无触发点，检查从不运行）；VFM-001-AP3 DSM 通道二未在发布节点全量消费（只跑增量或只跑聚类、不做 W5 语义…；VFM-001-AP4 配置注册表比对缺项（只比一侧，或比对的注册表版本非当前版）
- **兼容性**：CFG-001(requires)
- **施加约束** 5 项：方面 0←验证结论三值（pass/fail/escalate）：fail 于硬性质…；方面 7←证据工件 → ADR 引用源（T-F3）；方面 1←测试策略适配回馈（1.4 接收项的执行端）：验证成本过高的风格组合 → …；方面 9←失真信号、幻觉套件清单、长期失败用例 → 腐化监测输入…
- **formal_anchor**：T1(implements)
- **参考文献**：bib 13 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：本条是 @3329 手段映射注册表六类的**第一项**，其括注「结构性性质 V1/W4/X1 类」界定了它的独占作用面——**不运行系统即可判定**的性质族
- **数据来源层**（yaml 行内注释）：provenance: 骨架源/交叉表源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### VFM-002｜可执行检查程序

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：8.2.1-T-02
- **envelope** 可修改性：变更前置时间：`变更前置时间 ↓ 于本条（**主收益面**：@185 逐字「决策变更 → 自动重跑所有绑定其上的性质检查 → 违例即阻塞（硬性质）或标记（软性质）」——重跑为自动即无须人工排期复核，前置时间以下界为「触发点到结论产出的机器时延」；界形为**下界收敛项**，其阈值为参数化项而非定值，出处须为现状基线测量或业务方书面目标（@2801 四者之一）。就近族映射理由：本条的收益是**判定权的机器化**（T-F1），其直接后果是复核等待从关键路径移出 → 落 @2795 可修改性族的前置时间形态而非触达单元数形态（触达面不因判定方式改变）`
- **envelope** 合规：监管条款 → 可判定谓词的映射覆盖率：`映射覆盖率 ↑ 于本条（@3390 逐字「合规验证要求（监管条文 → 强制验证项与**证据留存期**，外部显式指定）」——本条把条文映射为白板谓词上的可判定命题，并以 @3373「合规出处（监管留存要求）**覆盖登记值**（外部显式指定权威最高）」承载留存期；界形为 **→ 1 的上界收敛项**，其上界为「可判定条文占全部强制验证项之比」，该比值是参数化项而非定值，出处须为监管条文清单与现状基线测量）。就近族映射理由：合规族（@2798）是本条唯一有外部显式指定权威的收益面；@2798 度量列逐字「审计、Y5/G 系列」——审计的可重放要求（@3372「审计方」明文列为重放主体）即本条的产出面`
- **envelope** 可观测性：追踪覆盖率：`追踪覆盖率 ↑ 于本条（@3371 七要素的第四项逐字「执行记录（CI 运行标识、环境描述）」＋@3372「任何有访问权的一方（人类评审者、后续 Agent、审计方）凭工件可重执行得到同一结论」——执行记录的可追及面即追踪覆盖，其下界为「每个入库工件均可回指唯一执行记录」；界形为**下界项（→ 全覆盖）**，未达即 @3372 末句「不可重放的『证据』降级为线索」。就近族映射理由：本条的产出是证据工件而非运行时行为，故不取 @2793 延迟族；@2799 可观测性族的追踪覆盖率形态是唯一能表达「工件 ↔ 执行记录」可追及性的在册形态，度量列逐字「基础设施勘察」与本条的勘察面同源`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（**代价面**：检查程序的执行项 + 证据工件的存储项，后者随 @3373 保存期限（所支撑决策的存续期 + 登记保留期，合规出处覆盖登记值）单调不减；界形为**不减项**，其上界由证据库存储预算参数化，出处须为现状基线测量或业务方书面目标）。就近族映射理由：本条不进入运行时请求路径（latency_budget_delta 据此省略，kind_profile_VFM optional 表 @d:registry/profiles.yaml#key-profiles[12].selection_profile.variant），代价落在 CI 与存储侧 → 取 @2793 性能族的资源占用形态`
- **成本**：ops_cost＝稳态运维面**低于 VFM-004 而高于 VFM-001**：本条无运行时开销（不进入请求路径）、无测试资产管理面，但有两项 VFM-00…｜聚合语义=itemwise
- **反模式** 4 项（P0×2／P1×2）：VFM-002-AP1 叙事性结论触发或解除阻塞（以「我看过了没问题」放行，或以「我感觉有风险」…；VFM-002-AP2 T-F2 命中（验证项已绑定一致性回归检查的触发条件）而未形式化为可执行…；VFM-002-AP3 证据工件七要素不齐备即入库，或不齐备的工件被 ADR 引用；VFM-002-AP4 工件无输入指纹或无程序版本，致结论不可重放（「证据」实为线索）
- **施加约束** 5 项：方面 0←验证结论三值（pass/fail/escalate）：fail 于硬性质…；方面 7←证据工件 → ADR 引用源（T-F3）；方面 1←测试策略适配回馈（1.4 接收项的执行端）：验证成本过高的风格组合 → …；方面 9←失真信号、幻觉套件清单、长期失败用例 → 腐化监测输入…
- **formal_anchor**：T1(implements)、T2(implements)、T3(implements)、T9(implements)
- **参考文献**：bib 61 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：本条是 @3329 六类的**第二项**，其括注「白板谓词上的机器判定」界定了它的独占作用面——**命题的实参是 0.7 的机器层谓词，其真值可由程序求值**
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### VFM-003｜模型检查

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：8.2.1-T-03
- **envelope** 可用性可靠性：SLO、错误预算〔1 − SLO〕、MTTR、RPO/RTO：`RPO/RTO 的可达性判定完备度 ↑ 于本条，MTTR ↓ 于本条（**主收益面**：Z8 @2604-2605 逐字「∀ orchestrated flow: orchestrator_state durable ∧ recoverable // 协调者可恢复（流程状态是 Y 域数据）—— 硬」——recoverable 的成立决定 RTO 有无有限上界；Z3 @2591-2594 的补偿路径完备（compensable → ∃ compensation ∧ idempotent）决定回退是否可在有限步内完成 → MTTR 的下界由「最短补偿路径长度」参数化。界形为**下界收敛项**，其阈值为参数化项而非定值，出处须为合同 SLA 或现状基线测量（@2801 四者之一）。就近族映射理由：本条守护的是状态机的可恢复性与补偿完备性，其失守的后果直接落在恢复时长与恢复点 → 取 @2794 可用性/可靠性族的 RPO/RTO 与 MTTR 形态；6.2.1 无「检出能力/覆盖/误报率」的在册形态（kind_profile_VFM note 的期望面差异登 G-VFM-1）`
- **envelope** 可用性目标（SLO）：`SLO 的成立由抽样证据升为穷举证据于本条（Z4 @2595-2597 逐字「Σ timeout_budget(path) ≤ sla_bound(path) ∧ ∀ 相邻级: t_downstream < t_upstream − propagation // 超时预算闭合 —— 条件硬」，其括注 @2597「SLA 上界与传播开销估计过 0.4 证据门槛时为硬；否则降软 + 保守界：超时取注册表保守默认，可推翻指标 = 实测传播延迟」——本条是「过门槛」这一前提的验证手段之一；界形为 **∀ path 的全称闭合项**，其上界 sla_bound(path) 由合同 SLA 或业务方书面目标给定，不得本地设定）。就近族映射理由：@3390 逐字「SLA 合同条款 → 端到端层判据的强制集」与 @2794 的 SLO 形态同源；本条的收益不是提高 SLO 数值而是提高其**判定完备度**（穷举 vs 抽样），故取 SLO 单指标形态而非整族形态（与上一项分工：上一项承载恢复面，本项承载预算闭合面）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（**代价面，且为六类中最陡**：状态空间穷举的计算与内存项随状态变量数组合爆炸，量级非单调线性；界形为**不减项**，其上界由交付空间的算力与时长预算参数化——@3483 逐字「执行成本超出交付空间预算（**CI 时长上限有出处：发布节奏要求**）」即该预算的出处形态，出处为业务方书面目标；超限时按 @3483 折衷并把降密度显式登记「**降密度显式登记，不做静默缺口**」）。就近族映射理由：本条不进入运行时请求路径（latency_budget_delta 据此省略，@d:registry/profiles.yaml#key-profiles[12].selection_profile.variant），其代价全部落在离线穷举侧 → 取 @2793 性能族的资源占用形态而非延迟形态`
- **成本**：ops_cost＝稳态运维面**六类中最低而单次执行成本最高**：本条无运行时开销（不进入请求路径）、无证据库的长期存储累积（穷举结论的工件量远小于 VFM-…｜聚合语义=itemwise
- **反模式** 4 项（P1×2／P2×2）：VFM-003-AP1 状态机类硬性质以测试抽样替代模型检查，且未登记手段缺口（计划矩阵显示已覆…；VFM-003-AP2 模型检查结论无可重放工件（缺被检模型版本、状态空间界定或搜索策略三者之一…；VFM-003-AP3 被检模型与实现漂移（模型据旧设计构造，实现已变更而模型未重建，结论以 p…；VFM-003-AP4 覆盖性质集与已登记 Z 系列不对账（只覆盖部分而计划矩阵不声明其界，覆盖…
- **施加约束** 5 项：方面 0←验证结论三值（pass/fail/escalate）：fail 于硬性质…；方面 7←证据工件 → ADR 引用源（T-F3）；方面 1←测试策略适配回馈（1.4 接收项的执行端）：验证成本过高的风格组合 → …；方面 9←失真信号、幻觉套件清单、长期失败用例 → 腐化监测输入…
- **formal_anchor**：T1(implements)
- **叙事（收益-成本）**：收益：本条是 @3329 六类的**第三项**，其括注「状态机性质 Z3/Z8 类」界定了它的独占作用面——**真值取决于状态转移序列的性质族**
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### VFM-004｜测试

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：8.2.1-T-04
- **envelope** 性能：延迟分位数（P50/P99，P99 = 延迟分布第 99 百分位数）：`P99 的达标判定由叙事性升为可重放工件于本条（**主收益面**：@3326「响应度量 → 测试判据」＋@3340 端到端层「六要素场景的响应度量、SLA 判据」＋@3390「SLA 合同条款 → 端到端层判据的强制集」；界形为**上界收敛项**，其上界 sla_bound 由合同 SLA 或业务方书面目标给定（@2801 四者之一），本条不设定数值只产出实测工件——8.6 示例一 @3467 的『实测 P99 = 具体毫秒数』（母本原文为裸数值，界形内不复述数字以免触 M3 的 0.17.7 门槛 2 假精确判据；逐字原文见 @3467 与本条 benefit_cost_analysis）因无工件（七要素缺五）被否定引用资格，(a) 分支「负载测试执行 + 七要素工件入库 → ADR 重新提交，引用合法」即本项的合法形态）。就近族映射理由：@2793 性能族的度量方式列逐字「负载测试、生产观测」，前者即本条、后者归 VFM-006 → 本条只承载负载测试侧的判定，生产观测侧不双计`
- **envelope** 可用性可靠性：SLO、错误预算〔1 − SLO〕、MTTR、RPO/RTO：`MTTR 与 RPO/RTO 的达标性由演练证据支撑于本条，错误预算的燃尽判据以注入结果为输入（@2794 度量方式列逐字「生产观测、故障演练、注入测试」——后两者即本条；@3348 补偿路径测试「每个 Saga 的每个 compensable 步骤的补偿操作 + pivot 步骤前后分类正确性（Z3 的动态面）」直接决定回退可否在有限步内完成 → MTTR 下界由最短补偿路径长度参数化；@3347 乱序/重复/丢失注入「按其语义注入对应故障（at-least-once → 重复注入验证幂等；乱序注入验证因果假设）」决定错误预算的失败额度是否被低估。界形为**下界收敛项**，其阈值为参数化项而非定值，出处须为合同 SLA 或现状基线测量）。就近族映射理由：本条与 VFM-003 共用该形态但分工不同——VFM-003 承载 RPO/RTO 可达性的**穷举判定**（envelope 第一项），本条承载**演练侧的实测证据**（@2794 度量方式列把「故障演练、注入测试」与「生产观测」并列，前两者非穷举）→ 不构成双计（同一 metric 的不同 bound_expr 轴）`
- **envelope** 可修改性：典型变更的实现成本（触达单元数、跨边界契约变更数）：`两项分量的**可测性**由本条提供（@3337 单元层「单元内职责、seam 可用性（W1/W2 的执行面）」——seam 可用即单元可独立验证，变更的触达面才可被局部测试隔离；@3339 契约层「事件 schema 演化、数据契约边界校验」——跨边界契约变更数的实测面即 schema 演化用例的通过/失败分布；界形为**度量能力项**而非数值上界：@2795 度量方式列逐字「变更案例回溯、DSM 密度（2.2.4 通道二的消费端之一）」，其中变更案例回溯的证据形态须由本条产出，否则回溯结论属叙事性（@3363 T-F1 双禁）。就近族映射理由：与 VFM-001 的同族形态分工——VFM-001 取 @2795 的单分量形态「触达单元数」（静态依赖面可求值），本条取双分量形态（跨边界契约变更数只能在运行/契约用例侧观测）`
- **envelope** 可伸缩性：单位资源增量带来的容量增量：`容量增量的实测证据由本条产出（@2796 度量方式列逐字「负载测试、伸缩演练」——两者均为本条手段：负载测试属性能/伸缩共用手段，伸缩演练属 @3350 混沌注入的同族演练面；界形为**比值项**，其分子分母均为参数化量，出处须为现状基线测量或业务方书面目标，本条不设定比值只产出实测点）。就近族映射理由：@2796 可伸缩性族的两形态中「伸缩操作时长」偏运维操作面（归方面 9／VFM-006 的观测侧），「单位资源增量带来的容量增量」偏验证产出面 → 本条取后者；6.2.1 无「检出能力/覆盖/误报率」的在册形态（kind_profile_VFM note 的期望面差异登 G-VFM-1）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（**代价面，且为六类中最高**：四层套件的 CI 执行项 + 测试资产的存储与维护项 + 注入/演练环境的搭建项，三者随单元数与卡片 failure_modes 数增长；界形为**不减项**，其上界由交付空间的 CI 时长与算力预算参数化——@3483 逐字「执行成本超出交付空间预算（**CI 时长上限有出处：发布节奏要求**）」即出处形态，超限时按 @3483 折衷：「合规项 + 不可逆故障模式项全自动全覆盖；可逆故障模式项按注册抽样率执行（抽样率是计划矩阵参数，变更走 ADR）」并「**降密度显式登记，不做静默缺口**」）。就近族映射理由：本条不进入运行时请求路径（latency_budget_delta 据此省略，@2508 的 Σ 消费路径只对行为模式的卡片求和；@d:registry/profiles.yaml#key-profiles[12].selection_profile.variant kind_profile_VFM 的 optional 表同旨），代价全部落在 CI 与资产侧 → 取 @2793 性能族的资源占用形态`
- **成本**：ops_cost＝稳态运维面**六类中最高，且形态为『高频高额』**（与 VFM-003 的「低频高额」、VFM-001/VFM-002 的「高频低额」均不同…｜聚合语义=itemwise
- **反模式** 4 项（P1×2／P2×2）：VFM-004-AP1 金字塔失真：端到端层用例占比越过登记上限，或单元层覆盖率与端到端通过率长…；VFM-004-AP2 集成层用例以测试替身替换真实依赖而未登记替身使用；VFM-004-AP3 已发布契约的契约测试套件缺项，或套件存在而未入 CI；VFM-004-AP4 注入用例集不覆盖卡片 failure_modes，且未按注册抽样率标注『…
- **兼容性**：CTR-009(requires)、CTR-010(requires)
- **施加约束** 5 项：方面 0←验证结论三值（pass/fail/escalate）：fail 于硬性质…；方面 7←证据工件 → ADR 引用源（T-F3）；方面 1←测试策略适配回馈（1.4 接收项的执行端）：验证成本过高的风格组合 → …；方面 9←失真信号、幻觉套件清单、长期失败用例 → 腐化监测输入…
- **formal_anchor**：T1(implements)、T4(implements)、T5(implements)、T6(implements)、T7(implements)
- **参考文献**：bib 60 [已核验]·metadata_extraction、bib 62 [已核验]·metadata_extraction、bib 63 [已核验（2026-09-15 以本地实书版权页为准更正副题；原著录 "System Resiliency in Complexity" 系笔误，见附录一第 15 行）]·metadata_extraction、bib 65 [已核验]·case_study
- **叙事（收益-成本）**：收益：本条是 @3329 六类的**第四项**，其括注「单元/集成/契约/行为注入/端到端」界定了它的独占作用面——轴向分界在**证据形态**：VFM-001 求值于代码/模型的**结构**（静态、无…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### VFM-005｜人工评审

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** costly｜**origin** hybrid
- **源行**：8.2.1-T-05
- **envelope** 可修改性：变更前置时间：`变更前置时间 ↑ 于本条（**代价面**：本条在发布节点与批准点引入**串行关卡**——@3383 明定验证计划评审的触发点是「发布节点」，@3380 明定设计评审在「高影响决策批准前」，两者均不可与开发并行；界形为**不减项**，其上界由发布节奏参数化，出处形态见 @3483 逐字「执行成本超出交付空间预算（**CI 时长上限有出处：发布节奏要求**）」同型，出处为业务方书面目标。裁剪是本项唯一的合法下降通道（@3386 通道保留 ≠ 通道加重），且裁剪须记 ADR）。就近族映射理由：本条的成本形态是人类工时的**串行占用**，其可观测后果落在交付节奏而非延迟或吞吐 → 取 @2795 可修改性族的「变更前置时间」形态；6.2.1 七族无「评审时长/人力工时」的在册形态（kind_profile_VFM note 的期望面差异一并登 G-VFM-1）`
- **envelope** 合规：监管条款 → 可判定谓词的映射覆盖率：`映射覆盖率 ↑ 于本条（**兜底面**：@3390 逐字「合规验证要求（监管条文 → 强制验证项与证据留存期，**外部显式指定**）」——凡监管条文无法静态映射为可判定谓词者（VFM-001 适用域之外），其判定义务不因不可自动化而豁免，由本条承载实质判断 → 界形为**补集项**＝1 − 可静态判定比例，该比例须有勘察出处（0.4 门槛，无据面登 SO-16）；@3483 逐字「合规相关验证项（出处 = 监管条文，外部显式指定）**不可裁剪**」即本项的刚性来源——本项不受 @3386 裁剪通道影响）。就近族映射理由：本条守护的是合规判定的**完备性**（无条文因不可自动化而脱漏）→ 取 @2798 合规族唯一在册形态「监管条款 → 可判定谓词的映射覆盖率」，与 VFM-001 同形态而作用面互补（VFM-001 承载可静态映射的部分，本条承载补集）`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（**代价面**：人类工时占用项。@3396 逐字「0.10 能力条款的受益域：**全量性质覆盖检查对人类成本过高而常缺省，对 Agent 趋零** → Agent 运行时 T1（每硬性质至少一手段）从『应然』变为『实然』」即该占用在双使用者下的**不对称形态**——同一评审点对人类是稀缺资源、对 Agent 只是材料备置成本；界形为**不减项**，其上界由团队规模与裁剪后的评审点集合参数化（@2801 四合法来源中取「现状基线测量」）。**本项与 VFM-003 envelope 第三项的分工**：彼为离线算力峰值（低频高额），此为人工时串行占用（随发布频次线性累积））。就近族映射理由：6.2.1 七族无「人力工时」在册形态，@2793 性能族「资源占用」为最近族（差异登 G-VFM-1）；本条不进入运行时请求路径 → cost_profile.latency_budget_delta 省略（@d:registry/profiles.yaml#key-profiles[12].selection_profile.variant）`
- **成本**：ops_cost＝稳态运维面**六类中最依赖组织事实而非技术设施**：无运行时开销（不进入请求路径）、无规则集维护面（对照 VFM-001）、无模型重建面（对…｜聚合语义=itemwise
- **反模式** 4 项（P0×1／P1×1／P2×2）：VFM-005-AP1 五评审点之一被静默删减（未排期、未举行或改为 Agent 自批），而计划…；VFM-005-AP2 人类评审记录未按证据工件保全（七要素缺项，或已保全但不可重放），而该记录…；VFM-005-AP3 评审点集合按部署规模裁剪而未记 ADR（缩减不可追溯，与静默删减在台账上…；VFM-005-AP4 材料性判定由 Agent 机械适用 materiality 谓词而无人工…
- **施加约束** 5 项：方面 0←验证结论三值（pass/fail/escalate）：fail 于硬性质…；方面 7←证据工件 → ADR 引用源（T-F3）；方面 1←测试策略适配回馈（1.4 接收项的执行端）：验证成本过高的风格组合 → …；方面 9←失真信号、幻觉套件清单、长期失败用例 → 腐化监测输入…
- **formal_anchor**：T1(implements)、T3(implements)、T8(implements)
- **叙事（收益-成本）**：收益：本条是 @3329 六类的**第五项**，其括注「（8.2.7，人类通道）」界定了它的独占作用面——**须人类作实质判断与须批准的性质族**
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### VFM-006｜生产监测

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：8.2.1-T-06
- **envelope** 性能：延迟分位数（P50/P99，P99 = 延迟分布第 99 百分位数）：`P99 ↑ 于本条的埋点开销项，同时本条是 P99 的**唯一生产侧度量端**（双面项）。代价面：埋点与采集位于请求路径 → 附加延迟项由 cost_profile.latency_budget_delta 参数化（本条为六类中唯一填实该槽者），界形为**附加项**，其上界出处须为合同 SLA 或现状基线测量（@2801 四合法来源之二）。收益面：@2793 度量方式列逐字「负载测试、**生产观测**」——无本条则该指标只有负载测试侧的估计值而无生产真值，@3392「**现状基线是验证判据的锚**（6.3 同源纪律：基线来自观测非文档）」即此意。就近族映射理由：取 @2793 性能族的延迟分位数形态（含母本括注全文，与 VFM-004 envelope 第三项同形态而作用面互补——彼为负载测试侧的判据，此为生产侧的真值）`
- **envelope** 可用性目标（SLO）：`SLO 的**可判定性** ↑ 于本条（界形为**判定端项**而非数值项：本条不改变 SLO 数值——数值出处按 @2801 须为合同 SLA、监管条文、业务方书面目标或现状基线测量四者之一——只使其达成与否可被判定）。@3634 逐字「错误预算燃尽率、基线漂移 | 6.4 施加项（Q7） | **预算耗尽 → P1；燃尽率异常 → P2 趋势监测**」即本条对该指标的判定形态；@2794 度量方式列含「生产观测」。**与 VFM-003 envelope 第二项的分工**：彼承载 SLO 的**穷举判定完备度**（sla_bound 的全称闭合，离线侧），此项承载 SLO 的**生产达成度**（燃尽率，运行时侧）——同一指标形态、两个不相交的作用面，故不重复（0.9 唯一真相）。就近族映射理由：取 @2794 可用性/可靠性族的 SLO 单指标形态（整族形态含 MTTR/RPO/RTO，其判定完备度已由 VFM-003 承载）`
- **envelope** 可观测性：追踪覆盖率：`追踪覆盖率对本条既是**前提项**也是**收益项**（双向）。前提面：@2799 可观测性族逐字「卡片 `observability_requires`（5.2.5）满足率、追踪覆盖率 | 基础设施勘察」＋@2508「observability_requires 未满足而模式已选用 = 『选了但养不起』…降软或阻塞」→ 覆盖率低于登记下界时本条的结论不成立（AP1），界形为**下界项**，其下界出处须为卡片登记的 observability_requires 集合（@2498-2505 槽四）。收益面：本条的部署本身提升该指标（埋点即覆盖）。就近族映射理由：取 @2799 可观测性族的追踪覆盖率形态（与 VFM-002 envelope 第三项同形态而作用面不同——彼为检查程序执行记录的可观测面，此为生产流量的追踪面）；整族形态「卡片 observability_requires（5.2.5）满足率、追踪覆盖率」已由 QAT/CRD 批在用，本条取单指标形态以免同族重复计息`
- **envelope** 性能：资源占用：`资源占用 ↑ 于本条（**代价面**：三项累积——采集侧（埋点与代理的 CPU/内存）、传输与存储侧（指标、日志、追踪数据的写入与索引）、留存侧（@3373 逐字「所支撑决策的存续期 + 注册表登记的保留期；**合规出处（监管留存要求）覆盖登记值**（外部显式指定权威最高）」→ 留存期可由外部拉长而不可本地缩短）。界形为**不减项**，其上界由交付空间的资源预算参数化（@3394），出处为现状基线测量或业务方书面目标；超限时的合法处置是按 @3483 折衷并「**降密度显式登记，不做静默缺口**」（抽样率是计划矩阵参数，变更走 ADR），不得静默缩短留存期。就近族映射理由：取 @2793 性能族的资源占用形态（本条不改变被监测系统的功能资源占用，只增加观测侧占用 → 与 VFM-003 的离线算力峰值、VFM-005 的人工时占用三者互不相交）`
- **成本**：ops_cost＝稳态运维面**六类中最高且为持续型**：本条是唯一进入运行时请求路径的手段（latency_budget_delta 填实的根据），故其成本…｜聚合语义=itemwise
- **反模式** 4 项（P1×3／P2×1）：VFM-006-AP1 行为模式已选用而生产观测面未满足其卡片 observability_re…；VFM-006-AP2 单点越阈即告警而无趋势窗口判据（阈值 + 趋势窗口双判据未启用），噪声淹…；VFM-006-AP3 放量或回滚判据以人工叙事替代注册参数（『看着还行』充当放量依据，或部署策…；VFM-006-AP4 生产信号产出后未登记入汇聚信号源清单（源方面与消费方式缺项）且无整改闭环…
- **施加约束** 5 项：方面 0←验证结论三值（pass/fail/escalate）：fail 于硬性质…；方面 7←证据工件 → ADR 引用源（T-F3）；方面 1←测试策略适配回馈（1.4 接收项的执行端）：验证成本过高的风格组合 → …；方面 9←失真信号、幻觉套件清单、长期失败用例 → 腐化监测输入…
- **formal_anchor**：T1(implements)
- **参考文献**：bib 64 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：本条是 @3329 六类的**第六项**，其括注「（与方面 9 共享信号源）」界定了它的独占作用面——**只能由生产流量观测判定的性质族**，同时界定了它的归属特殊性：它是六类中唯一**跨方面共…
- **数据来源层**（yaml 行内注释）：provenance: 骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源；narrative: 骨架源/交叉表源

## kind DPS（源表 9.2.5）

（DPS-001–DPS-005，共 5 条；kind_profile_DPS status=seed；块内按 entry_id 升序）

### DPS-001｜滚动发布

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：9.2.5-滚动发布
- **envelope** 可用性目标（SLO）：`availability(共存期) ≥ [容量裕度参数]（批次替换期实例数 ↓ → 可用容量 ↓；批次大小 ↑ → 单批故障影响面 ↑ 而替换轮数 ↓）；界形为**批次边界上的下界项**，裕度值须为现状容量基线测量，非定值`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`回滚触达单元数 = 单批实例集（≥ 单实例、≤ 全部实例）；批次大小 ↑ → 回滚粒度变粗而回滚次数 ↓；界形为**批次级上界**，批次大小是参数化项`
- **envelope** 延迟分位数 P99：`P99(共存期) = max(P99_old, P99_new) + [混合态路由开销]；新旧并存期两侧分位数同时可达 → 观测端 P99 为两版本上包络，单调不减；开销值待勘察`
- **成本**：ops_cost＝随实例总数与发布频次上升：每轮发布须编排批次、核对共存期兼容、按批次切片观测；相对序**低于 DPS-002**（无双环境与双写链路）而**…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：DPS-001-AP1 共存期新旧版本协议不兼容且无契约约束；DPS-001-AP2 把批次级回滚降级为单实例回滚（回滚粒度被误读为可按实例精细控制）；DPS-001-AP3 共存期版本分布不可观测（混合态被读作单一版本）
- **兼容性**：DPS-005(requires)
- **施加约束** 7 项：方面 0←P0 阻塞响应义务；方面 1←演化观测数据 → 风格重审提议的事实源；方面 1←已注册守护规则（P0/P1）→ 风格选择必须一致；方面 2←粒度上界类守护规则 → 分解策略约束…
- **formal_anchor**：G3(implements)
- **参考文献**：bib 67 [已核验（联网核验时间 2026-09-13，第 2 版版权页与发行方页面一致）]·metadata_extraction
- **叙事（收益-成本）**：收益：滚动发布把「发布」从一次性事件拆为**可观测的批次序列**——@3655 的「逐批替换实例」使故障影响面以批次为单位被切分，容量与错误率可按批次切片观测（observability_requir…
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源/人工判断/骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；compatibility: 交叉表源；constraints_imposed: 交叉表源

### DPS-002｜蓝绿发布

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：9.2.5-蓝绿发布
- **envelope** 可用性目标（SLO）：`RTO_蓝绿 = [切换脚本执行时长] ≤ RTO_合同/监管；切换回滚时长 = [切回蓝的执行时长] ≤ 同值上界；两个量均以**出处值**为上界，非团队自定值（@3656「RTO 出处为合同/监管」）；执行时长为待勘察参数`
- **envelope** 性能：资源占用：`峰值资源占用 = 2 × 稳态占用（新旧环境同时在位）；环境数 ↑ → 占用 ↑（系数固定为两环境）；系数由 @3656「资源双倍成本可承受」逐字给定，非本地推断`
- **envelope** 可用性目标（SLO）：`availability(切换窗口) ≥ [切换原子性参数]；切换非原子 → 窗口内存在部分流量走旧、部分走新的混合态 → 可用性下界由混合态时长决定；参数待勘察`
- **成本**：ops_cost＝策略族内**最高**：资源双倍成本（@3656 逐字）＋双环境生命周期管理＋双写链路维护；相对序高于 DPS-001／DPS-003／DPS…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：DPS-002-AP1 伪蓝绿：数据面不可切回而未显式声明（把流量切换当作全量可逆）；DPS-002-AP2 RTO 无合同/监管出处而按团队自定值判定「回滚时间要求已满足」；DPS-002-AP3 双环境长期并存（旧环境不按发布窗口回收）使资源双倍成本常态化
- **兼容性**：DPS-005(requires)
- **施加约束** 7 项：方面 0←P0 阻塞响应义务；方面 1←演化观测数据 → 风格重审提议的事实源；方面 1←已注册守护规则（P0/P1）→ 风格选择必须一致；方面 2←粒度上界类守护规则 → 分解策略约束…
- **formal_anchor**：G3(implements)
- **参考文献**：bib 67 [已核验（联网核验时间 2026-09-13，第 2 版版权页与发行方页面一致）]·metadata_extraction
- **叙事（收益-成本）**：收益：蓝绿把「回滚」从逐批撤销改为**一次流量切回**——@3656 卡片要点逐字「回滚最快（切回蓝）」，回退动作的复杂度与发布规模无关，这是本策略在 RTO 苛刻场合的核心价值（applicabil…
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源/人工判断/骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源

### DPS-003｜金丝雀发布

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：9.2.5-金丝雀发布
- **envelope** 可用性目标（SLO）：`故障影响面 ≤ 已放量比例（爆炸半径上界 = 流量比例）；放量比例 ↑ → 影响面上界 ↑ 而观测置信度 ↑；比例、阈值、观测窗三者为**注册参数**（@3657 逐字），非本地填值`
- **envelope** 延迟分位数 P99：`P99(新版本) ≤ [判据阈值]（阈值须为注册参数）；判据三件套缺一 → verdict 不成立 → 不得放量（G4 @3743）；阈值与观测窗待勘察`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`回退触达单元数 = 已放量实例集（≤ 全量实例）；放量比例 ↑ → 回退触达 ↑；界形为比例上界，比例为注册参数`
- **成本**：ops_cost＝随放量轮数与观测窗长度上升：每轮须判定、留痕、决定是否继续放量；相对序**高于 DPS-001**（多出判据维护与逐轮判定），**低于 DP…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：DPS-003-AP1 人工「看着还行」作为放量依据（放量判据未注册或退化为叙事）；DPS-003-AP2 单点越阈即判达标（未覆盖观测窗，判据退化为单次采样）；DPS-003-AP3 观测噪声未降即在噪声中判定放量（判据可信度前提缺失）
- **兼容性**：DPS-005(requires)
- **施加约束** 7 项：方面 0←P0 阻塞响应义务；方面 1←演化观测数据 → 风格重审提议的事实源；方面 1←已注册守护规则（P0/P1）→ 风格选择必须一致；方面 2←粒度上界类守护规则 → 分解策略约束…
- **formal_anchor**：G3(implements)、G4(implements)
- **参考文献**：bib 67 [已核验（联网核验时间 2026-09-13，第 2 版版权页与发行方页面一致）]·metadata_extraction
- **叙事（收益-成本）**：收益：金丝雀把「发布风险」转为**可测量的比例**——@3657 卡片要点逐字「爆炸半径最小」，故障影响面以已放量比例为上界（envelope 第一项的可用性上界），从而在放量早期以最小暴露换取判据置…
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源/人工判断/骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源

### DPS-004｜功能开关驱动发布

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：9.2.5-功能开关驱动发布
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`行为回退触达单元数 = 受开关控制的单元集（≤ 全部实例）；开关扇出 ↑ → 回退触达 ↑；界形为扇出上界，扇出为参数化项`
- **envelope** 可用性目标（SLO）：`expiry 覆盖率 = 1（∀ 行为级开关: 已登记 expiry ∨ 已批准 ADR(G…)）；未覆盖 → Z6 不成立（@2600）；[到期时刻具体值待勘察]`
- **envelope** 性能：资源占用：`开关矩阵规模 = 开关数 × 组合维数；组合维数 ↑ → 判定路径分支 ↑（组合爆炸）；规模为监测参数，P2 监测项（@3658 逐字）`
- **成本**：ops_cost＝随开关数与扇出规模上升：开关注册、到期复核、组合维度治理；相对序**低于 DPS-002**（无双环境与双写），**高于 DPS-005**…｜聚合语义=itemwise
- **反模式** 3 项（P0×1／P1×1／P2×1）：DPS-004-AP1 行为级开关无 expiry 登记（僵尸开关长期生效）；DPS-004-AP2 开关矩阵组合爆炸（组合维数增长未被监测）；DPS-004-AP3 以开关切换替代部署发布（把行为生效当作环境变更完成）
- **兼容性**：CFG-003(requires)、DPS-005(requires)
- **施加约束** 7 项：方面 0←P0 阻塞响应义务；方面 1←演化观测数据 → 风格重审提议的事实源；方面 1←已注册守护规则（P0/P1）→ 风格选择必须一致；方面 2←粒度上界类守护规则 → 分解策略约束…
- **formal_anchor**：G3(implements)、Z6(implements)
- **参考文献**：bib 67 [已核验（联网核验时间 2026-09-13，第 2 版版权页与发行方页面一致）]·metadata_extraction
- **叙事（收益-成本）**：收益：功能开关驱动发布把「部署」与「发布」拆为两个独立时刻——@3658 定义逐字「部署与发布解耦：代码先行部署，行为由开关控制」，由此获得三项能力：其一是**行为回退的即时性**（typical_r…
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源/人工判断/骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源

### DPS-005｜回滚规程

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：9.2.5-回滚规程
- **envelope** 可用性目标（SLO）：`规程完备度 = 判据 ∧ 操作序列 ∧ (数据方案 ∨ 显式「数据不可回滚」声明)；任一缺失 → G3 不成立 → 不予注册（@3659 逐字「无回滚规程的部署策略不予注册」）；判据阈值待勘察`
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`回滚触达单元数 = 受该规程约束的策略实例集（DPS-001 为单批、DPS-002 为全量切换、DPS-003 为已放量比例、DPS-004 为开关扇出）；触达上界随策略形态变化 → 规程须按策略逐条登记，不得一份通用`
- **envelope** 可用性目标（SLO）：`恢复时长 = 判据触发时延 + 操作序列执行时延；数据不可回滚时改为前滚修复时长（≥ 回滚时长，因前滚须重新验证）；两项时延均为待勘察参数，不以团队自定值为准（0.4）`
- **成本**：ops_cost＝每条策略一份规程：判据维护＋序列演练＋数据方案复核；相对序为策略族的**基线成本**（DPS-001…DPS-004 均在它之上叠加自身运维…｜聚合语义=itemwise
- **反模式** 3 项（P0×2／P1×1）：DPS-005-AP1 策略缺回滚规程（判据/序列/数据方案任一缺失）；DPS-005-AP2 数据不可回滚而未显式声明（回滚语义未改为前滚修复）；DPS-005-AP3 以「回滚脚本存在」代替「数据可回滚判定」
- **兼容性**：DPS-001(composable)、DPS-002(composable)、DPS-003(composable)、DPS-004(composable)
- **施加约束** 7 项：方面 0←P0 阻塞响应义务；方面 1←演化观测数据 → 风格重审提议的事实源；方面 1←已注册守护规则（P0/P1）→ 风格选择必须一致；方面 2←粒度上界类守护规则 → 分解策略约束…
- **formal_anchor**：G3(implements)
- **参考文献**：bib 46 [已核验（联网核验时间 2026-10-04，ISBN 与版次著录一致）]·metadata_extraction、bib 67 [已核验（联网核验时间 2026-09-13，第 2 版版权页与发行方页面一致）]·metadata_extraction
- **叙事（收益-成本）**：收益：回滚规程把「出事后怎么办」从**临场处置**转为**可注册、可演练、可判定**的规程——@3659 定义逐字「每策略必附：回滚判据（自动触发指标）、回滚操作序列、数据回滚方案或『数据不可回滚』显…
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源/人工判断/骨架源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；narrative: 骨架源

## kind GRD（源表 9.2.1）

（GRD-001–GRD-003，共 3 条；kind_profile_GRD status=seed；块内按 entry_id 升序）

### GRD-001｜P0（阻塞级）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.1-P0（阻塞级）
- **反模式** 3 项（P0×3）：GRD-001-AP1 运行时把 P0 级信号改判为 P1／P2（即兴改级）；GRD-001-AP2 P0 违例未消除即继续发布或放量（带病发布）；GRD-001-AP3 内部原因的 P0 违例走 Waiver 豁免
- **施加约束** 4 项：方面 0←P0 阻塞响应义务；方面 1←已注册守护规则（P0/P1）→ 风格选择必须一致；方面 8←整改项 → 回归验证需求；方面 10←机器层：G 谓词集 + 演化路线图
- **formal_anchor**：G1(implements)
- **叙事（收益-成本）**：收益：P0 模板把「已发生的硬性质违例」与「流程是否继续」直接绑定——@3600 响应义务逐字「即时阻塞：相关变更冻结、升级裁决启动（CH-C(2)）
- **数据来源层**（yaml 行内注释）：provenance: 人工判断/骨架源/交叉表源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### GRD-002｜P1（限期级）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.1-P1（限期级）
- **反模式** 3 项（P0×2／P1×1）：GRD-002-AP1 P1 逾期未升 P0，或以「延续」方式静默展期；GRD-002-AP2 P1 登记缺整改责任人或期限（限期整改降为无期限提示）；GRD-002-AP3 P2 单点越阈即改判 P1（趋势窗口判据未成立）
- **兼容性**：GRD-001(requires)
- **施加约束** 4 项：方面 1←已注册守护规则（P0/P1）→ 风格选择必须一致；方面 2←粒度上界类守护规则（如『单服务对外接口数 ≤ 30』，P1）→ 分解策略…；方面 8←整改项 → 回归验证需求；方面 10←机器层：G 谓词集 + 演化路线图
- **formal_anchor**：G5(implements)
- **叙事（收益-成本）**：收益：P1 模板把「尚可修复的违例」转为带期限的整改义务——@3601 响应义务逐字「限期整改：登记整改责任与期限，逾期自动升 P0
- **数据来源层**（yaml 行内注释）：provenance: 人工判断/骨架源/交叉表源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

### GRD-003｜P2（监测级）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：9.2.1-P2（监测级）
- **反模式** 3 项（P0×1／P1×1／P2×1）：GRD-003-AP1 P2 单点越阈即告警（阈值+趋势窗口双判据未成立）；GRD-003-AP2 P2 信号单独出现即触发整改或阻塞（监测级被当作行动级）；GRD-003-AP3 P2 信号只记录不聚合（积累后聚合分析义务被架空）
- **兼容性**：GRD-002(requires)
- **施加约束** 3 项：方面 1←演化观测数据 → 风格重审提议的事实源；方面 7←可推翻指标命中 → 自动重审提议（过 R2 门槛）；方面 10←机器层：G 谓词集 + 演化路线图
- **formal_anchor**：G7(implements)
- **叙事（收益-成本）**：收益：P2 模板承担「早期信号不误伤、积累后可判」的职责——@3602 定义逐字「结构漂移早期信号，单独出现不行动」，响应义务为「记录 + 阈值/趋势双判据监测（2.2.4 告警治理）
- **数据来源层**（yaml 行内注释）：provenance: 人工判断/骨架源/交叉表源；typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；constraints_imposed: 交叉表源

## kind PRJ（源表 10.2.2）

（PRJ-001–PRJ-011，共 11 条；kind_profile_PRJ status=seed；块内按 entry_id 升序）

### PRJ-001｜1.4 架构评审：系统整体组织原则

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-1.4
- **反模式** 3 项（P0×2／P1×1）：PRJ-001-AP1 架构评审无覆盖 {1.5 拓扑谓词集} 的投影规则（该义务行未履行）；PRJ-001-AP2 投影规则存在但未声明受众与问题（只列谓词子集）；PRJ-001-AP3 架构视图被手工修改而未回写谓词（双重真相）
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：把「架构评审该看什么」从评审人的临场提问固化为一条可判定的义务——@3903 明确「系统整体组织原则是什么」必须由 {1.5 拓扑谓词集} 回答，且必须表达所选风格
- **数据来源层**（yaml 行内注释）：provenance: 人工判断/交叉表源；typical_reversibility: 人工判断；constraints_imposed: 交叉表源

### PRJ-002｜2.4 分解评审：单元边界与依赖

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-2.4
- **反模式** 3 项（P0×2／P1×1）：PRJ-002-AP1 分解评审无覆盖 {2.5 边界谓词集} 的投影规则；PRJ-002-AP2 以目录树/包名列表冒充边界视图（未投影 2.5 谓词）；PRJ-002-AP3 边界视图与谓词快照手工分叉
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：分解评审最容易退化为「看目录树」——@3904 把「单元边界与依赖」钉在 {2.5 边界谓词集} 上，使边界是否成立由谓词而非包名决定

### PRJ-003｜4.4 数据评审：数据所有权与流动

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-4.4
- **反模式** 3 项（P0×2／P1×1）：PRJ-003-AP1 数据评审无覆盖 {Y 谓词集、血缘} 的投影规则；PRJ-003-AP2 以表结构清单冒充数据流动/血缘视图；PRJ-003-AP3 数据视图与谓词快照手工分叉（尤其血缘边被手工合并）
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：数据评审的核心争议是「这份数据归谁、从哪来、到哪去」——@3905 把答案钉在 {Y 谓词集、血缘} 上，表结构清单再详细也不构成所有权与流动的证明

### PRJ-004｜5.4 流程评审：行为与协调的时序、事件流与流程状态

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-5.4
- **反模式** 3 项（P0×2／P1×1）：PRJ-004-AP1 流程评审无覆盖 {Z 谓词集} 的投影规则；PRJ-004-AP2 以静态时序图截图冒充流程状态/事件流视图；PRJ-004-AP3 流程视图与谓词快照手工分叉（时序被手工调整）
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：流程评审最容易被「一张时序图」带过——@3906 把时序、事件流与流程状态钉在 {Z 谓词集} 上，评审人可核对状态迁移是否闭合，而不是只看调用顺序

### PRJ-005｜8.4 验证评审入口：验证计划与证据索引

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-8.4
- **反模式** 3 项（P0×2／P1×1）：PRJ-005-AP1 验证评审入口无覆盖 {T 谓词集} 的投影规则；PRJ-005-AP2 验证计划无证据索引（只列测试活动）；PRJ-005-AP3 验证结论声称通过但证据不可重放
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：验证评审入口若只收测试报告，评审人无法判断「验证边界是否成立」——@3907 把答案钉在 {T 谓词集} 上，验证计划因此必须结构化到谓词与证据索引，而不是活动清单

### PRJ-006｜9.4 守护评审：守护台账与健康度

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-9.4
- **反模式** 3 项（P0×1／P1×2）：PRJ-006-AP1 守护评审无覆盖 {G 谓词集、演化路线图} 的投影规则；PRJ-006-AP2 以告警数量统计冒充守护健康度；PRJ-006-AP3 守护台账与 Waiver 台账分离，健康度不可交叉核对
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：守护评审若只看告警数量，会把「规则不执行、告警无人理」的守护幻觉当成安静——@3908 把「守护台账与健康度」钉在 {G 谓词集、演化路线图} 上，评审人须看规则执行面、豁免闭环与演化路线

### PRJ-007｜8.2.7 评审点一 × 0.5：高影响决策该不该批

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-8.2.7 评审点一 × 0.5 批准材料
- **反模式** 3 项（P0×2／P1×1）：PRJ-007-AP1 批准评审无覆盖候选指针/applicability 逐条/compati…；PRJ-007-AP2 批准材料只给结论，缺候选集/applicability 逐条求值记录；PRJ-007-AP3 compatibility 检验结果与注册表版本不一致
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：高影响决策的批准最怕「材料没看全就签字」——@3909 把「该不该批」的材料钉成四要素：候选集注册表指针、applicability 逐条求值记录、compatibility 检验结果、S0–S…

### PRJ-008｜8.2.7 评审点二：低影响决策是否免于留痕

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-8.2.7 评审点二
- **反模式** 3 项（P0×2／P1×1）：PRJ-008-AP1 评审点二无覆盖简记包五字段的投影规则；PRJ-008-AP2 简记条目缺五字段之一（尤其依据指针）；PRJ-008-AP3 简记包按记录合并，条目不可独立追溯
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：低影响决策免于完整 ADR，但最容易被「免于留痕」误读——@3910 把抽查判据钉在简记包上：低影响是否真低、留痕是否齐全，由包内五字段回答

### PRJ-009｜8.2.7 评审点三：材料性判定是否被机械适用

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-8.2.7 评审点三
- **反模式** 3 项（P0×1／P1×2）：PRJ-009-AP1 评审点三无覆盖重审事实集与 R2 三条件判定记录的投影规则；PRJ-009-AP2 只投影 R2 结论，不投影三条件逐条判定；PRJ-009-AP3 把「更好的方法/算法」当作三空间新事实
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：重审提议最容易被「我发现了更好的做法」推动——@3911 把抽查判据钉在重审提议的事实集与 R2 三条件判定记录上，材料性是否被机械适用可逐条复核

### PRJ-010｜8.2.7 评审点四：验证边界是否成立

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-8.2.7 评审点四
- **反模式** 3 项（P0×2／P1×1）：PRJ-010-AP1 评审点四无覆盖计划矩阵与 FVR 接线状态的投影规则；PRJ-010-AP2 验证计划矩阵缺 8.2.1 必填要素（只列测试用例）；PRJ-010-AP3 硬性质声称已验证但 FVR 未接线
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：验证边界评审最容易被覆盖率数字带过——@3912 把「边界是否成立」钉在计划矩阵（8.2.1）与 FVR 接线状态（10.2.4）上，评审人可核对每条硬性质是否既有计划又有可执行检查

### PRJ-011｜8.2.7 评审点五：Waiver 该不该给

- **状态** seed（seed 资格：成立）｜**版本** 1.1.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：10.2.2-8.2.7 评审点五
- **反模式** 3 项（P0×2／P1×1）：PRJ-011-AP1 评审点五无覆盖 Waiver 五要素与守护台账的投影规则；PRJ-011-AP2 Waiver 五要素缺项仍投影为可批；PRJ-011-AP3 守护台账与 Waiver 要素分离，无法核对闭环
- **施加约束** 5 项：方面 0←同源生成：谓词为权威，视图为投影，禁止双重维护；方面 0←FVR 全覆盖：无 FVR 条目的性质不得声称「通过」；方面 7←视图生成记录、编译产物版本 = 决策证据的组成部分；方面 8←投影可重放性纳入证据保全的可重放判据…
- **formal_anchor**：E1(implements)
- **叙事（收益-成本）**：收益：Waiver 评审最怕「理由充分就批」——@3913 把「该不该给」钉在 Waiver 五要素与守护台账上，评审人须看违例事实、范围、期限、责任与台账闭环，而不是申请书修辞

## kind GOV（源表 0.5）

（GOV-001–GOV-006，共 6 条；kind_profile_GOV status=seed；块内按 entry_id 升序）

### GOV-001｜完整 ADR

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：0.5-完整 ADR
- **反模式** 3 项（P0×2／P1×1）：GOV-001-AP1 高影响决策未走批准路径（执行者自决或 Agent 代批）；GOV-001-AP2 完整 ADR 缺被拒候选及原因（只写结论与选择）；GOV-001-AP3 评估依据无三空间出处（凭偏好或方法流行度）
- **施加约束** 4 项：方面 0←完整 ADR 六字段齐备：背景、候选集、评估依据（三空间事实引用）、选择…；方面 0←高影响决策须经人类责任方或显式裁决角色批准后方可生效；方面 0←低影响决策可执行者自决，但仍须记录（免于完整 ADR 不免于留痕）；方面 0←批准材料引用注册表条目与 S0–S6 规程日志
- **formal_anchor**：R7(implements)、R1(implements)
- **参考文献**：bib 57 [已核验]·metadata_extraction
- **叙事（收益-成本）**：收益：完整 ADR 把「为什么这么定」从口头共识固化为六字段结构——@117 逐字要求背景、候选集、评估依据（三空间事实引用）、选择、被拒候选及原因、影响范围
- **数据来源层**（yaml 行内注释）：provenance: 人工判断；typical_reversibility: 人工判断；constraints_imposed: 交叉表源

### GOV-002｜接受约束 ADR（constraint-acceptance）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：0.5-接受约束 ADR
- **反模式** 3 项（P0×2／P1×1）：GOV-002-AP1 以「外部强加」跳过内部一致性检查，或发现矛盾仍继续推进；GOV-002-AP2 无出处的「外部强加」被登记为接受约束（把传闻或偏好当制度事实）；GOV-002-AP3 接受约束 ADR 未写「为何无备选分析」
- **施加约束** 3 项：方面 0←接受约束 ADR 必含三字段：约束内容与出处、为何无备选分析、内部一致性…；方面 0←锁定项与其他决策或目标矛盾时走 CH-A 第 5 步（阻塞声明 + 人类…；方面 0←外部约束须有正式制度文件级出处
- **formal_anchor**：R7(implements)
- **叙事（收益-成本）**：收益：接受约束 ADR 让「没有备选」成为可审计的结论而不是默认借口——@118 要求写明约束内容与出处、为何无备选分析、内部一致性检查结果
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源；typical_reversibility: 人工判断

### GOV-003｜张力承认 ADR（acknowledged-tension）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：0.5-张力承认 ADR
- **反模式** 3 项（P0×2／P1×1）：GOV-003-AP1 强加决策导致目标不可达，却记张力承认以规避阻塞；GOV-003-AP2 张力承认无代价量化或监测指标；GOV-003-AP3 临时状态决策被下游作为硬约束源引用而未附张力承认
- **施加约束** 3 项：方面 0←张力承认 ADR 必含四字段：强加决策出处、张力描述、代价量化、监测指标；方面 0←目标不可达不得记张力承认，须走 CH-A 第 5 步产出不可达性证据并发…；方面 0←临时状态决策的下游只按软约束消费，消费处必附张力承认 ADR
- **formal_anchor**：R6(implements)
- **叙事（收益-成本）**：收益：张力承认 ADR 是「服从但有代价」的专用记录——@119 要求强加决策出处、张力描述、代价量化、监测指标四字段
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源；typical_reversibility: 人工判断

### GOV-004｜保守假设 ADR（conservatism-proof）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：0.5-保守假设 ADR
- **反模式** 3 项（P0×2／P1×1）：GOV-004-AP1 保守假设无可推翻指标（不可推翻的永久假设）；GOV-004-AP2 用无出处阈值伪装保守界（假精确）；GOV-004-AP3 以保守界承载不可逆或高影响决策，绕过批准路径
- **施加约束** 3 项：方面 0←保守假设 ADR 必含四字段：缺失的信息、保守假设内容、为何保守、可推翻…；方面 0←可推翻指标须为可观测的量，实际值越阈即自动触发重审提议；方面 0←缺判定程序的硬约束降为软约束并记保守假设 ADR
- **formal_anchor**：R2(triggers)
- **叙事（收益-成本）**：收益：保守假设 ADR 把 CH-B 第一种处置（保守界）变成可推翻的临时结论——@120 要求写明缺失信息、假设内容、为何保守，以及可推翻指标
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源；typical_reversibility: 人工判断

### GOV-005｜权衡承认 ADR（acknowledged-tradeoff）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：0.5-权衡承认 ADR
- **反模式** 3 项（P0×1／P1×2）：GOV-005-AP1 冲突折衷无下限合法性来源（无界牺牲）；GOV-005-AP2 优先级由执行者偏好决定，而非外部指定或业务目标推导；GOV-005-AP3 只写「已权衡」而未写牺牲了什么
- **施加约束** 3 项：方面 0←权衡承认 ADR 必含四字段：冲突双方、优先级依据及出处、牺牲了什么、牺…；方面 0←优先级须为外部显式指定或由业务目标推导（附推导过程）；方面 0←不允许无界牺牲：牺牲必须有下限合法性来源
- **formal_anchor**：R7(implements)
- **叙事（收益-成本）**：收益：权衡承认 ADR 把「牺牲了什么、为什么可以牺牲到这个程度」写清楚——@121 要求冲突双方、优先级依据及出处、牺牲内容、牺牲的下限合法性来源
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源；typical_reversibility: 人工判断

### GOV-006｜重审提议（proposed-reopen）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** free｜**origin** hybrid
- **源行**：0.5-重审提议
- **反模式** 3 项（P0×2／P1×1）：GOV-006-AP1 以「发现更好的方法／算法／模式」为由提重审（非三空间新事实）；GOV-006-AP2 新事实未过材料性判定却被受理（事实虽新但不材料）；GOV-006-AP3 重审通过后静默级联修改下游，未逐一目检血缘
- **施加约束** 3 项：方面 0←重审提议必附 ≥1 条满足 0.4 出处门槛的新事实；方面 0←R2 三条件（有事实／是新／材料性）须逐条机器可查；方面 0←重审通过后按当前分级重走流程
- **formal_anchor**：R2(implements)、R8(implements)
- **叙事（收益-成本）**：收益：重审提议把「重开决策」的触发权交给三空间而非优化冲动——@122 要求附触发重审的三空间新事实与影响范围
- **数据来源层**（yaml 行内注释）：provenance: 交叉表源；typical_reversibility: 人工判断

## kind SRC（源表 9.2.3）

（SRC-001–SRC-008，共 8 条；kind_profile_SRC status=seed；块内按 entry_id 升序）

### SRC-001｜DSM 跨边界密度/反馈环趋势

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-DSM 跨边界密度/反馈环趋势
- **施加约束** 2 项：方面 9←本信号进入守护消费面：检测结果按 9.2.1 级别触发响应义务；方面 10←机器层：signals.detection_predicate 须最终可…
- **叙事（收益-成本）**：收益：把「跨边界调用密度」与「反馈环趋势」从一句格言变成两条可结构化的信号，级别升级条件写进 severity_condition，消费方式写进 consumption，避免在交付压力下被解释成「再看…
- **数据来源层**（yaml 行内注释）：provenance: 人工判断；typical_reversibility: 人工判断

### SRC-002｜契约漂移（流量 vs 注册契约）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-契约漂移（流量 vs 注册契约）
- **施加约束** 2 项：方面 9←本信号进入守护消费面：X1 违例即触发 P0 阻塞；方面 10←机器层：契约注册面与实际流量须可对账
- **formal_anchor**：G1(triggers)
- **叙事（收益-成本）**：收益：漂移的判定不是「感觉接口变了」，而是「流量不在注册契约内且无已批准例外」，天然满足 0.4 的出处与可判定门槛
- **数据来源层**（yaml 行内注释）：provenance: 人工判断

### SRC-003｜schema 漂移/所有权违例流量

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-schema 漂移、所有权违例流量
- **施加约束** 2 项：方面 9←Y2 违例进入 P0 阻塞面；方面 4←所有权判定以 owner 关系为准：绕过所有者的直写流量即违例
- **formal_anchor**：G1(triggers)
- **叙事（收益-成本）**：收益：把两类常被混为一谈的问题拆成两个独立子信号——schema 漂移是 P1 限期整改，所有权违例是 P0 阻塞

### SRC-004｜僵尸开关（expiry 超期）/隐式时序假设再现

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-僵尸开关（expiry 超期）、隐式时序假设再现
- **施加约束** 2 项：方面 9←行为级僵尸开关（Z6 违例）升 P0；方面 5←隐式时序假设须显式登记，不得以「一直这样」充当依据
- **formal_anchor**：G1(triggers)
- **叙事（收益-成本）**：收益：僵尸开关不再一律按 P2 记录——行为级开关直接升 P0，这条升级路径由 severity_condition 结构化，机器可读

### SRC-005｜错误预算燃尽率/基线漂移

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-错误预算燃尽率、基线漂移
- **施加约束** 2 项：方面 6←错误预算耗尽升 P1；方面 9←基线漂移须与包络判定联动：基线变更即重算可达性
- **叙事（收益-成本）**：收益：燃尽率与「预算是否耗尽」分成两级同一信号的两个状态，避免把「快用完了」直接当阻塞

### SRC-006｜保守假设可推翻指标命中

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-保守假设可推翻指标命中
- **施加约束** 2 项：方面 7←指标命中即三空间新事实：重审提议须过 R2 门槛；方面 9←命中记录进入守护消费面，不得只在会议纪要里提一句
- **叙事（收益-成本）**：收益：保守假设 ADR 的可推翻指标不再「写完就忘」——命中自动进入重审提议通道，且 gate 固定为 R2，杜绝以「指标动了」为由跳过材料性判定

### SRC-007｜金字塔失真/幻觉套件/长期失败用例

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-金字塔失真、幻觉套件、长期失败用例
- **施加约束** 2 项：方面 8←T5 基级 P2；方面 9←幻觉套件清理本身是整改项，须有闭环记录
- **叙事（收益-成本）**：收益：把 8.4 的 T5 基级与条件升级原样搬进 severity／severity_condition，T5 不再是一条只存在于散文里的分级

### SRC-008｜无据决策清单（现状补录遗留）

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** costly｜**origin** hybrid
- **源行**：9.2.3-无据决策清单（现状补录遗留）
- **施加约束** 2 项：方面 7←无据决策须周期消化：补证（找到出处）或补决策（重走流程）；方面 9←长期不消化 → P2 聚合告警（9.2.3 @3637）
- **叙事（收益-成本）**：收益：棕地补录中「先记下来再说」的决策有了固定出口——要么补出处，要么重走决策流程
- **数据来源层**（yaml 行内注释）：narrative: 人工判断；statement: 骨架源/人工判断；impact: 交叉表源；note: 交叉表源；status: 人工判断；judgment: 人工判断

---
生成于 2026-11-08T11:35:55｜源哈希（sha256 前 12 位）：`method_registry.yaml`→`ec8b0d755a96`；`profiles.yaml`→`2d5851b5f262`；`predicate_vocabulary.yaml`→`1ff907e960a2`
