#!/usr/bin/env python3
"""打包技能分发件：白名单复制 → 清单 → 归档 → 反向断言。

只用标准库。版本号从 SKILL.md 的 frontmatter 读取，不另设来源。

用法（仓库根目录）：
    python3 skills/software-engineering/scripts/build_package.py

退出码：0＝完成；1＝清单缺失、版本非法或归档含禁用项（并删除本次产物）。
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import sys
import tarfile
import unicodedata
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


def normalize_name(part: str) -> str:
    """NFKC、去空白、大小写不敏感、忽略前导点：`Tests `／`.tests` 与 `tests` 等价。

    同形字目录（如 Cyrillic `tеsts`）不做字符映射，而是在 iter_files 里
    直接拒绝含非 ASCII 字符的路径分量。
    """
    part = unicodedata.normalize("NFKC", part)
    part = "".join(ch for ch in part if not ch.isspace())
    return part.casefold().lstrip(".")


FORBIDDEN_NORMALIZED = {normalize_name(x) for x in FORBIDDEN_ANYWHERE}
EXCLUDE_NORMALIZED = {normalize_name(x) for x in EXCLUDE_DIR_NAMES}


def fold_literals(text: str) -> str:
    """折叠字符串常量：去掉空白、引号、反斜杠与拼接号。

    `"0.7." + "0"`、`"0.7.""0"`、`("0.7." "0")` 折叠后都会露出完整版本号。
    """
    return re.sub(r'[\s"\'+\\]', "", text)


def unescape_literals(text: str) -> str:
    """把 \\xNN、\\uNNNN、\\NNN 转义还原成字符，堵住 `\\x30.7.0` 这类写法。"""

    def _one(match: re.Match) -> str:
        try:
            return chr(int(match.group(1), 16))
        except ValueError:
            return match.group(0)

    text = re.sub(r"\\x([0-9a-fA-F]{2})", _one, text)
    text = re.sub(r"\\u([0-9a-fA-F]{4})", _one, text)
    text = re.sub(r"\\([0-7]{3})", _one, text)
    return text


def version_views(raw: bytes, text: str) -> list[str]:
    """同一文件的多种读法：原文、转义还原、常量折叠、去花括号、UTF-16。"""
    views = [text, unescape_literals(text)]
    for base in list(views):
        folded = fold_literals(base)
        views.append(folded)
        views.append(folded.replace("{", "").replace("}", ""))
    try:
        views.append(raw.decode("utf-16"))
    except (UnicodeError, LookupError):
        pass
    return views


def contains_version(raw: bytes, text: str, version: str) -> bool:
    """版本号是否以内嵌/拼接/转义/UTF-16 形式出现。

    f-string 与 `format(...)` 可能把主次版本号拆开：只要文件里存在 `0.7`
    这类片段且同时出现构造语法，就视为重复，不试图求值。
    """
    major_minor = version.rsplit(".", 1)[0]
    construct = bool(
        re.search(r"\bformat\s*\(", text)
        or re.search(r"[rRbB]?f[\"']", text)
    )
    for view in version_views(raw, text):
        if version in view:
            return True
        if construct and major_minor in view:
            return True
    return False


class PackageError(Exception):
    """打包前检查失败；由 main 统一转为退出码 1。"""


def fail(msg: str, staging: Path | None = None) -> int:
    if staging is not None and staging.exists():
        shutil.rmtree(staging)
    sys.stderr.write(f"打包失败：{msg}\n")
    return 1


def read_version() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', text, re.MULTILINE)
    if not m:
        raise PackageError("SKILL.md 缺合法的 version（应为 X.Y.Z）")
    return m.group(1)


def iter_files() -> list[Path]:
    files: list[Path] = []
    root_real = ROOT.resolve()
    for name in INCLUDE_FILES:
        p = ROOT / name
        if not p.is_file():
            raise PackageError(f"白名单文件缺失：{name}")
        files.append(p)
    for d in INCLUDE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            raise PackageError(f"白名单目录缺失：{d}/")
        for p in sorted(base.rglob("*")):
            rel = p.relative_to(ROOT)
            # 软链与特殊文件必须显式判定，不能靠 is_file() 静默跳过：
            # 目录软链、断链、FIFO/设备文件一律拒收并写明「未入包」。
            if p.is_symlink():
                if not p.exists():
                    raise PackageError(f"{rel.as_posix()} 是断链，未入包")
                if p.is_dir():
                    raise PackageError(
                        f"{rel.as_posix()} 是指向目录的软链，未入包"
                    )
                if not p.is_file():
                    raise PackageError(
                        f"{rel.as_posix()} 是特殊文件（非普通文件），未入包"
                    )
            elif p.is_dir():
                continue
            elif not p.is_file():
                raise PackageError(
                    f"{rel.as_posix()} 是特殊文件（FIFO／设备／套接字），未入包"
                )
            if any(normalize_name(part) in EXCLUDE_NORMALIZED for part in rel.parts):
                continue
            if p.suffix in EXCLUDE_SUFFIXES:
                continue
            # 同形字／尾随空格：路径分量必须是 ASCII，且归一化后等于原分量
            # （只允许大小写与 NFKC 等价差异，不允许靠不可见字符伪装）。
            for part in rel.parts:
                if any(ord(ch) > 127 for ch in part):
                    raise PackageError(
                        f"{rel.as_posix()} 含非 ASCII 路径分量：{part!r}"
                    )
                if normalize_name(part) != part.casefold().lstrip("."):
                    raise PackageError(
                        f"{rel.as_posix()} 路径分量含空白或不可见字符：{part!r}"
                    )
            # 特殊位（setuid／setgid／sticky）会随归档成员落到解包后的文件上。
            # 源文件带特殊位即拒收；归档构建时还会再次归一到 0644。
            if p.stat().st_mode & 0o7000:
                raise PackageError(
                    f"{rel.as_posix()} 带特殊位（mode={oct(p.stat().st_mode & 0o7777)}），"
                    "未入包"
                )
            # 硬链接：内容可能来自仓库内部资产，且打包后无法从路径判定来源。
            if p.stat().st_nlink > 1:
                raise PackageError(
                    f"{rel.as_posix()} 是硬链接（nlink={p.stat().st_nlink}），"
                    "不能证明内容不是内部资产"
                )
            # 软链与普通文件一律按解析后的真实路径判定：指向包源之外的
            # 内容不随包分发；指向内部资产的软链等同直接放入内部资产。
            real = p.resolve()
            try:
                real_rel = real.relative_to(root_real)
            except ValueError:
                raise PackageError(
                    f"{rel.as_posix()} 解析后落在包源之外：{real}"
                )
            bad_part = [part for part in real_rel.parts
                        if normalize_name(part) in FORBIDDEN_NORMALIZED]
            if bad_part:
                raise PackageError(
                    f"{rel.as_posix()} 指向内部资产：{real_rel.as_posix()}"
                )
            files.append(p)
    return files


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build() -> int:
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
        # 归一化：归档里不得出现 setuid／setgid／sticky 或可执行位。
        os.chmod(target, 0o644)

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
            # 归档成员统一为普通文件 0644：不带 setuid／setgid／sticky／可执行位。
            info.mode = 0o644
            info.type = tarfile.REGTYPE
            with p.open("rb") as fh:
                tar.addfile(info, fh)

    with tarfile.open(archive, "r:gz") as tar:
        members = [m for m in tar.getmembers() if m.isfile()]
        packaged = [Path(m.name).relative_to(pkg_name) for m in members]

    bad_modes = [m.name for m in members if (m.mode & 0o7777) != 0o644]
    if bad_modes:
        archive.unlink(missing_ok=True)
        return fail(
            "归档成员权限未归一到 0644（疑似 setuid／setgid／sticky）："
            + ", ".join(bad_modes[:5]),
            staging,
        )

    # 递归遍历整棵树：内部资产与 tests/ 出现在任意层级都拒绝（大小写不敏感）。
    hits = sorted({
        part
        for rel in packaged
        for part in rel.parts
        if normalize_name(part) in FORBIDDEN_NORMALIZED
        or normalize_name(part) in {"__pycache__", "work"}
    })
    if hits:
        archive.unlink(missing_ok=True)
        return fail("归档含禁用项：" + ", ".join(hits), staging)

    # 版本号单一来源：除 SKILL.md 与 PACKAGE-MANIFEST.txt 外，包内任何文件
    # 出现当前版本字面量都判失败。匹配前做常量折叠、转义还原、花括号剥离与
    # UTF-16 解码，避免邻接拼接／f-string／format／`\x30`／UTF-16 绕过。
    dup_version = sorted(
        rel.as_posix()
        for rel in packaged
        if rel.as_posix() not in VERSION_LITERAL_ALLOWED
        and contains_version(
            (staging / rel).read_bytes(),
            (staging / rel).read_text(encoding="utf-8", errors="replace"),
            version,
        )
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
    print("归档成员权限：0644（无 setuid／setgid／sticky／可执行位）")
    print("未入包项：0（目录软链／断链／特殊文件出现即拒绝，不静默忽略）")
    print(f"校验：{digest_file}  sha256={digest}")
    return 0


def main() -> int:
    try:
        return build()
    except PackageError as exc:
        sys.stderr.write(f"打包失败：{exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
