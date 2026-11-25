"""v0.4.1 source integrity tests. Synthetic originals; NOT jurisprudential tests."""
from __future__ import annotations
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_sources import verify_source, verify_manifest, normalize

PDF_ANCHOR = "Legal rules need defensible interpretation"
CONCEPT_ANCHOR = "A legal concept has boundaries"


class SourceGroundingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        from reportlab.pdfgen import canvas
        path = self.root / "doctoral_original.pdf"
        draw = canvas.Canvas(str(path), pagesize=(612, 792))
        draw.drawString(72, 730, "This is an illustrative doctoral passage.")
        draw.drawString(72, 711, PDF_ANCHOR)
        draw.showPage()
        draw.drawString(72, 730, CONCEPT_ANCHOR)
        draw.showPage()
        draw.save()
        self.pdf = path
        self.hash = hashlib.sha256(path.read_bytes()).hexdigest()

    def pdf_record(self):
        return {
            "source_id": "DOC_SYN",
            "source_kind": "thesis_pdf",
            "repository_url": "https://example.org/original-record",
            "download_url": "https://example.org/original.pdf",
            "local_path": self.pdf.name,
            "content_sha256": self.hash,
            "retrieved_at": "2026-11-25",
            "edition": "illustrative PDF v1",
            "publication_year": 2026,
            "extraction_method": "pypdf",
            "page_index": 0,
            "printed_page": "1",
            "anchor_text": PDF_ANCHOR,
        }

    def test_01_original_pdf_exact_match(self):
        x = verify_source(self.pdf_record(), self.root)
        self.assertEqual(x["state"], "VERIFIED_EXACT")
        self.assertEqual(x["page_index_verified"], 0)
        self.assertIsInstance(x["match_offset"], int)

    def test_02_pdf_wrong_page_never_verified(self):
        x = self.pdf_record()
        x["page_index"] = 1
        report = verify_source(x, self.root)
        self.assertEqual(report["state"], "UNVERIFIED")
        self.assertEqual(report["evidence"][0]["code"], "ANCHOR_OFF_PAGE")
        self.assertEqual(report["discovered_page_indices"], [0])

    def test_03_changed_original_bytes_fail_hash(self):
        x = self.pdf_record()
        x["content_sha256"] = "a" * 64
        y = verify_source(x, self.root)
        self.assertEqual(y["state"], "UNVERIFIED")
        self.assertEqual(y["evidence"][0]["code"], "HASH_MISMATCH")

    def test_04_missing_pinned_hash_is_only_partial(self):
        x = self.pdf_record()
        x.pop("content_sha256")
        self.assertEqual(verify_source(x, self.root)["state"], "PARTIAL")

    def test_05_page_discovery_is_not_inspection(self):
        x = self.pdf_record()
        x["page_index"] = None
        y = verify_source(x, self.root)
        self.assertEqual(y["state"], "PARTIAL")
        self.assertEqual(y["discovered_page_indices"], [0])

    def test_06_missing_source_is_unverified(self):
        x = self.pdf_record()
        x["local_path"] = "absent.pdf"
        self.assertEqual(verify_source(x, self.root)["state"], "UNVERIFIED")

    def test_07_path_escape_is_blocked(self):
        x = self.pdf_record()
        x["local_path"] = "../unrelated-secret.txt"
        y = verify_source(x, self.root)
        self.assertEqual(y["evidence"][0]["code"], "UNSAFE_PATH")

    def test_08_second_pdf_page_exactly_verifiable(self):
        x = self.pdf_record()
        x["page_index"] = 1
        x["anchor_text"] = CONCEPT_ANCHOR
        y = verify_source(x, self.root)
        self.assertEqual(y["state"], "VERIFIED_EXACT")
        self.assertEqual(y["page_index_verified"], 1)

    def test_09_pdf_text_only_ocr_needed(self):
        from reportlab.pdfgen import canvas
        path = self.root / "image_only.pdf"
        draw = canvas.Canvas(str(path))
        draw.rect(50, 50, 100, 100, fill=0)
        draw.save()
        x = self.pdf_record()
        x["local_path"] = "image_only.pdf"
        x["content_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        y = verify_source(x, self.root)
        self.assertEqual(y["state"], "PARTIAL")
        self.assertEqual(y["evidence"][0]["code"], "NO_EXTRACTABLE_TEXT")

    def test_10_normalized_whitespace_is_distinguished(self):
        x = self.pdf_record()
        x["anchor_text"] = "This is an illustrative doctoral passage. Legal rules need defensible interpretation"
        y = verify_source(x, self.root)
        self.assertEqual(y["state"], "VERIFIED_NORMALIZED")
        self.assertIn("normalization", " ".join(y["limitations"]).lower())

    def test_11_normalized_quote_cannot_change_meaning(self):
        self.assertEqual(normalize("A  B\nC"), "A B C")
        self.assertNotEqual(normalize("Rule is valid"), normalize("Rule is invalid"))
        self.assertNotEqual(normalize("Right"), normalize("right"))

    def test_12_utf8_source_can_be_verified_with_hash(self):
        original = self.root / "source.txt"
        original.write_text("Criterion X is required.", encoding="utf-8")
        x = {"source_id": "LAW_1", "source_kind": "text_utf8", "local_path": "source.txt",
             "content_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
             "anchor_text": "Criterion X is required.", "page_index": 0,
             "extraction_method": "utf8_text", "repository_url": "https://example.org"}
        y = verify_source(x, self.root)
        self.assertEqual(y["state"], "VERIFIED_EXACT")

    def test_13_misdeclared_pdf_extraction_is_rejected(self):
        x = self.pdf_record()
        x["extraction_method"] = "utf8_text"
        y = verify_source(x, self.root)
        self.assertEqual(y["evidence"][0]["code"], "EXTRACTION_METHOD_MISMATCH")

    def test_14_invalid_pdf_header_fails(self):
        p = self.root / "fake.pdf"
        p.write_bytes(b"fake document")
        x = self.pdf_record()
        x["local_path"] = "fake.pdf"
        x["content_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(verify_source(x, self.root)["state"], "UNVERIFIED")

    def test_15_manifest_counts_and_duplicate_ids(self):
        x, y = self.pdf_record(), self.pdf_record()
        r = verify_manifest({"sources": [x, y]}, self.root)
        self.assertEqual(r["counts"]["VERIFIED_EXACT"], 1)
        self.assertEqual(r["counts"]["UNVERIFIED"], 1)
        self.assertEqual(r["results"][1]["evidence"][-1]["code"], "DUPLICATE_SOURCE_ID")

    def test_16_legal_date_does_not_prove_validity(self):
        x = self.pdf_record()
        x["source_kind"] = "legal_pdf"
        x["applicability_date"] = "2026-11-25"
        report = verify_source(x, self.root)
        self.assertEqual(report["state"], "VERIFIED_EXACT")
        self.assertIn("not proof", " ".join(report["limitations"]).lower())

    def test_17_source_year_not_claimed_verified(self):
        x = self.pdf_record()
        report = verify_source(x, self.root)
        self.assertTrue(any("publication year" in note.lower() for note in report["limitations"]))

    def test_18_missing_anchor_unverified(self):
        x = self.pdf_record()
        x["anchor_text"] = "A completely different scientific proposition"
        y = verify_source(x, self.root)
        self.assertEqual(y["state"], "UNVERIFIED")
        self.assertEqual(y["evidence"][0]["code"], "ANCHOR_NOT_FOUND")

    def test_19_no_source_file_bytes_leak_in_result(self):
        y = verify_source(self.pdf_record(), self.root)
        output = json.dumps(y)
        self.assertNotIn("This is an illustrative doctoral passage.", output)
        self.assertNotIn(str(self.root), output)

    def test_20_manifest_rejects_nonlist(self):
        with self.assertRaises(ValueError):
            verify_manifest({"sources": {}}, self.root)


if __name__ == "__main__":
    unittest.main()
