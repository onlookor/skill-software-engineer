#!/usr/bin/env python3
"""白板模式版本兜底检查器（pattern_version）。

职责（母本 0.7 模式版本定义 ＋ 10.2.5 判据一）：
  1) 从母本 0.21.6 谓词块读取现行声明值 `pattern_version: pv-MAJOR.MINOR`；
  2) 校验白板声明的 pattern_version 与块声明值相等；
  3) 用规范化谓词块指纹兜底：
       - 块已变更而版本未递增 → fail（防「改了块忘了升版」）；
       - 版本已升但基线无对应条目 → fail（防「只写版本号、没有对应块」）。

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
DEFAULT_WHITEBOARD = ROOT / 'pilot/vertical-slice-20261112/whiteboard-pact-dsh.yaml'

BLOCK_HEADING = re.compile(r'^####\s+0\.21\.6\b')
DECL_RE = re.compile(r'pattern_version\s*:\s*(pv-\d+\.\d+)')
VER_RE = re.compile(r'^pv-(\d+)\.(\d+)$')


def read_block(mother_text: str) -> list[str]:
    """取 0.21.6 标题后的第一个围栏代码块（机器层谓词块）。"""
    lines = mother_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if BLOCK_HEADING.match(line):
            start = i
            break
    if start is None:
        raise SystemExit('未找到 0.21.6 标题')
    fence = None
    for i in range(start, len(lines)):
        if lines[i].strip().startswith('```'):
            fence = i
            break
    if fence is None:
        raise SystemExit('0.21.6 后未找到代码块')
    body = []
    for line in lines[fence + 1:]:
        if line.strip().startswith('```'):
            break
        body.append(line)
    if not body:
        raise SystemExit('0.21.6 谓词块为空')
    return body


def normalize(block_lines: list[str]) -> str:
    """规范化：去 `//` 注释、去首尾空白、跳空行、删所有空白，逐行以换行连接。"""
    out = []
    for line in block_lines:
        code = line.split('//', 1)[0]
        code = re.sub(r'\s+', '', code)
        if code:
            out.append(code)
    return '\n'.join(out)


def fingerprint(block_lines: list[str]) -> str:
    return hashlib.sha256(normalize(block_lines).encode('utf-8')).hexdigest()


def load_baseline() -> dict:
    if not BASELINE.exists():
        return {'baselines': {}}
    with open(BASELINE, encoding='utf-8') as f:
        return yaml.safe_load(f) or {'baselines': {}}


def write_baseline(data: dict) -> None:
    meta = data.get('meta', {})
    lines = [
        '# 白板模式版本基线（pattern_version 兜底校验）',
        '#',
        '# 依据：母本 0.7（模式版本＝谓词块的语义版本，MAJOR.MINOR）',
        '#       母本 0.21.6 谓词块首行的现行声明值。',
        '# 性质：数据侧基线，不是母本条款；只存「版本 → 规范化块指纹」，不定义模式语义。',
        '# 更新义务：谓词块语义变更 → 先递增声明值（0.7 义务）→ 再 --freeze 登记新基线；',
        '#   只 --freeze 不升版会被 check_pattern_version.py 判 fail（版本未递增）。',
        '',
        'meta:',
        f"  algorithm: \"{meta.get('algorithm', 'strip // comments, strip whitespace, drop blank lines, sha256')}\"",
        f"  source_block: \"0.21.6 机器层谓词块\"",
        f"  mother_sha256_at_freeze: \"{meta.get('mother_sha256_at_freeze', '')}\"",
        'baselines:',
    ]
    for ver in sorted(data.get('baselines', {})):
        e = data['baselines'][ver]
        lines += [
            f'  {ver}:',
            f"    fingerprint: \"{e['fingerprint']}\"",
            f"    mother_sha256: \"{e['mother_sha256']}\"",
            f"    recorded_at: \"{e['recorded_at']}\"",
            f"    note: \"{e.get('note', '')}\"",
        ]
    BASELINE.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--whiteboard', default=str(DEFAULT_WHITEBOARD))
    ap.add_argument('--freeze', action='store_true', help='把当前块指纹登记为现行版本的基线')
    ap.add_argument('--json', dest='json_out', help='把结果另存为 JSON')
    ap.add_argument('--date', default='2026-11-13', help='--freeze 记录日期')
    args = ap.parse_args()

    if not MOTHER.exists():
        print(f'母本不存在：{MOTHER}', file=sys.stderr)
        return 2
    mother_text = MOTHER.read_text(encoding='utf-8')
    block = read_block(mother_text)
    fp = fingerprint(block)

    decls = DECL_RE.findall('\n'.join(block))
    decl = decls[0] if decls else None
    result = {
        'mother_sha256': hashlib.sha256(mother_text.encode('utf-8')).hexdigest(),
        'block_fingerprint': fp,
        'declared_pattern_version': decl,
        'declaration_count': len(decls),
        'checks': [],
        'verdict': 'fail',
    }

    def rec(level: str, code: str, msg: str):
        result['checks'].append({'level': level, 'code': code, 'msg': msg})

    if decl is None:
        rec('fail', 'PV-1', '0.21.6 谓词块未声明 pattern_version')
    elif not VER_RE.match(decl):
        rec('fail', 'PV-1', f'pattern_version 形态非法：{decl}（应为 pv-MAJOR.MINOR）')
    else:
        rec('pass', 'PV-1', f'0.21.6 声明现行值 {decl}')
    if len(decls) > 1:
        rec('fail', 'PV-1b', f'0.21.6 内出现 {len(decls)} 处 pattern_version 声明，应唯一')

    baseline = load_baseline()
    entries = baseline.get('baselines') or {}

    if args.freeze:
        if decl is None:
            print('无法 freeze：块内无声明值', file=sys.stderr)
            return 2
        if decl in entries and entries[decl]['fingerprint'] != fp:
            print(f'拒绝 freeze：{decl} 已有基线且指纹不同，说明块改了但版本没递增（先按 0.7 升版）',
                  file=sys.stderr)
            return 1
        entries[decl] = {
            'fingerprint': fp,
            'mother_sha256': result['mother_sha256'],
            'recorded_at': args.date,
            'note': '首次登记' if decl not in entries else '复算一致，刷新母本哈希',
        }
        baseline['baselines'] = entries
        baseline['meta'] = {
            'algorithm': 'strip // comments, strip whitespace, drop blank lines, sha256',
            'mother_sha256_at_freeze': result['mother_sha256'],
        }
        write_baseline(baseline)
        rec('pass', 'PV-F', f'已登记基线 {decl}（fingerprint {fp[:12]}…）')
        result['verdict'] = 'pass' if not any(c['level'] == 'fail' for c in result['checks']) else 'fail'
        print(f'PV={result["verdict"]}  freeze {decl}  fingerprint={fp[:12]}…')
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
            rec('pass', 'PV-2', f'白板值 {wbv} 与块声明值相等')
        else:
            rec('fail', 'PV-2', f'白板值 {wbv} ≠ 块声明值 {decl}')
    else:
        rec('fail', 'PV-2', f'白板不存在：{wb_path}')

    if decl is not None:
        e = entries.get(decl)
        if e is None:
            rec('fail', 'PV-3', f'版本 {decl} 无基线：块已变更但未登记（先升版再 --freeze）')
        elif e['fingerprint'] == fp:
            rec('pass', 'PV-3', f'块指纹与 {decl} 基线一致（{fp[:12]}…）')
        else:
            rec('fail', 'PV-3', f'块已变更但版本未递增：{decl} 基线 {e["fingerprint"][:12]}… ≠ 当前 {fp[:12]}…')
        # 母本其他位置编辑导致的哈希漂移只作提示，不判 fail（这正是不用全文指纹作判据值的原因）
        result['mother_sha_drift'] = bool(e and e.get('mother_sha256') and e['mother_sha256'] != result['mother_sha256'])

    result['verdict'] = 'pass' if not any(c['level'] == 'fail' for c in result['checks']) else 'fail'
    for c in result['checks']:
        print(f"[{c['level']}] {c['code']}: {c['msg']}")
    print(f"PV={result['verdict']}  version={decl}  fingerprint={fp[:12]}…  "
          f"mother_sha_drift={result.get('mother_sha_drift')}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0 if result['verdict'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
