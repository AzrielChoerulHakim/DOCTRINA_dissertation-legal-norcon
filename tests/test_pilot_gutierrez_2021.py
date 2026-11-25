"""PILOT-002: bounded evaluation on a *published* PhD thesis, NOT doctoral grading.

Original source: Arantxa Telenia Gutierrez Raymondova, Taxonomy of Non-Pecuniary
Losses in English Tort Law (University of Edinburgh PhD, 2021), ch 2 pp 73-75,
ch 4 p 154: https://hdl.handle.net/1842/37829

Only four short, non-consecutive source phrases are used (24 words total).
This is NOT the complete dissertation or full source paragraphs; annotations
below are AI-proposed paraphrases, not author- or researcher-approved.

Counter-reading checked: MGN v Gulati [2015] EWCA Civ 1291 [45]-[48],
[95]-[103]: https://www.judiciary.uk/wp-content/uploads/2015/12/representative-claimants-v-mgn.pdf

The CI tests prove mechanical behaviour on a real-text *sample* only.
They do NOT adjudicate whether the thesis is internally invalid.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from doctrina_core import new_case, review, validate, markdown_report

# Total = 24 words from the thesis; no copyrighted whole paragraphs.
ANCHORS = [
    "the infringement of a protected interest",
    "the wrong and the losses that follow it",
    "distress can only be a consequence",
    "It is clearly illogical",
]


def build_pilot_case():
    case = new_case(
        "\n\n".join(ANCHORS),
        "concept",
        "The legal concept of non-pecuniary loss: normative versus consequential",
        locus="Gutierrez Raymondova (2021), ch 2 pp 73-75 and ch 4 p 154",
        jurisdiction="England and Wales; French-law comparison",
        temporal_scope="thesis published July 2021",
        source_filename="published-selected-short-excerpts.txt",
    )
    case["research_object"]["concept_usages"] = [{
        "usage": "non-pecuniary loss: normative and consequential structures",
        "locator": "Ch 2 printed pp 73-75; Ch 4 printed p 154",
        "inspection_status": "partial",
    }]
    case["sources"] = [
        {"id": "S_THESIS",
         "title": "Gutierrez Raymondova, Taxonomy of non-pecuniary losses (2021)",
         "url": "https://hdl.handle.net/1842/37829",
         "inspection_status": "partial"},
        {"id": "S_GULATI", "title": "MGN v Gulati [2015] EWCA Civ 1291",
         "url": "https://www.judiciary.uk/wp-content/uploads/2015/12/representative-claimants-v-mgn.pdf",
         "locator": "[45]-[48], [95]-[103]",
         "inspection_status": "partial"},
    ]
    common = {"attribution": "proposed", "provenance": "ai_proposed",
              "quotes": [], "support": [{"source_id": "S_THESIS", "state": "partial"}]}
    case["claims"] = [
        {**common, "id": "P1", "kind": "conceptual", "role": "premise",
         "passage_id": "T0001", "anchor_text": ANCHORS[0], "chapter_id": "CH2",
         "text": "In a normative/unipolar structure, invasion of the protected interest itself counts as an abstract loss; proof of consequential injury is not necessary for the structural account.",
         "premises": []},
        {**common, "id": "P2", "kind": "conceptual", "role": "premise",
         "passage_id": "T0002", "anchor_text": ANCHORS[1], "chapter_id": "CH2",
         "text": "In the consequential/bipolar structure, the original wrong is distinguished from the concrete consequences that flow from it.",
         "premises": []},
        {**common, "id": "P3", "kind": "conceptual", "role": "premise",
         "passage_id": "T0003", "anchor_text": ANCHORS[2], "chapter_id": "CH4",
         "text": "Emotional distress arising from misuse of private information is a consequence of the infringement, not the same conceptual level as the loss of control.",
         "premises": []},
        {**common, "id": "C1", "kind": "normative", "role": "derived",
         "passage_id": "T0004", "anchor_text": ANCHORS[3], "chapter_id": "CH4",
         "text": "Treating compensation for lost informational control and emotional distress as if they were independent and coequal heads is conceptually objectionable; the author favors coherent differentiation rather than treating them as symmetrical.",
         "premises": ["P1", "P2", "P3"], "inference": "conceptual-to-normative",
         "warrant": {
             "text": "Because distress is downstream of the violation, it is said to be unsound to present its compensation at the same conceptual level as compensation for the wrong itself.",
             "status": "ai_proposed",
             "normative_bridge": False,
         }},
    ]
    case["central_claim_id"] = "C1"
    case["chapters"] = [
        {"id": "CH2", "title": "Normative and consequential loss concepts",
         "claim_ids": ["P1", "P2"],
         "argumentative_task": "Define two distinct conceptual structures of loss"},
        {"id": "CH4", "title": "Application to privacy infringement",
         "claim_ids": ["P3", "C1"],
         "argumentative_task": "Apply distinctions and criticize asymmetric English classification"},
    ]
    case["objections"] = [{
        "id": "O1", "target_id": "C1", "status": "open", "severity": "major",
        "text": "A cause and its separate consequence can both receive compensation without conceptual identity or double recovery, provided damages are separated and overlapping quantum avoided.",
        "evidence_source_id": "S_GULATI", "evidence_locator": "[45]-[48], [95]-[103]",
        "researcher_reply": "NOT CONFIRMED",
    }]
    return case


class PublishedDissertationPilot(unittest.TestCase):
    def test_pilot_01_scope_and_source_anchors(self):
        case = build_pilot_case()
        codes = {f["code"] for f in validate(case)}
        self.assertEqual(case["research_object"]["primary_type"], "concept")
        self.assertFalse({"OBJECT_OUT_OF_SCOPE", "CLAIM_UNANCHORED",
                          "QUOTE_NOT_IN_PASSAGE", "AI_PROPOSED_AS_AUTHOR"} & codes)
        self.assertEqual(len(case["draft"]["passages"]), 4)

    def test_pilot_02_inference_warning_is_not_semantic_verdict(self):
        report = review(build_pilot_case())
        codes = {f["code"] for f in report["findings"]}
        self.assertIn("IA-06", codes)
        self.assertIn("OPEN_SERIOUS_OBJECTION", codes)
        self.assertIn("NOT validation of legal meaning", report["disclaimer"])
        self.assertEqual(report["gate"], "INTERNAL_REVISION_REQUIRED")

    def test_pilot_03_author_approval_and_novelty_remain_absent(self):
        case = build_pilot_case()
        self.assertTrue(all(x["provenance"] == "ai_proposed" for x in case["claims"]))
        self.assertFalse(case["readiness"]["researcher_approved"])
        self.assertEqual(case["originality"]["stage"], "locked")
        self.assertEqual(case["originality"]["final_status"], "NOT_READY")

    def test_pilot_04_report_names_provisional_inference(self):
        report = markdown_report(build_pilot_case())
        self.assertIn("Ch 4 p 154", report)
        self.assertIn("AI_PROPOSED" if "AI_PROPOSED" in report else "ai_proposed", report)
        self.assertIn("IA-06", report)
        self.assertIn("LOCKED", report)


if __name__ == "__main__":
    unittest.main()
