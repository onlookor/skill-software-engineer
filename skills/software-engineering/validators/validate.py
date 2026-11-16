#!/usr/bin/env python3
"""V01–V08：缺陷复现—最小修复技能的可执行自动检查。

约定：退出码 0＝pass，1＝fail，3＝cannot_evaluate（缺配置／缺输入／不可判）。
用法：
    python3 validate.py --config <配置快照.yaml> [--only V01 V02 ...]

配置快照里的七项使用前约定只从文件读取；本文件不内置任何项的值、默认值、示例值。
缺任一项即 cannot_evaluate（退出码 3），不静默通过。
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("cannot_evaluate: 缺少 PyYAML\n")
    sys.exit(3)

PASS, FAIL, CANNOT = 0, 1, 3


class Result:
    def __init__(self, vid: str, code: int, lines: list[str]):
        self.vid = vid
        self.code = code
        self.lines = lines


def ok(vid: str, *lines: str) -> Result:
    return Result(vid, PASS, list(lines))


def bad(vid: str, *lines: str) -> Result:
    return Result(vid, FAIL, list(lines))


def cannot(vid: str, *lines: str) -> Result:
    return Result(vid, CANNOT, list(lines))


# ---------------------------------------------------------------- 配置

CONFIG_KEYS = (
    "repo_path",
    "test_command",
    "build_command",
    "repro_runs",
    "repro_timeout_seconds",
    "allowed_scope",
    "cache_cleanup_policy",
)


class Ctx:
    def __init__(self, cfg: dict, repo: Path):
        self.cfg = cfg
        self.repo = repo
        self.timeout = cfg.get("repro_timeout_seconds")

    def get(self, name: str):
        return self.cfg.get(name)


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def load_config(path: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, [f"配置快照不存在：{path}"]
    except yaml.YAMLError as exc:
        return {}, [f"配置快照不是合法 YAML：{exc}"]
    if not isinstance(raw, dict):
        return {}, ["配置快照必须是 mapping"]
    unknown = sorted(set(raw) - set(CONFIG_KEYS))
    if unknown:
        errors.append(f"配置快照含未声明项：{', '.join(unknown)}")
    cfg = {k: raw[k] for k in CONFIG_KEYS if k in raw}

    repo_val = cfg.get("repo_path")
    if not isinstance(repo_val, str) or not repo_val.strip():
        errors.append("repo_path 未约定或不是非空字符串")
    else:
        repo = Path(repo_val).expanduser()
        if not repo.exists():
            errors.append(f"repo_path 不存在：{repo_val}")
        elif not repo.is_dir():
            errors.append(f"repo_path 不是目录：{repo_val}")
        else:
            try:
                top = subprocess.run(
                    ["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, timeout=30,
                )
            except (OSError, subprocess.SubprocessError) as exc:
                errors.append(f"repo_path 无法执行 git：{exc}")
            else:
                if top.returncode != 0:
                    errors.append(f"repo_path 不是 git 仓：{repo_val}")
                elif Path(top.stdout.strip()).resolve() != repo.resolve():
                    errors.append(f"repo_path 不是仓根：{repo_val}")

    test_cmd = cfg.get("test_command")
    if not isinstance(test_cmd, str) or not test_cmd.strip():
        errors.append("test_command 未约定或不是非空字符串")
    elif "\n" in test_cmd:
        errors.append("test_command 必须是单行命令")

    build_cmd = cfg.get("build_command")
    if build_cmd is not None:
        if not isinstance(build_cmd, str) or not build_cmd.strip():
            errors.append("build_command 已给出但不是非空字符串")
        elif "\n" in build_cmd:
            errors.append("build_command 必须是单行命令")

    runs = cfg.get("repro_runs")
    if not _is_int(runs) or runs < 2:
        errors.append("repro_runs 未约定或不满足 >= 2")

    timeout = cfg.get("repro_timeout_seconds")
    if not _is_int(timeout) or timeout < 1:
        errors.append("repro_timeout_seconds 未约定或不满足 >= 1")

    scope = cfg.get("allowed_scope")
    if not isinstance(scope, list) or not scope:
        errors.append("allowed_scope 未约定或为空")
    else:
        for entry in scope:
            if not isinstance(entry, str) or not entry.strip():
                errors.append("allowed_scope 含非字符串项")
                continue
            p = Path(entry)
            if p.is_absolute() or ".." in p.parts:
                errors.append(f"allowed_scope 项不是仓内相对路径：{entry}")
            elif not (Path(repo_val).expanduser() / p).exists():
                errors.append(f"allowed_scope 项在仓内不存在：{entry}")

    policy = cfg.get("cache_cleanup_policy")
    if not isinstance(policy, str) or not policy.strip():
        errors.append("cache_cleanup_policy 未约定或不是非空字符串")

    return cfg, errors


# ---------------------------------------------------------------- 通用读取

def load_frontmatter(path: Path) -> tuple[dict | None, str | None]:
    if not path.exists():
        return None, f"缺文件：{path.name}"
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, f"{path.name} 缺 YAML frontmatter"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, f"{path.name} 的 frontmatter 未闭合"
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return None, f"{path.name} 的 frontmatter 不是合法 YAML：{exc}"
    if not isinstance(data, dict):
        return None, f"{path.name} 的 frontmatter 必须是 mapping"
    return data, None


def nonempty_str(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def single_line(v) -> bool:
    return nonempty_str(v) and "\n" not in v


def hexish(v) -> bool:
    return isinstance(v, str) and bool(re.fullmatch(r"[0-9a-fA-F]{7,40}", v.strip()))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
ADDR_RE = re.compile(r"0x[0-9a-fA-F]+")
DUR_RE = re.compile(r"\b\d+(?:\.\d+)?\s?(?:ms|us|µs|ns|s)\b")
WS_RE = re.compile(r"\s+")


def fingerprint(text: str, repo: Path) -> str:
    t = ANSI_RE.sub("", text)
    t = t.replace(str(repo), "<repo>")
    t = ADDR_RE.sub("<addr>", t)
    t = DUR_RE.sub("<t>", t)
    t = WS_RE.sub(" ", t).strip()
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def run_command(cmd: str, cwd: Path, timeout: int) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd, shell=True, cwd=str(cwd), capture_output=True, text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise
    except OSError as exc:
        raise RuntimeError(str(exc))
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def parse_iso(v) -> bool:
    if not isinstance(v, str) or not v.strip():
        return False
    s = v.strip().replace("Z", "+00:00")
    try:
        datetime.fromisoformat(s)
        return True
    except ValueError:
        try:
            date.fromisoformat(s)
            return True
        except ValueError:
            return False


def patch_map(text: str) -> dict[str, list[str]]:
    files: dict[str, list[str]] = {}
    cur = None
    for line in text.splitlines():
        m = re.match(r"^diff --git a/(.+?) b/(.+)$", line)
        if m:
            cur = m.group(2)
            files.setdefault(cur, [])
            continue
        if cur is not None:
            files[cur].append(line)
    return files


def under_scope(path: str, scope: list[str]) -> bool:
    for entry in scope:
        e = entry.rstrip("/")
        if path == e or path.startswith(e + "/"):
            return True
    return False


def is_test_path(path: str) -> bool:
    parts = path.split("/")
    name = parts[-1]
    if any(p in ("tests", "test", "__tests__") for p in parts[:-1]):
        return True
    return bool(re.match(r"^(test_.*|.*_test\.[^.]+|.*\.test\.[^.]+|.*\.spec\.[^.]+)$", name))


ASSERT_RE = re.compile(
    r"\b(assert|expect|should|require|assertEqual|assertRaises|pytest\.raises|"
    r"t\.(Fatal|Fatalf|Error|Errorf))\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------- V01–V08

def v01(ctx: Ctx) -> Result:
    data, err = load_frontmatter(ctx.repo / "repro.md")
    if err:
        return cannot("V01", err)
    problems: list[str] = []
    repo = data.get("repo")
    if not isinstance(repo, dict):
        problems.append("repo 缺失或不是 mapping")
    else:
        if not nonempty_str(repo.get("url")):
            problems.append("repo.url 缺失或为空")
        if not hexish(repo.get("commit")):
            problems.append("repo.commit 不是 7–40 位十六进制")
    env = data.get("env")
    if not isinstance(env, dict):
        problems.append("env 缺失或不是 mapping")
    else:
        if not nonempty_str(env.get("os")):
            problems.append("env.os 缺失或为空")
        if not nonempty_str(env.get("runtime")):
            problems.append("env.runtime 缺失或为空")
        deps = env.get("dependencies")
        if not isinstance(deps, dict):
            problems.append("env.dependencies 缺失或不是 mapping")
        else:
            for k, v in deps.items():
                if not nonempty_str(str(k)) or not nonempty_str(str(v)):
                    problems.append("env.dependencies 存在空项")
                    break
    if not single_line(data.get("command")):
        problems.append("command 缺失、为空或不是单行")
    if not nonempty_str(data.get("expected")):
        problems.append("expected 缺失或为空")
    if not nonempty_str(data.get("actual")):
        problems.append("actual 缺失或为空")
    ec = data.get("exit_code")
    if not _is_int(ec) or ec == 0:
        problems.append("exit_code 缺失或等于 0")
    fp = data.get("fingerprint")
    if not isinstance(fp, dict):
        problems.append("fingerprint 缺失或不是 mapping")
    else:
        if not nonempty_str(fp.get("run1")) or not nonempty_str(fp.get("run2")):
            problems.append("fingerprint.run1／run2 缺失或为空")
        elif fp.get("run1") != fp.get("run2"):
            problems.append("fingerprint.run1 ≠ run2")
    if not parse_iso(data.get("first_observed")):
        problems.append("first_observed 缺失或不是 ISO-8601")
    if problems:
        return bad("V01", *problems)
    return ok("V01", "repro.md 八字段齐全且类型正确")


def v02(ctx: Ctx) -> Result:
    data, err = load_frontmatter(ctx.repo / "repro.md")
    if err:
        return cannot("V02", err)
    cmd = data.get("command")
    if not single_line(cmd):
        return cannot("V02", "repro.md.command 缺失或不可执行")
    runs = ctx.get("repro_runs")
    timeout = ctx.get("repro_timeout_seconds")
    fps, outs = [], []
    for i in range(runs):
        try:
            code, out = run_command(cmd, ctx.repo, timeout)
        except subprocess.TimeoutExpired:
            return cannot("V02", f"第 {i + 1} 次运行超时，无法判定")
        except RuntimeError as exc:
            return cannot("V02", f"第 {i + 1} 次运行无法启动：{exc}")
        if code == 0:
            return bad("V02", f"第 {i + 1} 次运行退出码为 0（期望非 0）")
        outs.append(code)
        fps.append(fingerprint(out, ctx.repo))
    if len(set(fps)) != 1:
        detail = "；".join(f"run{i + 1}={fp}" for i, fp in enumerate(fps))
        return bad("V02", "连跑失败摘要不一致：" + detail)
    declared = data.get("fingerprint")
    if not isinstance(declared, dict) or not nonempty_str(declared.get("run1")):
        return cannot("V02", "repro.md.fingerprint 缺失，无法与实跑比对")
    if declared.get("run1") != fps[0]:
        return bad(
            "V02",
            "repro.md.fingerprint 与实跑计算值不一致",
            f"声明值={declared.get('run1')}",
            f"实跑值={fps[0]}",
        )
    return ok("V02", f"连跑 {runs} 次均非 0，失败摘要一致：{fps[0]}")


def v03(ctx: Ctx) -> Result:
    metas = sorted((ctx.repo / "tests").glob("repro_*.meta.yaml"))
    if not metas:
        return cannot("V03", "缺 tests/repro_*.meta.yaml")
    if len(metas) > 1:
        return cannot("V03", "tests/ 下有多份 repro_*.meta.yaml，无法判定是哪一件")
    meta_path = metas[0]
    try:
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return cannot("V03", f"{meta_path.name} 不是合法 YAML：{exc}")
    if not isinstance(meta, dict):
        return cannot("V03", f"{meta_path.name} 必须是 mapping")
    problems: list[str] = []
    if not nonempty_str(meta.get("file")) or not (ctx.repo / str(meta.get("file"))).exists():
        problems.append("file 缺失或指向的文件不存在")
    if not nonempty_str(meta.get("test_id")):
        problems.append("test_id 缺失或为空")
    if not single_line(meta.get("single_run_command")):
        problems.append("single_run_command 缺失或不是单行")
    if not hexish(meta.get("base_commit")):
        problems.append("base_commit 不是 7–40 位十六进制")
    if not nonempty_str(meta.get("expected_failure")):
        problems.append("expected_failure 缺失或为空")
    if problems:
        return bad("V03", *problems)
    try:
        head = subprocess.run(
            ["git", "-C", str(ctx.repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return cannot("V03", f"git rev-parse 失败：{exc}")
    if head.returncode != 0:
        return cannot("V03", f"git rev-parse 失败：{head.stderr.strip()}")
    if not head.stdout.strip().startswith(str(meta["base_commit"]).lower()):
        return bad(
            "V03",
            "HEAD 与 base_commit 不一致，无法在 base 上判定",
            f"HEAD={head.stdout.strip()}",
            f"base_commit={meta['base_commit']}",
        )
    timeout = ctx.get("repro_timeout_seconds")
    try:
        code, out = run_command(meta["single_run_command"], ctx.repo, timeout)
    except subprocess.TimeoutExpired:
        return cannot("V03", "失败用例单独运行超时，无法判定")
    except RuntimeError as exc:
        return cannot("V03", f"失败用例单独运行无法启动：{exc}")
    if code == 0:
        return bad("V03", "失败用例单独运行却通过（期望失败）")
    return ok("V03", f"失败用例单独运行退出码={code}（非 0）")


def v04(ctx: Ctx) -> Result:
    patch = ctx.repo / "fix.patch"
    if not patch.exists():
        return cannot("V04", "缺 fix.patch")
    try:
        proc = subprocess.run(
            ["git", "-C", str(ctx.repo), "apply", "--check", "--whitespace=nowarn",
             str(patch)],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return cannot("V04", f"git apply --check 无法执行：{exc}")
    if proc.returncode != 0:
        return bad("V04", "git apply --check 未通过", proc.stderr.strip()[:800])
    return ok("V04", "git apply --check 通过")


def v05(ctx: Ctx) -> Result:
    patch = ctx.repo / "fix.patch"
    if not patch.exists():
        return cannot("V05", "缺 fix.patch")
    loc, err = load_frontmatter(ctx.repo / "localization.md")
    if err:
        return cannot("V05", err)
    touched = list(patch_map(patch.read_text(encoding="utf-8", errors="replace")))
    if not touched:
        return cannot("V05", "fix.patch 中解析不到 diff --git 行")
    files = loc.get("files")
    if not isinstance(files, list) or not files or not all(nonempty_str(f) for f in files):
        return bad("V05", "localization.md.files 缺失、为空或含非字符串项")
    scope = ctx.get("allowed_scope")
    outside_decl = [p for p in touched if not under_scope(p, files)]
    outside_scope = [p for p in touched if not under_scope(p, scope)]
    problems = []
    if outside_decl:
        problems.append("补丁触及 localization.md 未声明的文件：" + ", ".join(outside_decl))
    if outside_scope:
        problems.append("补丁触及 allowed_scope 之外的文件：" + ", ".join(outside_scope))
    if problems:
        return bad("V05", *problems)
    return ok("V05", f"touched_files={len(touched)}，均在声明范围与 allowed_scope 内")


def v06(ctx: Ctx) -> Result:
    patch = ctx.repo / "fix.patch"
    if not patch.exists():
        return cannot("V06", "缺 fix.patch")
    loc, err = load_frontmatter(ctx.repo / "localization.md")
    if err:
        return cannot("V06", err)
    kind = loc.get("evidence_kind")
    if kind not in ("direct", "indirect", "hypothesis"):
        return bad("V06", f"localization.md.evidence_kind 非法：{kind!r}")

    text = patch.read_text(encoding="utf-8", errors="replace")
    violations: list[str] = []
    for path, lines in patch_map(text).items():
        if not is_test_path(path):
            continue
        for line in lines:
            if line.startswith(("+++", "---")) or not line[:1] in ("+", "-"):
                continue
            if ASSERT_RE.search(line[1:]):
                violations.append(f"{path}: {line[:160]}")
    problems: list[str] = []
    if violations:
        problems.append("测试断言行发生改动：" + " | ".join(violations[:5]))

    banned = ("根因已确认", "彻底修复", "问题已解决")
    if kind == "hypothesis":
        hits = []
        for name in ("repro.md", "localization.md", "fix-report.md", "verify.log"):
            p = ctx.repo / name
            if not p.exists():
                continue
            body = p.read_text(encoding="utf-8", errors="replace")
            for phrase in banned:
                if phrase in body:
                    hits.append(f"{name} 含「{phrase}」")
        report, rerr = load_frontmatter(ctx.repo / "fix-report.md")
        if rerr is None and report.get("status") == "fixed":
            hits.append("fix-report.md.status 在 hypothesis 下写成了 fixed")
        if hits:
            problems.append("hypothesis 下出现冒充措辞：" + "；".join(hits))
    if problems:
        return bad("V06", *problems)
    return ok("V06", f"测试断言行零改动；evidence_kind={kind}")


def v07(ctx: Ctx) -> Result:
    cmd = ctx.get("test_command")
    if not single_line(cmd):
        return cannot("V07", "test_command 未约定或不可执行")
    timeout = ctx.get("repro_timeout_seconds")
    try:
        code, out = run_command(cmd, ctx.repo, timeout)
    except subprocess.TimeoutExpired:
        return cannot("V07", "既有测试运行超时，无法判定")
    except RuntimeError as exc:
        return cannot("V07", f"既有测试无法启动：{exc}")
    if code != 0:
        tail = WS_RE.sub(" ", out).strip()[-800:]
        return bad("V07", f"既有测试退出码={code}", tail)
    return ok("V07", "既有测试全绿（退出码 0）")


def v08(ctx: Ctx) -> Result:
    log_path = ctx.repo / "verify.log"
    if not log_path.exists():
        return cannot("V08", "缺 verify.log")
    try:
        log = yaml.safe_load(log_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return cannot("V08", f"verify.log 不是合法 YAML：{exc}")
    if not isinstance(log, dict):
        return cannot("V08", "verify.log 必须是 mapping")
    repro, err = load_frontmatter(ctx.repo / "repro.md")
    if err:
        return cannot("V08", err)
    repro_cmd = repro.get("command")
    test_cmd = ctx.get("test_command")
    if not single_line(repro_cmd):
        return cannot("V08", "repro.md.command 缺失")
    if not single_line(test_cmd):
        return cannot("V08", "test_command 未约定")

    problems: list[str] = []
    if not nonempty_str(log.get("run_id")):
        problems.append("run_id 缺失或为空")
    if not hexish(log.get("commit")):
        problems.append("commit 缺失或不是 7–40 位十六进制")
    patch = ctx.repo / "fix.patch"
    if not patch.exists():
        return cannot("V08", "缺 fix.patch，无法比对 patch_sha256")
    actual_sha = sha256_file(patch)
    if not isinstance(log.get("patch_sha256"), str) or not re.fullmatch(
        r"[0-9a-f]{64}", log.get("patch_sha256")
    ):
        problems.append("patch_sha256 缺失或不是 64 位小写十六进制")
    elif log["patch_sha256"] != actual_sha:
        problems.append(f"patch_sha256 与 fix.patch 不一致：log={log['patch_sha256']} actual={actual_sha}")

    used = log.get("test_command_used")
    if not single_line(used):
        problems.append("test_command_used 缺失或不是单行")
    elif used != test_cmd:
        problems.append("test_command_used 与约定的 test_command 不逐字一致")

    phases = log.get("phases")
    if not isinstance(phases, list) or len(phases) != 3:
        problems.append("phases 缺失或不是恰好 3 段")
        return bad("V08", *problems)
    expected = [(1, "nonzero"), (2, "zero"), (3, "nonzero")]
    for idx, (want_no, want_kind) in enumerate(expected):
        ph = phases[idx]
        if not isinstance(ph, dict):
            problems.append(f"phases[{idx}] 不是 mapping")
            continue
        if ph.get("phase") != want_no:
            problems.append(f"phases[{idx}].phase 应为 {want_no}，实为 {ph.get('phase')!r}")
        cmd = ph.get("command")
        ec = ph.get("exit_code")
        if not single_line(cmd):
            problems.append(f"phases[{idx}].command 缺失或不是单行")
            cmd = ""
        if not _is_int(ec):
            problems.append(f"phases[{idx}].exit_code 缺失或不是整数")
            continue
        if want_kind == "nonzero" and ec == 0:
            problems.append(f"第 {want_no} 段退出码为 0（期望非 0）")
        if want_kind == "zero" and ec != 0:
            problems.append(f"第 2 段退出码={ec}（期望 0）")
        if not parse_iso(ph.get("started_at")):
            problems.append(f"phases[{idx}].started_at 缺失或不是 ISO-8601")
        if ph.get("duration") is None or ph.get("duration") == "":
            problems.append(f"phases[{idx}].duration 缺失")
        if cmd:
            if repro_cmd not in cmd:
                problems.append(f"第 {want_no} 段命令未包含 repro 命令")
            if want_no == 2 and test_cmd not in cmd:
                problems.append("第 2 段命令未包含全量测试命令")
    if problems:
        return bad("V08", *problems)
    return ok("V08", "三段齐备，退出码序列＝非0／0／非0，sha 与补丁一致")


VALIDATORS = {
    "V01": v01, "V02": v02, "V03": v03, "V04": v04,
    "V05": v05, "V06": v06, "V07": v07, "V08": v08,
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="V01–V08 自动检查（退出码 0／1／3）")
    parser.add_argument("--config", required=True, help="配置快照 YAML 路径")
    parser.add_argument("--only", nargs="*", choices=sorted(VALIDATORS), help="只跑指定项")
    args = parser.parse_args(argv)

    cfg, errors = load_config(Path(args.config).expanduser())
    if errors:
        for line in errors:
            print(f"cannot_evaluate: {line}")
        return CANNOT
    ctx = Ctx(cfg, Path(cfg["repo_path"]).expanduser().resolve())

    selected = args.only or sorted(VALIDATORS)
    results = [VALIDATORS[vid](ctx) for vid in selected]
    for res in results:
        label = {PASS: "pass", FAIL: "fail", CANNOT: "cannot_evaluate"}[res.code]
        print(f"{res.vid} {label}")
        for line in res.lines:
            print(f"  {line}")
    codes = [r.code for r in results]
    if FAIL in codes:
        return FAIL
    if CANNOT in codes:
        return CANNOT
    return PASS


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
