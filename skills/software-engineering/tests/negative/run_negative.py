#!/usr/bin/env python3
"""负向用例：证明「该拦的拦住了」。

这些用例不进分发包（tests/ 不在打包白名单）。每个用例都构造一个应被拒绝的
场景，然后断言检查器确实拒绝。退出码 0 表示所有负向用例都被拦住；非 0 表示
有该拦而没拦住的路径。

用法（仓库根目录）：
    python3 skills/software-engineering/tests/negative/run_negative.py
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parents[2]
VALIDATE = PKG / "validators" / "validate.py"
CHECKER = PKG / "validators" / "check_blocker_log.py"
BUILDER = PKG / "scripts" / "build_package.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def sh(cmd: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)


def init_repo(path: Path) -> None:
    path.mkdir(parents=True)
    sh("git init -q", path)
    sh("git config user.email test@example.invalid", path)
    sh("git config user.name test", path)


def commit_all(path: Path) -> str:
    sh("git add -A", path)
    sh("git commit -q -m base", path)
    return sh("git rev-parse HEAD", path).stdout.strip()


def run_validator(repo: Path, config: Path, only: list[str]) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(VALIDATE), "--config", str(config), "--only", *only]
    return subprocess.run(cmd, capture_output=True, text=True)


def write_config(repo: Path, path: Path) -> None:
    path.write_text(
        "\n".join([
            f"repo_path: {repo}",
            "test_command: \"python3 -m unittest discover -s tests -p 'test_*.py'\"",
            "repro_runs: 2",
            "repro_timeout_seconds: 30",
            "allowed_scope:",
            "  - calc.py",
            "cache_cleanup_policy: \"清空 __pycache__\"",
        ]) + "\n",
        encoding="utf-8",
    )


def case_empty_test_and_patch(tmp: Path) -> str:
    """无 bug ＋ 空测试 ＋ 空补丁：V02/V03 必须拦住。"""
    repo = tmp / "empty"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "repro_empty.py").write_text("", encoding="utf-8")
    sha = commit_all(repo)
    (repo / "tests" / "repro_empty.meta.yaml").write_text(
        "\n".join([
            "file: tests/repro_empty.py",
            "test_id: repro_empty",
            "single_run_command: python3 tests/repro_empty.py",
            f"base_commit: {sha}",
            "expected_failure: should fail",
        ]) + "\n",
        encoding="utf-8",
    )
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        "command: python3 tests/repro_empty.py\nexpected: fail\nactual: pass\nexit_code: 1\n---\n"
        % sha,
        encoding="utf-8",
    )
    (repo / "fix.patch").write_text("", encoding="utf-8")
    cfg = tmp / "empty-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V02", "V03"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "V02" in out and "V03" in out, out
    return "V02/V03 拦住空测试与恒真失败命令"


def case_silent_failure(tmp: Path) -> str:
    """失败命令无输出：V02 必须以「输出为空」拦住。"""
    repo = tmp / "silent"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "repro_silent.py").write_text(
        "import sys\nsys.exit(1)\n", encoding="utf-8"
    )
    sha = commit_all(repo)
    (repo / "tests" / "repro_silent.meta.yaml").write_text(
        "\n".join([
            "file: tests/repro_silent.py",
            "test_id: repro_silent",
            "single_run_command: python3 tests/repro_silent.py",
            f"base_commit: {sha}",
            "expected_failure: should fail",
        ]) + "\n",
        encoding="utf-8",
    )
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        "command: python3 tests/repro_silent.py\nexpected: fail\nactual: pass\nexit_code: 1\n---\n"
        % sha,
        encoding="utf-8",
    )
    cfg = tmp / "silent-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V02"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "输出为空" in out, out
    return "V02 拦住无输出的恒真失败命令"


def case_composite_command(tmp: Path) -> str:
    """复合命令＋恒真断言：V02/V03 必须拦住。"""
    repo = tmp / "composite"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "repro_fake.py").write_text(
        "import unittest\n\n"
        "class T(unittest.TestCase):\n"
        "    def test_x(self):\n"
        "        self.assertTrue(True)\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "tests" / "repro_fake.meta.yaml").write_text(
        "\n".join([
            "file: tests/repro_fake.py",
            "test_id: T.test_x",
            "single_run_command: python3 tests/repro_fake.py; true",
            f"base_commit: {sha}",
            "expected_failure: should fail",
        ]) + "\n",
        encoding="utf-8",
    )
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        "command: python3 tests/repro_fake.py; true\nexpected: fail\n"
        "actual: pass\nexit_code: 1\n---\n" % sha,
        encoding="utf-8",
    )
    cfg = tmp / "composite-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V02", "V03"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "单条简单命令" in out and "非恒真断言" in out, out
    return "V02/V03 拦住复合命令与 assertTrue(True)"


def case_phase2_or_true(tmp: Path) -> str:
    """第②段用「失败复现 || true」伪造：V08 分开重跑必须拦住。"""
    repo = tmp / "phase2"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "repro_bug.py").write_text(
        "import sys\nsys.path.insert(0, '.')\n"
        "from calc import add\n"
        "assert add(1, 2) == 3, 'add broken'\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    patch_text = (
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,2 +1,3 @@\n"
        " def add(a, b):\n"
        "     return a - b\n"
        "+# noop\n"
    )
    (repo / "fix.patch").write_text(patch_text, encoding="utf-8")
    patch_sha = hashlib.sha256(patch_text.encode("utf-8")).hexdigest()
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        "command: python3 tests/repro_bug.py\nexpected: fail\nactual: pass\nexit_code: 1\n---\n"
        % sha,
        encoding="utf-8",
    )
    test_cmd = "python3 -m unittest discover -s tests -p 'test_*.py'"
    (repo / "verify.log").write_text(
        f"run_id: fake\ncommit: {sha}\npatch_sha256: {patch_sha}\n"
        f"test_command_used: \"{test_cmd}\"\n"
        "phases:\n"
        "  - phase: 1\n    command: python3 tests/repro_bug.py\n    exit_code: 1\n"
        "    started_at: 2026-11-16T00:00:00\n    duration: 0.1\n"
        "  - phase: 2\n"
        "    command: \"python3 tests/repro_bug.py || true; "
        f"{test_cmd}\"\n    exit_code: 0\n"
        "    started_at: 2026-11-16T00:00:01\n    duration: 0.1\n"
        "  - phase: 3\n    command: python3 tests/repro_bug.py\n    exit_code: 1\n"
        "    started_at: 2026-11-16T00:00:02\n    duration: 0.1\n",
        encoding="utf-8",
    )
    (repo / "fix-report.md").write_text(
        f"---\nstatus: fixed_unverified_root_cause\npatch_sha256: {patch_sha}\n"
        "touched_files:\n  - calc.py\nevidence_kind: direct\n---\n",
        encoding="utf-8",
    )
    cfg = tmp / "phase2-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V08"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "第②段单独重跑复现命令" in out, out
    return "V08 拦住第②段「失败复现 || true」的伪造"


def case_test_constant_patch(tmp: Path) -> str:
    """改测试常量凑绿而 bug 未修：V06 必须拦住。"""
    repo = tmp / "patch-test"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "repro_bug.py").write_text(
        "import sys\nsys.path.insert(0, '.')\n"
        "from calc import add\n"
        "assert add(1, 2) == 3, 'add broken'\n"
        'print("ok")\n',
        encoding="utf-8",
    )
    commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/tests/repro_bug.py b/tests/repro_bug.py\n"
        "--- a/tests/repro_bug.py\n"
        "+++ b/tests/repro_bug.py\n"
        "@@ -1,5 +1,5 @@\n"
        " import sys\n"
        " sys.path.insert(0, '.')\n"
        " from calc import add\n"
        "-assert add(1, 2) == 3, 'add broken'\n"
        "+assert add(1, 2) == -1, 'add broken'\n"
        ' print("ok")\n',
        encoding="utf-8",
    )
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - tests/repro_bug.py\n"
        "estimated_touched_files: 1\nestimated_diff_lines: 2\n---\n"
        "机制：加法实现写成了减法。\n",
        encoding="utf-8",
    )
    cfg = tmp / "patch-test-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V06"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "V06" in out and "测试路径改动违规" in out, out
    return "V06 拦住改测试常量凑绿"


def case_blocker_port(tmp: Path) -> str:
    """card_section 里带端口：卡点日志检查必须拦住。"""
    log = tmp / "blocker-port.yaml"
    log.write_text(
        "- card_file: SKILL.md\n"
        "  card_section: \"§3:8080\"\n"
        "  type: 表述歧义\n"
        "  summary: \"约定说明不清\"\n"
        "  skill_version: 0.4.0\n",
        encoding="utf-8",
    )
    res = subprocess.run(
        [sys.executable, str(CHECKER), str(log)], capture_output=True, text=True
    )
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "端口" in out or "card_section" in out, out
    return "卡点日志检查拦住 card_section 带端口"


def case_nested_forbidden_asset(tmp: Path) -> str:
    """嵌套目录里放 registry 资产：打包脚本必须拒绝并删除产物。"""
    src = tmp / "pkg-src"
    shutil.copytree(
        PKG,
        src,
        ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "work", "build"),
    )
    nested = src / "examples" / "defect-repro-fix" / "registry"
    nested.mkdir(parents=True)
    (nested / "evidence.yaml").write_text("should: not ship\n", encoding="utf-8")

    builder = load_module("build_package_negative", BUILDER)
    builder.ROOT = src
    builder.DIST = tmp / "dist"
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        code = builder.main()
    assert code == 1, f"应被拒却退出 {code}\n{err.getvalue()}"
    assert "registry" in err.getvalue(), err.getvalue()
    archives = list((tmp / "dist").glob("*.tar.gz"))
    assert not archives, f"失败后仍留下归档：{archives}"
    return "打包脚本拒绝嵌套禁用资产并删除产物"


def case_nested_tests_dir(tmp: Path) -> str:
    """嵌套 tests/ 目录：打包脚本必须拒绝并删除产物。"""
    src = tmp / "pkg-src-tests"
    shutil.copytree(
        PKG,
        src,
        ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "work", "build"),
    )
    nested = src / "validators" / "tests"
    nested.mkdir(parents=True)
    (nested / "leak.md").write_text("internal evidence\n", encoding="utf-8")

    builder = load_module("build_package_negative_tests", BUILDER)
    builder.ROOT = src
    builder.DIST = tmp / "dist-tests"
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        code = builder.main()
    assert code == 1, f"应被拒却退出 {code}\n{err.getvalue()}"
    assert "tests" in err.getvalue(), err.getvalue()
    archives = list((tmp / "dist-tests").glob("*.tar.gz"))
    assert not archives, f"失败后仍留下归档：{archives}"
    return "打包脚本拒绝任意层级的 tests/ 并删除产物"


def case_version_literal_dup(tmp: Path) -> str:
    """README 里重复版本字面量：打包脚本反向断言必须拦住。"""
    src = tmp / "pkg-src-version"
    shutil.copytree(
        PKG,
        src,
        ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "work", "build"),
    )
    version = re.search(
        r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$',
        (src / "SKILL.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    ).group(1)
    readme = src / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + f"\n> 版本 {version}\n", encoding="utf-8"
    )

    builder = load_module("build_package_negative_version", BUILDER)
    builder.ROOT = src
    builder.DIST = tmp / "dist-version"
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        code = builder.main()
    assert code == 1, f"应被拒却退出 {code}\n{err.getvalue()}"
    assert "版本字面量" in err.getvalue(), err.getvalue()
    archives = list((tmp / "dist-version").glob("*.tar.gz"))
    assert not archives, f"失败后仍留下归档：{archives}"
    return "打包脚本拒绝 README 里重复的版本号"


CASES = [
    case_empty_test_and_patch,
    case_silent_failure,
    case_composite_command,
    case_phase2_or_true,
    case_test_constant_patch,
    case_blocker_port,
    case_nested_forbidden_asset,
    case_nested_tests_dir,
    case_version_literal_dup,
]


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory(prefix="se-negative-") as raw:
        root = Path(raw)
        for i, case in enumerate(CASES, 1):
            case_dir = root / f"case-{i}"
            case_dir.mkdir()
            try:
                detail = case(case_dir)
            except AssertionError as exc:
                failures += 1
                print(f"FAIL  {case.__name__}: {exc}")
            except Exception as exc:  # 用例自身写错也要显式失败
                failures += 1
                print(f"ERROR {case.__name__}: {type(exc).__name__}: {exc}")
            else:
                print(f"BLOCKED  {case.__name__}: {detail}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} 个负向用例被拦住")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
