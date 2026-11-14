# W4 数据所有权草案（pact-dsh）

- 状态：**已批准并落地**（人类 `user`，2026-11-14：先按口径丙登记，同日确认「W4 通过」后转 pass，属人工核结论）。本文件作为批准记录保留，白板已登记。
- 依据仓库：`/home/user/projects/pact-dsh`（`dsh-plugin-pact` 0.1.2）
- 日期：2026-11-14
- 用法：§0 为批准后的最终归属，与下文候选冲突时以 §0 为准。

## 0 批准定稿（2026-11-14）

- [x] `owned_by(observer, events.jsonl, write)` — 依据 `src/observer.js:16 appendFileSync`（唯一写点）、`src/observer.js:9`（默认文件名）
- [x] `owned_by(index, events.jsonl, create_and_configure)` — 依据 `index.js:13`（创建 `FileSink`）、`config.mirrorDir`（路径；`null` 时不创建）
- [x] 进程级单例（backend 注册表、`FakePactBackend` 单例状态）**不算**共享数据对象，已剔除
- [x] 只读配置对象**不计入**所有权，已剔除
- [x] 撤回「单写者是否成立」确认项：它是判据结果，由检查器判，不作为登记输入

> **局限（必须随 pass 一并引用）**：W4 的 pass 是**人工核结论**。人类 `user` 于 2026-11-14 确认单一所有者（`observer` 写入权、`index` 创建/配置权），登记为 `human_review`；检查器只校验该记录存在，**不机械核单一所有者**。该检查与 V1 打包为「将来升级为机械校验」项（见 run-log §23.3／§24），升级后再回头复核。

---

## 1 仓库事实：全部持久化写点

对 `*.js`（排除 `node_modules`）检索 `appendFileSync|writeFileSync|createWriteStream|mkdirSync|renameSync|unlinkSync|openSync`，命中仅 2 处，均在 `src/observer.js`：

| # | 位置 | 语句 | 作用 |
|---|---|---|---|
| 1 | `src/observer.js:12` | `mkdirSync(dir, { recursive: true, mode: 0o700 })` | 创建审计目录（仅目录） |
| 2 | `src/observer.js:16` | `appendFileSync(this.file, ...)` | 追加一行 JSONL（唯一数据写入） |

**无一例外**：其余单元没有持久化写入。

## 2 共享数据对象清单（事实 + 候选归属）

> **批准后状态**：2.2／2.3／2.4（进程级单例与 backend 状态）按裁定**不算**共享数据对象；2.6（只读配置）**不计入**所有权；2.5（observer 内部缓冲）维持「不跨单元共享」。仅 2.1 的两条拆分条目生效，见 §0。

### 2.1 `events.jsonl`（审计镜像，持久化）

- 默认文件名：`src/observer.js:9`（`file = 'events.jsonl'`）
- 路径来源：`config.mirrorDir`；`index.js:13` 创建 `FileSink`（`mirrorDir === null` 时不创建）
- 写入点：`src/observer.js:16`（唯一）
- 写入路径：`index.js:16-21` 收到 `session/event` → `observer.record` → `src/observer.js:60-65` → `sink.append`
- 读取点：仓库内无读取者（append-only）
- 候选归属：**`observer`**（拥有 sink 实现与写路径）
- 需人类确认：`index` 决定是否创建 sink 与目录，是否把「生命周期/配置权」也计入所有者
- [ ] 同意 `owned_by(observer, events.jsonl)`
- [ ] 修改为：`owned_by(______, events.jsonl)`（请填）

### 2.2 `FakePactBackend._tokens`（内存，跨单元共享）

- 声明：`src/pact-backend.js:43`
- 写入：`src/pact-backend.js:151-152`（`tokens.set` / `this._tokens.set`）
- 读取：`src/pact-backend.js:73,122,146`
- 共享范围：`loop.js:11` 的进程级单例 `fakeBackend`（`loop.js:29-35`）被所有会话复用 → 跨会话共享
- 候选归属：**`pact-backend`**（状态封装在其类内，无外部直接写入）
- [ ] 同意 `owned_by(pact-backend, fake_backend.tokens)`
- [ ] 修改为：`owned_by(______, ______)`

### 2.3 `FakePactBackend._requests`（内存，跨单元共享）

- 声明：`src/pact-backend.js:44`
- 写入：`src/pact-backend.js:130`（幂等结果缓存）
- 读取：`src/pact-backend.js:106`
- 共享范围：同 2.2（进程级单例）
- 候选归属：**`pact-backend`**
- [ ] 同意 `owned_by(pact-backend, fake_backend.requests)`
- [ ] 修改为：`owned_by(______, ______)`

### 2.4 进程级 backend 注册表（内存，跨会话共享）

- `fakeBackend`：`loop.js:11` 声明、`loop.js:29-35` 惰性创建并复用
- `wasmBackends`：`loop.js:12` 声明、`loop.js:16` 读、`loop.js:25` 写
- 键空间：`domain/instance`（`loop.js:18-24`）
- 写入/读取点均只在 `loop-entry`
- 候选归属：**`loop-entry`**
- [ ] 同意 `owned_by(loop-entry, backend_registry)`
- [ ] 修改为：`owned_by(______, ______)`

### 2.5 审计内存缓冲 `records`（内存，非跨单元）

- 声明：`src/observer.js:52`；写入 `:58`；裁剪 `:59`；快照 `:68-69`
- 作用域：每个 observer 实例私有，`snapshot()` 仅在 observer 内部暴露
- 事实：**不跨单元共享**
- [ ] 同意「不计入共享数据对象」
- [ ] 反对，理由：`______________________`

### 2.6 配置对象（只读共享）

- 构建：`src/config.js:151` `loadConfig` → 归一化对象
- 写入：构建后无写入点（`DEFAULTS` 为 `Object.freeze`，`src/config.js:10`）
- 读取：`index.js:12`、`loop.js:8`（两个入口各构造一份）
- 候选归属：**`config`**（只读，非可变共享）
- [ ] 同意 `owned_by(config, config_snapshot)`（只读）
- [ ] 认为只读配置不算共享数据对象（不计入 W4）

## 3 `owned_by` 归属汇总草案

| 对象 | 候选所有者 | 依据强度 | 勾选 |
|---|---|---|---|
| `events.jsonl` | `observer` | 写路径唯一，但创建权在 `index` → 需确认 | - [ ] |
| `fake_backend.tokens` | `pact-backend` | 状态封装在类内，强 | - [ ] |
| `fake_backend.requests` | `pact-backend` | 同上，强 | - [ ] |
| `backend_registry` | `loop-entry` | 声明与读写均在该单元，强 | - [ ] |
| `config_snapshot` | `config` | 只读，弱（是否计入待定） | - [ ] |

## 4 需人类确认的点（已裁定）

1. `events.jsonl` 的所有者：**已拆分为两条**——`observer`（写入权）、`index`（创建/配置权），见 §0。
2. 进程级单例是否算共享数据对象：**不算**，已剔除。
3. 只读配置对象是否计入 W4：**不计入**，已剔除。
4. 「单写者是否成立」：**已撤回**，不作登记输入；由检查器判定。

## 5 已知局限（登记归登记，W4 判定仍需口径）

**人类已选口径丙，并于同日确认 W4 通过**：登记 `human_review`（`user`、human、2026-11-14）后 W4 转 **pass**。该 pass 是人工核结论，不是机械校验；后续与 V1 一起升级为机械校验，再回头复核。

## 6 未做事项

- 已写入白板 `owned_by` 2 条（登记人 `user`，2026-11-14），并登记 `human_review` 使 W4 转 pass；未做单一所有者机械校验；检查器改动仅限「从 `domain_data` 读取登记条目与人工核记录」。
