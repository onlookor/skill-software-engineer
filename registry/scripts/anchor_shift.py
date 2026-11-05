#!/usr/bin/env python3
"""插行位移：在指定文件插入行，并把落点跨过插入点的行号型锚机械加数（规范 §2.6）。

只处理「目标为母本（m）」的行号型锚（`@m:N` 与裸 `@N` 两种形态）：
  - 端点 >= 插入点 → 加 N；区间两端分别判断；
  - 目标为其他文件的锚一律不动；
  - 逐出现位置（文件／行／列）改写，禁止按串批量替换；
  - 冻结文件（0.22 as-of）、代码跨度、规范/提案自身不计改。

规范 §10.2（2026-11-05 插行位移裁定）：
  1. 区间锚若 起 < P ≤ 止（插入点在区间内部），不进自动位移结果，标 needs_review，
     由人工判定「扩展／重锚／降 D3」——禁止静默扩成 `@96-103`；
  2. 空行锚（落点为空行）判为不合规：只记录位置，不得输出「内容一致」；
  3. 插入行被已有区间覆盖与第 1 条同一处理；
  4. 位移后与别类同串时允许补 `@m:` 前缀（消歧不改语义），逐处登记 prefixed。

工具同时完成「插入 → 位移 → 落点内容复核」，因为内容复核必须持有插入前的原文。

用法:
  python3 registry/scripts/anchor_shift.py --root <root> --insert-at 100 \
      --insert-line '（演练插入行）' --apply --report /tmp/report.csv \
      --review-report /tmp/review.csv
退出码: 0=无例外且被复核端点内容一致; 1=存在例外或内容不一致; 2=参数/环境错误。
needs_review 不计例外，由 --review-report 与 summary 显式输出。
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(
    r'@(?:(?P<p>[mrpvcd]):)?(?P<a>\d{1,5})'
    r'(?:(?P<sep>[~-])(?P<b>\d{1,5}))?'
    r'(?P<sub>#[^\s，。；|）（]*)?$'
)


def load_detector(root: Path):
    spec = importlib.util.spec_from_file_location(
        'anchor_index_drill', root / 'registry/scripts/anchor_index.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_token(tok: str):
    m = TOKEN_RE.match(tok)
    if not m:
        return None
    return m.groupdict()


def shift_value(v: int, at: int, count: int) -> int:
    return v + count if v >= at else v


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='演练副本根目录（含 registry/scripts）')
    ap.add_argument('--insert-at', type=int, required=True, help='插入点（1-based，新的行占用该行号）')
    ap.add_argument('--insert-line', required=True, help='要插入的整行文本')
    ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--report', default='')
    ap.add_argument('--review-report', default='')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    mod = load_detector(root)
    mother = (root / '软件工程元框架成文法.md')
    if not mother.is_file():
        print('母本不存在', file=sys.stderr)
        return 2

    before_lines = mother.read_text(encoding='utf-8').split('\n')
    if not (1 <= args.insert_at <= len(before_lines) + 1):
        print('插入点越界', file=sys.stderr)
        return 2

    outdir = Path(tempfile.mkdtemp(prefix='anchor-shift-'))
    subprocess.run([sys.executable, str(root / 'registry/scripts/anchor_index.py'),
                    '--out', str(outdir)], capture_output=True)
    targets = list(csv.DictReader((outdir / 'targets.csv').open(encoding='utf-8')))

    frozen = set(mod.FROZEN)
    excl = set(getattr(mod, 'EXCLUDE_DOCS', set()))
    mother_rel = '软件工程元框架成文法.md'

    edits, skipped = [], Counter()
    review = []   # §10.2 需人工裁定的条目：区间内部插入、空行落点
    # 同一行内被另一锚点的字面 token 完整包住的「锚」不是独立引用
    # （典型：`@d:...md#sec-<标题>` 的标题文本里嵌着 `@2830`），不得独立位移。
    by_line: dict[tuple, list] = {}
    for r in targets:
        by_line.setdefault((r['file'], r['line']), []).append(r)
    embedded = set()
    for key, rs in by_line.items():
        for r in rs:
            s, e = int(r['col']), int(r['col']) + len(r['token'])
            for o in rs:
                os_, oe_ = int(o['col']), int(o['col']) + len(o['token'])
                if o is r:
                    continue
                if os_ <= s and e <= oe_ and (oe_ - os_) > (e - s):
                    embedded.add((r['file'], r['line'], r['col'], r['token']))
                    break
    # 已存在的（活跃文件）锚串 → 目标类，用于识别位移后新造的跨目标撞串
    token_kind: dict[str, set] = {}
    for r in targets:
        if r['file'] in frozen or r['file'] in excl or r.get('in_code_span') == 'True':
            continue
        if r['target_kind'] and r['target_kind'] != 'unknown':
            token_kind.setdefault(r['token'], set()).add(r['target_kind'])

    for r in targets:
        if r['target_kind'] != 'mother' or r['form'] not in ('legacy', 'prefix'):
            continue
        if (r['file'], r['line'], r['col'], r['token']) in embedded:
            skipped['嵌在另一锚点的字面标题内'] += 1
            continue
        if r['file'] == mother_rel:
            skipped['源文件即母本'] += 1
            continue
        if r['file'] in frozen:
            skipped['冻结 as-of（§8 不改写）'] += 1
            continue
        if r['file'] in excl:
            skipped['规范/提案自身（语法示例）'] += 1
            continue
        if r.get('in_code_span') == 'True':
            skipped['代码跨度豁免'] += 1
            continue
        parsed = parse_token(r['token'])
        if not parsed:
            skipped['非行号形态'] += 1
            continue
        a, b = int(parsed['a']), int(parsed['b']) if parsed['b'] else None
        # 规范 §10.2 第 1／3 条：插入点落在区间内部（起 < P ≤ 止）时不得自动扩展。
        # 保留原 token 不动，交给人工裁定；禁止把 `@96-102` 静默改成 `@96-103`。
        if b is not None and a < args.insert_at <= b:
            review.append(dict(file=r['file'], line=int(r['line']), col=int(r['col']),
                               token=r['token'], reason='span_inside_insert',
                               start=a, end=b))
            continue
        new_a = shift_value(a, args.insert_at, args.count)
        new_b = shift_value(b, args.insert_at, args.count) if b is not None else None
        if new_a == a and new_b == b:
            continue
        new_tok = '@' + (parsed['p'] + ':' if parsed['p'] else '') + str(new_a)
        if parsed['sep']:
            new_tok += parsed['sep'] + str(new_b)
        if parsed['sub']:
            new_tok += parsed['sub']
        # 撞串保护（规范 §10.2 第 4 条：允许补目标前缀，属消歧不改语义）：
        # 裸锚位移后若与既有（非母本）目标串同形，补显式 `@m:` 前缀，
        # 否则会新造 F-4 跨目标串（例：母本 @333→@334 撞上 profiles 的 @334）。
        # 代价：F-1 由 8,911 变 8,907＝“裸锚转显式锚”，不是计数丢失。
        prefixed = False
        if not parsed['p'] and token_kind.get(new_tok, {'mother'}) - {'mother'}:
            new_tok = '@m:' + new_tok[1:]
            prefixed = True
        edits.append(dict(file=r['file'], line=int(r['line']), col=int(r['col']),
                          token=r['token'], new_token=new_tok,
                          a=a, b=b, new_a=new_a, new_b=new_b, prefixed=prefixed,
                          span_inside=(b is not None and a < args.insert_at <= b)))

    # 逐出现位置改写：同一文件内按 (行, 列) 降序，避免列号漂移
    by_file: dict[str, list] = {}
    for e in edits:
        by_file.setdefault(e['file'], []).append(e)
    exceptions, applied = [], 0
    for rel, items in by_file.items():
        path = root / rel
        lines = path.read_text(encoding='utf-8').split('\n')
        for e in sorted(items, key=lambda x: (x['line'], x['col']), reverse=True):
            s = lines[e['line'] - 1]
            seg = s[e['col'] - 1:e['col'] - 1 + len(e['token'])]
            if seg != e['token']:
                exceptions.append(f'{rel}:{e["line"]}:{e["col"]} 原串不符 {seg!r}!={e["token"]!r}')
                continue
            lines[e['line'] - 1] = (s[:e['col'] - 1] + e['new_token']
                                    + s[e['col'] - 1 + len(e['token']):])
            e['applied'] = True
            applied += 1
        if args.apply:
            path.write_text('\n'.join(lines), encoding='utf-8')

    # 插入行（apply 时才写；内容复核用内存版前后文）
    after_lines = list(before_lines)
    if args.apply:
        after_lines = before_lines[:args.insert_at - 1] + [args.insert_line] + before_lines[args.insert_at - 1:]
        mother.write_text('\n'.join(after_lines), encoding='utf-8')
    else:
        after_lines = before_lines[:args.insert_at - 1] + [args.insert_line] + before_lines[args.insert_at - 1:]

    # 落点内容复核：插入前 a 行文本 vs 插入后新 a' 行文本（区间两端各查）
    # 规范 §10.2 第 2 条：落点为空行时只记录位置，不得输出「内容一致」。
    for e in edits:
        if not e.get('applied'):
            continue
        for endpoint, old, new in (('start', e['a'], e['new_a']),
                                   ('end', e['b'], e['new_b'])):
            if old is None:
                continue
            if not (1 <= old <= len(before_lines)):
                e[f'text_{endpoint}'] = False
                exceptions.append(f'{e["file"]}:{e["line"]} 端点{endpoint} 原行号 {old} 越界')
                continue
            txt_before = before_lines[old - 1]
            if not txt_before.strip():
                # 空行锚：判不合规，不参与一致性断言，只登记位置待清理
                e[f'text_{endpoint}'] = ''
                e['blank_landing'] = True
                if not any(x['file'] == e['file'] and x['line'] == e['line']
                           and x['col'] == e['col'] for x in review):
                    review.append(dict(file=e['file'], line=e['line'], col=e['col'],
                                       token=e['token'], reason='blank_landing',
                                       start=e['a'], end=e['b']))
                continue
            txt_after = after_lines[new - 1] if 1 <= new <= len(after_lines) else ''
            ok = txt_before == txt_after
            e[f'text_{endpoint}'] = ok
            if not ok:
                exceptions.append(f'{e["file"]}:{e["line"]} 端点{endpoint} '
                                  f'{old}->{new} 落点内容不一致')

    report_rows = []
    for e in edits:
        report_rows.append(dict(file=e['file'], line=e['line'], col=e['col'], token=e['token'],
                                new_token=e['new_token'], start=e['a'], new_start=e['new_a'],
                                end=e['b'], new_end=e['new_b'],
                                span_inside_insert=e['span_inside'],
                                applied=e.get('applied', False),
                                prefixed=e.get('prefixed', False),
                                blank_landing=e.get('blank_landing', ''),
                                review_reason='blank_landing' if e.get('blank_landing') else '',
                                text_start_ok=e.get('text_start', ''),
                                text_end_ok=e.get('text_end', '')))
    if args.report:
        with open(args.report, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(report_rows[0].keys()) if report_rows else
                               ['file', 'line', 'col', 'token', 'new_token'])
            w.writeheader()
            w.writerows(report_rows)
    if args.review_report:
        with open(args.review_report, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['file', 'line', 'col', 'token', 'reason', 'start', 'end'])
            w.writeheader()
            w.writerows(review)

    ranges = sum(1 for e in edits if e['b'] is not None and e.get('applied'))
    inside = sum(1 for e in edits if e['span_inside'] and e.get('applied'))
    prefixed = sum(1 for e in edits if e.get('applied') and e.get('prefixed'))
    blank = sum(1 for e in edits if e.get('applied') and e.get('blank_landing'))
    summary = dict(insert_at=args.insert_at, count=args.count, applied=bool(args.apply),
                   anchors_changed=applied, range_anchors=ranges,
                   endpoints_shifted=applied + sum(1 for e in edits
                                                    if e.get('applied') and e['b'] is not None
                                                    and e['new_b'] != e['b']),
                   span_inside_insert=inside, collision_prefixed=prefixed,
                   blank_landing=blank,
                   needs_review=len(review),
                   needs_review_span=sum(1 for x in review if x['reason'] == 'span_inside_insert'),
                   needs_review_blank=sum(1 for x in review if x['reason'] == 'blank_landing'),
                   review=[f'{x["file"]}:{x["line"]}:{x["col"]} {x["token"]} {x["reason"]}'
                           for x in review],
                   skipped=dict(skipped),
                   exceptions=len(exceptions))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for x in review:
        print(f'REVIEW {x["file"]}:{x["line"]}:{x["col"]} {x["token"]} {x["reason"]}', file=sys.stderr)
    for x in exceptions:
        print('EXCEPTION', x, file=sys.stderr)
    return 1 if exceptions else 0


if __name__ == '__main__':
    raise SystemExit(main())
