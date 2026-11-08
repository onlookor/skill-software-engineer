# 方法注册表（registry/）

本目录是**方法注册表的机器层权威源**（母本 0.17）与其同源投影。母本各方面 x.2 的方法空间表格是**种子数据源视图**，不是决策权威（0.17.1）。

**本文件是目录导览，不承担规约。** 数据侧规约与自检／台账规约分别位于两份独立文档；本文件只说明文件角色、使用方法与去向。

## 1. 文件与规约位置

| 文件 | 说明 | 规约位置 |
|---|---|---|
| `DATA-SPEC.md` | 《注册表数据侧规范》：文件角色、schema、键名映射、字段语义、谓词书写、编号先例、来源标注 | 本文档自身 |
| `CHECK-SPEC.md` | 《注册表自检与台账规范》：检查矩阵、级别、量词、执行顺序、台账登记、批次先例、变更纪律 | 本文档自身 |
| `profiles.yaml` | 18 个 kind 的字段剖面（元注册条目）＋剖面级缺口台账 | [DATA-SPEC](DATA-SPEC.md) D1.3、D2 |
| `predicate_vocabulary.yaml` | 母本机器层谓词清单的数据侧投影（非权威） | [DATA-SPEC](DATA-SPEC.md) D1.3、D3 |
| `method_registry.yaml` | 条目本体＋缺口台账＋状态迁移简记＋Waiver＋人工判断登记 | [DATA-SPEC](DATA-SPEC.md) D2；[CHECK-SPEC](CHECK-SPEC.md) C4 |
| `schedules.yaml` | 调度项注册表（C-1）：schema＋空表，本仓无实例 | [DATA-SPEC](DATA-SPEC.md) D1.3；附录 C.1 |
| `canary_gates.yaml` | 放量判据注册表（C-4）：schema＋空表，本仓无实例 | [DATA-SPEC](DATA-SPEC.md) D1.3；附录 C.1 |
| `test_doubles.yaml` | 测试替身使用登记表（C-15）：schema＋空表，本仓无实例 | [DATA-SPEC](DATA-SPEC.md) D1.3；附录 C.1 |
| `contract_changes.yaml` | 契约变更登记表（C-16）：schema＋空表，本仓无实例 | [DATA-SPEC](DATA-SPEC.md) D1.3；附录 C.1 |
| `config_changes.yaml` | 配置变更登记表（C-14）：schema＋空表，本仓无实例 | [DATA-SPEC](DATA-SPEC.md) D1.3；附录 C.1 |
| `pool_capacity.yaml` | 池容量注册表（C-6＋C-7 合并）：schema＋空表，本仓无实例 | [DATA-SPEC](DATA-SPEC.md) D1.3；附录 C.1 |
| `event_catalog.yaml` | 领域事件目录（C-9）：指针表 schema＋空表，本仓无实例 | [DATA-SPEC](DATA-SPEC.md) D1.3；附录 C.1 |
| `scripts/project.py` | 自检与同源投影工具 | [CHECK-SPEC](CHECK-SPEC.md) C1、C3 |
| `projections/*.md` | 人类可读投影与自检报告（生成物） | [CHECK-SPEC](CHECK-SPEC.md) C3.2 |

## 2. 上位文档

- 母本《软件工程元框架成文法》：0.17.2（条目 schema）、0.17.3（kind 枚举）、0.17.5（生命周期）、0.17.7（准入）、0.17.8（M 系列）、0.12（参考文献）、0.13（治理）。
- 变更登记：`../软件工程元框架成文法-changlog.md`。
- 目录规约：`../AGENTS.MD`。

## 3. 用法

```bash
cd registry
python3 scripts/project.py --check      # 仅自检，写 projections/自检报告.md
python3 scripts/project.py --project    # 自检 + 生成人类层投影
```

产物：`projections/STY.md`、`projections/自检报告.md`、`projections/勘察义务清单.md`、`projections/索引.md`。执行顺序、退出码与生成物纪律见 [CHECK-SPEC](CHECK-SPEC.md) C3。

## 4. 历史批次去哪儿了

原 §4「编号裁决留痕」的规范先例已迁入 [CHECK-SPEC](CHECK-SPEC.md) C5（逐条对照见其附录 A）；批次流水、历史计数与裁决全文保留于 git 历史与 changelog，本文件不再复述。
