"""P1 reconstruction fidelity regression / adversarial controls (synthetic Indonesian law prose).

Tests verify mechanics, not accurate legal interpretation or actual user identity.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from doctrina_core import new_case
from doctrina_fidelity import (
    begin, propose, version_sync, inspect, add_decision, approval_challenge,
    render_report, source_hash,
)

DRAFT = (
    "Penulis menyatakan bahwa kepentingan umum memerlukan pembatasan kewenangan.\n\n"
    "Menurut sarjana lain, semua tindakan negara selalu sah. Namun penulis menolak pendapat itu.\n\n"
    "Jika batas kewenangan tidak jelas, keputusan dapat diperdebatkan."
)


def make_case(text=DRAFT):
    case = new_case(text, "concept", "Kepentingan umum", locus="frasa dalam norma hipotetis",
                    jurisdiction="Indonesia")
    return begin(case, text)


def add_record(case, rid="P1", passage="T0001",
               quote="kepentingan umum memerlukan pembatasan kewenangan",
               voice="author", mode="explicit", premises=None, start=None, **extra):
    target = next(p for p in case["draft"]["passages"] if p["id"] == passage)
    a = target["verbatim"].find(quote) if start is None else start
    record = {
        "id": rid, "passage_id": passage, "span": {
            "start": a, "end": a+len(quote), "quote": quote,
        },
        "voice": voice, "mode": mode,
        "proposition": "Pembatasan kewenangan perlu dikaji untuk konsep kepentingan umum.",
        "voice_basis": "Kalimat penulis pada paragraf bersangkutan; belum disahkan",
        "context_passage_ids": ["T0001", "T0002"],
        "premise_ids": premises if premises is not None else [],
        "proposed_by": "auditor_unapproved",
    }
    record.update(extra)
    return propose(case, record)


def decided(case, rid="P1", decision="accept", reason="Saya telah memeriksa kalimat dan konteks"):
    return add_decision(case, DRAFT, rid, "Researcher test fixture", decision, reason,
                        approval_challenge(case, rid))


class FidelityTests(unittest.TestCase):
    def setUp(self):
        self.case = make_case()
        self.one = add_record(self.case)

    @staticmethod
    def codes(c, text=DRAFT):
        return {x["code"] for x in inspect(c, text)["findings"]}

    def test_p101_initialize_no_semantic_guess(self):
        self.assertEqual(self.case["reconstruction"]["records"], [])
        self.assertEqual(self.case["reconstruction"]["decisions"], [])

    def test_p102_reject_unmatched_original_hash(self):
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            begin(new_case("Text A", "concept", "C"), "Text B")

    def test_p103_reject_self_inconsistent_passage(self):
        x = new_case(DRAFT, "concept", "C")
        x["draft"]["passages"][0]["verbatim"] += " FORGED"
        with self.assertRaisesRegex(ValueError, "faithful"):
            begin(x, DRAFT)

    def test_p104_init_refuses_resetting_approvals(self):
        with self.assertRaisesRegex(ValueError, "already exists"):
            begin(self.case, DRAFT)

    def test_p105_proposal_cannot_be_automatically_approved(self):
        self.assertEqual(inspect(self.one, DRAFT)["gate"], "RESEARCHER_REVIEW_REQUIRED")
        self.assertEqual(inspect(self.one, DRAFT)["counts"]["confirmed"], 0)

    def test_p106_exact_quote_span_verified(self):
        self.assertTrue(inspect(self.one, DRAFT)["records"][0]["quote_verified_against_original"])

    def test_p107_propose_bad_span_rejected(self):
        with self.assertRaisesRegex(ValueError, "match"):
            add_record(self.case, start=0)

    def test_p108_propose_outside_span_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            add_record(self.case, start=999)

    def test_p109_repeated_quotes_require_exact_offsets(self):
        text = "Hak dan hak dapat dibedakan.\n\nHak."
        x = make_case(text)
        a = x["draft"]["passages"][0]["verbatim"].index("hak")
        record = {
            "id": "P1", "passage_id": "T0001",
            "span": {"start": a, "end": a+3, "quote": "hak"},
            "voice": "uncertain", "mode": "paraphrase",
            "proposition": "Dua pemakaian hak", "voice_basis": "Ambiguitas dalam kalimat",
            "context_passage_ids": ["T0001"], "premise_ids": [],
        }
        x = propose(x, record)
        self.assertTrue(inspect(x, text)["records"][0]["quote_verified_against_original"])

    def test_p110_independent_original_required(self):
        self.assertIn("ORIGINAL_DRAFT_UNAVAILABLE", self.codes(self.one, None))
        self.assertEqual(inspect(self.one, None)["gate"], "BLOCKED_SOURCE_OR_APPROVAL")

    def test_p111_changed_file_detected(self):
        self.assertIn("DRAFT_HASH_MISMATCH", self.codes(self.one, DRAFT + "\nModified"))

    def test_p112_mutated_case_passage_detected(self):
        x = copy.deepcopy(self.one)
        x["draft"]["passages"][0]["verbatim"] += " FORGED"
        self.assertIn("PASSAGE_NOT_IN_ORIGINAL", self.codes(x))

    def test_p113_bad_line_number_detected(self):
        x = copy.deepcopy(self.one)
        x["draft"]["passages"][0]["start_line"] = 44
        self.assertIn("PASSAGE_NOT_IN_ORIGINAL", self.codes(x))

    def test_p114_context_referent_must_exist(self):
        x = copy.deepcopy(self.one)
        x["reconstruction"]["records"][0]["context_passage_ids"] = ["T0012"]
        self.assertIn("CONTEXT_PASSAGE_NOT_FOUND", self.codes(x))

    def test_p115_voice_cannot_be_unexplained(self):
        x = copy.deepcopy(self.one)
        x["reconstruction"]["records"][0]["voice_basis"] = ""
        self.assertIn("VOICE_UNVERIFIED", self.codes(x))

    def test_p116_inferred_author_premise_not_explicit(self):
        x = add_record(self.case, mode="inferred")
        self.assertIn("PROPOSITION_NOT_AUTHOR_EXPLICIT", self.codes(x))

    def test_p117_opponent_speech_not_author_commitment(self):
        x = add_record(self.case, passage="T0002",
                       quote="semua tindakan negara selalu sah",
                       voice="opponent")
        self.assertIn("EXTERNAL_POSITION_UNADOPTED", self.codes(x))

    def test_p118_uncertain_speaker_flagged(self):
        x = add_record(self.case, voice="uncertain")
        self.assertIn("PASSAGE_CONTEXT_UNCERTAIN", self.codes(x))

    def test_p119_duplicate_record_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            add_record(self.one)

    def test_p120_duplicate_id_after_approval_rejected(self):
        with self.assertRaises(ValueError):
            add_record(decided(self.one))

    def test_p121_real_review_confirmation_synthetically_recorded(self):
        x = decided(self.one)
        result = inspect(x, DRAFT)
        self.assertEqual(result["gate"], "SELF_ATTESTED_FIDELITY_ONLY")
        self.assertEqual(result["counts"]["confirmed"], 1)
        self.assertTrue(result["records"][0]["self_attested_not_identity_verified"])

    def test_p122_confirmation_phrase_must_match_current_fingerprint(self):
        with self.assertRaisesRegex(ValueError, "confirmation"):
            add_decision(self.one, DRAFT, "P1", "Reviewer", "accept", "read", "CONFIRM P1 fake")

    def test_p123_reviewer_label_required(self):
        with self.assertRaisesRegex(ValueError, "required"):
            add_decision(self.one, DRAFT, "P1", "", "accept", "reason",
                         approval_challenge(self.one, "P1"))

    def test_p124_reason_required(self):
        with self.assertRaisesRegex(ValueError, "required"):
            add_decision(self.one, DRAFT, "P1", "Reviewer", "accept", "",
                         approval_challenge(self.one, "P1"))

    def test_p125_reject_decision_is_not_approval(self):
        x = decided(self.one, decision="reject")
        self.assertEqual(inspect(x, DRAFT)["records"][0]["status"], "RESEARCHER_REJECTED")
        self.assertEqual(inspect(x, DRAFT)["counts"]["confirmed"], 0)

    def test_p126_revision_decision_is_not_approval(self):
        x = decided(self.one, decision="revise")
        self.assertEqual(inspect(x, DRAFT)["records"][0]["status"], "REVISION_REQUESTED")

    def test_p127_record_rewording_stales_previous_approval(self):
        x = decided(self.one)
        x["reconstruction"]["records"][0]["proposition"] += " Tambahan."
        result = inspect(x, DRAFT)
        self.assertIn("APPROVAL_STALE", {i["code"] for i in result["findings"]})
        self.assertEqual(result["counts"]["stale"], 1)

    def test_p128_revision_sync_invalidates_approval(self):
        x = decided(self.one)
        edited = DRAFT.replace("memerlukan pembatasan", "perlu mempertimbangkan batas")
        x = version_sync(x, edited)
        result = inspect(x, edited)
        self.assertIn("APPROVAL_STALE", {i["code"] for i in result["findings"]})
        self.assertFalse(x["readiness"]["researcher_approved"])
        self.assertEqual(x["readiness"]["integration_review"], "re_review_required")

    def test_p129_dependent_premise_change_reopens_conclusion(self):
        x = add_record(self.one, rid="C1", passage="T0003",
                       quote="keputusan dapat diperdebatkan",
                       premises=["P1"])
        x = decided(x, "P1")
        x = decided(x, "C1")
        self.assertEqual(inspect(x, DRAFT)["counts"]["confirmed"], 2)
        x["reconstruction"]["records"][0]["proposition"] += " Revisi premis"
        result = inspect(x, DRAFT)
        self.assertIn("APPROVAL_STALE", self.codes(x))
        self.assertEqual(result["counts"]["confirmed"], 0)

    def test_p130_author_approval_is_not_copyable_from_json(self):
        x = copy.deepcopy(self.one)
        x["reconstruction"]["decisions"].append({
            "claim_id": "P1", "decision": "accept", "fingerprint": "x"*64,
            "draft_sha256": x["draft"]["sha256"],
            "attestation": "interactive_self_attested", "reviewer_label": "Fake"})
        self.assertEqual(inspect(x, DRAFT)["gate"], "BLOCKED_SOURCE_OR_APPROVAL")

    def test_p131_existing_graph_claim_requires_fidelity_record(self):
        x = self.one
        x["claims"] = [{
            "id": "Z999", "text": "A claim the author never made", "attribution": "author",
            "provenance": "researcher_approved", "passage_id": "T0001",
        }]
        self.assertIn("GRAPH_CLAIM_NOT_RECONSTRUCTED", self.codes(x))

    def test_p132_existing_graph_cannot_change_reconstructed_meaning(self):
        x = decided(self.one)
        x["claims"] = [{
            "id": "P1", "text": "Berbeda secara substansial", "attribution": "author",
            "provenance": "researcher_approved", "passage_id": "T0001",
        }]
        self.assertIn("GRAPH_PROPOSITION_DRIFT", self.codes(x))

    def test_p133_opponent_cannot_be_laundered_through_graph(self):
        x = add_record(self.case, passage="T0002", quote="semua tindakan negara selalu sah",
                       voice="opponent")
        x = decided(x)
        x["claims"] = [{
            "id": "P1", "text": x["reconstruction"]["records"][0]["proposition"],
            "attribution": "author", "provenance": "researcher_approved",
            "passage_id": "T0002",
        }]
        self.assertIn("GRAPH_SPEAKER_LAUNDERING", self.codes(x))

    def test_p134_inference_not_laundered_as_explicit_quote(self):
        x = add_record(self.case, mode="inferred")
        x = decided(x)
        x["claims"] = [{
            "id": "P1", "text": x["reconstruction"]["records"][0]["proposition"],
            "attribution": "author", "provenance": "author_explicit", "passage_id": "T0001",
        }]
        self.assertIn("GRAPH_EXPLICITNESS_LAUNDERING", self.codes(x))

    def test_p135_unapproved_claim_cannot_be_graph_approved(self):
        x = copy.deepcopy(self.one)
        x["claims"] = [{
            "id": "P1", "text": x["reconstruction"]["records"][0]["proposition"],
            "attribution": "author", "provenance": "researcher_approved", "passage_id": "T0001",
        }]
        self.assertIn("GRAPH_APPROVAL_UNSUPPORTED", self.codes(x))

    def test_p136_reapproval_after_revision_is_possible(self):
        x = decided(self.one)
        x["reconstruction"]["records"][0]["proposition"] += " Reworded."
        challenge = approval_challenge(x, "P1")
        x = add_decision(x, DRAFT, "P1", "Researcher", "accept", "I accept revised version", challenge)
        self.assertEqual(inspect(x, DRAFT)["gate"], "SELF_ATTESTED_FIDELITY_ONLY")

    def test_p137_identity_not_authenticated_and_novelty_locked(self):
        x = decided(self.one)
        r = inspect(x, DRAFT)
        self.assertIn("NOT independently authenticated", r["disclaimer"])
        self.assertEqual(r["originality"], "LOCKED")

    def test_p138_reports_code_and_quote_integrity(self):
        self.assertIn("author", render_report(self.one, DRAFT))
        self.assertIn("PROPOSED", render_report(self.one, DRAFT))

    def test_p139_noninteractive_cli_cannot_approve(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"case.json"
            draft = Path(folder)/"draft.txt"
            path.write_text(json.dumps(self.one, ensure_ascii=False), encoding="utf-8")
            draft.write_text(DRAFT, encoding="utf-8")
            p = subprocess.run(
                [sys.executable, str(ROOT/"scripts"/"fidelity_cli.py"), "decide",
                 "--case", str(path), "--draft", str(draft), "--id", "P1",
                 "--reviewer", "AI impersonation", "--decision", "accept",
                 "--reason", "silently approval", "--out", str(Path(folder)/"out.json")],
                input=approval_challenge(self.one, "P1"), text=True,
                capture_output=True)
            self.assertEqual(p.returncode, 2)
            self.assertIn("Refusing non-interactive approval", p.stderr)

    def test_p140_cli_start_propose_and_check(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            original = folder/"source.txt"
            original.write_text(DRAFT, encoding="utf-8")
            prior = folder/"case.json"
            prior.write_text(json.dumps(new_case(DRAFT, "concept", "Kepentingan umum",
                                                locus="contoh sintetis"), ensure_ascii=False), encoding="utf-8")
            staged = folder/"staged.json"
            proposed = folder/"proposed.json"
            report = folder/"fidelity-report.json"
            cli = [sys.executable, str(ROOT/"scripts"/"fidelity_cli.py")]
            p = subprocess.run(cli+["start", "--case", str(prior), "--draft", str(original),
                                    "--out", str(staged)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            quote = "kepentingan umum"
            start = DRAFT.index(quote)
            p = subprocess.run(cli+["propose", "--case", str(staged), "--id", "P1",
                       "--passage", "T0001", "--span-start", str(start),
                       "--span-end", str(start+len(quote)), "--quote", quote,
                       "--voice", "author", "--mode", "explicit",
                       "--proposition", "Konsep kepentingan umum perlu diuji",
                       "--voice-basis", "Penulis pada paragraf ini", "--context", "T0001",
                       "--out", str(proposed)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            p = subprocess.run(cli+["check", "--case", str(proposed), "--draft",
                       str(original), "--out", str(report)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(result["gate"], "RESEARCHER_REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
