#!/usr/bin/env python3
"""白板模式版本兜底检查器（pattern_version）。

职责（母本 0.7 模式版本定义 ＋ 10.2.5 判据一）：
  1) 按 `registry/DATA-SPEC.md` D1.4「母本机器层谓词块清单（权威）」逐块定位，取每节首个围栏块，
     按节序拼接后取规范化指纹（不写死块数；含无「**机器层谓词**」标记、仅以 `####`＋围栏书写的块）；
  2) 从 0.7 读取现行声明值 `pattern_version: pv-MAJOR.MINOR`（定义与现行值同处）；
  3) 校验白板声明的 pattern_version 与 0.7 声明值相等；
  4) 指纹兜底：
       - 谓词块变化而版本未递增 → fail（防「改了谓词忘了升版」）；
       - 块增加／删除／节归属变化 → fail 并点名；
       - 版本已升但基线无对应条目 → fail。

只读母本。`--freeze` 只写 registry/pattern_version_baseline.yaml。

用法：
  python3 registry/scripts/check_pattern_version.py
  python3 registry/scripts/check_pattern_version.py --whiteboard pilot/vertical-slice-20261112/whiteboard-pact-dsh.yaml
  python3 registry/scripts/check_pattern_version.py --freeze        # 版本合法递增后登记新基线
退出码：0=pass；1=fail；2=环境/参数错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print('需要 PyYAML', file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / 'registry'
MOTHER = ROOT / '软件工程元框架成文法.md'
BASELINE = REG / 'pattern_version_baseline.yaml'
DATA_SPEC = REG / 'DATA-SPEC.md'
DEFAULT_WHITEBOARD = ROOT / 'pilot/vertical-slice-20261112/whiteboard-pact-dsh.yaml'

SEC_RE = re.compile(r'^(#{2,4})\s+(.+)$')
SEC_NUM_RE = re.compile(r'^(\d+(?:\.\d+)+)\s')
BLOCK_ID_RE = re.compile(r'^\d+(?:\.\d+)+$')
DECL_RE = re.compile(r'pattern_version\s*:\s*(pv-\d+\.\d+)')
VER_RE = re.compile(r'^pv-(\d+)\.(\d+)$')
SEC07_RE = re.compile(r'^###\s+0\.7\b')


def load_authoritative_blocks() -> list[dict]:
    """读 DATA-SPEC D1.4 表格，返回权威块清单（块号＋声明名数＋备注）。

    D1.4 是母本机器层谓词块的唯一权威清单（本仓 D1.4 〔新立〕）；本脚本不另立名单、
    不写死数量，清单增删只改 D1.4。
    """
    if not DATA_SPEC.exists():
        return []
    out = []
    for line in DATA_SPEC.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) < 4:
            continue
        if not BLOCK_ID_RE.match(cells[1]):
            continue
        if not cells[2].startswith('@'):
            continue
        out.append({
            'id': cells[1],
            'declared_names': cells[3],
            'note': cells[4] if len(cells) > 4 else '',
        })
    return out


def discover_blocks(lines: list[str], spec: list[dict]) -> tuple[list[dict], list[str]]:
    """按 D1.4 权威清单逐块定位：节标题后首个围栏代码块。返回 (块列表, 未定位到的块号)。"""
    heads = []  # (行下标, 级别, 块号, 标题)
    for i, line in enumerate(lines):
        m = SEC_RE.match(line)
        if not m:
            continue
        title = m.group(2).strip()
        n = SEC_NUM_RE.match(title)
        heads.append((i, len(m.group(1)), n.group(1) if n else '', title))

    blocks, missing = [], []
    for entry in spec:
        pos = next((k for k, h in enumerate(heads) if h[2] == entry['id']), None)
        if pos is None:
            missing.append(entry['id'])
            continue
        start, level, _, title = heads[pos]
        end = len(lines)
        for nxt in heads[pos + 1:]:
            if nxt[1] <= level:
                end = nxt[0]
                break
        j = start + 1
        while j < end and not lines[j].strip().startswith('```'):
            j += 1
        if j >= end:
            missing.append(entry['id'])
            continue
        body = []
        j += 1
        while j < end and not lines[j].strip().startswith('```'):
            body.append(lines[j])
            j += 1
        if body:
            blocks.append({'section': title, 'block_id': entry['id'],
                           'line': start + 1, 'lines': body})
        else:
            missing.append(entry['id'])
    blocks.sort(key=lambda b: b['line'])  # 指纹按母本节序（文档顺序）聚合
    return blocks, missing


def normalize(block_lines: list[str]) -> str:
    """规范化：去 `//` 注释、去全部空白、跳空行；逐行以换行连接。"""
    out = []
    for line in block_lines:
        code = line.split('//', 1)[0]
        code = re.sub(r'\s+', '', code)
        if code:
            out.append(code)
    return '\n'.join(out)


def fingerprint(block_lines: list[str]) -> str:
    return hashlib.sha256(normalize(block_lines).encode('utf-8')).hexdigest()


def aggregate(blocks: list[dict]) -> str:
    text = '\n'.join(normalize(b['lines']) for b in blocks)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def get_declaration(lines: list[str]) -> tuple[str | None, int, int]:
    """只在 0.7 节内取声明值；返回 (值, 出现次数, 行号)。"""
    start = None
    for i, line in enumerate(lines):
        if SEC07_RE.match(line):
            start = i
            break
    if start is None:
        return None, 0, 0
    end = len(lines)
    for j in range(start + 1, len(lines)):
        m = SEC_RE.match(lines[j])
        if m and len(m.group(1)) <= 3:
            end = j
            break
    found = []
    for k in range(start, end):
        found += [(v, k + 1) for v in DECL_RE.findall(lines[k])]
    if not found:
        return None, 0, 0
    return found[0][0], len(found), found[0][1]


def load_baseline() -> dict:
    if not BASELINE.exists():
        return {'baselines': {}}
    with open(BASELINE, encoding='utf-8') as f:
        return yaml.safe_load(f) or {'baselines': {}}


def write_baseline(data: dict, mother_sha: str) -> None:
    lines = [
        '# 白板模式版本基线（pattern_version 兜底校验）',
        '#',
        '# 依据：母本 0.7（模式版本＝白板谓词集（各节机器层谓词块之并）的语义版本，现行值同处声明）；',
        '#       块清单＝registry/DATA-SPEC.md D1.4（唯一权威），每节取首个围栏块，数量不写死。',
        '# 性质：数据侧基线，不是母本条款；只存「版本 → 块清单与指纹」，不定义模式语义。',
        '# 更新义务：谓词集语义变更 → 先递增 0.7 声明值（0.7 义务）→ 再 --freeze 登记新基线；',
        '#   只 --freeze 不升版会被 check_pattern_version.py 判 fail（版本未递增）。',
        '',
        'meta:',
        '  algorithm: "block list from DATA-SPEC.md D1.4; first fenced block per block section; strip // comments & whitespace; drop blank lines; sha256; aggregate in document order"',
        f'  mother_sha256_at_freeze: "{mother_sha}"',
        'baselines:',
    ]
    for ver in sorted(data.get('baselines', {})):
        e = data['baselines'][ver]
        lines += [
            f'  {ver}:',
            f'    fingerprint: "{e["fingerprint"]}"',
            f'    block_count: {e["block_count"]}',
            f'    recorded_at: "{e["recorded_at"]}"',
            f'    note: "{e.get("note", "")}"',
            '    blocks:',
        ]
        for b in e['blocks']:
            lines += [
                f'      - section: "{b["section"]}"',
                f'        line: {b["line"]}',
                f'        fingerprint: "{b["fingerprint"]}"',
                f'        predicate_lines: {b["predicate_lines"]}',
            ]
    BASELINE.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--whiteboard', default=str(DEFAULT_WHITEBOARD))
    ap.add_argument('--freeze', action='store_true', help='把当前块清单与指纹登记为现行版本的基线')
    ap.add_argument('--force', action='store_true', help='口径更正时覆盖已有版本基线（须在 changlog 登记）')
    ap.add_argument('--json', dest='json_out', help='把结果另存为 JSON')
    ap.add_argument('--date', default='2026-11-13', help='--freeze 记录日期')
    ap.add_argument('--note', default='', help='--freeze 写入基线条目的备注（原因／批准依据）')
    args = ap.parse_args()

    if not MOTHER.exists():
        print(f'母本不存在：{MOTHER}', file=sys.stderr)
        return 2
    mother_text = MOTHER.read_text(encoding='utf-8')
    lines = mother_text.splitlines()
    mother_sha = hashlib.sha256(mother_text.encode('utf-8')).hexdigest()

    spec = load_authoritative_blocks()
    if not spec:
        print(f'无法读取 D1.4 权威块清单：{DATA_SPEC}', file=sys.stderr)
        return 2
    blocks, missing = discover_blocks(lines, spec)
    agg = aggregate(blocks)
    decl, decl_count, decl_line = get_declaration(lines)

    result = {
        'mother_sha256': mother_sha,
        'declared_pattern_version': decl,
        'declaration_line': decl_line,
        'declaration_count': decl_count,
        'block_count': len(blocks),
        'authoritative_block_count': len(spec),
        'blocks': [{'block_id': b['block_id'], 'section': b['section'], 'line': b['line'],
                    'predicate_lines': len(normalize(b['lines']).splitlines()),
                    'fingerprint': fingerprint(b['lines'])} for b in blocks],
        'aggregate_fingerprint': agg,
        'checks': [],
        'verdict': 'fail',
    }

    def rec(level: str, code: str, msg: str):
        result['checks'].append({'level': level, 'code': code, 'msg': msg})

    if missing:
        rec('fail', 'PV-0b', f'D1.4 权威清单中 {len(missing)} 块在母本定位失败：{sorted(missing)}')
    if not blocks:
        rec('fail', 'PV-0', '按 D1.4 权威清单未定位到任何机器层谓词块')
    else:
        rec('pass', 'PV-0', f'按 D1.4 权威清单定位 {len(blocks)}/{len(spec)} 块：'
                            + '；'.join(f"{b['block_id']}@{b['line']}" for b in blocks))

    if decl is None:
        rec('fail', 'PV-1', '0.7 内未声明 pattern_version')
    elif not VER_RE.match(decl):
        rec('fail', 'PV-1', f'pattern_version 形态非法：{decl}（应为 pv-MAJOR.MINOR）')
    else:
        rec('pass', 'PV-1', f'0.7 声明现行值 {decl}（第 {decl_line} 行）')
    if decl_count > 1:
        rec('fail', 'PV-1b', f'0.7 内出现 {decl_count} 处 pattern_version 声明，应唯一')

    baseline = load_baseline()
    entries = baseline.get('baselines') or {}

    if args.freeze:
        if decl is None:
            print('无法 freeze：0.7 内无声明值', file=sys.stderr)
            return 2
        old = entries.get(decl)
        if old and old['fingerprint'] != agg and not args.force:
            print(f'拒绝 freeze：{decl} 已有基线且指纹不同（先按 0.7 升版；口径更正用 --force 并登记 changlog）',
                  file=sys.stderr)
            return 1
        note = args.note or (old.get('note') if old else '首次登记')
        entries[decl] = {
            'fingerprint': agg,
            'block_count': len(blocks),
            'recorded_at': args.date,
            'note': note.replace('"', "'"),
            'blocks': result['blocks'],
        }
        baseline['baselines'] = entries
        write_baseline(baseline, mother_sha)
        rec('pass', 'PV-F', f'已登记基线 {decl}（{len(blocks)} 块，aggregate {agg[:12]}…）')
        result['verdict'] = 'fail' if any(c['level'] == 'fail' for c in result['checks']) else 'pass'
        print(f'PV={result["verdict"]}  freeze {decl}  blocks={len(blocks)}  aggregate={agg[:12]}…')
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        return 0 if result['verdict'] == 'pass' else 1

    wb_path = Path(args.whiteboard)
    if wb_path.exists():
        wb = yaml.safe_load(wb_path.read_text(encoding='utf-8')) or {}
        wbv = (wb.get('whiteboard') or {}).get('pattern_version')
        result['whiteboard'] = str(wb_path)
        result['whiteboard_pattern_version'] = wbv
        if wbv is None:
            rec('fail', 'PV-2', '白板 pattern_version 为 null／缺失')
        elif decl is not None and wbv == decl:
            rec('pass', 'PV-2', f'白板值 {wbv} 与 0.7 声明值相等')
        else:
            rec('fail', 'PV-2', f'白板值 {wbv} ≠ 0.7 声明值 {decl}')
    else:
        rec('fail', 'PV-2', f'白板不存在：{wb_path}')

    if decl is not None:
        e = entries.get(decl)
        if e is None:
            rec('fail', 'PV-3', f'版本 {decl} 无基线：先升版再 --freeze')
        elif e['fingerprint'] == agg and e.get('block_count') == len(blocks):
            rec('pass', 'PV-3', f'谓词块与 {decl} 基线一致（{len(blocks)} 块，aggregate {agg[:12]}…）')
        else:
            old_secs = {b['section']: b for b in e.get('blocks', [])}
            new_secs = {b['section']: b for b in result['blocks']}
            added = sorted(set(new_secs) - set(old_secs))
            removed = sorted(set(old_secs) - set(new_secs))
            changed = sorted(s for s in set(old_secs) & set(new_secs)
                             if old_secs[s]['fingerprint'] != new_secs[s]['fingerprint'])
            detail = []
            if e.get('block_count') != len(blocks):
                detail.append(f"块数 {e.get('block_count')}→{len(blocks)}")
            if added:
                detail.append('新增节：' + '、'.join(added))
            if removed:
                detail.append('删除节：' + '、'.join(removed))
            if changed:
                detail.append('变化节：' + '、'.join(changed))
            rec('fail', 'PV-3', f'谓词块已变更但版本未递增：{decl}；' + '；'.join(detail or ['aggregate 不一致']))
        result['mother_sha_drift'] = bool(e and e.get('mother_sha256') and e['mother_sha256'] != mother_sha)

    result['verdict'] = 'fail' if any(c['level'] == 'fail' for c in result['checks']) else 'pass'
    for c in result['checks']:
        print(f"[{c['level']}] {c['code']}: {c['msg']}")
    print(f"PV={result['verdict']}  version={decl}  blocks={len(blocks)}  aggregate={agg[:12]}…")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0 if result['verdict'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
