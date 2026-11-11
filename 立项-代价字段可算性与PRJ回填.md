# 立项：`cost_profile` 可算性与 PRJ 回填

> **性质**：立项说明，**不是施工单**。只把问题定死，不排期、不承诺批次、不替裁定做选择。
> **母本**：`软件工程元框架成文法.md`，4,807 行／589,640 字节／`sha256 d6829e70…`（本文件不改变母本）。
> **数据侧**：`registry/method_registry.yaml`（138 条）、`registry/profiles.yaml`。

## 0. 一句话

`cost_profile` 现在是人读的散文：110 条有该字段的条目里，**109 条 `ops_cost` 是方括号散文、0 条带量纲**，而母本 6.5 的 Q4 公式要求 `cost_ledger(quantified)`——量化清单无源可生成。同时 PRJ-001…011 共 77 个代价格是空白。两件事绑在一起：**A 不定，B 不能开工**。

## 1. 背景（实测，数字均可复现）

| 指标 | 实测 | 复现命令 |
|---|---|---|
| 条目总数 | 138 | `cd registry && python3 -c "import yaml;print(len(yaml.safe_load(open('method_registry.yaml'))['entries']))"` |
| 有 `cost_profile` 的条目 | 110 | 同上，改判 `e.get('cost_profile')` 非空 |
| 无 `cost_profile` 的条目 | **28**（PRJ 11、SRC 8、GOV 6、GRD 3） | 见附录 C-2 |
| `ops_cost` 非空条目 | 110 | 附录 C-3 |
| `ops_cost` 为方括号散文 | **109/110** | 附录 C-3（判 `'[' in ops_cost`） |
| `ops_cost` 带量纲（`数值+单位`） | **0/110** | 附录 C-3（正则 `\d+(ms|秒|分钟|小时|人日|%|GB|次|元…)`） |
| **机器可读率**（带量纲／有 `cost_profile`） | **0%** | 同上 |
| `cost_ledger` 的**实现** | **0 处** | `grep -rn "cost_ledger" --include=*.py . \| wc -l` → 0；文本出现 20 处，全部是谓词登记与散文引用，无产生该量的代码 |

> **与任务书数字的出入（据实说明）**：任务书写「42/138 条目无实质代价内容」「50/110 明写母本未量化」。按我能定义并复现的口径对不上：无 `cost_profile` 是 **28**；`ops_cost` 含「未量化」字样仅 **1** 条，cost 七字段任一含「母本」是 **57** 条。两种口径（全字段占位、任一字段占位）也都不产生 42／50。下文一律用上表口径，**不复用这两个数**。

## 2. 范围与非范围

**范围 A：`cost_profile` 的可算性**——让「量化代价」这件事有机器可读的回答，或明确承认它没有。

**范围 B：PRJ-001…011 的 77 格回填**——11 条 × 7 子字段（`latency_budget_delta`／`failure_modes`／`consistency_impact`／`observability_requires`／`ops_cost`／`skill_prerequisites`／`aggregation_semantics`）。

**非范围**：

- **GOV（6 条）不在本立项内**。取证结论是**无据**（见 §6），既不能并入 B，也不能按「不适用」删 NA；先裁定，再谈格子。
- **SRC／GRD（11 条）**已判 `participates: false`，`cost_profile` 整段合法缺省，不欠账。
- **不改母本文本**、不改检查器逻辑、不动基线——本立项只产出裁定所需的问题定义。
- **不含 0.18.4 的变体表补登记**（属文档债，见 §3.3，可独立先修）。

## 3. 依赖与前置

### 3.1 首要依赖：A 未定，B 不能开工

77 个格子该填**散文**还是**量纲值**，取决于 A 的二选一：选 ① 则格子必须落成可解析格式并按格式验收；选 ② 则格子只需人读清楚、不追量纲。**在 A 定稿前回填 B，等于先押注、再补依据**——回填值会在 A 定稿后大面积返工，且可能制造「看起来量化、其实不可解析」的假精确（母本 0.17.7 门槛 2 正是防这个）。

### 3.2 B 的当前红项（回填的目标）

`project.py --check` 现在 22 条硬失败，全部来自 PRJ：

```
[M2] PRJ-001 缺 ['cost_profile.latency_budget_delta', … 7 项]
…（PRJ-001…PRJ-011，共 11 条 M2）
[C-ST] PRJ-001 因 M2 未过，status 回落 draft 不计入 seed 资格
…（共 11 条 C-ST）
```

复现：

```bash
cd registry && python3 scripts/project.py --check; echo exit=$?   # exit=1
grep -c '^| PRJ-.*✗' projections/自检报告.md                      # 11
```

### 3.3 可独立先修的文档债：PRJ 的 `variant` 过期陈述

`profiles.yaml` 的 PRJ 剖面写着「缺口：0.18.4 未登记方面 10 的规程变体」，而 0.18.4 第 9 行已登记「投影词汇（10）｜S3 现状空间主导（既有文档生态，0.11）；受众纪律（10.2.1）在 S0 的 DP 声明中强制填写」。该注记落后于母本，属**文档债**，与 A 的选择无关，可先修（按 0.22 承诺一，修法是就地加「已被 0.18.4 覆盖」旁注或经裁定删缺口语，不静默改写原文）。

## 4. A 的二选一（不替裁定做选择）

### 选项 ①：给可量化子字段定义取值格式

**做法**：在 0.17.2 的 `cost_profile` 子字段定义处，为可量化子字段（至少 `latency_budget_delta`、`ops_cost`）规定取值格式，例如 `<数值><单位>/<基准>`（基准＝单次调用、单节点、每千次请求等），并规定缺值如何表达（`unknown` 与 `not_applicable` 必须可区分）。

**必须一并定义的**：

1. **哪些子字段必须量化**（其余可保持散文，但要有白名单）。
2. **量纲封闭表**（ms／秒／人日／元／GB／次……），允许的算子（Σ／max／单调）。
3. **缺值语义**：`未知` ≠ `不适用` ≠ `未填`，三者机器可区分。
4. **迁移口径**：110 条存量条目的 109 条方括号散文如何转（人工逐条 or 标记 `unknown`）。

**代价**：改 0.17.2 schema；改 `project.py` 的 M2／C-KP／占位符口径与 `predicate_vocabulary` 的 `cost_ledger` 定义；存量 110 条要么人工重写、要么批量打 `unknown`（后者会让「机器可读率」名义达标但实质空洞，须另设指标防自欺）。

**收益**：6.5 的 Q4 `cost_ledger(quantified)` 第一次有源；S4 包络校验与 S5 保守界判据从「读散文」变成「比数值」；跨条目聚合（`aggregation_semantics`：itemwise／additive／grouped_max／weighted_avg）才有意义。

### 选项 ②：承认只供人读，撤掉 `cost_ledger` 承诺

**做法**：明写 `cost_profile` 为**人读字段**，不承诺机器量化；同步撤掉或改写 6.5 的 Q4 公式（`∃ cost_ledger(quantified)`），并改 0.17.4 消费者一的 S4／S5 字段消费表述，避免「公式要求量化、字段只有散文」的悬空。

**必须一并处理的**：`predicate_vocabulary.yaml` 中 `cost_ledger` 谓词条目（现挂 6.5，`verified: true`）是删除、降级还是标注「不实现」；6.2.4 的 Σ 聚合细则若依赖量化，需同步限定为「有人读数值时可用」。

**代价**：失去跨条目代价聚合与不可区分时的保守界判据（S5 分支二）；6.5 的 Q4 从「可判定」退回「不可判定」，Q4 覆盖的范围要重划；已有依赖 `cost_ledger` 的散文（20 处）需逐处回改。

**收益**：文档与数据一致，不再有「公式要求、字段给不出」的结构性假承诺；检查器不必为不可能的性质背债。

## 5. 判据

### 5.1 A 的验收判据

**先定基线**：机器可读率 = 带量纲 `ops_cost` 条目数 ÷ 有 `cost_profile` 条目数 = **0/110 = 0%**。

```bash
cd registry && python3 - <<'EOF'
import yaml,re
E=yaml.safe_load(open('method_registry.yaml',encoding='utf-8'))['entries']
U=re.compile(r'\d+(?:\.\d+)?\s*(?:ms|毫秒|秒|分钟|小时|人日|人月|%|GB|MB|次|元|美元)')
ops=[(e['entry_id'],str(e['cost_profile']['ops_cost'])) for e in E
     if (e.get('cost_profile') or {}).get('ops_cost')]
q=[i for i,s in ops if U.search(s)]
print(f'{len(q)}/{len(ops)} = {len(q)/len(ops):.1%}')
EOF
```

- 选 ①：目标值由裁定给出（建议以「可量化子字段 100% 合规、`unknown` 可区分」为准），且必须给出**反自欺指标**（如「标 `unknown` 的比例不得超过 X%」，否则批量打 `unknown` 即可刷满合规率）。
- 选 ②：目标改为「`cost_ledger` 在母本与谓词表中不再作为量化承诺出现」，判据是 `grep -c cost_ledger` 的每一处都有新语义，且 6.5 的 Q4 公式措辞已改。

### 5.2 B 的验收判据

- `project.py --check` 的 PRJ 红项 **22 → 0**（M2 11＋C-ST 11）；
- C-ST 11 条随 M2 转绿后同步复核（不得靠回填一个字段蒙混，7 子字段齐全）；
- 有 `cost_profile` 条目数 110 → 121（PRJ 11 条补入），机器可读率按 A 的口径重算并记录。

```bash
cd registry && python3 scripts/project.py --check; echo exit=$?   # 期望 0
grep -c '^| PRJ-.*✗' projections/自检报告.md                      # 期望 0
```

## 6. 附：GOV 取证结论（无据，故不入范围）

以 0.18 规程本身取证，三档结论为 **③ 无据**：

- **① 直述：无**。0.18–0.18.8 全节 **0 处**出现「GOV」，**0 处**出现「治理」（`awk 'NR>=313 && NR<=455' … | grep -n "GOV\|治理"` 无命中；0.18.8 单节同样无命中）。
- **② 可推：不成立**。0.18.2 S1 的候选式逐字为 `{E ∈ registry | kind(E) 匹配 DP ∧ status(E) ∈ {active, seed(bootstrap)} ∧ applicability(E) 对 F 求值为真}`——**按 kind 匹配决策点，不按方面排除**，GOV 在结构上不被排除。0.18.4 变体表 9 行（方面 1、2、3、4、5、6、8、9、10），无方面 7／GOV，但该表**未声明为穷举**；反向还有两处拉力——0.18.1「（kind 枚举 0.17.3 全覆盖）」、0.17.3「每 kind 的选取算法剖面（哪些步骤必填哪些字段）在 0.18.4 实例化映射中登记」，都与表的缺失直接矛盾。三条线索（表缺行、0.18.1 全覆盖、0.17.3 断言）指向不一致，不能据此推出「不参与」。
- **③ 缺口具体缺哪一句**：缺一句**明确**「GOV 类条目不进入 0.18 质量属性选型，其消费路径为 0.5（ADR 亚型）与 7.2.3／7.2.4（简记格式与 materiality 判据 f）的模板引用」。
- **④ 这句话由谁承担（两个候选，须一并裁定）**：
  - **候选一：0.18.1 适用范围补排除句**。只关 GOV，改动面最小：只动 `0.18.1#p-1`，该段 LIVE 入向锚 **0**；条款号 214、units 7,407 均不变；仅该段指纹变化后重冻 fps。
  - **候选二：0.17.3 kind 表补「消费方」列**。把「每 kind 的消费方」显式化，会同时暴露 0.18.4 的方面缺口（STP／DFL／SCH／CFG 等，见施工单 R-10）；该条 LIVE 入向锚 **40**（整条 23＋行锚 17），18 行文本全变，units 不变但须重冻 fps。
  - 两者对 0.18.1／0.18.4 矛盾的处理方式不同：候选一只是把 GOV 排除出选型，不解释其余 kind；候选二让「哪些 kind 进 0.18、由谁消费」成为表内可查事实。**与 R-10 同批裁定。**
- 现状事实：GOV 条目实际被当作**模板／判据**消费（0.17.3 种子源 `0.5/7.2.3`；母本 2558 行「治理模板 kind = GOV」；7.2.2 的 `materiality` 判定谓词 f 登记为 GOV 条目）。这只是「另有用途」，**不能反推「因此不参与选型」**——本立项不据此判真假，也不由它决定 B 的范围。
- **R-10 补证（2026-11-11，详见施工单 §1bis R-10）**：
  - **覆盖单位**：0.18.4 列名是「决策点（方面）」，一行＝一个或一组**行名显式列出的决策点**（可合并，如「所有权/一致性（4）」），既不是整方面，也未声明按 kind 覆盖。故缺口按原文是 **8 个**（STP／DFL／RLP／SCH／CFG／GRD／SRC／GOV）；按整方面读才是 1 个（GOV）；「3」是混合读法，原文不支持。
  - **五个 `participates: true` 却表无行的 kind**（STP／DFL／RLP／SCH／CFG）三档定性均为 **未定义**：其 `variant` 逐字转抄 0.18.4 的「所有权/一致性（4）」「协调模式（5）」行（SCH／CFG 后半句为数据侧追加、母本无出处），`source` 仍只写 `0.18.4`；0.17.3 既说「登记」又限定「每 kind」，故 0.18.4 是唯一登记处。未定义的是**该 kind 的变体**，通用 S0–S6 仍适用。（若 Q2 裁为「0.18.4 只是摘要」，此定性改判「摘要不全」。）
  - **M2 现状**：GOV 6 条实测通过（GOV-001：required 18 项全部在案，N-A 9 抵扣），当前不计欠账；若 Q6 裁 `true`，则 6×7＝42 格并入 B。
  - 裁定所需的最小问题集（6 问）见施工单 R-10 补证三；GOV 的答案（Q6）与 Q1–Q5 同批给出。
  - **待裁定提案**：Q1–Q6 的推荐项、依赖前提、理由与可直接落地的措辞见施工单 R-10「待裁定提案」；全部为提案，母本与 registry 均未据此改动。

**条件性文本（备用，不写入母本）**：若日后裁为 `false`，可与 SRC／GRD 句式对齐为——「GOV 不参与 0.18 质量属性选型（0.18.2 S1 按 kind 匹配决策点，治理模板无对应 DP；0.18.4 未登记方面 7 剖面），由 0.5／7.2.3／7.2.4 作为模板与判据消费。」若裁为 `true`，则 GOV 6 条 × 7 子字段 = **42 格**并入 B，来源记「本次取证裁定」。

## 7. 风险

| 风险 | 说明 | 缓解 |
|---|---|---|
| 选 ① 后「批量 unknown 刷合规」 | 机器可读率名义达标、实质仍空 | 指标必须成对：合规率＋`unknown` 上限 |
| 选 ② 后 S5 保守界失去判据 | `ops_cost` 无法比较，不可区分时只能升级人类 | 同步把 S5 分支二的判据改写为 `typical_reversibility` 单判据或显式升级 |
| B 先于 A 开工 | 回填值在 A 定稿后返工 | 把 §3.1 依赖写进 B 的开工前置，未定 A 不开 B |
| PRJ 11 条被继续当「不适用」处理 | 与 SRC／GRD 混为一谈，账面变绿、实质缺项 | 保留 M2 红项作为欠账证据，不删 NA、不改 `participates` |
| GOV 长期悬空 | 6 条无判据，检查器既不放行也不报 | 保持「未判定」并登记缺口句（§6），不擅自择一 |

## 8. 不做会怎样

- **A 不做**：6.5 的 Q4 永远是悬空公式，`cost_ledger` 永远只有谓词登记没有实现；「代价可算」停留在口头，S4／S5 继续读散文；每新增一条目，就在堆一层不可聚合的文本。
- **B 不做**：22 条硬失败长期挂在 `--check` 上，成为「已知红」的噪声；红项一旦成为常态，新增真缺陷会被淹没——这正是本批花力气把红项压到「只剩 22 条已知欠账」的原因。
- **两件都不做**：`cost_profile` 既不可算、也不完整，而它被 0.17.4 列为 S4／S5 的消费字段——字段消费链在文档上是通的，在数据上是断的。

## 附录：复现命令

**C-1 条目与 `cost_profile` 覆盖**

```bash
cd registry && python3 - <<'EOF'
import yaml
E=yaml.safe_load(open('method_registry.yaml',encoding='utf-8'))['entries']
cp=[e for e in E if e.get('cost_profile')]
print('entries',len(E),'with cost_profile',len(cp),'without',len(E)-len(cp))
EOF
```

**C-2 无 `cost_profile` 的 kind 分布**

```bash
cd registry && python3 - <<'EOF'
import yaml,collections
E=yaml.safe_load(open('method_registry.yaml',encoding='utf-8'))['entries']
print(collections.Counter(e['kind'] for e in E if not e.get('cost_profile')))
EOF
```

**C-3 `ops_cost` 形态**

```bash
cd registry && python3 - <<'EOF'
import yaml,re
E=yaml.safe_load(open('method_registry.yaml',encoding='utf-8'))['entries']
U=re.compile(r'\d+(?:\.\d+)?\s*(?:ms|毫秒|秒|分钟|小时|人日|人月|%|GB|MB|次|元|美元)')
ops=[str(e['cost_profile']['ops_cost']) for e in E if (e.get('cost_profile') or {}).get('ops_cost')]
print('ops',len(ops),'bracket',sum(1 for s in ops if '[' in s),'dimensioned',sum(1 for s in ops if U.search(s)))
EOF
```

**C-4 `cost_ledger` 的实现数**

```bash
grep -rn "cost_ledger" --include=*.py . | wc -l     # 0
```

**C-5 当前红项**

```bash
cd registry && python3 scripts/project.py --check >/dev/null 2>&1; echo exit=$?
grep -c '^| PRJ-.*✗' projections/自检报告.md
```
