#!/usr/bin/env python3
"""卡点日志的机器校验：只判 schema、枚举、长度与脱敏黑名单。

用法：
    python3 check_blocker_log.py <blocker-log.yaml>

退出码：0＝合格或「未记录」；1＝存在不合格记录。
「未记录」按约定不判 fail。机器校验通过不等于可提交——仍需人判断。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("无法校验：缺少 PyYAML\n")
    sys.exit(1)

ALLOWED_KEYS = {"card_file", "card_section", "type", "summary", "skill_version"}
TYPES = {"字段缺", "表述歧义", "通过条件不清", "缺外部信息"}
CARD_FILES = {
    "SKILL.md", "S1-repro.md", "S2-localize-fix.md", "S3-verify.md",
    "repro.md", "failing-test.md", "fix-patch.md", "verify-log.md",
    "validate.py", "V09-checklist.md", "README.md", "PACKAGING.md",
}
SECTION_RE = re.compile(r"^[\w§#.\-·（）()、:：\u4e00-\u9fff ]{1,40}$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
SUMMARY_MAX = 80

BLACKLIST: list[tuple[str, re.Pattern[str]]] = [
    ("代码反引号", re.compile(r"`")),
    ("代码块围栏", re.compile(r"~{3,}")),
    ("花括号／分号／箭头", re.compile(r"[{};]|=>|->|::")),
    ("赋值表达式", re.compile(r"\b[A-Za-z_]\w*\s*=\s*\S")),
    ("代码关键字", re.compile(
        r"\b(def|class|function|import|from|return|SELECT|INSERT|UPDATE|DELETE|CREATE|#include|package)\b"
    )),
    ("路径分隔符", re.compile(r"[/\\~]")),
    ("URL／SSH／邮箱", re.compile(r"://|\bgit@|[\w.+-]+@[\w.-]+")),
    ("IPv4", re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")),
    ("IPv6", re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){2,}[0-9a-fA-F]{1,4}\b")),
    ("内部域名后缀", re.compile(r"\b[\w-]+\.(?:local|internal|corp|lan|home|intra)\b", re.I)),
    ("localhost", re.compile(r"\blocalhost\b", re.I)),
    ("端口", re.compile(r":\d{2,5}\b")),
    ("长十六进制／令牌", re.compile(r"\b[0-9a-fA-F]{16,}\b|\b[A-Za-z0-9_-]{32,}\b")),
]


def check_record(idx: int, rec) -> list[str]:
    where = f"记录 {idx}"
    if not isinstance(rec, dict):
        return [f"{where}：不是 mapping"]
    problems: list[str] = []
    keys = set(map(str, rec))
    if keys != ALLOWED_KEYS:
        missing = sorted(ALLOWED_KEYS - keys)
        extra = sorted(keys - ALLOWED_KEYS)
        if missing:
            problems.append(f"{where}：缺键 {', '.join(missing)}")
        if extra:
            problems.append(f"{where}：多出未允许的键 {', '.join(extra)}")

    card = rec.get("card_file")
    if not isinstance(card, str) or card not in CARD_FILES:
        problems.append(f"{where}：card_file 不在白名单或不是字符串：{card!r}")

    section = rec.get("card_section")
    if not isinstance(section, str) or not SECTION_RE.fullmatch(section.strip()):
        problems.append(f"{where}：card_section 缺失或含不允许字符（限 1–40 字符）")
    else:
        for label, pattern in BLACKLIST:
            if pattern.search(section.strip()):
                problems.append(f"{where}：card_section 命中黑名单「{label}」")

    kind = rec.get("type")
    if kind not in TYPES:
        problems.append(f"{where}：type 不是四类之一：{kind!r}")

    summary = rec.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        problems.append(f"{where}：summary 缺失或为空")
    else:
        text = summary.strip()
        if "\n" in text or "\r" in text:
            problems.append(f"{where}：summary 必须是单行")
        if len(text) > SUMMARY_MAX:
            problems.append(f"{where}：summary 长度 {len(text)} 超过 {SUMMARY_MAX}")
        for label, pattern in BLACKLIST:
            if pattern.search(text):
                problems.append(f"{where}：summary 命中黑名单「{label}」")

    version = rec.get("skill_version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version.strip()):
        problems.append(f"{where}：skill_version 不是 X.Y.Z：{version!r}")

    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        sys.stderr.write("用法：python3 check_blocker_log.py <blocker-log.yaml>\n")
        return 1
    path = Path(argv[0]).expanduser()
    if not path.exists() or not path.read_text(encoding="utf-8", errors="replace").strip():
        print("未记录：没有卡点日志（按约定不判 fail）")
        return 0
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"不合格：不是合法 YAML：{exc}")
        return 1
    if data is None:
        print("未记录：没有卡点日志（按约定不判 fail）")
        return 0
    if not isinstance(data, list):
        print("不合格：日志必须是记录序列（YAML list）")
        return 1

    problems = [msg for i, rec in enumerate(data, start=1) for msg in check_record(i, rec)]
    if problems:
        for msg in problems:
            print(msg)
        return 1
    print(f"合格：{len(data)} 条记录通过机器校验；仍需人判断（黑名单判不了不带点的仓库名／主机名／账号，也判不了描述是否真的抽象）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
