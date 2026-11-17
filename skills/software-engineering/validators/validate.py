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
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import tokenize
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    # 本文件自己要求受控隔离，自己的负向套件也会在 `python3 -I` 下被调用：
    # `-I` 只是忽略 PYTHONPATH／用户 site，并不禁用系统 site-packages。
    # 这里显式补回站点目录（含用户 site，PyYAML 可能装在那里），导入成功后再移除，
    # 不让这些目录继续影响本进程后续的模块解析。
    _added: list[str] = []
    try:
        import site

        for _d in list(site.getsitepackages()) + [site.getusersitepackages()]:
            if _d and os.path.isdir(_d) and _d not in sys.path:
                sys.path.append(_d)
                _added.append(_d)
    except Exception:
        pass
    try:
        import yaml
    except ImportError:
        sys.stderr.write("cannot_evaluate: 缺少 PyYAML\n")
        sys.exit(3)
    for _d in _added:
        while _d in sys.path:
            sys.path.remove(_d)

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

# 快照元数据：不参与「七项缺一即无法判定」，只用于记录约定时间与双方身份。
SNAPSHOT_META_KEYS = ("agreed_at", "agreed_by")


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
    unknown = sorted(set(raw) - set(CONFIG_KEYS) - set(SNAPSHOT_META_KEYS))
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

    agreed_at = raw.get("agreed_at")
    if agreed_at is not None and not _isoish(agreed_at):
        errors.append("agreed_at 已给出但不是 ISO-8601 日期或日期时间")

    agreed_by = raw.get("agreed_by")
    if agreed_by is not None:
        if (
            not isinstance(agreed_by, list)
            or len(agreed_by) != 2
            or not all(nonempty_str(x) for x in agreed_by)
        ):
            errors.append("agreed_by 已给出但必须恰好两项非空身份（部署方与使用方）")

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


# 受控执行引导：在解释器隔离模式下运行声明的测试脚本。
# - `-I`：隔离模式（忽略 PYTHON* 环境变量、不加脚本目录、不加用户 site）；
# - `-S`：跳过 site 初始化，从而不执行 sitecustomize；
# - 引导内只恢复系统 site-packages（不执行 sitecustomize/usercustomize），
#   把仓库根放到 sys.path[0]，工作目录钉在仓库根；
# - trace 模式下用标准库 trace 采集覆盖行：当前线程、测试自己新建的线程
#   （threading.settrace），以及测试自己拉起的子进程（子进程由 SITECUSTOMIZE
#   采集并写独立文件，引导结束时合并）。
# - 覆盖率结果经继承的文件描述符写回（fd 号走环境变量，路径不经 argv），
#   避免测试从 /proc/self/cmdline 读到输出通道。
# 覆盖率工具用标准库实现，不引入新依赖，也不属于新的挂载期能力声明。
BOOTSTRAP = r'''
import json, os, runpy, sys, threading, trace

repo, script, mode = sys.argv[1], sys.argv[2], sys.argv[3]
out_fd = int(os.environ.get("SE_COV_FD", "3"))
boot = sys.argv[0]
os.chdir(repo)
sys.path.insert(0, repo)
# 测试脚本里常见 `unittest.main()`：它按 sys.argv 解析用例名，这里必须去掉引导参数。
sys.argv = [script]
try:
    import site
    for d in site.getsitepackages():
        if os.path.isdir(d):
            site.addsitedir(d)
except Exception:
    pass
# 显式屏蔽：即使仓库根或 site-packages 里有同名模块，也不得被导入。
sys.modules["sitecustomize"] = None
sys.modules["usercustomize"] = None


def main():
    try:
        runpy.run_path(script, run_name="__main__")
        return 0
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        return code if isinstance(code, int) else 1
    except BaseException:
        # 未捕获异常必须留下输出，否则 V02 无法区分「静默失败」与「真的失败」。
        # 引导自身路径每次都在新的临时目录里，写进输出会让指纹不稳定。
        import traceback
        sys.stderr.write(traceback.format_exc().replace(boot, "<bootstrap>"))
        return 1


def _rel(fn):
    try:
        rel = os.path.relpath(os.path.realpath(fn), repo)
    except ValueError:
        return None
    if rel.startswith(".."):
        return None
    return rel.replace(os.sep, "/")


def _dump(exit_code, tracer=None):
    covered = {}
    if tracer is not None:
        for (fn, lineno), _count in tracer.results().counts.items():
            rel = _rel(fn)
            if rel is not None:
                covered.setdefault(rel, []).append(lineno)
    # 合并子进程覆盖率：由 SITECUSTOMIZE 写在 SE_COV_DIR/cov-<pid>.json。
    child_dir = os.environ.get("SE_COV_DIR")
    if child_dir and os.path.isdir(child_dir):
        for name in sorted(os.listdir(child_dir)):
            if not (name.startswith("cov-") and name.endswith(".json")):
                continue
            try:
                with open(os.path.join(child_dir, name), encoding="utf-8") as fh:
                    doc = json.load(fh)
            except (OSError, ValueError):
                continue
            for path, lines in (doc.get("covered") or {}).items():
                if isinstance(path, str) and isinstance(lines, list):
                    covered.setdefault(path, []).extend(
                        x for x in lines if isinstance(x, int)
                    )
    payload = {"exit": exit_code,
               "covered": {k: sorted(set(v)) for k, v in covered.items()}}
    with os.fdopen(out_fd, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)


if mode == "plain":
    _dump(main())
    sys.exit(0)

tracer = trace.Trace(count=True, trace=False,
                     ignoredirs=[sys.prefix, sys.exec_prefix])
# 当前线程之外，测试自己新建的线程也要采（threading.settrace 只对之后创建的线程生效）。
threading.settrace(tracer.globaltrace)
code = 0
try:
    code = tracer.runfunc(main)
except BaseException:
    code = 1
_dump(code, tracer)
sys.exit(0)
'''

# 子进程覆盖率注入点：测试自己拉起的子进程若不是 `-I`／`-S`，启动时会经
# PYTHONPATH 导入本文件。它只写覆盖率，不改变被测行为。
SITECUSTOMIZE = r'''
import atexit, json, os, sys, threading, trace

_repo = os.environ.get("SE_COV_REPO", "")
_out_dir = os.environ.get("SE_COV_DIR", "")
if _repo and _out_dir and not os.environ.get("SE_COV_ACTIVE"):
    os.environ["SE_COV_ACTIVE"] = "1"
    _tracer = trace.Trace(count=True, trace=False,
                          ignoredirs=[sys.prefix, sys.exec_prefix])

    def _dump():
        sys.settrace(None)
        threading.settrace(None)
        covered = {}
        for (fn, lineno), _count in _tracer.results().counts.items():
            try:
                rel = os.path.relpath(os.path.realpath(fn), _repo)
            except ValueError:
                continue
            if rel.startswith(".."):
                continue
            covered.setdefault(rel.replace(os.sep, "/"), []).append(lineno)
        path = os.path.join(_out_dir, "cov-%d.json" % os.getpid())
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"pid": os.getpid(),
                           "covered": {k: sorted(set(v))
                                       for k, v in covered.items()}}, fh)
        except OSError:
            pass

    atexit.register(_dump)
    threading.settrace(_tracer.globaltrace)
    sys.settrace(_tracer.globaltrace)
'''


def parse_isolated_command(cmd, repo: Path) -> tuple[Path | None, str | None]:
    """只接受 `python3 -I <仓内相对路径>`；返回 (脚本绝对路径, 问题描述)。"""
    if not isinstance(cmd, str) or not cmd.strip():
        return None, "命令为空"
    if "\n" in cmd or "\r" in cmd:
        return None, "命令含换行"
    try:
        tokens = shlex.split(cmd)
    except ValueError:
        return None, "命令无法按 shell 规则切分"
    if len(tokens) != 3:
        return None, (
            "只允许 `python3 -I <仓内相对路径>`（恰好三个词；"
            "不接参数、不接 -m/-c、不使用 bash/env/赋值前缀）"
        )
    if tokens[0] != "python3":
        return None, "解释器只允许字面量 `python3`（不接 ./、版本后缀或其它别名）"
    if tokens[1] != "-I":
        return None, "解释器必须带 -I（隔离模式）"
    raw = tokens[2]
    rel = Path(raw)
    if rel.is_absolute():
        return None, "路径必须是仓内相对路径，不接受绝对路径"
    if ".." in rel.parts:
        return None, "路径含 ..，可能指向仓外"
    try:
        real = (repo / rel).resolve(strict=True)
    except OSError:
        return None, f"测试文件不存在：{raw}"
    root = repo.resolve()
    if real != root and root not in real.parents:
        return None, "路径解析后落在仓库之外（含软链指向仓外）"
    if not real.is_file():
        return None, "路径不是文件"
    return real, None


def _clean_env() -> dict:
    """清空所有 PYTHON* 环境变量（PYTHONPATH／PYTHONSTARTUP／PYTHONHOME 等）。"""
    return {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}


def _exec_isolated(repo: Path, script: Path, timeout: int, trace_mode: bool):
    """在隔离引导下执行脚本；返回 (退出码, 输出, 覆盖行或 None)。

    覆盖率结果经继承的 fd 写回，输出路径不进 argv；子进程覆盖率目录走
    SE_COV_DIR（只含 sitecustomize.py 的临时目录同时作为 PYTHONPATH）。
    """
    with tempfile.TemporaryDirectory(prefix="validate-iso-") as tmpdir:
        # 源码 mtime 的秒级精度不足以让 Python 失效旧 pyc；补丁前后文件大小相同
        # 时尤其会读到 baseline 的字节码。执行前统一清掉缓存，保证跑的是当前源码。
        _clear_pycache(repo)
        tmp = Path(tmpdir)
        boot = tmp / "bootstrap.py"
        boot.write_text(BOOTSTRAP, encoding="utf-8")
        out = tmp / "coverage.json"
        env = _clean_env()
        env["SE_COV_REPO"] = str(repo)
        if trace_mode:
            child_cov = tmp / "child-cov"
            child_cov.mkdir()
            (tmp / "sitecustomize.py").write_text(SITECUSTOMIZE, encoding="utf-8")
            env["PYTHONPATH"] = str(tmp)
            env["SE_COV_DIR"] = str(child_cov)
        argv = [sys.executable or "python3", "-I", "-S", "-B", str(boot),
                str(repo), str(script), "trace" if trace_mode else "plain"]
        with out.open("w", encoding="utf-8") as out_fh:
            env["SE_COV_FD"] = str(out_fh.fileno())
            try:
                proc = subprocess.run(
                    argv, cwd=str(repo), env=env,
                    pass_fds=(out_fh.fileno(),),
                    capture_output=True, text=True, timeout=timeout,
                )
            except subprocess.TimeoutExpired:
                raise
            except OSError as exc:
                raise RuntimeError(str(exc))
        text = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0 or not out.exists():
            raise RuntimeError(
                "受控执行引导异常退出（退出码="
                f"{proc.returncode}）：" + text.strip()[-500:]
            )
        try:
            covered = json.loads(out.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"受控执行结果不可读：{exc}")
        code = covered.get("exit")
        if not isinstance(code, int):
            raise RuntimeError("受控执行结果缺退出码")
        return code, text, (covered if trace_mode else None)


def run_command(cmd: str, cwd: Path, timeout: int) -> tuple[int, str]:
    """按白名单形式解释并受控执行命令（非 trace 模式）。"""
    script, problem = parse_isolated_command(cmd, cwd)
    if problem:
        raise RuntimeError(problem)
    code, text, _covered = _exec_isolated(cwd, script, timeout, trace_mode=False)
    return code, text


def run_traced_command(cmd: str, repo: Path, timeout: int):
    """受控执行并采集覆盖行；返回 (退出码, 输出, covered)。"""
    script, problem = parse_isolated_command(cmd, repo)
    if problem:
        raise RuntimeError(problem)
    return _exec_isolated(repo, script, timeout, trace_mode=True)


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


def _isoish(v) -> bool:
    """YAML 会把裸日期解析成 date/datetime，这里一并接受。"""
    if isinstance(v, (date, datetime)):
        return True
    return parse_iso(v)


def load_repro_meta(repo: Path) -> tuple[dict | None, str | None]:
    """读取唯一的 tests/repro_*.meta.yaml。"""
    metas = sorted((repo / "tests").glob("repro_*.meta.yaml"))
    if not metas:
        return None, "缺 tests/repro_*.meta.yaml"
    if len(metas) > 1:
        return None, "tests/ 下有多份 repro_*.meta.yaml，无法判定是哪一件"
    try:
        meta = yaml.safe_load(metas[0].read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, f"{metas[0].name} 不是合法 YAML：{exc}"
    if not isinstance(meta, dict):
        return None, f"{metas[0].name} 必须是 mapping"
    return meta, None


def repo_relative_test_path(raw, repo: Path) -> tuple[Path | None, str | None]:
    """测试文件必须是仓内 tests/ 下的相对路径；返回 (解析后的真实路径, 问题)。"""
    if not nonempty_str(raw):
        return None, "file 缺失或为空"
    p = Path(raw)
    if p.is_absolute():
        return None, "file 必须是仓内相对路径，不接受绝对路径"
    if ".." in p.parts:
        return None, "file 含 ..，可能指向仓外"
    if not p.parts or p.parts[0].lower().lstrip(".") != "tests":
        return None, "file 必须位于仓内 tests/ 下"
    try:
        real = (repo / p).resolve(strict=True)
    except OSError:
        return None, "file 指向的文件不存在"
    root = repo.resolve()
    if real != root and root not in real.parents:
        return None, "file 解析后落在仓库之外（含软链指向仓外）"
    if not real.is_file():
        return None, "file 指向的不是文件"
    return real, None


# 可识别的恒真／常量断言：只覆盖固定写法，语义上的「恒真」判不了。
TRIVIAL_ASSERTIONS = (
    re.compile(r"\bassert\s+(True|1)\s*$"),
    re.compile(r"\bassert\s+not\s+(False|0)\s*$"),
    re.compile(r"\bassertTrue\(\s*(True|1|true)\s*\)"),
    re.compile(r"\bassertEqual\(\s*([0-9]+)\s*,\s*\1\s*\)"),
)


def code_only_lines(source: str) -> list[str]:
    """去掉注释与字符串字面量后的代码行。

    `# assert ...` 与 `"assert ..."` 都不是断言；只保留 NAME／OP 记号，
    这样文本匹配不会被注释或字符串骗过。tokenize 失败时退化为逐行去 # 注释。
    """
    spans: dict[int, list[tuple[int, str]]] = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type in (tokenize.NAME, tokenize.OP, tokenize.NUMBER):
                spans.setdefault(tok.start[0], []).append((tok.start[1], tok.string))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return [line.split("#", 1)[0] for line in source.splitlines()]
    out = []
    for i in range(1, len(source.splitlines()) + 1):
        out.append(" ".join(s for _, s in sorted(spans.get(i, []))))
    return out


def has_nontrivial_assertion(body: str) -> bool:
    """测试文件里至少有一行代码（不含注释与字符串）不是可识别的恒真断言。"""
    candidates = [
        line for line in code_only_lines(body)
        if ASSERT_RE.search(line) or re.search(r"\bassert\b", line)
    ]
    if not candidates:
        return False
    return any(
        not any(pattern.search(line) for pattern in TRIVIAL_ASSERTIONS)
        for line in candidates
    )


def diff_line_count(text: str) -> int:
    """统计补丁中实际增删的行数（不含 +++/--- 文件头）。"""
    n = 0
    for line in text.splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line[:1] in ("+", "-"):
            n += 1
    return n


def git(repo: Path, *args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, timeout=timeout,
    )


def patch_entries(text: str) -> list[dict]:
    """解析补丁为逐文件条目：保留 a 侧与 b 侧路径（改名时两者不同）。"""
    entries: list[dict] = []
    cur: dict | None = None
    for line in text.splitlines():
        m = re.match(r"^diff --git a/(.+?) b/(.+)$", line)
        if m:
            cur = {"a": m.group(1), "b": m.group(2), "lines": []}
            entries.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^rename from (.+)$", line)
        if m:
            cur["a"] = m.group(1)
            continue
        m = re.match(r"^rename to (.+)$", line)
        if m:
            cur["b"] = m.group(1)
            continue
        cur["lines"].append(line)
    return entries


def patch_map(text: str) -> dict[str, list[str]]:
    """b 侧路径 → 行；仅用于「补丁触及了哪些文件」。"""
    return {entry["b"]: entry["lines"] for entry in patch_entries(text)}


def production_patch_regions(text: str) -> tuple[dict[str, set[int]], dict[str, set[int]]]:
    """生产代码被补丁改动的行：返回 (base 侧, patched 侧) 的路径→行号集合。

    base 侧取被删除的 a 文件行号，patched 侧取被新增的 b 文件行号；
    改名时两侧路径各自生效。测试路径与上下文行不计入。
    """
    base: dict[str, set[int]] = {}
    patched: dict[str, set[int]] = {}
    for entry in patch_entries(text):
        a_path, b_path = entry["a"], entry["b"]
        a_test, b_test = is_test_path(a_path), is_test_path(b_path)
        a_lines: set[int] = set()
        b_lines: set[int] = set()
        a_cur = b_cur = None
        for line in entry["lines"]:
            m = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if m:
                a_cur, b_cur = int(m.group(1)), int(m.group(2))
                continue
            if a_cur is None:
                continue
            if line.startswith("+"):
                if not b_test:
                    b_lines.add(b_cur)
                b_cur += 1
            elif line.startswith("-"):
                if not a_test:
                    a_lines.add(a_cur)
                a_cur += 1
            elif line.startswith(" ") or line == "":
                a_cur += 1
                b_cur += 1
        if a_lines:
            base.setdefault(a_path, set()).update(a_lines)
        if b_lines:
            patched.setdefault(b_path, set()).update(b_lines)
    return base, patched


def under_scope(path: str, scope: list[str]) -> bool:
    for entry in scope:
        e = entry.rstrip("/")
        if path == e or path.startswith(e + "/"):
            return True
    return False


def is_test_path(path: str) -> bool:
    parts = path.split("/")
    name = parts[-1]
    dirs = [p.lower().lstrip(".") for p in parts[:-1]]
    if any(p in ("tests", "test", "__tests__") for p in dirs):
        return True
    return bool(re.match(
        r"^(test_.*|.*_test\.[^.]+|.*\.test\.[^.]+|.*\.spec\.[^.]+)$", name.lower()
    ))


# ---------------------------------------------------------------- 变异检验

MUTATION_OP_SWAPS = {
    "==": "!=", "!=": "==", "<=": "<", ">=": ">", "<": "<=", ">": ">=",
    "+": "-", "-": "+", "*": "/", "/": "*",
}
MUTATION_NAME_SWAPS = {"and": "or", "or": "and", "True": "False", "False": "True"}


def mutation_candidates(line: str) -> list[str]:
    """对一行代码造文本变异：翻转比较符、换运算符、常量 ±1、布尔取反。

    只替换 NAME／OP／NUMBER 记号，注释与字符串天然不参与（不产生变异）。
    一行无法 tokenize（如续行）时返回空，由调用方按「该行不可敏化」处理。
    """
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(line + "\n").readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return []
    out: list[str] = []
    for tok in toks:
        replacement = None
        if tok.type == tokenize.OP and tok.string in MUTATION_OP_SWAPS:
            replacement = MUTATION_OP_SWAPS[tok.string]
        elif tok.type == tokenize.NAME and tok.string in MUTATION_NAME_SWAPS:
            replacement = MUTATION_NAME_SWAPS[tok.string]
        elif tok.type == tokenize.NUMBER and re.fullmatch(r"\d+", tok.string):
            replacement = str(int(tok.string) + 1)
        if replacement is None or tok.end[0] != 1:
            continue
        out.append(line[:tok.start[1]] + replacement + line[tok.end[1]:])
    # 去重并保序；同一行不需要无限多个变异。
    seen, uniq = set(), []
    for cand in out:
        if cand not in seen:
            seen.add(cand)
            uniq.append(cand)
    return uniq[:8]


def patch_mutation_targets(text: str) -> list[dict]:
    """补丁触及的生产代码行：新增行逐行变异，改动块整块回退作删除行变异。"""
    targets: list[dict] = []
    for entry in patch_entries(text):
        a_path, b_path = entry["a"], entry["b"]
        if is_test_path(a_path) or is_test_path(b_path):
            continue
        a_cur = b_cur = None
        added: list[tuple[int, str]] = []
        blocks: list[dict] = []
        cur: dict | None = None
        for line in entry["lines"]:
            m = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if m:
                a_cur, b_cur = int(m.group(1)), int(m.group(2))
                cur = {"insert": None, "deleted": [], "added": []}
                blocks.append(cur)
                continue
            if a_cur is None:
                continue
            if line.startswith("+"):
                added.append((b_cur, line[1:]))
                if cur is not None:
                    if cur["insert"] is None:
                        cur["insert"] = b_cur - 1
                    cur["added"].append(line[1:])
                b_cur += 1
            elif line.startswith("-"):
                if cur is not None and cur["insert"] is None:
                    cur["insert"] = b_cur - 1
                if cur is not None:
                    cur["deleted"].append(line[1:])
                a_cur += 1
            elif line.startswith(" ") or line == "":
                a_cur += 1
                b_cur += 1
        revert = [
            (b["insert"], b["deleted"], b["added"])
            for b in blocks
            if b["insert"] is not None and (b["deleted"] or b["added"])
        ]
        if added or revert:
            targets.append({"path": b_path, "added": added, "revert": revert})
    return targets


def _clear_pycache(repo: Path) -> None:
    for cache in repo.rglob("__pycache__"):
        if ".git" in cache.parts:
            continue
        for child in cache.iterdir():
            try:
                child.unlink()
            except OSError:
                pass
        try:
            cache.rmdir()
        except OSError:
            pass


def _compiles(source: str, path: Path) -> bool:
    if path.suffix != ".py":
        return True
    try:
        compile(source, str(path), "exec")
    except (SyntaxError, ValueError):
        return False
    return True


def _replaced_line(lines: list[str], index: int, replacement: str) -> list[str]:
    old = lines[index]
    ending = old[len(old.rstrip("\r\n")):]
    return lines[:index] + [replacement + ending] + lines[index + 1:]


def _reverted_block(lines: list[str], insert: int, deleted: list[str],
                    added: list[str]) -> list[str] | None:
    if insert is None:
        return None
    if insert < 0 or insert > len(lines):
        return None
    end = insert + len(added)
    current = [line.rstrip("\r\n") for line in lines[insert:end]]
    if current != added:
        return None
    restored = [d + "\n" for d in deleted]
    return lines[:insert] + restored + lines[end:]


def _mutant_killed(repo: Path, cmd: str, timeout: int) -> bool:
    _clear_pycache(repo)
    try:
        code, _out = run_command(cmd, repo, timeout)
    except (subprocess.TimeoutExpired, RuntimeError):
        return False
    return code != 0


def run_mutation_checks(repo: Path, cmd: str, timeout: int, patch_text: str) -> list[str]:
    """在 patched 态逐行造变异并重跑复现测试；测试必须变红。

    返回失败理由列表；空列表表示补丁触及的生产代码行都被测试敏感覆盖。
    纯新增补丁没有 base 侧删除行，但每个新增行仍要过这一关。
    """
    targets = patch_mutation_targets(patch_text)
    if not targets:
        return ["补丁未在生产代码上触碰任何行，无法造出变异"]
    failures: list[str] = []
    for target in targets:
        path = repo / target["path"]
        if not path.is_file():
            failures.append(f'{target["path"]}：补丁应用后文件不存在，无法造变异')
            continue
        original = path.read_text(encoding="utf-8", errors="surrogateescape")
        lines = original.splitlines(keepends=True)
        try:
            for lineno, text in target["added"]:
                if not 1 <= lineno <= len(lines):
                    failures.append(f'{target["path"]}:{lineno} 越界，无法造变异')
                    continue
                candidates = mutation_candidates(text)
                if not candidates:
                    continue
                killed = False
                for candidate in candidates:
                    mutated = _replaced_line(lines, lineno - 1, candidate)
                    source = "".join(mutated)
                    if not _compiles(source, path):
                        continue
                    path.write_text(source, encoding="utf-8")
                    if _mutant_killed(repo, cmd, timeout):
                        killed = True
                        break
                path.write_text(original, encoding="utf-8")
                if not killed:
                    failures.append(
                        f'{target["path"]}:{lineno} 的变异均未使复现测试变红'
                        "（补丁行未被测试敏感覆盖）"
                    )
            for insert, deleted, added in target["revert"]:
                mutated = _reverted_block(lines, insert, deleted, added)
                if mutated is None:
                    failures.append(f'{target["path"]} 无法定位删除块，不能造回退变异')
                    continue
                source = "".join(mutated)
                if not _compiles(source, path):
                    failures.append(
                        f'{target["path"]} 的回退变异不可编译，无法判定删除行敏感性'
                    )
                    continue
                path.write_text(source, encoding="utf-8")
                if not _mutant_killed(repo, cmd, timeout):
                    failures.append(
                        f'{target["path"]} 的删除行被回退后复现测试仍通过'
                        "（补丁行未被测试敏感覆盖）"
                    )
        finally:
            path.write_text(original, encoding="utf-8")
    return failures


ASSERT_RE = re.compile(
    r"\b(assert(?:ionerror)?|expect|should|require|assertEqual|assertRaises|pytest\.raises|"
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
    if not _isoish(data.get("first_observed")):
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
    meta, merr = load_repro_meta(ctx.repo)
    if merr:
        return cannot("V02", merr)
    test_real, ferr = repo_relative_test_path(meta.get("file"), ctx.repo)
    if ferr:
        return bad("V02", "repro 元数据的 file 不合格：" + ferr)
    script, cmd_problem = parse_isolated_command(cmd, ctx.repo)
    if cmd_problem:
        return bad("V02", "复现命令只允许 `python3 -I <仓内相对路径>`：" + cmd_problem)
    if script != test_real:
        return bad(
            "V02",
            "复现命令执行的脚本与 repro 元数据的 file 不一致",
            f"命令={script.relative_to(ctx.repo.resolve()).as_posix()}",
            f"file={meta.get('file')}",
        )
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
        if not out.strip():
            return bad(
                "V02",
                f"第 {i + 1} 次运行输出为空；空输出无法构成失败证据，"
                "且空输出摘要恒为同一值",
            )
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
    meta, merr = load_repro_meta(ctx.repo)
    if merr:
        return cannot("V03", merr)
    problems: list[str] = []
    test_real, ferr = repo_relative_test_path(meta.get("file"), ctx.repo)
    if ferr:
        problems.append(ferr)
    elif test_real.stat().st_size == 0:
        problems.append("失败测试文件为空")
    else:
        body = test_real.read_text(encoding="utf-8", errors="replace")
        if not has_nontrivial_assertion(body):
            problems.append(
                "失败测试文件没有可判定的非恒真断言"
                "（只有 assertTrue(True) 这类常量断言也算不合格）"
            )
    if not nonempty_str(meta.get("test_id")):
        problems.append("test_id 缺失或为空")
    single = meta.get("single_run_command")
    if not single_line(single):
        problems.append("single_run_command 缺失或不是单行")
    else:
        script, cmd_problem = parse_isolated_command(single, ctx.repo)
        if cmd_problem:
            problems.append(
                "single_run_command 只允许 `python3 -I <仓内相对路径>`：" + cmd_problem
            )
        elif test_real is not None and script != test_real:
            problems.append(
                "single_run_command 执行的脚本与 file 不一致，"
                "无法确认它真的在执行该失败测试"
            )
    if not hexish(meta.get("base_commit")):
        problems.append("base_commit 不是 7–40 位十六进制")
    if not nonempty_str(meta.get("expected_failure")):
        problems.append("expected_failure 缺失或为空")
    if problems:
        return bad("V03", *problems)
    try:
        head = git(ctx.repo, "rev-parse", "HEAD", timeout=30)
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
    problems: list[str] = []

    est_files = loc.get("estimated_touched_files")
    est_lines = loc.get("estimated_diff_lines")
    actual_files = len(patch_map(text))
    actual_lines = diff_line_count(text)
    if not _is_int(est_files) or est_files < 0:
        problems.append(
            "localization.md.estimated_touched_files 缺失或不是非负整数，无法做最小性对照"
        )
    elif est_files != actual_files:
        problems.append(
            f"最小性对照不一致：预估触及 {est_files} 个文件，实际 {actual_files} 个"
            "（不一致时 evidence_kind 只能按 hypothesis 重写）"
        )
    if not _is_int(est_lines) or est_lines < 0:
        problems.append(
            "localization.md.estimated_diff_lines 缺失或不是非负整数，无法做最小性对照"
        )
    elif est_lines != actual_lines:
        problems.append(
            f"最小性对照不一致：预估改动 {est_lines} 行，实际 {actual_lines} 行"
            "（不一致时 evidence_kind 只能按 hypothesis 重写）"
        )

    violations: list[str] = []
    for entry in patch_entries(text):
        old, new, lines = entry["a"], entry["b"], entry["lines"]
        old_test, new_test = is_test_path(old), is_test_path(new)
        is_new = any(
            line.startswith("--- /dev/null") or line.startswith("new file mode")
            for line in lines
        )
        changed = [
            line for line in lines
            if line[:1] in ("+", "-") and not line.startswith(("+++", "---"))
        ]
        if new_test:
            if is_new:
                if not re.search(r"(^|/)repro_[^/]+$", new):
                    violations.append(f"{new}: 新增测试文件不是 repro_*")
            elif old != new:
                violations.append(f"{old} -> {new}: 测试路径文件被改名或移动")
            elif changed:
                violations.append(
                    f"{new}: 测试目录下已有文件被改写 {len(changed)} 行"
                    "（断言、测试数据、夹具一律不改）"
                )
        elif old_test and old != new:
            violations.append(f"{old} -> {new}: 测试路径文件被移出 tests 区域")
    if violations:
        problems.append("测试路径改动违规：" + " | ".join(violations[:5]))
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
    return ok("V06", f"补丁未改写测试路径已有文件（含改名与测试数据）；最小性对照一致；evidence_kind={kind}")


def v07(ctx: Ctx) -> Result:
    cmd = ctx.get("test_command")
    if not single_line(cmd):
        return cannot("V07", "test_command 未约定或不可执行")
    script, problem = parse_isolated_command(cmd, ctx.repo)
    if problem:
        return bad("V07", "test_command 只允许 `python3 -I <仓内相对路径>`：" + problem)
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
    _rs, rp = parse_isolated_command(repro_cmd, ctx.repo)
    if rp:
        return bad("V08", "repro.md.command 非法：" + rp)
    _ts, tp = parse_isolated_command(test_cmd, ctx.repo)
    if tp:
        return bad("V08", "test_command 非法：" + tp)

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
        if not _isoish(ph.get("started_at")):
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

    # 以下不采信日志自述：核对 HEAD、工作区，并实际重跑三段。
    try:
        head = git(ctx.repo, "rev-parse", "HEAD", timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        return cannot("V08", f"git rev-parse 失败：{exc}")
    if head.returncode != 0:
        return cannot("V08", f"git rev-parse 失败：{head.stderr.strip()}")
    head_sha = head.stdout.strip()
    if str(log["commit"]).lower() != head_sha.lower():
        return bad(
            "V08",
            "verify.log.commit 与当前 HEAD 不一致",
            f"log={log['commit']}",
            f"HEAD={head_sha}",
        )

    try:
        dirty = git(ctx.repo, "status", "--porcelain", "--untracked-files=no", timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        return cannot("V08", f"git status 失败：{exc}")
    if dirty.returncode != 0:
        return cannot("V08", f"git status 失败：{dirty.stderr.strip()}")
    if dirty.stdout.strip():
        return bad(
            "V08",
            "工作区有未提交的已跟踪文件改动，无法确认验证日志对应干净检出",
            dirty.stdout.strip()[:800],
        )

    try:
        can_apply = git(
            ctx.repo, "apply", "--check", "--whitespace=nowarn", "fix.patch", timeout=120
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return cannot("V08", f"git apply --check 失败：{exc}")
    if can_apply.returncode != 0:
        return bad(
            "V08",
            "fix.patch 当前无法干净应用（可能已被应用），无法重跑第①段",
            can_apply.stderr.strip()[:400],
        )

    timeout = ctx.get("repro_timeout_seconds")
    patch_text = patch.read_text(encoding="utf-8", errors="replace")

    def rerun_traced(label: str, command: str):
        try:
            return run_traced_command(command, ctx.repo, timeout)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"{label}重跑超时，无法判定")
        except RuntimeError as exc:
            raise RuntimeError(f"{label}重跑无法执行：{exc}")

    def rerun_plain(label: str, command: str) -> int:
        try:
            code, _out = run_command(command, ctx.repo, timeout)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"{label}重跑超时，无法判定")
        except RuntimeError as exc:
            raise RuntimeError(f"{label}重跑无法执行：{exc}")
        return code

    # 第①段：补丁未应用，单独重跑复现命令（同时采集 base 覆盖行），应失败
    try:
        c1, _o1, cov_base = rerun_traced("第①段", repro_cmd)
    except RuntimeError as exc:
        return cannot("V08", str(exc))
    if c1 == 0:
        return bad("V08", "第①段重跑退出码为 0（期望非 0）")
    if c1 != phases[0]["exit_code"]:
        return bad(
            "V08",
            "第①段重跑退出码与日志不一致",
            f"重跑={c1}",
            f"日志={phases[0]['exit_code']}",
        )

    # 第②段：应用补丁后，复现命令与测试命令分别重跑，各自必须为 0
    try:
        applied = git(
            ctx.repo, "apply", "--whitespace=nowarn", "fix.patch", timeout=120
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return cannot("V08", f"重跑时应用 fix.patch 失败：{exc}")
    if applied.returncode != 0:
        return cannot("V08", "重跑时无法应用 fix.patch：" + applied.stderr.strip()[:400])
    try:
        try:
            c2_repro, _o2, cov_patched = rerun_traced("第②段-复现", repro_cmd)
        except RuntimeError as exc:
            return cannot("V08", str(exc))
        if c2_repro != 0:
            return bad(
                "V08",
                f"第②段单独重跑复现命令退出码={c2_repro}（期望 0）；"
                "整条命令为 0 不能代替复现转绿",
            )
        # 覆盖率：补丁触及的生产代码行，必须在 base 与 patched 两态都被该测试执行到。
        base_regions, patched_regions = production_patch_regions(patch_text)
        if not base_regions and not patched_regions:
            return bad(
                "V08",
                "补丁未在生产代码上触碰任何行，无法证明修复与复现测试相关",
            )
        base_cov = {k: set(v) for k, v in ((cov_base or {}).get("covered") or {}).items()}
        patched_cov = {
            k: set(v) for k, v in ((cov_patched or {}).get("covered") or {}).items()
        }
        gaps: list[str] = []
        for path, lines in base_regions.items():
            if not (lines & base_cov.get(path, set())):
                gaps.append(f"{path}（base）")
        for path, lines in patched_regions.items():
            if not (lines & patched_cov.get(path, set())):
                gaps.append(f"{path}（patched）")
        if gaps:
            return bad(
                "V08",
                "补丁行未被复现测试覆盖，无法证明该测试与修复相关："
                + "、".join(gaps[:5]),
            )
        try:
            c2_tests = rerun_plain("第②段-全量测试", test_cmd)
        except RuntimeError as exc:
            return cannot("V08", str(exc))
        if c2_tests != 0:
            return bad("V08", f"第②段重跑测试命令退出码={c2_tests}（期望 0）")
        if phases[1]["exit_code"] != 0:
            return bad("V08", "verify.log 第②段记录的退出码不是 0")

        # 变异检验：补丁触及的每一行生产代码都要能造出让测试变红的变异。
        # 纯新增补丁的 base 侧为空，但新增行同样要过这一关，不再有「只查 patched」的缺口。
        try:
            mutation_failures = run_mutation_checks(
                ctx.repo, repro_cmd, ctx.timeout, patch_text
            )
        except (OSError, RuntimeError) as exc:
            return cannot("V08", f"变异检验无法执行：{exc}")
        if mutation_failures:
            return bad(
                "V08",
                "变异检验未通过：补丁行未被测试敏感覆盖",
                *mutation_failures[:5],
            )
    finally:
        try:
            reverted = git(
                ctx.repo, "apply", "-R", "--whitespace=nowarn", "fix.patch", timeout=120
            )
        except (OSError, subprocess.SubprocessError):
            reverted = None
    if reverted is None or reverted.returncode != 0:
        return cannot("V08", "重跑后撤销 fix.patch 失败，工作区可能已污染")

    # 第③段：撤补丁后单独重跑复现命令，应再次失败
    try:
        c3 = rerun_plain("第③段", repro_cmd)
    except RuntimeError as exc:
        return cannot("V08", str(exc))
    if c3 == 0:
        return bad("V08", "第③段重跑退出码为 0（撤补丁后仍未复败）")
    if c3 != phases[2]["exit_code"]:
        return bad(
            "V08",
            "第③段重跑退出码与日志不一致",
            f"重跑={c3}",
            f"日志={phases[2]['exit_code']}",
        )

    # V09 必须人工执行：自动检查不采信任何字段自证「已复核」。
    report, rerr = load_frontmatter(ctx.repo / "fix-report.md")
    if rerr:
        return bad("V08", "缺 fix-report.md 或格式不合法：" + rerr)
    status = report.get("status")
    if status not in ("fixed", "fixed_unverified_root_cause", "not_fixed"):
        return bad("V08", f"fix-report.md.status 非法：{status!r}")
    if status == "fixed":
        return bad(
            "V08",
            "status=fixed 不在自动判定范围：V09 必须由人执行，"
            "v09_signoff 等仓内字段可由执行方书写，不能作为复核成立的证据；"
            "自动检查阶段请保持 fixed_unverified_root_cause",
        )

    return ok(
        "V08",
        "三段已实际重跑（非0／0／非0）；覆盖交集非空；变异检验通过；"
        "commit 与 HEAD 一致；工作区无已跟踪改动；sha 与补丁一致；"
        "V09 未自动判定（必须人工执行）",
    )


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
