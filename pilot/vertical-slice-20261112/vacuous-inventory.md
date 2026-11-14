# 空真清单（判据四首轮全量，fvr-full-run-1.json）

- 生成时间：2026-11-13
- 分母：母本 39 条硬性质（`hard-properties.snapshot.json`）
- 判定：`vacuous=true` 仅当**量化域本身为空**；「检查器已接但域数据源未登记」不算空真，记 `escalate`。
- 首轮实跑：pass 25 / fail 0 / escalate 14 / vacuous 8（其中 escalate 含 E7 批准缺失 1 条，与本表 13 条共同构成 14）。

## 一、真空真（8 条）——本部署无该类实例

| 性质 | 检查程序 | 空集依据（实跑证据） |
|---|---|---|
| M8 | checks/m.py::m8 | `method_registry` 无 `seed_revalidation` 记录（未发生种子重校验事件） |
| M14 | checks/m.py::m14 | 白板无快速通道使用记录 |
| M20 | checks/m.py::m20 | 白板无 `conflict_instance` 写入（无 A0×A0 不相容实例） |
| M25 | checks/m.py::m25 | changlog 无 FM 目录变更记录（本轮未改目录） |
| W7 | checks/w.py::w7 | 无分解主策略决策（`DP-*-DECOMP` 未启动） |
| R8 | checks/r.py::r8 | 白板无 `reopen_proposal`／`reopen(` 记录（未发生需求重开） |
| E1 | checks/e.py::e1 | 5 个评审点均未声明 `predicate_subset`；`view_instances` 集合为空 → 量化域为空 |
| E2 | checks/e.py::e2 | 无 `view_instance`，无视图实例可校验生成来源 |

## 二、原按空真处理、经复核不算空真（13 条，已改为 escalate）

以下各项的量化域**不是空集**：部署中存在对应对象（模块、交互、契约、测试、部署策略、依赖、数据实体），只是白板/注册面未登记。按「尚未接入检查」处理，不得记空真。

| 性质 | 检查程序 | 域内对象 | 未登记项 |
|---|---|---|---|
| V1 | checks/v.py::v1 | 分层/依赖 | 白板无 `dependency_rule` 实例 |
| V2 | checks/v.py::v2 | 单元间连接 | 白板无 `connects` 写入 |
| W1 | checks/w.py::w1 | 模块 | 白板无 `module_inventory` |
| W2 | checks/w.py::w2 | 模块 | 白板无 `module_inventory` |
| W4 | checks/w.py::w4 | 数据实体 | 白板无 `owned_by` 写入 |
| X1 | checks/x.py::x1 | 交互 | 白板无 `connects`／契约写入 |
| X2 | checks/x.py::x2 | 契约 | 白板无 `contract` 写入 |
| X5 | checks/x.py::x5 | 契约生命周期 | 白板无 `contract` 写入 |
| X6 | checks/x.py::x6 | 共享数据访问 | 白板无 `shared_data_access` 写入 |
| T4 | checks/t.py::t4 | 测试单元 | 白板无 `unit_test_inventory` |
| T6 | checks/t.py::t6 | 已发布契约 | 白板无 `contract` 写入 |
| G3 | checks/g.py::g3 | 部署策略 | 白板无 `deploy_strategy` |
| G7 | checks/g.py::g7 | P2 信号 | 白板无 P2 信号/告警阈值 |

## 三、与「21 条」对账

原首轮 21 条空真＝本表一（8 条）＋本表二（13 条）。表二改为 `escalate` 后，vacuous 收缩为 8，escalate 变为 14（13＋E7）。此变更只影响 verdict 分布，不影响判据四「接线完成＋首轮全量证据」的成立。
