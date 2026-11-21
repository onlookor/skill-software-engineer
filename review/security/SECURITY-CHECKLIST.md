# 推送前安全审核检查单（SECURITY-CHECKLIST）

> 状态：**已批准生效**（人类 2026-11-21 批准，登记于 `CHANGELOG.md` 批次 0026）。
> 依据：`AGENTS.MD` 安全审核条款（独立复核规程条款之后一条）。
> 本检查单是该条款必查项的可执行版本；审核与独立复核是两件事，互不替代。
> 本目录（`review/security/`）只放审核记录与本检查单，不随包发布（打包源树为 `skills/software-engineering/`，本目录在其外）。

## 0. 触发时机

任何 `git push`、打标签、打包、发布或升版本之前。无审核记录即视为未审核，不得执行上述操作。

## 1. 审核对象（不只当前工作区）

```bash
# 待推送的全部提交与其差异（以 origin/main 为例，按实际远端与分支替换）
git log --oneline origin/main..HEAD
git diff origin/main...HEAD

# 全历史检索（每个必查项模式都要跑一遍 --all -S / -G）
git log --all -S'<模式>' --oneline
git log --all -G'<正则>' --oneline
```

## 2. 必查项（命中任一项即不得推送）

### ① 私钥与凭据

```bash
git log --all -p | grep -nE 'BEGIN [A-Z ]*PRIVATE KEY|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}'
git log --all -p | grep -inE '(password|passwd|secret|token|api[_-]?key)\s*[:=]'
git log --all --name-only --pretty=format: | sort -u | grep -E '(^|/)\.(netrc|env)(\.|$)'
```

### ② 本机环境信息

```bash
git log --all -p | grep -nE '~/\.ssh|/home/[a-z0-9_-]+/|/Users/[a-z0-9_-]+/'
git log --all -p | grep -nE '\b(10\.[0-9]+|192\.168|172\.(1[6-9]|2[0-9]|3[01]))\.[0-9]+\.[0-9]+\b'
git log --all -p | grep -inE 'hostname|proxy|:[0-9]{4,5}\b'
```

主机名、内网／代理地址与端口、`~/.ssh` 路径、登录用户名、终端回显的个人标识均在禁止之列；
命中后逐条人工确认是否本机真实信息（示例占位符如 `user@example.com` 不算，但须记录甄别理由）。

### ③ 与任务无关的私人内容

```bash
git log --all --name-only --pretty=format: | sort -u | grep -iE '\.(png|jpg|jpeg|gif|webp)$|screenshot|截图|私人|笔记|run[-_]log|fingerprint|指纹'
```

私人笔记、日志、截图、主机指纹记录：与任务无关即命中；与任务相关的证据也须确认不含 ①② 类信息。

## 3. 判定与处置

- 命中任一项：**不得推送**。确需保留的内容放仓外私人目录，仓内只留脱敏摘要。
- 已进远端的命中：按「一旦进入远端即视为已泄露」处理——清除历史不等于收回凭据，相关密钥与 token **须轮换**，轮换完成情况记入审核记录。
- 全部必查项零命中（或命中已脱敏并记录甄别理由）：出具审核记录后方可推送。

## 4. 审核记录（无记录即视为未审核）

- 落点：`review/security/<YYYYMMDD>-<批次号或 SHA 范围>.md`，只追加，不随包发布。
- 必含字段：审核人、日期、审核对象（SHA 范围＋全历史声明）、每个必查项的执行命令与输出摘要、逐项判定（零命中／命中及处置）、结论（可推送／不得推送）。
- 执行方自审的记录只陈述「按本检查单执行了什么、看到了什么」，不得写成「已复核」——独立复核另走 `独立复核规程.md`。

## 5. 不可逆操作门

改写历史（`filter-branch`／`filter-repo`）、`push --force*`、删除远端分支或标签：

1. 先取得**人类明确授权**（授权原文或指针记入审核记录）；
2. 先做备份：`git bundle create ../<repo>-backup-<YYYYMMDD>.bundle --all`（备份放仓外）；
3. 操作后重跑本检查单全历史部分，确认清除彻底；涉及凭据的按第 3 节轮换。
