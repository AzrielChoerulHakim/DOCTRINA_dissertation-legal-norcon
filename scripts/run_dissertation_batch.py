#!/usr/bin/env python3
"""Reproducible short-excerpt batch pilot audit (P003-P009).

Does NOT download/source-verify full PDF files. Findings diagnose an auditor-
proposed argument graph, not doctoral correctness, degree quality or novelty.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "tests")]

from doctrina_core import review
from test_pilot_batch_003_009 import CASES, build_pilot


def generate(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    results = []
    for spec in CASES:
        case = build_pilot(spec)
        machine = review(case)
        assert machine["counts"]["critical"] == 0, spec["id"]
        assert machine["gate"] == "STRUCTURAL_REVIEW_WITH_LIMITATIONS", spec["id"]
        result = {
            "id": spec["id"],
            "author": spec["author"],
            "year": spec["year"],
            "title": spec["title"],
            "research_object": spec["object"],
            "source_url": spec["repo"],
            "pdf_url": spec["pdf"],
            "selected_passage_locus": spec["locus"],
            "coverage": spec["depth"],
            "human_review_hypothesis": spec["challenge"],
            "strongest_charitable_reply": spec["reply"],
            "source_original_bytes_machine_verified": False,
            "actual_author_approval": False,
            "novelty_review": "LOCKED",
            "machine": machine,
        }
        results.append(result)
        print("{} | {} | gate={} | critical={} other={}".format(
            spec["id"], spec["object"], machine["gate"],
            machine["counts"]["critical"], machine["counts"]["other"]))
    report = {
        "batch": "P003-P009 (2026-11-25)",
        "research_object_counts": {"concept": sum(r["research_object"] == "concept" for r in results),
                                   "norm": sum(r["research_object"] == "norm" for r in results)},
        "tested": len(results),
        "status": "STRUCTURAL_PILOT_ONLY",
        "academic_semantic_accuracy": "NOT_MEASURED",
        "source_byte_hash_verification": "NOT_IMPLEMENTED",
        "researcher_confirmation_count": 0,
        "independent_academic_reviewer_count": 0,
        "explanation": "Results are assertions about a constructed reviewer hypothesis graph, not verified full doctoral manuscripts.",
        "results": results,
    }
    (outdir / "batch_machine_results.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    lines = [
        "# DOCTRINA Batch P003-P009 — Mechanical excerpt audit",
        "",
        "Status: TECHNICAL PASS / SUBSTANTIVE LEGAL ACCURACY UNVALIDATED.",
        "",
        "Case IDs | Object | Gate | Critical structural issues | Other review items",
        "---|---|---|---:|---:",
    ]
    for r in results:
        d = r["machine"]
        lines.append("{} | {} | {} | {} | {}".format(
            r["id"], r["research_object"], d["gate"], d["counts"]["critical"], d["counts"]["other"]))
    lines += ["", "## Scope warnings", "",
              "- The stored text contains micro-excerpts, not complete thesis paragraphs.",
              "- The source URL and chapter locator were verified by a human reviewer via repository-hosted searchable PDF text; Python verifies the excerpt's internal consistency but does NOT match it against PDF bytes.",
              "- All reconstructed claims are AI-proposed hypotheses, NOT the author's certified thesis propositions.",
              "- Review questions are qualitative prompts; mechanical 0 critical does NOT prove validity.",
              "- Final normative / interpretative / conceptual novelty remains LOCKED.",
              ""]
    for r in results:
        lines += ["## {} — {}".format(r["id"], r["title"]), "",
                  "- Source: " + r["source_url"],
                  "- Extract location: " + r["selected_passage_locus"],
                  "- Main objection to examine (not a verified scholarly error): " + r["human_review_hypothesis"],
                  "- Strongest possible answer: " + r["strongest_charitable_reply"],
                  ""]
    (outdir / "batch_machine_summary.md").write_text(
        "\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="/tmp/doctrina-batch", type=Path)
    args = parser.parse_args()
    generate(args.out_dir)
