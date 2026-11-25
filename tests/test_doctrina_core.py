"""DOCTRINA v0.4: structural/evidentiary regression tests, NOT scholarly validity tests."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from doctrina_core import (new_case, migrate_legacy, read_case, review, validate,
                           markdown_report, split_passages)


class DoctrinaCoreTests(unittest.TestCase):
    def concept(self):
        x = new_case("Definisi kepentingan umum memerlukan justifikasi.\n\n"
                     "Akibat pembatasan hak harus ditelaah.", "concept", "Kepentingan umum",
                     locus="penggunaan dalam aturan pengadaan tanah")
        x["research_object"]["concept_usages"] = [
            {"usage": "kepentingan umum", "locator": "contoh sintetis: paragraf 1",
             "inspection_status": "unverified"}
        ]
        return x

    def norm(self):
        x = new_case("Norma hipotetis A berlaku dengan syarat B.", "norm", "Norma A",
                     locus="ketentuan hipotetis A", jurisdiction="Indonesia",
                     temporal_scope="skenario hipotetis")
        x["research_object"]["legal_materials"] = [
            {"locator": "sumber sintetis A", "inspection_status": "inspected"}
        ]
        return x

    @staticmethod
    def codes(x):
        return {v["code"] for v in validate(x)}

    def test_v01_reject_theory_object(self):
        with self.assertRaises(ValueError):
            new_case("text", "theory", "Kelsen")

    def test_v02_required_legal_object_name(self):
        with self.assertRaises(ValueError):
            new_case("text", "norm", "")

    def test_v03_norm_case_is_accepted(self):
        x = self.norm()
        self.assertNotIn("OBJECT_OUT_OF_SCOPE", self.codes(x))
        self.assertNotIn("NORM_NO_JURISDICTION", self.codes(x))

    def test_v04_concept_case_is_accepted(self):
        self.assertNotIn("CONCEPT_USAGE_NOT_INSPECTED", self.codes(self.concept()))

    def test_v05_detect_missing_norm_source_and_scope(self):
        x = new_case("teks", "norm", "Norma", locus="Pasal ilustratif")
        self.assertTrue({"NORM_NO_JURISDICTION", "NORM_NO_TEMPORAL_SCOPE",
                         "NORM_SOURCE_NOT_INSPECTED"}.issubset(self.codes(x)))

    def test_v06_concept_usage_missing(self):
        x = new_case("teks", "concept", "Konsep", locus="contoh ilustratif")
        self.assertIn("CONCEPT_USAGE_NOT_INSPECTED", self.codes(x))

    def test_v07_preserves_verbatim_and_line_offsets(self):
        draft = "  Argumen α satu.\n\nArgumen β dua.\n"
        result = split_passages(draft)
        self.assertEqual(len(result), 2)
        for paragraph in result:
            self.assertEqual(draft[paragraph["start_offset"]:paragraph["end_offset"]], paragraph["verbatim"])
        self.assertEqual(result[1]["start_line"], 3)

    def test_v08_intake_does_not_invent_claims(self):
        x = self.concept()
        self.assertEqual(x["claims"], [])
        self.assertEqual(x["central_claim_id"], None)
        self.assertEqual(review(x)["gate"], "DRAFT_RECONSTRUCTION_REQUIRED")

    def test_v09_detect_theory_object_in_json_tampering(self):
        x = self.concept()
        x["research_object"]["primary_type"] = "theory"
        self.assertIn("OBJECT_OUT_OF_SCOPE", self.codes(x))

    def test_v10_annotated_author_claim_requires_exact_quote(self):
        x = self.concept()
        x["claims"] = [{
            "id": "P1", "text": "Pemahaman konsep itu belum cukup.",
            "kind": "conceptual", "role": "premise", "premises": [],
            "attribution": "author", "provenance": "author_explicit",
            "passage_id": "T0001", "anchor_text": "kalimat yang tidak terdapat dalam paragraf",
        }]
        self.assertIn("AUTHOR_QUOTE_NOT_VERIFIED", self.codes(x))
        self.assertEqual(review(x)["gate"], "INTERNAL_REVISION_REQUIRED")

    def test_v11_legitimate_exact_quote_allowed(self):
        x = self.concept()
        x["claims"] = [{
            "id": "P1", "text": "Menganalisis definisi",
            "kind": "conceptual", "role": "premise", "premises": [],
            "attribution": "author", "provenance": "author_explicit",
            "passage_id": "T0001", "anchor_text": "Definisi kepentingan umum",
        }]
        self.assertNotIn("AUTHOR_QUOTE_NOT_VERIFIED", self.codes(x))

    def test_v12_ai_cannot_silently_impersonate_author(self):
        x = self.concept()
        x["claims"] = [{
            "id": "C1", "kind": "conceptual", "role": "premise", "premises": [],
            "text": "Asumsi usulan AI", "passage_id": "T0001",
            "attribution": "author", "provenance": "ai_proposed",
        }]
        self.assertIn("AI_PROPOSED_AS_AUTHOR", self.codes(x))

    def test_v13_reconstructed_opponent_premise_not_auto_adopted(self):
        x = self.concept()
        x["claims"] = [
            {"id": "P1", "kind": "conceptual", "role": "premise", "premises": [],
             "text": "Premis lawan", "passage_id": "T0001",
             "attribution": "opponent", "provenance": "researcher_approved"},
            {"id": "C1", "kind": "normative", "role": "derived", "premises": ["P1"],
             "warrant": {"text": "Jembatan perlu diuji", "normative_bridge": True},
             "text": "Kesimpulan peneliti", "passage_id": "T0001",
             "attribution": "author", "provenance": "researcher_approved",
             "inference": "normative-constructive"},
        ]
        self.assertIn("RIVAL_PREMISE_UNADOPTED", self.codes(x))

    def test_v14_originality_locked(self):
        x = self.concept()
        x["originality"] = {"stage": "final", "final_status": "SUPPORTED_WITH_LIMITATIONS"}
        self.assertIn("NOVELTY_EARLY", self.codes(x))

    def test_v15_normative_defect_found_by_existing_engine(self):
        x = self.concept()
        x["claims"] = [
            {"id": "P1", "kind": "descriptive", "role": "premise", "premises": [],
             "text": "Negara menentukan suatu istilah", "passage_id": "T0001",
             "attribution": "author", "provenance": "researcher_approved"},
            {"id": "C1", "kind": "normative", "role": "derived", "premises": ["P1"],
             "warrant": {"text": "Asal definisi dianggap cukup", "normative_bridge": False},
             "inference": "normative-constructive", "text": "Semua tindakan tidak sah",
             "passage_id": "T0002", "attribution": "author",
             "provenance": "researcher_approved"},
        ]
        x["central_claim_id"] = "C1"
        self.assertIn("IA-06", {f["code"] for f in review(x)["findings"]})

    def test_v16_legacy_case_migration_explicit(self):
        old = {"claims": [{"id": "C1", "role": "premise", "kind": "conceptual",
                           "text": "Legacy assertion", "premises": []}],
               "central_claim_id": "C1", "chapters": [], "sources": [],
               "objections": [], "readiness": {}}
        x = migrate_legacy(old, "concept", "Kepentingan umum")
        self.assertEqual(x["schema_version"], "0.4.0")
        self.assertEqual(x["claims"][0]["provenance"], "legacy_unverified")
        self.assertIn("CLAIM_UNANCHORED", self.codes(x))

    def test_v17_report_makes_provenance_limits_explicit(self):
        x = self.concept()
        report = markdown_report(x)
        self.assertIn("NOT", report)
        self.assertIn("LOCKED", report)
        self.assertIn("candidate text units", report)

    def test_v18_source_filename_sanitized(self):
        x = new_case("hi", "norm", "Norm", source_filename="/private/secret/draft.txt")
        self.assertEqual(x["draft"]["filename"], "draft.txt")
        self.assertNotIn("/private", json.dumps(x))

    def test_v19_cli_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            draft = Path(folder)/"draft.txt"
            case = Path(folder)/"case.json"
            report = Path(folder)/"report.md"
            draft.write_text("Pernyataan hipotetis.\n\nPernyataan kedua.", encoding="utf-8")
            command = [sys.executable, str(ROOT/"scripts"/"doctrina_cli.py")]
            p = subprocess.run(command + ["init", "--input", str(draft),
                           "--object", "concept", "--title", "Kepentingan umum",
                           "--locus", "contoh", "--out", str(case)],
                           capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(len(read_case(case)["draft"]["passages"]), 2)
            p = subprocess.run(command + ["report", str(case), "--out", str(report)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("DOCTRINA v0.4", report.read_text(encoding="utf-8"))

    def test_v20_regression_migration_does_not_claim_originality(self):
        x = migrate_legacy({"claims": [], "originality": {"final_status": "candidate"}},
                           "concept", "konsep contoh", locus="contoh")
        self.assertEqual(x["originality"]["stage"], "locked")
        self.assertEqual(x["originality"]["final_status"], "NOT_READY")


if __name__ == "__main__":
    unittest.main()
