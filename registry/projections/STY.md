# 方法条目卡片（人类层投影）

> 本文件由 `scripts/project.py` 自动生成（机器层→人类层同源投影，母本 0.9／编译规范 E2），**禁止手改**；修改 registry/ 任一源后重跑 `python3 scripts/project.py --project`。

- 批次：种子批次一：STY（kind 前缀见 0.17.3 首行）＋种子批次二：OWN（kind 前缀见 0.17.3）＋种子批次三：CSL（kind 前缀见 0.17.3）＋种子批次四：CRD（kind 前缀见 0.17.3）＋种子批次五：DEC（kind 前缀见 0.17.3）＋种子批次六：CTR（kind 前缀见 0.17.3）＋种子批次七：STP（kind 前缀见 0.17.3）
- 版本：registry_version 1.0.0
- 条目：合计 65 条＝STY 24 条＋OWN 4 条＋CSL 5 条＋CRD 8 条＋DEC 8 条＋CTR 12 条＋STP 4 条
- kind 覆盖：STY 全覆盖（1.2.1/1.2.2/1.2.3/1.2.4 四表全部行）＋ OWN 全覆盖（4.2.1 全部 4 行）＋ CSL 全覆盖（4.2.3 全部 5 行）＋ CRD 全覆盖（5.2.1 全部 4 行＋5.2.2 全部 4 行）＋ DEC 全覆盖（2.2.1 全部 8 行）＋ CTR 全覆盖（3.2.1 全部 6 行＋3.2.2 全部 6 行）＋ STP 全覆盖（4.2.2 全部 4 行）；其余 10 kind 待后续批次
- 文件名沿用 README §6 既定产物名 `STY.md`（该产物首块 kind 为 STY 时的历史命名）；改文件名属规范面变更，须走 ADR＋人工批准，本投影不自行改名。
- 编号：STY 块内分块序为 README §4 裁决，锚定 STY-004（母本反例 18-A 既有引用一致，MJ-1）；母本零改动。
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
- **数据来源层**（yaml 行内注释）：typical_reversibility: 人工判断；applicability: 骨架源/交叉表源；envelope: 骨架源；constraints_imposed: 交叉表源；formal_anchor: 交叉表源；narrative: 人工判断；status: 人工判断

---
生成于 2026-09-28T23:00:45｜源哈希（sha256 前 12 位）：`method_registry.yaml`→`836f6afb03bc`；`profiles.yaml`→`38f69b45e48a`；`predicate_vocabulary.yaml`→`a10c2164b1a5`
