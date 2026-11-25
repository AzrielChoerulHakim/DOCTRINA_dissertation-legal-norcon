"""P1 exact-byte and CRLF reproducibility tests."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from doctrina_core import split_passages
from doctrina_fidelity import begin, inspect

class ByteFidelity(unittest.TestCase):
    def test_b01_crlf_passage_boundaries_preserved(self):
        source = "Premis α.\r\n\r\nKesimpulan β."
        parts = split_passages(source)
        self.assertEqual(len(parts), 2)
        for x in parts:
            self.assertEqual(source[x["start_offset"]:x["end_offset"]], x["verbatim"])
        self.assertEqual(parts[1]["start_line"], 3)

    def test_b02_sha_over_exact_source_bytes_not_newline_normalization(self):
        original = "Norma berlaku.\r\n\r\nKondisi berbeda.\r\n"
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            inp = folder/"draft.txt"
            casefile = folder/"case.json"
            inp.write_bytes(original.encode("utf-8"))
            run = subprocess.run(
                [sys.executable, str(ROOT/"scripts"/"doctrina_cli.py"), "init",
                 "--input", str(inp), "--object", "norm", "--title", "Norma hipotetis",
                 "--locus", "contoh", "--out", str(casefile)],
                capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            case = json.loads(casefile.read_text(encoding="utf-8"))
            self.assertEqual(case["draft"]["sha256"], hashlib.sha256(inp.read_bytes()).hexdigest())
            self.assertEqual(len(case["draft"]["passages"]), 2)
            reviewed = begin(case, inp.read_bytes().decode("utf-8"))
            self.assertNotIn("DRAFT_HASH_MISMATCH",
                             {x["code"] for x in inspect(reviewed, inp.read_bytes().decode("utf-8"))["findings"]})

    def test_b03_newline_normalization_is_detected(self):
        original = "A.\r\n\r\nB."
        from doctrina_core import new_case
        x = begin(new_case(original, "concept", "C"), original)
        normalized = original.replace("\r\n", "\n")
        self.assertIn("DRAFT_HASH_MISMATCH",
                      {i["code"] for i in inspect(x, normalized)["findings"]})

    def test_b04_unicode_codepoint_spans_preserve_combining_marks(self):
        text = "Rumusan e\u0301 tidak sama dengan é.\n\nMakna hukum."
        from doctrina_core import new_case
        x = begin(new_case(text, "concept", "C"), text)
        parts = x["draft"]["passages"]
        self.assertEqual(len(parts), 2)
        self.assertEqual(text[parts[0]["start_offset"]:parts[0]["end_offset"]], parts[0]["verbatim"])
        self.assertNotEqual("e\u0301", "é")


if __name__ == "__main__":
    unittest.main()
