#!/usr/bin/env python3
"""registry/checks/common.py —— 性质检查器的公共上下文与判定构造。

判定域（母本 6.2.4／E5）：{pass, fail, escalate}，不引入第四值。
空真（母本 5.4 口径）：记 pass 并置 vacuous=True，附空集依据。
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / 'registry'
PILOT = ROOT / 'pilot/vertical-slice-20261112'
MOTHER = ROOT / '软件工程元框架成文法.md'
CARDS_DIR = PILOT

HARD_RE = re.compile(r'^\s*([A-Z]\d+):.*(?:——|—)\s*硬', re.M)
SEC_RE = re.compile(r'^(#{2,4})\s+(.+)$')
PRED_HEAD_RE = re.compile(r'^\*\*机器层谓词\*\*')

VERDICTS = ('pass', 'fail', 'escalate')


def load_yaml(path):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def mother_text() -> str:
    return MOTHER.read_text(encoding='utf-8')


def hard_properties(text: str) -> list[str]:
    return list(dict.fromkeys(HARD_RE.findall(text)))


def predicate_blocks(text: str) -> list[dict]:
    """发现全部「**机器层谓词**」块：节标题、谓词名。"""
    out = []
    section = ''
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = SEC_RE.match(line)
        if m:
            section = m.group(2).strip()
            continue
        if not PRED_HEAD_RE.match(line.strip()):
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith('```'):
            j += 1
        body = []
        j += 1
        while j < len(lines) and not lines[j].strip().startswith('```'):
            body.append(lines[j])
            j += 1
        names = []
        for b in body:
            names += re.findall(r'([a-z_][a-z0-9_]*)\s*\(', b.split('//', 1)[0])
        out.append({'section': section, 'line': i + 1, 'names': names})
    return out


def registry_entries() -> list[dict]:
    return load_yaml(REG / 'method_registry.yaml').get('entries', [])


def cards() -> dict[str, dict]:
    out = {}
    for p in sorted(CARDS_DIR.glob('*.card.yaml')):
        d = load_yaml(p)
        if isinstance(d, dict) and d.get('card_id'):
            out[d['card_id']] = d
    return out


def snapshot() -> dict:
    p = PILOT / 'hard-properties.snapshot.json'
    if not p.exists():
        return {}
    import json
    return json.loads(p.read_text(encoding='utf-8'))


def build_context() -> dict:
    text = mother_text()
    reg = load_yaml(REG / 'method_registry.yaml')
    prof_doc = load_yaml(REG / 'profiles.yaml')
    # 剖面物化与点路径判定复用 project.py（M2 的权威实现），避免两套口径
    import importlib.util
    spec = importlib.util.spec_from_file_location('registry_project', REG / 'scripts/project.py')
    pmod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pmod)
    common_req = prof_doc.get('common_required') or {}
    mat = {p.get('describes_kind'): pmod.materialize_profile(common_req, p)
           for p in prof_doc.get('profiles') or []}
    return {
        'root': ROOT,
        'mother': text,
        'mother_sha': hashlib.sha256(text.encode('utf-8')).hexdigest(),
        'hard': hard_properties(text),
        'blocks': predicate_blocks(text),
        'entries': reg.get('entries', []),
        'registry_meta': reg.get('meta', {}),
        'profiles': prof_doc,
        'mat': mat,
        'has_path': pmod.has_path,
        'cards': cards(),
        'snapshot': snapshot(),
        'results': {},
        'whiteboard': (PILOT / 'whiteboard-pact-dsh.yaml').read_text(encoding='utf-8'),
        'changlog': (ROOT / '软件工程元框架成文法-changlog.md').read_text(encoding='utf-8'),
        'plan': (PILOT / 'plan-criterion4-20261113.md').read_text(encoding='utf-8'),
    }


def whiteboard_doc(ctx) -> dict:
    """解析白板实例（ctx['whiteboard'] 为原始 YAML 文本）。"""
    doc = yaml.safe_load(ctx['whiteboard']) or {}
    return doc.get('whiteboard') or {}


def domain_data(ctx, key):
    """取 whiteboard.domain_data[key]；键不存在返回 None（区分「未登记」与「显式空集」）。"""
    dd = whiteboard_doc(ctx).get('domain_data') or {}
    return dd[key] if key in dd else None


def verdict(pid: str, v: str, evidence: str, reason: str = '', vacuous: bool = False) -> dict:
    assert v in VERDICTS, v
    return {'property': pid, 'verdict': v, 'evidence': evidence, 'reason': reason,
            'vacuous': vacuous, 'route': 'pass' if v == 'pass' else ('fail' if v == 'fail' else 'escalate')}


def ok(pid: str, evidence: str, reason: str = '', vacuous: bool = False) -> dict:
    return verdict(pid, 'pass', evidence, reason, vacuous)


def bad(pid: str, evidence: str, reason: str = '') -> dict:
    return verdict(pid, 'fail', evidence, reason)


def esc(pid: str, evidence: str, reason: str = '') -> dict:
    return verdict(pid, 'escalate', evidence, reason)
