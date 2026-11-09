#!/usr/bin/env python3
"""B−1 迁移前只读审计（ADR-ANCHOR-01 §7.1bis／§7.7）。

做两件事：
  A. 围栏内 `#code-` 标识抽取率：语义 ID 可自动定位几条、退序位几条、落分隔行几条。
  B. 结构地址 + 落点指纹比对：以 --since 快照为基线，分类「位移／内容改写／其它」。

用法（在 software-engineering/ 下）：
  python3 registry/scripts/anchor_index.py --out /tmp/ai-audit
  python3 registry/scripts/anchor_migration_audit.py --out /tmp/ai-audit --since 3625876

只读：不写仓库文件；快照写到临时目录。
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anchor_index as A  # noqa: E402

MOTHER = '软件工程元框架成文法.md'


def snapshot_doc(commit: str) -> A.Doc:
    text = subprocess.run(['git', 'show', f'{commit}:{MOTHER}'], cwd=A.ROOT,
                          check=True, capture_output=True, text=True).stdout
    tmp = Path(tempfile.mkdtemp(prefix='anchor-snap-')) / MOTHER
    tmp.write_text(text, encoding='utf-8')
    orig = A.ROOT
    A.ROOT = tmp.parent
    try:
        return A.Doc(MOTHER)
    finally:
        A.ROOT = orig


def address(snap: A.Doc, n: int, line_key: dict):
    if not (1 <= n <= len(snap.lines)):
        return None, '', 'out_of_range'
    c = snap.clause_at(n)
    if not c:
        return None, '', 'no_clause'
    clause = c[2]
    if n in {x[0] for x in snap.headings}:
        return clause, 'head', 'heading'
    if n in snap.fence_lines:
        lines = snap.code_lines(clause)
        return (clause, 'code-%d' % (lines.index(n) + 1), 'code') if n in lines \
            else (clause, '', 'fence_delim')
    s = snap.lines[n - 1].strip()
    if s.startswith('|'):
        k = line_key.get((clause, n))
        return (clause, k.lstrip('#'), 'table_row') if k else (clause, '', 'table_row_nokey')
    if re.match(r'^(?:[-*+]|\d+[.)])\s', s):
        p = [k for k, v in snap.list_item_paths(clause).items() if v == n]
        return (clause, 'li-' + p[0], 'list_item') if p else (clause, '', 'list_nopath')
    if s and not s.startswith('#'):
        lines = snap.para_lines(clause)
        return (clause, 'p-%d' % (lines.index(n) + 1), 'paragraph') if n in lines \
            else (clause, '', 'paragraph_other')
    return clause, '', 'blank'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, help='anchor_index.py 的输出目录')
    ap.add_argument('--since', default='3625876', help='基线快照 commit（默认 B−1 前 3625876）')
    args = ap.parse_args()

    out = Path(args.out)
    snap = snapshot_doc(args.since)
    cur = A.Doc(MOTHER)
    tv = {(r['file'], r['line'], r['col'], r['token']): r
          for r in csv.DictReader(open(out / 'targets.csv'))
          if r['scope'] == 'live' and r['target_file'] == MOTHER
          and r['form'] in ('legacy', 'prefix')}
    anchors = [r for r in csv.DictReader(open(out / 'resolvability.csv'))
               if (r['file'], r['line'], r['col'], r['token']) in tv]
    print('LIVE 母本行号锚', len(anchors))

    # ── A：code- 抽取率 ──
    code = [(r, int(r['landing_line'])) for r in anchors
            if int(r['landing_line']) in snap.fence_lines
            and not snap.lines[int(r['landing_line']) - 1].lstrip().startswith('```')]
    per = collections.defaultdict(list)
    for r, n in code:
        m = A.CODE_LINE_ID_RE.match(snap.lines[n - 1].strip())
        per[((r.get('clause') or '?'), m.group(1) if m else '')].append((r, n))
    auto = ordinal = 0
    for (clause, cid), items in per.items():
        unique = cid and len({n for _r, n in items}) == 1
        auto += len(items) if unique else 0
        ordinal += 0 if unique else len(items)
    no_id = sum(1 for _r, n in code if not A.CODE_LINE_ID_RE.match(snap.lines[n - 1].strip()))
    print('围栏正文行锚', len(code), '语义ID自动', auto,
          '退序位', ordinal, '自动率 %.1f%%' % (100.0 * auto / max(1, len(code))),
          '无标识', no_id)
    delim = sum(1 for r in anchors if int(r['landing_line']) in snap.fence_lines
                and snap.lines[int(r['landing_line']) - 1].lstrip().startswith('```'))
    print('围栏内合计', len(code) + delim, '（正文', len(code), '＋分隔行', delim, '）')

    # ── B：结构地址 + 指纹 ──
    rk_snap, _u, _a = A.derive_row_keys({MOTHER: snap})
    line_key = {(x['clause'], x['line']): x['key'] for x in rk_snap}
    rk_cur, _u2, _a2 = A.derive_row_keys({MOTHER: cur})
    rkm = A.build_rowkey_map(rk_cur)
    reg, _ids = A.load_registry()
    terms = A.vocab_terms()
    docs = {MOTHER: cur}
    buckets = collections.Counter()
    details = []
    for r in anchors:
        n = int(r['landing_line'])
        clause, sub, form = address(snap, n, line_key)
        oldfp = A.landing_fingerprint(snap, n, form)
        if not clause or not sub or not oldfp:
            buckets['其它:' + form] += 1
            continue
        res = A.resolve_struct('m', clause, sub, docs, rkm, reg, terms)
        if res['resolvable_to'] == 'none':
            buckets['其它:不可解析'] += 1
            continue
        newfp = A.landing_fingerprint(cur, res['landing_line'], form)
        if newfp == oldfp:
            buckets['一致'] += 1
            continue
        span = cur.clause_span(clause)
        hit = span and any(oldfp in re.sub(r'\s+', ' ', cur.lines[i - 1].strip())
                           for i in range(span[0] + 1, span[1]))
        tag = '位移' if hit else '内容改写'
        buckets[tag] += 1
        details.append((r['file'], r['line'], r['token'], form, tag,
                        f'{clause}#{sub} @{n}->{res["landing_line"]}'))
    print('── F-3 指纹比对分类 ──')
    for k, v in buckets.most_common():
        print('%-16s %d' % (k, v))
    print('指纹不一致合计', buckets['位移'] + buckets['内容改写'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
