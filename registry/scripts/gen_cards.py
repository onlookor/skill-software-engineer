#!/usr/bin/env python3
"""gen_cards.py —— 从母本 0.18.2 与 kind 剖面机械生成 8 张实质卡＋10 张躯干卡。

口径（判据四裁定）：
- 实质卡：S0–S6 步骤动作逐字取自母本 0.18.2，步骤骨架/shape 由本脚本生成；不手写。
- 躯干卡：只含 outputs.predicate_writes 与 registry_refs，无 FVR、无 discipline_checks、无 steps。
- 谓词写者：按 DAG 顺序贪心分配，每个谓词恰有一个写者（procedure 谓词除外，按 DP 局部写入）。
- 跨方面认领：性质所在节首段≠卡片方面 → cross_aspect: true ＋ owner_of_record。
- 生成后自检：DAG 无环、被引用卡存在、每个 upstream_predicate 有写者。

用法：python3 registry/scripts/gen_cards.py [--check]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MOTHER = ROOT / '软件工程元框架成文法.md'
PILOT = ROOT / 'pilot' / 'vertical-slice-20261112'
REG = ROOT / 'registry'

# card_id, kind, aspect, 谓词写者来源, 类型
CARDS = [
    ('G-CAND-01', 'STY', 1, '1.5', 'sub'),
    ('G-CAND-02', 'DEC', 2, '2.5', 'sub'),
    ('G-CAND-03', 'CTR', 3, '3.5', 'sub'),
    ('G-CAND-04', 'QAT', 6, '6.5', 'sub'),
    ('G-CAND-05', 'GOV', 7, '7.5', 'sub'),
    ('G-CAND-06', 'VFM', 8, '8.5', 'sub'),
    ('G-CAND-07', 'GRD', 9, '9.5', 'sub'),
    ('G-CAND-08', 'PRJ', 10, '10.5', 'sub'),
    ('G-TRUNK-OWN', 'OWN', 4, '4.5', 'trunk'),
    ('G-TRUNK-CSL', 'CSL', 4, '4.5', 'trunk'),
    ('G-TRUNK-DFL', 'DFL', 4, '4.5', 'trunk'),
    ('G-TRUNK-STP', 'STP', 5, '5.5', 'trunk'),
    ('G-TRUNK-SCH', 'SCH', 5, '5.5', 'trunk'),
    ('G-TRUNK-RLP', 'RLP', 5, '5.5', 'trunk'),
    ('G-TRUNK-DPS', 'DPS', 9, '9.5', 'trunk'),
    ('G-TRUNK-CRD', 'CRD', 0, '0.19.6', 'trunk'),
    ('G-TRUNK-CFG', 'CFG', 0, '0.20.4', 'trunk'),
    ('G-TRUNK-SRC', 'SRC', 0, '0.17.8', 'trunk'),
]

# 同一节内的谓词按 trunk 分摊（否则首个卡片独占整节）
SPLIT = {
    'OWN': ['dataset', 'owner', 'shared_write_exception', 'access_path', 'sensitivity'],
    'CSL': ['consistency_level', 'consistency_rationale', 'invariant'],
    'DFL': ['data_flow', 'data_lineage'],
    'STP': ['interaction_flow', 'orchestrator', 'saga', 'step_class', 'compensation',
            'timeout_budget', 'quality_impact_card'],
    'RLP': ['idempotent', 'delivery_semantics', 'idempotency', 'flag',
            'cleanup_filed', 'expiry_of'],
    'SCH': ['time_semantics'],
    'DPS': ['deploy_strategy', 'canary_gate', 'evolution_path', 'strangler_sequence'],
}

# 认领表（性质 ID → 归属卡）；并集＝39 条硬性质
CLAIMS = {
    'G-CAND-01': ['M10', 'M11', 'M12', 'M14', 'M15'],
    'G-CAND-02': ['M1', 'M2', 'M3', 'M4', 'M8', 'M9'],
    'G-CAND-03': ['M20', 'M22', 'M23', 'M24', 'M25'],
    'G-CAND-04': ['X1', 'X2', 'X5', 'X6'],
    'G-CAND-05': ['W1', 'W2', 'W4', 'W7'],
    'G-CAND-06': ['V1', 'V2', 'V5', 'E1', 'E2', 'E3', 'E5', 'E7'],
    'G-CAND-07': ['T1', 'T4', 'T6'],
    'G-CAND-08': ['G3', 'G7', 'Q1', 'R8'],
}

# 步骤 shape：与 G-CAND-01 已验证的谓词形态一致（避免 arity/词表漂移）
SHAPE = {
    'S0': ([r'[决策点声明：DP_id, aspect={aspect}, kind={kind}, question, affected_predicates]'],
           ['selection_context(DP, F, C)', 'selection_procedure(DP, S0, C0)']),
    'S1': (['selection_context(DP, F, C)'],
           ['step_log(DP, S1, In, Evals, candidate_set, T, Executor)', 'exclusion_record(DP, E, P)']),
    'S2': (['selection_context(DP, F, C)'],
           ['step_log(DP, S2, In, Evals, survivor_set, T, Executor)', 'exclusion_record(DP, E, P)']),
    'S3': (['selection_context(DP, F, C)'],
           ['step_log(DP, S3, In, Evals, feasible_set, T, Executor)']),
    'S4': (['feasible_set', 'has_six_elements(G)'],
           ['step_log(DP, S4, In, Evals, verdicts, T, Executor)', 'verdict_table(DP, c, g, v)']),
    'S5': (['verdict_table(DP, c, g, v)'],
           ['step_log(DP, S5, In, Evals, selected_entry, T, Executor)',
            'selection_procedure(DP, S5, C5)']),
    'S6': (['step_log(DP, S5, In, Evals, selected_entry, T, Executor)'],
           ['selection_procedure(DP, S6, C6)']),
}

PROCEDURE = ['selection_context(DP, F, C)', 'selection_procedure(DP, S0..S6, Cn)',
             'step_log(DP, Sn, In, Evals, Out, T, Executor)', 'exclusion_record(DP, E, P)',
             'verdict_table(DP, c, g, v)']

HEAD_RE = re.compile(r'^#{2,4}\s*(\d+(?:\.\d+)*)')
BLOCK_HEAD = re.compile(r'^\*\*机器层谓词\*\*')
STEP_HEAD = re.compile(r'^\*\*(S[0-6])\s+([^*]+)\*\*')


def mother_lines():
    return MOTHER.read_text(encoding='utf-8').splitlines()


def parse_steps(lines) -> dict:
    """0.18.2 内按 S0–S6 抽取 输入/操作/输出/失败分支。"""
    out, cur = {}, None
    for ln in lines:
        m = STEP_HEAD.match(ln)
        if m:
            cur = m.group(1)
            out[cur] = {'title': m.group(2).strip()}
            continue
        if cur is None:
            continue
        for key, field in (('输入', 'input'), ('操作', 'action'), ('输出', 'output'),
                           ('失败分支', 'failure')):
            if ln.startswith(f'- {key}：'):
                out[cur][field] = ln.split('：', 1)[1].strip()
    return out


def section_blocks(lines) -> dict:
    """节号 → 该节机器层谓词块内的谓词名列表。"""
    out, cur, in_block = {}, 'HEAD', False
    for ln in lines:
        h = HEAD_RE.match(ln)
        if h:
            cur, in_block = h.group(1), False
            continue
        if BLOCK_HEAD.match(ln.strip()):
            in_block = True
            continue
        if in_block:
            if ln.strip().startswith('```'):
                in_block = False
                continue
            m = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(', ln)
            if m:
                out.setdefault(cur, [])
                if m.group(1) not in out[cur]:
                    out[cur].append(m.group(1))
    return out


def property_sections(lines) -> dict:
    out, sec = {}, 'HEAD'
    for ln in lines:
        h = HEAD_RE.match(ln)
        if h:
            sec = h.group(1)
        m = re.match(r'^\s*([A-Z]\d+):.*(?:——|—)\s*硬', ln)
        if m and m.group(1) not in out:
            out[m.group(1)] = sec
    return out


def routes(failure: str) -> list:
    seen = []
    for tok in re.findall(r'\b(?:FM-\d+|CH-[A-E])\b', failure or ''):
        if tok not in seen:
            seen.append(tok)
    return seen


def build_writes(blocks: dict) -> dict:
    writes = {}
    for cid, kind, aspect, sec, typ in CARDS:
        names = SPLIT.get(kind) or blocks.get(sec, [])
        writes[cid] = list(dict.fromkeys(names))
    for cid, kind, aspect, sec, typ in CARDS:
        if typ == 'sub':
            writes[cid] = list(dict.fromkeys(writes[cid] + PROCEDURE))
    return writes


def parents() -> dict:
    order = [c[0] for c in CARDS]
    # 装配 DAG：SRC→…→DPS 单链，实质卡按 1,2,3,6,7,8,9,10 方面序插入
    chain = ['G-TRUNK-SRC', 'G-TRUNK-OWN', 'G-TRUNK-CSL', 'G-TRUNK-DFL', 'G-CAND-02',
             'G-CAND-01', 'G-CAND-03', 'G-TRUNK-STP', 'G-CAND-04', 'G-CAND-05',
             'G-CAND-06', 'G-CAND-07', 'G-CAND-08', 'G-TRUNK-DPS', 'G-TRUNK-RLP',
             'G-TRUNK-SCH', 'G-TRUNK-CFG', 'G-TRUNK-CRD']
    assert sorted(chain) == sorted(order), 'DAG 覆盖全部卡片'
    par = {chain[0]: []}
    for a, b in zip(chain, chain[1:]):
        par[b] = [a]
    return par


def validate(cards: dict, writes: dict, par: dict):
    errs = []
    ids = {c['card_id'] for c in cards.values()}
    # 1 DAG 无环
    state = {}

    def dfs(n):
        state[n] = 1
        for p in par.get(n, []):
            if state.get(p) == 1:
                errs.append(f'DAG 成环：{p}→{n}')
            elif state.get(p, 0) == 0:
                dfs(p)
        state[n] = 2

    for n in ids:
        if state.get(n, 0) == 0:
            dfs(n)
    # 2 被引用卡存在 + 3 上游谓词有写者
    writer = {}
    for cid, ws in writes.items():
        for w in ws:
            writer.setdefault(w.split('(')[0].strip(), cid)
    for cid, c in cards.items():
        ups = c.get('inputs', {}).get('upstream_cards') or []
        for up in ups:
            if up not in ids:
                errs.append(f'{cid} 引用不存在的上游卡：{up}')
        for pred in c.get('inputs', {}).get('upstream_predicates') or []:
            base = pred.split('(')[0].strip()
            if base not in writer:
                errs.append(f'{cid} 上游谓词无写者：{base}')
    return errs


def emit(card: dict, path: Path):
    header = (f"# {card['card_id']} —— 机械生成卡（registry/scripts/gen_cards.py）\n"
              f"# 编译源：软件工程元框架成文法.md（sha256 c0bb9879…）0.18.2 S0–S6 逐字动作；\n"
              f"#   kind={card.get('_kind')}，方面={card.get('_aspect')}；生成时间 2026-11-13。\n"
              f"# 谓词写者与上下游按编译期 DAG 骨架分配；语义对应待后续批次按 0.18.4 精化。\n")
    body = yaml.safe_dump(card, allow_unicode=True, sort_keys=False, width=1000)
    path.write_text(header + body, encoding='utf-8')


def gen_fvr(lines, psect):
    """按认领表生成 8 份 FVR 集：每条接一个真实检查器（导入取得，不手写映射）。"""
    import hashlib
    import sys
    sys.path.insert(0, str(REG / 'checks'))
    import m as cm
    import e as ce
    import w as cw
    import x as cx
    import v as cv
    import t as ct
    import g as cg
    import q as cq
    import r as cr

    order = {}
    for mod in (cm, ce, cw, cx, cv, ct, cg, cq, cr):
        for fn in list(getattr(mod, 'CHECKS', {}).values()) + \
                list(getattr(mod, 'DEFERRED', {}).values()):
            order[fn.__name__.upper()] = fn

    art = yaml.safe_load((PILOT / 'artifact.yaml').read_text(encoding='utf-8'))['compilation_artifact']
    label = art['version']['label']
    stmt = {}
    for ln in lines:
        mm = re.match(r'^\s*([A-Z]\d+):\s*(.*)$', ln)
        if mm and mm.group(1) not in stmt:
            stmt[mm.group(1)] = mm.group(2).strip()[:400]
    out = []
    for cid, pids in CLAIMS.items():
        entries = []
        for pid in pids:
            fn = order.get(pid)
            if fn is None:
                raise SystemExit(f'无检查器：{pid}')
            modname = fn.__module__.split('.')[-1]
            entries.append({
                'property_id': pid,
                'statement': stmt.get(pid, ''),
                'source_section': psect.get(pid, ''),
                'check_program': f'registry/checks/{modname}.py::{fn.__name__}',
                'static_dynamic': 'dynamic' if pid in ('E3', 'E5') else 'static',
                'trigger_wiring': 'registry/checks/runner.py 全量执行，逐条落盘',
                'evidence_form': f'fvr-full-run-1.json 中 property_id={pid} 的 verdict/evidence 行',
                'failure_route': {
                    'pass': '记 pass；空真同时记 vacuous 与空集依据',
                    'fail': '阻塞事件＋缺口登记（0.13）',
                    'escalate': '升级声明（0.19.4）',
                },
                'wired': True,
                'owner_of_record': cid,
            })
        doc = {
            'fvr_set': {
                'id': f'FVR-PACT-DSH-{cid}',
                'version': '1.1.0',
                'card': cid,
                'artifact_version': label,
                'property_count': len(pids),
                'owner_of_record': cid,
                'definition': '10.2.4 FVR_entry；检查器为 registry/checks/ 下的真实可执行函数',
            },
            'fvr_entries': entries,
        }
        path = PILOT / f'fvr-{cid}.yaml'
        path.write_text('# 由 registry/scripts/gen_cards.py --fvr 生成；勿手改条目接线。\n' +
                        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=1000),
                        encoding='utf-8')
        out.append((cid, path, len(pids), hashlib.sha256(path.read_bytes()).hexdigest()))
    return out


def main() -> int:
    lines = mother_lines()
    steps = parse_steps(lines)
    blocks = section_blocks(lines)
    psect = property_sections(lines)
    if '--fvr' in sys.argv:
        for cid, p, n, sha in gen_fvr(lines, psect):
            print(f'{p.name}: {n} 条  sha256={sha}')
        return 0
    art = yaml.safe_load((PILOT / 'artifact.yaml').read_text(encoding='utf-8'))['compilation_artifact']
    label = art['version']['label']
    entries = yaml.safe_load((REG / 'method_registry.yaml').read_text(encoding='utf-8'))['entries']
    by_kind = {}
    for e in entries:
        if e.get('status') in ('active', 'seed'):
            by_kind.setdefault(e.get('kind'), []).append(e['entry_id'])

    writes = build_writes(blocks)
    par = parents()
    cards = {}
    for cid, kind, aspect, sec, typ in CARDS:
        up = par[cid]
        base = {
            'card_id': cid,
            'version': {'major': 0, 'minor': 1, 'patch': 0},
            'artifact_version': label,
            'outputs': {'predicate_writes': writes[cid]},
            'registry_refs': sorted(by_kind.get(kind, []))[:6],
            '_kind': kind,
            '_aspect': aspect,
        }
        if typ == 'sub':
            refs = sorted(by_kind.get(kind, []))[:4]
            step_list = []
            for i in range(7):
                sid = f'S{i}'
                spec = steps[sid]
                cons, prod = SHAPE[sid]
                step_list.append({
                    'step_id': sid,
                    'action': f"{sid} {spec['title']}：{spec.get('action', '')}",
                    'consumes': [x.format(aspect=aspect, kind=kind) for x in cons],
                    'produces': list(prod),
                    'registry_refs': refs,
                    'source_anchor': f'0.18.2-{sid}',
                    'failure_branches': [
                        {'condition': f"母本 0.18.2-{sid} 失败分支（{r}）",
                         'route': r,
                         'artifact': spec.get('failure', '')[:200]}
                        for r in routes(spec.get('failure'))
                    ],
                })
            claims = CLAIMS[cid]
            cross, same = [], []
            for pid in claims:
                psec = psect.get(pid, '')
                if psec and psec.split('.')[0] == str(aspect):
                    same.append(pid)
                else:
                    cross.append(pid)
            base = {
                'card_id': cid,
                'version': {'major': 0, 'minor': 1, 'patch': 0},
                'source_anchors': ['0.18.2', '0.18.3', '0.18.6', '0.17.4', '0.6', '0.20.2'],
                'artifact_version': label,
                'trigger': {
                    'event_pattern': (f"[决策点声明：DP_id, aspect={aspect}, kind={kind}, question, "
                                      f"affected_predicates] ∧ ¬selection_procedure(DP, ·, ·)"),
                    'guard_conditions': ['∀f∈F: sourced(f)', 'constraints_materialized(C)'],
                },
                'inputs': {
                    'required_facts': [
                        {'predicate_expr': '∀f∈F: sourced(f)',
                         'source_obligation': '0.4 出处门槛（source_ref + trust_grade）'},
                        {'predicate_expr': 'constraints_materialized(C)',
                         'source_obligation': '0.4 ＋ 7.2.1 血缘查询'},
                        {'predicate_expr': 'has_six_elements(G)',
                         'source_obligation': '6.2.1 六要素质量场景（S4 输入）'},
                    ],
                    'upstream_predicates': writes[up[0]] if up else [],
                    'upstream_cards': up,
                },
                'steps': step_list,
                'outputs': {
                    'predicate_writes': writes[cid],
                    'evidence_artifacts': [
                        {'artifact_kind': k, 'elements_checklist': [
                            '白板谓词快照（含版本向量）', '检查程序/测试套件版本',
                            '输入数据指纹（哈希）', '执行记录（CI 运行标识、环境描述）',
                            '结论三元组（pass | fail→阻塞事件 ID | escalate→升级声明 ID）',
                            '时间戳', '执行者（人类署名或 Agent 凭据）']}
                        for k in ('ADR', 'step_log', '批准请求/升级声明')
                    ],
                },
                'discipline_checks': same + cross,
                'cross_aspect_claims': [
                    {'property_id': p, 'cross_aspect': True, 'owner_of_record': cid,
                     'section': psect.get(p, ''), 'aspect_of_card': aspect} for p in cross
                ],
                'approval_route': {
                    'impact_rule': '7.2.2', 'high_impact_category': '完整ADR',
                    'unreachable_branch': 'FM-2 → 0.10 三出路',
                },
                '_kind': kind,
                '_aspect': aspect,
            }
        cards[cid] = {k: v for k, v in base.items() if not k.startswith('_')}

    errs = validate({k: v for k, v in cards.items()}, writes, par)
    if errs:
        print('VALIDATION FAIL')
        for e in errs:
            print(' -', e)
        return 1

    for cid, kind, aspect, sec, typ in CARDS:
        c = dict(cards[cid])
        c['_kind'], c['_aspect'] = kind, aspect
        emit(c, PILOT / f'{cid}.card.yaml')

    covered = sorted({p for ids in CLAIMS.values() for p in ids})
    print(f'cards={len(cards)} sub={sum(1 for c in CARDS if c[4] == "sub")} '
          f'trunk={sum(1 for c in CARDS if c[4] == "trunk")} claims={len(covered)}')
    print('predicate writers:', {p: c for c, ws in writes.items() for p in ws}.__len__(), 'distinct')
    print('DAG ok / upstream cards ok / upstream predicates written')
    return 0


if __name__ == '__main__':
    sys.exit(main())
