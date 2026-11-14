# 草案：DEP-PACT-DSH-01 回滚声明（2026-11-14）

> **状态：草案，未生效**。不落地、不改 `release.yml`、不改部署策略登记。
> 上游：G3 要求 `DEP-PACT-DSH-01` 具备 `rollback` 与 `compatible_with_style`；本文只解决 `rollback`。
> 事实基线：包 `dsh-plugin-pact@0.1.2` 已发布 npm；[release.yml](file:///home/user/projects/pact-dsh/.github/workflows/release.yml) 由 `v*` 标签触发，
> 执行 `npm run check` → `npm test` → `npm publish --provenance --access public`；无 deprecate／回滚任务。

## 背景

npm 已发布版本在超过 72 小时或已有依赖者后**不可真正撤回**，且同一版本号不可重复发布。
因此「回滚」只能是以下两种之一，二者后果不同，需要人类勾选。

## 路径一：`deprecate`（标记弃用，不换版本）

**做法**：对已发布版本执行 `npm deprecate dsh-plugin-pact@0.1.2 "<原因与替代版本>"`。

| 维度 | 后果 |
|---|---|
| 对消费者 | 安装仍会成功，代码仍是坏版本；npm 安装时显示弃用警告；已锁定的 lockfile 不受影响 |
| 对版本号 | 不产生新版本，`0.1.2` 仍是 `latest`；不可撤回、不可重发同号 |
| 对 `release.yml` 的要求 | 需新增 `workflow_dispatch` 任务：校验输入版本与消息、使用有 deprecate 权限的 npm 凭据（`NPM_TOKEN` secret；现有 OIDC 发布流程不覆盖 deprecate），不构建产物 |

**优点**：动作最快，不改代码、不动 `latest`，对消费者是明确信号。
**缺点**：**不修复任何东西**；新用户仍会装到坏版本；必须有后续版本才算真正回滚。

## 路径二：发新版回退（新版本号承载旧代码）

**做法**：回退到上一个可用实现（revert 或重新提交旧实现），升补丁号发布（如 `0.1.3`）。

| 维度 | 后果 |
|---|---|
| 对消费者 | `^0.1.x` 范围在下次安装时自动拿到修复；精确锁定 `0.1.2` 的消费者仍需手动升级；无需改代码 |
| 对版本号 | 产生新补丁 `0.1.3`，`latest` 前移；`0.1.2` 仍留在 registry（不可撤回） |
| 对 `release.yml` 的要求 | **现有 tag 触发流程即可**：revert commit → `package.json` 升补丁 → 打 `v0.1.3` 标签 → 现有任务执行 check/test/publish。若要一键化，可加 `workflow_dispatch` 输入基线 tag 并自动升号，但非必需 |

**优点**：真正修复，符合 npm 版本单调递增的约束；对范围依赖的消费者近乎透明。
**缺点**：需要一次完整的发布流程；精确锁定旧版的消费者不会自动修复；`0.1.2` 仍可被安装。

## 对比

| 维度 | ① deprecate | ② 发新版回退 |
|---|---|---|
| 是否修复缺陷 | 否 | 是 |
| 是否产生新版本 | 否 | 是 |
| 对 `^0.1.x` 消费者 | 仍装坏版本（带警告） | 下次安装自动修复 |
| 对精确锁定消费者 | 仅警告 | 需手动升级 |
| 对 `release.yml` | 需新增 deprecate 任务＋凭据 | 现有 tag 流程即可 |
| 可逆性 | 可撤销弃用标记 | 新版本不可撤回，只能再发新版 |

## 建议默认值（待人类勾选）

**默认采用「② 发新版回退为主，① deprecate 为配套标注」：**

1. 确认 `0.1.2` 存在需回滚的缺陷后，先发 `0.1.3`（revert + 补丁号），让范围依赖的消费者尽快恢复。
2. 同时对 `0.1.2` 执行 `deprecate`，消息指向 `0.1.3`，避免新用户继续安装坏版本。
3. `rollback` 字段记录为：「发补丁版回退＋对缺陷版本 deprecate；已发布版本不可撤回」。

理由：单独 deprecate 不修复问题；单独发新版会让新用户仍可能命中旧版。两者组合成本最低、覆盖最全。

## 待人类勾选

- [ ] 采用建议默认值（发新版回退＋deprecate 配套）
- [ ] 只采用 deprecate（接受「不修复」）
- [ ] 只采用发新版回退（接受旧版仍可安装）
- [ ] `release.yml` 是否新增 `workflow_dispatch` 一键回滚任务（默认不做）
- [ ] deprecate 使用的 npm 凭据方式（`NPM_TOKEN` secret / 其他）

## 明确不做

- 不修改 `release.yml`。
- 不执行任何 npm 命令。
- 不改白板 `deploy_strategy.rollback`；等人类勾选后再登记。
