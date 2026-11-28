#!/usr/bin/env python3
"""Structural-only check of a private directed-construction ledger. No semantic verdict."""
import argparse
import json
from pathlib import Path

KINDS = {"idea", "core", "subargument", "development", "intermediate", "synthesis"}
RELATIONS = {"supports", "derives", "bounds", "tests", "revises", "contextualizes", "synthesizes"}
STATES = {"proposed", "open", "supported", "challenged", "rejected", "re_review_required"}

def filled(x):
    return isinstance(x, str) and bool(x.strip())

def audit(data):
    findings = []
    def flag(code, target):
        findings.append({"code": code, "target": target})
    if not isinstance(data, dict):
        return [{"code": "INVALID_LEDGER", "target": "root"}]
    obj = data.get("object")
    if not isinstance(obj, dict) or obj.get("type") not in ("norm", "judgment", "concept"):
        flag("OBJECT_INVALID", "object")
    if not isinstance(obj, dict) or not all(filled(obj.get(k)) for k in ("locus", "jurisdiction", "timeframe")):
        flag("OBJECT_SCOPE_MISSING", "object")
    if not filled(data.get("question")):
        flag("QUESTION_MISSING", "question")
    if data.get("novelty_direction") not in ("normative", "interpretative", "conceptual", "undecided"):
        flag("NOVELTY_DIRECTION_INVALID", "novelty_direction")
    method = data.get("method")
    if not isinstance(method, dict) or method.get("route") not in ("symbolic", "deconstruction", "combined") or not filled(method.get("warrant")):
        flag("METHOD_INVALID", "method")
    elif method["route"] == "combined" and not filled(method.get("handoff")):
        flag("METHOD_HANDOFF_MISSING", "method")
    nodes = {}
    rows = data.get("nodes", [])
    if not isinstance(rows, list):
        flag("NODES_INVALID", "nodes")
        rows = []
    for row in rows:
        if not isinstance(row, dict) or not filled(row.get("id")):
            flag("NODE_INVALID", "nodes")
            continue
        k = row["id"]
        if k in nodes:
            flag("DUPLICATE_NODE", k)
            continue
        nodes[k] = row
        if row.get("kind") not in KINDS or not filled(row.get("statement")) or row.get("status") not in STATES:
            flag("NODE_INVALID", k)
    ideas = [k for k, n in nodes.items() if n.get("kind") == "idea"]
    cores = [k for k, n in nodes.items() if n.get("kind") == "core"]
    if len(ideas) != 1 or len(cores) != 1:
        flag("CORE_IDEA_ARGUMENT_REQUIRED", "nodes")
    parents, deps = {}, {}
    for k, n in nodes.items():
        parents[k], deps[k] = [], []
        ps = n.get("parents")
        ds = n.get("depends_on")
        if not isinstance(ps, list):
            flag("PARENTS_INVALID", k)
            ps = []
        for p in ps:
            if not isinstance(p, dict) or not filled(p.get("id")) or p.get("id") not in nodes or p.get("relation") not in RELATIONS:
                flag("PARENT_INVALID", k)
            else:
                parents[k].append(p["id"])
        if not isinstance(ds, list):
            flag("DEPENDENCIES_INVALID", k)
            ds = []
        for d in ds:
            if not filled(d) or d not in nodes:
                flag("DEPENDENCY_INVALID", k)
            else:
                deps[k].append(d)
        if n.get("kind") == "idea" and parents[k]:
            flag("IDEA_HAS_PARENT", k)
        if n.get("kind") in ("intermediate", "synthesis") and not deps[k]:
            flag("CONCLUSION_WITHOUT_DEPENDENCIES", k)

    def reachable(graph, start):
        seen, pending = set(), list(graph.get(start, []))
        while pending:
            k = pending.pop()
            if k not in seen:
                seen.add(k)
                pending.extend(graph.get(k, []))
        return seen

    for k, n in nodes.items():
        ancestry = reachable(parents, k)
        if k in ancestry or k in reachable(deps, k):
            flag("CYCLE", k)
        if n.get("kind") != "idea" and not any(i in ancestry for i in ideas):
            flag("UNLINKED_TO_IDEA", k)
        if n.get("kind") not in ("idea", "core") and not any(c in ancestry for c in cores):
            flag("UNLINKED_TO_CORE", k)
        if n.get("status") == "supported" and any(nodes[d].get("status") in ("rejected", "re_review_required", "challenged") for d in reachable(deps, k)):
            flag("STALE_DEPENDENT", k)

    searches = data.get("searches", [])
    if not isinstance(searches, list):
        flag("SEARCHES_INVALID", "searches")
        searches = []
    seen_searches = set()
    for s in searches:
        if not isinstance(s, dict):
            flag("SEARCH_INVALID", "searches")
            continue
        sid = s.get("id")
        if not filled(sid):
            flag("SEARCH_INVALID", "searches")
            continue
        if sid in seen_searches:
            flag("DUPLICATE_SEARCH", sid)
        seen_searches.add(sid)
        if not filled(s.get("target")) or s["target"] not in nodes:
            flag("SEARCH_UNLINKED", sid)
        if not all(filled(s.get(x)) for x in ("question", "expected_evidence", "stop_criterion")):
            flag("SEARCH_UNBOUNDED", sid)
    return findings

def impacted(data, changed):
    """Transitive downstream inferential dependents, not semantic impact prediction."""
    nodes = data.get("nodes", [])
    affected = set(changed)
    while True:
        prior = set(affected)
        for n in nodes:
            if any(d in affected for d in n.get("depends_on", [])):
                affected.add(n["id"])
        if affected == prior:
            return sorted(affected - set(changed))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ledger", type=Path)
    p.add_argument("--changed", nargs="*", default=[])
    a = p.parse_args()
    data = json.loads(a.ledger.read_text(encoding="utf-8"))
    findings = audit(data)
    print(json.dumps({"scope":"structural_only_not_semantic_or_novelty_validation",
                      "findings":findings, "impacted":impacted(data, a.changed) if a.changed and not findings else []}, indent=2))
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())
