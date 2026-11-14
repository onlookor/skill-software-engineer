# 13 条 escalate 的可裁清单（2026-11-13）

性质：pilot 记录，不是母本条款。本文件只做**清单与方案**，未改任何检查器、未改白板、未改母本。

## 0 口径

- 判定源：`registry/checks/{v,w,x,t,g}.py`；当前 escalate 的唯一原因是白板缺对应键（`whiteboard-pact-dsh.yaml` 无这些键）。
- 部署实体：`/home/user/projects/pact-dsh`（`dsh-plugin-pact` 0.1.2，已发布 npm；7 个 `src` 模块＋2 个入口，8 个测试文件，CI 只跑 `npm run check`＋`npm test`）。
- 「补齐后会变成什么」分三类：
  - **P（机械）**：检查器有真判据，数据齐备后按规则判 pass/fail。
  - **P（粗判）**：检查器只查「键是否存在」，一登记就 pass，**不校验内容**——这类 pass 名不副实，必须先升级判据。
  - **仍 E / 转 F**：检查器在数据齐备后仍返回 escalate，或按真判据会 fail。
- 本清单**不落任何改动**；凡新增白板登记键或升级判据的动作，均待人类批准后执行。

## 1 总表

| 性质 | 缺的域数据源（白板键／谓词） | 母本锚点 | 现在由谁／什么产出 | 在案可替代数据 | 补齐后 |
|---|---|---|---|---|---|
| V1 | `dependency_rule(·,·,forbidden)` 实例 | 1.5 @1105 | 架构分层决策（人）；当前无 | `pact-dsh` 导入图可自动导出（9 模块、11 条内部 import 边） | **P（机械）**：有环 fail，无环 pass |
| V2 | `connects(u1,u2,p)`＋style 允许协议集 | 1.5 @1106 | 运行时接口清单（人）；当前无 | README＋`cordis.patch.yml` 可推出唯一同步链 | **P（粗判）**：不校验 `p ∈ allowed_protocols(S)` |
| W1 | `module_inventory` | 2.5 @1337（0.15 冻结项） | 代码库文件树 | 9 个模块（`index.js`、`loop.js`、`src/*.js`） | **仍 E**：现有数据后仍返回「需人工核接缝封闭」 |
| W2 | `module_inventory` | 2.5 @1338 | 代码库文件树 | 9 模块＋8 测试文件的映射 | **仍 E**：仍返回「需人工核可独立验证」 |
| W4 | `owned_by(M,d)`／`data_owner` | 2.5 @1341 | 无 | `observer.js` 审计 JSONL 是唯一数据出口（隐含单写者） | **仍 E**：仍返回「需人工核单一所有者」 |
| X1 | `connects(...)`＋契约注册 | 3.5 @1587 | 无契约注册表 | `pact-backend.js` 头注释的 backend contract＋`FakePactBackend` 同形实现 | **P（粗判）**：不校验 `covers(C,u1,u2)` |
| X2 | `contract(...)` 注册 | 3.5 @1588 | 无 | `package.json` 0.1.2＋`exports`＋`peerDependencies`（版本/兼容的最接近物） | **P（粗判）**：不校验 version／compat_policy |
| X5 | `contract(...)` 注册 | 3.5 @1593 | 无 | 无逐契约 ADR；仅 3 份项目级 ADR | **P（粗判）**：登记即 pass，但「发布即批准」无 ADR 证据 |
| X6 | `shared_data_access(...)` 写入 | 3.5 @1594（3.2.3 四条件） | 无 | 当前无跨单元共享数据（可声明空集） | **P（粗判）**；若声明空集，应改 vacuous 而非 pass |
| T4 | `unit_test_inventory` | 8.5 @2980 | `test/` 目录＋CI | 8 个测试文件覆盖 7 个 src 模块＋patch 清单；两个入口无直接测试 | **P（粗判）**；判据升级后入口会成缺口 |
| T6 | `contract(...)`＋CI 契约测试 | 8.5 @2983 | 无契约测试；CI 仅单元测试 | 无 | **仍 E／转 F**：无契约测试套件 |
| G3 | `deploy_strategy` | 9.5 @3259 | `release.yml`＋`cordis.patch.yml` | 有发布与 patch 面；**无回滚程序** | **P（粗判）**；判据升级后因缺回滚转 F |
| G7 | P2 信号＋阈值/趋势窗 | 9.5 @3266 | 无 | 无 | **P（粗判）**；判据升级后转 F |

## 2 不需要新建数据源的项（批 A，优先）

这些项的**原始数据已在案**，只缺「登记／映射」；仍属新增白板键，故本轮只出方案。

### A-1 W1、W2（模块目录）
- 现成数据：`pact-dsh` 的 `index.js`、`loop.js`、`src/{config,govern,loop,names,observer,pact-backend,wasm-backend}.js`，共 9 个模块。
- 接缝证据：`FakePactBackend`、`createWasmBackend` 可替换后端；8 个测试文件对 7 个 src 模块直测。
- 卡点：检查器在 `module_inventory` 存在后**仍只返回 escalate**（`w.py::w1/w2`）。要转 pass 必须新增判定规则（seam 判据、独立验证判据），这是**改判据**，须人裁。

### A-2 T4（单元测试清单）
- 现成数据：`test/{config,govern,names,observer,wasm-backend,fake-backend,loop-routing,manifest}.test.js`；CI `npm test` 执行 `node --test test/*.test.js`。
- 映射：7 个 src 模块（`fake-backend` 测 `pact-backend`）＋`cordis.patch.yml` 清单；`index.js`、`loop.js` 两个装配入口无直接测试。
- 补齐后：若只登记清单，**粗判 pass**；若按「∀unit M: test_suite ≠ ∅」真判，两个入口缺套件，需补测试或把它们排除在单元清单外（需人裁定性）。

### A-3 X2、X5（契约版本与发布批准）
- 现成数据：`package.json` `version: 0.1.2`（已发布 npm）、`exports` 显式导出面、`peerDependencies` 约束。
- 缺口：没有「契约」清单，也没有逐契约 ADR；现有 3 份 ADR 是项目级（STYLE／ENV／TS-CON）。
- 补齐后：登记即**粗判 pass**，但 X5 的「发布即批准」实际缺 ADR 证据，建议先补判据再登记。

### A-4 X1（交互→契约覆盖，部分）
- 现成数据：`src/pact-backend.js` 头注释声明 backend contract；`FakePactBackend` 与 `createWasmBackend` 同形实现，可作「已验证覆盖」的线索。
- 缺口：无 `connects` 实例、无契约注册表；且现有检查只认 `connects(` 是否存在。
- 补齐后：**粗判 pass**，不能证明「无未登记跨单元交互」。

### A-5 G3（部署策略，部分）
- 现成数据：`.github/workflows/release.yml`（tag 触发、OIDC 发布）、`cordis.patch.yml`（禁用原 agent-loop、插入两行）。
- 缺口：**无回滚程序**；`compatible(strategy, active_style)` 无判定面。
- 补齐后：**粗判 pass**；按真判据会 fail（缺 rollback）。

## 3 需要新数据源的项（批 B）

### B-1 V1（禁止依赖规则）
- 缺的是**规则本身**，不是图。导入图可从 `pact-dsh` 自动导出（`config←names`、`govern←names`、`loop←govern,names`、`index←config,observer`、入口←src…）。
- 有了图仍不能判：`dependency_rule(·,·,forbidden)` 是架构决策，须人给（例如「src 不得反向依赖入口」）。
- 补齐后：**真判据**，无环 pass，有环 fail。

### B-2 V2（连接协议与允许集）
- 缺 `connects(u1,u2,p)` 实例；可推出的只有「DSH agent loop → PACT backend」的进程内同步调用，不是网络协议。
- 允许集须从 `style(pact-dsh, 同步请求-响应)` 派生，但母本未给 `allowed_protocols(S)` 的取值表（需人裁口径）。
- 补齐后：**粗判 pass**；真判据需要 `p ∈ allowed_protocols(S)` 的可判定右项。

### B-3 W4（数据单一所有者）
- 缺数据实体清单与 `owned_by`。可辨认的实体只有审计日志（`observer.js` 写 JSONL），归属隐含为 pact-dsh 自身。
- 补齐后：**仍 escalate**；要判必须新增「所有权判据」（改检查器）。

### B-4 X6（共享数据访问）
- 当前部署**没有**跨单元共享数据；这是「域为空」而非「数据源未登记」。
- 正确处理：登记显式空集并记 **vacuous**（如 M8 先例），不是 pass。
- 若未来出现共享数据，才需要 3.2.3 四条件的登记与判据。

### B-5 T6（契约测试）
- 缺契约测试套件。CI 只跑单元测试；`manifest.test.js` 校验的是 bundle patch 名称，不是契约测试。
- 补齐后：仍 **escalate／fail**——必须先建契约测试，再谈 pass。

### B-6 G7（P2 信号告警）
- 无 P2 信号、无阈值、无趋势窗口；仓库无监控/告警配置。
- 补齐后：**粗判 pass**；真判据（双判据成立）需要阈值与窗口数据。

## 4 必须先知会的判定面问题

1. **9 个检查器是「存在即 pass」**：V2、X1、X2、X5、X6、T4、T6、G3、G7 只判断白板键/谓词是否出现，不校验内容。直接补登记会把 escalate 变 pass，但性质并未真正核验。建议：先升级判据，再补数据；或明确接受「登记即 pass」的弱语义。
2. **3 个检查器在数据齐备后仍 escalate**：W1、W2、W4（`w.py` 第二条分支就是 escalate）。这三条即使补数据也转不了 pass，必须改判据。
3. **空集与未登记要分开**：X6（共享数据）当前是空集，应按 vacuous；W4、G7 也可能落在空集或未登记，需要逐条定性。

## 5 需人类裁定的事项

- **D-A 登记键白名单**：是否批准新增 `module_inventory`、`dependency_rule`、`connects`、`contract`、`unit_test_inventory`、`deploy_strategy`、`P2`／`alarm_threshold`、`shared_data_access`、`owned_by` 这些白板键（可分两批）。
- **D-B 判据升级**：是否同意先把 9 个「存在即 pass」检查器升级为真校验；否则补齐后的 pass 不可信。
- **D-C 空集定性**：X6 是否按 vacuous 记录；`index.js`／`loop.js` 两个入口是否算独立单元（影响 T4）。
- **D-D 批 A 落地**：批准后，批 A（W1/W2/T4/X2/X5/G3 部分）按什么顺序落；登记人是否仍记 `user`。

## 6 前置一致性欠账（落批 A 前应修）

`whiteboard-pact-dsh.yaml` 仍写 `artifact_version: pilot-20261112.8`、`style` 状态 `provisional`、SM-DR `provisional`、10.2.5「1/6」。这些与现行 `.9`／`approved`／`6/6` 不一致。登记新键前应先修正基线，否则新数据会挂在过期白板上。本轮未改。

## 7 落地结果（2026-11-14，批 A）

四条裁定 D-A～D-D 已获人类批准并执行，详见 run-log §21。要点：

- **前置欠账已修**：白板 `artifact_version` → `.9`、`style`／SM-DR → `approved`、`grounding_status` → 6/6（v1.6.0）。
- **9 个检查器已升级**为内容校验（V2/X1/X2/X5/X6/T4/T6/G3/G7），不再「存在即 pass」。
- **批 A 已登记**：`module_inventory`(9)、`unit_test_inventory`(9)、`connects`(1)、`contract`(1)、`deploy_strategy`(1)、`shared_data_access`(`[]`)。
- **实跑分布**：pass 29 / fail 4 / escalate 6 / vacuous 9（此前 26/0/13/8）。

逐条结局：

| 性质 | 落地后 | 说明 |
|---|---|---|
| V2 | **pass** | 批 A 因 X1 需要 `connects` 而一并登记；协议在 style 允许集内 |
| X1 | **pass** | 1 条 connects 被 `CT-PACT-BACKEND-01` 覆盖 |
| X6 | **pass（vacuous）** | `shared_data_access: []` 显式空集（D-C） |
| X2 | **fail** | 契约缺 `compat_policy` |
| X5 | **fail** | 契约为 published 但无 ADR |
| T4 | **fail** | `index`、`loop-entry` 无测试（D-C 按独立单元计） |
| G3 | **fail** | 部署策略缺 `rollback` 与 `compatible_with_style` |
| V1/W1/W2/W4/T6/G7 | **仍 escalate** | 批 B，数据源未登记 |

本清单的 §4 三个判定面问题已处理：问题 1（存在即 pass）已升级；问题 2（W1/W2/W4 仍 escalate）待批 B 改判据；问题 3（空集 vs 未登记）已按 D-C 落地 X6。

## 8 批 B 第一步（2026-11-14）

- **T6 已落地**：仓库 `test/` 8 个文件均非契约测试，登记 `contract_tests: []`（显式空集）→ T6 escalate→**fail**（published 契约无契约测试）。
- **现行分布**：pass 29 / fail 5 / escalate 5 / vacuous 9；10.2.5 v1.8.0 仍 6/6（附同一分布）。
- **剩余 5 条 escalate**：V1、W1、W2、W4、G7。缺什么、由谁产出、两种口径的后果见 run-log §22.3–22.4，等待人类裁定。

## 9 批 B 第二步（2026-11-14）：V1/W4 登记（弱校验）

- **V1 已落地**：登记 `layer_of` 9 条＋`dependency_rule` 3 条；escalate→**pass**，但为弱校验（不展开 `layer_of`，只判层规则无环）。
- **W4 已落地**：登记 `owned_by` 2 条（`observer` 写入权、`index` 创建/配置权）；按口径丙仍 **escalate**（待人工核单一所有者）。
- **排除项**：进程级单例不算共享数据对象；只读配置不计入；撤回「单写者是否成立」确认项。
- **打包升级**：V1/W4 合并为「将来升级为机械校验」一项（run-log §23.3）。
- **现行分布**：pass 30 / fail 5 / escalate 4 / vacuous 9；10.2.5 v1.9.0 仍 6/6（附同一分布）。剩余 escalate：W1、W2、W4、G7。

## 10 批 B 第三步（2026-11-14）：W4 人工核转 pass

- 人类确认「W4 通过，升级机械校验后再回头看」，登记为 `human_review`（`approved_by=user`、`approver_kind=human`、`approved_at=2026-11-14`）。
- 归属：`observer` → `events.jsonl` 写入权；`index` → 创建/配置权。
- W4 escalate→**pass**，属**人工核结论**而非机械校验；与 V1 同列 `weak_checks`／`packed_upgrade`。
- **现行分布**：pass 31 / fail 5 / escalate 3 / vacuous 9；10.2.5 v1.10.0 仍 6/6（附同一分布）。剩余 escalate：W1、W2、G7。
