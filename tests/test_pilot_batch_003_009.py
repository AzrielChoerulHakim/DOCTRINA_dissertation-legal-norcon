"""PILOTS P003-P009: seven real, published dissertation SHORT-EXCERPT tests.

Only brief phrases copied from university-hosted PDFs are stored. These synthetic
argument graphs are PROPOSED BY THE AUDITOR and do not model full dissertations.
A passing test validates code behaviour on these anchored excerpts, not
accuracy of source parsing, inferential adequacy or academic acceptability.
"""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from doctrina_core import new_case, validate, review, markdown_report
from audit_argument_graph import revision_impact

BATCH = json.loads((ROOT / "examples" / "dissertation_batch_003_009.json").read_text(encoding="utf-8"))
CASES = BATCH["cases"]


def build_pilot(spec):
    """Construct a reviewer-proposed graph from SHORT source excerpts.

    Crucially, passage_id anchors the auditor-supplied excerpt file, not the
    whole source PDF; upstream PDF fidelity is NOT automatically verified.
    """
    c = new_case(
        "\n\n".join(spec["anchors"]),
        spec["object"],
        spec["object_title"],
        locus=spec["locus"],
        jurisdiction=spec["jurisdiction"],
        temporal_scope=spec["temporal_scope"],
        source_filename=spec["id"].lower() + "_short_excerpts_only.txt",
    )
    c["research_object"]["source_state"] = "partial"
    if spec["object"] == "norm":
        c["research_object"]["legal_materials"] = [{
            "locator": spec["locus"],
            "inspection_status": "partial",
            "verification_limit": "human viewed selected extracted PDF passages; original PDF bytes not validated by runtime",
        }]
    else:
        c["research_object"]["concept_usages"] = [{
            "usage": spec["object_title"],
            "locator": spec["locus"],
            "inspection_status": "partial",
        }]
    c["sources"] = [{
        "id": "S_THESIS",
        "title": spec["title"],
        "author": spec["author"],
        "year": spec["year"],
        "url": spec["pdf"],
        "locator": spec["locus"],
        "inspection_status": "partial",
    }]
    if spec.get("comparator"):
        c["sources"].append({
            "id": "S_LATER_CASE",
            "title": "Later authority; NOT available to the historical thesis author",
            "url": spec["comparator"],
            "inspection_status": "partial",
        })
    c["source_review"] = {
        "kind": spec["depth"],
        "source_excerpts_only": True,
        "upstream_pdf_text_not_machine_verified": True,
        "researcher_approved": False,
        "auditor_hypothesis_not_thesis_verdict": True,
    }
    shared = {
        "attribution": "proposed",
        "provenance": "ai_proposed",
        "quotes": [],
        "support": [{"source_id": "S_THESIS", "state": "partial"}],
    }
    ids = ["P1", "P2", "C1"]
    for i, cid in enumerate(ids):
        is_conclusion = i == 2
        claim = {
            **shared,
            "id": cid,
            "kind": spec["kinds"][i],
            "role": "derived" if is_conclusion else "premise",
            "text": spec["reconstructed"][i],
            "chapter_id": "CH2" if is_conclusion else "CH1",
            "passage_id": f"T{i+1:04d}",
            "anchor_text": spec["anchors"][i],
            "premises": ["P1", "P2"] if is_conclusion else [],
        }
        if is_conclusion:
            claim["inference"] = "interpretative" if claim["kind"] != "normative" else "normative-constructive"
            claim["warrant"] = {
                "text": spec["warrant"],
                "status": "ai_proposed",
                "normative_bridge": spec["object"] == "norm" and spec["kinds"][1] == "normative",
            }
        c["claims"].append(claim)
    c["central_claim_id"] = "C1"
    c["chapters"] = [
        {"id": "CH1", "title": "Sources and premise register; NOT actual chapter labels",
         "claim_ids": ["P1", "P2"],
         "argumentative_task": "Reconstruct premise-level distinctions from selected passages"},
        {"id": "CH2", "title": "Proposed central inference; NOT an actual chapter label",
         "claim_ids": ["C1"],
         "argumentative_task": "Track bounded examiner objection and possible counterargument"},
    ]
    c["objections"] = [{
        "id": "O1",
        "target_id": "C1",
        "status": "open",
        "severity": "major",
        "text": spec["challenge"],
        "proposed_charitable_reply": spec["reply"],
        "researcher_approved": False,
    }]
    return c


class BatchTest(unittest.TestCase):
    def check_case(self, spec):
        case = build_pilot(spec)
        findings = validate(case)
        codes = {f["code"] for f in findings}
        self.assertEqual(case["research_object"]["primary_type"], spec["object"])
        self.assertNotIn("OBJECT_OUT_OF_SCOPE", codes)
        self.assertNotIn("AI_PROPOSED_AS_AUTHOR", codes)
        self.assertNotIn("CLAIM_UNANCHORED", codes)
        self.assertNotIn("QUOTE_NOT_IN_PASSAGE", codes)
        self.assertTrue(all(x["provenance"] == "ai_proposed" for x in case["claims"]))
        self.assertTrue(case["source_review"]["upstream_pdf_text_not_machine_verified"])
        self.assertFalse(case["readiness"]["researcher_approved"])
        self.assertEqual(case["originality"]["stage"], "locked")
        self.assertEqual(case["originality"]["final_status"], "NOT_READY")
        result = review(case)
        self.assertEqual(result["gate"], "STRUCTURAL_REVIEW_WITH_LIMITATIONS")
        machine_codes = {f["code"] for f in result["findings"]}
        self.assertIn("OPEN_SERIOUS_OBJECTION", machine_codes)
        self.assertNotIn("IA-06", machine_codes,
                         "Do not manufacture a missing normative bridge when the auditor records one")
        self.assertEqual(result["counts"]["critical"], 0,
                         "Full authored arguments are NOT reconstructed, so no critical scholarly verdict")
        self.assertIn("NOT validation of legal meaning", result["disclaimer"])
        self.assertIn("LOCKED", markdown_report(case))
        return case

    def test_p003_liau_standing(self):
        self.check_case(CASES[0])

    def test_p004_downey_identity(self):
        self.check_case(CASES[1])

    def test_p005_mcmillan_embryo(self):
        self.check_case(CASES[2])

    def test_p006_dyrkolbotn_takings(self):
        self.check_case(CASES[3])

    def test_p007_frydrych_rights(self):
        self.check_case(CASES[4])

    def test_p008_conte_penalties(self):
        case = self.check_case(CASES[5])
        self.assertIn("2014", case["research_object"]["temporal_scope"])
        self.assertEqual(len(case["sources"]), 2,
                         "Later 2015 authority must be separate from the 2014 thesis text")

    def test_p009_gunatilleke_iccpr(self):
        self.check_case(CASES[6])

    def test_author_imposture_negative_control(self):
        case = build_pilot(CASES[0])
        case["claims"][0]["attribution"] = "author"
        self.assertIn("AI_PROPOSED_AS_AUTHOR", {x["code"] for x in validate(case)})

    def test_normative_bridge_omission_negative_control(self):
        # NOT a genuine finding against P006 or P009; show how bad reconstruction
        # can create an artificial serious IA-06 machine flag.
        case = build_pilot(CASES[6])
        case["claims"][1]["kind"] = "descriptive"
        case["claims"][2]["warrant"]["normative_bridge"] = False
        self.assertIn("IA-06", {f["code"] for f in review(case)["findings"]})

    def test_norm_source_remains_partially_inspected(self):
        for spec in CASES:
            if spec["object"] == "norm":
                self.assertIn("NORM_SOURCE_UNVERIFIED",
                    {x["code"] for x in validate(build_pilot(spec))})

    def test_change_propagation_premise_to_conclusion(self):
        for spec in CASES:
            impact = revision_impact(build_pilot(spec), "P1")
            self.assertEqual(impact["downstream_claim_ids"], ["C1"])
            self.assertEqual(impact["affected_chapter_ids"], ["CH1", "CH2"])

    def test_bounded_quoting_and_distinct_real_sources(self):
        self.assertEqual(len(CASES), 7)
        self.assertEqual(len({c["pdf"] for c in CASES}), 7)
        for spec in CASES:
            # Copyright: each indexed thesis contributes well under 25
            # directly quoted words to this test fixture.
            self.assertLessEqual(sum(len(p.split()) for p in spec["anchors"]), 25)
            self.assertIn(spec["object"], {"norm", "concept"})

    def test_early_novelty_inference_is_rejected(self):
        case = build_pilot(CASES[4])
        case["originality"]["stage"] = "final"
        self.assertIn("NOVELTY_EARLY", {x["code"] for x in validate(case)})


if __name__ == "__main__":
    unittest.main()
