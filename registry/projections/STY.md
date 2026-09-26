# STY 架构风格条目（人类层投影）

> 本文件由 `scripts/project.py` 自动生成（机器层→人类层同源投影，母本 0.9／编译规范 E2），**禁止手改**；修改 registry/ 任一源后重跑 `python3 scripts/project.py --project`。

- 批次：种子批次一：STY（kind 前缀见 0.17.3 首行）＋种子批次二：OWN（kind 前缀见 0.17.3）＋种子批次三：CSL（kind 前缀见 0.17.3）＋种子批次四：CRD（kind 前缀见 0.17.3）＋种子批次五：DEC（kind 前缀见 0.17.3）
- 版本：registry_version 1.0.0
- 编号：README §4 裁决的分块序，锚定 STY-004（母本反例 18-A 既有引用一致，MJ-1）；母本零改动。
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

- **状态** seed（seed 资格：成立）｜**版本** 1.0.0｜**可逆性** bounded｜**origin** hybrid
- **源行**：1.2.1-MVC 及变体（MVP/MVVM）
- **envelope** 可修改性：典型变更的实现成本（触达单元数）：`表现层替换 → touched_units = |表现层单元|，且 touched_units(领域) = 0（表现-领域-交互三分 + 单向数据流）；领域逻辑渗入控制器/视图时该上界失效（见 STY-012-AP1）`
- **成本**：ops_cost＝无独立运维面；成本落在表现层构建与前端交付管道｜聚合语义=itemwise
- **反模式** 1 项（P1×1）：STY-012-AP1 领域逻辑渗入控制器/视图
- **施加约束** 3 项：方面 2←风格收窄分解策略可行集：表现/领域/交互为三类分解单元，领域规则不得以表…；方面 6←本条目 envelope = 质量目标可达性上界（V4 消费）；方面 10←机器层：1.5 拓扑谓词集
- **formal_anchor**：V1(implements)、V4(consumed_by)、V5(implements)
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
- **反模式** 1 项（P1×1）：STY-015-AP1 模块边界只在文档里，代码里随意穿透
- **兼容性**：STY-014(composable)、STY-023(composable)
- **施加约束** 6 项：方面 2←分解可纯逻辑边界（1.4 施→2 单体行），且内部模块边界须强制：模块为…；方面 3←进程内调用可用（1.4 施→3 单体行）；方面 4←共享数据库可用（1.4 施→4 单体行）；方面 5←进程内编排、本地事务可用（1.4 施→5 单体行）…
- **formal_anchor**：V1(implements)、V2(implements)、V4(consumed_by)、V5(implements)
- **参考文献**：bib 3 [已核验]·metadata_extraction、bib 2 [已核验]·metadata_extraction、bib 23 [已核验]·narrative_only
- **叙事（收益-成本）**：收益：以单体的性能/事务优势（网络跳数 = 0、ACID 可用）换取接近微服务的可修改性（变更触达面被模块边界收敛），并保留未来拆分选项（迁移成本上界 = 边界契约面）
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源；envelope: 骨架源；cost_profile: 骨架源/人工判断；compatibility: 骨架源；constraints_imposed: 交叉表源/骨架源/人工判断；anti_patterns: 骨架源/人工判断

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
- **施加约束** 3 项：方面 1←对 Agent 为强制步骤（纪律一，@1312）：每一个候选必须来自方法…；方面 1←匹配度排序不得替代规程其余步骤：不得增步、跳步、改序、在步骤内引入规程外…；方面 10←机器层：逐候选求值记录与得分入 selection_log / step…
- **formal_anchor**：V5(triggers)
- **叙事（收益-成本）**：收益：把风格选择变成可机器执行的匹配问题——问题特征向量 × 各风格条目的适用条件谓词 → 匹配度排序，使『候选从何而来』有唯一合法答案（注册表条目），从而封死 Agent 凭训练语料流行度自由提案的…
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；cost_profile: 人工判断

---
生成于 2026-09-26T23:08:38｜源哈希（sha256 前 12 位）：`method_registry.yaml`→`12cabd596964`；`profiles.yaml`→`0bd8e2e17384`；`predicate_vocabulary.yaml`→`a10c2164b1a5`
