# 打包与安装

> 目标：用户**不克隆仓库**也能装。本文件既是打包清单，也是安装说明。
> 版本以 `SKILL.md` frontmatter 的 `version` 为唯一来源；当前 `0.2.0`。

## 一、包里放什么

只放运行技能所需的最小集合，全部来自 `skills/software-engineering/`：

| 路径 | 内容 | 为什么在包里 |
|---|---|---|
| `SKILL.md` | 路由表、不变量、挂载期交互协议、七项无值声明 | 技能入口，必须常驻可读 |
| `stages/S1-repro.md`、`S2-localize-fix.md`、`S3-verify.md` | 三张阶段卡 | 路由命中后要加载 |
| `schemas/repro.md`、`failing-test.md`、`fix-patch.md`、`verify-log.md`、`blocker-log.md` | 交付物 schema 与卡点日志 schema | 产出格式与机器可判部分 |
| `validators/validate.py`、`check_blocker_log.py`、`V09-checklist.md`、`README.md` | V01–V08 可执行、V09 人工清单、卡点日志校验 | 交付物与日志校验 |
| `examples/defect-repro-fix/` | 真 bug、失败测试、补丁、配置快照、`run.py`、`README.md` | 装完即可自检一条命令 |
| `PACKAGING.md`、`BACKFLOW.md` | 本文件与回流流程 | 安装说明与卡点回流随包走 |

包内另生成 `PACKAGE-MANIFEST.txt`（版本号＋逐文件 sha256），不手工维护。

## 二、包里不放什么

以下一律**不进入分发包**，它们属于编译工作区资产或本仓内部证据，对装技能的用户既无用又是噪声：

- `registry/`、`pilot/`、`adr/`、`archieve/`、`pact/`；
- 母本 `软件工程元框架成文法.md` 及其 changelog、编译规范、总账/施工单/方案/白板等根目录文档；
- 任何 run-log、编译产物、锚索引、`anchor_baseline.json`、检查器脚本与卡片；
- 本仓内部测试证据 `skills/software-engineering/tests/`（如路由测试记录）；
- 打包脚本自身 `skills/software-engineering/scripts/`；
- `.git`、`__pycache__`、`*.pyc`、示例运行产物 `examples/*/work/`。

打包脚本会在归档后**反向断言**：归档内不得出现上述任何名字，出现即以退出码 1 失败。

## 三、产物形态

每次打包产出两件等价物（同一份内容）：

```
dist/software-engineering-0.2.0/                  # 目录形态，顶层即技能根
dist/software-engineering-0.2.0.tar.gz            # 归档形态
dist/software-engineering-0.2.0.tar.gz.sha256     # 归档校验值
```

目录形态的顶层目录就是安装后的技能目录，`SKILL.md` 在它下面第一层。

## 四、谁来打包、谁来装、装到哪

| 角色 | 动作 | 在哪 |
|---|---|---|
| 维护者（交付方） | 运行打包命令，产出 `dist/` 下两件产物 | 本仓根目录 |
| 发布者（交付方） | 把 `*.tar.gz` 与 `*.sha256` 作为 release 附件提供 | 仓库的 release / 内部分发点（本仓不出自动化） |
| 安装者（使用方） | 下载归档 → 校验 sha256 → 解包 → 放进 agent 的 skills 目录 | 目标机器 |

**装到哪里**：装到目标 agent 的「技能目录」下，目录名取 `software-engineering`，使入口为 `<skills-dir>/software-engineering/SKILL.md`。本仓自身的形态就是 `<workspace>/skills/software-engineering/`，可作参照；具体目录名由宿主 agent 的约定决定，本文件不替宿主定默认值。

## 五、可执行命令

打包（维护者，在仓库根目录）：

```bash
python3 skills/software-engineering/scripts/build_package.py
```

脚本只用 Python 标准库，不引入新依赖；版本号从 `SKILL.md` 读取，不另行维护；重复运行会先清空 `dist/` 下同名产物。

安装（使用方，不需要仓库）：

```bash
sha256sum -c software-engineering-0.2.0.tar.gz.sha256
tar -xzf software-engineering-0.2.0.tar.gz
# 得到 software-engineering-0.2.0/；移动到 agent 的 skills 目录并改名为 software-engineering
mv software-engineering-0.2.0 <skills-dir>/software-engineering
```

装完自检（可选，不需要真实项目）：

```bash
python3 <skills-dir>/software-engineering/examples/defect-repro-fix/run.py
```

退出码 0 表示示例闭环（V01–V08）在安装位置上跑通；它只证明安装完整，不证明技能在真实仓库上可用。

## 六、失败处理

- 归档内出现「不放什么」中的任何名字 → 脚本退出码 1，删除本次产物，不发布。
- `SKILL.md` 缺 `version` 或版本串非法（非 `X.Y.Z`）→ 退出码 1。
- 白名单路径缺失 → 退出码 1（缺 `SKILL.md`、`stages/`、`schemas/`、`validators/`、`examples/` 任一）。
- 安装后自检非 0 → 先核对版本与 sha256 是否匹配，再查宿主 agent 的 skills 目录约定；不得跳过校验直接覆盖旧版本。
