#!/usr/bin/env python3
"""最便宜的守门：pilot 文档里的 YAML 块必须能被 yaml.safe_load 解析。

背景：demo-01 的「完整记录」曾因 statement 以反引号开头而不是合法 YAML，
任何工具都没读过它（见 demo-01 §8.4）。检查器全绿不等于命题可解析，同理。

用法：
    python3 pilot/check-yaml.py            # 检查默认两份文档
    python3 pilot/check-yaml.py <文件>...   # 检查指定文件

建议每次改 pilot 文档后、提交前跑一次。
"""

from pathlib import Path
import re
import sys

import yaml

BASE = Path(__file__).resolve().parent
DEFAULT = [
    BASE / "demo-01-dot-vs-variadic.md",
    BASE / "delivery-space-survey-template.md",
]


def yaml_blocks(text: str):
    """逐个产出 (起始行号, 块内容)。"""
    for match in re.finditer(r"```yaml\n(.*?)```", text, re.S):
        line = text[: match.start(1)].count("\n") + 1
        yield line, match.group(1)


def main(argv):
    paths = [Path(p) for p in argv] or DEFAULT
    failures = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for line, body in yaml_blocks(text):
            try:
                yaml.safe_load(body)
            except yaml.YAMLError as exc:
                failures += 1
                print(f"FAIL {path.name}:{line}: {exc}")
    if failures:
        print(f"{failures} 个 YAML 块解析失败")
        return 1
    print(f"OK：{len(paths)} 个文件、全部 YAML 块可解析")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
