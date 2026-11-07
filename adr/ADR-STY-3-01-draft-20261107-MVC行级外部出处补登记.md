# ADR 草案：`G-STY-3`／STY-012 的 MVC 行级外部出处补登记

| 项 | 值 |
|---|---|
| ADR 编号 | **`ADR-STY-3-01`** |
| 状态 | **draft（草案；2026-11-07 起草。待人类批准；本轮不落地、不改母本）** |
| 日期 | 2026-11-07 |
| 决策类目 | 参考书目扩充与条目出处补登记（0.12／0.13／0.22；不改条目字段语义、不改 0.17 系列条款） |
| 关联 | `G-STY-3`、SO-3、`STY-012`、`ADR-GAP-01` §5.5(5)／§3.1、`ADR-STY-FIM-01` §5.5(2)、书目 1／2／20／21／22、0.12、0.13、0.22 |
| 批准 | 人类责任方；Agent 仅备材料（0.10） |

## 1. 决策问题

`G-STY-3` 原文：「`STY-012`（MVC 及变体）在母本参考文献登记提取面中无合法来源」。其 `route` 已写明：**勘察补书目并按 0.12 定 `compile_usage` → 母本参考文献表扩充（高影响，走 R2/ADR）**。

本 ADR 裁决：用哪一条书目、以何种登记面，把 `1.2.1-MVC 及变体（MVP/MVVM）` 补到**行级外部出处**，并使 STY-012 从 `mother-row` 改为 `external`。

## 2. 事实基线

### 2.1 现登记面逐条排除（2026-11-07 复核）

| 书目 | 登记面逐字 | 锚点 | 是否覆盖 1.2.1-MVC 行 |
|---|---|---|---|
| 1 | 「1.2.1 抽象结构风格词汇表（分层、管道-过滤器、黑板、微内核、Broker）」 | @1871 | **否**：明列五项，不含 MVC |
| 2 | 「风格对比与架构决策方法」 | @1872 | **否**：表级面，未登记 MVC 章节 |
| 20 | 六边形／端口-适配器 | @1896 | 否 |
| 21 | Clean Architecture | @1897 | 否 |
| 22 | Onion Architecture | @1898 | 否 |

全库检索（`MVC`／`Model-View-Controller`／`Model View`／`MVP`／`MVVM`／`表现层`）**仅命中母本 @1347（1.2.1 表行本身）**；全部 x.7 书目行零命中。

**书目 2 的正文复核**：本地 EPUB（*Fundamentals of Software Architecture*, 2nd ed., 2025, ISBN 9781098175511）第 9 章仅顺带提及「layered components … inspired by Model-View-Controller separation」，**不给出 MVC 的过程定义、适用条件、包络与反模式**；若以其作行级出处，即 M6「以不承载该主张的文献充当出处」。故书目 2 不是可用的 ①。

### 2.2 候选文献与本地资源

| 候选 | 覆盖 | 本地资源 | 结论 |
|---|---|---|---|
| Martin Fowler, **"GUI Architectures"**, martinfowler.com, **2006-07-18**, https://martinfowler.com/eaaDev/uiArchs.html | 导言明确把 MVC 及其变体（Application Model／**MVP**／**Presentation Model**／**MVVM**）列为讨论对象；正文含 MVC、VisualWorks Application Model、MVP、Humble View 各节 | 无原始存档（在线在位，2026-11-07 抓取） | **主著录候选** |
| Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002（版权页 © 2003）, ISBN 0-321-12742-0 | 第 14 章 Web Presentation Patterns：MVC、Supervising Controller／Passive View（MVP 变体） | **在库**：resources/se PDF+EPUB（2026-09-15 内容核验） | **本地编译锚点**（补强 MVC／MVP 的书级权威） |
| Fowler, "Presentation Model"（2004） | Presentation Model／MVVM 前身 | 无 | 后备增补（见 §8） |

> **可信度风险（须在批准时明示）**：GUI Architectures 一文作者自述为 draft form，并声明「不要把我的描述当作权威」。本 ADR 的处理是：**该文只用于模式谱系与结构区分**；MVC／MVP 的书级权威由本地 PoEAA 第 14 章承担；条目的 envelope／anti_patterns 仍以母本 1.2.1 表行为准，不把该文当唯一判据。若人类认为 draft 自述不足以作 `metadata_extraction` 主著录，则按 §8 回退为「PoEAA 主著录＋该文展开锚点」。

## 3. 决策 A：新增书目 81 并登记 1.2.1-MVC 行级提取面

### 3.1 完整著录（拟写入母本 10.8）

```
81. Martin Fowler. "GUI Architectures." martinfowler.com, 2006-07-18. https://martinfowler.com/eaaDev/uiArchs.html `[已核验（在线在位：2026-11-07 抓取；标题、日期、目录与正文一致；作者自述为 draft form、非权威描述——本条仅用于模式谱系与结构区分，不单独承载判定）]` **本地编译锚点**：Martin Fowler. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002（版权页 © 2003；ISBN 0-321-12742-0）（**本地资源**：resources/se PDF+EPUB，2026-09-15 内容核验；第 14 章 Web Presentation Patterns 含 Model View Controller／Supervising Controller／Passive View）。`compile_usage=metadata_extraction` → **1.2.1-MVC 及变体（MVP/MVVM）的行级登记面**：MVC＝表现与领域分离、以观察者事件同步表现状态；MVP＝Presenter 中介、View 被动（Humble View）；Presentation Model／MVVM＝表现状态外置为可测试模型。
```

### 3.2 编号 81 的依据

1. 0.12 @1867：「全文献按**全文连续唯一编号**登记」「新增条目一律追加于相应节末，编号不复用不重排（0.22 承诺一）」；该行现记「编号 28–80」。
2. 现最大编号 80 → 下一个连续唯一编号为 **81**；不复用、不重排。
3. `project.py` 的 `BIB_LINE_RE = ^(\d{1,3})\.\s` 接受 1–3 位编号，81 合法；书目解析要求该行落在含「参考文献」且不含「治理条款」的节内。

### 3.3 行级覆盖说明（为什么能覆盖 MVC／MVP／Presentation Model）

| 行内词项 | 该文对应内容 | 与 1.2.1 表行的对应 |
|---|---|---|
| MVC | 表现与领域分离；controller 处理输入、view 渲染、model 承载领域状态；以观察者事件同步表现状态 | 对应表行「表现-领域-交互三分，单向数据流」 |
| MVP | Presenter 承担表现逻辑、View 被动（Humble View） | 对应表行变体「MVP」 |
| Presentation Model／MVVM | 表现状态外置为可测试的 presentation model，view 仅绑定 | 对应表行变体「MVVM」 |

**限制**：该文导言列名 MVVM，但正文以「Presentation Model」论述；§8 要求在落地前**补抓全文并逐字核验 Presentation Model 节**，核验不成立则不落地。

### 3.4 母本位置、写法与 `@m` 位移

| 写法 | 具体动作 | 新增行 | 预计位移（母本目标锚点） | 跨插入点区间锚 | 0.12 影响 | 取舍 |
|---|---|---|---|---|---|---|
| **甲（推荐）** | 在 §10.7 末（@4228 空行后）新增 `### 10.8 增补参考文献（跨方面）` ＋ 空行 ＋ 条目 81；@11／@1867 仅**行内**补「81 见 10.8」 | **3 行** | **32 处（去重 14 token）整体 +3**；0 处跨点区间锚 | 0 | 需 ADR 明文例外：跨方面增补置于文献序列末位（编号单调） | 位移最小；编号文档顺序单调；§2.7「1–27」原句不动 |
| 乙（0.12 字面读法） | 在 §2.7 末（@1904 空行）插 1 行；@1867「1–27」改「1–27、81」 | **1 行** | **7,403 处（去重 827 token）整体 +1**；0 处跨点区间锚 | 0 | 字面符合「相应节末」 | 位移最大；文档顺序出现 81 在 28 之前，需另释「编号连续按登记时序」 |
| 丙（零插行） | 在既有书目行内追加 81 | 0 行 | 0 | 0 | 不适用 | **不可行**：`BIB_LINE_RE` 要求行首 `81. ` 且位于「参考文献」节内；内联 81 不被解析，`bib_id: 81` 反查失败。若改记宿主 `bib_id: 2`，宿主不承载 MVC 主张 → M6 违反 |

> 位移量以 2026-11-07 `anchor_index.py` 快照实测（`targets.csv`，目标＝母本，端点 ≥ 插入点）；冻结文件仅做快照复算，不重写历史。甲案另需重抽母本机械抽印本（总纲单行本）与锚点索引。

## 4. STY-012 的数据改动（批准后执行）

```yaml
provenance:
  origin: hybrid                    # 不变：表格骨架 + 人工转写
  source_class: external            # mother-row → external（1.2.1-MVC 行级外部登记面）
  source_pointers:
    - {source_type: row_id, value: "1.2.1-MVC 及变体（MVP/MVVM）", verified: true}
    - {source_type: clause_id, value: "1.2.1", verified: true}
    - {source_type: bib_id, value: "81", verified: true}
references:
  - bib_id: "81"
    support_claim: "MVC＝表现与领域分离＋经事件（观察者）同步表现状态；MVP＝Presenter 承担表现逻辑、View 被动（Humble View）；Presentation Model／MVVM＝表现状态外置为可测试模型；三者共同构成 1.2.1『MVC 及变体』行的外部文献支撑面"
    compile_usage: metadata_extraction
    trust_grade: "[已核验]"
```

- **版本**：建议维持 `1.0.0`。理由：0.17.2 未规定条目 semver 语义；本轮不改任何字段内容，仅补出处类别与引用；与上一批已关闭的 18 行（均未升版）同口径。若人类要求「出处变更即升版」，则记 `1.1.0`（minor），二者择一，ADR 批准时定。
- `G-STY-3` 关闭按 **①（补到行级）**，`closure.basis`＝「书目 81 行级覆盖 1.2.1-MVC 及变体」；`evidence`含书目 81 原文、PoEAA 第 14 章、以及 §2.1 的排除检索记录。**不按 ③ 关闭**。
- `SO-3` 同批关闭（其 scope 内 `G-STY-5` 已关闭，`G-STY-3` 为本轮最后一项）。

## 5. 对投影与抽印本的预期变化

| 产物 | 预期变化 |
|---|---|
| `registry/projections/STY.md` | STY-012 新增「参考文献：bib 81 …」行；其余字段与 seed 资格不变 |
| `registry/projections/索引.md` | 书目 81 行登记并与 STY-012 互链；open gap 3→2；open SO 4→3 |
| `registry/projections/勘察义务清单.md` | SO-3 移出 open；`G-STY-3` 转 closed |
| `registry/projections/自检报告.md` | `references` 64→65；`external` 33→34；`mother-row` 74→73；未分类仍 0；硬失败 0／软警告 0 |
| 母本机械抽印本＋锚点索引 | 按甲案：索引重抽；32 处（14 token）目标锚 +3；附录与冻结快照不变 |

## 6. 被否方案

| 方案 | 内容 | 否决理由 |
|---|---|---|
| B（FIM-1） | 把 @1347「表现-领域-交互三分，单向数据流」当定义面，STY-012 改 `mother-definition` | **F1 不成立**：该行是结构定义，不是「过程／判定规则」；FIM 原为元方法判据（`ADR-STY-FIM-01` §1／§6），扩到结构风格属解释面扩张；且不增加任何外部佐证，等于把公认外部模式改标为「框架内生」 |
| C（`ADR-GAP-01` ③a） | 维持 `mother-row`，以「在所登记书目范围内无行级出处」关闭 | **§5.5(5) 明文禁止**：存在尚未登记但可登记的行级书目时必须走 ①；本 ADR §2.2 已找到可用书目面，③ 会把「未扩充」洗成「无出处」。D2 限定措辞不能救此案 |

## 7. 批准前置（须人类逐项确认）

1. 同意 0.12 扩充：新增书目 81，`compile_usage=metadata_extraction`。
2. 同意放置写法（甲：新增 10.8 增补区；或乙：§2.7 末插行），并接受对应位移量。
3. 同意母本改动：@11／@1867 行内补 81 指向；按甲案新增 10.8 三行。
4. 同意 STY-012 数据改动与版本口径（保持 1.0.0 或升 1.1.0）。
5. 同意 `G-STY-3` 按 ① 关闭、`SO-3` 同批关闭。
6. 同意落地前完成全文核验（Presentation Model／MVVM 逐字）与本地/在线著录复核；核验不成立则不落地。

## 8. 风险与回退

- **draft 自述风险**：若人类不接受 GUI Architectures 作 `metadata_extraction` 主著录 → 回退为「81＝PoEAA（书级权威、本地在库）＋ GUI Architectures 作展开锚点」；若 MVVM 仍无着落，再增书目 82（Fowler, "Presentation Model", 2004）。编号、放置、位移不变。
- **全文未核实**：本轮抓取为节选，未逐字确认 Presentation Model 节；**落地前必须补抓全文并核验**，否则 `support_claim` 中的 MVVM 部分不得写入。
- **解析风险**：10.8 标题须含「参考文献」且不含「治理条款」，条目行须以 `81. ` 行首起；否则 `bib_id: 81` 解析失败、M6 报硬失败。
- **回退**：不批准则 `G-STY-3`／SO-3 维持 open，`STY-012` 维持 `mother-row`／`references: []`，母本零改动、零位移。

## 9. 本轮边界

- **零落地**：不改母本、不改台账、不改 `project.py`、不关闭 gap／SO。
- **零提交**：本草案与 INDEX 行单独成文，是否提交由人类批准时定。
- `G-PRJ-1`／`G-SRC-1` 不触碰。
