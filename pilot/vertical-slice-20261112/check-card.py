#!/usr/bin/env python3
"""check-card.py —— 对 pilot 卡片执行编译规范 6.2–6.5 的 F1/F2/F3 检查。

用法：
    python3 check-card.py [card.yaml] [artifact.yaml]

退出码：0 = 无 fail（escalate 不阻断，按 6.5 随产物发布）；1 = 存在 fail。

注意：这是 pilot 工具，不是 registry/scripts 的正式检查器；判定口径以
《编译规范》6.2–6.5 为准，本脚本只实现其中可机械化的部分。
"""
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MOTHER = ROOT / "软件工程元框架成文法.md"
REGISTRY = ROOT / "registry" / "method_registry.yaml"
VOCAB = ROOT / "registry" / "predicate_vocabulary.yaml"

BUILTIN = {"sourced", "approved", "declared", "registered", "compatible", "has", "now"}
FM_RE = re.compile(r"^FM-(?:[0-9]|1[0-5])$")
CH_RE = re.compile(r"^CH-[A-E]$")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def mask_brackets(s: str) -> str:
    # DATA-SPEC D3.10：方括号内文本不参与谓词名抽取。
    return re.sub(r"\[[^\]]*\]", "", s)


def names_in(expr: str):
    return re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", mask_brackets(expr))


def top_level_args(expr: str, name: str):
    m = re.search(rf"\b{re.escape(name)}\s*\(", expr)
    if not m:
        return None
    i = m.end()
    depth = 1
    args, cur = [], []
    while i < len(expr) and depth:
        ch = expr[i]
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
            if depth == 0:
                break
        if ch == "," and depth == 1:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    tail = "".join(cur).strip()
    if tail or args:
        args.append(tail)
    return args


def collect_vocab_names(node, out):
    if isinstance(node, dict):
        if "name" in node and isinstance(node["name"], str):
            out.add(node["name"])
        for v in node.values():
            collect_vocab_names(v, out)
    elif isinstance(node, list):
        for v in node:
            collect_vocab_names(v, out)
    return out


def main():
    card_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "G-CAND-01.card.yaml"
    artifact_path = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "artifact.yaml"
    card = load_yaml(card_path)
    artifact = load_yaml(artifact_path)["compilation_artifact"]
    mother = MOTHER.read_text(encoding="utf-8")
    registry = load_yaml(REGISTRY)
    vocab_names = collect_vocab_names(load_yaml(VOCAB), set())

    entries = {e["entry_id"]: e for e in registry.get("entries", [])}
    all_exprs = []

    result = {"F1": [], "F2": [], "F3": {}, "arity": [], "summary": {}}

    def rec(bucket, level, msg):
        result[bucket].append({"level": level, "msg": msg})

    # ---------- F1 步骤完整且可溯源 ----------
    def anchor_ok(cid):
        base = re.sub(r"-S\d+$", "", cid)
        return re.search(rf"^#{{2,4}}\s*{re.escape(base)}\b", mother, re.M) is not None

    for a in card.get("source_anchors", []):
        if not anchor_ok(str(a)):
            rec("F1", "fail", f"卡片级 source_anchor 在母本中无对应标题：{a}")
    steps = card.get("steps", [])
    expected = [f"S{i}" for i in range(7)]
    got = [s.get("step_id") for s in steps]
    if got != expected:
        rec("F1", "fail", f"步骤序列应为 S0–S6，实际 {got}")
    else:
        rec("F1", "pass", "步骤序列 S0–S6 连续、无跳步/增步/改序")
    for s in steps:
        if not anchor_ok(str(s.get("source_anchor", ""))):
            rec("F1", "fail", f"{s.get('step_id')} source_anchor 不可溯源：{s.get('source_anchor')}")
        for key in ("action", "consumes", "produces", "registry_refs", "source_anchor", "failure_branches"):
            if key not in s:
                rec("F1", "fail", f"{s.get('step_id')} 缺字段 {key}")
        all_exprs.extend(s.get("consumes", []) + s.get("produces", []))
    if not any(x["level"] == "fail" for x in result["F1"]):
        rec("F1", "pass", "每步 source_anchor 均可在母本中定位")

    # ---------- F2 引用闭合 ----------
    # R1 registry_refs
    for s in steps:
        for ref in s.get("registry_refs", []):
            e = entries.get(ref)
            if not e:
                rec("F2", "fail", f"{s['step_id']} registry_ref 不存在：{ref}")
            elif e.get("status") not in ("active", "seed"):
                rec("F2", "fail", f"{s['step_id']} registry_ref 状态不可消费：{ref} status={e.get('status')}")
    rec("F2", "pass", f"R1 registry_refs 全部存在且 status ∈ {{active, seed}}（{len(entries)} 条在册）"
        if not any(x["level"] == "fail" for x in result["F2"]) else "R1 存在失败项")

    # R2 predicate names
    all_exprs += card.get("trigger", {}).get("guard_conditions", [])
    all_exprs.append(card.get("trigger", {}).get("event_pattern", ""))
    for f in card.get("inputs", {}).get("required_facts", []):
        all_exprs.append(f.get("predicate_expr", ""))
    seen = set()
    for expr in all_exprs:
        for name in names_in(expr):
            if name in seen or name in BUILTIN:
                continue
            seen.add(name)
            if name in vocab_names:
                rec("F2", "pass", f"R2 谓词名在册：{name}")
            elif name in mother:
                rec("F2", "escalate", f"R2 谓词名在母本正文出现但未入谓词清单（甲类缺口线索）：{name}")
            else:
                rec("F2", "fail", f"R2 谓词名在母本中不存在（编译期幻觉嫌疑）：{name}")

    # R3 discipline_checks
    for pid in card.get("discipline_checks", []):
        if re.search(rf"^\s*{re.escape(pid)}:", mother, re.M):
            rec("F2", "pass", f"R3 性质 ID 在母本中登记：{pid}")
        else:
            rec("F2", "fail", f"R3 性质 ID 在母本中不存在：{pid}")

    # R4 failure routes
    for s in steps:
        for fb in s.get("failure_branches", []):
            route = str(fb.get("route", ""))
            if FM_RE.match(route) or CH_RE.match(route):
                if route.startswith("FM-") and not re.search(rf"\|\s*\*\*{re.escape(route)}\*\*", mother):
                    rec("F2", "fail", f"R4 {s['step_id']} 路由 {route} 不在 FM 目录")
                else:
                    rec("F2", "pass", f"R4 {s['step_id']} 路由闭合：{route}")
            else:
                rec("F2", "fail", f"R4 {s['step_id']} 路由不闭合：{route}")

    # R5 upstream cards
    card_ids = {c["card_id"] for c in artifact.get("cards", [])}
    for up in card.get("inputs", {}).get("upstream_cards", []):
        if up in card_ids:
            rec("F2", "pass", f"R5 上游卡片存在：{up}")
        else:
            rec("F2", "fail", f"R5 上游卡片不存在：{up}")
    if not card.get("inputs", {}).get("upstream_cards"):
        rec("F2", "pass", "R5 无上游卡片引用（空集，闭合）")

    # ---------- arity（S-12 同型，非 F2 判据） ----------
    for expr in all_exprs:
        for name in names_in(expr):
            if name not in vocab_names:
                continue
            args = top_level_args(mask_brackets(expr), name)
            if args is None:
                continue
            # 取词表 arity
            meta = None
            stack = [load_yaml(VOCAB)]
            while stack:
                n = stack.pop()
                if isinstance(n, dict):
                    if n.get("name") == name and "arity" in n:
                        meta = n
                        break
                    stack.extend(n.values())
                elif isinstance(n, list):
                    stack.extend(n)
            if not meta:
                continue
            arity = meta["arity"]
            variadic = meta.get("variadic", False)
            ok = (len(args) >= arity) if variadic else (len(args) == arity)
            result["arity"].append({"name": name, "arity": arity, "argc": len(args),
                                    "level": "pass" if ok else "fail", "expr": expr})

    # ---------- F3 硬性质覆盖 ----------
    hard = re.findall(r"^\s*([A-Z]\d+):.*(?:——|—)\s*硬", mother, re.M)
    hard = list(dict.fromkeys(hard))
    covered = set(card.get("discipline_checks", []))
    missing = [p for p in hard if p not in covered]
    scoped = ["M10", "M11", "M12", "M14", "M15"]
    missing_scoped = [p for p in scoped if p not in covered]
    result["F3"] = {
        "registry_hard_properties": len(hard),
        "covered": sorted(covered),
        "missing_count": len(missing),
        "missing_sample": missing[:12],
        "full_verdict": "fail" if missing else "pass",
        "scoped_properties": scoped,
        "scoped_verdict": "pass" if not missing_scoped else "fail",
        "note": "F3 的规范判据是全量硬性质覆盖；scoped 判读是本试跑自定的切片口径，不属规范。",
    }

    # ---------- E4 接线（装配入口一致性） ----------
    e4 = {
        "card_artifact_version": card.get("artifact_version"),
        "artifact_label": artifact.get("version", {}).get("label"),
        "registry_version": artifact.get("version", {}).get("registry_version"),
        "match": card.get("artifact_version") == artifact.get("version", {}).get("label"),
    }

    # ---------- summary ----------
    fails = [x for x in result["F1"] if x["level"] == "fail"]
    fails += [x for x in result["F2"] if x["level"] == "fail"]
    fails += [x for x in result["arity"] if x["level"] == "fail"]
    if result["F3"]["full_verdict"] == "fail":
        fails.append({"level": "fail", "msg": "F3 全量硬性质覆盖不足"})
    if not e4["match"]:
        fails.append({"level": "fail", "msg": "E4 卡片 artifact_version 与产物标签不一致"})

    f2_levels = {x["level"] for x in result["F2"]}
    result["F2_verdict"] = ("fail" if "fail" in f2_levels
                            else "escalate" if "escalate" in f2_levels
                            else "pass")
    result["F1_verdict"] = ("pass" if not any(x["level"] == "fail" for x in result["F1"]) else "fail")
    result["E4"] = e4
    result["summary"] = {
        "fail_count": len(fails),
        "escalate_names": sorted({x["msg"].split("：")[-1] for x in result["F2"]
                                  if x["level"] == "escalate"}),
        "exit_code": 1 if fails else 0,
    }

    out = HERE / "fidelity.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"card={card['card_id']} v{card['version']}")
    print(f"F1={result['F1_verdict']}  F2={result['F2_verdict']}  F3(full)={result['F3']['full_verdict']}  F3(scoped)={result['F3']['scoped_verdict']}")
    print(f"E4 match={e4['match']}  fail_count={len(fails)}  exit={result['summary']['exit_code']}")
    if result["summary"]["escalate_names"]:
        print("escalate:", ", ".join(result["summary"]["escalate_names"]))
    for f in fails:
        print("FAIL:", f["msg"])
    print(f"→ {out}")
    return result["summary"]["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
