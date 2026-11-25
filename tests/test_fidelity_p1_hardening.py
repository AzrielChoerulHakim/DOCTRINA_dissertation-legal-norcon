"""P1 hardening against context omission and proposition-mode laundering."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from doctrina_fidelity import inspect, add_decision, approval_challenge
from test_fidelity_p1 import make_case, add_record, DRAFT


class P1Hardening(unittest.TestCase):
    @staticmethod
    def codes(case):
        return {x["code"] for x in inspect(case, DRAFT)["findings"]}

    def test_h01_source_passage_must_be_in_reviewed_context(self):
        case = add_record(make_case())
        case["reconstruction"]["records"][0]["context_passage_ids"] = ["T0002"]
        self.assertIn("CONTEXT_SOURCE_NOT_REVIEWED", self.codes(case))

    def test_h02_author_question_cannot_become_assertion(self):
        case = add_record(make_case(), mode="question")
        case["claims"] = [{
            "id": "P1", "text": case["reconstruction"]["records"][0]["proposition"],
            "attribution": "author", "provenance": "ai_proposed",
            "passage_id": "T0001",
        }]
        self.assertIn("GRAPH_QUESTION_AS_ASSERTION", self.codes(case))

    def test_h03_conditional_author_statement_needs_qualifier(self):
        case = add_record(make_case(), mode="conditional")
        case["claims"] = [{
            "id": "P1", "text": case["reconstruction"]["records"][0]["proposition"],
            "attribution": "author", "provenance": "researcher_approved",
            "passage_id": "T0001",
        }]
        self.assertIn("GRAPH_CONDITION_DROPPED", self.codes(case))

    def test_h04_explicit_qualifier_preserves_conditional_mode(self):
        case = add_record(make_case(), mode="conditional")
        case["claims"] = [{
            "id": "P1", "text": case["reconstruction"]["records"][0]["proposition"],
            "attribution": "author", "provenance": "ai_proposed",
            "passage_id": "T0001", "qualifier": "Only if conditions A and B apply",
        }]
        self.assertNotIn("GRAPH_CONDITION_DROPPED", self.codes(case))

    def test_h05_approval_rejected_when_unrelated_original_passage_corrupted(self):
        case = add_record(make_case())
        case["draft"]["passages"][1]["verbatim"] += " FORGED"
        with self.assertRaisesRegex(ValueError, "invalid"):
            add_decision(case, DRAFT, "P1", "Researcher", "accept",
                         "Read the original", approval_challenge(case, "P1"))

    def test_h06_fidelity_records_cannot_inherit_approval_without_premise(self):
        case = add_record(make_case())
        case = add_record(case, rid="C1", passage="T0003",
                          quote="keputusan dapat diperdebatkan", premises=["P1"])
        case = add_decision(case, DRAFT, "C1", "Researcher", "accept",
                            "Confirm proposed conclusion conditionally",
                            approval_challenge(case, "C1"))
        result = inspect(case, DRAFT)
        self.assertIn("DEPENDENCY_UNCONFIRMED", {x["code"] for x in result["findings"]})
        self.assertEqual(result["counts"]["confirmed"], 0)


if __name__ == "__main__":
    unittest.main()
