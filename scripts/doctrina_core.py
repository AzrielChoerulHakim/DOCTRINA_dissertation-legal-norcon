"""Norm/Concept dissertation intake, grounded reconstruction ledger and mechanical review.

No semantic inference, law verification or novelty certification is claimed.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from audit_argument_graph import audit_document

VERSION = "0.4.0"
TYPES = {"norm", "concept"}
ATTRIBUTIONS = {"author", "opponent", "quoted_source", "proposed"}
PROVENANCE = {"author_explicit", "researcher_approved", "ai_proposed", "legacy_unverified"}
REVIEWS = ("internal_review", "dialectical_review", "integration_review", "defense_review")
QUESTIONS = {
    "norm": [
        "Which exact legal norm, authoritative text, version and jurisdiction are examined?",
        "Are hierarchy, applicable dates, conditions and exceptions accounted for?",
        "What warrant connects the norm to the author's legal conclusion?",
        "Are positive-law validity, moral legitimacy and policy preference distinct?",
        "What is the strongest contrary reading and resulting legal consequence?",
    ],
    "concept": [
        "Where is the legal concept used in sources actually inspected?",
        "Are concept, legal definition and rival conceptions distinguished?",
        "What boundary case would test the proposed criteria or meaning?",
        "Does an argument move from a definition to a legal remedy without a warrant?",
        "What legally relevant difference follows from the conceptual analysis?",
    ],
}


def issue(code: str, level: str, target: str, explanation: str) -> dict:
    return dict(code=code, level=level, target=target, explanation=explanation)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def split_passages(text: str) -> list[dict]:
    """Paragraph candidate segmentation: exact source substrings and Unicode offsets."""
    passages = []
    for m in re.finditer(r"\S[\s\S]*?(?=\n[ \t]*\n|\Z)", text):
        start, end = m.span()
        while end > start and text[end-1].isspace():
            end -= 1
        if start >= end:
            continue
        passages.append({
            "id": f"T{len(passages)+1:04d}",
            "verbatim": text[start:end],
            "start_offset": start,
            "end_offset": end,
            "start_line": text.count("\n", 0, start)+1,
            "end_line": text.count("\n", 0, end-1)+1,
            "status": "unclassified_passage_not_claim",
        })
    return passages


def new_case(text: str, primary_type: str, title: str, *, locus: str = "",
             jurisdiction: str = "", temporal_scope: str = "",
             source_filename: str = "draft.txt") -> dict:
    if primary_type not in TYPES:
        raise ValueError("Object must be norm or concept; theory is outside DOCTRINA")
    if not nonempty(title):
        raise ValueError("Named legal norm or concept required")
    return {
        "schema_version": VERSION,
        "research_object": {
            "primary_type": primary_type, "title": title.strip(),
            "exact_locus": locus.strip(), "jurisdiction": jurisdiction.strip(),
            "temporal_scope": temporal_scope.strip(),
            "source_state": "unverified",
            "legal_materials": [], "concept_usages": [],
        },
        "draft": {
            "filename": Path(source_filename).name,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "passages": split_passages(text), "confidentiality": "local_only",
        },
        "central_claim_id": None, "claims": [], "chapters": [],
        "objections": [], "sources": [],
        "readiness": {**{x: "pending" for x in REVIEWS}, "researcher_approved": False},
        "originality": {"stage": "locked", "final_status": "NOT_READY"},
    }


def migrate_legacy(legacy: dict, primary_type: str, title: str, *,
                   locus: str = "", jurisdiction: str = "", temporal_scope: str = "") -> dict:
    if legacy.get("schema_version") == VERSION:
        raise ValueError("Already v0.4")
    data = new_case("", primary_type, title, locus=locus,
                    jurisdiction=jurisdiction, temporal_scope=temporal_scope,
                    source_filename="legacy-unanchored.txt")
    for key in ("central_claim_id", "claims", "chapters", "objections", "sources", "readiness"):
        if key in legacy:
            data[key] = json.loads(json.dumps(legacy[key]))
    for claim in data["claims"]:
        if isinstance(claim, dict):
            claim.setdefault("provenance", "legacy_unverified")
    data["migration"] = {"from": legacy.get("schema_version", "v0.3"),
                         "status": "requires_original_draft_anchors"}
    return data


def validate(case: dict) -> list[dict]:
    findings = []
    def add(code, level, loc, msg):
        findings.append(issue(code, level, loc, msg))

    if not isinstance(case, dict):
        return [issue("INVALID_CASE", "critical", "root", "Expected a JSON object")]
    if case.get("schema_version") != VERSION:
        add("INVALID_VERSION", "critical", "schema_version", "Explicit migration to v0.4 required")
    obj = case.get("research_object")
    if not isinstance(obj, dict):
        return findings + [issue("OBJECT_REQUIRED", "critical", "research_object", "Select norm or concept")]
    t = obj.get("primary_type")
    if t not in TYPES:
        add("OBJECT_OUT_OF_SCOPE", "critical", "research_object.primary_type", "Only norm or concept; theories disallowed")
    if not nonempty(obj.get("title")):
        add("OBJECT_UNNAMED", "critical", "research_object.title", "Name the legal norm/concept")
    if not nonempty(obj.get("exact_locus")):
        add("OBJECT_LOCUS_UNVERIFIED", "major", "research_object.exact_locus", "Exact legal source or concept usage needed")

    if t == "norm":
        if not nonempty(obj.get("jurisdiction")):
            add("NORM_NO_JURISDICTION", "major", "research_object.jurisdiction", "Specify jurisdiction")
        if not nonempty(obj.get("temporal_scope")):
            add("NORM_NO_TEMPORAL_SCOPE", "major", "research_object.temporal_scope", "Specify relevant law-in-force date")
        materials = obj.get("legal_materials", [])
        if not isinstance(materials, list):
            add("INVALID_LEGAL_MATERIALS", "critical", "research_object.legal_materials", "List expected")
        elif not materials:
            add("NORM_SOURCE_NOT_INSPECTED", "major", "research_object.legal_materials", "Authoritative source/version not yet inspected")
        else:
            for i, m in enumerate(materials):
                if not isinstance(m, dict) or not nonempty(m.get("locator")):
                    add("NORM_SOURCE_LOCATOR", "major", f"legal_materials[{i}]", "Exact locator required")
                if not isinstance(m, dict) or m.get("inspection_status") != "inspected":
                    add("NORM_SOURCE_UNVERIFIED", "major", f"legal_materials[{i}]", "Source passage not inspected")
    elif t == "concept":
        usages = obj.get("concept_usages", [])
        if not isinstance(usages, list):
            add("INVALID_CONCEPT_USAGES", "critical", "concept_usages", "List expected")
        elif not usages:
            add("CONCEPT_USAGE_NOT_INSPECTED", "major", "concept_usages", "Ground concept in located legal uses")
        else:
            for i, u in enumerate(usages):
                if not isinstance(u, dict) or not nonempty(u.get("locator")) or not nonempty(u.get("usage")):
                    add("CONCEPT_USAGE_LOCATOR", "major", f"concept_usages[{i}]", "Usage and locator required")
    draft = case.get("draft")
    if not isinstance(draft, dict):
        add("DRAFT_MISSING", "critical", "draft", "Draft object required")
        draft = {}
    passage_list = draft.get("passages", [])
    if not isinstance(passage_list, list):
        add("PASSAGES_INVALID", "critical", "draft.passages", "List expected")
        passage_list = []
    passages = {}
    for i, p in enumerate(passage_list):
        if not isinstance(p, dict) or not nonempty(p.get("id")) or not isinstance(p.get("verbatim"), str):
            add("PASSAGE_INVALID", "critical", f"draft.passages[{i}]", "ID and verbatim required")
            continue
        if p["id"] in passages:
            add("DUPLICATE_PASSAGE", "critical", p["id"], "Passage ID duplicated")
        passages[p["id"]] = p
        start, end = p.get("start_offset"), p.get("end_offset")
        if not isinstance(start, int) or not isinstance(end, int) or end-start != len(p["verbatim"]):
            add("PASSAGE_OFFSET_INCONSISTENT", "critical", p["id"], "Offsets do not match verbatim text length")

    claims = case.get("claims", [])
    if not isinstance(claims, list):
        add("CLAIMS_INVALID", "critical", "claims", "List expected")
        claims = []
    if not claims:
        add("RECONSTRUCTION_PENDING", "review", "claims", "Passages are NOT reconstructed arguments")
    known = {}
    for i, c in enumerate(claims):
        if not isinstance(c, dict):
            add("CLAIM_INVALID", "critical", f"claims[{i}]", "Object expected")
            continue
        cid = str(c.get("id") or f"claims[{i}]")
        if cid in known:
            add("DUPLICATE_CLAIM", "critical", cid, "Claim ID duplicated")
        known[cid] = c
        if c.get("attribution") not in ATTRIBUTIONS:
            add("ATTRIBUTION_REQUIRED", "major", cid, "Mark author / opponent / quoted_source / proposed")
        provenance = c.get("provenance")
        if provenance not in PROVENANCE:
            add("PROVENANCE_REQUIRED", "major", cid, "Mark author_explicit / researcher_approved / ai_proposed")
        if provenance == "ai_proposed" and c.get("attribution") == "author":
            add("AI_PROPOSED_AS_AUTHOR", "critical", cid, "Proposed claim cannot be represented as author-endorsed")
        passage = passages.get(c.get("passage_id"))
        if passage is None:
            add("CLAIM_UNANCHORED", "critical", cid, "Claim needs locator in actual draft")
        else:
            anchor = c.get("anchor_text")
            if provenance == "author_explicit" and (not nonempty(anchor) or anchor not in passage["verbatim"]):
                add("AUTHOR_QUOTE_NOT_VERIFIED", "critical", cid, "Author-explicit quotation must match original passage")
            if nonempty(anchor) and anchor not in passage["verbatim"]:
                add("QUOTE_NOT_IN_PASSAGE", "critical", cid, "Claim anchor is not in the specified paragraph")
        if provenance == "legacy_unverified":
            add("LEGACY_NEEDS_REANCHOR", "major", cid, "Legacy claim must be checked against original draft")
    for c in claims:
        if not isinstance(c, dict):
            continue
        for pid in c.get("premises", []) if isinstance(c.get("premises", []), list) else []:
            if pid in known and known[pid].get("attribution") in {"opponent", "quoted_source"}:
                if c.get("attribution") == "author" and not c.get("opponent_premise_adopted"):
                    add("RIVAL_PREMISE_UNADOPTED", "review", str(c.get("id")), "Author conclusion relies on rival; check if adoption is explicit")
    novelty = case.get("originality")
    if not isinstance(novelty, dict) or novelty.get("stage") != "locked":
        add("NOVELTY_EARLY", "critical", "originality.stage", "Novelty evaluation belongs to final stage only")
    elif novelty.get("final_status") not in (None, "NOT_READY"):
        add("NOVELTY_VERDICT_EARLY", "critical", "originality.final_status", "No novelty verdict in internal review")
    return findings


def review(case: dict) -> dict:
    findings = validate(case)
    claims = case.get("claims", [])
    graph = None
    if isinstance(claims, list) and claims and all(isinstance(c, dict) for c in claims):
        graph = audit_document(case, "draft")
        findings.extend(graph.get("findings", []))
    critical = sum(x["level"] == "critical" for x in findings)
    if critical:
        gate = "INTERNAL_REVISION_REQUIRED"
    elif not claims:
        gate = "DRAFT_RECONSTRUCTION_REQUIRED"
    elif findings:
        gate = "STRUCTURAL_REVIEW_WITH_LIMITATIONS"
    else:
        gate = "STRUCTURAL_REVIEW_COMPLETE_NOT_SEMANTICALLY_VALIDATED"
    t = (case.get("research_object") or {}).get("primary_type")
    return {
        "schema_version": VERSION, "gate": gate, "research_object": t,
        "counts": {"critical": critical, "other": len(findings)-critical},
        "findings": findings, "review_questions": QUESTIONS.get(t, []),
        "originality": "LOCKED (normative / interpretative / conceptual only, final stage)",
        "disclaimer": "This is mechanical lint, NOT validation of legal meaning, substantive inference or academic novelty",
    }


def markdown_report(case: dict) -> str:
    result = review(case)
    obj = case.get("research_object", {})
    draft = case.get("draft", {})
    passages = {p.get("id"): p for p in draft.get("passages", []) if isinstance(p, dict)}
    lines = [
        "# DOCTRINA v0.4 — Internal Argument Review", "",
        "**Research object:** " + str(obj.get("primary_type", "unknown")) + " — " + str(obj.get("title", "unknown")),
        "**Legal source / concept locus:** " + str(obj.get("exact_locus") or "UNVERIFIED"),
        "**Gate:** " + result["gate"], "",
        "## Reconstruction — researcher verification required", "",
    ]
    if not case.get("claims"):
        lines += ["No actual semantic claims have been reconstructed. Passages are candidate text units only.", ""]
    for c in case.get("claims", []):
        if not isinstance(c, dict):
            continue
        p = passages.get(c.get("passage_id"), {})
        warrant = c.get("warrant") if isinstance(c.get("warrant"), dict) else {}
        lines += [
            "### " + str(c.get("id", "unknown")),
            "- Recorded claim: " + str(c.get("text") or "MISSING"),
            "- Attribution / provenance: " + str(c.get("attribution", "UNKNOWN")) + " / " + str(c.get("provenance", "UNKNOWN")),
            "- Draft locator: " + str(c.get("passage_id", "MISSING")) + ", lines " + str(p.get("start_line", "?")) + "–" + str(p.get("end_line", "?")),
            "- Verbatim anchor: " + str(c.get("anchor_text") or "NOT PROVIDED / PROPOSED"),
            "- Premises: " + ", ".join(c.get("premises", [])),
            "- Warrant: " + str(warrant.get("text") or "NOT RECORDED"),
            "- Strongest response (researcher-provided): " + str(c.get("researcher_response") or "NOT ASSESSED"),
            "- Minimal repair option (requires approval): " + str(c.get("repair_option") or "NOT ASSESSED"),
            "",
        ]
    lines += ["## Mechanical findings", ""]
    for f in result["findings"]:
        lines.append("- " + str(f["code"]) + " [" + str(f["level"]) + "] at " + str(f["target"]) + ": " + str(f["explanation"]))
    if not result["findings"]:
        lines.append("No structural findings. This does not prove an argument correct.")
    lines += ["", "## Substantive questions requiring human examination", ""]
    lines += ["- " + q for q in result["review_questions"]]
    lines += [
        "", "## Author and reviewer decisions", "",
        "- Confirm intended claims and the status of any proposed hidden premises.",
        "- Inspect original legal materials and verify exact interpretations.",
        "- Evaluate warrant adequacy, rival readings and chapter impacts.",
        "- Accept/reject changes only with researcher approval.",
        "",
        "**Final originality:** LOCKED. No normative, interpretative or conceptual novelty verdict has been made.",
        "",
    ]
    return "\n".join(lines)


def read_case(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Case must be a JSON object")
    return data
