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

## 11 R-1 重跑：S5→S6（2026-11-12，编译规范 5.7 生效后）

**输入不变**：`DP-1-STYLE`、`G-CAND-01`、`selected_entry=STY-001 v0.1.0`、同一白板与事实集。

**投影执行**（按 5.7 P1–P3 机械执行）：

| 步 | 结果 | 依据 |
|---|---|---|
| P1 scope | `pact-dsh` | S0 事实绝对指针 `system:pact-dsh/src/govern.js#L79-L90`、`system:pact-dsh/package.json#L27-L29` 给出唯一 system 候选；`system:src/pact-backend.js#L52` 无 system 段，按相对路径记 warning **C-R1-1**（原文保留） |
| P2 S | `(·, ·, 同步请求-响应, ·)` | `STY-001.provenance.source_pointers` 的 `row_id=1.2.3-同步请求-响应` → 槽 1.2.3；其余槽 `·` |
| P3 实例 | `style(pact-dsh, (·, ·, 同步请求-响应, ·))` | 2.3 嵌套 term_list；部分组合，`·` 槽下游求值 unknown |

**S6 逐步对照**：

| 步 | 上次（2026-11-12 首跑） | 本次（R-1 重跑） | 说明 |
|---|---|---|---|
| (i) 影响分级 | pass | pass | `impact_scope={2,6,10}`、`reversibility=costly` |
| (ii) 路由 | 完整 ADR（批准链未实例化） | 完整 ADR（批准链未实例化） | 高影响；批准角色仍缺 |
| (iii) 谓词 diff | **blocked：entry→style 映射缺失** | **pass：实例可生成** | 仅写 `pending_projection`，不写 `committed`（(ii) 未批准；0.7 禁裸写） |
| (iv) 回归触发 | 未达 | 未达 | 依赖 (iii) committed |
| (v) 批准不可达 | blocked | **blocked（当前唯一卡点）** | FM-2 → 0.10；SM-DR=`blocked` |

**结论**：

1. S6 不再卡在 (iii)。5.7 的投影规则足以从 `STY-001` 的既有字段生成 `style(pact-dsh, (·, ·, 同步请求-响应, ·))`，语法（2.3 嵌套 term_list）与语义（1.5 四子维度部分组合）均成立。
2. S6 仍 **blocked**，当前卡在 **(v) 批准不可达**（FM-2 → 0.10）。这是 `SO-PILOT-3`（0.5 批准角色实例缺失），不是投影规则缺口；本次不自行补批准角色。
3. 「能写出」≠「允许写入」：实例只进 `pending_projection`；`committed` 须待 (ii) 批准，版本向量不动。
4. 新增证据缺陷 **C-R1-1**：`system:src/pact-backend.js#L52` 缺 system 段。不阻断本次投影（唯一绝对 system 候选已定），登记为 `SO-PILOT-5`。
5. `SO-PILOT-2` 关闭；`SO-PILOT-1`（S4 目标集）与 `SO-PILOT-3`（批准角色）仍开放。

## 12 第二轮：目标集与批准角色登记、S4/S6 复跑、10.2.5 复判（2026-11-12）

> §3–§5 是首轮（2026-11-12 上午）结论，保留为历史记录；本节是第二轮复跑，冲突时以本节为准。

### 12.1 本轮口径与输入

- 接受 pilot 切片口径：不追 39 条硬性质全认领（F3 全量仍 fail），不扩卡片集到 C4 全量。
- 人类裁定输入：目标集四项（P99 ≤ 500 ms、单机可用性 ≥ 99.0%、变更前置时间 ≤ 1 工作日、单库强一致＋跨服务最终一致 ≤ 5 s）；批准角色三项（主批准人 wgz、备选链空、时限 48 h）。
- 性质：不改母本任何条款；新缺口一律登记决策点。

### 12.2 正式落点（带版本）

| 对象 | 落点 | 版本 | 指纹 |
|---|---|---|---|
| 目标集 | `target-set-pact-dsh.yaml` | `TS-PACT-DSH-001 v1.0.0` | `sha256:3cf0433c…a23` |
| 批准角色注册表 | `registry/approval_registry.yaml` | `pact-dsh v1.0.0` | `sha256:a0457a4e…013` |
| 包络实参绑定 | `envelope-bindings-pact-dsh.yaml` | `EB-PACT-DSH-STY-001 v1.0.0` | `sha256:93bc90cf…d8c` |
| S4 verdict | `s4-verdict-pact-dsh.yaml` | `S4-DP-1-STYLE-20261112 v1.0.0` | `sha256:b8d91cff…537` |
| 决策记录 | `ADR-DP1-STYLE.md` | `ADR-DP1-STYLE` | — |
| 10.2.5 判定 | `10.2.5-verdict-pact-dsh.yaml` | `GA-PACT-DSH-20261112-2 v1.0.0` | — |

框架级 `registry/method_registry.yaml` 未改动（STY-001 仍只有符号式）；实参只落在部署级绑定文件。

### 12.3 S4 复跑

路径模型 `PATH-PACT-DSH-SYNC-001`：3 个同步段（SEG-HOOK / SEG-DECIDE / SEG-BACKEND），单进程；可用性按 1 个独立故障域计。

| 目标 | 代入 | 目标界 | verdict | 余量 |
|---|---|---|---|---|
| G-LAT-01 延迟 | 3 × 150 ms = 450 ms | ≤ 500 ms | reachable_with_cost | 50 ms |
| G-AVL-01 可用性 | 99.5%（上界） | ≥ 99.0% | reachable_with_cost | 0.5 pp |
| G-LT-01 变更前置时间 | 0.5 工作日 | ≤ 1 工作日 | reachable_with_cost | 0.5 天 |
| G-CON-01 一致性 | 单库强一致成立；跨服务 n/a | 单库强一致；跨服务 ≤5 s | reachable_with_cost | 跨服务无制品 |

- 判定谓词 `∃c: verdict(c)=reachable ∨ reachable_with_cost`：**pass**（STY-001 对四个硬目标均 `reachable_with_cost`）。
- **必须同时读的三条限定**：
  1. 实参全是预算/假设，不是实测；pass 是「未被包络界反驳」。
  2. G-AVL-01 的包络是上界式（≤ Π），只能反驳不可达，不能证明可达（D-21）。
  3. G-CON-01 无包络可依（D-19），跨服务子句无制品（D-18）。
- 与首轮对比：首轮 S4 = blocked（无目标集、无实参）；本轮 S4 = pass（有 verdict），代价是引入预算假设。

### 12.4 S6 复跑

| 步 | 首轮 | 本轮 | 说明 |
|---|---|---|---|
| (i) 影响分级 | pass | pass | `impact_scope={2,6,10}`、`reversibility=costly` → 高影响 |
| (ii) 路由 | 完整 ADR＋批准（批准链缺） | **pass** | 完整 ADR＋批准：wgz，2026-11-12T21:29:21+08:00，48 h |
| (iii) 谓词 diff | 映射缺失 | **pass** | `style(pact-dsh,(·,·,同步请求-响应,·))`；version_vector `{1:1,6:1,10:0}` |
| (iv) 回归触发 | 未达 | **已达** | 谓词变更已登记；绑定性质重跑清单见 FVR |
| (v) 批准不可达 | blocked | **解除** | 批准可达（`GOV-PACT-001` 仍为风险） |

SM-DR 迁移：`blocked --re_review(human)--> under_review --approve(human)--> approved --grounding_fail(system)--> provisional`。

**S6 (v) 结论：解除。** 但决策记录不是 `approved` 而是 `provisional`：10.2.5 未过（见 12.5），按母本 10.2.5 末段「未过验收判据而开始产出设计决策…全部标 provisional」。

### 12.5 10.2.5 六判据复判

| # | 判据 | 结论 | 证据 |
|---|---|---|---|
| 1 | 白板存在且模式版本匹配 | **fail** | 白板存在；`pattern_version: null`，母本未定义模式版本号（D-10） |
| 2 | 五注册表非空且版本在案 | **fail（2/5）** | 方法 v1.0.0 ＋ 批准 pact-dsh v1.0.0；守护注册表缺文件；FVR 无版本；投影规则无版本 |
| 3 | E4 版本一致 | **pass** | 卡片 `pilot-20261112.2` = 产物 label；registry 1.0.0；`check-card.py` E4 match=True |
| 4 | 全部硬性质 FVR 接线＋首轮全量执行证据 | **fail（5/39）** | 切片口径明确不追全量；无首轮全量执行工件 |
| 5 | 评审点排期＋责任人 | **fail（待定）** | 责任人 wgz 已登记；排期="产物出来后再定"（人类指示），**未闭合** |
| 6 | 部署可行性勘察三状态＋declared_by | **fail** | 批准 confirmed_present、CI confirmed_present、P0 undetermined；`declared_by: wgz` 已具名；P0 的 `deadline` 无日期可绑（D-16） |

**汇总：1 pass / 5 fail。框架在 pact-dsh 上仍未接地。**

**可评估性结论**：卡片现在**可评估**（S4 有逐目标 verdict、S6 有批准与完整 ADR、E4 一致）；但决策**不生效**，只能以 `provisional` 存在，下游消费受限。要生效须先闭合判据 1/2/4/5/6。

### 12.6 本轮登记的决策点（不改母本）

| ID | 决策点 | 处置 |
|---|---|---|
| D-12 | 目标集无正式 schema/注册表落点 | 落在 pilot 文件，标 `[自定]` |
| D-13 | 0.5.1 要求声明批准角色注册表但无文件/字段 schema | 按 registry 辅助注册表惯例自建，标 `[自定]` |
| D-14 | STY-001 同一 `path` 承载延迟求和与可用性乘积，分解粒度未定义 | 延迟按同步段、可用性按故障域，显式分列 |
| D-15 | 可用性统计窗口与计划内维护口径未指定 | 暂按月度，记 TS-OPEN-1 |
| D-16 | 判据六 `undetermined` 的 `deadline` 无可绑日期 | 记 null 并标待定 |
| D-17 | 判据五评审点排期无日期字段 | 责任人 wgz，排期"产物出来后再定"，pending |
| D-18 | S4 三值 verdict 无 `n/a` | 跨服务子句按 n/a 处理并记录 |
| D-19 | STY-001 envelope 无一致性 metric | G-CON-01 判定标 `[自定]` 外推 |
| D-20 | 0.5.1 未规定备选批准链是否允许为空 | 按"已声明空链、穷尽即不可达"，记 GOV-PACT-002 |
| D-21 | 上界式包络下 `reachable_with_cost` 只能读作"未被反驳" | 在 S4 与 ADR 显式标注 |

### 12.7 文件变更清单

新增：`target-set-pact-dsh.yaml`、`envelope-bindings-pact-dsh.yaml`、`s4-verdict-pact-dsh.yaml`、`10.2.5-verdict-pact-dsh.yaml`、`ADR-DP1-STYLE.md`、`registry/approval_registry.yaml`。
修改：`whiteboard-pact-dsh.yaml`、`artifact.yaml`（`pilot-20261112.2` / seq 2）、`G-CAND-01.card.yaml`（v0.2.0）、`fidelity.json`（重跑生成）、本文件。
未提交 commit（按用户指示）。

### 12.8 复现命令

```bash
cd /home/wgz/projects/skills/software-engineering/pilot/vertical-slice-20261112
python3 check-card.py            # F1 pass / F2 escalate / F3 full fail / E4 match=True
cat fidelity.json

cd /home/wgz/projects/skills/software-engineering
sha256sum registry/method_registry.yaml registry/approval_registry.yaml \
  pilot/vertical-slice-20261112/target-set-pact-dsh.yaml \
  pilot/vertical-slice-20261112/envelope-bindings-pact-dsh.yaml \
  pilot/vertical-slice-20261112/s4-verdict-pact-dsh.yaml
```

## 13 第三轮：补齐判据五/六的日期，10.2.5 复判为 3/6（2026-11-12）

### 13.1 人类批准的输入

- 判据五五个评审点触发点（点一追溯评审 `2026-11-19`；点二/三/五首次 `2026-12-31`、此后每季度；点四发布节点，暂以 `2026-12-31` 兜底）。
- 判据六 P0 保持 `undetermined`，`deadline: 2026-12-31`，`conversion_event: 首次生产部署前`，`declared_by: wgz`。
- 明确要求：不得为了判据好看改状态；判据六 pass 只代表声明完整；判据一/二/四维持 fail。

### 13.2 判据五：五个评审点

| 点 | 形态 | 触发点 | 备注 |
|---|---|---|---|
| RP-1 设计评审 | 日期（追溯） | 2026-11-19 | **批准前时序未满足**：ADR 已于 2026-11-12 批准，本次为追溯评审，不记为时序合规 |
| RP-2 简记包抽查 | 周期 | 首次 2026-12-31，每季度 | 可与 RP-3 同场 |
| RP-3 材料性抽查 | 周期 | 首次 2026-12-31，每季度 | 可与 RP-2 同场 |
| RP-4 验证计划评审 | 发布节点 | 2026-12-31（兜底） | 兜底不是发布节点本身；发布排期确定后替换 |
| RP-5 Waiver 评审 | 按需＋季度空检 | 首次 2026-12-31，每季度 | 避免额外裁剪 ADR |

- 责任人统一 `wgz`。
- 字段形态 `review_points / trigger_type / trigger / interval / owner` 是**本轮部署级约定**（D-17）；母本只有 `scheduled(rp)` 谓词且不在谓词词表，无字段 schema。

### 13.3 判据六：P0 的 deadline

- `state` 保持 `undetermined`（未改成 `confirmed_present`）。
- `deadline: 2026-12-31`；`conversion_event: 首次生产部署前`；`declared_by: wgz`。
- 到期未转的后果按母本 10.2.5：强制转 `confirmed_absent`，并按 9.3 判部署形态可行性缺陷。
- **判据六 pass 只代表声明完整，不代表 P0 响应能力存在。**

### 13.4 复判结果：1/6 → 3/6

| # | 判据 | 第二轮 | 第三轮 | 说明 |
|---|---|---|---|---|
| 1 | 白板模式版本匹配 | fail | **fail** | 未处理；`pattern_version: null` |
| 2 | 五注册表版本在案 | fail | **fail** | 未处理；严格 2/5 |
| 3 | E4 版本一致 | pass | **pass** | 产物推进到 `pilot-20261112.3`，E4 match=True |
| 4 | FVR 全量接线 | fail | **fail** | 未处理；5/39 |
| 5 | 评审点排期＋责任人 | fail | **pass** | 五点触发点齐全；RP-1 为追溯评审 |
| 6 | 可行性勘察声明 | fail | **pass** | P0 补 `deadline`，声明完整；能力仍缺 |

- 汇总：**3 pass / 3 fail**。
- 决策记录仍为 `provisional`：判据一/二/四未闭合。
- 未提交 commit。

### 13.5 文件变更

修改：`10.2.5-verdict-pact-dsh.yaml`（`GA-PACT-DSH-20261112-3 v1.1.0`）、`ADR-DP1-STYLE.md`（§7/§8/§9/§10 同步）、`artifact.yaml`（`pilot-20261112.3`/seq 3）、`G-CAND-01.card.yaml`（artifact_version）、`whiteboard-pact-dsh.yaml`（artifact_version、grounding_status）、`fidelity.json`（重跑生成）、本文件。

---

## 14 第 1 批：可用性口径变更（D-15-A ＋ D-14-A）

### 14.1 口径决定

- **D-15-A**：目标集 G-AVL-01 六要素补齐——统计窗口＝自然月；不可用＝健康探针连续失败 ≥ 1 min；计划内维护不计入分母，但须提前 ≥ 24 h 公告并单独登记。`TS-OPEN-1` 关闭。目标值 99.0% 未变。
- **D-14-A**：`STY-001` 包络拆为 `path_lat`（按执行序的同步段序列，用于 Σ）与 `path_f`（独立故障域集合，同进程内多段计 1 域，用于 Π）。注册表 `1.0.0 → 1.1.0`，处理记录 `MJ-30`。Σ／Π／单调方向三段逐字保留，未新增规范命题、未新增 metric、未改 source 指针。
- 治理：注册表条目变更属 0.13「变更即高影响决策」→ 完整 ADR（`ADR-STY-ENV-01.md`）＋ wgz 批准；批准来源为 2026-11-12 会话指令（D-15-A/D-14-A 打包执行），已在 ADR 头部如实引用。

### 14.2 版本推进

| 文件 | 版本 | sha256（新） |
|---|---|---|
| `registry/method_registry.yaml` | 1.0.0 → **1.1.0**（仍 138 条） | `aaa8361e…435ffd` |
| `target-set-pact-dsh.yaml` | 1.0.0 → **1.1.0** | `d2c1338d…a54386` |
| `envelope-bindings-pact-dsh.yaml` | 1.0.0 → **1.1.0**（新增 `decomposition` 节） | `9fb4908c…6488ad` |
| `s4-verdict-pact-dsh.yaml` | 1.0.0 → **1.1.0** | `43506f54…0c28509` |
| `artifact.yaml` | `pilot-20261112.3` → **`.4`**（seq 4，registry 1.1.0） | — |
| `G-CAND-01.card.yaml` / `whiteboard-pact-dsh.yaml` | `artifact_version` → `pilot-20261112.4` | — |

### 14.3 S4 重跑结果（四行逐条比对）

| 目标 | 代入 | 界 | 余量 | verdict | 与 v1.0.0 比对 |
|---|---|---|---|---|---|
| G-LAT-01 | `path_lat` 3 段 × 150 ms = 450 ms | ≤ 500 ms | 50 ms | `reachable_with_cost` | 不变 |
| G-AVL-01 | `path_f` 1 域 × 99.5% | ≥ 99.0% | 0.5 pp | `reachable_with_cost` | 不变 |
| G-LT-01 | 1 单元 × 0.5 工作日 | ≤ 1 工作日 | 0.5 工作日 | `reachable_with_cost` | 不变 |
| G-CON-01 | 单库强一致成立；跨服务 n/a | 同 | — | `reachable_with_cost` | 不变 |

判定谓词 `pass`；`aggregate_verdict=reachable_with_cost`。本次重跑的唯一动因是输入口径变更，不是新证据。

### 14.4 检查结果

- `project.py --project`：自检 1240 条记录、硬失败 0、软警告 20；F-11 pass（Δlines 11，按 `ADR-STY-ENV-01` 用 `file_bulk` 声明，未触碰锚点与指纹）。
- `check-card.py`：F1 pass／F2 escalate（`selection_context`）／F3(full) fail 34 条／F3(scoped) pass／**E4 match=True**；exit 1 由 F3 全量 fail 所致，与上轮同因。
- 10.2.5 **本批不重跑**：现有 `GA-PACT-DSH-20261112-3 v1.1.0` 的 3/6 针对 `.3` 产物，对 `.4` 已过期；待第 3 批完成后统一重跑。

### 14.5 未闭合与遗留

- D-18（G-CON-01 跨服务子句无合法赋值）、D-19（无一致性包络）、D-21（上界式语义）按第 2、3 批处理。
- 10.2.5 判据一/二/四仍 fail；ADR-DP1-STYLE 仍 `provisional`。
- 未推送；本地 commit 见下一行记录。

---

## 15 第 2 批：0.4 重判硬目标集合（D-18-B）＋ S4 证明强度注解（D-21-B）

### 15.1 D-18-B：G-CON-01 拆分

- 依据母本 0.4 三条件逐条求值：可观测 ✓、有出处 ✓、**可验证 ✗**（本部署无跨服务路径，判定程序不可执行）。
- 处置：原复合目标拆为 **G-CON-01a**（单库强一致，硬，三条件全成立）与 **G-CON-01b**（跨服务 ≤5 s，**软**）。
- 这是**对已批准输入的追溯修改**；目标集 `revision` 记明改了什么、为什么、谁批的（wgz，2026-11-12 会话指令即重新签字）。
- 保守假设 ADR：`ADR-TS-CON-01b.md`（类型＝conservatism-proof；可推翻指标＝首条跨服务路径出现／远端 backend／第二写者）。
- `TS-OPEN-2` 保持 `open`：约束本身未消失，只是不再作为硬目标参与 S4 判定。

### 15.2 D-21-B：proof_strength 注解

- 编译规范：`proof_strength // {analytic_upper_bound, measured_baseline}`，并新增一段明确"**不是第三个值域**，不得替代 three_value，不得据此把 reachable 读成已证明"。
- S4 verdict 每行新增 `proof_strength: analytic_upper_bound`（本切片全部是解析上界／结构事实，无实测基线）。
- **边界**：成文法 > 编译规范，本字段只加注解，不改 `reachable` 语义；母本层面的澄清留给第 3 批 D-21-A。

### 15.3 版本推进

| 文件 | 版本 | sha256（新） |
|---|---|---|
| `target-set-pact-dsh.yaml` | 1.1.0 → **1.2.0** | `7a37e340…fa2990` |
| `envelope-bindings-pact-dsh.yaml` | 1.1.0 → **1.2.0**（`soft_targets` 节） | `3bfb3f89…0fc6ac` |
| `s4-verdict-pact-dsh.yaml` | 1.1.0 → **1.2.0**（`target_grades`／`not_judged`／`proof_strength`） | `11e82e3f…0f76ae` |
| `编译规范.md` | 未版本化（文本变更） | `6b4e485a…52cee9c` |
| `artifact.yaml` | `pilot-20261112.4` → **`.5`**（seq 5；registry 仍 1.1.0） | — |
| 卡片／白板 | `artifact_version` → `pilot-20261112.5` | — |

### 15.4 S4 重跑结果

| 目标 | 级别 | 代入 | verdict | proof_strength |
|---|---|---|---|---|
| G-LAT-01 | 硬 | 450 ms ≤ 500 ms | `reachable_with_cost` | `analytic_upper_bound` |
| G-AVL-01 | 硬 | 99.5% ≥ 99.0% | `reachable_with_cost` | `analytic_upper_bound` |
| G-LT-01 | 硬 | 0.5 ≤ 1 工作日 | `reachable_with_cost` | `analytic_upper_bound` |
| G-CON-01a | 硬 | 单线程单写者，读己之写成立 | `reachable_with_cost` | `analytic_upper_bound` |
| G-CON-01b | **软** | 无路径、不可判定 | **不判定**（`not_judged`） | — |

判定谓词 `pass`（对 4 条硬目标）；`aggregate_verdict=reachable_with_cost`。三条原 verdict 逐条不变；一致性行由复合目标改写为单库子句，verdict 仍为 `reachable_with_cost`。

### 15.5 检查结果

- `check-card.py`：F1 pass／F2 escalate／F3(full) fail 34／F3(scoped) pass／**E4 match=True**（`pilot-20261112.5`）；exit 1 由 F3 全量 fail 所致。
- 本批未改注册表，未触发 `project.py` 的 F-11；registry_version 仍 1.1.0。
- 10.2.5 仍不重跑（对 `.5` 过期），待第 3 批。

### 15.6 未闭合

- D-19（无一致性包络）：G-CON-01a 判定仍属 `[自定]` 外推。
- D-21 母本语义、D-20 备选链空值：第 3 批。
- 10.2.5 判据一/二/四仍 fail；ADR-DP1-STYLE 仍 `provisional`。

## 16 第 3 批：母本两处最小修订（D-21-A／D-20-A）与全套复检

### 16.1 前置行号位移量化

插入前实测（`anchor_index.py` → `targets.csv` 逐锚解析）：

| 口径 | 冻结裸行号锚 | 指向母本 | 错位 |
|---|---|---|---|
| 全量 | **2,937**（legacy 2,928＋prefix 9） | **1,827** | — |
| 变体 B（新增一行） | — | — | **1,562**（231–3702 段 +1＝1,323；≥3703 段 +2＝239）＋1 处区间锚跨 3703 需人工裁定 |
| 变体 A（同段追加） | — | — | **0** |

结论：取 **A**，错位 0，未触及「百处即停」闸门。按 ADR-ANCHOR-01 D3，frozen 侧不重写、不重算；行号未变，连漂移登记都不需要。

### 16.2 母本改动（只加不改）

| 条款 | 行 | 追加句 |
|---|---|---|
| 0.8 | 230（段尾） | 包络是上界式断言；「覆盖目标」只证明「未被反驳」，不构成可达性证明；S4 的可达／有代价可达按「当前证据下未被反驳」解释，须附可推翻指标（D-21-A） |
| 0.5.1 | 3702（段尾） | 备选批准链允许为空但须 `backup_chain: []` 显式声明；空链＝升级链立即穷尽、批准不可达，按 0.10 第三条处置；不得跳过升级或默认通过（D-20-A） |

母本 **4,811 行不变**、591,285→591,753 字节（+468）；`sha256 6d4b0100…`→**`413e3ac4…21c535`**；条款号仍 **214**。

### 16.3 过渡注记撤销（D-21-C 收尾）

- `ADR-STY-ENV-01.md §3.3`：删「本批保留过渡注记」，改指母本 0.8 已明文。
- `ADR-DP1-STYLE.md §9` D-21 行：改为**已闭合（D-21-A／B）**。
- `s4-verdict-pact-dsh.yaml` caveat：改为「母本 0.8 已明文，本注解是其部署级投影」。
- `envelope-bindings-pact-dsh.yaml` `cross_cutting_gaps.D-21`：标 `resolved`，版本 1.2.0→**1.3.0**。

### 16.4 版本推进

| 文件 | 版本 | sha256（新） |
|---|---|---|
| 母本 | 内容哈希 | `413e3ac4…21c535` |
| `envelope-bindings-pact-dsh.yaml` | 1.2.0 → **1.3.0** | `6449cbe4…77b230` |
| `s4-verdict-pact-dsh.yaml` | 1.2.0 → **1.3.0** | `5e55ca75…b6cd2c` |
| `artifact.yaml` | `.5` → **`.6`**（seq 6；framework 新哈希） | — |
| 卡片／白板 | `artifact_version` → `pilot-20261112.6` | — |
| `10.2.5-verdict-pact-dsh.yaml` | 1.1.0 → **1.2.0**（id `GA-PACT-DSH-20261112-4`） | — |

### 16.5 检查结果

- `anchor_index.py --freeze-baseline` 后复跑：15 项全 pass／info、`failures: []`、F-9 986；基线 units／fps **7,470／7,470**（重冻后内容未变）。
- `project.py --check`：**硬失败 0**、软警告 20；`todo.md` 状态块由 `--project` 按事实同步（字节数 +468）。
- `project.py --project`：F-11 **pass**；`file_bulk` 声明 `自检报告.md` Δlines 21（waiver `ADR-DP1-STYLE`——该 ADR §4 记录本次 framework_version 迁移）；其余三个投影 Δlines 0。
- `check-card.py`：F1 pass／F2 escalate／F3(full) fail 34／F3(scoped) pass／**E4 match=True**（`pilot-20261112.6`）；exit 1 仍由 F3 全量 fail 所致。
- 变更历史已按成文法配套文件约定追加至 `软件工程元框架成文法-changlog.md`（2026-11-12 第 3 批）。

### 16.6 10.2.5 第四轮

`GA-PACT-DSH-20261112-4` v1.2.0，针对 `.6` 全量复核：**3/6**，判据三/五/六 pass、一/二/四 fail，**无判据转号**。上一份 3/6 记录（`...-3`）针对 `.3` 产物，已归档。

### 16.7 未闭合

- D-19（STY-001 无一致性包络）：G-CON-01a 判定仍属 `[自定]` 外推。
- 10.2.5 判据一/二/四仍 fail；ADR-DP1-STYLE 仍 `provisional`。
- `approval_registry.yaml` 的 `GOV-PACT-002` 保留为历史登记（母本 0.5.1 已补空链语义，部署早已显式 `backup_chain: []`，未改该文件以避免无谓的版本级联）。
