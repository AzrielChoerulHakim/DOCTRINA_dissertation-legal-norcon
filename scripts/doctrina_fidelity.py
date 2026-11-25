"""DOCTRINA v0.4.2 — source-bound, researcher-controlled reconstruction fidelity.

This layer never infers a legal proposition from prose. Exact anchors, speaking
voice, context and author assent are distinct checks. Approval is self-attested
at a local terminal (NOT an identity-verified electronic signature).
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

from doctrina_core import split_passages

PROTOCOL = "1.0"
VOICES = {"author", "opponent", "quoted_source", "hypothetical", "uncertain"}
MODES = {"explicit", "paraphrase", "inferred", "question", "conditional"}
REVIEW_CHOICES = {"accept", "reject", "revise"}
STATES = {"RESEARCHER_CONFIRMED", "RESEARCHER_REJECTED", "REVISION_REQUESTED",
          "PROPOSED", "STALE_APPROVAL", "SOURCE_INVALID", "UNREVIEWABLE"}
GATE_WARNINGS = {"VOICE_UNVERIFIED", "RECONSTRUCTION_UNAPPROVED",
                 "EXTERNAL_POSITION_UNADOPTED", "CONTEXT_NOT_REVIEWED",
                 "PROPOSITION_NOT_AUTHOR_EXPLICIT", "PASSAGE_CONTEXT_UNCERTAIN"}


def digest(data: Any) -> str:
    """Deterministic digest for a JSON object, not a cryptographic signature."""
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def source_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def issue(code: str, level: str, target: str, detail: str) -> dict:
    return {"code": code, "level": level, "target": target, "explanation": detail}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def begin(case: dict, original_text: str) -> dict:
    """Create P1 staging only if original source and all passage spans match."""
    if not isinstance(original_text, str):
        raise ValueError("Original draft must be UTF-8 decoded text")
    if not isinstance(case.get("draft"), dict):
        raise ValueError("Missing draft")
    if source_hash(original_text) != case["draft"].get("sha256"):
        raise ValueError("Source draft SHA-256 does not match case; refuse reconstruction")
    for p in case["draft"].get("passages", []):
        if not _valid_passage(p, original_text):
            raise ValueError("Stored draft passages are not faithful to source bytes")
    if "reconstruction" in case:
        raise ValueError("Reconstruction already exists; do not reset approvals")
    out = copy.deepcopy(case)
    out["reconstruction"] = {
        "protocol": PROTOCOL,
        "draft_sha256": source_hash(original_text),
        "records": [],
        "decisions": [],
        "status": "researcher_confirmation_required",
    }
    return out


def _valid_passage(p: Any, text: str) -> bool:
    if not isinstance(p, dict):
        return False
    a, b = p.get("start_offset"), p.get("end_offset")
    if isinstance(a, bool) or isinstance(b, bool):
        return False
    if not isinstance(a, int) or not isinstance(b, int) or not (0 <= a < b <= len(text)):
        return False
    return (text[a:b] == p.get("verbatim")
            and p.get("start_line") == text.count("\n", 0, a) + 1
            and p.get("end_line") == text.count("\n", 0, b - 1) + 1)


def propose(case: dict, record: dict) -> dict:
    """Store candidate reconstruction: no inference, approval or voice certification."""
    if not isinstance(case.get("reconstruction"), dict):
        raise ValueError("Run begin() against the original draft first")
    if not isinstance(record, dict) or not nonempty(record.get("id")):
        raise ValueError("Reconstruction record needs a stable ID")
    if record.get("voice") not in VOICES or record.get("mode") not in MODES:
        raise ValueError("Classify voice and mode; choose uncertain if undecidable")
    if not nonempty(record.get("proposition")):
        raise ValueError("Candidate proposition must be explicit, marked as auditor-proposed")
    if not nonempty(record.get("voice_basis")):
        raise ValueError("Describe textual reasons for the speaking-voice hypothesis")
    if not isinstance(record.get("context_passage_ids"), list):
        raise ValueError("Record reviewed context passages, even if empty")
    if not isinstance(record.get("premise_ids", []), list):
        raise ValueError("Premises must be claim ID list")
    c = copy.deepcopy(case)
    records = c["reconstruction"]["records"]
    if any(r.get("id") == record["id"] for r in records):
        raise ValueError("Duplicate record ID; edit via versioned replacement, not duplicate")
    p = next((p for p in c["draft"].get("passages", [])
              if p.get("id") == record.get("passage_id")), None)
    s = record.get("span")
    if p is None or not isinstance(s, dict):
        raise ValueError("Use a real passage ID and explicit local span")
    a, b = s.get("start"), s.get("end")
    if type(a) is not int or type(b) is not int or not (0 <= a < b <= len(p["verbatim"])):
        raise ValueError("Span is outside original paragraph")
    if s.get("quote") != p["verbatim"][a:b]:
        raise ValueError("Quote and offsets do not match verbatim paragraph")
    records.append(copy.deepcopy(record))
    return c


def version_sync(case: dict, edited_text: str) -> dict:
    """Replace draft's physical text while preserving decisions to reveal staleness.

    Changing ANY draft byte invalidates all existing approvals; never inherit
    confirmation even when a sentence happens to remain unchanged elsewhere.
    """
    if not isinstance(case.get("reconstruction"), dict):
        raise ValueError("No reconstruction to sync")
    out = copy.deepcopy(case)
    out["draft"]["sha256"] = source_hash(edited_text)
    out["draft"]["passages"] = split_passages(edited_text)
    out["reconstruction"]["draft_sha256"] = source_hash(edited_text)
    out["reconstruction"]["status"] = "recheck_required_after_revision"
    for key in ("internal_review", "dialectical_review", "integration_review", "defense_review"):
        if isinstance(out.get("readiness"), dict):
            out["readiness"][key] = "re_review_required"
    if isinstance(out.get("readiness"), dict):
        out["readiness"]["researcher_approved"] = False
    return out


def _records_by_id(records: list[dict]) -> dict[str, dict]:
    return {r["id"]: r for r in records if isinstance(r, dict) and nonempty(r.get("id"))}


def _fingerprints(records: dict[str, dict], expected_draft_hash: str
                  ) -> tuple[dict[str, str], set[str], set[str]]:
    """Full dependency closure; altered premises revoke dependent claim approvals."""
    hashes: dict[str, str] = {}
    visiting: set[str] = set()
    cyclic: set[str] = set()
    missing: set[str] = set()

    def visit(rid: str) -> str:
        if rid in hashes:
            return hashes[rid]
        if rid in visiting:
            cyclic.add(rid)
            return "CYCLE"
        r = records.get(rid)
        if r is None:
            missing.add(rid)
            return "MISSING"
        visiting.add(rid)
        parents = r.get("premise_ids", [])
        if not isinstance(parents, list):
            parents = []
        dependencies = [(p, visit(p)) for p in parents if isinstance(p, str)]
        visiting.remove(rid)
        hashes[rid] = digest({"source_sha256": expected_draft_hash,
                              "record": r, "dependent_premises": dependencies})
        return hashes[rid]

    for rid in records:
        visit(rid)
    return hashes, cyclic, missing


def inspect(case: dict, original_text: str | None) -> dict:
    """Fail closed: no original draft = no independently verified fidelity."""
    flags: list[dict] = []
    def add(code, level, target, detail):
        flags.append(issue(code, level, target, detail))

    block = case.get("reconstruction") if isinstance(case, dict) else None
    if not isinstance(block, dict) or block.get("protocol") != PROTOCOL:
        return {
            "gate": "NOT_INITIALIZED", "findings": [issue(
                "RECONSTRUCTION_PROTOCOL_MISSING", "critical", "reconstruction",
                "Initialize from the authorized original draft; legacy claims are not verified")],
            "records": [], "counts": {"confirmed": 0, "unconfirmed": 0, "stale": 0},
            "disclaimer": "No semantic, scholarly, or authorial reliability has been certified",
        }
    draft = case.get("draft", {}) if isinstance(case.get("draft"), dict) else {}
    records_raw = block.get("records", [])
    decisions = block.get("decisions", [])
    if not isinstance(records_raw, list):
        records_raw = []
        add("INVALID_RECORDS", "critical", "reconstruction.records", "Expected array")
    if not isinstance(decisions, list):
        decisions = []
        add("INVALID_DECISIONS", "critical", "reconstruction.decisions", "Expected array")
    if original_text is None:
        add("ORIGINAL_DRAFT_UNAVAILABLE", "critical", "draft",
            "No external original text supplied; JSON excerpts cannot verify themselves")
    elif not isinstance(original_text, str):
        add("INVALID_DRAFT", "critical", "draft", "Original draft must be UTF-8 text")
    else:
        sha = source_hash(original_text)
        if sha != draft.get("sha256") or sha != block.get("draft_sha256"):
            add("DRAFT_HASH_MISMATCH", "critical", "draft.sha256",
                "Original file differs from case/reconstruction; approvals cannot be trusted")
        for p in draft.get("passages", []):
            if not _valid_passage(p, original_text):
                add("PASSAGE_NOT_IN_ORIGINAL", "critical",
                    p.get("id", "unknown") if isinstance(p, dict) else "unknown",
                    "Passage offsets, lines, or content do not match independently supplied original")
    passage_map = {p["id"]: p for p in draft.get("passages", [])
                   if isinstance(p, dict) and nonempty(p.get("id"))}
    records = _records_by_id(records_raw)
    if len(records) != len(records_raw):
        add("DUPLICATE_OR_MISSING_RECORD_ID", "critical", "reconstruction.records",
            "Every reconstruction entry needs a unique stable ID")
    confirmed: set[str] = set()
    bad: set[str] = set()
    states: list[dict] = []
    fingerprints, cycles, missing = _fingerprints(records, str(block.get("draft_sha256")))
    for rid in sorted(cycles):
        add("DEPENDENCY_CYCLE_UNRESOLVED", "major", rid,
            "Unable to validate dependent approval closure; not automatically a logical fallacy")
        bad.add(rid)
    for rid in sorted(missing):
        add("PREMISE_RECORD_MISSING", "critical", rid, "Referenced proposition does not exist")
    real_text = isinstance(original_text, str) and source_hash(original_text) == draft.get("sha256") == block.get("draft_sha256")
    for rid, r in records.items():
        problem = False
        p = passage_map.get(r.get("passage_id"))
        span = r.get("span")
        if p is None or not isinstance(span, dict):
            add("CLAIM_SPAN_MISSING", "critical", rid, "Requires passage ID and exact quote span")
            problem = True
        else:
            a, b = span.get("start"), span.get("end")
            if type(a) is not int or type(b) is not int or not (0 <= a < b <= len(p["verbatim"])):
                add("CLAIM_SPAN_INVALID", "critical", rid, "Span must be inside verbatim source paragraph")
                problem = True
            elif p["verbatim"][a:b] != span.get("quote"):
                add("CLAIM_QUOTE_MISMATCH", "critical", rid, "Excerpt not identical to provided draft passage")
                problem = True
        if r.get("voice") not in VOICES or not nonempty(r.get("voice_basis")):
            add("VOICE_UNVERIFIED", "major", rid, "Speaking voice must be reasoned, not inferred from presence of a quote")
            problem = True
        if r.get("mode") not in MODES:
            add("MODE_UNCLASSIFIED", "major", rid, "Explicit/paraphrase/inferred/question/conditional required")
            problem = True
        if not nonempty(r.get("proposition")):
            add("PROPOSITION_MISSING", "critical", rid, "Meaning statement cannot be blank")
            problem = True
        context = r.get("context_passage_ids")
        if not isinstance(context, list):
            add("CONTEXT_NOT_REVIEWED", "major", rid, "Record which adjacent passages were read")
            problem = True
        elif any(x not in passage_map for x in context):
            add("CONTEXT_PASSAGE_NOT_FOUND", "critical", rid, "Context refers to a nonexistent passage")
            problem = True
        if r.get("mode") == "inferred" and r.get("voice") == "author":
            add("PROPOSITION_NOT_AUTHOR_EXPLICIT", "review", rid,
                "Inferred hidden premise cannot be described as explicitly written by author")
        if r.get("voice") in {"opponent", "quoted_source", "hypothetical"} and r.get("mode") == "explicit":
            add("EXTERNAL_POSITION_UNADOPTED", "review", rid,
                "Exact sentence is NOT automatically adopted by dissertation author")
        if r.get("voice") == "uncertain":
            add("PASSAGE_CONTEXT_UNCERTAIN", "review", rid,
                "Reviewer must establish speaker / stance before final author attribution")
        if problem:
            bad.add(rid)
        relevant = [d for d in decisions if isinstance(d, dict) and d.get("claim_id") == rid]
        latest = relevant[-1] if relevant else None
        status = "PROPOSED"
        if latest:
            if latest.get("fingerprint") != fingerprints.get(rid) or latest.get("draft_sha256") != block.get("draft_sha256"):
                status = "STALE_APPROVAL"
                add("APPROVAL_STALE", "critical", rid,
                    "Source, proposition, premise dependency, or reconstruction data changed after prior decision")
            elif latest.get("attestation") != "interactive_self_attested" or not nonempty(latest.get("reviewer_label")):
                status = "UNREVIEWABLE"
                add("APPROVAL_NOT_VERIFIABLE", "critical", rid,
                    "Decision needs declared local-interactive self-attestation; NOT an external signature")
            elif latest.get("decision") == "accept":
                status = "RESEARCHER_CONFIRMED"
            elif latest.get("decision") == "reject":
                status = "RESEARCHER_REJECTED"
            elif latest.get("decision") == "revise":
                status = "REVISION_REQUESTED"
            else:
                status = "UNREVIEWABLE"
                add("INVALID_REVIEW_DECISION", "critical", rid, "Unknown decision")
        if not real_text or problem or rid in bad or cycles:
            if status == "RESEARCHER_CONFIRMED":
                status = "SOURCE_INVALID"
        if status == "RESEARCHER_CONFIRMED":
            confirmed.add(rid)
        states.append({
            "id": rid, "status": status, "voice": r.get("voice"),
            "mode": r.get("mode"), "passage_id": r.get("passage_id"),
            "quote_verified_against_original": bool(real_text and not problem),
            "self_attested_not_identity_verified": status == "RESEARCHER_CONFIRMED",
        })

    # Approval is not transitive unless every premise was itself confirmed and current.
    for s in states:
        if s["status"] == "RESEARCHER_CONFIRMED":
            rec = records[s["id"]]
            uncertain_parents = [pid for pid in rec.get("premise_ids", []) if pid not in confirmed]
            if uncertain_parents:
                s["status"] = "UNREVIEWABLE"
                add("DEPENDENCY_UNCONFIRMED", "major", s["id"],
                    "Derived proposition depends on unapproved/invalid premises: " + ", ".join(uncertain_parents))
                confirmed.discard(s["id"])
    # Critical safeguard: a preexisting v0.4 graph may falsely claim approval.
    for claim in case.get("claims", []):
        if not isinstance(claim, dict):
            continue
        cid = claim.get("id")
        r = records.get(cid)
        if not r:
            add("GRAPH_CLAIM_NOT_RECONSTRUCTED", "major", str(cid),
                "Existing graph claim lacks fidelity record; cannot inherit confirmed status")
            continue
        if claim.get("text") != r.get("proposition"):
            add("GRAPH_PROPOSITION_DRIFT", "critical", str(cid),
                "Graph proposition differs from fidelity-reviewed reconstruction text")
        if claim.get("attribution") == "author" and r.get("voice") != "author":
            add("GRAPH_SPEAKER_LAUNDERING", "critical", str(cid),
                "Graph ascribes opponent/quoted/hypothetical/uncertain position to dissertation author")
        if claim.get("provenance") == "author_explicit" and r.get("mode") != "explicit":
            add("GRAPH_EXPLICITNESS_LAUNDERING", "critical", str(cid),
                "An inferred or paraphrased record cannot be silently labelled author_explicit")
        if claim.get("provenance") in ("researcher_approved", "author_explicit") and cid not in confirmed:
            add("GRAPH_APPROVAL_UNSUPPORTED", "critical", str(cid),
                "Graph claims author approval unsupported by current self-attested source-bound P1 decision")

    if not records:
        add("RECONSTRUCTION_PENDING", "review", "reconstruction.records",
            "No authored propositions reconstructed from original draft")
    approved = sum(s["status"] == "RESEARCHER_CONFIRMED" for s in states)
    stale = sum(s["status"] == "STALE_APPROVAL" for s in states)
    severe = sum(f["level"] == "critical" for f in flags)
    if severe:
        gate = "BLOCKED_SOURCE_OR_APPROVAL"
    elif not records:
        gate = "RECONSTRUCTION_REQUIRED"
    elif approved != len(records):
        gate = "RESEARCHER_REVIEW_REQUIRED"
    else:
        gate = "SELF_ATTESTED_FIDELITY_ONLY"
    return {
        "protocol": PROTOCOL, "gate": gate, "records": states,
        "counts": {"confirmed": approved, "unconfirmed": len(states)-approved, "stale": stale},
        "findings": flags, "originality": "LOCKED",
        "disclaimer": (
            "Verbatim/offset/source hashes are mechanical. Voice, meaning and researcher "
            "decisions are self-attested, NOT independently authenticated or semantically proven; "
            "no academic validity, legal correctness, or novelty is certified."
        ),
    }


def add_decision(case: dict, original_text: str, rid: str, reviewer_label: str,
                 decision: str, reason: str, confirmation: str) -> dict:
    """Record an *explicit* approval, only after the human passes the CLI prompt.

    Callers must obtain the exact confirmation phrase from a real human, never
    auto-generate it in a deployed agent. Tests may supply it synthetically.
    """
    if decision not in REVIEW_CHOICES:
        raise ValueError("Decision must accept / reject / revise")
    if not nonempty(reviewer_label) or not nonempty(reason):
        raise ValueError("Reviewer label and explicit reason are required")
    review = inspect(case, original_text)
    rid_map = {r["id"]: r for r in case["reconstruction"]["records"]}
    if rid not in rid_map:
        raise ValueError("No such claim")
    fatal = [f for f in review["findings"]
             if f["level"] == "critical" and f["target"] in {rid, "draft", "draft.sha256"}]
    if fatal:
        raise ValueError("Source/record is invalid; cannot record approval")
    fingerprints, cycles, missing = _fingerprints(rid_map, case["reconstruction"]["draft_sha256"])
    if cycles or missing:
        raise ValueError("Unresolved graph dependency prevents approval")
    if confirmation != f"CONFIRM {rid} {fingerprints[rid][:12]}":
        raise ValueError("Explicit interactive confirmation phrase required; never auto-approve")
    out = copy.deepcopy(case)
    out["reconstruction"]["decisions"].append({
        "claim_id": rid, "decision": decision, "reason": reason,
        "reviewer_label": reviewer_label,
        "attestation": "interactive_self_attested",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "fingerprint": fingerprints[rid],
        "draft_sha256": case["reconstruction"]["draft_sha256"],
    })
    return out


def approval_challenge(case: dict, rid: str) -> str:
    block = case["reconstruction"]
    recs = _records_by_id(block["records"])
    if rid not in recs:
        raise ValueError("Unknown claim ID")
    hashes, cycles, missing = _fingerprints(recs, block["draft_sha256"])
    if cycles or missing:
        raise ValueError("Unresolved reconstruction dependencies")
    return f"CONFIRM {rid} {hashes[rid][:12]}"


def render_report(case: dict, original_text: str | None) -> str:
    r = inspect(case, original_text)
    lines = [
        "# DOCTRINA P1 — Author-Faithful Reconstruction",
        "", "**Gate:** " + r["gate"],
        "", "## Claim-level fidelity", "",
    ]
    for rec in r["records"]:
        lines.append(f"- **{rec['id']}** — {rec['status']} | voice={rec['voice']} | "
                     f"mode={rec['mode']} | passage={rec['passage_id']} | "
                     f"original match={rec['quote_verified_against_original']}")
    lines += ["", "## Source, attribution and approval findings", ""]
    if not r["findings"]:
        lines.append("No declared mechanical findings; substantive accuracy is not certified.")
    else:
        for f in r["findings"]:
            lines.append(f"- **{f['code']}** [{f['level']}] {f['target']}: {f['explanation']}")
    lines += ["", "## Integrity notes", "",
              "- Source excerpts must match an independent, authorized original draft.",
              "- Voice classifications need nearby text and human interpretation.",
              "- A local decision is self-attested, NOT a cryptographic identity verification.",
              "- Modified draft text, a proposition, or a premise revokes affected approvals.",
              "- Existing graph author-attribution is blocked without matching live P1 approvals.",
              "- Do not run novelty review: normative / interpretative / conceptual remain LOCKED.",
              "", r["disclaimer"], ""]
    return "\n".join(lines)
