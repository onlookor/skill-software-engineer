#!/usr/bin/env python3
"""正向用例：证明「真修复不会被误杀」。

覆盖两类此前会被 V08 误判的场景：
  - 断言写在 subprocess 子脚本里（父进程只转发退出码）；
  - 断言写在 threading.Thread 里（异常由测试自己收集后抛出）；
以及一条纯新增补丁（只加行、base 侧为空），证明它仍要过变异检验。

用法（仓库根目录）：
    python3 skills/software-engineering/tests/positive/run_positive.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "negative"))

from run_negative import (  # noqa: E402
    commit_all,
    init_repo,
    run_validator,
    write_config,
    write_repro_and_meta,
    write_verify,
)

ALL = ["V01", "V02", "V03", "V04", "V05", "V06", "V07", "V08"]


def write_localization(repo: Path, diff_lines: int) -> None:
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - calc.py\n"
        f"estimated_touched_files: 1\nestimated_diff_lines: {diff_lines}\n---\n"
        "机制：加法实现写成了减法。\n",
        encoding="utf-8",
    )


def write_fix(repo: Path, test_name: str) -> str:
    (repo / "fix.patch").write_text(
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a - b\n"
        "+    return a + b\n",
        encoding="utf-8",
    )
    repro_cmd = f"python3 -I tests/{test_name}"
    return repro_cmd


def base_fixture(repo: Path) -> None:
    init_repo(repo)
    (repo / "calc.py").write_text(
        "def add(a, b):\n    return a - b\n", encoding="utf-8"
    )
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text(
        "import sys\nsys.exit(0)\n", encoding="utf-8"
    )


def case_thread_assertion(tmp: Path) -> str:
    """断言在子线程里：真修复必须能通过 V01–V08。"""
    repo = tmp / "thread"
    base_fixture(repo)
    (repo / "tests" / "repro_thread.py").write_text(
        "import sys, threading\n"
        "sys.path.insert(0, '.')\n"
        "from calc import add\n"
        "errors = []\n"
        "def work():\n"
        "    try:\n"
        "        assert add(1, 2) == 3, 'add broken'\n"
        "    except BaseException as exc:\n"
        "        errors.append(exc)\n"
        "thread = threading.Thread(target=work)\n"
        "thread.start()\n"
        "thread.join()\n"
        "if errors:\n"
        "    raise errors[0]\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    repro_cmd = write_fix(repo, "repro_thread.py")
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_thread.py")
    write_localization(repo, 2)
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "thread-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ALL)
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"真修复被误杀：退出 {res.returncode}\n{out}"
    return "子线程断言的真修复通过 V01–V08"


def case_subprocess_assertion(tmp: Path) -> str:
    """断言在子进程里：真修复必须能通过 V01–V08（覆盖率要能采到子进程）。"""
    repo = tmp / "subprocess"
    base_fixture(repo)
    (repo / "tests" / "child_check.py").write_text(
        "import sys\n"
        "sys.path.insert(0, '.')\n"
        "from calc import add\n"
        "assert add(1, 2) == 3, 'add broken'\n",
        encoding="utf-8",
    )
    (repo / "tests" / "repro_sub.py").write_text(
        "import subprocess, sys\n"
        "result = subprocess.run([sys.executable, 'tests/child_check.py'])\n"
        "assert result.returncode == 0, '子进程断言失败'\n"
        "sys.exit(result.returncode)\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    repro_cmd = write_fix(repo, "repro_sub.py")
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_sub.py")
    write_localization(repo, 2)
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "subprocess-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ALL)
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"真修复被误杀：退出 {res.returncode}\n{out}"
    return "子进程断言的真修复通过 V01–V08（子进程覆盖已合并）"


def case_pure_addition(tmp: Path) -> str:
    """纯新增补丁（base 侧为空）：新增守卫行必须过变异检验，真修复应通过。"""
    repo = tmp / "pure-add"
    init_repo(repo)
    (repo / "calc.py").write_text(
        "def safe_div(a, b):\n    return a / b\n", encoding="utf-8"
    )
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text(
        "import sys\nsys.exit(0)\n", encoding="utf-8"
    )
    (repo / "tests" / "repro_div.py").write_text(
        "import sys\n"
        "sys.path.insert(0, '.')\n"
        "from calc import safe_div\n"
        "try:\n"
        "    safe_div(1, 0)\n"
        "except ValueError:\n"
        "    pass\n"
        "else:\n"
        "    raise AssertionError('expected ValueError')\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,2 +1,4 @@\n"
        " def safe_div(a, b):\n"
        "+    if b == 0:\n"
        "+        raise ValueError('b must not be zero')\n"
        "     return a / b\n",
        encoding="utf-8",
    )
    repro_cmd = "python3 -I tests/repro_div.py"
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_div.py")
    write_localization(repo, 2)
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "pure-add-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ALL)
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"纯新增真修复被误杀：退出 {res.returncode}\n{out}"
    return "纯新增补丁通过覆盖与变异检验"


CASES = [case_thread_assertion, case_subprocess_assertion, case_pure_addition]


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory(prefix="se-positive-") as raw:
        root = Path(raw)
        for i, case in enumerate(CASES, 1):
            case_dir = root / f"case-{i}"
            case_dir.mkdir()
            try:
                detail = case(case_dir)
            except AssertionError as exc:
                failures += 1
                print(f"FAIL  {case.__name__}: {exc}")
            except Exception as exc:
                failures += 1
                print(f"ERROR {case.__name__}: {type(exc).__name__}: {exc}")
            else:
                print(f"PASS  {case.__name__}: {detail}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} 个正向用例通过")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
