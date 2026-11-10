#!/usr/bin/env python3
"""搬家逐字校验（moved_verbatim）：同一段文字在两次提交中的形态做行级双向 diff。

存在理由：F-1～F-10 只约束「有锚单元」——无人指向的正文对检测器完全不可见。
故搬家批次收尾必须用本工具做一次不依赖锚点的逐字校验（施工总则第 8 条，B3b 起生效）。

只读：文本经 `git show <rev>:<file>` 取得，不写任何文件、不改工作树。

用法:
  python3 registry/scripts/moved_verbatim.py --src 5309a19:0.5#p-3 --dst HEAD:0.5.1#p-1
  python3 registry/scripts/moved_verbatim.py --src A:0.20.3#li-3 --dst B:0.20.6#li-1-4
  python3 registry/scripts/moved_verbatim.py --src A:0.5#p-3 --dst B:0.5.1#p-1 --file 编译规范.md

选择子（`REV:CLAUSE#SEL`）:
  p-N      该条款内第 N 个正文段落（不含标题/表格/列表/围栏/空行）
  li-N     该条款内第 N 个列表项（按缩进层级，路径形如 2.1）
  li-N-M   列表项 N 到 M（含），用于「一段搬成多条」
  t-N      该条款内第 N 张表（含表头与分隔行；按出现顺序，围栏内不计）
  all      整条条款（标题行之后至下一条同级/更高级标题之前）

判定:
  删除行与插入行作为多重集完全相等 → 「纯位置变化」（退出码 0）
  否则 → 存在字符差异（退出码 1），逐条列出并给出字符相似度
  允许的差异只有两类：位置变化、已声明的指针句或收束句；
  其余任何字符差异即判失败，不得以「语义等价」「逻辑蕴含」「删繁」为由通过。
"""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FILE = '软件工程元框架成文法.md'

HEAD_RE = re.compile(r'^(#{2,6})\s+((?:\d+\.)+\d*)\s')
LI_RE = re.compile(r'^(?:[-*+]|\d+[.)])\s')


def git_show(rev: str, rel: str) -> list[str]:
    p = subprocess.run(['git', 'show', f'{rev}:{rel}'], cwd=ROOT,
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f'无法读取 {rev}:{rel}\n{p.stderr.strip()}')
    return p.stdout.split('\n')


def fenced(lines: list[str]) -> set[int]:
    out, inside = set(), False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith('```'):
            inside = not inside
            out.add(i)
        elif inside:
            out.add(i)
    return out


def clause_span(lines: list[str], clause: str):
    heads = []
    for i, ln in enumerate(lines, 1):
        if i in fenced(lines):
            continue
        m = HEAD_RE.match(ln)
        if m:
            heads.append((i, len(m.group(1)), m.group(2).strip()))
    hits = [(ln, lvl) for (ln, lvl, num) in heads if num == clause]
    if len(hits) != 1:
        raise SystemExit(f'条款号 {clause} 命中 {len(hits)} 次（需唯一）')
    ln, lvl = hits[0]
    end = len(lines) + 1
    for (l2, lvl2, _n) in heads:
        if l2 > ln and lvl2 <= lvl:
            end = l2
            break
    return ln, end


def para_lines(lines: list[str], clause: str) -> list[int]:
    start, end = clause_span(lines, clause)
    fence = fenced(lines)
    out = []
    for i in range(start + 1, end):
        s = lines[i - 1].strip()
        if i in fence or not s or s.startswith('#') or s.startswith('|'):
            continue
        if set(s) <= set('-|: '):
            continue
        if LI_RE.match(s):
            continue
        out.append(i)
    return out


def list_items(lines: list[str], clause: str) -> dict[str, int]:
    start, end = clause_span(lines, clause)
    fence = fenced(lines)
    out, counters = {}, []
    for i in range(start + 1, end):
        raw = lines[i - 1]
        s = raw.strip()
        if i in fence or not LI_RE.match(s):
            continue
        level = min((len(raw) - len(raw.lstrip(' '))) // 2, 5)
        while len(counters) <= level:
            counters.append(0)
        counters[level] += 1
        del counters[level + 1:]
        out['.'.join(str(c) for c in counters)] = i
    return out


def tables(lines: list[str], clause: str) -> list[list[int]]:
    start, end = clause_span(lines, clause)
    fence = fenced(lines)
    blocks, cur = [], []
    for i in range(start + 1, end):
        if i not in fence and lines[i - 1].strip().startswith('|'):
            cur.append(i)
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def select(lines: list[str], clause: str, sel: str) -> list[str]:
    if sel == 'all':
        start, end = clause_span(lines, clause)
        return [lines[i - 1] for i in range(start + 1, end)]
    m = re.fullmatch(r'p-(\d+)', sel)
    if m:
        ps = para_lines(lines, clause)
        n = int(m.group(1))
        if not 1 <= n <= len(ps):
            raise SystemExit(f'{clause} 只有 {len(ps)} 个段落，取不到 p-{n}')
        return [lines[ps[n - 1] - 1]]
    m = re.fullmatch(r'li-(\d+)(?:-(\d+))?', sel)
    if m:
        items = list_items(lines, clause)
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        tops = [k for k in items if k.count('.') == 0]
        if not tops:
            raise SystemExit(f'{clause} 内无顶层列表项')
        pick = []
        for n in range(a, b + 1):
            if n < 1 or n > len(tops):
                raise SystemExit(f'{clause} 只有 {len(tops)} 个顶层列表项，取不到 li-{n}')
            top = tops[n - 1]
            pick += [items[k] for k in items if k == top or k.startswith(top + '.')]
        return [lines[i - 1] for i in sorted(pick)]
    m = re.fullmatch(r't-(\d+)', sel)
    if m:
        blocks = tables(lines, clause)
        n = int(m.group(1))
        if not 1 <= n <= len(blocks):
            raise SystemExit(f'{clause} 只有 {len(blocks)} 张表，取不到 t-{n}')
        return [lines[i - 1] for i in blocks[n - 1]]
    raise SystemExit(f'无法识别的选择子: {sel}')


def parse_spec(spec: str):
    if ':' not in spec:
        raise SystemExit(f'选择子须为 REV:CLAUSE#SEL，收到 {spec}')
    rev, rest = spec.split(':', 1)
    clause, sel = (rest.split('#', 1) + ['all'])[:2] if '#' in rest else (rest, 'all')
    return rev, clause.strip(), sel.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='搬家前 REV:CLAUSE#SEL')
    ap.add_argument('--dst', required=True, help='搬家后 REV:CLAUSE#SEL')
    ap.add_argument('--file', default=DEFAULT_FILE)
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()

    s_rev, s_clause, s_sel = parse_spec(a.src)
    d_rev, d_clause, d_sel = parse_spec(a.dst)
    old = select(git_show(s_rev, a.file), s_clause, s_sel)
    new = select(git_show(d_rev, a.file), d_clause, d_sel)
    old = [x for x in old if x.strip()]
    new = [x for x in new if x.strip()]

    print(f'原文 {a.src}  →  {len(old)} 行')
    print(f'新址 {a.dst}  →  {len(new)} 行')

    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    deleted, inserted = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        if tag in ('delete', 'replace'):
            deleted += old[i1:i2]
        if tag in ('insert', 'replace'):
            inserted += new[j1:j2]
        if tag == 'replace':
            for o, n in zip(old[i1:i2], new[j1:j2]):
                r = difflib.SequenceMatcher(None, o, n).ratio()
                print(f'[改] 字符相似度 {r:.3f}')
                print(f'     旧: {o[:110]}')
                print(f'     新: {n[:110]}')
        elif tag == 'delete':
            for o in old[i1:i2]:
                print(f'[删] {o[:110]}')
        else:
            for n in new[j1:j2]:
                print(f'[增] {n[:110]}')

    same = Counter(deleted) == Counter(inserted)
    if not deleted and not inserted:
        verdict = '通过：零字符差异'
        code = 0
    elif same:
        verdict = (f'通过：纯位置变化（删 {len(deleted)} 行 / 增 {len(inserted)} 行，'
                   f'行集合多重集相等）')
        code = 0
    else:
        verdict = (f'不通过：存在字符差异（删 {len(deleted)} 行 / 增 {len(inserted)} 行）；'
                   f'仅当差异全属「已声明的指针句或收束句」方可人工放行')
        code = 1
    print(verdict)
    return code


if __name__ == '__main__':
    sys.exit(main())
