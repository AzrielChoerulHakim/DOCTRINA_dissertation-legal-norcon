"""P1 in core and CLI: fail-closed integration; no inferred legal truth."""
from __future__ import annotations
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from doctrina_core import new_case, review, markdown_report
from doctrina_fidelity import begin, propose, add_decision, approval_challenge
from test_fidelity_p1 import DRAFT, make_case, add_record


class CoreIntegration(unittest.TestCase):
    def test_core_01_no_p1_remains_legacy_compatible(self):
        legacy = new_case(DRAFT, "concept", "Kepentingan umum", locus="ilustrasi")
        self.assertEqual(review(legacy)["gate"], "DRAFT_RECONSTRUCTION_REQUIRED")
        self.assertIsNone(review(legacy)["fidelity"])

    def test_core_02_p1_without_external_draft_fails_closed(self):
        case = add_record(make_case())
        result = review(case)
        self.assertEqual(result["gate"], "INTERNAL_REVISION_REQUIRED")
        self.assertIn("ORIGINAL_DRAFT_UNAVAILABLE", {x["code"] for x in result["findings"]})

    def test_core_03_p1_with_original_but_unreviewed_not_success(self):
        case = add_record(make_case())
        result = review(case, original_text=DRAFT)
        self.assertEqual(result["fidelity"]["gate"], "RESEARCHER_REVIEW_REQUIRED")
        self.assertEqual(result["gate"], "DRAFT_RECONSTRUCTION_REQUIRED")

    def test_core_04_approved_fidelity_does_not_certify_valid_norm(self):
        case = add_record(make_case())
        case = add_decision(
            case, DRAFT, "P1", "Test researcher", "accept", "Read with context",
            approval_challenge(case, "P1"))
        result = review(case, original_text=DRAFT)
        self.assertEqual(result["fidelity"]["gate"], "SELF_ATTESTED_FIDELITY_ONLY")
        self.assertEqual(result["gate"], "DRAFT_RECONSTRUCTION_REQUIRED")
        self.assertIn("NOT validation of legal meaning", result["disclaimer"])

    def test_core_05_markdown_contains_fidelity_section(self):
        case = add_record(make_case())
        result = markdown_report(case, original_text=DRAFT)
        self.assertIn("DOCTRINA P1", result)
        self.assertIn("RESEARCHER_REVIEW_REQUIRED", result)
        self.assertIn("LOCKED", result)

    def test_core_06_author_laundering_is_critical(self):
        case = add_record(make_case(), voice="uncertain")
        case["claims"] = [{
            "id": "P1", "role": "premise", "kind": "conceptual",
            "premises": [], "passage_id": "T0001",
            "text": case["reconstruction"]["records"][0]["proposition"],
            "attribution": "author", "provenance": "author_explicit",
            "anchor_text": case["reconstruction"]["records"][0]["span"]["quote"],
        }]
        result = review(case, original_text=DRAFT)
        codes = {x["code"] for x in result["findings"]}
        self.assertIn("GRAPH_SPEAKER_LAUNDERING", codes)
        self.assertIn("GRAPH_APPROVAL_UNSUPPORTED", codes)

    def test_core_07_old_check_cli_requires_original_for_p1(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            case = add_record(make_case())
            case_path = folder/"case.json"
            draft_path = folder/"draft.txt"
            case_path.write_text(json.dumps(case, ensure_ascii=False), encoding="utf-8")
            draft_path.write_text(DRAFT, encoding="utf-8")
            cli = [sys.executable, str(ROOT/"scripts"/"doctrina_cli.py")]
            no_original = subprocess.run(cli+["check", str(case_path)],
                                         capture_output=True, text=True)
            self.assertEqual(no_original.returncode, 2)
            self.assertIn("ORIGINAL_DRAFT_UNAVAILABLE", no_original.stdout)
            with_original = subprocess.run(
                cli+["check", str(case_path), "--original-draft", str(draft_path)],
                capture_output=True, text=True)
            self.assertEqual(with_original.returncode, 0, with_original.stderr)
            result = json.loads(with_original.stdout)
            self.assertEqual(result["fidelity"]["gate"], "RESEARCHER_REVIEW_REQUIRED")

    def test_core_08_markdown_report_no_source_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            case = add_record(make_case())
            file = folder/"case.json"
            file.write_text(json.dumps(case, ensure_ascii=False), encoding="utf-8")
            cli = [sys.executable, str(ROOT/"scripts"/"doctrina_cli.py")]
            r = subprocess.run(cli+["report", str(file)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)
            self.assertIn("ORIGINAL_DRAFT_UNAVAILABLE", r.stdout)


if __name__ == "__main__":
    unittest.main()
