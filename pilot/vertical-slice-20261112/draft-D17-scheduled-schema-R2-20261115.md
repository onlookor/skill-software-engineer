# 草案 ③：D-17 `scheduled(rp)` schema —— O1 已采纳并落地

> 性质：O1（数据层 schema，不动母本）已于 2026-11-15 由人类裁定采纳，实例落盘 `registry/review_points.yaml`。
> 母本、谓词词表、`pattern_version` 均未改；`10.2.5-verdict` 的 `field_convention` 已指向新文件。

## 1 缺口的事实核对（含一处旧结论更正）

| 事实 | 现状 | 出处 |
|---|---|---|
| 机器层谓词 | `review_point(rp, kind ∈ 8.2.7五类, scheduled, records)`，**arity 4，无 `owner` 槽** | 母本 8.5 @2962 |
| 硬性质 | `T8: ∀ rp: scheduled(rp) ∧ records preserved` | 母本 8.5 @2986 |
| `review_point` 是否在册 | **在册**，arity 4 | `registry/predicate_vocabulary.yaml#L126` |
| `scheduled` 是否在册 | **在册**，arity 1，但形态是 `review_point` 的第 3 槽别名（`base_predicates: [review_point]`） | 同上 `#L290`、`#L452` |
| `records` 是否在册 | 同上，第 4 槽别名 | `#L453` |
| 评审点触发形态 | 四类：CI 每次提交／回归触发条件命中／发布节点／周期 | 母本 8.2.1 @2856 |
| 评审点集合 | 五类：设计评审、简记包抽查、材料性抽查、验证计划评审、例外/Waiver 评审 | 母本 8.2.7 @2907-2911 |
| 判据五要求 | 「评审点集合已排期**且有责任人**」 | 母本 10.2.5 @4569 |

**更正一条旧结论**：`10.2.5-verdict-pact-dsh.yaml#L153` 写「`scheduled` 不在谓词词表（`method_registry.yaml#L8959`）」。该行引的是 2026-10-11 的实测；`ADR-VGEX-01`（2026-11-07 批准）已把 `review_point` 入表，并把 `scheduled`／`records` 登记为槽别名。**准确表述是：`scheduled` 在册但无独立值域，schema 仍缺。** 本文件不修改该判定记录，更正建议列入待签（S-D17-4）。

## 2 缺口拆成四条

| 编号 | 缺口 | 后果 |
|---|---|---|
| G-1 | `review_point` 实例无字段 schema（`trigger_type`／`trigger`／`interval`／`owner`／`records` 的形态与必填性） | 每个部署自行约定，换人即漂移 |
| G-2 | `scheduled(rp)` 无真值条件（什么样的实例算「已排期」） | T8 只能靠人读，不能机械判 |
| G-3 | `review_point` arity 4 **没有 `owner` 槽**，而判据五要求责任人 | 「有责任人」在机器层不可表达 |
| G-4 | `records preserved` 无字段形态（空检算不算、首次未到期算不算） | 空检与欠账难以区分 |

## 3 三个选项

### O1｜数据层 schema，不动母本（推荐）

新建 `registry/review_points.yaml`（辅助注册表，沿用 `schedules.yaml`／`guard_registry.yaml` 的 `meta/entries` 惯例），义务锚点引 8.5／8.2.7／10.2.5-5，并把 D-17 登记为「部署级 schema 缺口」。

```yaml
meta:
  law_file: ../软件工程元框架成文法.md
  registry_version: {major: 1, minor: 0, patch: 0}
  obligation_anchor:
    source_type: clause_id
    value: "8.5"                       # review_point 第 3/4 槽
    quote: "review_point(rp, kind ∈ 8.2.7五类, scheduled, records)"
    verified: true
  schema_status: schema+instances
  instance_state: "pact-dsh 五点（RP-1…RP-5）"
entry_fields:
  - {name: rp, type: string, required: true}
  - {name: kind, type: "enum: 设计评审|简记包抽查|材料性抽查|验证计划评审|例外Waiver评审", required: true}
  - {name: trigger_type, type: "enum: 日期|周期|发布节点|按需+季度空检", required: true}
  - {name: trigger, type: "date|null", required: true, note: "发布节点形态为 null，由 fallback 日期兜底"}
  - {name: interval, type: "string|null", required: true, note: "周期/空检必填"}
  - {name: owner, type: string, required: true, note: "判据五『有责任人』的承载字段"}
  - {name: records, type: "string|null", required: true, note: "null=尚未执行；不得以空检代替记录"}
  - {name: status, type: "enum: pending|done|overdue", required: true}
```

真值条件（写在 schema 头，作为 `scheduled(rp)` 的部署级判读）：

```
scheduled(rp) ≜ ∃e: e.rp = rp ∧ e.trigger_type ∈ 四形态
              ∧ (e.trigger ≠ null ∨ e.fallback ≠ null)
              ∧ (e.trigger_type ∉ {周期, 按需+季度空检} ∨ e.interval ≠ null)
              ∧ e.owner ≠ null
```

- **成本**：新增 1 文件；`10.2.5-verdict` 的 `field_convention` 指向该文件（1 文件）；`artifact.yaml` 增 `registry_snapshot.review_points`（1 文件）；重编译 `.11`＋18 卡版本对齐＋C7 报告（约 21 文件）。**母本、锚索引、`pattern_version` 均不动。**
- **代价**：G-3 仍在机器层不可表达；`owner` 只在数据层可查。这是 O1 的诚实边界。

### O2｜母本 R2：扩 `review_point` arity 4→5，并定义 `scheduled` 值域

在母本 8.5 把谓词改为 `review_point(rp, kind, scheduled, records, owner)`，并在块内加 `scheduled(rp)` 的真值说明；同步 `predicate_vocabulary.yaml`。

- **成本链**：母本 sha 变（4,811 行可不变，但内容变）→ 锚索引重建（2,939 条、F-9 986 对 drift 必须 0）→ 8.5 块内容变 → `pattern_version` 聚合指纹变，需重冻 `pv-1.2` → 产物 `.11`＋18 卡＋FVR 证据＋10.2.5 判据一/五＋C7 报告＋白板。**≥25 文件，且需 R2 门槛与人类修订批准。**
- **收益**：G-3 在机器层可表达；T8 可完全机械判。
- **风险**：`pattern_version` 重冻牵连所有卡的版本一致性；锚索引重建若出现 drift，需先归零才能继续。

### O3｜维持现状，只登记债

- **成本**：0。
- **代价**：判据五的「有责任人」始终靠部署级约定；每次重编译都要重申；G-2 无法机械化。
- **不建议**：它把可消除的缺口留成长期债，而 O1 的成本只是版本对齐。

## 4 推荐

**O1**：用 1 个新文件 + 一次重编译换掉「无 schema」这一缺口，不动母本与冻结基线；G-3 的机器层缺口如实留在 O1 的边界声明里，不假装解决。若人类要求 `owner` 必须进机器层，再走 O2。

## 5 现有五点对 O1 schema 的适配核对（只读）

| rp | kind | trigger_type | trigger | interval | owner | 适配 |
|---|---|---|---|---|---|---|
| RP-1 | 设计评审 | 日期（追溯） | 2026-11-19 | null | user | 通过（`retroactive` 需加注记字段或写入 records） |
| RP-2 | 简记包抽查 | 周期 | 2026-12-31 | 每季度 | user | 通过 |
| RP-3 | 材料性抽查 | 周期 | 2026-12-31 | 每季度 | user | 通过 |
| RP-4 | 验证计划评审 | 发布节点 | null（`fallback: 2026-12-31`） | null | user | 通过（依赖 `fallback` 字段，schema 需补该字段） |
| RP-5 | 例外/Waiver 评审 | 按需+季度空检 | 2026-12-31 | 每季度 | user | 通过（空检记录需与 `records` 区分） |

> 结论：O1 schema 需补两个字段才能无损承接现状——`fallback`（RP-4）与 `retroactive`／`timing_status`（RP-1）。补进 O1 后 5/5 通过。此为草案修正，不涉及母本。

## 6 待签

| 编号 | 待签内容 | 授权方 | 备注 |
|---|---|---|---|
| S-D17-1 | 选项 O1／O2／O3（推荐 O1） | 人类责任方 | O2 才触母本 |
| S-D17-2 | 若选 O2：R2 提议＋母本修订批准 | 人类责任方 | 母本改动权 |
| S-D17-3 | O1 的登记落点（新文件 vs 并入现有注册表） | 人类责任方 | 影响 `--check` |
| S-D17-4 | 是否更正 `10.2.5-verdict#L153` 的旧结论（scheduled 已在册） | 人类责任方 | 判定记录文本，agent 不改 |
