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
import ast
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


class IntegrityViolation(RuntimeError):
    """运行时完整性校验失败：导入期改写了断言设施或采集入口，执行证据不可信。"""


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
# - 运行时完整性：在导入任何仓内代码之前对断言设施、内置执行入口、trace
#   与采集入口、sys.modules 基线留可信原件；执行完毕再比对。被替换／删除即
#   上报「断言设施在导入期被改写」，校验器据此判 cannot_evaluate。不依赖
#   触发方式（元类、描述符、cached_property、装饰器、新模块都一样）。
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

# ---- 运行时完整性：导入任何仓内代码之前留可信原件 ----
# 断言设施、内置执行入口、trace 与采集入口、sys.modules 基线。
_ASSERT_FAMILY = (
    "assertEqual", "assertNotEqual", "assertTrue", "assertFalse",
    "assertIs", "assertIsNot", "assertIsNone", "assertIsNotNone",
    "assertIn", "assertNotIn", "assertIsInstance", "assertNotIsInstance",
    "assertRaises", "assertRaisesRegex", "assertWarns", "assertWarnsRegex",
    "assertRegex", "assertNotRegex", "assertAlmostEqual",
    "assertNotAlmostEqual", "assertGreater", "assertGreaterEqual",
    "assertLess", "assertLessEqual", "assertCountEqual",
    "assertMultiLineEqual", "assertListEqual", "assertTupleEqual",
    "assertDictEqual", "assertSetEqual", "assertLogs", "assertNoLogs",
    "fail", "subTest",
)
_GUARD_BUILTINS = (
    "__import__", "eval", "exec", "compile", "open", "AssertionError",
)


def _integrity_snapshot():
    import builtins, unittest
    snap = []
    tc = unittest.TestCase
    for name in _ASSERT_FAMILY:
        snap.append(("unittest.TestCase." + name, tc, name, getattr(tc, name, None)))
    for name in _GUARD_BUILTINS:
        snap.append(("builtins." + name, builtins, name, getattr(builtins, name, None)))
    snap.append(("trace.Trace", trace, "Trace", trace.Trace))
    for name in ("runfunc", "globaltrace"):
        snap.append(("trace.Trace." + name, trace.Trace, name,
                     getattr(trace.Trace, name, None)))
    snap.append(("threading.settrace", threading, "settrace", threading.settrace))
    snap.append(("sys.settrace", sys, "settrace", sys.settrace))
    snap.append(("runpy.run_path", runpy, "run_path", runpy.run_path))
    modules = [
        (name, mod) for name, mod in sys.modules.items()
        if name not in ("__main__", "__mp_main__")
    ]
    return snap, modules


def _integrity_violations(snap, modules):
    out = []
    for label, parent, attr, original in snap:
        if getattr(parent, attr, None) is not original:
            out.append(label + " 被替换或删除")
    for name, mod in modules:
        if sys.modules.get(name) is not mod:
            out.append("sys.modules[%r] 被替换或删除" % name)
    return out


_INTEGRITY_SNAP, _INTEGRITY_MODULES = _integrity_snapshot()


failure = {"error": None}


def main():
    try:
        runpy.run_path(script, run_name="__main__")
        return 0
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        if not isinstance(code, int):
            # `sys.exit("msg")` 是提前退出，不是断言失败；记下类型供变异判据区分。
            failure["error"] = "SystemExit"
            return 1
        return code
    except BaseException as exc:
        # 未捕获异常必须留下输出，否则 V02 无法区分「静默失败」与「真的失败」。
        # 引导自身路径每次都在新的临时目录里，写进输出会让指纹不稳定。
        # 变异检验需要区分「断言失败」与「崩溃」，这里只记异常类型名。
        failure["error"] = type(exc).__name__
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
    payload = {"exit": exit_code, "error": failure["error"],
               "covered": {k: sorted(set(v)) for k, v in covered.items()},
               "integrity": _integrity_violations(
                   _INTEGRITY_SNAP, _INTEGRITY_MODULES)}
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
        violations = covered.get("integrity")
        if not isinstance(violations, list):
            violations = []
        violations = [v for v in violations if isinstance(v, str) and v]
        if violations:
            raise IntegrityViolation(
                "断言设施在导入期被改写：" + "；".join(violations[:5])
            )
        error = covered.get("error")
        if not isinstance(error, str) or not error:
            error = None
        return code, text, (covered if trace_mode else None), error


def run_command_classified(cmd: str, cwd: Path, timeout: int) -> tuple[int, str, str | None]:
    """受控执行并返回（退出码, 输出, 未捕获异常类型）；供变异判据区分崩溃与断言失败。"""
    script, problem = parse_isolated_command(cmd, cwd)
    if problem:
        raise RuntimeError(problem)
    code, text, _covered, error = _exec_isolated(cwd, script, timeout, trace_mode=False)
    return code, text, error


def run_command(cmd: str, cwd: Path, timeout: int) -> tuple[int, str]:
    """按白名单形式解释并受控执行命令（非 trace 模式）。"""
    code, text, _error = run_command_classified(cmd, cwd, timeout)
    return code, text


def run_traced_command(cmd: str, repo: Path, timeout: int):
    """受控执行并采集覆盖行；返回 (退出码, 输出, covered)。"""
    script, problem = parse_isolated_command(cmd, repo)
    if problem:
        raise RuntimeError(problem)
    code, text, covered, _error = _exec_isolated(repo, script, timeout, trace_mode=True)
    return code, text, covered


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


# ---------------------------------------------------------------- 补丁结构约束

def patch_file_edits(text: str) -> list[dict]:
    """按文件列出补丁的增行／删行及其 a／b 侧行号。"""
    out: list[dict] = []
    for entry in patch_entries(text):
        added: list[tuple[int, str]] = []
        deleted: list[tuple[int, str]] = []
        a_cur = b_cur = None
        lines = entry["lines"]
        new_file = any(
            line.startswith("new file mode") or line == "--- /dev/null"
            for line in lines
        )
        deleted_file = any(
            line.startswith("deleted file mode") or line == "+++ /dev/null"
            for line in lines
        )
        for line in lines:
            m = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if m:
                a_cur, b_cur = int(m.group(1)), int(m.group(2))
                continue
            if a_cur is None:
                continue
            if line.startswith("+"):
                added.append((b_cur, line[1:]))
                b_cur += 1
            elif line.startswith("-"):
                deleted.append((a_cur, line[1:]))
                a_cur += 1
            elif line.startswith(" ") or line == "":
                a_cur += 1
                b_cur += 1
        out.append({
            "a": entry["a"], "b": entry["b"], "lines": lines,
            "added": added, "deleted": deleted,
            "new": new_file, "deleted_file": deleted_file,
        })
    return out


def apply_hunks_to_source(base_text: str, hunk_lines: list[str]) -> str | None:
    """把补丁的 hunk 应用到 base 源码；上下文不匹配时返回 None。"""
    base = base_text.splitlines(keepends=True)
    out: list[str] = []
    pos = 0
    in_hunk = False
    for line in hunk_lines:
        m = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if m:
            start = int(m.group(1)) - 1
            if start < pos or start > len(base):
                return None
            out.extend(base[pos:start])
            pos = start
            in_hunk = True
            continue
        if not in_hunk or line.startswith("\\"):
            continue
        if line.startswith("+"):
            out.append(line[1:] + "\n")
        elif line.startswith("-"):
            if pos >= len(base) or base[pos].rstrip("\r\n") != line[1:]:
                return None
            pos += 1
        else:
            text = line[1:] if line.startswith(" ") else line
            if pos >= len(base) or base[pos].rstrip("\r\n") != text:
                return None
            out.append(base[pos])
            pos += 1
    out.extend(base[pos:])
    return "".join(out)


# ------------------------------------------------------ 声明式 / 可执行语句

# 只允许这些装饰器出现在声明式改动里；其它装饰器是导入期任意调用。
DECLARATIVE_DECORATORS = {
    "dataclass", "field", "property", "staticmethod", "classmethod",
    "abstractmethod", "abstractproperty", "cached_property", "total_ordering",
    "override", "final", "runtime_checkable", "no_type_check",
    "dataclass_transform", "lru_cache", "singledispatch",
    "singledispatchmethod", "contextmanager", "asynccontextmanager", "wraps",
    "deprecated",
}
# 模块级赋值里出现这些接收者时按「导入期可执行」处理，不当作声明式常量。
MODULE_LEVEL_DANGEROUS = {
    "os", "sys", "subprocess", "unittest", "builtins", "shutil", "importlib",
    "io", "codecs", "mmap", "runpy", "pkgutil", "ctypes", "pickle", "marshal",
    "operator", "tempfile", "pathlib", "glob", "socket", "sitecustomize",
    "usercustomize", "inspect", "linecache",
}
DANGEROUS_CALL_NAMES = {
    "open", "exec", "eval", "__import__", "getattr", "setattr", "delattr",
    "compile", "globals", "locals", "vars", "breakpoint", "input",
}


def _structure_maps(source: str) -> tuple[set[int], ast.Module]:
    """返回（全部函数／方法体行, AST）。"""
    tree = ast.parse(source)
    body: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            body.update(range(node.body[0].lineno, (node.end_lineno or node.lineno) + 1))
    return body, tree


def _root_name(node: ast.AST) -> str | None:
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def _pure_value(node: ast.AST | None) -> bool:
    """模块级赋值右侧是否只含声明式内容（不调用危险接收者）。

    字面量算术（负号、`~`、`1 << 4`、`2**3`）与字面量容器都算纯值；
    运算符节点本身不是表达式，递归时应直接放行，否则 `-1`、`0 - 1`
    会被误判成模块级可执行语句。
    """
    if node is None:
        return True
    if isinstance(node, (ast.Constant, ast.Name)):
        return True
    if isinstance(node, (ast.operator, ast.unaryop, ast.cmpop, ast.boolop,
                         ast.expr_context)):
        return True
    if isinstance(node, ast.Attribute):
        return _pure_value(node.value)
    if isinstance(node, ast.Call):
        root = _root_name(node.func)
        name = (
            node.func.attr if isinstance(node.func, ast.Attribute)
            else getattr(node.func, "id", "")
        )
        if root in MODULE_LEVEL_DANGEROUS or name in DANGEROUS_CALL_NAMES:
            return False
        return (
            _pure_value(node.func)
            and all(_pure_value(a) for a in node.args)
            and all(_pure_value(k.value) for k in node.keywords)
        )
    if isinstance(node, (ast.Tuple, ast.List, ast.Set, ast.Dict, ast.Subscript,
                         ast.Slice, ast.Starred, ast.JoinedStr, ast.FormattedValue,
                         ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.IfExp,
                         ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp,
                         ast.GeneratorExp, ast.comprehension)):
        return all(_pure_value(c) for c in ast.iter_child_nodes(node))
    return False


def _declarative_decorator(stmt: ast.AST) -> bool:
    for d in getattr(stmt, "decorator_list", []):
        node = d.func if isinstance(d, ast.Call) else d
        name = node.attr if isinstance(node, ast.Attribute) else getattr(node, "id", "")
        if name not in DECLARATIVE_DECORATORS:
            return False
    return True


def _innermost_stmt(
    stmts: list[ast.stmt], lineno: int
) -> tuple[str | None, ast.stmt | None]:
    """找到 lineno 所属的模块／类体语句（不进入函数体）。"""
    for s in stmts:
        end = getattr(s, "end_lineno", None) or s.lineno
        decos = getattr(s, "decorator_list", [])
        start = min([s.lineno] + [d.lineno for d in decos]) if decos else s.lineno
        if not (start <= lineno <= end):
            continue
        if decos and any(
            d.lineno <= lineno <= (d.end_lineno or d.lineno) for d in decos
        ):
            return "decorator", s
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return ("def", s) if lineno < s.body[0].lineno else (None, s)
        if isinstance(s, ast.ClassDef):
            if lineno < s.body[0].lineno:
                return "class", s
            return _innermost_stmt(s.body, lineno)
        bodies: list[ast.stmt] = []
        for field in ("body", "orelse", "finalbody"):
            bodies.extend(getattr(s, field, []) or [])
        if isinstance(s, ast.Try):
            for h in s.handlers:
                bodies.extend(h.body)
        if not bodies:
            return "stmt", s
        found, node = _innermost_stmt(bodies, lineno)
        if found is not None:
            return found, node
        return "executable", s
    return None, None


def _classify_line(tree: ast.Module, lineno: int) -> tuple[str, str]:
    """非函数体行：('ok'|'cannot', 原因)。"""
    kind, stmt = _innermost_stmt(tree.body, lineno)
    if kind is None or stmt is None:
        return "cannot", "module"
    if kind in ("def", "class"):
        return "ok", ""
    if kind == "decorator":
        return ("ok", "") if _declarative_decorator(stmt) else ("cannot", "import")
    if kind == "executable":
        return "cannot", "module"
    if isinstance(stmt, (ast.Import, ast.ImportFrom)):
        return "ok", ""
    if isinstance(stmt, ast.Assign):
        ok = all(isinstance(t, ast.Name) for t in stmt.targets) and _pure_value(stmt.value)
        return ("ok", "") if ok else ("cannot", "module")
    if isinstance(stmt, ast.AnnAssign):
        ok = isinstance(stmt.target, ast.Name) and _pure_value(stmt.value)
        return ("ok", "") if ok else ("cannot", "module")
    if isinstance(stmt, ast.AugAssign):
        ok = isinstance(stmt.target, ast.Name) and _pure_value(stmt.value)
        return ("ok", "") if ok else ("cannot", "module")
    if isinstance(stmt, ast.Expr):
        if isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
            return "ok", ""
        return "cannot", "module"
    if isinstance(stmt, (ast.Pass, ast.Global, ast.Nonlocal)):
        return "ok", ""
    return "cannot", "module"


SCOPE_MESSAGE = "该缺陷需要改模块级声明，超出本技能适用面"


def patch_structural_violations(repo: Path, text: str) -> list[str]:
    """检查补丁改动行的执行时机；返回无法判定（cannot_evaluate）的原因。

    规则：
      · 函数／方法体内的改动：放行（导入期是否可达不再由语法位置推断，
        由运行时完整性校验覆盖：断言设施在导入期被改写会被直接判 cannot）；
      · 模块级可执行语句（Expr 调用、猴补丁、控制流头等）：cannot_evaluate；
      · 声明式改动（import、模块常量、类属性／dataclass 默认值、docstring、
        声明式装饰器、def/class 头）：放行。
    测试路径不在本规则范围（V06 另行处理）。
    """
    cannots: list[str] = []
    for entry in patch_file_edits(text):
        paths = [p for p in (entry["a"], entry["b"]) if p and p != "/dev/null"]
        if not paths or any(is_test_path(p) for p in paths):
            continue
        if not any(p.endswith(".py") for p in paths):
            continue
        base_text = ""
        base_body: set[int] = set()
        base_tree: ast.Module | None = None
        if not entry["new"]:
            base_path = repo / entry["a"]
            if not base_path.is_file():
                cannots.append(
                    f'{entry["a"]}：补丁的 base 侧文件不存在，无法判断执行时机'
                )
                continue
            base_text = base_path.read_text(encoding="utf-8", errors="replace")
            try:
                base_body, base_tree = _structure_maps(base_text)
            except SyntaxError as exc:
                cannots.append(f'{entry["a"]}：base 源码无法解析（{exc}）')
                continue
        patched_body: set[int] = set()
        patched_tree: ast.Module | None = None
        if entry["added"]:
            if entry["new"]:
                patched_text = "".join(t + "\n" for _n, t in entry["added"])
            else:
                patched_text = apply_hunks_to_source(base_text, entry["lines"])
            if patched_text is None:
                cannots.append(f'{entry["b"]}：补丁无法应用到 base 源码，无法判断结构')
                continue
            try:
                patched_body, patched_tree = _structure_maps(patched_text)
            except SyntaxError as exc:
                cannots.append(f'{entry["b"]}：补丁后源码无法解析（{exc}）')
                continue
        for lineno, line in entry["deleted"]:
            if not line.strip():
                continue
            if lineno in base_body:
                continue
            kind, _reason = _classify_line(base_tree, lineno) if base_tree else ("cannot", "module")
            if kind != "ok":
                cannots.append(
                    f'{entry["a"]}:{lineno} 改的是模块级可执行语句，'
                    f"{SCOPE_MESSAGE}：" + line.strip()[:80]
                )
        for lineno, line in entry["added"]:
            if not line.strip():
                continue
            if lineno in patched_body:
                continue
            kind, _reason = _classify_line(patched_tree, lineno) if patched_tree else ("cannot", "module")
            if kind != "ok":
                cannots.append(
                    f'{entry["b"]}:{lineno} 改的是模块级可执行语句，'
                    f"{SCOPE_MESSAGE}：" + line.strip()[:80]
                )
    return cannots


# ---------------------------------------------------------------- 复现测试白名单

BANNED_TEST_MODULES = {
    "os", "subprocess", "importlib", "builtins", "sitecustomize", "usercustomize",
    "inspect", "linecache", "shutil", "io", "codecs", "mmap", "runpy", "pkgutil",
    "operator", "ctypes", "pickle", "marshal", "pathlib", "tempfile", "glob",
    "socket", "atexit", "sysconfig", "resource", "fcntl", "signal", "mock",
}
BANNED_TEST_NAMES = {
    "open", "exec", "eval", "__import__", "__builtins__",
    "getattr", "setattr", "delattr", "hasattr", "globals", "locals", "vars",
    "__dict__", "compile", "breakpoint",
}
BANNED_TEST_ATTRS = {
    "open", "read_text", "read_bytes", "write_text", "write_bytes",
    "readlines", "readline", "getsource", "environ", "modules", "mock", "patch",
    "__dict__", "__globals__", "__code__", "__closure__", "__subclasses__",
    "__bases__", "__mro__", "__class__", "__getattribute__", "__setattr__",
    "__delattr__", "__builtins__", "__loader__", "__spec__", "__reduce__",
    "__reduce_ex__", "mro",
}
# sys 只允许这两种用法（把仓根加入模块搜索路径），其余一律视为越界。
SYS_ALLOWED_METHODS = {"insert", "append"}
# 断言方法：这些调用本身允许出现在复现测试里。
ASSERTION_METHOD_NAMES = {
    "assertEqual", "assertNotEqual", "assertTrue", "assertFalse",
    "assertIs", "assertIsNot", "assertIsNone", "assertIsNotNone",
    "assertIn", "assertNotIn", "assertIsInstance", "assertNotIsInstance",
    "assertRaises", "assertRaisesRegex", "assertWarns", "assertWarnsRegex",
    "assertRegex", "assertNotRegex", "assertAlmostEqual",
    "assertNotAlmostEqual", "assertGreater", "assertGreaterEqual",
    "assertLess", "assertLessEqual", "assertCountEqual",
    "assertMultiLineEqual", "assertListEqual", "assertTupleEqual",
    "assertDictEqual", "assertSetEqual", "assertLogs", "assertNoLogs",
    "fail", "subTest",
}
# 这些断言方法的参数里必须至少有一个字面量期望值。
EXPECTED_LITERAL_METHODS = {
    "assertEqual", "assertNotEqual", "assertAlmostEqual",
    "assertNotAlmostEqual", "assertIn", "assertNotIn", "assertIs",
    "assertIsNot", "assertGreater", "assertGreaterEqual", "assertLess",
    "assertLessEqual", "assertRegex", "assertNotRegex", "assertCountEqual",
    "assertMultiLineEqual", "assertListEqual", "assertTupleEqual",
    "assertDictEqual", "assertSetEqual",
}
# 断言里允许出现的非入口调用：类型谓词，不构造期望值。
ASSERTION_PURE_CALLS = {"isinstance", "issubclass", "callable"}
LITERAL_BINOPS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor,
)
LITERAL_UNARYOPS = (ast.UAdd, ast.USub, ast.Invert)


def _literal_expr(node: ast.AST | None) -> bool:
    """期望值是否是字面量（含负号与字面量算术、字面量容器）。"""
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, LITERAL_UNARYOPS):
        return _literal_expr(node.operand)
    if isinstance(node, ast.BinOp) and isinstance(node.op, LITERAL_BINOPS):
        return _literal_expr(node.left) and _literal_expr(node.right)
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return all(_literal_expr(e) for e in node.elts)
    if isinstance(node, ast.Dict):
        return all(k is not None and _literal_expr(k) for k in node.keys) and all(
            _literal_expr(v) for v in node.values
        )
    if isinstance(node, ast.JoinedStr):
        return all(_literal_expr(v) for v in node.values)
    if isinstance(node, ast.FormattedValue):
        return _literal_expr(node.value)
    return False


def parse_under_test(raw) -> tuple[dict[str, set[str]] | None, str | None]:
    """解析 repro.md 的 under_test（`calc.add` 或 `[calc.add, calc.mul]`）。"""
    if raw is None:
        return None, "repro.md 未声明 under_test（被测入口）"
    items = raw if isinstance(raw, list) else [raw]
    if not items:
        return None, "repro.md 的 under_test 为空"
    mapping: dict[str, set[str]] = {}
    for item in items:
        if not nonempty_str(item) or "." not in str(item):
            return None, f"repro.md 的 under_test 项非法：{item!r}（应形如 calc.add）"
        mod, sym = str(item).rsplit(".", 1)
        if not mod or not sym or sym == "*":
            return None, f"repro.md 的 under_test 项非法：{item!r}（应形如 calc.add）"
        mapping.setdefault(mod, set()).add(sym)
    return mapping, None


def _module_candidates(repo: Path, parts: list[str]) -> tuple[Path | None, list[str]]:
    """找 `a.b.c` 里最长的模块前缀，返回（源文件, 剩余属性路径）。"""
    for cut in range(len(parts) - 1, 0, -1):
        rel = Path(*parts[:cut])
        for cand in (
            repo / rel.with_suffix(".py"),
            repo / rel / "__init__.py",
            repo / "src" / rel.with_suffix(".py"),
            repo / "src" / rel / "__init__.py",
        ):
            if cand.is_file():
                return cand, parts[cut:]
    return None, []


def _find_callable(body: list[ast.stmt], rest: list[str]) -> ast.AST | None:
    current = body
    for i, name in enumerate(rest):
        stmt = next(
            (
                s for s in current
                if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and s.name == name
            ),
            None,
        )
        if stmt is None:
            return None
        if i == len(rest) - 1:
            return stmt
        if not isinstance(stmt, ast.ClassDef):
            return None
        current = stmt.body
    return None


def under_test_entry_problems(
    repo: Path, mapping: dict[str, set[str]]
) -> tuple[list[str], list[str]]:
    """`under_test` 只允许函数／类入口；常量与模块名在 V01 就拒。"""
    problems: list[str] = []
    unresolved: list[str] = []
    for mod, syms in mapping.items():
        for sym in sorted(syms):
            source, rest = _module_candidates(repo, f"{mod}.{sym}".split("."))
            label = f"{mod}.{sym}"
            if source is None:
                unresolved.append(label)
                continue
            try:
                tree = ast.parse(source.read_text(encoding="utf-8", errors="replace"))
            except (OSError, SyntaxError) as exc:
                unresolved.append(f"{label}（源码无法解析：{exc}）")
                continue
            if _find_callable(tree.body, rest) is None:
                problems.append(
                    f"under_test 项 {label} 不是模块级可调用入口（只允许函数或类）"
                )
    return problems, unresolved


def _assignment_targets(node: ast.AST) -> list[ast.AST]:
    if isinstance(node, ast.Assign):
        return list(node.targets)
    if isinstance(node, (ast.AnnAssign, ast.AugAssign, ast.For, ast.AsyncFor)):
        return [node.target]
    if isinstance(node, ast.Delete):
        return list(node.targets)
    if isinstance(node, ast.NamedExpr):
        return [node.target]
    return []


def _resolves_to_local(repo: Path | None, name: str) -> bool:
    """`name` 的首段是否能在仓内解析成模块或包（用于识别本地夹具）。"""
    if repo is None or not name:
        return False
    base = repo / name.split(".")[0]
    return base.with_suffix(".py").is_file() or base.is_dir()


def test_code_violations(
    path: Path,
    under_test: dict[str, set[str]] | None = None,
    repo: Path | None = None,
) -> list[str]:
    """复现测试只能是「调用声明的被测入口并断言」。

    禁止：读文件、碰环境、起子进程、动态取名、猴补丁外部对象、`sys` 除
    `path.insert/append` 外的任何用法；不得读取被测模块入口之外的属性；
    不得导入 `unittest.mock` 或与 `under_test` 无关的本地夹具模块；断言里
    的期望值必须是字面量，不得用调用表达式构造。
    """
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (OSError, SyntaxError) as exc:
        return [f"复现测试无法解析：{exc}"]
    hits: set[str] = set()
    imported: dict[str, str] = {}
    sys_aliases: set[str] = set()
    entry_alias_module: dict[str, str] = {}
    entry_symbols: dict[str, set[str]] = dict(under_test or {})
    direct_entries: set[str] = set()

    def _entry_module(name: str) -> bool:
        return any(
            mod == name or name.startswith(mod + ".") or mod.startswith(name + ".")
            for mod in entry_symbols
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                bind = alias.asname or top
                imported[bind] = alias.name
                if top in BANNED_TEST_MODULES:
                    hits.add(f"不得导入 {alias.name}")
                if top == "tests":
                    hits.add("不得导入本地夹具模块（tests.*）")
                elif _resolves_to_local(repo, alias.name) and not _entry_module(alias.name):
                    hits.add(
                        f"不得导入与 under_test 无关的仓内模块 {alias.name}（本地夹具）"
                    )
                if alias.name == "sys":
                    sys_aliases.add(bind)
                if alias.name in entry_symbols:
                    entry_alias_module[bind] = alias.name
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            top = mod.split(".")[0]
            for alias in node.names:
                if alias.name != "*":
                    imported[alias.asname or alias.name] = f"{mod}.{alias.name}"
            if node.level > 0:
                hits.add("不得使用相对导入（本地夹具）")
            if top in BANNED_TEST_MODULES:
                hits.add(f"不得从 {mod} 导入")
            if mod == "unittest.mock" or mod.startswith("unittest.mock."):
                hits.add("不得导入 unittest.mock")
            elif mod == "unittest" and any(a.name == "mock" for a in node.names):
                hits.add("不得导入 unittest.mock")
            if top == "tests":
                hits.add("不得导入本地夹具模块（tests.*）")
            elif _resolves_to_local(repo, mod) and not _entry_module(mod):
                hits.add(
                    f"不得导入与 under_test 无关的仓内模块 {mod}（本地夹具）"
                )
            if mod == "sys":
                hits.add(
                    "不得从 sys 导入（只允许 import sys 后 sys.path.insert／append）"
                )
            if mod in entry_symbols:
                allowed = entry_symbols[mod]
                for alias in node.names:
                    if alias.name == "*":
                        hits.add(f"不得从 {mod} 导入 *")
                    elif alias.name not in allowed:
                        hits.add(
                            "只能使用声明的被测入口 "
                            f"{mod}.{'／'.join(sorted(allowed))}，不得读取 {alias.name}"
                        )
                    else:
                        direct_entries.add(alias.asname or alias.name)

    # 只放行 sys.path.insert/append(索引, ".")；绝对路径、`..`、其它参数都拒绝。
    sys_allowed: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in SYS_ALLOWED_METHODS:
            continue
        path_attr = node.func.value
        if not (
            isinstance(path_attr, ast.Attribute)
            and path_attr.attr == "path"
            and isinstance(path_attr.value, ast.Name)
            and path_attr.value.id in sys_aliases
        ):
            continue
        args_ok = all(
            isinstance(a, ast.Constant) and isinstance(a.value, (int, str))
            for a in node.args
        )
        strs = [
            a.value for a in node.args
            if isinstance(a, ast.Constant) and isinstance(a.value, str)
        ]
        if args_ok and strs and all(v in (".", "./") for v in strs):
            for sub in ast.walk(node.func):
                sys_allowed.add(id(sub))

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id in BANNED_TEST_NAMES:
                hits.add(f"不得使用 {node.id}")
            if node.id in sys_aliases and id(node) not in sys_allowed:
                hits.add(
                    "sys 只允许 sys.path.insert／append 把仓根加入路径，"
                    "不得读取 sys 的其它属性"
                )
        elif isinstance(node, ast.Attribute):
            if node.attr in BANNED_TEST_ATTRS:
                hits.add(f"不得使用 .{node.attr}")
            root = _root_name(node)
            if root in entry_alias_module:
                allowed = entry_symbols[entry_alias_module[root]]
                if node.attr not in allowed:
                    hits.add(
                        "只能使用声明的被测入口 "
                        f"{entry_alias_module[root]}.{'／'.join(sorted(allowed))}，"
                        f"不得读取 .{node.attr}"
                    )
            if root in direct_entries:
                hits.add(f"不得读取被测入口 {root} 的其它属性（.{node.attr}）")

    # 猴补丁：给任何已导入对象的属性赋值／删除（unittest.TestX.y = …）。
    for node in ast.walk(tree):
        for target in _assignment_targets(node):
            for sub in ast.walk(target):
                if isinstance(sub, ast.Attribute):
                    root = _root_name(sub)
                    if root in imported:
                        hits.add(f"不得给 {root} 的属性赋值（猴补丁）")

    # 期望值独立性：断言里的期望值必须是字面量。调用只允许被测入口、
    # 断言方法本身与类型谓词；`int("-1")`、`calc.make_expected()` 一律拒绝。
    def _call_allowed(call: ast.Call) -> bool:
        func = call.func
        if isinstance(func, ast.Name):
            return func.id in direct_entries or func.id in ASSERTION_PURE_CALLS
        if isinstance(func, ast.Attribute):
            root = _root_name(func)
            if (
                root in entry_alias_module
                and func.attr in entry_symbols[entry_alias_module[root]]
            ):
                return True
            if func.attr in ASSERTION_METHOD_NAMES:
                return True
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            compares = [
                n for n in ast.walk(node.test) if isinstance(n, ast.Compare)
            ]
            if compares and not any(
                _literal_expr(x)
                for cmp_node in compares
                for x in [cmp_node.left, *cmp_node.comparators]
            ):
                hits.add(
                    "断言里的期望值必须是字面量（不得取自被测代码或运行时计算）"
                )
            for sub in ast.walk(node.test):
                if isinstance(sub, ast.Call) and not _call_allowed(sub):
                    hits.add(
                        "断言中只允许调用被测入口或断言方法；"
                        "期望值必须是字面量（不得用 int(\"-1\") 这类调用构造）"
                    )
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in EXPECTED_LITERAL_METHODS
        ):
            if not any(_literal_expr(a) for a in node.args):
                hits.add(
                    f"{node.func.attr} 的期望值必须是字面量"
                    "（不得取自被测代码或运行时计算）"
                )
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and not _call_allowed(sub):
                    hits.add(
                        "断言中只允许调用被测入口或断言方法；期望值必须是字面量"
                    )
    return sorted(hits)


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
    """补丁触及的生产代码行：新增行逐行变异，每个连续改动块整块回退作删除行变异。"""
    targets: list[dict] = []
    for entry in patch_entries(text):
        a_path, b_path = entry["a"], entry["b"]
        if is_test_path(a_path) or is_test_path(b_path):
            continue
        a_cur = b_cur = None
        added: list[tuple[int, str]] = []
        blocks: list[dict] = []
        run: dict | None = None

        def flush() -> None:
            nonlocal run
            if run is not None and (run["deleted"] or run["added"]):
                blocks.append(run)
            run = None

        for line in entry["lines"]:
            m = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if m:
                flush()
                a_cur, b_cur = int(m.group(1)), int(m.group(2))
                continue
            if a_cur is None:
                continue
            if line.startswith("+"):
                if run is None:
                    run = {"insert": b_cur - 1, "deleted": [], "added": []}
                added.append((b_cur, line[1:]))
                run["added"].append(line[1:])
                b_cur += 1
            elif line.startswith("-"):
                if run is None:
                    run = {"insert": b_cur - 1, "deleted": [], "added": []}
                run["deleted"].append(line[1:])
                a_cur += 1
            elif line.startswith(" ") or line == "":
                # 上下文把同一 hunk 切成多个独立改动块；每块单独回退。
                flush()
                a_cur += 1
                b_cur += 1
        flush()
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


UNITTEST_SUMMARY_RE = re.compile(r"^FAILED \(([^)]*)\)", re.MULTILINE)
TEST_COUNT_RE = re.compile(r"(\d+) (failed|error|errors)\b")


def classify_test_outcome(code: int, text: str, error_type: str | None) -> str:
    """把一次受控执行归类为 passed／assertion／crash。

    只有 assertion（断言失败）能作为「变异被杀死」的证据。
    崩溃、提前退出（含 `os._exit`／`SystemExit`）、超时都不算。
    """
    if code == 0:
        return "passed"
    m = UNITTEST_SUMMARY_RE.search(text)
    if m:
        summary = m.group(1)
        failures = re.search(r"failures=(\d+)", summary)
        errors = re.search(r"errors=(\d+)", summary)
        if failures and int(failures.group(1)) > 0:
            return "assertion"
        if errors and int(errors.group(1)) > 0:
            return "crash"
    counts: dict[str, int] = {}
    for num, kind in TEST_COUNT_RE.findall(text):
        counts[kind] = counts.get(kind, 0) + int(num)
    if counts.get("failed", 0):
        return "assertion"
    if counts.get("error", 0) or counts.get("errors", 0):
        return "crash"
    if error_type == "AssertionError":
        return "assertion"
    if error_type:
        return "crash"
    if re.search(r"\bAssertionError\b", text):
        return "assertion"
    return "crash"


def _mutant_outcome(repo: Path, cmd: str, timeout: int) -> tuple[str, str]:
    """运行一次变异体，返回（passed／assertion／crash／timeout，说明）。"""
    _clear_pycache(repo)
    try:
        code, text, error = run_command_classified(cmd, repo, timeout)
    except IntegrityViolation:
        raise
    except subprocess.TimeoutExpired:
        return "timeout", "变异后测试超时"
    except RuntimeError as exc:
        return "crash", f"变异后无法受控执行：{exc}"
    kind = classify_test_outcome(code, text, error)
    if kind == "crash":
        return kind, f"退出码={code}，未捕获异常={error or '非断言异常或提前退出'}"
    return kind, ""


def run_mutation_checks(repo: Path, cmd: str, timeout: int, patch_text: str) -> list[str]:
    """在 patched 态逐行造变异并重跑复现测试；测试必须以断言失败变红。

    返回失败理由列表；空列表表示补丁触及的生产代码行都被测试敏感覆盖。
    纯新增补丁没有 base 侧删除行，但每个新增行仍要过这一关。
    整份补丁都造不出可编译变异即 fail，不把「改不动的行」算作通过。
    """
    targets = patch_mutation_targets(patch_text)
    if not targets:
        return ["补丁未在生产代码上触碰任何行，无法造出变异"]
    failures: list[str] = []
    executed_mutants = 0
    immutable: list[str] = []
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
                    immutable.append(f'{target["path"]}:{lineno}')
                    continue
                outcomes: list[str] = []
                killed = False
                for candidate in candidates:
                    mutated = _replaced_line(lines, lineno - 1, candidate)
                    source = "".join(mutated)
                    if not _compiles(source, path):
                        continue
                    path.write_text(source, encoding="utf-8")
                    executed_mutants += 1
                    kind, _detail = _mutant_outcome(repo, cmd, timeout)
                    outcomes.append(kind)
                    if kind == "assertion":
                        killed = True
                        break
                path.write_text(original, encoding="utf-8")
                if not killed:
                    note = ""
                    if outcomes and all(o != "passed" for o in outcomes):
                        note = "（变异后测试崩溃或超时，不算断言失败）"
                    elif not outcomes:
                        note = "（没有可编译的变异）"
                    failures.append(
                        f'{target["path"]}:{lineno} 的变异均未使复现测试以断言失败变红'
                        + note
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
                executed_mutants += 1
                kind, detail = _mutant_outcome(repo, cmd, timeout)
                if kind == "passed":
                    failures.append(
                        f'{target["path"]} 的删除行被回退后复现测试仍通过'
                        "（补丁行未被测试敏感覆盖）"
                    )
                elif kind != "assertion":
                    failures.append(
                        f'{target["path"]} 的删除行回退后测试未以断言失败告终'
                        f"（{detail}），不能算杀死变异"
                    )
        finally:
            path.write_text(original, encoding="utf-8")
    if not executed_mutants:
        # 所有改动行都是 docstring／注释／纯字符串等改不动的行：没有造出任何变异。
        failures.append(
            "补丁行全部造不出可编译变异（改不动的行不算敏感覆盖证据）"
            + ("：" + "、".join(immutable[:8]) if immutable else "")
        )
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
    mapping, uerr = parse_under_test(data.get("under_test"))
    if uerr:
        problems.append(uerr)
    if problems:
        return bad("V01", *problems)
    entry_problems, unresolved = under_test_entry_problems(ctx.repo, mapping or {})
    if entry_problems:
        return bad("V01", *entry_problems)
    if unresolved:
        return cannot(
            "V01",
            "无法定位 under_test 的源文件，不能确认是可调用入口："
            + "；".join(unresolved),
        )
    return ok("V01", "repro.md 九字段齐全且类型正确；under_test 均为可调用入口")


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
        except IntegrityViolation as exc:
            return cannot("V02", f"第 {i + 1} 次运行：{exc}")
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
    under_test: dict[str, set[str]] | None = None
    repro, rerr = load_frontmatter(ctx.repo / "repro.md")
    if rerr:
        problems.append(f"repro.md 无法解析：{rerr}")
    else:
        under_test, uerr = parse_under_test(repro.get("under_test"))
        if uerr:
            problems.append(uerr)
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
        wl = test_code_violations(test_real, under_test, ctx.repo)
        if wl:
            problems.append("复现测试不在白名单内：" + "；".join(wl[:5]))
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
    except IntegrityViolation as exc:
        return cannot("V03", str(exc))
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
    struct_cannot = patch_structural_violations(ctx.repo, text)
    if struct_cannot:
        return cannot("V06", *struct_cannot[:5])
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
    except IntegrityViolation as exc:
        return cannot("V07", str(exc))
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
    if _rs is not None:
        under_test, uerr = parse_under_test(repro.get("under_test"))
        if uerr:
            return bad("V08", uerr)
        wl = test_code_violations(_rs, under_test, ctx.repo)
        if wl:
            return bad("V08", "复现测试不在白名单内：" + "；".join(wl[:5]))
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
        except IntegrityViolation:
            raise
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"{label}重跑超时，无法判定")
        except RuntimeError as exc:
            raise RuntimeError(f"{label}重跑无法执行：{exc}")

    def rerun_plain(label: str, command: str) -> int:
        try:
            code, _out = run_command(command, ctx.repo, timeout)
        except IntegrityViolation:
            raise
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
