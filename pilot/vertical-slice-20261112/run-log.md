# 最小垂直切片运行记录（2026-11-12）

> 目标：第一次把「成文法 → 技能卡片 → 真实仓库跑 S0–S6 → 10.2.5 六判据」走一遍。
> 结论先行：**规程走到了 S6(iii) 停住；10.2.5 六条中 1 条通过（判据三，且是切片口径）、5 条 fail／不可判定。**
> 本记录中每条判断都标 `[规范]`（编译规范/母本写明）或 `[自定]`（规范未写、本次自定）。未改母本、未改 registry 数据。

---

## 0 范围与对象

| 项 | 值 |
|---|---|
| 运行对象 | `/home/user/projects/pact-dsh` @ `0f9b357`（真实小仓库；Node.js DSH 插件；只读，未改动） |
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
cd /home/user/projects/pact-dsh
git rev-parse --short HEAD            # 0f9b357
grep -R "timeout\|retry\|circuit\|AbortSignal" src index.js loop.js   # 0 命中

cd /home/user/projects/skills/software-engineering/pilot/vertical-slice-20261112
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
- 人类裁定输入：目标集四项（P99 ≤ 500 ms、单机可用性 ≥ 99.0%、变更前置时间 ≤ 1 工作日、单库强一致＋跨服务最终一致 ≤ 5 s）；批准角色三项（主批准人 user、备选链空、时限 48 h）。
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
| (ii) 路由 | 完整 ADR＋批准（批准链缺） | **pass** | 完整 ADR＋批准：user，2026-11-12T21:29:21+08:00，48 h |
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
| 5 | 评审点排期＋责任人 | **fail（待定）** | 责任人 user 已登记；排期="产物出来后再定"（人类指示），**未闭合** |
| 6 | 部署可行性勘察三状态＋declared_by | **fail** | 批准 confirmed_present、CI confirmed_present、P0 undetermined；`declared_by: user` 已具名；P0 的 `deadline` 无日期可绑（D-16） |

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
| D-17 | 判据五评审点排期无日期字段 | 责任人 user，排期"产物出来后再定"，pending |
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
cd /home/user/projects/skills/software-engineering/pilot/vertical-slice-20261112
python3 check-card.py            # F1 pass / F2 escalate / F3 full fail / E4 match=True
cat fidelity.json

cd /home/user/projects/skills/software-engineering
sha256sum registry/method_registry.yaml registry/approval_registry.yaml \
  pilot/vertical-slice-20261112/target-set-pact-dsh.yaml \
  pilot/vertical-slice-20261112/envelope-bindings-pact-dsh.yaml \
  pilot/vertical-slice-20261112/s4-verdict-pact-dsh.yaml
```

## 13 第三轮：补齐判据五/六的日期，10.2.5 复判为 3/6（2026-11-12）

### 13.1 人类批准的输入

- 判据五五个评审点触发点（点一追溯评审 `2026-11-19`；点二/三/五首次 `2026-12-31`、此后每季度；点四发布节点，暂以 `2026-12-31` 兜底）。
- 判据六 P0 保持 `undetermined`，`deadline: 2026-12-31`，`conversion_event: 首次生产部署前`，`declared_by: user`。
- 明确要求：不得为了判据好看改状态；判据六 pass 只代表声明完整；判据一/二/四维持 fail。

### 13.2 判据五：五个评审点

| 点 | 形态 | 触发点 | 备注 |
|---|---|---|---|
| RP-1 设计评审 | 日期（追溯） | 2026-11-19 | **批准前时序未满足**：ADR 已于 2026-11-12 批准，本次为追溯评审，不记为时序合规 |
| RP-2 简记包抽查 | 周期 | 首次 2026-12-31，每季度 | 可与 RP-3 同场 |
| RP-3 材料性抽查 | 周期 | 首次 2026-12-31，每季度 | 可与 RP-2 同场 |
| RP-4 验证计划评审 | 发布节点 | 2026-12-31（兜底） | 兜底不是发布节点本身；发布排期确定后替换 |
| RP-5 Waiver 评审 | 按需＋季度空检 | 首次 2026-12-31，每季度 | 避免额外裁剪 ADR |

- 责任人统一 `user`。
- 字段形态 `review_points / trigger_type / trigger / interval / owner` 是**本轮部署级约定**（D-17）；母本只有 `scheduled(rp)` 谓词且不在谓词词表，无字段 schema。

### 13.3 判据六：P0 的 deadline

- `state` 保持 `undetermined`（未改成 `confirmed_present`）。
- `deadline: 2026-12-31`；`conversion_event: 首次生产部署前`；`declared_by: user`。
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
- 治理：注册表条目变更属 0.13「变更即高影响决策」→ 完整 ADR（`ADR-STY-ENV-01.md`）＋ user 批准；批准来源为 2026-11-12 会话指令（D-15-A/D-14-A 打包执行），已在 ADR 头部如实引用。

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
- 这是**对已批准输入的追溯修改**；目标集 `revision` 记明改了什么、为什么、谁批的（user，2026-11-12 会话指令即重新签字）。
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
## 17 判据二补齐：守护／FVR／投影三注册面

### 17.1 缺口与处置（只建注册面，不动母本）

| 注册面 | 原状 | 处置 | 新文件／位置 |
|---|---|---|---|
| 守护规则 | 母本 9.2.2 有条目形态，仓库无文件（DATA-SPEC C-12 只有 `status` 字段结论） | 按 `schedules.yaml` 的 meta/entries 惯例建表；5 条均为仓库既有闸门的登记，标 `draft`（9.2.2 要求新增规则＝完整 ADR＋批准，未获批准不得 active） | `registry/guard_registry.yaml` v1.0.0 |
| FVR | `fvr-G-CAND-01.yaml` 有条目但无版本归属 | 建索引表，登记 FVR 集版本与 sha；条目本体仍留卡片侧（10.2.4 以卡片为归属单元） | `registry/fvr_registry.yaml` v1.0.0；FVR 文件加 `fvr_set` 头（v1.0.0） |
| 投影规则 | 编译规范／CHECK-SPEC 有规则，无带版本的注册面 | 建表登记 4 条注册表→人类层投影（PR-01～04，active） | `registry/projection_registry.yaml` v1.0.0 |

新增决策点：**D-22**（守护注册面无文件/字段规范）、**D-23**（投影规则注册面无文件/字段规范）、**D-24**（FVR 注册面无版本归属）。三者均为「母本未给注册面规范、按既有惯例自建」，不改母本。

### 17.2 判据二判定

2/5 → **5/5**（方法 1.1.0＋批准 1.0.0＋守护 1.0.0＋FVR 1.0.0＋投影 1.0.0），10.2.5 总评 **3/6 → 4/6**。

**边界（如实记）**：判据二 pass 只证明「注册面存在且版本在案」。守护规则 5 条为 `draft`，尚不可消费；FVR 集仍只接 6 条性质，覆盖率问题属判据四，不因本判据闭合而消失。

### 17.3 版本与检查

- artifact `.6` → **`.7`**（seq 7）；卡片／白板 `artifact_version` 同步；10.2.5 升 **v1.3.0**（id 不变 `GA-PACT-DSH-20261112-4`）。
- `project.py --check`：**硬失败 0**、软警告 20；`check-card.py`：**E4 match=True**（`.7`），exit 1 仍仅因 F3 全量 5/39。
- `anchor_index.py`：结果见 §17.4。

### 17.4 锚点索引

`anchor_index.py` 实跑：F-1～F-10 全 pass、`failures: []`、F-9 986、INFO-2 仍 2,937 条冻结行号锚（新增三个注册面为 sandbox，未进入 LIVE 约束域，也未引入母本锚）；基线无需重冻。

## 18 判据一闭合：母本定义 `pattern_version`（2026-11-13）

**裁定来源**：人类 2026-11-13「判据一走路线 A」，按 `options-criterion1-20261113.md` 末节写法落地。

### 18.1 母本两处同段追加

| 位置 | 内容 | 备注 |
|---|---|---|
| 0.7 版本化条（@220 句尾） | `pattern_version` ＝白板谓词块（0.21.6）的模式标识，取语义版本 `MAJOR.MINOR`；语义变更递增 MINOR、不兼容递增 MAJOR 并登记 changlog；未递增而块已变更＝声明失效；判据一的「一致」＝白板值＝块声明值 | 只加不改，不增行 |
| 0.21.6 谓词块首行（@865 行尾） | 注释 `// 本块模式版本 pattern_version: pv-1.0；变更按 0.7 语义版本义务递增` | 只加不改，不增行 |

**为什么是两处**：0.7 给语义、0.21.6 给现行值；缺后者则「一致」的右项为空，判据仍不可判定。**为什么 10.2.5 不动**：判据只比对、不定义被比对项，判据自带定义会让判据自证。

**事实性提示（不改条文）**：0.21.6 在母本中的标题是「形式化锚点（M27–M30）」，条文按人类裁定称其为「白板谓词块（0.21.6）」。若后续把「白板谓词块」理解为其他小节，需重新裁定。

### 18.2 兜底检查器

- `registry/scripts/check_pattern_version.py`：PV-1（块声明值与形态）、PV-2（白板值＝声明值）、PV-3（块规范化指纹＝该版本基线；不一致即「块改了版本没升」）三查；`--freeze` 只在版本合法递增后登记新基线。
- `registry/pattern_version_baseline.yaml`：`pv-1.0 → 8889d129c94c…`。
- 规范化算法：去 `//` 注释、去全部空白、去空行后逐行 sha256；已登记 DATA-SPEC D1.3＋D6.7 与 README。
- 实跑：`PV=pass`，`mother_sha_drift=False`（母本哈希与冻结时一致）。

### 18.3 版本与判定

- 母本：4,811 行不变、591,753→**592,233 字节**、`sha256 413e3ac4…`→**`8d9577f4…1d8079`**、条款 **214**。
- artifact `.7` → **`.8`**（seq 8）；卡片／白板同步；framework_version 四类落点同步（artifact、卡片、ADR-DP1-STYLE、ADR-STY-ENV-01）。
- 白板 `pattern_version: null` → **`"pv-1.0"`**；10.2.5 升 **v1.4.0**，判据一 fail→pass，总评 **4/6 → 5/6**；ADR-DP1-STYLE 仍 provisional（判据四未过）。

### 18.4 检查

- `check_pattern_version.py`：pass（PV-1/2/3）。
- `project.py --check`：**硬失败 0**、软警告 20、占位符 1,481＝事实 1＋槽 1,480。
- `project.py --project`：F-11 pass，Δlines 21（`registry/projections/自检报告.md`，waiver `ADR-DP1-STYLE`，`/tmp/expected-changes-pv.json` 的 `file_bulk`）。
- `check-card.py`：F1 pass、F2 escalate（`selection_context`）、F3 全量 fail（5/39，判据四待做）、E4 match=True（`.8`）。
- `anchor_index.py`：F-1～F-10 全 pass、`failures: []`、F-9 986、INFO-2 冻结行号锚 **2,937 条不变**、漂移 **0**（同段追加，未新增行）。

### 18.5 更正（2026-11-13）：0.21.6 不是全量白板谓词块

**发现**：0.21.6 的机器层谓词块只有 5 行（`sm_state` / `sm_transition` / `sm_permission` / `concurrent_invariant` / `snapshot`）；母本共 14 处「**机器层谓词**」块、134 行。原写法「白板谓词块（0.21.6）」把局部当全量，`pv-1.0` 只覆盖 3.7%。

**整改**：0.7 @220 改称「白板谓词集（各节机器层谓词块之并）」并同处声明 `pattern_version: pv-1.0`；删除 0.21.6 @865 行尾注释；`check_pattern_version.py` 改为自动发现全部块（不写死数量），PV-0 打印块清单，PV-3 校验块数／节归属／指纹并可点名增删；基线重算为 14 块、aggregate `0753e743…`。artifact 保持 `.8`。

**实跑**：PV-0/1/2/3 全 pass（14 块、134 行）；`project.py --check` 硬失败 0；`--project` F-11 pass（自检报告 Δlines 21，waiver `ADR-DP1-STYLE`）；`check-card.py` E4 match=True（`.8`）、F1 pass、F2 escalate、F3 5/39；`anchor_index` 全 pass、冻结锚 2,937、漂移 0。判据一仍 pass，10.2.5 **5/6**。

---

## 19 判据四闭合（2026-11-13）：卡片集、FVR 接线与首轮全量

### 19.1 产出

- `registry/scripts/gen_cards.py`：从母本 0.18.2 S0–S6 与 kind 剖面机械生成 8 张实质卡（G-CAND-01..08）＋10 张躯干卡（G-TRUNK-OWN/CSL/DFL/STP/SCH/RLP/DPS/CRD/CFG/SRC），共 18 张。步骤动作逐字取母本；躯干卡只含 `outputs.predicate_writes` 与 `registry_refs`。
- 闭包自检：DAG 无环（单链 18 节点）、被引用卡全部存在、每个 `upstream_predicate` 有写者；跨方面认领写 `cross_aspect_claims`（含 `owner_of_record`）。
- `gen_cards.py --fvr`：8 份 `fvr-G-CAND-0X.yaml`（v1.1.0），每条 `property_id` 接 `registry/checks/` 下真实检查器，`wired: true`；`registry/fvr_registry.yaml` 升 1.1.0（8 集、39 条）。
- `artifact.yaml`：`.8 → .9`（seq 9），卡片清单 18 条＋`dependency_graph`；registry_snapshot 的 fvr_registry 升 1.1.0。

### 19.2 E7 待批：编译规程变更批准记录所需形态

`E7` 现为 escalate：changlog 有「编译规程变更权」与编译规范修订记录，但没有可机读的批准记录。补齐以下记录后 E7 可判定：

1. **前置**：在 `registry/approval_registry.yaml` 增加决策类 `编译规程变更`，主批准人登记为人类用户（`user`），并在 `approval_role_instances` 中给出 `confirmed_present`。当前 4 类中没有这一类，属注册表变更（高影响）。
2. **记录文件**：`registry/compilation_regime_changes.yaml`（新表），每条至少含：
   - `change_id`、`changed_at`（ISO8601）
   - `scope`：被改条款/章节 ID 列表
   - `from_sha256` / `to_sha256`：编译规范文件前后指纹
   - `summary`
   - `approved_by`：必须是人（`user`），`approver_kind: human`
   - `approval_role_class: 编译规程变更`
   - `approved_at`、`approval_evidence`（ADR ID＋会话消息指针）
   - `artifact_seq`、`status: approved`
3. **谁批准**：`approval_registry.yaml` 中「编译规程变更」类主批准人；不得由 agent 自批。
4. **判定**：E7 检查器读到 `status=approved` 且 `approved_by` 为人时转 pass；缺任一字段仍 escalate。

### 19.3 空真复核

首轮 21 条候选空真经复核：8 条为真空真（M8/M14/M20/M25/W7/R8/E1/E2），13 条属「域数据源未登记」不算空真（V1/V2/W1/W2/W4/X1/X2/X5/X6/T4/T6/G3/G7），检查器已改为 `escalate`。清单见 `vacuous-inventory.md`。

### 19.4 实跑

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 pass=25 fail=0 escalate=14 vacuous=8 |
| E3 | pass（39/39 FVR 条目＋检查程序＋首轮 verdict） |
| `check-card.py --all` | cards=18 F1=pass F2=escalate F3(full)=39/39 E4 match=True exit=0 |
| `check_pattern_version.py` | PV-0/1/2/3 全 pass，14 块，aggregate 0753e743… |
| `project.py --check` | 硬失败 0、软警告 20、占位符 1,481＝事实 1＋槽 1,480 |
| `project.py --project` | F-11 pass，Δkeys 0、Δfps 0、Δlines 0 |
| `anchor_index.py` | failures []；frozen_anchors 2,939；drift 0；assertions 仅 info |
| 10.2.5 | **6/6**（判据四 fail→pass），v1.5.0；当时分布 pass 25 / fail 0 / escalate 14 / vacuous 8。当时（v1.10.0）分布 pass 31 / fail 5 / escalate 3 / vacuous 9（fail＝X2／X5／T4／T6／G3） |

- 母本未改动（行数 4,811、sha256 c0bb9879…）；未推送。
- ADR-DP1-STYLE 仍标 provisional：转 approved 属 SM-DR 迁移，本轮未自动执行。

---

## 20 治理回填（2026-11-13）：ADR 转 approved、编译规程变更登记与 E7 转 pass

### 20.1 人类裁定（两项，本轮执行）

1. ADR-DP1-STYLE 转 `approved`，按 SM-DR 正式迁移、不跳级。
2. 建 E7 所需批准记录并回填既有母本改动；`approved_by` 一律 `user`/human，不得 agent 自批；无批准依据者标待补。

### 20.2 ADR-DP1-STYLE：`provisional → approved`

| 项 | 值 |
|---|---|
| 迁移 | `provisional → approved`，trigger `retro_approve`，权限 human（母本 SM-DR 迁移表 @780） |
| 完整链 | `blocked → under_review → approved → provisional → approved`（不跳级） |
| 批准人 | `user`（`approver_kind: human`） |
| 批准时间 | 2026-11-13 |
| 批准证据 | 人类口头批准，来源＝2026-11-13 本轮对话（父会话转达） |
| 同步落点 | ADR 头部＋§2＋§7＋§8＋§10；`10.2.5` 的 `consequence` 与 caveat；`artifact.yaml` 的 `verdicts.adr`（含 `state_history` / `last_transition`）；`checks/v.py::v5` 改为解析状态行 |

10.2.5 版本：v1.5.0 → **v1.6.0**（与第二项一并推进，避免为空改版本）。

### 20.3 批准登记面

- `registry/approval_registry.yaml` 升 **1.1.0**：新增决策类「编译规程变更」，主批准人 `user`（human），`backup_chain: []`，时限 48h；`GOV-PACT-001` 由「四个决策类」改「五个」。
- 新建 `registry/compilation_regime_changes.yaml`（v1.0.0，3 条）：字段按裁定形态；`from/to` 由 git 实算，不估算；哈希链首尾相接且末条 `to_sha256` ＝母本现行 `c0bb9879…`。

| change_id | commit | scope | from → to（前 8 位） | artifact_seq |
|---|---|---|---|---|
| `CRC-PACT-DSH-20261112-01` | `e7afd07` | 0.8（D-21-A）＋0.5.1（D-20-A） | `6d4b0100` → `413e3ac4` | 6 |
| `CRC-PACT-DSH-20261113-02` | `2b58c19` | 0.7 定义＋0.21.6 声明 | `413e3ac4` → `8d9577f4` | 8 |
| `CRC-PACT-DSH-20261113-03` | `a171cb1` | 0.7 改称＋删除 0.21.6 行尾注释（更正，取代 -02 对 0.21.6 的声明） | `8d9577f4` → `c0bb9879` | 8 |

### 20.4 E7 判定口径

`e.py::e7` 不再扫 changlog 文本，改读 `compilation_regime_changes.yaml`：

- 任一条 `approver_kind ≠ human` 或 `approved_by` 非人 → **fail**（0.25.1：Agent 不得自行修改编译规程）；
- 任一条 `status ≠ approved` → **escalate**，点名待补项（不补假批准）；
- `from/to` 断链，或末条 `to_sha256 ≠ 母本现行哈希` → **fail**（母本改了但未登记）。
- 表不存在 → escalate；表存在但无记录 → 空真 pass。

### 20.5 实跑

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=26** fail=0 **escalate=13** vacuous=8 |
| E7 | **pass**（3 条均人类批准，哈希链连续，末条＝母本现行 `c0bb9879…`） |
| E3 / E5 | pass / pass（39/39） |
| `check-card.py --all` | cards=18 F1=pass F2=escalate F3(full)=39/39 E4 match=True exit=0 |
| `check_pattern_version.py` | PV-0/1/2/3 全 pass，14 块，aggregate 0753e743… |
| `project.py --check` | 记录 1,240 条；硬失败 0；软警告 20；占位符 1,481＝事实 1＋槽 1,480 |
| `project.py --project` | F-11 pass，Δkeys 0、Δfps 0、Δlines 0 |
| `anchor_index.py` | failures []，frozen_anchors 2,939，live 3，drift 0（`by_drift: n/a` 全部）；F-1～F-10/CFG-01 全 pass |
| 10.2.5 | **6/6**，v1.6.0；当时分布 pass 26 / fail 0 / escalate 13 / vacuous 8。当时（v1.10.0）分布 pass 31 / fail 5 / escalate 3 / vacuous 9（fail＝X2／X5／T4／T6／G3） |

注：`fvr-full-run-1.json` 已由本次复跑覆盖（现为 pass 26／escalate 13）；首轮分布 pass 25／escalate 14 见 §19.4 与本文件 git 历史。复跑未改任何检查器的判定口径，唯一变化是 E7 读取新的批准登记表。

### 20.6 「待补批准依据」清单

**空。** 三条改动均有可指认的人类批准依据：

- `e7afd07`：人类口令「人类批准按你推荐的方案、打包方式与排序执行……第 3 批（母本修订，一次做完）」，落于 `软件工程元框架成文法-changlog.md`「2026-11-12：试点第 3 批」节（逐字口令）。
- `2b58c19`：人类裁定「判据一走路线 A」，落于 run-log §18＋`options-criterion1-20261113.md`（**转述**，非逐字口令）。人类已于 2026-11-13 明确确认该转述构成批准（**已追认**，`status` 维持 approved，不转 pending）。
- `a171cb1`：人类裁定「走方案甲」，并要求 0.7 改称「白板谓词集」、删除 0.21.6 行尾注释（本轮会话逐字转述，落于 run-log §18.5）。

未补任何假批准；母本未改动、未推送。

---

## 21. 第七轮（2026-11-14）：批 A 登记与 9 个检查器升级

### 21.1 人类裁定（D-A～D-D）

| 编号 | 裁定 | 本轮落地 |
|---|---|---|
| D-A | 批准新增白板登记键，采用白名单，只收母本已定义的键名 | 只在 `whiteboard.domain_data` 下登记母本键名，未自造键 |
| D-B | 先升级 9 个「存在即 pass」检查器为真校验，再补登记 | V2/X1/X2/X5/X6/T4/T6/G3/G7 全部改为校验内容 |
| D-C | X6 记 vacuous；`index.js`／`loop.js` 按独立单元计 | `shared_data_access: []` 显式空集 → vacuous；模块清单含两个入口，T4 按 9 个单元判定 |
| D-D | 先修白板基线，再按 W1/W2 → T4 → X2/X5 → X1 → G3 落批 A | 基线三处已修；批 A 数据已登记；登记人 `user`，agent 不自批 |

批 B（V1/V2/W4/X6/T6/G7 及 G3 回滚部分的新数据）不在本轮范围。

### 21.2 检查器升级口径

统一三态语义（`common.py` 新增 `whiteboard_doc()`／`domain_data()`）：

- **数据源未登记**（键不存在）→ `escalate`，写明缺哪个键；
- **显式空集**（键存在且为空）→ `pass` + `vacuous: true`；
- **数据在案但不满足** → `fail`，逐条点名不满足的条目。

| 检查器 | 升级后的校验内容 |
|---|---|
| V2 | 每条 connects 的 `protocol` 必须 ∈ style 允许协议集；空集 vacuous |
| X1 | 每条 connects 必须被某契约（provider＋consumer）覆盖 |
| X2 | 每份契约必须有 `version` 与 `compat_policy` |
| X5 | `lifecycle: published` 的契约必须带 `adr` 且 ADR 状态 approved |
| X6 | 非空时四条件（`weak_coupling`／`read_only_or_single_writer`／`no_cross_unit_transaction`／`via_data_contract`）均须 True；空集 vacuous |
| T4 | 每个单元须有非空测试；入口单元按独立单元计（D-C） |
| T6 | 已发布契约须有 `contract_tests` 且 `in_ci: true` |
| G3 | 每条部署策略须有 `rollback` 真值且 `compatible_with_style is True` |
| G7 | 每条 P2 信号须有 `alarm_threshold` 与 `trend_window` |

### 21.3 白板基线修三处（D-D 前置）

1. `artifact_version`: `pilot-20261112.8` → `.9`（卡片与 artifact.yaml 早已是 `.9`）；
2. `style.state`: `provisional` → `approved`（与 2026-11-13 SM-DR 迁移一致），`note` 改 6/6（v1.6.0；当时（v1.9.0）真实分布 pass 30 / fail 5 / escalate 4 / vacuous 9，fail＝X2／X5／T4／T6／G3）；
3. 白板内 `grounding_status`: 1/6 → 6 比 0（v1.6.0）。

### 21.4 批 A 登记内容与数据来源

`/home/user/projects/pact-dsh`（`dsh-plugin-pact` 0.1.2）勘察所得，全部为仓库现有事实，无估算：

- `module_inventory`：9 项（`index`、`loop-entry`、`config`、`govern`、`loop-core`、`names`、`observer`、`pact-backend`、`wasm-backend`）；
- `unit_test_inventory`：9 条；`index`、`loop-entry` 的 `test_files: []`；
- `connects`：1 条（`loop-core → pact-backend`，协议 `同步请求-响应`）；
- `contract`：`CT-PACT-BACKEND-01`（`version: "0.1.2"`，`compat_policy: null`，`lifecycle: published`，`adr: null`）；
- `deploy_strategy`：`DEP-PACT-DSH-01`（`rollback: null`，`compatible_with_style: null`）；
- `shared_data_access`：`[]`（显式空集）。

### 21.5 实跑结果

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=29 fail=4 escalate=6 vacuous=9** |
| 10.2.5 | **6/6**，v1.7.0（当时分布 pass 29 / fail 4 / escalate 6 / vacuous 9，fail＝X2／X5／T4／G3；当时（v1.10.0）分布 pass 31 / fail 5 / escalate 3 / vacuous 9，fail＝X2／X5／T4／T6／G3） |
| `check-card.py --all` | cards=18 F1=pass F2=escalate F3(full)=39/39 E4 match=True exit=0 |
| `check_pattern_version.py` | PV-0/1/2/3 全 pass，14 块，aggregate 0753e743… |

`pass 29` 中含 9 条 vacuous（X6 为显式空集，其余为域本身无实例）。

### 21.6 4 条 fail

| 性质 | 原因 |
|---|---|
| X2 | `CT-PACT-BACKEND-01` 缺 `compat_policy` |
| X5 | 该契约为 `published` 但 `adr: null`，无已批准 ADR |
| T4 | 9 个单元中 `index`、`loop-entry` 无测试（D-C 口径） |
| G3 | `DEP-PACT-DSH-01` 缺 `rollback` 与 `compatible_with_style` |

这 4 条不是接线缺口，是升级为内容校验后揭示的真实数据缺口；补齐对应字段后重判。

### 21.7 6 条剩余 escalate（批 B）

V1（无 `dependency_rule`）、W1/W2（`module_inventory` 已登记但需人工核归属）、W4（无 `owned_by`）、T6（无 `contract_tests`）、G7（无 P2 信号）。均在 `escalate-adjudication-20261113.md` 批 B 清单内。

**注**：V2 原在批 B，因 X1 需要 `connects` 才能判定，批 A 一并登记了 `connects`，V2 遂顺带具备数据源并转为 pass（协议在 style 允许集内）。这一项的口径变化由数据依赖导致，非扩大登记面。

### 21.8 判据四口径（人类裁定，2026-11-14）

**裁定**：39 条硬性质**全部具备可复现 verdict 即判据四成立**；fail 属有效结论，不计为判据不成立。10.2.5 维持 **6/6**、v1.7.0 不回退。

**不是豁免**：fail 记录的是真实缺陷，不把未满足的性质记成 pass，也不降低判定力。它与 escalate（数据源未登记、不可判）同属可复现结论，二者都必须逐条登记。

**v1.7.0 时真实分布**：pass 29 / fail 4 / escalate 6 / vacuous 9（此前 pass 26 / fail 0 / escalate 13 / vacuous 8）。**当时（v1.10.0）**：pass 31 / fail 5 / escalate 3 / vacuous 9。凡引用 6/6 处均须同时给出当时或现行分布。

**已知缺陷登记（在案，不在本轮修复范围）**：

| 性质 | 缺陷 |
|---|---|
| X2 | `CT-PACT-BACKEND-01` 缺 `compat_policy` |
| X5 | `CT-PACT-BACKEND-01` 为 `published`，但无 ADR |
| T4 | `index`、`loop-entry` 无测试（D-C：入口按独立单元计） |
| G3 | `DEP-PACT-DSH-01` 缺 `rollback` 与 `compatible_with_style` |

该口径已同步写入 `10.2.5-verdict-pact-dsh.yaml` 判据四的 `interpretation`／`known_defects` 与文件头说明，以及 `artifact.yaml` 的 `scope_note`。

---

## 22. 批 B 第一步（2026-11-14）：契约测试清单登记

### 22.1 可凭仓库事实补齐的项

`/home/user/projects/pact-dsh/test/` 共 8 个测试文件（config、fake-backend、govern、loop-routing、manifest、names、observer、wasm-backend），无契约测试。据此在白板 `domain_data` 登记 `contract_tests: []`（显式空集），未新造键。

### 22.2 结果

| 性质 | 变化 | 依据 |
|---|---|---|
| T6 | escalate → **fail** | `CT-PACT-BACKEND-01` 为 published，但 `contract_tests` 显式为空 |

**当时（v1.8.0）分布：pass 29 / fail 5 / escalate 5 / vacuous 9**；10.2.5 升 **v1.8.0**，仍 **6/6**（附当时分布）。4 条 fail 增至 5 条（新增 T6），已并入 `known_defects`。**当时（v1.10.0）分布：pass 31 / fail 5 / escalate 3 / vacuous 9**。

### 22.3 剩余 5 条 escalate：缺什么、由谁产出

| 性质 | 缺的数据源 | 现状与产出者 |
|---|---|---|
| V1 | `dependency_rule(·,·,forbidden)` 实例 | 仓库只有 11 条实际 import 边（构成 DAG），无显式分层与禁止规则；需架构责任人（`user`）定分层口径 |
| W1 | 接缝封闭的人工核结论 | `module_inventory` 已在案（9 个单元）；JS 无接口声明，机器无法判定「接缝封闭」 |
| W2 | 可独立验证的人工核结论 | 7 个 src 模块有测试，`index`／`loop-entry` 无；是否算「可独立验证」需人判 |
| W4 | `owned_by` 数据所有权声明 | 仓库事实：`src/observer.js` 写 append-only `events.jsonl`（`src/observer.js#L5-L16`）；所有权归属是设计声明，需数据责任人确认 |
| G7 | P2 信号及其阈值/窗口 | 仓库无监控/告警配置；`registry/guard_registry.yaml` 有 GR-005（P2，阈值「漂移只登记不追」，无 `trend_window`） |

### 22.4 待人类选择的两种口径（本轮未定）

| 性质 | 选项 A（后果） | 选项 B（后果） | 选项 C |
|---|---|---|---|
| V1 | 按观测 import 方向登记 11 条反向禁止边 `dependency_rule(v,u,forbidden)` → 反向图必无环 → **pass**；代价：判定近乎同义反复，「反向禁止」是策略声明而非仓库事实 | 先声明 `layer_of`＋分层禁止规则，升级 V1 按层展开 → 需新增登记键与判据；当前无显式分层，须你定层 | 维持 escalate，等架构责任人给分层与规则 |
| W1 | 登记人工核结论（reviewer=`user`、日期、结论）并升级 checker 消费 → pass/fail 由结论定 | 机械化：每模块须有显式导出接口且无未声明跨模块访问 → JS 无接口声明，大概率 fail | 维持 escalate |
| W2 | 登记人工核结论 → pass/fail 由结论定 | 机械化：每模块有独立测试或显式豁免 → `index`／`loop-entry` 无测试，将 fail | 维持 escalate |
| W4 | 登记 `shared_data_access` 审计日志条目 `owned_by: observer`（仓库事实），升级 w4 校验单一所有者 → **pass** | 维持 escalate，由数据责任人确认所有权 | — |
| G7 | 把 GR-005 登记为 P2 信号（阈值在、无趋势窗口）→ **fail** | 等运维定义 P2 信号与阈值/窗口 → 维持 escalate | — |

未自行选择，等待裁定后落下一批。

---

## 23. 批 B 第二步（2026-11-14）：V1/W4 登记，弱校验

人类全量批准两份草案（登记人 `user`），裁定 V1 口径甲、W4 口径丙，均标注为弱校验。

### 23.1 落地内容

| 项 | 内容 |
|---|---|
| V1 | 登记 `layer_of` 9 条（3 层全覆盖）＋`dependency_rule` 3 条 forbidden；检查器改为从 `domain_data` 读条目，仍只判字面层规则无环 |
| W4 | 登记 `owned_by` 2 条：`observer → events.jsonl(write)`、`index → events.jsonl(create_and_configure)`；检查器改为读 `owned_by` 条目并点名归属，仍判 escalate |

排除项：进程级单例（backend 注册表、`FakePactBackend` 单例状态）不算共享数据对象；只读配置不计入；撤回「单写者是否成立」确认项（属判据结果）。

### 23.2 弱校验限制（必须随结论引用）

- **V1**：不展开 `layer_of` 到单元边，pass 只表示禁止层规则无环，**不代表单元级依赖已核**。
- **W4**：不机械核单一所有者，登记后仍判 **escalate**，登记不自动转 pass。

### 23.3 打包升级项

V1/W4 合并为一项「将来升级为机械校验」：

1. V1 按 `layer_of` 展开层规则 × 实际 import 边求值；
2. W4 机械核「对象 → 所有者一对一」「每对象唯一所有者」「写入点归属与登记一致」。

升级前，产物中引用 V1 的 pass 必须同时给出弱校验说明。

### 23.4 实跑分布

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=30 fail=5 escalate=4 vacuous=9** |
| V1 | **pass**（3 条 forbidden 层规则无环；弱校验） |
| W4 | **escalate**（已登记 2 条所有权，待人工核单一所有者；口径丙） |
| 10.2.5 | **6/6**，v1.9.0（真实分布 pass 30 / fail 5 / escalate 4 / vacuous 9） |

剩余 4 条 escalate：W1、W2、W4、G7；5 条 fail：X2、X5、T4、T6、G3。

---

## 24. 批 B 第三步（2026-11-14）：W4 人工核转 pass

人类确认「W4 通过，升级机械校验后再回头看」。据此把该确认登记为 W4 的人工核依据：

- `approved_by: user`、`approver_kind: human`、`approved_at: 2026-11-14`
- 归属确认：`observer` → `events.jsonl` 写入权；`index` → 创建/配置权
- 记录位置：白板 `owned_by` 两条各自的 `human_review` 字段

检查器口径：每条 `owned_by` 都带 human 确认记录时 W4 判 pass；缺记录回退 escalate。pass 属**人工核结论，非机械校验**，已与 V1 同列 `weak_checks`／`packed_upgrade`。

### 24.1 实跑分布

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=31 fail=5 escalate=3 vacuous=9** |
| V1 | pass（弱校验） |
| W4 | pass（人工核） |
| 10.2.5 | **6/6**，v1.10.0（真实分布 pass 31 / fail 5 / escalate 3 / vacuous 9） |

剩余 3 条 escalate：W1、W2、G7；5 条 fail：X2、X5、T4、T6、G3。

---

## 25. 批 B 第四步（2026-11-14）：收掉最后三条 escalate

人类批准按方案 A／机械口径收口，三条各自结局如下。

### 25.1 W1（接缝封闭）：人工核结论 → pass

- 登记位置：白板 `domain_data.human_review`，`property: W1`。
- 记录：`approved_by: user`、`approver_kind: human`、`approved_at: 2026-11-14`。
- 结论文本（原文，供核对措辞）：

> W1 接缝封闭：覆盖面为 module_inventory 全部 9 个单元（index、loop-entry、config、govern、loop-core、names、observer、pact-backend、wasm-backend）。逐一核对模块间调用与 import，未发现经由未声明接口的跨模块访问，无例外。

- 性质：**人工核结论**，不是机械校验；检查器只校验记录字段与结论存在，不做接缝机械核对。与 W4 同类登记（`human_review`），不得计入机械校验通过。
- 已列入 `weak_checks`／`packed_upgrade`（与 V1、W4 打包为将来机械校验项）。

### 25.2 W2（可独立验证）：机械口径 → fail

- 检查器改为与 T4 同构：用 `module_inventory` × `unit_test_inventory` 求无独立测试的单元。
- 实跑结论：`2/9 个单元无独立测试，不可独立验证：['index', 'loop-entry']`。
- 性质：**机械判定 fail**，数据在案（测试清单显式给出两单元 `test_files: []`），不是空真、不是 escalate。

### 25.3 G7（P2 告警）：登记 P2 信号后判 fail

- 登记位置：白板 `domain_data.p2_signals`，`id: GR-005`、`level: P2`、`alarm_threshold: 漂移只登记不追`、`trend_window: null`。
- 实跑结论：`1/1 条 P2 信号缺阈值或趋势窗：["GR-005 缺 ['trend_window']"]`。
- 性质：**机械判定 fail**：有阈值、无趋势窗口；缺 `trend_window` 是仓库 `guard_registry.yaml` 的既有事实。

### 25.4 实跑分布

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=32 fail=7 escalate=0 vacuous=9** |
| W1 | **pass**（人工核结论，非机械校验） |
| W2 | **fail**（index、loop-entry 无独立测试） |
| G7 | **fail**（GR-005 缺 trend_window） |
| 10.2.5 | **6/6**，v1.11.0（真实分布 pass 32 / fail 7 / escalate 0 / vacuous 9） |

7 条 fail：X2、X5、T4、T6、G3、W2、G7；**0 条 escalate**。pass 中含 9 条 vacuous。

---

## 26. 批 B 第五步（2026-11-14）：V1/W4 升机械校验，G7 修复，契约兼容策略草案

人类批准「路线二全做＋路线一 V1/W4」，但仍不改 `pact-dsh`（入口测试、契约文档、部署策略尚缺人类口径）。本轮落地三项。

### 26.1 V1：机械校验（读源码）

- 白板新增 `target_repo: /home/user/projects/pact-dsh`。
- `v1` 改为：按 `module_inventory.path` 读 9 个单元源码，正则提取相对 `import`／`export from`／字面量 `import()`／`require()`，解析到单元 id；逐边用 `layer_of` 映射层并核对 3 条 forbidden 规则；另查禁止层规则图无环。
- 实跑：`机械校验：扫描 9 个单元源码，11 条相对 import 边，逐边核对 3 条 forbidden 层规则无违反；禁止层规则图无环`。
- 反例验证：在临时副本的 `src/observer.js` 注入 `import { loadConfig } from './config.js'`（L2→L1），V1 立即 fail：`1/12 条 import 边违反禁止依赖：['observer(L2-foundation)→config(L1-core)']`。
- 性质：**真机械校验**（读取仓库源码，不是核对登记文本）。

### 26.2 W4：机械校验（读源码写点/创建点）

- `w4` 改为：扫描 9 个单元源码，找出含对象名且有写 API（`appendFileSync`／`writeFileSync`／`createWriteStream` 等）的单元，以及构造写点单元所定义类的单元。
- 实跑：`机械校验：2 条所有权与源码写点一致（events.jsonl 唯一写点 observer；events.jsonl 唯一创建点 index（构造 ['FileSink']））`。
- 反例验证：在临时副本的 `index.js` 注入第二处 `appendFileSync('events.jsonl', …)`，W4 立即 fail：`写点=['index','observer']`，并报「index 同时持写入权与创建/配置权」。
- 性质：**真机械校验**。`owned_by.human_review` 保留为历史证据，但不再是判定输入。

### 26.3 G7：可配置趋势窗 → pass

- `registry/guard_registry.yaml` 的 `GR-005.params` 新增：
  `trend_window: {metric: count, value: 10, configurable: true}`；`metric` 取 `count`（默认）或 `time`（天），`value` 可配。
- 白板 `p2_signals` 同步为同一配置。
- `g7` 改为校验该结构（metric 合法、value>0），缺失或非法即 fail。
- 实跑：`1 条 P2 信号均配置阈值与趋势窗（GR-005=count/10；metric 与 value 可配置）`。
- 性质：**机械判定 pass**；10 次为默认值，人类未另行指定，可随时改。

### 26.4 契约兼容策略草案（只起草）

- 新增 `draft-CT-compat-policy-20261114.md`：对比严格语义化／宽松／契约版本＋弃用窗口三种候选，逐项给出收益、代价、对 X2/X5/T6 的影响、对已发布 0.1.2 的影响与 X2 能否 pass；推荐候选三，窗口「一个小版本或 30 天，取较长者」。
- 未改 `pact-dsh`、未改白板 `compat_policy`、未写 ADR；等人类选定。

### 26.5 实跑分布

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=33 fail=6 escalate=0 vacuous=9** |
| V1 | **pass（机械校验）** |
| W1 | **pass（人工核结论，仍非机械校验）** |
| W4 | **pass（机械校验）** |
| G7 | **pass（机械校验；趋势窗可配置）** |
| 10.2.5 | **6/6**，v1.12.0（真实分布 pass 33 / fail 6 / escalate 0 / vacuous 9） |

6 条 fail：X2、X5、T4、T6、G3、W2；**0 条 escalate**。pass 中含 9 条 vacuous。

---

## 27. 批 A 入口测试（2026-11-14）：T4/W2 转 pass，契约策略选定，回滚草案

人类确认契约策略取候选三、趋势窗默认 10 次不变。本轮在 `pact-dsh` 只新增测试，未改生产代码。

### 27.1 契约策略选定与 ADR 草案

- `draft-CT-compat-policy-20261114.md` 标注「候选三已由人类选定（2026-11-14）」，补充契约版本语义、弃用窗口语义（一个小版本或 30 天取较长者）、版本号示例与未选方案理由；①② 的对比保留。
- 新增 `draft-ADR-CT-PACT-BACKEND-01-20261114.md`：状态 Proposed，记录发布决定、备选、后果、窗口语义与对 0.1.2 的影响；`approved_by` 与 `approved_at` 留空，明确 Agent 不得自批。
- 未写入 `pact-dsh`、未填白板 `compat_policy`；X2／X5／T6 维持 fail。

### 27.2 批 A：index 测试

- 新增 `test/index.test.js`（4 个用例）：`mirrorDir: null` 不建审计文件、只记录 session 事件且只保留白名单字段、effect disposer 退订、非法配置在装监听前 fail fast。

### 27.3 批 A：loop-entry 测试（未改生产代码）

- 新增 `test/loop-entry.test.js` 与 `test/fixtures/agent-loop-stub.mjs`。
- 用 `node:module` 的 `registerHooks` 在测试进程内把未安装的 peer 依赖 `@deepseek-ai/dsh-agent-loop` 解析到本地桩，再动态 import 入口；`PACT_DSH_CONFIG` 在 import 前注入，绕开顶层 `loadConfig` 副作用。
- 覆盖：导出类是 AgentLoop 子类、非法配置导致 import 拒绝、`pactInstall` 把 participants/fakeEnabled 传入 `backendFor`（禁用后端时 pre-step 返回 reject）、effect 释放 4 个 hook。
- `npm test`：**57 tests / 57 pass / 0 fail**。
- 结论：**不需要改生产代码**即可覆盖 loop-entry。

### 27.4 批 C：回滚声明草案（只起草）

- 新增 `draft-DEP-rollback-20261114.md`：对比 `deprecate` 与「发新版回退」的消费者影响、版本号影响、对 `release.yml` 的要求；建议默认「发新版回退为主＋deprecate 配套」，待人类勾选。
- 未改 `release.yml`、未执行 npm 命令、未登记 `deploy_strategy.rollback`。

### 27.5 实跑分布

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=35 fail=4 escalate=0 vacuous=9** |
| T4 | **pass（机械校验：9 个单元均有非空测试集）** |
| W2 | **pass（机械校验：9 个单元均有独立测试文件）** |
| V1／W4／G7 | pass（机械校验，v1.12.0 起） |
| W1 | pass（**人工核结论，非机械校验**） |
| 10.2.5 | **6/6**，v1.13.0（真实分布 pass 35 / fail 4 / escalate 0 / vacuous 9） |

4 条 fail：X2、X5、T6、G3；**0 条 escalate**。pass 中含 9 条 vacuous。

---

## 28. 第十四轮（2026-11-14）：ADR 批准迁入、X2/T6/G3 落地，分布 39/0/0/9

人类按父会话转述的五条全部批准，逐条落地。

### 28.1 ADR 批准并迁入目标仓（X5）

- 新建 `/home/user/projects/pact-dsh/adr/ADR-0002-CT-PACT-BACKEND-01.md`（该仓无既有 `adr/` 惯例，按人类授权新建）。
- 头部字段：`approved_by: user`、`approver_kind: human`、`approved_at: 2026-11-14`、批准依据「2026-11-14 人类批准」、`决策记录状态：**\`approved\`**`。
- 正文记录发布决定、弃用窗口语义、被拒候选、后果、对已发布 0.1.2 的影响与实施项；批准记录节明确「Agent 未自批，状态迁移依据人类 2026-11-14 批准」。
- 检查器适配：`x.py::_adr_state` 先按 `target_repo` 解析 ADR 路径，找不到再回退 pilot 目录，使 ADR 迁出 pilot 后 X5 仍可判。
- 结果：**X5 pass（机械校验）**——`1 份已发布契约均有已批准 ADR`。

### 28.2 X2：兼容策略写入白板

- 白板 `contract[0].compat_policy` 登记候选三：契约版本与包版本解耦（`CT-PACT-BACKEND-01@<major>`，当前 `@1` 对应包 `0.1.2`）；加性变更升 minor；破坏性变更升 major 并保留旧契约面至少一个小版本或 30 天（取较长者），窗口内不得删除；窗口未满删除或未升 major 视为违约。
- `contract[0].adr` 指向 `adr/ADR-0002-CT-PACT-BACKEND-01.md`，`evidence` 补 ADR 与 npm 发布事实。
- 结果：**X2 pass（机械校验）**——`1 份契约均带 version 与 compat_policy`。

### 28.3 T6：新增契约测试

- 新建 `pact-dsh/test/contract.test.js`（只加测试文件，未改生产代码，复用既有 `FakePactBackend`／`WasmPactBackend` 与 `test/fixtures` 桩）。
- 4 个用例：
  1. `PUBLISHED_SURFACE` 七方法（`enabled/gates/status/seed/produce/consume/close`）在两个实现上均保留，且只允许新增可选方法（「只增不删／旧面保留」断言）；
  2. Fake 后端全契约调用与结果形状；
  3. Fake 后端错误码（`InvalidKey`／`InvalidRequest`／`Disabled`／`DuplicateToken`／`UnknownToken`／`IdempotencyConflict`／`BackendUnavailable`）；
  4. Wasm 后端七调用透传与错误码保留。
- 白板 `contract_tests` 由显式空集改为登记该文件，`in_ci: true`（`ci.yml` 的 `npm test` 会执行）。
- `npm test`：**61 tests / 61 pass / 0 fail**（新增 4 项）。
- 结果：**T6 pass（机械校验）**——`1 份已发布契约的契约测试均在 CI 执行`。

### 28.4 G3：回滚与风格符合性

- 采纳默认方案：**发补丁版回退为主＋对缺陷版 `deprecate`**（已发布版本不可真正撤回，同号不可重发）。
- `deploy_strategy[0].rollback` 写明确机制；`compatible_with_style: true`；新增 `style_conformance` 5 条，逐条对上 `ADR-DP1-STYLE` 约束：
  1. STY-001 同步请求-响应（pre-step/pre-tool 内同步 await，无队列）；
  2. 不注册 `AgentFactory`（factory 归被覆盖的 `agent-loop` 行）；
  3. 仅按 `id` 覆盖 `cordis.patch.yml` 行（禁用原行＋插入 `pact-agent-loop`／`dsh-pact-observe`）；
  4. 不新增故障域（进程内 Fake 默认；wasm 本地惰性导入）；
  5. 单可部署单元（`release.yml` 一次 tag 产出单个单元）。
- 结果：**G3 pass（机械校验）**——`1 条部署策略均含回滚且风格兼容判定为真`。

### 28.5 实跑分布

| 项 | 结果 |
|---|---|
| `runner.py` | hard=39 executed=39 blocks=14 **pass=39 fail=0 escalate=0 vacuous=9** |
| X2／X5／T6／G3 | 全部 **pass（机械校验）** |
| `npm test`（pact-dsh） | 61/61 |
| 10.2.5 | **6/6**，v1.14.0（真实分布 pass 39 / fail 0 / escalate 0 / vacuous 9） |

**39 条 pass 的构成（不得只报总数）**：29 条为机械校验；**1 条为人工核结论（W1）**；**9 条为 vacuous（空真，pass＋vacuous: true）**。escalate 与 fail 均已清零。

### 28.6 提交范围

- `skills` 仓一个 commit：检查器（`common.py`／`v.py`／`w.py`／`g.py`／`x.py`）、`guard_registry.yaml`、白板、10.2.5、artifact、run-log、adjudication、两份草案（契约策略、回滚）。
- `pact-dsh` 仓一个 commit：`adr/ADR-0002-CT-PACT-BACKEND-01.md`、`test/contract.test.js`、`test/index.test.js`、`test/loop-entry.test.js`、`test/fixtures/agent-loop-stub.mjs`、`README.md`（契约兼容策略节与测试计数）。未改生产代码。
- 两仓均未 `git add -A`、均未推送。

---

## 29. 启动编译就绪度核对（2026-11-14）：停点重判与 C4/C5/C6/C7 现状

目的：判据闭合（v1.14.0）后，核对"正式路径停在 A-2／A-3、试点路径停在 C4／C6"是否仍成立，并推进不需要人类裁定的部分。

### 29.1 停点一（A-2／A-3）：已失效

仓库内可查到的 A-2／A-3 即 `escalate-adjudication-20261113.md` 批 A 的两项：

| 项 | 内容 | 现状 |
|---|---|---|
| A-2 | T4（单元有非空测试集） | v1.13.0 转 **pass**（新增 `test/index.test.js`、`test/loop-entry.test.js`） |
| A-3 | X2／X5（契约版本与兼容策略、已发布契约的 ADR） | v1.14.0 转 **pass**（`ADR-0002-CT-PACT-BACKEND-01` 经人类批准迁入、`compat_policy` 登记） |

→ 该停点不再成立。若上游指的是另一份 A-x 清单，请指明文件，本记录只对仓库内可查到的 A 批负责。

### 29.2 停点二（C4／C6）：C4 成立，C6 仅剩一条 escalate

以只读方式独立重算（不复用 `check-card.py` 的聚合结果）：

| 判据 | 核验方式 | 结果 |
|---|---|---|
| C4（每条硬性质至少一张卡认领） | 18 张卡的 `discipline_checks` 并集 vs `hard-properties.snapshot.json` 的 39 条 | **39/39，无未认领** |
| C5（引用闭合） | 33 个 `outputs.predicate_writes` 谓词集 vs 各卡 `inputs.upstream_predicates` | **0 条悬空引用** |
| C6-F1（锚定命中） | `fidelity-all.json` | pass（8 张实质卡 S0–S6 全锚定；10 张躯干卡按"无步骤，F1–F3 不适用"跳过） |
| C6-F3（硬性质覆盖） | 同上 | pass 39/39 |
| C6-F2（引用闭合） | 同上 | **escalate：`selection_context`，8 张实质卡同因** |
| C6-E4 | 卡片 `artifact_version` vs 产物标签 | match（`pilot-20261112.9`） |

`selection_context` 的根因（已核到行）：母本 L328／L333／L440 按白板谓词使用，但 0.18.6 机器层谓词块（L411–415）未登记；`registry/predicate_vocabulary.yaml` 亦无；而 `编译规范.md` L90 又把 `selection_context` 举为机器层谓词示例。属**登记遗漏**，不是语义争议。

处置的两条硬约束：
- `编译规范.md` §6.5：escalate 批量**不阻塞发布**，但清单须随产物发布；
- C6 判定谓词要求 `fidelity_verdict = pass`，故 C6 不能记 pass；补登记是母本改动（0.7 要求谓词集语义变更递增 MINOR），**须人类裁定**。

→ 本轮起草 [`R2提案-selection_context-谓词登记-20261114.md`](../../R2提案-selection_context-谓词登记-20261114.md)（`R2-PRED-SC-01`，甲类，未批准、未自批），含 A／B／C 三方案、代价与建议默认 A。

### 29.3 C7：未执行，且前置未齐

| C7 前置 | 现状 |
|---|---|
| 版本齐一（E4） | 成立（`.9`） |
| `fidelity_verdict = pass` | **不成立**（F2 escalate） |
| 覆盖率报告（锚定缺口／软性质未覆盖／存疑来源三清单随产物发布） | **缺**——仓内无该报告 |

→ 不能进 C7；即使 F2 转 pass，仍需先出覆盖率报告。

### 29.4 正式路径的真实卡点（结论）

不是 A-2／A-3，而是两件：

1. **10 个 kind 的实质卡未编译**：`G-TRUNK-CFG/CRD/CSL/DFL/DPS/OWN/RLP/SCH/SRC/STP` 均为 `gen_cards.py` 机械生成的骨架（无 `steps`、无 `discipline_checks`、无 FVR，注释写"语义对应待后续批次按 0.18.4 精化"）。正式编译对这 10 个 kind 只能进 `registry_refs`，F1–F3 一律不适用。
2. **`selection_context` 登记**（见 29.2）——所有方法选型类决策的公共前置。

### 29.5 本轮推进与未推进

- 推进：C4／C5 独立重算落记录；C6 escalate 根因定位到母本行号；起草 `R2-PRED-SC-01`；量化躯干卡缺口（10/18）。
- 未推进（需人类）：`selection_context` 三选一（建议 A）；10 个躯干 kind 的精化批次范围与顺序；C7 覆盖率报告的口径（三清单各自的数据源）。

### 29.6 待人类裁定（选项＋后果＋建议默认）

| 编号 | 问题 | 选项 | 后果 | 建议默认 |
|---|---|---|---|---|
| H-1 | `selection_context` 如何处置 | A 母本 0.18.6 补登记 + `pv-1.1`；B 卡片改写；C 维持 escalate | A：F2 转 pass、C6 可闭合，代价是 `pattern_version` 基线整体切换；B：触碰 §1.4(4) 禁令；C：C6 不闭合、缺口在正式编译放大 | **A** |
| H-2 | 10 个躯干 kind 是否启动精化 | 全量／按依赖序分批／暂不启动 | 精化后才谈得上正式编译全量卡片集；分批可先打通一个方面 | **按依赖序分批**（先 DFL／STP：其谓词已被实质卡 `upstream_predicates` 引用，其余 8 个目前无下游消费者） |
| H-3 | C7 覆盖率报告数据源 | 复用 `registry/reports/` 既有清单／新建专用三清单 | 决定 C7 何时可执行；不影响 C6 | **复用既有清单，缺项单列** |

---

## 30. 第十五轮（2026-11-14）：`selection_context` 补登记、C6 闭合、DFL／STP 精化

人类批准 H-1（方案 A）、H-2（先做 DFL 与 STP）、H-3（复用既有清单）。

### 30.1 母本改动（只动 0.18.6 与 0.7 声明值）

| 项 | 改前 | 改后 |
|---|---|---|
| 总行数 | 4,811 | **4,811（不变）** |
| sha256 | `c0bb9879b65c…c17c4510` | `469d64c023a8…0cb3f8f3` |
| 0.18.6 谓词块 | 4 条（`selection_procedure`／`step_log`／`exclusion_record`／`verdict_table`） | 5 条（+`selection_context(DP, F, C)`） |
| 0.7 声明值 | `pattern_version: pv-1.0` | `pattern_version: pv-1.1` |

- 补登记方式：占用 0.18.6 块内原空行（原 416 行），**行内追加、不新增行**，因此 416 行之后的所有行号不位移。
- 2,939 条冻结锚未重冻，`anchor_index.py` 复跑：**F-9 漂移核对 986 对，drift = 0**；F-1～F-8、F-10 全部 pass。
- 首轮曾因在 `predicate_vocabulary` 注释里新增 `@m:0.18.6#code-5` 引用触发 F-10 fail（新增引用未声明），已改为不带锚引用的文字描述，复跑全过。

### 30.2 判据一（`check_pattern_version.py`）

- PV-0（块发现 14／行 134）、PV-1（单一来源）、PV-1b（全文仅一处现行值）、PV-2（白板一致 `pv-1.1`）、PV-3（`pv-1.1` 基线已冻结）**全 pass**。
- **必须登记的异常**：0.18.6 不在检查器自动发现的 14 块内（它没有 `**机器层谓词**` 标记行，而是 `####` 标题＋围栏），`registry/DATA-SPEC.md` D1.4 的权威清单是 **17 块**。因此 `pv-1.1` 的 aggregate 与 `pv-1.0` **完全相同**（`0753e743d6f0…`）。版本递增依 0.7 语义成立，但块指纹兜底看不见本次改动。**是否把检查器扩到 17 块需人裁**（会影响全部历史指纹，必须重冻）。

### 30.3 C6：由 escalate 转 pass

`check-card.py --all`：`cards=18  F1=pass  F2=pass  F3(full)=pass (39/39)  F3(scoped)=pass  E4 match=True  fail_count=0`。
`selection_context` 已入 `predicate_vocabulary`（`registry_version` 1.1.0，arity 3），F2 的 R2 不再命中。**C6 闭合**。

### 30.4 全量分布

`hard=39 executed=39 blocks=14 pass=39 fail=0 escalate=0 vacuous=9`；E7 pass（4 条编译规程变更均经人类批准，哈希链连续且末条＝现行母本哈希）。构成仍为 29 机械／1 人工核（W1）／9 空真。

### 30.5 H-2：DFL／STP 精化

- 两张卡由躯干骨架升为 **0.2.0**：补齐 0.18.2 S0–S6 七个步骤（动作逐字取自母本）、`trigger`、`inputs`、`source_anchors`、失败分支；保留原躯干卡的谓词分配（DFL：`data_flow`／`data_lineage`；STP：`interaction_flow`／`orchestrator`／`saga`／`step_class`／`compensation`／`timeout_budget`／`quality_impact_card`）。
- 依赖序：DFL 上游 `G-TRUNK-CSL`；STP 上游 `G-CAND-03`（与 artifact DAG 一致）。
- 变体口径：0.18.1 把 DFL／STP 列入「尚未登记 0.18.4 变体」的 5 类（另外 3 类为 SCH／CFG／RLP），须按 0.18.8 补登记；本卡按 0.17.3「暂按通用 S0–S6 执行」，卡内 `variant_note` 已写明。
- 不精化的 8 个 kind 及理由：CSL／OWN 与 DFL 同属方面 4、SCH／RLP 与 STP 同属方面 5，变体未登记且当前无下游消费者；CFG／CRD／DPS／SRC 属方面 7／3 的注册类目，其价值链尚未在本切片打通。动手前先等 DFL／STP 的编译结果验证通用变体口径。
- **遗留同步项**：`registry/scripts/gen_cards.py` 的 `CARDS` 表仍把 DFL／STP 标为 `trunk`；若重跑生成器会覆盖本版卡。未改生成器（避免波及其余 16 张卡），登记为待办。

### 30.6 H-3：C7 覆盖率报告的数据源核对

| 清单 | 既有数据源 | 能否支撑 |
|---|---|---|
| 锚定缺口清单 | `registry/anchor_index/`（`resolvability.csv`／`drift.csv`／`assertions.csv`） | **能**（本轮 F-9 986 对、缺口 0） |
| 软性质未覆盖清单 | 无软性质登记表；`fvr_registry.yaml` 只登记 39 条硬性质 | **不能**——缺分母 |
| 存疑来源清单 | `registry/method_registry.yaml` 的 `source_status`／`verified`、`profiles.yaml` 的 `provenance.source_class`（hybrid／`[自定]`） | **部分能**——字段在，但无聚合表 |

结论：C7 的覆盖率报告**不新建清单**，但三清单里只有锚定缺口可直接生成；软性质缺分母，存疑来源需一次性聚合。两者都要先定口径，列入待裁项。

### 30.7 本轮改动文件（未提交）

母本、`registry/predicate_vocabulary.yaml`、`registry/pattern_version_baseline.yaml`、`registry/compilation_regime_changes.yaml`、`registry/anchor_index/*`（复跑产物）、`R2提案-selection_context-谓词登记-20261114.md`、`artifact.yaml`、`10.2.5-verdict-pact-dsh.yaml`、`whiteboard-pact-dsh.yaml`、`fidelity-all.json`、两张 DFL／STP 卡、本日志。

## 31. D 批：pv-1.1 指纹盲区修复、生成器防覆盖、四个 kind 精化、C7 两项口径（2026-11-14）

人类批准 D1–D4（2026-11-14，`user`）；本轮不提交。

### 31.1 D1：判据一检查器扩到 17 块并重冻基线

**根因**：`check_pattern_version.py` 原 `discover_blocks()` 只认 `**机器层谓词**` 标记行，发现 14 块；0.18.6／0.22.4／0.23.5 仅以 `####` 标题＋围栏书写，未入指纹，故 pv-1.1 的 aggregate 曾与 pv-1.0 相同（`0753e743d6f0…`）。

**改法**：块清单改从 `registry/DATA-SPEC.md` D1.4 表格读取（唯一权威，脚本不写死数量）；对每个块号定位节标题，取该节**首个围栏代码块**，按母本文档顺序聚合。`--freeze` 新增 `--note`（记录重冻原因／批准依据）。`registry/checks/common.py::predicate_blocks()` 改为复用同一发现实现，消除「判据一 17 块／runner 14 块」两套口径。

**重冻前后**：

| 项 | 重冻前 | 重冻后 |
|---|---|---|
| 块数 | 14 | **17** |
| aggregate | `0753e743d6f0…` | **`f329ce90ad77dc2249bd467b47ffee9e12ddcf43d2969e59c100662383b44c4c`** |

新增 3 块（D1.4 中原本就有、旧规则漏发现）：

| 块 | 母本标题行 | 块内构成 | 块指纹（前 12） |
|---|---|---|---|
| 0.18.6 | @409 | 5 条谓词声明（含 H-1 新增 `selection_context`）＋6 条 M 性质（M10–M15） | `f245b957638a…` |
| 0.22.4 | @4046 | 7 条谓词声明＋3 条 M 性质（M31–M33） | `81d7e021e749…` |
| 0.23.5 | @4267 | 3 条谓词声明＋2 条 M 性质（M34–M35） | `713fde55d5e5…` |

**分离结论**：pv-1.1 的 aggregate 已与 pv-1.0 不同（`f329ce90…` ≠ `0753e743…`），盲区消除。**但须注明不可直接同比**：pv-1.0 条目是旧发现口径（14 块）下的历史记录，其数值无法在现行口径下重算（需历史母本）；已在基线 `pv-1.0.note` 写明「历史记录，勿按现行口径重算」。

**口径提示（不擅自改）**：新增 3 块的围栏内同时含 M 性质条款，故块指纹覆盖这些性质行（比只盖谓词声明更严）；`predicate_lines` 因此计 11／10／5 行。另发现 D1.4 表的「声明名数」已滞后：0.18.6 记 4（H-1 后实为 5）、0.22.4 记 4（实为 7）、合计「142 调用／141 名」亦为旧值——已按人类指令在 §31.6 逐块实算校正。

**复跑**：判据一 PV-0/PV-1/PV-1b/PV-2/PV-3 全 pass（17 块，aggregate `f329ce90…`）；锚索引 F-1～F-10 全 pass，F-9 986 对 **drift=0**；全量分布 `hard=39 executed=39 blocks=17 pass=39 fail=0 escalate=0 vacuous=9`。母本未再改动（4,811 行，sha256 `469d64c023a8…`）。

### 31.2 D2：生成器防覆盖

`gen_cards.py` 新增 `refined_card()`：生成前读回既有卡，`version ≥ 0.2.0` 或既有卡无法解析 → 打印 `skip` 并保留原文件；机械生成只负责 0.1.0 骨架卡。文档头同步写明该防覆盖口径。

**干跑验证**：对 18 张卡取 `sha256sum` 快照 → 重跑 `gen_cards.py` → 再取快照：**18/18 逐字节不变**；输出 `skip G-TRUNK-DFL`、`skip G-TRUNK-STP`、`skip G-TRUNK-CSL`、`skip G-TRUNK-OWN`、`skip G-TRUNK-SCH`、`skip G-TRUNK-RLP`（均 0.2.0），其余 12 张 0.1.0 重写后内容一致。

### 31.3 D3：CSL／OWN／SCH／RLP 精化

四张均由躯干骨架升 **0.2.0**，口径与 DFL／STP 完全一致：S0–S6 动作逐字取自 0.18.2；补 `trigger`／`inputs`／`source_anchors`／失败分支／`approval_route`；**保留原躯干卡谓词分配**；依赖序取 artifact DAG。

| 卡 | 变体口径 | 上游 | 种子锚 | 谓词写入（保留原分配） |
|---|---|---|---|---|
| G-TRUNK-CSL | 0.18.4 第 4 行为**已登记**变体：逐数据集合迭代、S6 恒为高影响、S5 前强制「业务语义论证」工件 | G-TRUNK-OWN | 4.2.3 | consistency_level／consistency_rationale／invariant |
| G-TRUNK-OWN | 同上（第 4 行）；单一所有者判据见 4.5（Y1） | G-TRUNK-SRC | 4.2.1 | dataset／owner／shared_write_exception／access_path／sensitivity |
| G-TRUNK-SCH | 0.18.1 未登记变体（待 0.18.8），按 0.17.3 暂按通用 S0–S6 | G-TRUNK-RLP | 5.2.4 | time_semantics |
| G-TRUNK-RLP | 同上；种子源 5.2.3 | G-TRUNK-DPS | 5.2.3 | idempotent／delivery_semantics／idempotency／flag／cleanup_filed／expiry_of |

**不动 CFG／CRD／DPS／SRC 的理由**：四者的价值链在本切片未打通——CFG 依赖 SCH 的部署/调度决策产物、CRD 依赖 CFG、DPS 依赖方面 8/9 的质量与可观测产出、SRC 依赖目标仓的 source registry 实体（本切片只有试点数据）；且它们无自有 0.18.4 变体或变体未登记。先行精化会把「未消费的上游谓词」写成硬依赖，制造假 DAG。登记为后续批次。

`check-card.py --all`：`cards=18 F1=pass F2=pass F3(full)=pass (39/39) F3(scoped)=pass E4 match=True fail_count=0`。

### 31.4 D4：C7 两项口径

**软性质（有条款，建分母）**：母本围栏性质块内以 `—— 软` 标注者构成分母，来源＝母本条款本身；`—— 条件硬`／`—— 升级型` 不计入（前者是硬性质的条件形态，后者按失败升级处理）。

- 分母 **16** 条：M13、M21、M26、W5、W6、X4、X7、Y4、Y7、Z5、Q6、Q7、T5、T7、G9、M5。
- 覆盖 **0** 条（无任何软性质被 FVR 或检查器以 property_id 绑定）→ **未覆盖 16** 条。不是「无可登记分母」，也不是空真。

**存疑来源（聚合脚本，不建人工清单）**：新增 pilot 工具 `c7-coverage.py`，从注册面自动聚合，产出 `c7-coverage-report.yaml`：

| 注册面 | 条目 | `source_status` | 未核验指针 | 非母本来源（external） | source_class 分布 |
|---|---|---|---|---|---|
| method_registry | 138 | **字段不存在（absent）** | **0** | **34** | mother-row 73／mother-clause 29／external 34／mother-definition 2 |
| profiles | 18 | **字段不存在（absent）** | 0 | 0 | mother-clause 18 |

`source_status` 在现 schema 中不存在，报告如实记 `absent`，未臆造字段（人类所说的该字段由 `verified`＋`source_class` 替代承担）。34 条 external 条目为存疑来源清单主体（STY-008/009/012/016/020/023、OWN-003、CSL-004/005、CRD-001/002/005/006、DEC-001/005/006、CTR-002/004/008/009、STP-003/004、DFL-001、RLP-004/005/006/007、SCH-002、CFG-003、DPS-001～005）。

C7 三清单数据源现已齐备：锚定缺口＝`anchor_index`（本轮 0 缺口）、软性质未覆盖＝16、存疑来源＝34。C7 本身（发布与版本对齐）仍待正式发布动作，不自行宣告。

### 31.5 本轮改动文件（未提交）

母本（未改，仅确认 sha `469d64c0…`）、`registry/scripts/check_pattern_version.py`、`registry/checks/common.py`、`registry/pattern_version_baseline.yaml`、`registry/scripts/gen_cards.py`、`pilot/vertical-slice-20261112/{G-TRUNK-CSL,G-TRUNK-OWN,G-TRUNK-SCH,G-TRUNK-RLP}.card.yaml`、`pilot/vertical-slice-20261112/c7-coverage.py`（新）、`pilot/vertical-slice-20261112/c7-coverage-report.yaml`（新）、`artifact.yaml`、`10.2.5-verdict-pact-dsh.yaml`、`whiteboard-pact-dsh.yaml`、`fidelity-all.json`、`fvr-full-run-1.json`、`registry/compilation_regime_changes.yaml`、`registry/predicate_vocabulary.yaml`、`R2提案-selection_context-谓词登记-20261114.md`、本日志。（`registry/anchor_index/*` 复跑后无差异，未改动。）

### 31.6 D1.4 声明名数校正（提交前）

按现行母本（4,811 行）逐块实算，7 处不符已改，合计行同步：1.5 `8→9`（补 `node_role`）、2.5 `9→8`、5.5 `14→12`、6.5 `11→10`、7.5 `11→9`、0.18.6 `4→5`（`selection_context`）、0.22.4 `4→7`；合计 `142 调用／141 名 →` **`141 调用／140 名`**（`envelope` 仍于 1.5／6.5 两见）。行号列仍为 4,461 行版历史值，已在表头注明仅作定位参考。判据一复跑 aggregate 仍为 `f329ce90ad77…`（D1.4 只决定块清单，不参与指纹），全量仍 `39/0/0/9`。

## 32. C7 口径收口（2026-11-15）：三清单定位与判定谓词机核

本轮从 `3721343`（父 `4fff065`）干净状态接续；未重跑损坏修复、未重做已闭合判据、未推送。

### 32.1 起点核实

- HEAD `3721343c4911ad98622174251ef0539eaeedec6a`，父 `4fff065`；工作区 0 改动；无 `index.lock`；0 字节对象 0；`git fsck` 仅 3 条悬空 commit（无错误）；领先 `origin/main` 11 个提交、未推送。
- 母本 4,811 行、sha256 `469d64c0…`；判据一 17 块、aggregate `f329ce90ad77…`，PV-0～PV-3 全 pass。
- 全量 `hard=39 executed=39 blocks=17 pass=39 fail=0 escalate=0 vacuous=9`；`check-card.py --all`：`cards=18 F1=pass F2=pass F3(full)=pass 39/39 E4 match=True fail_count=0`。

### 32.2 C7 判定谓词（原文口径，不本地改写）

- `编译规范.md` §5.1 C7：判定谓词 = **`version_consistent ∧ fidelity_verdict = pass`**；三清单（锚定缺口／软性质未覆盖／存疑来源）**随产物发布**，不是发布门槛。
- §5.1 C2：锚定覆盖率维度**唯一**发布阈值 = 悬空引用类缺口（R2-B）= 0；其余锚定缺口不阻塞。
- 故「16 条软性质未覆盖」「34 条 external 来源」**非空也不阻塞 C7**；但也不能据此写成「已覆盖／已核验」。

### 32.3 两项未闭合口径的收口

**（1）软性质未覆盖 16——口径闭合，决策待裁**

- 分母规则按母本条款机核：`—— 软` 命中 **16** 条（M13、M21、M26、W5、W6、X4、X7、Y4、Y7、Z5、Q6、Q7、T5、T7、G9、M5）。
- 排除项复核：`—— 条件硬` 3 条（W3、X3、Z4）＋ `—— 升级型` 1 条（Z7），不计入分母；T5 标注「软/条件升级」按当前软态计入。
- 覆盖 **0**（FVR 注册面与 9 组检查器均未以 property_id 绑定）。
- 依 `编译规范.md` 3.3 映射表，软性质「覆盖为可选，未覆盖登记为覆盖率缺口（非阻塞）」→ 16 条作为已知缺口随报告发布。是否将其升为机械检查，属待裁项 B。

**（2）存疑来源 34——口径闭合为「出处构成清单」，缺陷 0**

新增强化聚合（`c7-coverage.py`）后机核：

| 注册面 | 指针总数 | verified | 未核验 | bib_id 去重 | 可解析 | external 类 |
|---|---|---|---|---|---|---|
| method_registry | 1,365 | 1,365 | **0** | 43 | **43/43**（母本书目 1–81） | 34 |
| profiles | 79 | 79 | **0** | 0 | — | 0 |

- 34 条 external 全部 `origin=hybrid`、全部指针 `verified: true`、bib_id 全部解析；它们是**出处构成**（母本条款 + 外部书目混合），不是 `编译规范.md` 4.5 所说的 `unverified_source` 缺陷。
- 结论：**存疑来源缺陷 = 0**；34 条仅作出处透明化列出，不再计为「未核验来源」。
- 限制保留：`verified: true` 是注册面自报字段；独立复核依据为《指针核对报告.md》（书目 1–80 闭合、悬空 0）与《参考资料缺口核对报告.md》（内容级核对），均为 2026-09 历史快照，本轮**未重做**内容级核对。是否要求独立复核，属待裁项 C。

### 32.4 C7 判定谓词机核结果（新发现：版本对齐未成立）

`c7-coverage-report.yaml` 新增 `c7_predicate_check`，逐项机核：

| 谓词分量 | 结果 | 依据 |
|---|---|---|
| `fidelity_verdict = pass` | **true** | `fidelity-all.json`：F1 pass、F2 pass、F3(full) 39/39 pass |
| `version_consistent` | **false** | `artifact.version.framework_version = sha256:c0bb9879…`（H-1 母本改动前），现行母本 `sha256:469d64c0…`；`registry_version` 两侧均 1.1.0，一致 |
| `predicate_satisfied` | **false** | 合取失效 |

- 按母本 0.23.9 `SM-CA-TRANS`，framework 变更应触发 **CA-03 `valid → stale`**；C7 失败分支要求重编译（以编译完成时刻的最新版本为准）。
- 重编译的连带面：`artifact_seq` 9→10、label `pilot-20261112.10`、18 张卡 `artifact_version` 同步、重跑 F1–F3 与 E4、更新 `10.2.5` 判据三证据——这会改动已闭合判据的证据面，故**本轮不自行执行**（延续 §31.4「C7 不自行宣告」）。
- 产物清单中未改 `version` 字段，只在 `artifact.yaml` 加注记 + `coverage_report` 指针（注记写明「按 CA-03 应记 stale」）。

### 32.5 待裁项（不自批）

| 编号 | 问题 | 选项 | 后果 | 建议默认 |
|---|---|---|---|---|
| C7-A | 版本对齐：framework_version 滞后于 H-1 后的母本 | ① 重编译到 `.10`；② 保持 `.9` 并记 `stale` 不发布；③ 其他对齐口径 | ① 恢复 `version_consistent`，但改 18 卡与判据三证据；② C7 判定谓词不成立、不能发布 | **①**（C7 失败分支的规定动作） |
| C7-B | 16 条软性质是否升机械检查 | ① 维持非阻塞缺口；② 逐条接检查器 | ① 与 3.3「软性质覆盖为可选」一致；② 需新增检查器与判定口径 | **①** |
| C7-C | 34 条 external 是否要求独立复核 | ① 接受为出处构成清单；② 要求内容级复核 | ① 依赖注册面自报 `verified`；② 需重做书目核对 | **①**，并把 `verified` 的独立复核依据标注为历史快照 |
| C7-D | W1 人工核升级判据 | 先由人类定义「已声明接口」判据，再机械核未声明跨模块访问 | 未定义前 W1 只能保持人工核结论 | 未定义 |
| C7-E | 编译规范 2.1 记 bib 范围 1–80，母本书目已至 81（2026-11-07 跨方面增补） | 修订编译规范 / 维持现状并注记 | 编译规范属人类修订权（§1.6），Agent 不自改 | 注记后由人类决定 |

### 32.6 本轮改动文件（未提交）

`pilot/vertical-slice-20261112/c7-coverage.py`（增强：C7 谓词机核、bib_id 解析、external 与未核验分离）、`pilot/vertical-slice-20261112/c7-coverage-report.yaml`（重建）、`pilot/vertical-slice-20261112/artifact.yaml`（`coverage_report` 指针＋版本对齐注记；未改 `version` 字段）、`pilot/vertical-slice-20261112/escalate-adjudication-20261113.md`（追加 §15 收尾）、本日志；`fidelity-all.json` 复跑无差异；`fvr-full-run-1.json` 复跑仅 `generated_at` 差异（`18:24:44 → 10:38:28`），已还原，结论不变。母本未改（4,811 行、`469d64c0…`），未推送。

## 33. C7-A 重编译执行（2026-11-15，人类批准）

人类逐项裁定：C7-A 取「重编译」；C7-B／C／D 按建议默认；C7-E 只加注记、不改条文。执行如下。

### 33.1 版本三元组对齐

| 字段 | 重编译前 | 重编译后 |
|---|---|---|
| `framework_version` | `sha256:c0bb9879…17c4510`（H-1 前） | `sha256:469d64c0…3f8f3`（现行母本） |
| `registry_version` | 1.1.0 | 1.1.0（未变） |
| `artifact_seq` | 9 | **10** |
| `label` / 卡 `artifact_version` | `pilot-20261112.9` | **`pilot-20261112.10`** |

### 33.2 18 张卡对齐的完整性核对

- 仅替换 `artifact_version` 行（文本级，未重排 YAML）；**18/18** 改毕。
- 以「剔除 `artifact_version` 行后的内容哈希」逐张比对：**内容变化 0 张**。
- 6 张 0.2.0 精化卡（DFL、STP、CSL、OWN、SCH、RLP）版本字段保持 `0.2.0`，正文原样。
- 未运行 `gen_cards.py`（其 `version ≥ 0.2.0` skip 保护未被触发，也未被绕过）。

### 33.3 C7 谓词与判定

- `version_consistent`：false → **true**；`fidelity_verdict = pass`（F1/F2/F3 39/39）；`predicate_satisfied = true`。
- 只做版本对齐；**未执行 SM-CA `compiling → valid` 与发布动作**（发布仍待人类另行决定）。
- `10.2.5-verdict-pact-dsh.yaml` 升 **v1.17.0**：`artifact` 改 `pilot-20261112.10`，判据三证据同步标签与 framework_version；判据一/二/四～六未变。

### 33.4 C7-B／C／D 默认落地与 C7-E 注记

- **C7-B**：16 条软性质维持非阻塞缺口（编译规范 3.3），不接检查器。
- **C7-C**：34 条 external 接受为出处构成清单；报告与 §15 注明 `verified` 的独立复核依据为 2026-09 历史快照。
- **C7-D**：W1 保持人工核结论；升级前置「已声明接口」判据未定义。
- **C7-E**：`编译规范.md` 2.1 `bib_id` 行加注记（母本书目 2026-11-07 增补 81 于 10.8，范围 1–80 存在漂移）；**范围值 1–80 未改**，修订权仍属人类。

### 33.5 复跑结果（重编译后）

- 判据一：`PV=pass`，`pv-1.1`，**17 块**，aggregate `f329ce90ad77…`（未变）。
- 全量：`hard=39 executed=39 blocks=17 pass=39 fail=0 escalate=0 vacuous=9`。
- 卡检：`cards=18 F1=pass F2=pass F3(full)=pass 39/39 E4 match=True fail_count=0`。
- 锚索引：ESC-01 与 F-1～F-10 全 pass，F-9 986 对，`failures: []`。
- 母本未改（4,811 行、`469d64c0…`）。

### 33.6 待提交文件

见本节之后 `git status`：上一轮 5 个文件（`c7-coverage.py`、`c7-coverage-report.yaml`、`artifact.yaml`、`escalate-adjudication-20261113.md`、`run-log.md`）＋本轮 18 张卡＋`10.2.5-verdict-pact-dsh.yaml`＋`编译规范.md`。不推送。
