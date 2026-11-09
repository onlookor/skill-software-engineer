"""B−1 锚点迁移工具（ADR-ANCHOR-01 §7）。

做三件事：
  1. 以 B−1 前的母本快照（默认 838dc8f）为「改前结构」，把每条行号锚映射为结构地址；
  2. 以当前母本校验新地址可解析、落点指纹可比对；
  3. --apply 时按原 col 就地替换源文件中的锚 token，行数不变。

用法（在 software-engineering/ 下）：
  python3 registry/scripts/anchor_migrate.py --plan
  python3 registry/scripts/anchor_migrate.py --apply

只读默认：--plan 只写 registry/anchor_index/b1_migration_ledger.csv，不改源文件。
"""
from __future__ import annotations

import argparse
import ast
import collections
import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anchor_index as A  # noqa: E402
import anchor_migration_audit as M  # noqa: E402

MOTHER = '软件工程元框架成文法.md'
SKIP_SRC = {'registry/scripts/anchor_index.py', 'registry/scripts/anchor_migrate.py'}
LEDGER = Path('registry/anchor_index/b1_migration_ledger.csv')


def ensure_snapshot(outdir: Path) -> None:
    t = outdir / 'targets.csv'
    if t.is_file():
        with t.open(encoding='utf-8') as f:
            if 'scope' in next(csv.reader(f)):
                return
    outdir.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, 'registry/scripts/anchor_index.py', '--out', str(outdir)],
                   cwd=A.ROOT, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def load_rows(outdir: Path):
    targets = list(csv.DictReader(open(outdir / 'targets.csv', encoding='utf-8')))
    res = {(r['file'], r['line'], r['col'], r['token']): r
           for r in csv.DictReader(open(outdir / 'resolvability.csv', encoding='utf-8'))}
    return targets, res


def yaml_ctx(path: Path):
    """行 → (entry_id, 字段点路径)。"""
    out, ent, stack = {}, None, []
    for i, ln in enumerate(path.read_text(encoding='utf-8').split('\n'), 1):
        m = re.match(r'^(\s*)-\s+entry_id:\s*(\S+)\s*$', ln)
        if m:
            ent, stack = m.group(2), []
            out[i] = (ent, '')
            continue
        if ent is None:
            out[i] = (None, '')
            continue
        m = re.match(r'^(\s*)(?:-\s+)?([A-Za-z_][\w-]*):', ln)
        if m and not re.match(r'^\s*-\s+\{', ln):
            ind, key = len(m.group(1)), m.group(2)
            while stack and stack[-1][0] >= ind:
                stack.pop()
            if key != 'entry_id':
                stack.append((ind, key))
        ind = len(ln) - len(ln.lstrip(' '))
        while stack and stack[-1][0] > ind:
            stack.pop()
        out[i] = (ent, '.'.join(k for _i, k in stack))
    return out


def project_index():
    src = (A.ROOT / 'registry/scripts/project.py').read_text(encoding='utf-8')
    tree = ast.parse(src)
    funcs, syms = [], []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append((node.name, node.lineno, getattr(node, 'end_lineno', node.lineno)))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    syms.append((t.id, node.lineno, getattr(node, 'end_lineno', node.lineno)))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            syms.append((node.target.id, node.lineno, getattr(node, 'end_lineno', node.lineno)))
    return funcs, syms


def prev_nonblank(doc, line):
    j = line - 1
    while j >= 1 and not doc.lines[j - 1].strip():
        j -= 1
    return j if j >= 1 else None


def fence_of(doc, line):
    open_at = None
    for i, ln in enumerate(doc.lines, 1):
        if ln.lstrip().startswith('```'):
            if open_at is None:
                open_at = i
            else:
                if open_at <= line <= i:
                    return open_at, i
                open_at = None
    return None


def sec_addr(rel, line, doc):
    if not (1 <= line <= len(doc.lines)):
        return None, 'out_of_range'
    if not doc.lines[line - 1].strip():
        line = prev_nonblank(doc, line) or line
    best = None
    for hl, title in doc.titles:
        if hl <= line:
            best = title
        else:
            break
    if not best:
        return None, '无标题'
    title, n = A.sec_match(doc, best)
    if not title or n != 1:
        return None, '标题不唯一'
    return f'@d:{rel}#sec-{title}', '最近标题'


def mother_addr(doc_snap, line, line_key, doc_cur, rkm_cur):
    clause, sub, form = M.address(doc_snap, line, line_key)
    if form == 'heading':
        token = f'@m:{clause}'
    elif form in ('paragraph', 'list_item'):
        token = f'@m:{clause}#{sub}'
    elif form == 'table_row':
        token = f'@m:{clause}#{sub}'
    elif form == 'code':
        token = f'@m:{clause}#{sub}'
        m = A.CODE_LINE_ID_RE.match(doc_snap.lines[line - 1].strip())
        if m:
            ids = doc_snap.code_ids(clause).get(m.group(1), [])
            if len(ids) == 1:
                token = f'@m:{clause}#code-{m.group(1)}'
    elif form == 'table_row_nokey':
        token, sub = f'@m:{clause}', ''
        form = 'table_row_nokey'
    elif form == 'fence_delim':
        span = fence_of(doc_snap, line)
        if not span:
            return None, form, '围栏未配对'
        a, b = span
        target = a + 1 if line == a else b - 1
        if not (a < target < b):
            return None, form, '空围栏'
        body = [i for i in range(a + 1, b) if doc_snap.lines[i - 1].strip()]
        if not body:
            return None, form, '空围栏'
        target = body[0] if line == a else body[-1]
        c2, s2, f2 = M.address(doc_snap, target, line_key)
        if not c2:
            return None, form, '围栏正文无条款'
        token = f'@m:{c2}#{s2}' if s2 else f'@m:{c2}'
        m = A.CODE_LINE_ID_RE.match(doc_snap.lines[target - 1].strip())
        if m:
            ids = doc_snap.code_ids(c2).get(m.group(1), [])
            if len(ids) == 1:
                token = f'@m:{c2}#code-{m.group(1)}'
        sub, form = s2, 'fence_delim'
    elif form == 'blank':
        p = prev_nonblank(doc_snap, line)
        if not p:
            return None, form, '文首空行'
        c2, s2, f2 = M.address(doc_snap, p, line_key)
        if f2 == 'fence_delim':
            span = fence_of(doc_snap, p)
            if not span:
                return None, form, '空行前围栏未配对'
            a, b = span
            p2 = b - 1 if p == b else a + 1
            c2, s2, f2 = M.address(doc_snap, p2, line_key)
        if not c2 or f2 in ('blank', 'no_clause', 'out_of_range', 'table_row_nokey'):
            return None, form, f'空行前项不可归位 {f2}'
        token = f'@m:{c2}#{s2}' if s2 else f'@m:{c2}'
        if f2 == 'code':
            m = A.CODE_LINE_ID_RE.match(doc_snap.lines[p2 - 1].strip())
            if m:
                ids = doc_snap.code_ids(c2).get(m.group(1), [])
                if len(ids) == 1:
                    token = f'@m:{c2}#code-{m.group(1)}'
        form = 'blank'
    elif form == 'no_clause':
        token, note = sec_addr(MOTHER, line, doc_cur)
        return token, form, note or '无条款号'
    elif form == 'out_of_range':
        return None, form, '越界陈旧锚'
    else:
        return None, form, f'未处理 {form}'
    return token, form, ''


def validate(token, docs, rkm, reg, terms, funcs, syms):
    if not token:
        return False, ''
    if token.startswith('@m:'):
        body = token[3:]
        clause, _, sub = body.partition('#')
        r = A.resolve_struct('m', clause, sub, docs, rkm, reg, terms)
        return r['resolvable_to'] != 'none', r['landing_line']
    if token.startswith('@r:'):
        body = token[3:]
        ent, _, sub = body.partition('#')
        sub = 'field-' + sub if sub else ''
        r = A.resolve_struct('r', ent, sub, docs, rkm, reg, terms)
        return r['resolvable_to'] != 'none', ''
    if token.startswith('@v:'):
        r = A.resolve_struct('v', token[3:], '', docs, rkm, reg, terms)
        return r['resolvable_to'] != 'none', ''
    if token.startswith('@p:'):
        body = token[3:]
        kind, _, path = body.partition('#')
        if not A.profile_exists(kind):
            return False, ''
        return (A.profile_field_valid(kind, path) if path else True), ''
    if token.startswith('@d:'):
        body = token[3:]
        rel, _, rest = body.partition('#')
        if rest.startswith('fn-'):
            return A.fn_symbol_valid(A.ROOT / rel, rest[3:]), ''
        if rest.startswith('key-'):
            return A.key_symbol_valid(A.ROOT / rel, rest[4:]), ''
        if rest.startswith('sec-'):
            doc = docs.get(rel) or A.Doc(rel)
            title, n = A.sec_match(doc, rest[4:])
            return bool(title) and n == 1, ''
    return False, ''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--snapshot-dir', default='')
    ap.add_argument('--since', default='838dc8f')
    ap.add_argument('--out', default=str(LEDGER))
    ap.add_argument('--plan', action='store_true')
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    if not args.apply:
        args.plan = True

    snapdir = Path(args.snapshot_dir) if args.snapshot_dir else Path(tempfile.mkdtemp(prefix='b1-snap-'))
    ensure_snapshot(snapdir)
    targets, res = load_rows(snapdir)
    doc_snap = M.snapshot_doc(args.since)
    rowkey_snap, _u, _a = A.derive_row_keys({MOTHER: doc_snap})
    line_key = {(r['clause'], r['line']): r['key'] for r in rowkey_snap}

    targets_all = set()
    for r in targets:
        if r['scope'] == 'live' and r['target_file']:
            targets_all.add(r['target_file'])
    docs = {rel: A.Doc(rel) for rel in targets_all}
    docs[MOTHER] = A.Doc(MOTHER)
    rowkey_cur, _u2, _a2 = A.derive_row_keys(docs)
    rkm_cur = A.build_rowkey_map(rowkey_cur)
    reg, _ids = A.load_registry()
    terms = A.vocab_terms()
    funcs, syms = project_index()
    reg_ctx = yaml_ctx(A.ROOT / 'registry/method_registry.yaml')
    prof_ctx = yaml_ctx(A.ROOT / 'registry/profiles.yaml')

    def innermost_func(line):
        cand = [(s, e, n) for n, s, e in funcs if s <= line <= e]
        return min(cand)[2] if cand else None

    def sym_at(line):
        for n, s, e in syms:
            if s <= line <= e:
                return n
        return None

    rows = []
    live = [r for r in targets if r['scope'] == 'live' and r['form'] in ('legacy', 'prefix')]
    for r in live:
        rr = res[(r['file'], r['line'], r['col'], r['token'])]
        kind, tf, line = r['target_kind'], r['target_file'], int(rr['landing_line'] or 0)
        token, form, note = None, '', ''
        cat = 'auto'
        if kind == 'mother':
            token, form, note = mother_addr(doc_snap, line, line_key, docs[MOTHER], rkm_cur)
            cat = 'semi' if form in ('table_row_nokey', 'no_clause') else ('manual' if form in ('blank', 'fence_delim', 'out_of_range') else 'auto')
        elif kind == 'registry':
            ent, path = reg_ctx.get(line, (None, ''))
            e = A.entry_by_id(reg, ent) if ent else None
            if e is None:
                token, note = None, 'registry 行无 entry'
            else:
                p = path
                while p and not A.has_path(e, p):
                    p = p.rsplit('.', 1)[0] if '.' in p else ''
                token = f'@r:{ent}#{p}' if p else f'@r:{ent}'
                note = f'yaml 字段 {p or "(entry)"}'
            cat = 'semi'
        elif kind == 'profiles':
            ent, path = prof_ctx.get(line, (None, ''))
            if ent and ent.startswith('kind_profile_'):
                kd = ent[len('kind_profile_'):]
                p = path
                while p and not A.profile_field_valid(kd, p):
                    p = p.rsplit('.', 1)[0] if '.' in p else ''
                token = f'@p:{kd}#{p}' if p else f'@p:{kd}'
                note = f'profile 字段 {p or "(kind)"}'
            else:
                note = 'profiles 行无 kind'
        elif kind == 'vocab':
            doc = docs['registry/predicate_vocabulary.yaml']
            term = None
            for j in range(line, 0, -1):
                m = re.search(r'name:\s*([A-Za-z_][\w]*)', doc.lines[j - 1])
                if m:
                    term = m.group(1)
                    break
            if term:
                token, note = f'@v:{term}', term
            else:
                note = '无谓词项'
        elif kind == 'compile':
            token, note = sec_addr('编译规范.md', line, docs['编译规范.md'])
        elif kind == 'doc' and tf.endswith('.py'):
            m = re.fullmatch(r'@(\d+)(?:-(\d+))?', r['token'])
            a = int(m.group(1)); b = int(m.group(2) or a) if m else line
            manual9 = {'@223-224', '@225', '@1032-1044', '@1035-1043'}
            if r['token'] in manual9:
                hit = [n for n, s, e in syms if not (e < a or s > b)]
                if not hit:
                    p = prev_nonblank(A.Doc(tf), a)
                    hit = [sym_at(p)] if p and sym_at(p) else []
                if hit:
                    token = f'@d:{tf}#key-{hit[0]}'
                    cat, note = 'manual', f'模块级符号 {hit[0]}（R-5 待确认）'
                else:
                    note = f'模块级符号不可定位 line={a}'
            else:
                fn = innermost_func(a) or innermost_func(line)
                if fn:
                    token, note = f'@d:{tf}#fn-{fn}', fn
                else:
                    note = f'无函数归属 line={a}'
        elif kind == 'doc':
            token, note = sec_addr(tf, line, docs[tf])
        else:
            note = f'未处理 target_kind={kind}'

        ok, landing = validate(token, docs, rkm_cur, reg, terms, funcs, syms)
        if token and not ok:
            cat = 'manual'
            note = (note + '; ' if note else '') + '新地址不可解析'
        if not token:
            cat = 'manual' if form in ('out_of_range', 'blank') or kind == 'profiles' else cat
        if form == 'out_of_range' or (kind == 'doc' and tf.endswith('.py') and not token):
            token = '@!GAP:' + (r['token'].replace('@', 'stale-') if form == 'out_of_range' else 'project-no-unit')
            cat, note = 'manual', note or 'R-2 登记 GAP'
        fp = ''
        if kind == 'mother' and form in ('heading', 'paragraph', 'list_item', 'table_row', 'code') and ok:
            f_old = A.landing_fingerprint(doc_snap, line, form if form != 'heading' else 'heading')
            f_new = A.landing_fingerprint(docs[MOTHER], landing, 'table_row' if form == 'table_row' else form)
            fp = 'match' if f_old == f_new else 'diff'
        rows.append(dict(src=r['file'], line=r['line'], col=r['col'], old_token=r['token'],
                         form=r['form'], target_kind=kind, target_file=tf,
                         old_landing_line=line, old_form=rr['landing_form'],
                         new_token=token or '', category=cat, note=note, fp_match=fp))

    for r in targets:
        if r['scope'] == 'live' and r['form'] == 'struct' and r['target_kind'] == 'registry':
            rows.append(dict(src=r['file'], line=r['line'], col=r['col'], old_token=r['token'],
                             form=r['form'], target_kind=r['target_kind'],
                             target_file=r['target_file'], old_landing_line='', old_form='struct',
                             new_token=r['token'], category='auto',
                             note='存量已清（F-2 清理批）', fp_match='n/a'))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print('ledger', out, 'rows', len(rows))
    print('category', dict(collections.Counter(r['category'] for r in rows)))
    print('by kind', dict(collections.Counter((r['target_kind'], r['category']) for r in rows)))
    bad = [r for r in rows if not r['new_token']]
    print('empty new_token', len(bad))
    for r in bad[:20]:
        print('  ', r['src'], r['line'], r['old_token'], r['category'], r['note'])
    print('fp', dict(collections.Counter(r['fp_match'] for r in rows)))

    if not args.apply:
        return 0

    byfile = collections.defaultdict(list)
    for r in rows:
        if r['new_token'] and r['new_token'] != r['old_token']:
            byfile[r['src']].append(r)
    for rel, rs in byfile.items():
        p = A.ROOT / rel
        lines = p.read_text(encoding='utf-8').split('\n')
        for r in sorted(rs, key=lambda x: (int(x['line']), -int(x['col']))):
            i, c, old, new = int(r['line']) - 1, int(r['col']) - 1, r['old_token'], r['new_token']
            if lines[i][c:c + len(old)] != old:
                print('ABORT mismatch', rel, r['line'], r['col'], old, repr(lines[i][c:c + len(old)]))
                return 2
            lines[i] = lines[i][:c] + new + lines[i][c + len(old):]
        p.write_text('\n'.join(lines), encoding='utf-8')
        print('applied', rel, len(rs))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
