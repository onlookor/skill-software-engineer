# 判据四方案：39 条硬性质全量认领路径

> 状态：**方案，未执行**。目标是 39/39（全量，非切片）。本方案不改母本、不改注册表条目语义；所有归属与判定口径中标「推断」者待人类裁定。
> 依据：母本 10.2.4（FVR schema）、10.2.5 判据四、E3（`∀ property(hard): ∃ fvr_entry ∧ wired ∧ first_full_run has evidence`）、T1；编译规范 6.2–6.5、8.2。
> 现状：F3 全量 5/39（G-CAND-01 的 `discipline_checks` 只有 M10/M11/M12/M14/M15）。

## 1. 39 条硬性质的实测构成

`check-card.py` 的 F3 口径＝母本行内标记正则 `^\s*([A-Z]\d+):.*(——|—)\s*硬`，实测 **39 条**：

| 系列 | 条数 | 性质 ID |
|---|---|---|
| M（总纲机制） | 16 | M1 M2 M3 M4 M8 M9 M10 M11 M12 M14 M15 M20 M22 M23 M24 M25 |
| E（方面 10） | 5 | E1 E2 E3 E5 E7 |
| W（方面 2） | 4 | W1 W2 W4 W7 |
| X（方面 3） | 4 | X1 X2 X5 X6 |
| V（方面 1） | 3 | V1 V2 V5 |
| T（方面 8） | 3 | T1 T4 T6 |
| G（方面 9） | 2 | G3 G7 |
| Q（方面 6） | 1 | Q1 |
| R（方面 7） | 1 | R8 |

Y（方面 4）、Z（方面 5）**无硬性质**——这是事实，不是排除；需在矩阵中显式登记「该方面硬性质数＝0」，避免被读成漏项。

## 2. 认领规则（谁写谓词，谁认领）

**主认领人 = 该硬性质所约束谓词的写者卡**（`outputs.predicate_writes` 的生产者）。依据：E3 的 `fvr_entry` 是「性质 × 检查程序」，若认领卡不写该谓词，检查程序无执行域。推断：同一谓词多写者时，取「首次建立该谓词的规程卡」为主认领，其余卡用 `upstream_cards` 引用，不重复认领。

按此规则的建议归属（**推断，待裁定项见 §5-1／5-7**）：

| 卡（kind） | 方面 | 认领硬性质 | 条数 |
|---|---|---|---|
| G-CAND-01（STY） | 1 | V1 V2 V5 ＋ M10 M11 M12 M14 M15 | 8 |
| G-CAND-02（DEC） | 2 | W1 W2 W4 W7 | 4 |
| G-CAND-03（CTR） | 3 | X1 X2 X5 X6 | 4 |
| G-CAND-04（QAT） | 6 | Q1 | 1 |
| G-CAND-05（GOV） | 7＋总纲 | R8 E7 M1 M2 M3 M4 M8 M9 M20 M22 M23 M24 M25 | 13 |
| G-CAND-06（VFM） | 8 | T1 T4 T6 | 3 |
| G-CAND-07（GRD） | 9 | G3 G7 | 2 |
| G-CAND-08（PRJ） | 10 | E1 E2 E3 E5 | 4 |
| **合计** | | | **39** |

覆盖 8 张卡、8 个 kind（STY/DEC/CTR/QAT/GOV/VFM/GRD/PRJ）；其余 10 个 kind（OWN/STP/CSL/DFL/CRD/RLP/SCH/CFG/DPS/SRC）不直接认领硬性质，但其选型卡仍需存在以闭合 `upstream_cards`（例如 CSL 卡是 STY 卡的上游）。

## 3. 卡片集怎么生成

三层，全部由母本＋注册表派生，不手写内容：

1. **卡骨架生成器**（新增 `registry/scripts/gen_cards.py`，或扩展 `project.py`）：对 18 个 kind 各生成一张卡骨架——`trigger` 取 0.18.2 决策点声明；`steps` 取 S0–S6 模板（逐字引 0.18.2）；`inputs/required_facts` 取 0.3 三类输入解包；`outputs.predicate_writes` 取该 kind 条目的 `constraints_imposed`／剖面字段；`registry_refs` 取注册表条目。
2. **性质绑定**：生成器按 §2 的归属表写入 `discipline_checks`（这是 F3 的计分字段），并同步生成该卡的 FVR 条目（§4）。
3. **人不写卡、只审卡**：生成物与母本逐字对应关系落 `run-log`，避免"手写 39 条"变成新的幻觉源。

## 4. FVR 接线怎么闭合

每条硬性质一行 FVR entry，五要素（10.2.4）＋可执行检查程序：

| 性质组 | 检查程序来源 | 现状 | 缺口 |
|---|---|---|---|
| M10–M15 | `check-card.py` F1/F2 已有 | 已接 | 无（可复用） |
| E2 | `project.py --check` F-11 | 已接（部分） | 只覆盖投影同源，非全称 |
| E3 | `check-card.py` F3 本身 | 自指 | 需在全量闭合后自洽 |
| E4/E5/E7 | 版本一致性／三值路由／规程变更审批 | 部分 | 三值路由检查器未独立成程序 |
| V1 V2 V5、W1 W2 W4 W7、X1 X2 X5 X6 | 需新增结构性检查器（依赖环、协议白名单、ADR 存在性、单一所有者、契约注册） | 未接 | **约 15 个检查器** |
| Q1、T1 T4 T6、G3 G7、R8、M1–M4/M8/M9/M20/M22–M25 | 多为注册表结构检查＋文档证据检查 | 未接 | **约 16 个检查器＋证据模板** |

**执行域**：已有 CI（`.github/workflows/ci.yml`）。接线完成的定义＝`fvr_entry.wired=true` 且 CI 能调用对应程序返回 `pass|fail|escalate` 之一并路由（E5）。

**首轮全量证据**：在单一 commit 上跑一次全量 FVR，产出 `pilot/<试跑>/fvr-full-run-<seq>.json`（含 39 行 verdict＋ci_run_id＋时间戳＋执行者），作为 `first_full_run evidence`。

## 5. 需要口径裁定的点（不自行决定）

| # | 裁定点 | 可选口径 | 影响 |
|---|---|---|---|
| 1 | 卡片集粒度 | (a) 18 kind 卡；(b) 8 方面卡；(c) 混合 10 卡 | 决定卡数、依赖图规模、`upstream_cards` 写法 |
| 2 | 「39 条」的权威来源 | (a) 以 F3 正则派生为权威；(b) 以母本人工清单为权威（需先修订该清单） | 若正则漏计（如 G3 的硬标记被截断），39 可能低估 |
| 3 | 框架元性质归属 | (a) 由目标系统卡认领（本方案）；(b) 另设「框架自治理卡」；(c) 部署级 FVR 集承载 | 决定 E3 的归属单元与卡 schema 是否要扩展 |
| 4 | 空真性质 | (a) 记 `pass`（空真成立）；(b) 记 `not_applicable` 并扩展三值；(c) 记 `escalate` | (b) 会触碰 E5 三值封闭，可能需母本解释 |
| 5 | 首轮全量 | (a) 单次运行覆盖 39；(b) 同 commit 分批执行后合并 | 决定证据工件形态与 CI 编排 |
| 6 | `upstream_cards` 闭合判据 | (a) DAG 无环＋卡存在；(b) 再加「每个 upstream_predicate 有写者」 | (b) 更严，需谓词→写者索引 |
| 7 | 跨方面认领 | (a) 允许（如 STY 认领 M10–M15）；(b) 严格按方面 | 决定 §2 归属表是否成立 |
| 8 | 检查器落点 | (a) 新建 `registry/checks/`；(b) 并入 `scripts/` | 影响 DATA-SPEC／CI／目录约定 |

## 6. 不建议的捷径（明确排除）

- 把 39 个 ID 直接塞进 `discipline_checks` 而不建 FVR entry／检查程序——这只骗过 F3 计分，违反 E3 的 `wired ∧ evidence`。
- 把判据四改成「切片够用」——口径收窄，已按人类要求排除。
