#!/usr/bin/env python3
"""示例：缺陷复现—最小修复的一次完整闭环。

一条命令：
    python3 skills/software-engineering/examples/defect-repro-fix/run.py

脚本在 work/ 下重建一个临时 git 仓（真 bug＋既有测试），按 S1→S2→S3 的顺序
生成交付物，并在正确的状态点调用 validators/validate.py 的 V01–V08。
任何一条自动检查非 0，脚本以非 0 退出。V09 是人工清单，本脚本不跑。
"""
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import pathlib
import shutil
import subprocess
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
SKILL_DIR = HERE.parent.parent
VALIDATE = SKILL_DIR / "validators" / "validate.py"
CONFIG = HERE / "config.yaml"
WORK = HERE / "work"

_spec = importlib.util.spec_from_file_location("skill_validate", VALIDATE)
_v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v)


def sh(cmd: str, *, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        cmd, shell=True, cwd=str(WORK), capture_output=True, text=True, timeout=120
    )
    if check and proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
        raise SystemExit(f"命令失败：{cmd}")
    return proc


def run_validator(vid: str) -> int:
    proc = subprocess.run(
        [sys.executable, str(VALIDATE), "--config", str(CONFIG), "--only", vid],
        cwd=str(HERE), capture_output=True, text=True, timeout=180,
    )
    print(proc.stdout.rstrip())
    if proc.returncode != 0:
        print(f"  [exit={proc.returncode}]")
    return proc.returncode


def clear_caches() -> None:
    for d in (WORK / "__pycache__", WORK / "tests" / "__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def main() -> int:
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    repro_cmd = "python3 -I tests/repro_add.py"
    test_cmd = cfg["test_command"]
    timeout = cfg["repro_timeout_seconds"]

    print(f"== 重建示例仓：{WORK}")
    if WORK.exists():
        shutil.rmtree(WORK)
    (WORK / "tests").mkdir(parents=True)
    shutil.copy(HERE / "base" / "calc.py", WORK / "calc.py")
    shutil.copy(HERE / "base" / "existing-tests" / "test_calc.py", WORK / "tests" / "test_calc.py")
    sh("git init -q")
    sh("git config user.email example@example.invalid")
    sh("git config user.name example")
    sh("git add calc.py tests/test_calc.py")
    sh("git commit -qm 'example base'")
    head = sh("git rev-parse HEAD").stdout.strip()
    print(f"   base commit={head}")

    shutil.copy(HERE / "artifacts" / "repro_add.py", WORK / "tests" / "repro_add.py")
    shutil.copy(HERE / "artifacts" / "run_all.py", WORK / "tests" / "run_all.py")
    shutil.copy(HERE / "artifacts" / "fix.patch", WORK / "fix.patch")
    shutil.copy(HERE / "artifacts" / "localization.md", WORK / "localization.md")

    # S1：连跑两次取失败摘要（期望值由 repro.md 声明，引导自行比对）
    observations = {"sum": 5}
    fingerprints, codes = [], []
    for _ in range(cfg["repro_runs"]):
        code, out = _v.run_command(repro_cmd, WORK, timeout, expected=observations)
        codes.append(code)
        fingerprints.append(_v.fingerprint(out, WORK))
    repro = {
        "repo": {"url": WORK.as_uri(), "commit": head},
        "env": {"os": "linux", "runtime": "python3", "dependencies": {}},
        "command": repro_cmd,
        "under_test": "calc.add",
        "observations": observations,
        "expected": "add(2, 3) 返回 5",
        "actual": "observation mismatch: sum expected=5 observed=-1",
        "exit_code": codes[0],
        "fingerprint": {"run1": fingerprints[0], "run2": fingerprints[1]},
        "first_observed": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    (WORK / "repro.md").write_text(
        "---\n" + yaml.safe_dump(repro, sort_keys=False, allow_unicode=True) + "---\n\n"
        "在 base 上单独运行失败用例，连续两次失败且失败摘要一致。\n",
        encoding="utf-8",
    )
    meta = {
        "file": "tests/repro_add.py",
        "test_id": "tests.repro_add.observe",
        "single_run_command": repro_cmd,
        "base_commit": head,
        "expected_failure": "observation mismatch: sum expected=5 observed=-1",
    }
    (WORK / "tests" / "repro_add.meta.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    failed: list[str] = []
    print("\n== S1 通过条件（补丁前）")
    for vid in ("V01", "V02", "V03"):
        if run_validator(vid) != 0:
            failed.append(vid)

    print("\n== S2 通过条件（补丁未应用）")
    for vid in ("V04", "V05", "V06"):
        if run_validator(vid) != 0:
            failed.append(vid)

    print("\n== S3 三段验证")

    def timed(cmd: str, label: str | None = None, expected: dict | None = None) -> dict:
        started = datetime.datetime.now().astimezone()
        if label is None:
            code, _out = _v.run_command(cmd, WORK, timeout, expected=expected)
        else:
            # 第②段在日志里记复合命令，但执行时两条命令分开跑：
            # 复合命令不能作为复现命令单独执行，也不允许拼接。
            first, _o1 = _v.run_command(repro_cmd, WORK, timeout, expected=expected)
            second, _o2 = _v.run_command(test_cmd, WORK, timeout)
            code = 0 if first == 0 and second == 0 else 1
        ended = datetime.datetime.now().astimezone()
        return {
            "command": label or cmd,
            "exit_code": code,
            "started_at": started.isoformat(timespec="seconds"),
            "duration": round((ended - started).total_seconds(), 3),
        }

    clear_caches()
    p1 = timed(repro_cmd, expected=observations)
    print(f"  第①段 base 复现失败：exit={p1['exit_code']}")
    sh("git apply fix.patch")
    clear_caches()
    print("  补丁已应用")
    if run_validator("V07") != 0:
        failed.append("V07")
    p2 = timed(repro_cmd, label=f"{repro_cmd} && {test_cmd}", expected=observations)
    print(f"  第②段 复现转绿且全量测试绿：exit={p2['exit_code']}")
    sh("git apply -R fix.patch")
    clear_caches()
    p3 = timed(repro_cmd, expected=observations)
    print(f"  第③段 撤补丁复败：exit={p3['exit_code']}")

    patch_sha = hashlib.sha256((WORK / "fix.patch").read_bytes()).hexdigest()
    verify = {
        "run_id": f"example-{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}",
        "commit": head,
        "patch_sha256": patch_sha,
        "test_command_used": test_cmd,
        "phases": [dict(phase=i, **p) for i, p in enumerate((p1, p2, p3), start=1)],
    }
    (WORK / "verify.log").write_text(
        yaml.safe_dump(verify, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (WORK / "fix-report.md").write_text(
        "---\n"
        f"status: fixed_unverified_root_cause\n"
        f"patch_sha256: {patch_sha}\n"
        "touched_files:\n  - calc.py\n"
        "evidence_kind: direct\n"
        "---\n\n"
        "三段验证已由 run.py 执行；V09 未复核，状态不升格为 fixed。\n",
        encoding="utf-8",
    )
    print("\n== S3 通过条件（日志已写）")
    if run_validator("V08") != 0:
        failed.append("V08")

    print("\n== 结果")
    if failed:
        print(f"fail: {', '.join(failed)}")
        return 1
    print("V01–V08 全 pass；V09 为人工清单，未执行")
    print(f"交付物保留在：{WORK}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
