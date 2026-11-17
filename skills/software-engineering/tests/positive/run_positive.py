#!/usr/bin/env python3
"""正向用例：证明「真修复不会被误杀」。

覆盖：
  - 断言写在 threading.Thread 里（异常由测试自己收集后抛出）；
  - 纯新增补丁（只加行、base 侧为空），新增守卫行仍要过变异检验；
  - 正常使用 `import` 与 `from ... import` 的测试放行；
  - 合法的函数体内修复（改 return 行、加守卫行）不被结构规则误杀。

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
    """断言在子进程里：复现测试白名单不允许 subprocess，本用例必须被拒。"""
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
    assert res.returncode == 1, f"含 subprocess 的复现测试未被白名单拦住：退出 {res.returncode}\n{out}"
    assert "白名单" in out and "subprocess" in out, out
    return "复现测试白名单拦住 subprocess"


def case_import_forms(tmp: Path) -> str:
    """正常 import 与 from ... import：白名单必须放行，函数体内修复必须通过。"""
    repo = tmp / "import-forms"
    base_fixture(repo)
    (repo / "tests" / "repro_imports.py").write_text(
        "import sys\n"
        "sys.path.insert(0, '.')\n"
        "import calc\n"
        "from calc import add\n"
        "assert add(1, 2) == 3, 'add broken'\n"
        "assert calc.add(2, 3) == 5, 'calc.add broken'\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    repro_cmd = write_fix(repo, "repro_imports.py")
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_imports.py")
    write_localization(repo, 2)
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "import-forms-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ALL)
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"正常 import 的真修复被误杀：退出 {res.returncode}\n{out}"
    return "正常 import 与 from import 的测试通过白名单与全部检查"


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
        "except BaseException as exc:\n"
        "    raise AssertionError('unexpected %s' % type(exc).__name__) from exc\n"
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


def case_two_change_points(tmp: Path) -> str:
    """B3b：两个改点落在同一个 hunk、中间隔两行上下文，不得误报无法定位删除块。"""
    repo = tmp / "two-points"
    init_repo(repo)
    (repo / "calc.py").write_text(
        "def add(a, b):\n"
        "    return a - b\n"
        "\n"
        "def mul(a, b):\n"
        "    return a / b\n",
        encoding="utf-8",
    )
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text(
        "import sys\nsys.exit(0)\n",
        encoding="utf-8",
    )
    (repo / "tests" / "repro_both.py").write_text(
        "import sys\nsys.path.insert(0, '.')\n"
        "from calc import add, mul\n"
        "assert add(1, 2) == 3, 'add broken'\n"
        "assert mul(2, 3) == 6, 'mul broken'\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    repro_cmd = "python3 -I tests/repro_both.py"
    (repo / "fix.patch").write_text(
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,5 +1,5 @@\n"
        " def add(a, b):\n"
        "-    return a - b\n"
        "+    return a + b\n"
        " \n"
        " def mul(a, b):\n"
        "-    return a / b\n"
        "+    return a * b\n",
        encoding="utf-8",
    )
    write_repro_and_meta(repo, sha, repro_cmd, "tests/repro_both.py")
    write_localization(repo, 4)
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "two-points-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ALL)
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"同一 hunk 双改点的真修复被误杀：退出 {res.returncode}\n{out}"
    assert "无法定位删除块" not in out, out
    return "同一 hunk 内两个改动块分别回退，变异检验通过"


CASES = [
    case_thread_assertion,
    case_subprocess_assertion,
    case_import_forms,
    case_pure_addition,
    case_two_change_points,
]


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
