# V1 分层草案（pact-dsh）

- 状态：**已批准并落地**（人类 `user`，2026-11-14，口径甲＝弱校验）。本文件作为批准记录保留，白板已登记。
- 依据仓库：`/home/user/projects/pact-dsh`（`dsh-plugin-pact` 0.1.2）
- 日期：2026-11-14
- 用法：勾选项即批准项；标「待人类拍」处已由人类拍定，保留原文作为审批记录。

> **局限（必须随 pass 一并引用）**：现行 V1 检查器只读字面 `dependency_rule` 层规则边，**不展开 `layer_of` 到单元边**。因此 V1 的 pass 仅表示「禁止层规则本身无环」，**不代表单元级依赖已核**。该检查已与 W4 打包为「将来升级为机械校验」项（见 run-log §23），升级前不得把此 pass 当作真校验通过。

---

## 1 仓库事实：9 个单元与 11 条内部 import 边

单元口径沿用 D-C：`index.js` 与 `loop.js` 各算独立入口单元。

### 1.1 单元清单（事实）

| 单元 id | 文件 | 行数 | 角色（据文件头注释） |
|---|---|---|---|
| `index` | `index.js` | 30 | DSH host 插件入口，注册 session/event 审计镜像（`index.js#L5-L10`） |
| `loop-entry` | `loop.js` | 38 | AgentLoop 工厂入口，按 `domain/instance` 分发 backend（`loop.js#L8-L38`） |
| `config` | `src/config.js` | 170 | 环境/文件配置归一化（`src/config.js#L40,L151`） |
| `govern` | `src/govern.js` | 169 | 治理器（门/令牌/终止检查） |
| `loop-core` | `src/loop.js` | 111 | `PactAgentLoop` 实现（`src/loop.js#L17-L21`） |
| `names` | `src/names.js` | 31 | 名称校验与实例键派生（无内部 import） |
| `observer` | `src/observer.js` | 75 | 审计记录归约与 JSONL sink（无内部 import） |
| `pact-backend` | `src/pact-backend.js` | 161 | backend 契约与内存实现（无内部 import） |
| `wasm-backend` | `src/wasm-backend.js` | 76 | WASM host 适配器（仅 import `pact-backend`） |

### 1.2 全部内部 import 边（事实，11 条）

| # | 文件:行 | from → to |
|---|---|---|
| 1 | `index.js:2` | `index` → `config`（`loadConfig`） |
| 2 | `index.js:3` | `index` → `observer`（`FileSink`, `createObserver`） |
| 3 | `loop.js:3` | `loop-entry` → `config`（`loadConfig`） |
| 4 | `loop.js:4` | `loop-entry` → `loop-core`（`createPactLoop`） |
| 5 | `loop.js:5` | `loop-entry` → `pact-backend`（`FakePactBackend`） |
| 6 | `loop.js:6` | `loop-entry` → `wasm-backend`（`createWasmBackend`） |
| 7 | `src/config.js:1` | `config` → `names`（`isValidName`） |
| 8 | `src/govern.js:1` | `govern` → `names`（`instanceFromSession`, `isPactPreset`, `participantFor`） |
| 9 | `src/loop.js:1` | `loop-core` → `govern`（`createGovernor`） |
| 10 | `src/loop.js:2` | `loop-core` → `names`（`instanceFromSession`, `isPactPreset`） |
| 11 | `src/wasm-backend.js:1` | `wasm-backend` → `pact-backend`（`PactBackendError`） |

**事实结论**：上述 11 条边构成有向无环图（无回指入口、无 `names`/`observer`/`pact-backend` 向外依赖）。

---

## 2 草案 A：层数与层名（设计选择，待人类拍）

建议 3 层：

- [x] **L0-entry（入口层）**：被宿主/工厂调用，可依赖 L1、L2。
- [x] **L1-core（核心层）**：PACT 语义与配置，只能依赖 L2。
- [x] **L2-foundation（基础层）**：无内部业务依赖，层内允许互相依赖。

层名本身是设计选择，可改（如 `entry/core/base`）。

## 3 草案 B：每个模块所属层（设计选择，待人类拍）

| 单元 | 提议层 | 判断依据 | 勾选 |
|---|---|---|---|
| `index` | L0-entry | 仅被 DSH 宿主调用；只向外 import（`index.js:2-3`） | - [x] |
| `loop-entry` | L0-entry | 导出工厂；只向外 import（`loop.js:3-6`） | - [x] |
| `config` | L1-core | 被两个入口依赖（边 1、3），自身只依赖 `names`（边 7） | - [x] |
| `govern` | L1-core | 只被 `loop-core` 依赖（边 9），自身只依赖 `names`（边 8） | - [x] |
| `loop-core` | L1-core | 被入口依赖（边 4），依赖 `govern`/`names`（边 9、10） | - [x] |
| `names` | L2-foundation | 被 `config`/`govern`/`loop-core` 依赖（边 7、8、10），自身无内部 import | - [x] |
| `observer` | L2-foundation | 只被 `index` 依赖（边 2），自身无内部 import | - [x] |
| `pact-backend` | L2-foundation | 被 `loop-entry`/`wasm-backend` 依赖（边 5、11），自身无内部 import | - [x] |
| `wasm-backend` | L2-foundation | 只依赖 `pact-backend`（边 11），被 `loop-entry` 依赖（边 6） | - [x] |

**注**：9 个单元全覆盖（含 `index`、`loop-entry`）。

## 4 草案 C：跨层允许/禁止方向（设计选择，待人类拍）

- [x] **允许**：L0 → L1、L0 → L2、L1 → L2、同层内互相依赖
- [x] **禁止**：L1 → L0、L2 → L0、L2 → L1

**事实核验**：现有 11 条边在上述方向上**违例 0 条**（边 1–11 均落在允许集内）。

## 5 草案 D：具体登记条目

### 5.1 `layer_of(component, L)`（9 条，每条勾选）

- [x] `layer_of(index, L0-entry)`
- [x] `layer_of(loop-entry, L0-entry)`
- [x] `layer_of(config, L1-core)`
- [x] `layer_of(govern, L1-core)`
- [x] `layer_of(loop-core, L1-core)`
- [x] `layer_of(names, L2-foundation)`
- [x] `layer_of(observer, L2-foundation)`
- [x] `layer_of(pact-backend, L2-foundation)`
- [x] `layer_of(wasm-backend, L2-foundation)`

依据：§3 的 import 关系；**层名与归属是设计选择**。

### 5.2 `dependency_rule(·,·,forbidden)`（3 条，每条勾选）

- [x] `dependency_rule(L1-core, L0-entry, forbidden)`
- [x] `dependency_rule(L2-foundation, L0-entry, forbidden)`
- [x] `dependency_rule(L2-foundation, L1-core, forbidden)`

依据：§4 的禁止方向。三边 `L1→L0`、`L2→L0`、`L2→L1` 构成 DAG，无环。

## 6 事实 vs 设计选择对照

| 内容 | 性质 |
|---|---|
| 9 个单元及文件位置 | 仓库事实 |
| 11 条 import 边及行号 | 仓库事实 |
| 现有依赖无环 | 仓库事实 |
| 现有边对提议规则违例 0 条 | 仓库事实（相对提议规则） |
| 3 层及层名 | 设计选择，待人类拍 |
| 9 个单元的层归属 | 设计选择，待人类拍 |
| 允许/禁止方向 | 设计选择，待人类拍 |
| 3 条 `dependency_rule` | 设计选择的编码 |

## 7 已知局限（需人类在两种口径间选择）

1. **现行 V1 检查器只读 `dependency_rule` 字面边**（`registry/checks/v.py#L46-L59`），不展开 `layer_of`；因此上述 3 条规则实质只检查「层规则本身是否成环」。
   - 口径甲（**人类已选**）：接受此弱校验，登记后 V1 直接 pass。
   - 口径乙：升级 V1 为「按 `layer_of` 展开层规则 × 实际 import 边」校验（需要 import 边清单登记或静态扫描），判据更强，但属检查器升级。
2. `allowed` 方向未登记（只登 `forbidden`），V1 谓词只消费 forbidden；是否同时登记 allowed 由人类定。

## 8 未做事项

- 已写入白板 `layer_of` 9 条与 `dependency_rule` 3 条（登记人 `user`，2026-11-14）；未升级检查器、未展开 `layer_of`。检查器改动仅限「从 `domain_data` 读取登记条目」，判定口径仍是字面规则边（弱校验）。
