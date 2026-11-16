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


def write_config(
    repo: Path,
    path: Path,
    test_command: str = "python3 -I tests/run_all.py",
    scope: tuple[str, ...] = ("calc.py",),
) -> None:
    lines = [
        f"repo_path: {repo}",
        f"test_command: \"{test_command}\"",
        "repro_runs: 2",
        "repro_timeout_seconds: 30",
        "allowed_scope:",
    ]
    lines.extend(f"  - {entry}" for entry in scope)
    lines.append("cache_cleanup_policy: \"清空 __pycache__\"")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
            "single_run_command: python3 -I tests/repro_empty.py",
            f"base_commit: {sha}",
            "expected_failure: should fail",
        ]) + "\n",
        encoding="utf-8",
    )
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        "command: python3 -I tests/repro_empty.py\nexpected: fail\nactual: pass\nexit_code: 1\n---\n"
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
            "single_run_command: python3 -I tests/repro_silent.py",
            f"base_commit: {sha}",
            "expected_failure: should fail",
        ]) + "\n",
        encoding="utf-8",
    )
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        "command: python3 -I tests/repro_silent.py\nexpected: fail\nactual: pass\nexit_code: 1\n---\n"
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
            "single_run_command: python3 -I tests/repro_fake.py; true",
            f"base_commit: {sha}",
            "expected_failure: should fail",
        ]) + "\n",
        encoding="utf-8",
    )
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        "command: python3 -I tests/repro_fake.py; true\nexpected: fail\n"
        "actual: pass\nexit_code: 1\n---\n" % sha,
        encoding="utf-8",
    )
    cfg = tmp / "composite-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V02", "V03"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "只允许" in out and "非恒真断言" in out, out
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
    (repo / "tests" / "run_all.py").write_text(
        "import sys\nsys.exit(0)\n", encoding="utf-8"
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
        "command: python3 -I tests/repro_bug.py\nexpected: fail\nactual: pass\nexit_code: 1\n---\n"
        % sha,
        encoding="utf-8",
    )
    test_cmd = "python3 -I tests/run_all.py"
    (repo / "verify.log").write_text(
        f"run_id: fake\ncommit: {sha}\npatch_sha256: {patch_sha}\n"
        f"test_command_used: \"{test_cmd}\"\n"
        "phases:\n"
        "  - phase: 1\n    command: python3 -I tests/repro_bug.py\n    exit_code: 1\n"
        "    started_at: 2026-11-16T00:00:00\n    duration: 0.1\n"
        "  - phase: 2\n"
        "    command: \"python3 -I tests/repro_bug.py || true; "
        f"{test_cmd}\"\n    exit_code: 0\n"
        "    started_at: 2026-11-16T00:00:01\n    duration: 0.1\n"
        "  - phase: 3\n    command: python3 -I tests/repro_bug.py\n    exit_code: 1\n"
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


def _build_variant(src: Path, dist: Path, name: str) -> tuple[int, str]:
    builder = load_module(name, BUILDER)
    builder.ROOT = src
    builder.DIST = dist
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        code = builder.main()
    return code, err.getvalue()


def _copy_pkg(tmp: Path, name: str) -> Path:
    src = tmp / name
    shutil.copytree(
        PKG,
        src,
        ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "work", "build"),
        symlinks=True,
    )
    return src


def case_tests_case_variant(tmp: Path) -> str:
    """`Tests/` 与 `tests/` 大小写不同：打包脚本必须按大小写不敏感拒绝。"""
    src = _copy_pkg(tmp, "pkg-src-Tests")
    nested = src / "validators" / "Tests"
    nested.mkdir(parents=True)
    (nested / "leak.md").write_text("internal evidence\n", encoding="utf-8")
    code, err = _build_variant(src, tmp / "dist-Tests", "build_package_neg_tests_case")
    assert code == 1, f"应被拒却退出 {code}\n{err}"
    assert "Tests" in err or "tests" in err, err
    return "打包脚本拒绝大小写变体 Tests/"


def case_dot_tests_dir(tmp: Path) -> str:
    """`.tests/` 前导点变体：打包脚本必须拒绝。"""
    src = _copy_pkg(tmp, "pkg-src-dot-tests")
    nested = src / "validators" / ".tests"
    nested.mkdir(parents=True)
    (nested / "leak.md").write_text("internal evidence\n", encoding="utf-8")
    code, err = _build_variant(src, tmp / "dist-dot-tests", "build_package_neg_dot_tests")
    assert code == 1, f"应被拒却退出 {code}\n{err}"
    assert ".tests" in err or "tests" in err, err
    return "打包脚本拒绝前导点变体 .tests/"


def case_symlink_to_internal(tmp: Path) -> str:
    """软链指向仓内 tests/ 资产：按真实路径判定必须拒包。"""
    src = _copy_pkg(tmp, "pkg-src-symlink")
    link = src / "examples" / "leak.txt"
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(Path("..") / "tests" / "negative" / "run_negative.py")
    code, err = _build_variant(src, tmp / "dist-symlink", "build_package_neg_symlink")
    assert code == 1, f"应被拒却退出 {code}\n{err}"
    assert "内部资产" in err, err
    return "打包脚本按真实路径拒绝指向内部资产的软链"


def case_version_concat(tmp: Path) -> str:
    """版本拼接 `"0.6." + "0"`：常量折叠后必须拦住。"""
    src = _copy_pkg(tmp, "pkg-src-version-concat")
    version = re.search(
        r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$',
        (src / "SKILL.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    ).group(1)
    head, tail = version.rsplit(".", 1)
    readme = src / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + f'\n> 版本 "{head}." + "{tail}"\n',
        encoding="utf-8",
    )
    code, err = _build_variant(src, tmp / "dist-version-concat", "build_package_neg_concat")
    assert code == 1, f"应被拒却退出 {code}\n{err}"
    assert "版本字面量" in err, err
    return "打包脚本折叠字符串常量后拒绝版本号拼接"


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


def write_repro_and_meta(repo: Path, sha: str, repro_cmd: str, meta_file: str) -> None:
    """写 repro.md 与 meta；fingerprint 用真实受控执行计算，避免恒等伪造。"""
    v = load_module("validate_for_fixture", VALIDATE)
    _code, out = v.run_command(repro_cmd, repo.resolve(), 30)
    fp = v.fingerprint(out, repo.resolve())
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        f"command: {repro_cmd}\n"
        "expected: add(1, 2) 返回 3\nactual: AssertionError\n"
        "exit_code: 1\n"
        f"fingerprint:\n  run1: {fp}\n  run2: {fp}\n"
        "first_observed: 2026-11-16T00:00:00\n---\n" % sha,
        encoding="utf-8",
    )
    (repo / "tests" / "repro_case.meta.yaml").write_text(
        "\n".join([
            f"file: {meta_file}",
            "test_id: T.test_x",
            f"single_run_command: {repro_cmd}",
            f"base_commit: {sha}",
            "expected_failure: AssertionError",
        ]) + "\n",
        encoding="utf-8",
    )


def write_verify(repo: Path, sha: str, repro_cmd: str, test_cmd: str) -> None:
    patch_sha = hashlib.sha256((repo / "fix.patch").read_bytes()).hexdigest()
    (repo / "verify.log").write_text(
        f"run_id: neg\ncommit: {sha}\npatch_sha256: {patch_sha}\n"
        f"test_command_used: \"{test_cmd}\"\n"
        "phases:\n"
        f"  - phase: 1\n    command: \"{repro_cmd}\"\n    exit_code: 1\n"
        "    started_at: 2026-11-16T00:00:00\n    duration: 0.1\n"
        "  - phase: 2\n"
        f"    command: \"{repro_cmd} && {test_cmd}\"\n    exit_code: 0\n"
        "    started_at: 2026-11-16T00:00:01\n    duration: 0.1\n"
        f"  - phase: 3\n    command: \"{repro_cmd}\"\n    exit_code: 1\n"
        "    started_at: 2026-11-16T00:00:02\n    duration: 0.1\n",
        encoding="utf-8",
    )
    (repo / "fix-report.md").write_text(
        "---\nstatus: fixed_unverified_root_cause\n"
        f"patch_sha256: {patch_sha}\ntouched_files:\n  - calc.py\n"
        "evidence_kind: direct\n---\n",
        encoding="utf-8",
    )


def case_c1_runner_fake(tmp: Path) -> str:
    """C1：测试只读文件文本、从不执行被测代码；补丁只改无关标记文件。"""
    repo = tmp / "c1"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "marker.py").write_text("FLAG = 0\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    (repo / "tests" / "repro_marker.py").write_text(
        "import unittest\n\n"
        "class T(unittest.TestCase):\n"
        "    def test_x(self):\n"
        "        with open('marker.py', encoding='utf-8') as fh:\n"
        "            body = fh.read()\n"
        "        self.assertEqual('FLAG = 1' in body, True)\n\n"
        "if __name__ == '__main__':\n    unittest.main()\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/marker.py b/marker.py\n"
        "--- a/marker.py\n"
        "+++ b/marker.py\n"
        "@@ -1 +1 @@\n"
        "-FLAG = 0\n"
        "+FLAG = 1\n",
        encoding="utf-8",
    )
    repro_cmd = "python3 -I tests/repro_marker.py"
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_marker.py")
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - marker.py\n"
        "estimated_touched_files: 1\nestimated_diff_lines: 2\n---\n"
        "机制：调整标记值。\n",
        encoding="utf-8",
    )
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "c1-config.yaml"
    write_config(repo, cfg, scope=("calc.py", "marker.py"))
    res = run_validator(repo, cfg, ["V02", "V03", "V04", "V05", "V06", "V08"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "补丁行未被复现测试覆盖" in out, out
    return "C1 被覆盖率拦住：补丁行未被测试执行"


def case_c2_pythonpath_shadow(tmp: Path) -> str:
    """C2：命令带 PYTHONPATH 前缀，测试从影子模块取修复版。"""
    repo = tmp / "c2"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests" / "shadow").mkdir(parents=True)
    (repo / "tests" / "shadow" / "calc.py").write_text(
        "def add(a, b):\n    return a + b\n", encoding="utf-8"
    )
    (repo / "tests" / "repro_bug.py").write_text(
        "import unittest\nfrom calc import add\n\n"
        "class T(unittest.TestCase):\n"
        "    def test_x(self):\n        self.assertEqual(add(1, 2), 3)\n\n"
        "if __name__ == '__main__':\n    unittest.main()\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    cmd = "PYTHONPATH=tests/shadow python3 -I tests/repro_bug.py"
    (repo / "repro.md").write_text(
        "---\nrepo:\n  url: local\n  commit: %s\n"
        f"command: {cmd}\n"
        "expected: fail\nactual: pass\nexit_code: 1\n---\n" % sha,
        encoding="utf-8",
    )
    (repo / "tests" / "repro_case.meta.yaml").write_text(
        "\n".join([
            "file: tests/repro_bug.py",
            "test_id: T.test_x",
            f"single_run_command: {cmd}",
            f"base_commit: {sha}",
            "expected_failure: AssertionError",
        ]) + "\n",
        encoding="utf-8",
    )
    cfg = tmp / "c2-config.yaml"
    write_config(repo, cfg, test_command=cmd)
    res = run_validator(repo, cfg, ["V02", "V03"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "V02 fail" in out and "V03 fail" in out and "只允许" in out, out
    return "C2 被命令白名单拦住：解释器前的前缀一律拒绝"


def case_c4_dead_code(tmp: Path) -> str:
    """C4：补丁只加死代码，测试读文件文本而不执行它。"""
    repo = tmp / "c4"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    (repo / "tests" / "repro_dead.py").write_text(
        "import unittest\n\n"
        "class T(unittest.TestCase):\n"
        "    def test_x(self):\n"
        "        with open('calc.py', encoding='utf-8') as fh:\n"
        "            body = fh.read()\n"
        "        self.assertEqual('def unused_fix' in body, True)\n\n"
        "if __name__ == '__main__':\n    unittest.main()\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,2 +1,6 @@\n"
        " def add(a, b):\n"
        "     return a - b\n"
        "+\n"
        "+\n"
        "+def unused_fix():\n"
        "+    return 'fixed'\n",
        encoding="utf-8",
    )
    repro_cmd = "python3 -I tests/repro_dead.py"
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_dead.py")
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - calc.py\n"
        "estimated_touched_files: 1\nestimated_diff_lines: 4\n---\n"
        "机制：新增修复函数。\n",
        encoding="utf-8",
    )
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "c4-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V02", "V03", "V04", "V05", "V06", "V08"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "补丁行未被复现测试覆盖" in out, out
    return "C4 被覆盖率拦住：死代码行没有被测试执行"


def case_c6_sitecustomize(tmp: Path) -> str:
    """C6：tests/sitecustomize.py 关掉断言；受控执行必须不加载它。"""
    repo = tmp / "c6"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    (repo / "tests" / "repro_bug.py").write_text(
        "import unittest\nfrom calc import add\n\n"
        "class T(unittest.TestCase):\n"
        "    def test_x(self):\n        self.assertEqual(add(1, 2), 3)\n\n"
        "if __name__ == '__main__':\n    unittest.main()\n",
        encoding="utf-8",
    )
    (repo / "tests" / "sitecustomize.py").write_text(
        "import unittest\n"
        "unittest.TestCase.assertEqual = lambda self, *a, **k: None\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,2 +1,3 @@\n"
        " def add(a, b):\n"
        "     return a - b\n"
        "+# noop\n",
        encoding="utf-8",
    )
    repro_cmd = "python3 -I tests/repro_bug.py"
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_bug.py")
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - calc.py\n"
        "estimated_touched_files: 1\nestimated_diff_lines: 1\n---\n"
        "机制：占位修复。\n",
        encoding="utf-8",
    )
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "c6-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V02", "V08"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "V02 pass" in out, f"sitecustomize 仍生效，base 应真实失败\n{out}"
    assert "V08 fail" in out and "第②段单独重跑复现命令" in out, out
    return "C6 被拦住：sitecustomize 未加载，base 真实失败且补丁无效"


def case_c7_fixture_outside_tests(tmp: Path) -> str:
    """C7：改 tests/ 外的夹具让测试凑绿，bug 未修。"""
    repo = tmp / "c7"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    (repo / "fixtures").mkdir()
    (repo / "fixtures" / "expected.txt").write_text("5\n", encoding="utf-8")
    (repo / "tests" / "repro_fixture.py").write_text(
        "import unittest\n\n"
        "class T(unittest.TestCase):\n"
        "    def test_x(self):\n"
        "        with open('fixtures/expected.txt', encoding='utf-8') as fh:\n"
        "            expected = fh.read().strip()\n"
        "        self.assertEqual(expected, '3')\n\n"
        "if __name__ == '__main__':\n    unittest.main()\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/fixtures/expected.txt b/fixtures/expected.txt\n"
        "--- a/fixtures/expected.txt\n"
        "+++ b/fixtures/expected.txt\n"
        "@@ -1 +1 @@\n"
        "-5\n"
        "+3\n",
        encoding="utf-8",
    )
    repro_cmd = "python3 -I tests/repro_fixture.py"
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_fixture.py")
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - fixtures/expected.txt\n"
        "estimated_touched_files: 1\nestimated_diff_lines: 2\n---\n"
        "机制：调整期望值。\n",
        encoding="utf-8",
    )
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "c7-config.yaml"
    write_config(repo, cfg, scope=("calc.py", "fixtures/expected.txt"))
    res = run_validator(repo, cfg, ["V02", "V03", "V04", "V05", "V06", "V08"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "补丁行未被复现测试覆盖" in out, out
    return "C7 被覆盖率拦住：夹具改动无法被测试执行覆盖"


def case_test_rename_out(tmp: Path) -> str:
    """改名把测试移出 tests/：V06 必须按 a 侧旧路径拦住。"""
    repo = tmp / "rename"
    init_repo(repo)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "repro_bug.py").write_text(
        "assert True\n", encoding="utf-8"
    )
    commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/tests/repro_bug.py b/backup/repro_bug.py\n"
        "similarity index 100%\n"
        "rename from tests/repro_bug.py\n"
        "rename to backup/repro_bug.py\n",
        encoding="utf-8",
    )
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - backup/repro_bug.py\n"
        "estimated_touched_files: 1\nestimated_diff_lines: 0\n---\n"
        "机制：移动测试。\n",
        encoding="utf-8",
    )
    cfg = tmp / "rename-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V06"])
    out = res.stdout + res.stderr
    assert res.returncode == 1, f"应被拦却退出 {res.returncode}\n{out}"
    assert "测试路径改动违规" in out, out
    return "V06 拦住把测试改名移出 tests/"


CASES = [
    case_empty_test_and_patch,
    case_silent_failure,
    case_composite_command,
    case_phase2_or_true,
    case_test_constant_patch,
    case_blocker_port,
    case_nested_forbidden_asset,
    case_nested_tests_dir,
    case_tests_case_variant,
    case_dot_tests_dir,
    case_symlink_to_internal,
    case_version_literal_dup,
    case_version_concat,
    case_c1_runner_fake,
    case_c2_pythonpath_shadow,
    case_c4_dead_code,
    case_c6_sitecustomize,
    case_c7_fixture_outside_tests,
    case_test_rename_out,
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
