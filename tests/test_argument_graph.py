"""Executable mechanical tests; they do NOT validate substantive doctoral reasoning."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_argument_graph import audit_document, revision_impact  # noqa: E402

with (ROOT / "examples" / "kepentingan-umum-illustrative.json").open(encoding="utf-8") as fh:
    DEMO = json.load(fh)


class ArgumentGraphTests(unittest.TestCase):
    def base(self):
        return copy.deepcopy(DEMO)

    @staticmethod
    def has(report, code):
        return any(x["code"] == code for x in report["findings"])

    def test_M01_positive_complete_synthetic(self):
        result = audit_document(self.base())
        self.assertEqual(result["counts"]["critical"], 0)

    def test_M02_missing_derived_warrant(self):
        x = self.base()
        del x["claims"][2]["warrant"]
        report = audit_document(x)
        self.assertTrue(self.has(report, "IA-01"))
        self.assertEqual(report["gate"], "INTERNAL_REVISION_REQUIRED")

    def test_M03_dangling_premise(self):
        x = self.base()
        x["claims"][2]["premises"].append("P404")
        self.assertTrue(self.has(audit_document(x), "DANGLING_PREMISE"))

    def test_M04_descriptive_only_to_normative_is_blocked(self):
        x = self.base()
        x["claims"][1]["kind"] = "descriptive"
        x["claims"][2]["warrant"]["normative_bridge"] = False
        self.assertTrue(self.has(audit_document(x), "IA-06"))

    def test_M05_explicit_bridge_is_not_auto_rejected(self):
        x = self.base()
        x["claims"][1]["kind"] = "descriptive"
        x["claims"][2]["warrant"]["normative_bridge"] = True
        self.assertFalse(self.has(audit_document(x), "IA-06"))

    def test_M06_recursive_cycle_is_review_not_auto_fallacy(self):
        x = self.base()
        x["claims"][0]["role"] = "derived"
        x["claims"][0]["premises"] = ["C1"]
        x["claims"][0]["warrant"] = {"text": "Putative reflective-equilibrium feedback"}
        r = audit_document(x)
        self.assertTrue(self.has(r, "IA-02"))
        self.assertFalse(any(a["code"] == "IA-02" and a["level"] == "critical" for a in r["findings"]))

    def test_M07_unverified_verbatim_quote_is_blocked(self):
        x = self.base()
        x["sources"] = [{"id": "S1", "title": "Example metadata"}]
        x["claims"][2]["quotes"] = [{"source_id": "S1", "text": "Quoted words", "inspection_status": "metadata_only", "locator": ""}]
        self.assertTrue(self.has(audit_document(x), "UNVERIFIED_QUOTE"))

    def test_M08_open_serious_objection_blocks_final(self):
        x = self.base()
        x["objections"][0]["status"] = "open"
        self.assertTrue(self.has(audit_document(x, "pre-originality"), "OPEN_SERIOUS_OBJECTION"))
        self.assertEqual(audit_document(x, "pre-originality")["gate"], "ORIGINALITY_REVIEW_INCOMPLETE")

    def test_M09_revision_cascades_to_claim_and_chapters(self):
        r = revision_impact(self.base(), "P2")
        self.assertEqual(r["downstream_claim_ids"], ["C1"])
        self.assertEqual(r["affected_chapter_ids"], ["CH1", "CH2"])

    def test_M10_incomplete_reviews_block_final(self):
        x = self.base()
        x["readiness"].update({k: "passed" for k in ("internal_review", "dialectical_review", "integration_review", "defense_review")})
        x["readiness"]["researcher_approved"] = True
        x["readiness"]["defense_review"] = "pending"
        self.assertTrue(self.has(audit_document(x, "pre-originality"), "REVIEW_NOT_PASSED"))

    def test_M11_direct_self_dependency_blocked(self):
        x = self.base()
        x["claims"][2]["premises"] = ["P1", "C1"]
        self.assertTrue(self.has(audit_document(x), "DIRECT_SELF_DEPENDENCY"))

    def test_M12_duplicate_id_blocked(self):
        x = self.base()
        x["claims"].append(copy.deepcopy(x["claims"][0]))
        self.assertTrue(self.has(audit_document(x), "DUPLICATE_ID"))

    def test_M13_metadata_not_substantive_evidence(self):
        x = self.base()
        x["sources"] = [{"id": "S1", "title": "Unexamined book"}]
        x["claims"][0]["support"] = [{"source_id": "S1", "state": "metadata_only", "supports_substance": True}]
        self.assertTrue(self.has(audit_document(x), "METADATA_NOT_SUBSTANCE"))

    def test_M14_ready_only_for_last_review_not_novelty_certification(self):
        x = self.base()
        x["readiness"].update({k: "passed" for k in ("internal_review", "dialectical_review", "integration_review", "defense_review")})
        x["readiness"]["researcher_approved"] = True
        x["objections"][0]["status"] = "responded"
        report = audit_document(x, "pre-originality")
        self.assertEqual(report["gate"], "READY_FOR_FINAL_ORIGINALITY_REVIEW")
        self.assertIn("NOT semantic validity", report["disclaimer"])

    def test_M15_absent_researcher_approval_blocks_final(self):
        x = self.base()
        x["readiness"].update({k: "passed" for k in ("internal_review", "dialectical_review", "integration_review", "defense_review")})
        x["readiness"]["researcher_approved"] = False
        self.assertTrue(self.has(audit_document(x, "pre-originality"), "NO_RESEARCHER_APPROVAL"))

    def test_M16_cross_chapter_link_missing(self):
        x = self.base()
        x["chapters"][1]["claim_ids"] = ["C404"]
        self.assertTrue(self.has(audit_document(x), "CHAPTER_DANGLING_CLAIM"))

    def test_M17_declared_contradiction_requires_review(self):
        x = self.base()
        x["claims"][0]["contradicts"] = ["P2"]
        r = audit_document(x)
        self.assertTrue(self.has(r, "IA-05"))
        self.assertTrue(any(f["code"] == "IA-05" and f["level"] == "review" for f in r["findings"]))

    def test_M18_nonexistent_claim_impact_returns_error(self):
        self.assertEqual(revision_impact(self.base(), "MISSING")["error"], "unknown claim")


if __name__ == "__main__":
    unittest.main()
