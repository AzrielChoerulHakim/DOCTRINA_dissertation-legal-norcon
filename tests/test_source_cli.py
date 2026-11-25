"""Integrated v0.4.1 CLI source check — local UTF-8 fixture, no network."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "doctrina_cli.py"


class SourceCLITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / "original-law.txt"
        source.write_text("The illustrative clause grants a legal power.", encoding="utf-8")
        self.payload = {
            "sources": [{
                "source_id": "LAW_DEMO",
                "source_kind": "text_utf8",
                "repository_url": "https://example.org/legal-record",
                "local_path": "original-law.txt",
                "content_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "extraction_method": "utf8_text",
                "page_index": 0,
                "anchor_text": "illustrative clause grants a legal power",
            }]
        }
        self.manifest = self.root / "manifest.json"
        self.manifest.write_text(json.dumps(self.payload), encoding="utf-8")

    def run_cli(self):
        out = self.root / "source-report.json"
        p = subprocess.run(
            [sys.executable, str(CLI), "verify-sources",
             "--manifest", str(self.manifest),
             "--source-root", str(self.root),
             "--out", str(out)],
            capture_output=True, text=True)
        return p, json.loads(out.read_text(encoding="utf-8"))

    def test_cli_01_exact_source_success(self):
        process, r = self.run_cli()
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(r["counts"]["VERIFIED_EXACT"], 1)

    def test_cli_02_unverified_original_exits_nonzero(self):
        self.payload["sources"][0]["content_sha256"] = "e" * 64
        self.manifest.write_text(json.dumps(self.payload), encoding="utf-8")
        process, r = self.run_cli()
        self.assertEqual(process.returncode, 2)
        self.assertEqual(r["results"][0]["evidence"][0]["code"], "HASH_MISMATCH")


if __name__ == "__main__":
    unittest.main()
