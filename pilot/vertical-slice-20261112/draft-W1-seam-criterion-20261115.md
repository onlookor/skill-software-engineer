# 草案 ②：W1「已声明接口」判据（候选 B 已批准并落地）

> 性质：判据已由人类于 2026-11-15 批准（候选 B＋边界＋固定观测项），检查器已落地于 `registry/checks/w.py`。
> 本轮不改母本、不改任何冻结基线；产物 `.11` 重编译另行执行。

## 1 条款与现状

- 母本 2.5（@1337）：`W1: ∀M: seam(M)` —— 可测试性硬约束（0.15 冻结项），硬。
- 母本 8.2.2：单元层覆盖「seam 可用性（W1/W2 的执行面）」。
- 当前实现 `registry/checks/w.py::w1`：读白板 `human_review` 中 `property=W1` 的记录，校验 `approver_kind=human`、`approved_by`、`conclusion`；**不做任何接缝机械核对**。
- 当前结论（`10.2.5-verdict-pact-dsh.yaml` 判据四）：W1 = 人工核 pass，覆盖 9 单元，「无未声明跨模块访问、无例外」。
- 因此 W1 是 39 条中**唯一**非机械的一条；升级前缺的不是代码，是「已声明接口」的定义。

## 2 判据候选（人类三选一）

| 候选 | 定义 | 机械可判 | 误报风险 | 现状基线 |
|---|---|---|---|---|
| **A** | 每个单元的跨单元访问**只经目标单元的静态导出**（ESM named/default export）；包外访问只经 `package.json` `exports` 入口 | 是 | 低（只拒绝「导入不存在的导出名」与「越界路径」） | 通过 |
| **B（推荐）** | A ＋ 每个单元**至少一个静态导出**（`seam(M)` 的「存在可测试接口」字面要求） | 是 | 低（纯副作用入口仍可 `export default`） | 通过 |
| **C** | A ＋ 运行时访问监测（拦截未声明的跨模块属性访问） | 部分（需运行时 hook） | 高（动态语言、原型链、反射） | 未实现 |

**推荐 B**：它把 W1 的「存在可测试接口」拆成两个可机械判定的合取项，不引入运行时依赖，也不改变母本语义。C 不建议：成本最高，且对 0.15 冻结项而言，静态面已足以覆盖「未声明跨模块访问」。

**A/B 的共同边界（需人类确认）**：

1. 只覆盖**静态 ESM**（`import ... from './x'`）；`import()`、`import * as`、CommonJS `require` 一律 **escalate**（不静默 pass）。
2. 判定对象是 `module_inventory` 的 9 个单元（`{id, path, role}`），**测试文件不参与**（测试替身另行按 8.2.2 登记；否则 9 个测试文件直连 `src/*` 会整批失败）。
3. 路径解析为相对路径规范化；目标不在 `module_inventory` → fail（越界访问）。
4. `package.json` `exports` 面为 `.`／`./loop`／`./locale/*.json`／`./icon` 四项；非 JS 入口（`locale/*.json`、`icon.svg`）不参与导入名判定。

## 3 判据形式化（候选 B）

```
seam(M) ≜ exports_static(M) ≠ ∅
        ∧ ∀(M1 → M2, n) ∈ static_import_edges: n ∈ exports_static(M2)
        ∧ ∀(M1 → M2) ∈ static_import_edges: path(M2) ∈ module_inventory

外部访问（包外消费者）：只允许经 package.json exports 声明的入口
```

`exports_static(M)` ＝ `export function|class|const|let|var` 声明名 ∪ `export { … }` 列名 ∪ `{default}`（当存在 `export default`）。

## 4 机械核设计（落地时才改 `w.py`）

- 输入：`domain_data(ctx,'module_inventory')`（已有）＋ 源码；不新增白板域。
- 路径：`ctx['root'] / unit['path']`，复用 `source_files(ctx)` 的读取能力。
- 判定：
  - 无 `module_inventory` → `escalate`（沿用现行 `NOTE`，非空真）；
  - 存在单元但源码不可读 → `escalate`；
  - 出现第 2 节边界外的导入形态 → `escalate` 并点名（不 pass）；
  - 任一边界违规 → `fail` 并列出 `{from, to, name}`；
  - 全部满足 → `pass`，证据附「N 单元 / E 边 / B 绑定 / 0 违规」。
- 移除对 `human_review` 的依赖；历史人工核记录保留为**历史证据**，不再作为 pass 依据。

## 5 只读预演（非判定）

口径：9 单元、静态相对导入、排除 `test/`。

| 指标 | 实测 |
|---|---|
| 单元数 | 9 |
| 文件级导入边 | **11** |
| 命名绑定数 | **15** |
| 违规（基线） | **0** |
| 注入反例：删除 `src/names.js` 的 `isPactPreset` 导出 | **2 条绑定失败**（`src/govern.js`、`src/loop.js`），检出正确 |

导出面实测：`index{apply}`、`loop{default}`、`config{PactConfigError,loadConfig,normalizeConfig}`、`govern{STOP_MESSAGE,createGovernor}`、`loop-core{createPactLoop}`、`names{NAME_RE,instanceFromSession,isPactPreset,isValidName,participantFor}`、`observer{FileSink,auditRecord,createObserver}`、`pact-backend{FakePactBackend,PactBackendError}`、`wasm-backend{createWasmBackend}`。

结论：候选 B 在现状代码上**无假阳性**，且注入反例可被检出。但**这不等于 W1 已升级**——判据未签，检查器未改。

## 6 升级的连带面（将来执行时的成本）

| 对象 | 变更 | 量级 |
|---|---|---|
| `registry/checks/w.py` | 重写 `w1()`；删除 `human_review` 依赖 | 1 文件，约 80–110 行 |
| FVR 证据 | W1 行由人工核改为机械核；证据字段改「9 单元 / 11 边 / 15 绑定 / 0 违规」 | 1–2 文件 |
| `10.2.5-verdict-pact-dsh.yaml` | 判据四分布：29 机械＋1 人工核＋9 空真 → **30 机械＋0 人工核＋9 空真** | 1 文件 |
| `artifact.yaml` | 检查器与证据变更 → 产物重编译，`artifact_seq` +1（`.11`），`recompile_map` 增行 | 1 文件 |
| 18 张卡 | `artifact_version` 对齐 `.11`（内容不得覆盖；沿用 0.2.0 保护） | 18 文件，仅版本字段 |
| C7 报告 | 复跑 `c7-coverage.py` | 2 文件 |
| 母本 / 锚索引 / `pattern_version` | **不动** | 0 |
| 合计 | 约 **23–25 文件**，无母本改动 | 低–中 |

## 7 批准与固定观测项

**2026-11-15 人类批准**：候选 B；边界按「只有静态相对路径的动态加载才 escalate，非字面量/非相对路径按外部注入排除」。

**固定观测项（人类附加条件）**：`excluded_dynamic_loads` 是 W1 证据的**固定字段**，每次复跑必须报出当前值，不得只写一次或省略。理由：该排除项等于一个可被滥用的豁免口子，数值上涨即说明有人用动态加载绕过依赖检查。

输出契约（`registry/checks/w.py::_w1_metrics`）：

```yaml
metrics:
  units: 9
  import_edges: 11
  bindings: 15
  violations: 0
  excluded_dynamic_loads: 1          # 每轮必报；null = 未能测量
  excluded_dynamic_load_units: ["wasm-backend"]
```

| 编号 | 内容 | 状态 |
|---|---|---|
| S-W1-1 | 判据选 B | 已批准（2026-11-15） |
| S-W1-2 | 边界四条 | 已批准（2026-11-15，动态加载边界按上述修订版） |
| S-W1-3 | 升级随下一次产物重编译（`.11`）执行 | **未执行**：检查器已生效，产物版本标签待 `.11` |
| S-W1-4 | `excluded_dynamic_loads` 固定观测字段 | 已写入检查器输出契约，当前值 **1** |
