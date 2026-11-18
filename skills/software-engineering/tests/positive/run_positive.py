#!/usr/bin/env python3
"""正向用例：证明「真修复不会被误杀」。

覆盖：
  - 点号方法入口（`calc.Calc.add`）的真修复能通过全部检查；
  - 纯新增补丁（只加行、base 侧为空），新增行仍要过变异检验；
  - 正常使用 `import` 与 `from ... import` 的测试放行；
  - 合法的函数体内修复（改 return 行、加守卫行）不被结构规则误杀；
  - 越界的 subprocess 复现测试仍被白名单拒绝。

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


def case_method_entry(tmp: Path) -> str:
    """点号方法入口的真修复必须能通过 V01–V08（含变异检验）。"""
    repo = tmp / "method"
    init_repo(repo)
    (repo / "calc.py").write_text(
        "class Calc:\n"
        "    def add(self, a, b):\n"
        "        return a - b\n",
        encoding="utf-8",
    )
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text(
        "import sys\nsys.exit(0)\n", encoding="utf-8"
    )
    (repo / "tests" / "repro_method.py").write_text(
        "import sys\n"
        "sys.path.insert(0, '.')\n"
        "from calc import Calc\n\n"
        "def observe():\n"
        "    return {'sum': Calc().add(1, 2)}\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,3 +1,3 @@\n"
        " class Calc:\n"
        "     def add(self, a, b):\n"
        "-        return a - b\n"
        "+        return a + b\n",
        encoding="utf-8",
    )
    repro_cmd = "python3 -I tests/repro_method.py"
    write_repro_and_meta(
        repo, sha, repro_cmd, "tests/repro_method.py",
        "calc.Calc.add", observations={"sum": 3},
    )
    write_localization(repo, 2)
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "method-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ALL)
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"方法入口的真修复被误杀：退出 {res.returncode}\n{out}"
    return "点号方法入口的真修复通过 V01–V08"


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
        "from calc import add\n\n"
        "def observe():\n"
        "    return {'sum': add(1, 2), 'total': calc.add(2, 3)}\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    repro_cmd = write_fix(repo, "repro_imports.py")
    write_repro_and_meta(
        repo, sha, repro_cmd, "tests/repro_imports.py",
        observations={"sum": 3, "total": 5},
    )
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
        "def status(code):\n    return 0\n", encoding="utf-8"
    )
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text(
        "import sys\nsys.exit(0)\n", encoding="utf-8"
    )
    (repo / "tests" / "repro_status.py").write_text(
        "import sys\n"
        "sys.path.insert(0, '.')\n"
        "from calc import status\n\n"
        "def observe():\n"
        "    return {'status': status(404)}\n",
        encoding="utf-8",
    )
    sha = commit_all(repo)
    (repo / "fix.patch").write_text(
        "diff --git a/calc.py b/calc.py\n"
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -1,2 +1,4 @@\n"
        " def status(code):\n"
        "+    if code == 404:\n"
        "+        return -1\n"
        "     return 0\n",
        encoding="utf-8",
    )
    repro_cmd = "python3 -I tests/repro_status.py"
    write_repro_and_meta(
        repo, sha, repro_cmd, "tests/repro_status.py",
        "calc.status", observations={"status": -1},
    )
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
        "from calc import add, mul\n\n"
        "def observe():\n"
        "    return {'sum': add(1, 2), 'product': mul(2, 3)}\n",
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
    write_repro_and_meta(
        repo, sha, repro_cmd, "tests/repro_both.py", ["calc.add", "calc.mul"],
        observations={"sum": 3, "product": 6},
    )
    write_localization(repo, 4)
    write_verify(repo, sha, repro_cmd, "python3 -I tests/run_all.py")
    cfg = tmp / "two-points-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ALL)
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"同一 hunk 双改点的真修复被误杀：退出 {res.returncode}\n{out}"
    assert "无法定位删除块" not in out, out
    return "同一 hunk 内两个改动块分别回退，变异检验通过"


def _unified(path: str, before: str, after: str) -> str:
    import difflib

    diff = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
            lineterm="",
        )
    )
    return f"diff --git a/{path} b/{path}\n" + "\n".join(diff) + "\n"


def _new_file(path: str, body: str) -> str:
    lines = body.splitlines()
    hunk = f"@@ -0,0 +1,{len(lines)} @@\n" + "".join("+" + l + "\n" for l in lines)
    return (
        f"diff --git a/{path} b/{path}\n"
        "new file mode 100644\n"
        "--- /dev/null\n"
        f"+++ b/{path}\n" + hunk
    )


def _changed_lines(patch: str) -> int:
    return sum(
        1
        for line in patch.splitlines()
        if line[:1] in ("+", "-") and not line.startswith(("+++", "---"))
    )


def case_declarative_shapes(tmp: Path) -> str:
    """V06 不得罚正确修复：模块常量、纯 import、类／dataclass 默认值、
    模块级 try/except 内赋值、新建生产模块都必须放行。"""
    repo = tmp / "declarative"
    init_repo(repo)
    before = (
        "import dataclasses\n"
        "import logging\n"
        "\n"
        "THRESHOLD = 9\n"
        'LOG = logging.getLogger("x")\n'
        "\n"
        "@dataclasses.dataclass\n"
        "class Config:\n"
        "    limit: int = 1\n"
        "\n"
        "class Box:\n"
        "    width = 1\n"
        "\n"
        "try:\n"
        "    import math\n"
        "except ImportError:\n"
        "    math = None\n"
        "\n"
        "def add(a, b):\n"
        "    return a - b\n"
    )
    after = (
        "import dataclasses\n"
        "import logging\n"
        "import math\n"
        "\n"
        "THRESHOLD = 2\n"
        'LOG = logging.getLogger("y")\n'
        "\n"
        "@dataclasses.dataclass\n"
        "class Config:\n"
        "    limit: int = 2\n"
        "\n"
        "class Box:\n"
        "    width = 2\n"
        "\n"
        "try:\n"
        "    import math\n"
        "except ImportError:\n"
        "    math = 0\n"
        "\n"
        "def add(a, b):\n"
        "    return math.floor(a + b)\n"
    )
    extra = (
        '"""extra helpers."""\n'
        "import dataclasses\n"
        "\n"
        "TAU = 6\n"
        "\n"
        "@dataclasses.dataclass\n"
        "class Point:\n"
        "    x: int = 0\n"
        "    y: int = 0\n"
        "\n"
        "class Holder:\n"
        "    value = 1\n"
        "\n"
        "def double(n):\n"
        "    return n * 2\n"
    )
    (repo / "calc.py").write_text(before, encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "run_all.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    (repo / "localization.md").write_text(
        "---\nevidence_kind: direct\nfiles:\n  - calc.py\n  - extra.py\n"
        f"estimated_touched_files: 2\nestimated_diff_lines: {_changed_lines(_unified('calc.py', before, after) + _new_file('extra.py', extra))}\n---\n"
        "机制：声明式改动。\n",
        encoding="utf-8",
    )
    patch = _unified("calc.py", before, after) + _new_file("extra.py", extra)
    (repo / "fix.patch").write_text(patch, encoding="utf-8")
    cfg = tmp / "declarative-config.yaml"
    write_config(repo, cfg)
    res = run_validator(repo, cfg, ["V06"])
    out = res.stdout + res.stderr
    assert res.returncode == 0, f"声明式正确修复被 V06 误杀：退出 {res.returncode}\n{out}"
    return "V06 放行模块常量、纯 import、类属性、dataclass 默认值、try 内赋值与新模块"


CASES = [
    case_method_entry,
    case_subprocess_assertion,
    case_import_forms,
    case_pure_addition,
    case_two_change_points,
    case_declarative_shapes,
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
