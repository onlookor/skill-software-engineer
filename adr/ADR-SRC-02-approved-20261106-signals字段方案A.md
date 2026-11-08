# ADR 草案：方案 A —— 0.17.2 增 `signals` 字段，承载 9.2.3 逐子信号

| 项 | 值 |
|---|---|
| ADR 编号 | **ADR-SRC-02（草案）** |
| 状态 | 草案；**2026-11-06 已获人类责任方批准（0.13 高影响变更）**，按 §11 顺序执行 |
| 日期 | 2026-11-06 |
| 决策类目 | 注册表制度变更（0.17.2 条目 schema 增字段；0.17.8 M2 增量；profiles 剖面变更；8 条 SRC 发布） |
| 前置 | `ADR-SRC-01`（方案③：SRC kind 建置）；母本 0.17.3 已有 SRC 行（现行第 404 行）；9.2.3 已插登记注记（现行第 3624 行） |
| 关联 | `G-GRD-1`／`SO-17`；`R2-SRC-01`；`G-SRC-1`（本 ADR 新立）；`ADR-PRJ-2-01`（E3 豁免同型判读） |
| 影响面 | 母本 1 行；`registry/scripts/project.py`；`registry/profiles.yaml` 18 个剖面；`registry/method_registry.yaml` 8 条条目＋1 条 gap＋2 条 closure；四件投影；README／changelog |
| 批准 | 人类责任方；Agent 只执行、不自行裁定（0.10 第一条） |

> **本轮变更摘要**：A 方向＝在 `registry_entry` 块内新增 `signals` 字段。三项已定子选项：①写法 I（插 1 行，接受 6,839 处机械位移与 7 条 `needs_review`，**同批清零**）；②M4 **不扩**到 `signals`，只做非空校验、禁用方括号占位，另立 `G-SRC-1` 欠账；③剖面走 N-A（`signals` 进 `common_required`，17 个非 SRC kind 逐条 `not_applicable`，SRC 走 `required_extra` 必填）。本文件只定义变更，**不自证正确**；执行与验收见 §11。

## 1. 背景：8 条 SRC 为什么卡在发布前

### 1.1 母本事实

1. 9.2.3 表（现行第 3614–3622 行）共 **9 个数据行**：非部署 **8 行**（3614–3621）＋部署 **1 行**（3622，行内含 **3 个指标**：部署失败率／回滚率／变更前置时间）。部署三项归 `DPS`（`ADR-SRC-01` §2.6），故 SRC 立 **8 条**。
2. 8 个非部署行中，**4 行是多级别／多子信号**：SRC-003（Y2 违例 → P0；schema 漂移 → P1）、SRC-004（Z6 违例 → P0（行为级开关）；其余 P2）、SRC-005（预算耗尽 → P1；燃尽率异常 → P2 趋势）、SRC-007（T5 分级：P2，条件升 P1）。
3. 9.2.3 引导句（现行第 3610 行）订明每条须「注明源方面与**消费方式**」；消费方式不是自由描述，而是「阻塞／整改／趋势监测／重审提议／聚合告警」这类**可枚举的处置面**。
4. 9.2.1（现行第 3582–3586 行）把 P0／P1／P2 的响应义务固定为阻塞／限期整改／监测；T5 的**基级 P2＋条件升 P1**写在 8.4 可验证性质块（现行第 3338 行）与形式化行（现行第 3438–3439 行）。

### 1.2 卡点（三条，缺一不可）

1. **`anti_patterns.signal_level` 是单值枚举**（`P0|P1|P2`，0.17.2 第 363 行）。T5 的「P2 基级＋`distortion ∧ ∃ hard property 无下层覆盖` 时升 P1」无法用单值承载；SRC-003／004／005 的同行双子信号也会被压成同一值。
2. **没有字段承载「消费方式」**。若塞进 `description`／`narrative`，消费方式退化为自由文本——机器读不到，等于在注册表里再造一处**非权威真源**（0.9 SSOT 纪律的反例）。
3. **SRC-006 的重审提议须带 `gate: R2`**（9.2.3 第 3619 行逐字「须过 R2 门槛」）。`anti_patterns` 的任何字段都装不下这个门槛标记。

> 结论：在发布前停住是**正确的**。若当时强行发布，8 条 SRC 中至少 5 条会丢失级别或消费方式，且丢失方式不可机器检出。

### 1.3 候选与选择

| 候选 | 形态 | 结论 |
|---|---|---|
| **A（本 ADR）** | 0.17.2 `registry_entry` 增 `signals` 字段；逐子信号、结构化级别与消费方式 | **采用** |
| B | 复用 `anti_patterns`，一条子信号一个 anti-pattern 项 | 否决，理由见 §2 |
| 零插行 | `signals` 只写进剖面或 0.17.2 之后的行文，不进 `registry_entry` 块 | 否决，理由见 §7.3 |

## 2. 决策

### 2.1 方向 A

在 `registry_entry` 块内、`anti_patterns` 之后（现行第 364 行 `]` 之后、第 365 行 `formal_anchor` 之前）插入 **1 行** `signals` 定义。字段是**条目层**字段，不是 kind 私有扩展；`signals` 进 `profiles.yaml` 的 `common_required`，由剖面逐 kind 判定必填或 `not_applicable`。

### 2.2 子选项 1：写法 I（插 1 行）

- 插入点：`--insert-at 365`（按**原始**行号计；插在 `anti_patterns` 的 `]` 与 `formal_anchor` 之间）。
- 母本行数：**4,429 → 4,430**。
- 接受代价：**6,839 处机械位移**、**7 条 `needs_review`**（1 条区间锚＋6 条空行锚），实测见 §7。
- **硬约束**：7 条 `needs_review` 必须在**同一批落盘后清零**，不许留债。清零方式见 §7.2。

### 2.3 子选项 2：M4 不扩，但立欠账 `G-SRC-1`

- `signals.detection_predicate` 本批只做**非空校验**（S-4），**不进 M4**（M4 仍只扫 `anti_patterns[].detection_predicate` 与 `applicability` 三空间）。
- **禁用方括号占位**：这些是**待定义谓词**（词汇缺口），不是待勘察事实（事实缺口），也不是决策期参数槽。方括号会被占位普查计入槽；若带 `待勘察：` 前缀更会升为事实占位并触发 M15 勘察义务——两种都是**错分账**。详见 §8.1。
- 新增 `G-SRC-1` 登记「SRC 谓词词汇未登记」，全文见 §12。

### 2.4 子选项 3：剖面走 N-A

| 项 | 取值 |
|---|---|
| `signals` 在 `common_required` | 是（新增一组，`source` 指 0.17.2） |
| 17 个非 SRC kind | 逐条 `not_applicable`：`field: signals`＋`reason`＋`provenance: compiled`＋`source: 0.17.2` |
| SRC 剖面 | `required_extra: [signals]`；`not_applicable` 保持既有 8 项（`envelope`＋7 个 `cost_profile.*`） |
| 既有 130 条条目 | **零改动**（N-A 落在剖面，不落在条目） |

> **风险提示（如实保留）**：17 条 N-A 用的是**同一段 reason**。若审阅要求逐句反证，这 17 条会变成 17 条独立论证（每条都要证明「本 kind 的条目形态不可能承载 9.2.3 信号」），工作量按 §9 高档计。

## 3. 否决 B 的理由

B＝把每个子信号写成一条 `anti_patterns` 项，用 `signal_level` 标级别、把消费方式写进 `description`。否决理由三条：

1. **语义挪用**。`anti_patterns` 的语义是「反模式」；0.17.4 的消费者二是**守护规则播种**（方面 9 从 `anti_patterns` 派生 G 规则）。信号源是「被汇聚消费的观测面」，不是「反模式」。混用会让守护消费者读到非守护材料，且未来无法仅凭 kind 区分两类语义。
2. **单值仍装不下**。B 只能二选一：要么把「基级＋条件升级」拆成两条 anti-pattern（同一信号失去身份，`pattern_id` 变成两条，汇聚表的一行被复制成 N 条）；要么压成单值（T5 的 P1 升级分支消失）。两种都不可接受。
3. **消费方式必然退成自由文本**。`anti_patterns` 没有消费方式字段，只能写进 `description`；`gate: R2` 也只能写成句子。这正是「又造一处机器读不到的真源」，与本框架 0.9 的 SSOT 纪律正面冲突。

**与零插行的比较**：零插行虽然 0 位移、0 review，但 `signals` 会只存在于剖面与 0.17.2 之外的散文里——即**正式形状（`registry_entry` 块）与 M2 校验面两处约定不一致**。这与 `delivery_space` 的旧病同源（schema 里没有该字段、剖面上却按字段判定），故否决。

## 4. 字段定义全文

### 4.1 母本拟落盘行（单行，插入于现行第 365 行前）

```
  signals = [ { signal_id, name, detection_predicate, severity ∈ P0|P1|P2, severity_condition = { when_predicate, raise_to ∈ P0|P1|P2 } | null, consumption = [ { action ∈ block|remediate|monitor_trend|re_review|aggregate, gate ∈ {R2}（可选）, note（可选） } ] } ]  // 9.2.3 漂移／腐化信号源的逐子信号登记；kind SRC 必填，其余 kind 按剖面 not_applicable
```

> 副本实测时插入的是同字段的同义短行（`signal_id, name, detection_predicate, severity ∈ P0|P1|P2, severity_condition, consumption`）。位移计数只取决于**插入行数与插入位置**，与行内文本无关；落盘采用上式（自描述、含嵌套取值域）。

### 4.2 展开式（供实现与审阅）

```
signals = [
  { signal_id,            // 见 §4.3(1)
    name,                 // 见 §4.3(2)
    detection_predicate,  // 见 §4.3(3)
    severity ∈ P0|P1|P2,  // 基级；见 §4.3(4)
    severity_condition =
        null
      | { when_predicate,             // 升级触发谓词；非空、禁用方括号
          raise_to ∈ P0|P1|P2 },      // 必须严格高于 severity
    consumption = [                   // C3 数组：action／gate／note 三键；非空
      { action ∈ block|remediate|monitor_trend|re_review|aggregate,
        gate ∈ {R2}（仅 re_review 必填，其余禁带）,
        note（可选） }
    ]
  }
]
```

### 4.3 各键取值域与语义

| 键 | 必填 | 取值域 | 语义与约束 |
|---|---|---|---|
| `signal_id` | 是 | `{entry_id}-S{n}`，`n` 从 1 起 | 按母本 9.2.3 行内**子信号出现顺序**连续编号；同条目内唯一；**只增不改号、不复用、不重排**（0.22 编号纪律下沉到子信号层；删除留空洞） |
| `name` | 是 | 非空字符串 | **逐字取母本行内子信号名，不意译**（如「schema 漂移」「所有权违例流量」「僵尸开关（expiry 超期）」） |
| `detection_predicate` | 是 | 非空字符串 | 检测谓词表达式；**禁方括号**（§8.1）；本批不保证机器可执行——可执行性以 `G-SRC-1` 结清为准 |
| `severity` | 是 | `P0|P1|P2` | 基级；母本行明示则逐字，未给级按 §4.4 定级 |
| `severity_condition` | 是（可为 `null`） | `null` 或 `{when_predicate, raise_to}` | 恰好两键；`when_predicate` 非空且禁方括号；`raise_to` 严格高于 `severity`（序 `P2 < P1 < P0`）；`severity=P0` 时必须 `null` |
| `consumption` | 是 | 非空数组 | C3＝三键数组；每项 `action` 必填且 ∈ 五值；`gate` 仅 `re_review` 可带且值只能是 `R2`；`note` 可选 |
| `action` | 是 | `block` | 触发阻塞：硬性质联动或 P0（即时冻结／升级裁决） |
| | | `remediate` | 进入整改闭环：限期整改、清理、补证／补决策 |
| | | `monitor_trend` | 阈值＋趋势监测（不阻塞） |
| | | `re_review` | 自动重审提议；**必须带 `gate: R2`**（9.2.3 第 3619 行） |
| | | `aggregate` | 周期聚合／聚合告警（长期不消化时的汇总面） |
| `gate` | 条件必填 | `R2` | 仅 `re_review` 必填；其他 `action` 带 `gate` 即违反 S-8 |
| `note` | 否 | 字符串 | 说明；缺失或空串只记 info（S-9），不阻断 |

**为何 `severity` 与 `consumption` 正交**：9.2.1 定响应义务，9.2.3 定消费方式；两者不是一一映射。S-5／S-6 只管级别合法与升级方向，S-7／S-8 只管消费方式合法，不做「P2 必须 monitor_trend」这类交叉约束——母本没有这种对应关系，强加即本地造规范。

### 4.4 定级口径（母本未给级时的保守规则）

1. 母本明示级别 → 逐字采用。
2. 母本只给条件升级 → 基级取被升级前的级别，条件写入 `severity_condition`。
3. 母本完全未给级 → 按 9.2.1 **P2（监测级）**保守定级，并在条目 `narrative.typical_scenarios` 注明「母本未给级，按 P2 定级」。
4. 9.2.1 的「典型信号源」列举是示例性清单，与 9.2.3 的逐子信号判定冲突时，**以 9.2.3 为准**（9.2.3 是信号源的登记条款）。本批受影响处：`schema 漂移`（9.2.1 P2 示例 vs 9.2.3 → P1）、`僵尸开关`（按 9.2.3 以「行为级」为条件从 P2 升 P0，兼容 9.2.1 的一般 P2）。

### 4.5 14 个子信号与定级（发布清单）

| 条目 | 子信号 `name`（逐字） | 基级 | `severity_condition` | `consumption` |
|---|---|---|---|---|
| SRC-001 | DSM 跨边界密度 | P2 | 恶化持续（连续窗口同向漂移）→ P1 | `monitor_trend`＋`remediate` |
| SRC-001 | 反馈环趋势 | P2 | 同上 | `monitor_trend`＋`remediate` |
| SRC-002 | 契约漂移（流量 vs 注册契约） | P0 | — | `block` |
| SRC-003 | schema 漂移 | P1 | — | `remediate` |
| SRC-003 | 所有权违例流量 | P0 | — | `block` |
| SRC-004 | 僵尸开关（expiry 超期） | P2 | 行为级开关（Z6 违例）→ P0 | `block`＋`monitor_trend` |
| SRC-004 | 隐式时序假设再现 | P2 | — | `monitor_trend` |
| SRC-005 | 错误预算燃尽率 | P2 | 预算耗尽 → P1 | `monitor_trend`＋`remediate` |
| SRC-005 | 基线漂移 | P2 | — | `monitor_trend` |
| SRC-006 | 保守假设可推翻指标命中 | P2 | — | `re_review`（`gate: R2`） |
| SRC-007 | 金字塔失真 | P2 | `distortion ∧ ∃ hard property 无下层覆盖` → P1 | `monitor_trend`＋`remediate` |
| SRC-007 | 幻觉套件 | P2 | — | `remediate` |
| SRC-007 | 长期失败用例 | P2 | — | `monitor_trend` |
| SRC-008 | 无据决策清单（现状补录遗留） | P2 | — | `remediate`＋`aggregate` |

合计 **14** 个子信号（＝2＋1＋2＋2＋2＋1＋3＋1）。其中 `severity_condition` 非空 **5** 条（SRC-001 两条、SRC-004 一条、SRC-005 一条、SRC-007 一条）。

### 4.6 示例（结构与风格基准）

```yaml
    signals:
      - signal_id: SRC-005-S1
        name: "错误预算燃尽率"
        detection_predicate: "burn_rate(·) 连续窗口越阈 ∧ 趋势同向"
        severity: P2
        severity_condition:
          when_predicate: "错误预算耗尽"
          raise_to: P1
        consumption:
          - {action: monitor_trend, note: "燃尽率异常 → P2 趋势监测"}
          - {action: remediate, note: "预算耗尽升 P1 后限期整改（9.2.1）"}
      - signal_id: SRC-006-S1
        name: "保守假设可推翻指标命中"
        detection_predicate: "∃ adr: falsification_metric(adr) ∧ metric_hit(adr)"
        severity: P2
        severity_condition: null
        consumption:
          - {action: re_review, gate: R2, note: "命中即三空间新事实，重审提议须过 R2 门槛（9.2.3 第 3619 行）"}
```

## 5. M2 增量：S-1～S-9

S 系列在 `check_m2` 内执行；**无论 `status` 是否为 `draft` 都执行**（与 `check_schema` 同层，先于 M2 量词域跳过）。`ENTRY_FIELDS` 同步加入 `signals`（否则 schema 面即报「0.17.2 之外字段」）。

| 规则 | 级别 | 判据 |
|---|---|---|
| **S-1** | hard | `signals` 必须是数组；每项必须是对象；每项键集 ⊆ `{signal_id, name, detection_predicate, severity, severity_condition, consumption}` |
| **S-2** | hard | `signal_id`／`name`／`detection_predicate`／`severity`／`consumption` 五键必须出现且非空；`severity_condition` 键必须出现（值可为 `null`） |
| **S-3** | hard | `signal_id` 形态 `^<entry_id>-S[1-9][0-9]*$`；序号从 1 起**连续**、按数组顺序严格递增、同条目唯一 |
| **S-4** | hard | `name`／`detection_predicate` 去空白后非空；`detection_predicate` **不得含 `[` 或 `]`**（本批口径，防占位虚增；见 §8.1） |
| **S-5** | hard | `severity ∈ {P0, P1, P2}` |
| **S-6** | hard | `severity_condition` 为 `null`，或恰好两键 `{when_predicate, raise_to}`；`when_predicate` 非空且不含方括号；`raise_to ∈ {P0,P1,P2}` 且严格高于 `severity`；`severity=P0` 时不得为非 `null` |
| **S-7** | hard | `consumption` 为非空数组；每项键集 ⊆ `{action, gate, note}`；`action ∈ {block, remediate, monitor_trend, re_review, aggregate}` |
| **S-8** | hard | `gate` 仅允许出现于 `action=re_review`，且值必须为 `R2`；`re_review` 缺 `gate` → 失败；其他 `action` 带 `gate` → 失败 |
| **S-9** | info | `note` 缺失或为空串 → 记 info（提示，不阻断 seed 资格） |

**为何 S-9 只到 info**：`note` 是解释性补充，不是决策面；把它做成 hard 会迫使为每条信号编造说明，违反「禁默认值假充」。

**为何不做「P2 必须 monitor_trend」**：见 §4.3 末段——母本未给级别与消费方式的对应表，本地强加即造规范。

## 6. 17 个非 SRC kind 的 `signals` 判定

> 注册写法（17 条同形）：`not_applicable` 追加一项 `{field: signals, reason: "<下表统一句>", provenance: compiled, source: {source_type: clause_id, value: "0.17.2"}}`。统一句：**「本 kind 的条目是被 0.18 选型消费的设计方法／模板，不承载 9.2.3 的漂移／腐化信号源语义；`signals` 的逐子信号登记仅适用于 kind SRC（0.17.2 `signals` 条＋0.17.3 SRC 行），本 kind 按 `not_applicable` 显式登记，非省略。」**

| # | kind | 名称 | 判定 | 条目形态（为何不承载信号源） |
|---|---|---|---|---|
| 1 | STY | 架构风格 | `not_applicable` | 可选风格（骨架选择对象） |
| 2 | DEC | 分解策略 | `not_applicable` | 可选分解策略 |
| 3 | CTR | 契约形态／治理策略 | `not_applicable` | 可选契约形态 |
| 4 | OWN | 数据所有权模式 | `not_applicable` | 可选所有权模式 |
| 5 | STP | 存储拓扑 | `not_applicable` | 可选存储拓扑 |
| 6 | CSL | 一致性机制 | `not_applicable` | 可选一致性机制 |
| 7 | DFL | 数据流动机制 | `not_applicable` | 可选数据流动机制 |
| 8 | CRD | 协调风格／长流程模式 | `not_applicable` | 可选协调模式 |
| 9 | RLP | 可靠性模式 | `not_applicable` | 可选可靠性模式 |
| 10 | SCH | 调度／时间语义策略 | `not_applicable` | 可选调度策略 |
| 11 | CFG | 配置治理策略 | `not_applicable` | 可选配置治理策略（其信号在 9.2.3 由 SRC 承载） |
| 12 | QAT | 质量战术 | `not_applicable` | 可选质量战术 |
| 13 | VFM | 验证手段 | `not_applicable` | 可选验证手段 |
| 14 | GRD | 守护规则模板 | `not_applicable` | 守护规则模板；信号源是它的**输入**，不是它的字段 |
| 15 | DPS | 部署策略 | `not_applicable` | 可选部署策略（其部署三指标归 DPS 条目，而非 `signals`） |
| 16 | PRJ | 投影词汇／规则 | `not_applicable` | 投影词汇／规则 |
| 17 | GOV | 治理模板 | `not_applicable` | ADR 亚型与简记模板 |

**SRC（第 18 个 kind）**：`required_extra: [signals]`，不 N-A；8 条条目必须带 `signals` 数组。
**既有 130 条**：`common_required` 新增字段被 17 个 kind 的 N-A 完全抵消，物化后 `required` 面**不变**，故零改动。

## 7. 锚点影响（写法 I 的副本实测）

### 7.1 实测数字

副本 `/tmp/srcdraft-A2`（整工作树复制；真实仓库 0 改动），`anchor_shift.py --insert-at 365`，插入 1 行：

| 指标 | 实测值 | 说明 |
|---|---|---|
| 插入点 | 365（原始行号） | 364 `]` 后、`formal_anchor` 前 |
| 母本行数 | 4,429 → **4,430** | +1 |
| 动锚数（每锚只计一次） | **6,839** | 母本目标、legacy／prefix 两形态 |
| 其中区间锚 | **993** | 两端分别判断 |
| 端点位移总数 | **7,832** | ＝6,839＋993 |
| `needs_review` | **7** | 1 条区间内部＋6 条空行锚（明细见 §7.2） |
| 撞串补前缀 | **0** | — |
| 例外（原串不符等） | **0** | — |
| 跳过：冻结 as-of | 1,505 | 0.22 不改写 |
| 跳过：嵌入标题内的锚 | 81 | 不独立位移 |
| 跳过：代码跨度 | 183 | 字面示例豁免 |

**检测器复核（副本）**：F-2～F-8 **pass**，`prefix_unresolved=0`；F-1 为**现状度量**（**8,816** 处裸行号，fail 属既有口径，不是本批新增失败；7 条 review 清零后副本实测 **8,806**，最终仓库重跑为 8,814，差额来自本批新增记录）。

### 7.2 7 条 `needs_review` 与同批清零

| # | 位置 | 原锚 | 类型 | 清零动作（同批落盘后立即执行） |
|---|---|---|---|---|
| 1 | `registry/scripts/project.py:7` | `@322-381` | `span_inside_insert` | 改**条款锚** `@m:0.17.2`（不再随行号漂移） |
| 2 | `registry/README.md:171` | `@377-380` | `blank_landing` | 改文字引用：`profiles.yaml` 的 CFG 剖面 `optional` 段 |
| 3 | `registry/README.md:201` | `@377-380` | `blank_landing` | 同上 |
| 4 | `registry/method_registry.yaml:9369` | `@380` | `blank_landing` | 删去裸行号清单，改「`registry/README.md` 既有写法先例」 |
| 5 | `registry/method_registry.yaml:11744` | `@382` | `blank_landing` | 改文字引用：CFG 剖面 `entry_level_exemptions` |
| 6 | `registry/method_registry.yaml:12190` | `@382` | `blank_landing` | 同上 |
| 7 | `registry/method_registry.yaml:12450` | `@382` | `blank_landing` | 同上（该行已有 `@p:CFG#optional` 符号锚，保持） |

- **不许留债**：清零后必须重跑 `anchor_index.py`，`needs_review` 必须为 **0** 才可进入下一批次。
- **区间锚不等于自动扩展**：`@322-381` 指 schema 块；块内插入后若机械扩为 `@322-382`，则下次再插又要改。改条款锚是**去行号化**，不是逃避。

### 7.3 为什么否决零插行

| 维度 | 零插行（追加到第 381 行之后） | 写法 I（插 1 行在 365） |
|---|---|---|
| 位移／review | 0／0 | 6,839／7（同批清零） |
| `registry_entry` 正式形状 | **无 `signals`** | 有 |
| M2 校验面 | 有 `signals` 校验 | 有 |
| 后果 | 两处约定不一致，同 `delivery_space` 旧病 | 单一定义面 |

零插行的代价不是位移，而是**两层表达不一致**：`registry_entry` 是机器决策层的权威形状（0.17.2／编译规范 2.4 逐字采用），M2 若按剖面校验 `signals`，条目本体却声明「0.17.2 之外的字段」为非法——同一字段在形状面非法、在检查面必填。这不是可接受的折衷，是自相矛盾。

## 8. 投影、字数与占位符口径

### 8.1 占位符口径（为何本批不增加槽数）

现状（`projections/自检报告.md`）：原方括号总数 **1,483** ＝ 事实占位 **1** ＋ 未绑定槽 **1,482**。

- 本批 14 条 `detection_predicate` 与 5 条 `when_predicate` **一律不写方括号** → 方括号总数**不变**。
- **为何禁方括号**：方括号在普查里只有一个身份——「占位」。带 `待勘察：` 前缀时计为**事实占位**并产生 M15 勘察义务（把「谓词没定义」错记成「事实没勘察」）；不带前缀时计为**未绑定槽**（把词汇缺口伪装成决策期参数槽）。两者都会让 1,482 这个账**虚增**，且掩盖真实缺口。
- **正确记账**：谓词缺口记在 `G-SRC-1`（类型＝谓词词汇缺口），不占事实账、不占槽账。
- **验收判据**：本批后 `原方括号总数` 仍须为 **1,483**（事实 1＋槽 1,482），差 1 即失败。

### 8.2 投影与字数预估

| 产物 | 现状 | 本批后（预估） |
|---|---|---|
| 母本 | 4,429 行 | **4,430 行**（+1 行，约 210–260 字符） |
| `method_registry.yaml` 条目 | 130 条 | **138 条**（+8 条，约 420–560 行／12,000–18,000 字符） |
| `method_registry.yaml` gap | 22 条 | **23 条**（+1 条，约 8 行） |
| `profiles.yaml` | 17＋1 剖面 | `common_required` +1 组（约 7 行）；17 条 N-A（约 85 行）；SRC +1 行 → 约 **95–110 行** |
| `scripts/project.py` | — | +45–70 行（常量＋S-1～S-9＋调用） |
| `projections/自检报告.md` | 350 行 | 约 **365–380 行** |
| `projections/索引.md` | 306 行 | 约 **315–330 行** |
| `projections/勘察义务清单.md` | 133 行 | **133 行**（无新事实占位） |
| `projections/STY.md` | 1,946 行 | **1,946 行**（STY-only 投影，不含 SRC） |
| README／changelog | — | +60–90 行 |

> 投影行数以执行后 `--project` 实测为准；上表只作工作量与审阅范围预估。

## 9. 工作量两档

| 档 | 范围 | 估算 | 触发条件 |
|---|---|---|---|
| **低档（推荐）** | 本 ADR §11 全部步骤：母本 1 行、位移＋7 review、S-1～S-9、18 剖面、8 条 SRC、1 gap、2 closure、投影、文档 | **600–800 行 diff**（约 1.5–2.5 人日） | 17 条 N-A 按统一 reason 通过审阅 |
| **高档** | 低档＋17 条 N-A 逐句反证（17 条独立论证）＋谓词逐条登记进 `predicate_vocabulary.yaml`（R2）＋M4 扩到 `signals` 并重跑 | **800–1,050 行 diff**（约 3–5 人日） | 审阅要求逐条论证，或要求在发布前关闭 `G-SRC-1` |

## 10. 不可逆点与回退

| 点 | 事件 | 不可逆性 | 回退 |
|---|---|---|---|
| **P1** | 母本插入 1 行＋6,839 锚位移 | 中：机械可逆，但必须**整批**回退 | 未提交：`git -C /home/wgz/projects/skills/software-engineering restore -- 软件工程元框架成文法.md registry/README.md registry/method_registry.yaml registry/scripts/project.py`；已提交：`git -C /home/wgz/projects/skills/software-engineering revert <sha>`（不 rewrite history） |
| **P2** | SRC-001…SRC-008 编号发布 | **高**：0.22 编号永不复用、不重排 | 发布后**不能收回**；只能 `status: retired` 并留空洞，引用须迁移 |
| **P3** | M2 S-1～S-9 上线 | 低：代码可回退 | revert 该 commit 即可；条目数据不受影响 |
| **P4** | 17 条 N-A 与 SRC `required_extra` | 低：剖面数据可回退 | revert 剖面 commit；条目数据不受影响 |
| **P5** | `G-SRC-1` 登记 | 低：`status: open → closed` 可改 | 不删除；关闭须写 `closure` 块 |
| **P6** | 四件投影重生成 | 低：生成物，可重算 | `python3 registry/scripts/project.py --project` |

**最小可逆集**（本 ADR 落盘后、执行前）：ADR 文件本身＋副本实测；母本、`project.py`、`profiles.yaml`、`method_registry.yaml`、投影均 0 改动。

## 11. 批准后执行顺序

> 用户已于 2026-11-06 批准本 ADR；以下为执行清单。每阶段完成后单独 commit（只 commit 不 push）。

| # | 阶段 | 动作 | 通过判据 |
|---|---|---|---|
| 0 | ADR | 落盘本文件并 commit | 仅 1 个文件 |
| 1 | 母本＋位移 | 插 1 行（365）；跑 `anchor_shift.py`；清 7 条 review | 母本 4,430；`needs_review=0`；F-2～F-8 pass；`prefix_unresolved=0` |
| 2 | M2 | `ENTRY_FIELDS` 加 `signals`；实现 S-1～S-9；跑 `--check` | 既有 130 条 M2 全过（无 signals 不触发 S 规则）；无硬失败新增 |
| 3 | 剖面 | `common_required` 加 `signals`；17 N-A；SRC `required_extra: [signals]`；更新 SRC 豁免 scope | `C-KP` 18 个剖面全过；物化 required 面与现状一致（既有条目零改动） |
| 4 | 8 条 SRC | 写 SRC-001…008（14 子信号）；`meta.entry_count: 138`；`batch`／`kind_coverage` 追加；`status_transitions` 加 ST-SRC-01 | `--check`：entries=138；M2／M3／M4／M6／M9／C-ENV／C-ST 全过；占位符仍 1,483 |
| 5 | 台账 | 新增 `G-SRC-1`；`G-GRD-1`／`SO-17` 写 closure（statement／impact／route 逐字保留） | gap 计数 22→23；closure 五要素齐备 |
| 6 | 投影＋文档 | 同一次 `--project`；README 新增批次节；changelog 按批次追加 | 四件投影重生成；README／changelog 只追加不改写 |
| 7 | 终验 | 前后对比表（entries、kind 计数、自检、指针、占位、F-1～F-8、prefix、review、母本行数、numstat） | 全部指标符合 §11 判据 |

**提交批次**：①ADR；②母本＋M2；③剖面；④8 条 SRC；⑤台账；⑥投影；⑦文档。每批报哈希、文件范围、`git status`、与 `origin/main` 的领先数。

## 12. 欠账 gap：`G-SRC-1`

```yaml
  - gap_id: G-SRC-1
    type: 谓词词汇缺口（signals.detection_predicate 的谓词未登记）
    statement: "0.17.2 新增 signals 后，8 条 SRC 的 detection_predicate 需要可执行谓词；母本 9.2.3 只给自然语言信号描述（如「僵尸开关（expiry 超期）」「错误预算燃尽率」「金字塔失真」），未给谓词名。registry/predicate_vocabulary.yaml 实测未登记本批所需谓词——已知至少 expiry（VG-05）、pyramid_distortion／distortion（VG-07）、burn_rate（VG-06 Q7 面）四名在册面缺失，另有本批新引用的 unregistered_interaction／metric_hit 等尚无登记出处。本批不本地造词、不以调用式伪装已登记。"
    impact: "本批 M4 不扫 signals（只做 S-4 非空校验），故 signals.detection_predicate 是**未机器封闭的文本**，不得被读作「可执行谓词」。为防错分账，本批 detection_predicate／when_predicate 一律**禁方括号**：带 `待勘察：` 会误生成 M15 勘察义务，不带会虚增槽数；故占位符口径维持 1,483（事实 1＋槽 1,482）。不影响 M2 必填与 seed 资格（S-1～S-9 全过）。"
    affected: "SRC-001…SRC-008 的 signals[].detection_predicate 与 signals[].severity_condition.when_predicate；predicate_vocabulary.yaml；M4 检查面（现不覆盖 signals）"
    route: "逐条把谓词登记进 predicate_vocabulary.yaml（走 R2 提议；该文件为非权威投影，权威在母本 x.5／0.17.8／0.18.6 等）→ 登记完成后另开 ADR，把 M4 扩到 signals[].detection_predicate 并重跑 M4。登记前保持 open；不得以调用式（如 expiry(flag)）冒充已登记谓词，也不得以方括号占位替代登记。"
    status: open
```

## 13. 风险与未决（如实登记）

1. **17 条 uniform reason 的审阅风险**：见 §2.4。若被要求逐句反证，按 §9 高档计；本 ADR 不预付该工作量。
2. **`severity` 与 `consumption` 无交叉校验**：这是有意的（母本无对应表）；若审阅要求「P2 只能 monitor_trend」，须先以 R2 补母本对应关系，不能在本批加本地规则。
3. **9.2.1 示例与 9.2.3 逐子判定的两处张力**：`schema 漂移`（P2 示例 vs P1 判定）、`僵尸开关`（一般 P2 vs 行为级 P0）。本 ADR 按 §4.4 采用 9.2.3，并在条目 narrative 注明；若审阅要求以 9.2.1 为准，须改 §4.5 定级表并重跑 S-6。
4. **SRC 的 `applicability` 三空间为空列表**：SRC 不参与 0.18 选型（`ADR-SRC-01` §2.7），三空间谓词不构成选择面；为空是「不适用」而非「未勘察」（不触发 M15）。若审阅要求逐年给出适用条件，须先解决 M4 词汇封闭（同 `G-SRC-1` 同源）。
5. **`G-SRC-1` 未关闭前，`signals` 的可执行性不可宣称**：任何投影或 README 不得写「SRC 检测谓词已可执行」。
   〔**2026-11-08 状态（追加，不改写上文）**：`G-SRC-1` 已由 `ADR-SRC-P0-06` 闭合——M4 已覆盖 `signals[].detection_predicate` 与 `severity_condition.when_predicate`，S-11 已转 hard 并覆盖两字段；本项约束的适用期随之结束，「signals 判据可执行」自该日起可以据实宣称，但仅限「词汇封闭＋含已登记调用」这层含义，不含「整串可解析／元数匹配」（见 `ADR-SRC-P0-06` §9 残余）。〕

## 14. 参考

- [ADR-SRC-01-draft-20261105-9.2.3九信号源方案③.md](file:///home/wgz/projects/skills/software-engineering/adr/ADR-SRC-01-draft-20261105-9.2.3九信号源方案③.md)
- [母本 0.17.2／0.17.3／9.2.1／9.2.3](file:///home/wgz/projects/skills/software-engineering/软件工程元框架成文法.md)
- [profiles.yaml](file:///home/wgz/projects/skills/software-engineering/registry/profiles.yaml)
- [method_registry.yaml](file:///home/wgz/projects/skills/software-engineering/registry/method_registry.yaml)
- [project.py](file:///home/wgz/projects/skills/software-engineering/registry/scripts/project.py)
- [predicate_vocabulary.yaml](file:///home/wgz/projects/skills/software-engineering/registry/predicate_vocabulary.yaml)
- [锚点与引用规范.md](file:///home/wgz/projects/skills/software-engineering/锚点与引用规范.md)
- 副本实测：`/tmp/srcdraft-A2`、`/tmp/A2-out.json`、`/tmp/A2-review.csv`
