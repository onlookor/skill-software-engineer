#!/usr/bin/env python3
"""打包技能分发件：白名单复制 → 清单 → 归档 → 反向断言。

只用标准库。版本号从 SKILL.md 的 frontmatter 读取，不另设来源。

用法（仓库根目录）：
    python3 skills/software-engineering/scripts/build_package.py

退出码：0＝完成；1＝清单缺失、版本非法或归档含禁用项（并删除本次产物）。
"""
from __future__ import annotations

import hashlib
import re
import shutil
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT.parent.parent / "dist"

INCLUDE_FILES = ("README.md", "SKILL.md", "PACKAGING.md", "BACKFLOW.md")
INCLUDE_DIRS = ("stages", "schemas", "validators", "examples")

EXCLUDE_DIR_NAMES = {"__pycache__", ".git", "work", "dist", "build", ".pytest_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}

# 递归禁用：这些名字出现在归档的任意层级都判失败（仓库内部资产与内部证据）。
# tests 也在其中：内部测试证据不随包分发；示例仓需要模拟「既有测试」的夹具
# 命名为 base/existing-tests/，因此不需要为 tests 开例外。
FORBIDDEN_ANYWHERE = {
    "registry", "pilot", "adr", "archieve", "pact", "scripts", "tests",
    "run-log", "run_log", "anchor_baseline.json",
    "软件工程元框架成文法.md", "软件工程元框架成文法-changlog.md",
    "编译规范.md", "编译规范-changlog.md", "changelog.md",
}

# 版本字面量只允许出现在这两处：唯一来源 SKILL.md 与打包时生成的清单。
VERSION_LITERAL_ALLOWED = {"SKILL.md", "PACKAGE-MANIFEST.txt"}


def fail(msg: str, staging: Path | None = None) -> int:
    if staging is not None and staging.exists():
        shutil.rmtree(staging)
    sys.stderr.write(f"打包失败：{msg}\n")
    return 1


def read_version() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', text, re.MULTILINE)
    if not m:
        raise SystemExit("打包失败：SKILL.md 缺合法的 version（应为 X.Y.Z）")
    return m.group(1)


def iter_files() -> list[Path]:
    files: list[Path] = []
    for name in INCLUDE_FILES:
        p = ROOT / name
        if not p.is_file():
            raise SystemExit(f"打包失败：白名单文件缺失：{name}")
        files.append(p)
    for d in INCLUDE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            raise SystemExit(f"打包失败：白名单目录缺失：{d}/")
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if any(part in EXCLUDE_DIR_NAMES for part in p.relative_to(ROOT).parts):
                continue
            if p.suffix in EXCLUDE_SUFFIXES:
                continue
            files.append(p)
    return files


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    version = read_version()
    pkg_name = f"software-engineering-{version}"
    staging = DIST / pkg_name
    archive = DIST / f"{pkg_name}.tar.gz"
    digest_file = DIST / f"{pkg_name}.tar.gz.sha256"

    DIST.mkdir(parents=True, exist_ok=True)
    for stale in (staging, archive, digest_file):
        if stale.is_dir():
            shutil.rmtree(stale)
        elif stale.exists():
            stale.unlink()

    source_files = iter_files()
    for src in source_files:
        rel = src.relative_to(ROOT)
        target = staging / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)

    manifest = [f"package: {pkg_name}", f"version: {version}", "files:"]
    for src in source_files:
        rel = src.relative_to(ROOT)
        manifest.append(f"{sha256(src)}  {rel.as_posix()}")
    (staging / "PACKAGE-MANIFEST.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")

    with tarfile.open(archive, "w:gz") as tar:
        for p in sorted(staging.rglob("*")):
            if not p.is_file():
                continue
            arcname = f"{pkg_name}/{p.relative_to(staging).as_posix()}"
            info = tar.gettarinfo(str(p), arcname=arcname)
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            with p.open("rb") as fh:
                tar.addfile(info, fh)

    with tarfile.open(archive, "r:gz") as tar:
        packaged = [Path(m.name).relative_to(pkg_name) for m in tar.getmembers() if m.isfile()]

    # 递归遍历整棵树：内部资产与 tests/ 出现在任意层级都拒绝。
    hits = sorted({
        token
        for rel in packaged
        for token in (
            [part for part in rel.parts if part in FORBIDDEN_ANYWHERE]
            + [part for part in rel.parts if part in {"__pycache__", "work"}]
        )
    })
    if hits:
        archive.unlink(missing_ok=True)
        return fail("归档含禁用项：" + ", ".join(hits), staging)

    # 版本号单一来源：除 SKILL.md 与 PACKAGE-MANIFEST.txt 外，包内任何文件
    # 出现当前版本字面量都判失败，防止 README／PACKAGING 又长出第二份版本号。
    dup_version = sorted(
        rel.as_posix()
        for rel in packaged
        if rel.as_posix() not in VERSION_LITERAL_ALLOWED
        and version in (staging / rel).read_text(encoding="utf-8", errors="replace")
    )
    if dup_version:
        archive.unlink(missing_ok=True)
        return fail(
            f"版本字面量 {version} 只允许出现在 SKILL.md 与 PACKAGE-MANIFEST.txt，"
            "以下文件重复了版本号：" + ", ".join(dup_version),
            staging,
        )

    digest = sha256(archive)
    digest_file.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")

    print(f"版本：{version}")
    print(f"目录：{staging}（{len(packaged)} 个文件，含 PACKAGE-MANIFEST.txt）")
    print(f"归档：{archive}")
    print(f"校验：{digest_file}  sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
