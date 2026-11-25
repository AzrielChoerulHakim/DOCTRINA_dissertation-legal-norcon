#!/usr/bin/env python3
"""DOCTRINA v0.3 deterministic argument-ledger linter.

IMPORTANT: Lint detects *declared* structural and evidentiary issues. It cannot
judge philosophical truth, substantive validity, interpretive fairness or novelty.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

REVIEW_STAGES = ("internal_review", "dialectical_review", "integration_review", "defense_review")
VALID_KINDS = {"descriptive", "conceptual", "doctrinal", "interpretive", "normative", "empirical", "critical", "ontological"}
VALID_SOURCE_STATES = {"inspected", "partial", "metadata_only", "unverified"}
VALID_OBJECTION_STATUSES = {"open", "responded", "conceded", "reframed", "deferred_with_justification"}


def audit_document(data: dict[str, Any], mode: str = "draft") -> dict[str, Any]:
    """Return mechanical findings; never a scholarly truth or originality verdict."""
    if mode not in {"draft", "pre-originality"}:
        raise ValueError("mode must be draft or pre-originality")
    findings: list[dict[str, Any]] = []

    def add(code: str, level: str, target: str, explanation: str) -> None:
        findings.append(dict(code=code, level=level, target=target, explanation=explanation))

    if not isinstance(data, dict):
        return {"gate": "INTERNAL_REVISION_REQUIRED", "findings": [{"code": "MALFORMED", "level": "critical", "target": "project", "explanation": "JSON root must be an object"}]}

    claims = data.get("claims", [])
    chapters = data.get("chapters", [])
    objections = data.get("objections", [])
    sources = data.get("sources", [])
    if not all(isinstance(x, list) for x in [claims, chapters, objections, sources]):
        return {"gate": "INTERNAL_REVISION_REQUIRED", "findings": [{"code": "MALFORMED", "level": "critical", "target": "project", "explanation": "claims/chapters/objections/sources must be arrays"}]}
    if any(not isinstance(x, dict) for seq in [claims, chapters, objections, sources] for x in seq):
        return {"gate": "INTERNAL_REVISION_REQUIRED", "findings": [{"code": "MALFORMED", "level": "critical", "target": "project", "explanation": "list elements must be objects"}]}

    def unique(records: list[dict[str, Any]], category: str) -> dict[str, dict[str, Any]]:
        d: dict[str, dict[str, Any]] = {}
        for n, record in enumerate(records):
            ident = record.get("id")
            if not isinstance(ident, str) or not ident.strip():
                add("MISSING_ID", "critical", f"{category}[{n}]", "Record lacks a stable string ID")
                continue
            if ident in d:
                add("DUPLICATE_ID", "critical", ident, f"Repeated {category} ID")
            d[ident] = record
        return d

    by_claim = unique(claims, "claim")
    by_chapter = unique(chapters, "chapter")
    by_source = unique(sources, "source")
    unique(objections, "objection")
    thesis_id = data.get("central_claim_id")
    if not thesis_id or thesis_id not in by_claim:
        add("MISSING_THESIS", "critical", "project", "Central thesis claim must exist")

    dependents: dict[str, set[str]] = defaultdict(set)
    for claim_id, claim in by_claim.items():
        kind = claim.get("kind")
        role = claim.get("role", "derived")
        premise_ids = claim.get("premises", [])
        if not isinstance(premise_ids, list):
            add("BAD_PREMISES", "critical", claim_id, "premises must be a list of claim IDs")
            continue
        if kind not in VALID_KINDS:
            add("BAD_CLAIM_KIND", "critical", claim_id, "Unknown claim kind; use declared taxonomy")
        if not str(claim.get("text", "")).strip():
            add("MISSING_CLAIM_TEXT", "critical", claim_id, "Claim content is empty")
        if role == "derived":
            if not premise_ids:
                add("IA-01", "critical", claim_id, "Derived claim lacks premise identifiers")
            warrant = claim.get("warrant")
            if not isinstance(warrant, dict) or not str(warrant.get("text", "")).strip():
                add("IA-01", "critical", claim_id, "Derived claim lacks explicit inferential warrant")
            if not str(claim.get("inference", "")).strip():
                add("MISSING_INFERENCE", "major", claim_id, "Classify inferential move before review")
        else:
            warrant = claim.get("warrant", {})

        for premise in premise_ids:
            if not isinstance(premise, str) or premise not in by_claim:
                add("DANGLING_PREMISE", "critical", claim_id, f"Missing referenced premise: {premise!r}")
            elif premise == claim_id:
                add("DIRECT_SELF_DEPENDENCY", "critical", claim_id, "Claim immediately supports itself")
            else:
                dependents[premise].add(claim_id)

        if kind == "normative" and role == "derived":
            has_normative_premise = any(by_claim.get(pid, {}).get("kind") == "normative" for pid in premise_ids)
            explicit_normative_warrant = isinstance(warrant, dict) and warrant.get("normative_bridge") is True
            if not (has_normative_premise or explicit_normative_warrant):
                add("IA-06", "critical", claim_id, "Normative conclusion lacks declared normative premise or normative_bridge")

        chapter_id = claim.get("chapter_id")
        if chapter_id is not None and chapter_id not in by_chapter:
            add("UNKNOWN_CHAPTER", "major", claim_id, f"Referenced chapter {chapter_id!r} is undefined")

        for q in claim.get("quotes", []):
            if not isinstance(q, dict):
                add("BAD_QUOTE", "critical", claim_id, "Quoted item must be a structured object")
                continue
            sid = q.get("source_id")
            if sid not in by_source:
                add("QUOTE_UNKNOWN_SOURCE", "critical", claim_id, f"Quote source {sid!r} is absent")
            if q.get("inspection_status") != "inspected" or not q.get("locator"):
                add("UNVERIFIED_QUOTE", "critical", claim_id, "Direct quote must have inspected passage and locator")
            if not str(q.get("text", "")).strip():
                add("EMPTY_QUOTE", "major", claim_id, "Quotation record missing verbatim text")
        for s in claim.get("support", []):
            if not isinstance(s, dict):
                add("BAD_SUPPORT", "major", claim_id, "Support item must be object")
                continue
            sid = s.get("source_id")
            if sid not in by_source:
                add("UNKNOWN_SUPPORT", "major", claim_id, f"Unknown source {sid!r}")
            if s.get("state") not in VALID_SOURCE_STATES:
                add("UNKNOWN_SOURCE_STATE", "major", claim_id, "Source coverage state must be declared")
            if s.get("state") == "metadata_only" and s.get("supports_substance") is True:
                add("METADATA_NOT_SUBSTANCE", "critical", claim_id, "Metadata cannot substantiate a substantive interpretation")

    # Nontrivial cycles require interpretive review; not automatically petitio principii.
    color: dict[str, int] = {}
    reported: set[tuple[str, str]] = set()
    def dfs(v: str) -> None:
        color[v] = 1
        for parent in by_claim.get(v, {}).get("premises", []):
            if parent not in by_claim or parent == v:
                continue
            if color.get(parent, 0) == 1:
                k = tuple(sorted((v, parent)))
                if k not in reported:
                    add("IA-02", "review", v, "Dependency cycle detected; check petitio principii versus justified interpretive iteration")
                    reported.add(k)
            elif color.get(parent, 0) == 0:
                dfs(parent)
        color[v] = 2
    for cid in by_claim:
        if color.get(cid, 0) == 0:
            dfs(cid)

    # Declared disagreement is a candidate for review, not a semantic proof of contradiction.
    for cid, claim in by_claim.items():
        for other in claim.get("contradicts", []):
            if other not in by_claim:
                add("UNKNOWN_CONTRADICTION_TARGET", "major", cid, f"Unknown contrary claim {other!r}")
            else:
                add("IA-05", "review", cid, f"Declared tension with {other}; compare scope, stance and temporal conditions")

    for chapid, chap in by_chapter.items():
        attached = chap.get("claim_ids", [])
        if not attached:
            add("IA-14", "review", chapid, "Chapter has no linked claims; document its argumentative function")
        for cid in attached:
            if cid not in by_claim:
                add("CHAPTER_DANGLING_CLAIM", "major", chapid, f"Chapter references missing claim {cid!r}")
        if not chap.get("argumentative_task"):
            add("MISSING_CHAPTER_TASK", "review", chapid, "State chapter's role in central thesis")

    for objection in objections:
        oid = objection.get("id", "unknown-objection")
        if objection.get("target_id") not in by_claim:
            add("OBJECTION_DANGLING", "major", str(oid), "Objection target claim is missing")
        if objection.get("status") not in VALID_OBJECTION_STATUSES:
            add("OBJECTION_BAD_STATUS", "major", str(oid), "Objection status must be explicit")
        if objection.get("status") == "open":
            severity = objection.get("severity", "major")
            if severity in {"foundational", "major"}:
                level = "critical" if mode == "pre-originality" else "review"
                add("OPEN_SERIOUS_OBJECTION", level, str(oid), f"Open {severity} objection prevents completed dialectical review")

    readiness = data.get("readiness", {})
    if not isinstance(readiness, dict):
        readiness = {}
    if mode == "pre-originality":
        for stage in REVIEW_STAGES:
            if readiness.get(stage) != "passed":
                add("REVIEW_NOT_PASSED", "critical", stage, "Required review not recorded as passed; this is a declaration, not independent verification")
        if readiness.get("researcher_approved") is not True:
            add("NO_RESEARCHER_APPROVAL", "critical", "project", "Researcher must authorize final originality review")

    criticals = sum(f["level"] == "critical" for f in findings)
    warnings = sum(f["level"] in {"major", "review"} for f in findings)
    if mode == "pre-originality":
        gate = "ORIGINALITY_REVIEW_INCOMPLETE" if criticals else "READY_FOR_FINAL_ORIGINALITY_REVIEW"
    elif criticals:
        gate = "INTERNAL_REVISION_REQUIRED"
    elif warnings and readiness.get("internal_review") == "passed":
        gate = "INTERNAL_STABLE_WITH_LIMITATIONS"
    else:
        gate = "DRAFT_IN_PROGRESS"
    return {"mode": mode, "gate": gate, "counts": {"critical": criticals, "other": warnings}, "findings": findings,
            "disclaimer": "Only mechanical checks of declarations and links; NOT semantic validity, scholarly originality, or doctoral approval"}


def revision_impact(data: dict[str, Any], changed_id: str) -> dict[str, Any]:
    claims = {x["id"]: x for x in data.get("claims", []) if isinstance(x, dict) and "id" in x}
    if changed_id not in claims:
        return {"changed_id": changed_id, "error": "unknown claim"}
    dependents: dict[str, set[str]] = defaultdict(set)
    for cid, record in claims.items():
        for premise in record.get("premises", []):
            if premise in claims:
                dependents[premise].add(cid)
    affected = set()
    queue = [changed_id]
    while queue:
        curr = queue.pop(0)
        for dep in sorted(dependents.get(curr, [])):
            if dep not in affected and dep != changed_id:
                affected.add(dep)
                queue.append(dep)
    relevant = affected | {changed_id}
    chapters = []
    for ch in data.get("chapters", []):
        if any(c in relevant for c in ch.get("claim_ids", [])):
            chapters.append(ch.get("id"))
    return {"changed_id": changed_id, "downstream_claim_ids": sorted(affected),
            "affected_chapter_ids": sorted(x for x in chapters if x), "action": "RE_REVIEW_REQUIRED; approvals are not inherited"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSON argument ledger")
    parser.add_argument("--mode", choices=["draft", "pre-originality"], default="draft")
    parser.add_argument("--impact", metavar="CLAIM_ID", help="Trace dependent claims and chapters")
    parser.add_argument("--json", action="store_true", help="JSON output instead of text")
    args = parser.parse_args()
    try:
        data = json.loads(args.path.read_text(encoding="utf-8"))
        result = revision_impact(data, args.impact) if args.impact else audit_document(data, args.mode)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        if not args.impact and result["counts"]["critical"] > 0:
            raise SystemExit(2)
        if args.impact and "error" in result:
            raise SystemExit(2)
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
