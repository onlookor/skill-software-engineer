# 最小垂直切片运行记录（2026-11-12）

> 目标：第一次把「成文法 → 技能卡片 → 真实仓库跑 S0–S6 → 10.2.5 六判据」走一遍。
> 结论先行：**规程走到了 S6(iii) 停住；10.2.5 六条中 1 条通过（判据三，且是切片口径）、5 条 fail／不可判定。**
> 本记录中每条判断都标 `[规范]`（编译规范/母本写明）或 `[自定]`（规范未写、本次自定）。未改母本、未改 registry 数据。

---

## 0 范围与对象

| 项 | 值 |
|---|---|
| 运行对象 | `/home/wgz/projects/pact-dsh` @ `0f9b357`（真实小仓库；Node.js DSH 插件；只读，未改动） |
| 对象规模 | `src/*.js`＋`index.js`＋`loop.js` 约 1.0k 行；零运行时依赖；peer dep 仅 `@deepseek-ai/dsh-agent-loop ^0.2.1-rc.2` |
| 决策点 | `DP-1-STYLE`：治理判定路径（agent loop 钩子 ↔ PACT 后端）采用哪种通信风格 |
| 候选 | STY-001 同步请求-响应、STY-002 异步消息 |
| 下游引用 | PRJ-001（1.4 架构评审投影义务）、PRJ-002（2.4 分解评审投影义务）——只在 S6 的人类层投影义务处引用，**不是 S6 步骤输入** |
| 卡片 | `G-CAND-01`（0.18 选型规程总纲卡，编译规范 2.2 规定 `G` 前缀） |
| 产物 | `artifact.yaml`（版本三元组）＋`fvr-G-CAND-01.yaml`＋`whiteboard-pact-dsh.yaml` |
| 忠实性检查 | `check-card.py` → `fidelity.json` |

选 4 条的理由：STY-001/002 同属 1.2.3 同一决策点、applicability 可直接对仓库事实求值；PRJ-001/002 是该决策在方面 10 的投影义务承接者，能让"人类层投影"这条线也被真实引用。没有扩到全量（registry 共 138 条）。

---

## 1 选中条目（逐条核对 seed 资格）

| 条目 | kind | status | 在本切片中的角色 | 关键字段 |
|---|---|---|---|---|
| STY-001 同步请求-响应 | STY | seed | 候选 | applicability 3 项；delivery_space 空；envelope 3 项；constraints_imposed→方面 2/6/10（全 hard）；typical_reversibility=costly |
| STY-002 异步消息 | STY | seed | 候选 | applicability 3+1+1 项；envelope 3 项；constraints_imposed→方面 3/5/6/10；typical_reversibility=costly |
| PRJ-001 1.4 架构评审：系统整体组织原则 | PRJ | seed | S6 投影义务的承接条目 | 投影规则：评审必须覆盖 1.5 拓扑谓词集并表达所选风格 |
| PRJ-002 2.4 分解评审：单元边界与依赖 | PRJ | seed | S6 投影义务的承接条目 | 投影规则：评审必须覆盖 2.5 边界谓词 |

`[规范]` 0.17.7 六项准入：四条均已 `seed`，`project.py --check` 在册无硬失败（138 条全量口径）。

---

## 2 卡片与产物

- 卡片：[`G-CAND-01.card.yaml`](G-CAND-01.card.yaml)
- 卡片自检：`F1=pass`、`F2=escalate`（1 个名字）、`F3(full)=fail`（39 条硬性质覆盖 5 条）、`F3(scoped)=pass`、`E4 match=true`
- 产物清单：[`artifact.yaml`](artifact.yaml)；FVR：[`fvr-G-CAND-01.yaml`](fvr-G-CAND-01.yaml)；白板：[`whiteboard-pact-dsh.yaml`](whiteboard-pact-dsh.yaml)
- 检查器：[`check-card.py`](check-card.py)（pilot 工具，不是 `registry/scripts` 正式检查器）

`[规范]` 卡片六字段骨架、`G` 前缀、`source_anchor` 到步骤级、`discipline_checks` 绑硬性质、`approval_route` 的 `FM-2 → 0.10 三出路`，均按编译规范 2.2 写。
`[自定]` `artifact_version` 用标签 `pilot-20261112.1` 指向产物；`framework_version` 用母本 sha256 前 12 位（母本无版本号，见 §7 D-3）。

---

## 3 S0–S6 逐步判定

| 步骤 | 判定谓词（母本 0.18.2） | 本次结果 | 依据 | 失败分支 |
|---|---|---|---|---|
| S0 | `facts_sourced(F) ∧ constraints_materialized(C)` | **pass（条件）** | 10 条事实全部有指针（`system:path#Lx`，`[自定]` 出处类型）；C＝DSH peer dep 外部强加＋无上游已定决策 | 未触发；但 goal set 不在 S0 输入清单，漏检在 S4 暴露 |
| S1 | `candidate_set ≠ ∅` | **pass** | `candidate_set={STY-001}`；STY-002 applicability=false（F3/F5/F6/F7） | FM-3 未触发 |
| S2 | `survivor_set ≠ ∅ ∧ 无 hard_conflict` | **pass** | `survivor_set={STY-001}`；STY-004 tension 不在候选集；无已定条目 | FM-4 未触发 |
| S3 | `feasible_set ≠ ∅` | **pass（CH-B）** | `feasible_set={STY-001}`；`skill_prerequisites` 两项在代码中为零命中（F8）→ 按 CH-B 保守假设＋可推翻指标，不排除 | CH-B 已记录；FM-4 未触发 |
| S4 | `∃c: verdict(c) ∈ {reachable, reachable_with_cost}`（对全部硬目标） | **blocked** | 无方面 6 目标集（F9）；envelope 的 `bound_expr` 全是符号式，无场景参数值 → three_value 无法赋值 | 规范无对应分支 → `[自定]` 按 0.6(a) 走 CH-B |
| S5 | `selected_entry ≠ ⊥` | **pass（条件）** | 只剩 STY-001，默认选中；质量 verdict 缺失（不是 reachable） | 分支一/二都不适用（无 Δscore） |
| S6 | 决策记录＋谓词 diff＋版本向量推进 | **blocked（停在 iii）** | (i)(ii) 完成：impact_scope={2,6,10}、reversibility=costly → 完整 ADR＋批准；(iii) entry→`style(scope,S)` 映射缺失；(v) 批准不可达 → FM-2 → costly 只许阻塞等待 | FM-2 触发；SM-DR=`blocked` |

### 3.1 逐条事实（selection log 主体）

`[规范]` 事实出处门槛按 0.4：每条事实带 `source_ref`＋`trust_grade`。`[自定]` 2.1 的 `source_type` 只有 `{clause_id,bib_id,row_id}`，代码事实无类型可填；本记录用 `system:path#Lx` 作为 pilot 第六类，**不主张为规范内合法值**（见 §7 D-1）。

| ID | 事实 | 值 | 指针 | 强度 |
|---|---|---|---|---|
| F1 | `[需要即时结果]`（治理门） | true | `system:pact-dsh/src/govern.js#L79-L90`（`onPreStep` 在 `next()` 前 `await decide`）；`#L97-L108`（`onPreTool` 同） | 强 |
| F2 | `[调用链短]` | true | hook → `onPreTool` → `decide` → `enabledOrNull` → `backend.enabled`，进程内 3 跳；`system:src/pact-backend.js#L52`、`src/wasm-backend.js#L59` | 强 |
| F3 | `[存在可用消息中间件]` | false | `system:pact-dsh/package.json#L27-L29`（只有 peer dep，无 dependencies）；全仓无 broker 客户端/配置 | 强（勘察为无） |
| F4 | `[既有平台/中间件提供同步端点能力]` | true | 后端接口 `enabled(participant,key)` 为进程内 async 请求-响应；fake＋wasm 两实现 | 中（判定面未定义，见 A0） |
| F5 | `[需要削峰]` | false | 治理门必须在工具执行前给出判定（F1）；`config.js#L23,L140` govern 模式 failClosed 强制 true | 中强 |
| F6 | `[需要时间解耦]` | false | 同上；观察者在 `observer.js#L47` 的有界缓冲审计路径上，不在门路径 | 中强 |
| F7 | `[存在可靠投递要求]` | false | 门路径无投递语义；仅审计镜像有有界缓冲 | 中强 |
| F8 | 无超时/重试/熔断实现 | true | `grep -R "timeout\|retry\|circuit\|AbortSignal" src index.js loop.js` → 0 命中；`src/govern.js#L55-L64` 仅 try/catch→null | 强 |
| F9 | 无方面 6 目标集/质量场景/SLO 文档 | true | `git ls-files` 无 `docs/`、`adr/`、`slo`、`quality`、`scenario` 文件 | 强（勘察为无） |
| F10 | 外部强加约束：DSH host API | true | `system:pact-dsh/package.json#L27-L29` peer dep `@deepseek-ai/dsh-agent-loop ^0.2.1-rc.2`；README 明确"不重写 ReactLoopAgent" | 强 |

### 3.2 判断（assessments）

| ID | 判断 | 依据 | 强度 |
|---|---|---|---|
| A0 | `[既有平台/中间件提供同步端点能力]` 涵盖"进程内 async 请求-响应" | 1.2.3 行＋1.3 交叉表；但两侧都没定义"同步端点能力"的判定面 | 中；`[自定]` |
| A1 | STY-001 applicability=true | F1∧F2∧A0 | 中强 |
| A2 | STY-002 applicability=false | F3∧F5∧F6∧F7；全部为 false 而非 unknown | 强 |
| A3 | STY-001 无 hard_conflict | compatibility 仅 STY-004 `tension`，且不在候选集；无已定条目 | 强 |
| A4 | S3 不排除 STY-001，按 CH-B 补能力 | F8 显示技能缺口；skill_prerequisites 属 cost_profile，不是 S3 点名的 delivery_space | 中；`[自定]` |
| A5 | S4 无法赋值 | 缺目标集＋缺参数值；three_value 无 unknown | 强；`[自定]` 处置 |
| A6 | S5 选中 STY-001 | 唯一可行候选；verdict 缺失 | 中；`[自定]` 处置 |
| A7 | S6 高影响＋批准不可达 | impact_scope={2,6,10}；reversibility=costly；无批准角色实例 | 强 |
| A8 | S6(iii) 映射缺失 | 0.17.2 条目 schema 无 `style(scope,S)` 的 S 值字段；`formal_anchor` 只有性质 ID | 强；**硬停点** |

### 3.3 候选结论

| 候选 | 结论 | 依据 |
|---|---|---|
| STY-001 | S5 选中；S4 无 verdict；S6 决策 blocked | A1/A3/A4/A6/A7；quality 可达性未证 |
| STY-002 | S1 排除（applicability=false） | A2；非 unknown，无 M15 勘察义务 |

---

## 4 编译忠实性检查（编译规范 6.2–6.5）

| 检查 | 结果 | 说明 |
|---|---|---|
| F1 步骤完整且可溯源 | **pass** | S0–S6 连续；每步 `source_anchor`（`0.18.2-Sn`）都能在母本定位 |
| F2 R1 registry_refs | **pass** | STY-001/002、PRJ-001/002 存在且 `status=seed` |
| F2 R2 谓词名 | **escalate** | `selection_context`：母本 0.18.2 正文有、0.18.6 机器层谓词块无 → 按 6.2 甲类缺口线索 |
| F2 R3 性质 ID | **pass** | M10/M11/M12/M14/M15 在母本登记 |
| F2 R4 失败路由 | **pass** | FM-1/2/3/4/5、CH-B/CH-C 均闭合 |
| F2 R5 上游卡片 | **pass** | 空集 |
| F3 硬性质覆盖（全量） | **fail** | 母本硬性质 39 条，卡只覆盖 5 条；缺 34 条（M20/M22/M23/M24/M25、V1/V2/V5、W1/W2/W4/W7…） |
| F3 硬性质覆盖（切片口径） | **pass** | 仅 M10–M15；`[自定]` 口径，规范无"部分产物"概念 |
| E4 版本一致 | **pass（切片口径）** | 卡片 `artifact_version`＝产物 `label`；`registry_version=1.0.0`；`framework_version` 用内容哈希（母本无版本号） |

`[规范]` 6.5：F1 fail 或 F2 fail → 拒绝发布；escalate 并发 → 不阻塞发布但清单随产物发布。本次 F2 为 escalate，可发布但带清单；F3 全量 fail → **完整产物不可发布**，本卡只能作为 pilot draft。

---

## 5 10.2.5 六判据逐条

| # | 判据 | 结论 | 证据/原因 |
|---|---|---|---|
| 1 | 白板存在且谓词模式与成文法一致（模式版本号匹配） | **fail／不可判定** | 白板记录存在（`whiteboard-pact-dsh.yaml`）；但母本与 0.21 均未声明白板模式版本号，`pattern_version=null`，"匹配"无法证明 |
| 2 | 五个注册表非空且版本在案 | **fail** | 在案：方法注册表（138 条，v1.0.0）、谓词词表（v1.0.0）；PRJ 条目在方法注册表内，无独立投影规则注册表文件。缺实例：批准注册表、守护规则注册表、FVR 注册表 → 2/5（把 PRJ 算入为 3/5），三者无版本 |
| 3 | 技能卡片编译产物版本与注册表版本一致（E4） | **pass（切片口径）** | 卡片↔产物标签一致；registry v1.0.0；framework_version 为内容哈希，等式的"版本"是 `[自定]` 定义 |
| 4 | 全部硬性质 FVR 接线完成且首轮全量执行有证据工件 | **fail** | 只接了 M10–M12/M14/M15；34/39 未覆盖；已接的也只有静态检查记录，无"首轮全量执行"证据 |
| 5 | 评审点集合已排期且有责任人 | **fail** | 无评审排期、无责任人；部署侧无角色注册表 |
| 6 | 部署可行性勘察结论已登记（批准角色、P0 响应、CI） | **fail** | CI＝confirmed_present（`ci.yml#L18-L19` 跑 `npm run check`＋`npm test`）；批准角色、P0 响应＝undetermined；`declared_by` 无法填具名角色（pilot schema §1.2 禁占位）→ 声明不完整，按 undetermined 处理 |

**汇总：1 条 pass（判据三，且依赖自定版本口径）、5 条 fail／不可判定。框架在 pact-dsh 上"未接地"。**

---

## 6 规范覆盖不到的决策点（本切片最重要的产出）

| # | 决策点 | 我选了什么 | 依据 | 性质 |
|---|---|---|---|---|
| D-1 | 代码事实的 `source_ref` 类型 | `system:path#Lx`（pilot 第六类） | 0.4 要求可定位；2.1 只列 clause/bib/row | `[自定]` 类型扩展，不主张入规范 |
| D-2 | "同步端点能力"判定面 | 进程内 `await` 直接返回值＝同步端点 | 1.2.3/1.3 未定义 | `[自定]` |
| D-3 | `framework_version` 取值 | 母本 sha256 前 12 位 | 母本无版本号，E4 又要求版本相等 | `[自定]` |
| D-4 | S0 输入不含方面 6 目标集 | S0 判 pass；S4 暴露后回填 CH-B | 0.18.2 S0 输入清单只列事实/约束 | `[自定]` 回填；母本 S0 漏项 |
| D-5 | S3 的"能力无出处"是否含 `skill_prerequisites` | 含，但按 CH-B 保留候选、不排除 | 0.17.2 把 skill_prerequisites 放 cost_profile；S3 只点名 delivery_space | `[自定]` |
| D-6 | S4 缺目标集/参数时的路由 | 按 0.6(a) 不决定性 → CH-B | S4 失败分支只覆盖"全部候选对某硬目标 unreachable" | `[自定]` 跨条路由 |
| D-7 | S5 的 verdict 缺失（null） | 视为"非 unreachable"，保留并选中 | 0.18.2 S5 输入写"verdict ≠ unreachable"，未定义 null | `[自定]` |
| D-8 | selected_entry → `style(scope,S)` 映射 | **停手，不造字段** | 0.17.2 条目 schema 无承载字段；`formal_anchor` 不是谓词值 | `[自定]` 停手点；需人裁 |
| D-9 | 切片 F3 口径 | 全量 fail＋scoped pass 双报 | 规范 F3 是全量；切片不可能过 | `[自定]` 口径，不主张为规范 |
| D-10 | 白板模式版本号 | `null` | 10.2.5 判据一要求匹配，母本/0.21 未声明 | `[自定]` 记录方式 |
| D-11 | PRJ-001/002 的消费位置 | 只在 S6 输出的人类层投影义务处引用 | S6 步骤文本不含投影；0.9/10.2.2 是下游义务 | `[自定]` 下游接线，不是 S6 步骤 |

---

## 7 卡住点与需人裁项

**硬停点（按用户指令停手，未自行圆）**

- **R-1（S6(iii)）**：0.17.2 条目 schema 没有任何字段承载"选中条目 → 白板谓词实例"的投影。0.18.2 S6(iii) 要求"所涉方面谓词 diff"，但 `formal_anchor` 只给性质 ID（V2/V4/V5），不给 `style(scope, S)` 的 S。要么母本给 0.17.2 加字段（母本让步），要么编译规范定义投影规则（丙类）。**我没有二选一，停在这里。**
- **R-2（S4）**：0.18.2 S4 的失败分支不覆盖"目标集缺失/参数缺失"，S0 输入清单也不含目标集。要么给 S0 增输入＋S4 增分支（母本让步），要么确认 0.6(a) 不决定性可覆盖（无需改母本）。本次按后者执行，但这是解释，不是明文。
- **R-3（F2 R2）**：`selection_context` 是 0.18.2 的 S0 输出谓词，却不在 0.18.6 机器层谓词块。补登记是母本改动；从卡片删去则 S0 输出无处落。需裁。
- **R-4（10.2.5 判据一）**：母本没有"白板模式版本号"的定义；判据一无法可执行判定。需补定义或改判据。
- **R-5（10.2.5 判据六）**：`declared_by` 要求具名角色，pilot 没有。是否允许"人类责任方待补"的临时声明？我按 pilot schema §1.2 判**不允许**，故判据六 fail。

---

## 8 这次切片证明了什么 / 没证明什么

**证明了**

1. 成文法条款可以机械编译成卡片：F1（步骤序列＋步骤级锚点）全通过；F2 的 R1/R3/R4/R5 全通过；E4 版本指针可闭合。
2. S0–S3 可以在真实仓库上按条目字段（applicability／compatibility／cost_profile）求值，排除有记录、有指针。
3. 10.2.5 可以逐条给出可执行判定，而不是只写"已接地"；本次得到明确的 1 pass／5 fail，且每条 fail 都能指到具体缺失对象。
4. 失败点可以定位到条款/字段（S4 分支缺口、S6 投影字段缺口、`selection_context` 未登记、五注册表缺三），不是"整体跑不通"。

**没证明**

1. 没证明编译产物能通过 F3 全量：单卡只覆盖 5/39 条硬性质，按 6.5 不可发布为完整产物。
2. 没证明 S4 能在缺目标集时工作：本次 S4 是 **blocked**，不是 pass；也没有任何候选拿到 reachable/reachable_with_cost。
3. 没证明 S6 能落地：entry→谓词映射缺失，决策停在 SM-DR `blocked`；没有 ADR 被批准，也没有谓词 diff 写入。
4. 没证明 10.2.5 六判据可满足：5 条 fail／不可判定，"框架已接地"不成立。
5. 没证明 PRJ 条目能被 S0–S6 自然消费：它们只在 S6 的下游投影义务处被引用，是 `[自定]` 接线，不是规程步骤。
6. 没证明多决策点、多卡、跨方面依赖、并发协议；本切片只有 1 卡、1 决策点、单写入方。
7. 没证明 FVR 首轮全量执行：只有静态检查与记录，没有执行证据工件。

---

## 9 复现命令

```bash
cd /home/wgz/projects/pact-dsh
git rev-parse --short HEAD            # 0f9b357
grep -R "timeout\|retry\|circuit\|AbortSignal" src index.js loop.js   # 0 命中

cd /home/wgz/projects/skills/software-engineering/pilot/vertical-slice-20261112
python3 check-card.py                 # F1 pass / F2 escalate / F3 full fail / E4 match
cat fidelity.json
```

## 10 文件清单

| 文件 | 作用 |
|---|---|
| `G-CAND-01.card.yaml` | 技能卡片（编译单元） |
| `artifact.yaml` | 产物清单与版本三元组 |
| `fvr-G-CAND-01.yaml` | M10–M15＋E4 的 FVR 条目 |
| `whiteboard-pact-dsh.yaml` | 白板状态、缺失谓词、SM-DR blocked |
| `check-card.py` | F1/F2/F3/E4 检查器 |
| `fidelity.json` | 检查器输出 |
| `run-log.md` | 本记录 |
