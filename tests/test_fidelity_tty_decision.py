"""P1 local interactive decision flow tests; synthetic reviewer only, no real signature."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from fidelity_cli import main
from doctrina_fidelity import approval_challenge, inspect
from test_fidelity_p1 import add_record, make_case, DRAFT


class InteractiveDecisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.case = add_record(make_case())
        self.case_file = self.folder/"case.json"
        self.draft_file = self.folder/"draft.txt"
        self.output = self.folder/"reviewed.json"
        self.case_file.write_text(json.dumps(self.case, ensure_ascii=False), encoding="utf-8")
        self.draft_file.write_bytes(DRAFT.encode("utf-8"))
        self.args = ["decide", "--case", str(self.case_file),
                     "--draft", str(self.draft_file), "--id", "P1",
                     "--reviewer", "Synthetic reviewer (test only)",
                     "--decision", "accept", "--reason", "Reviewed source context",
                     "--out", str(self.output)]

    def test_i01_local_terminal_with_exact_token_records_synthetic_decision(self):
        with (patch.object(sys.stdin, "isatty", return_value=True),
              patch.object(sys.stdout, "isatty", return_value=True),
              patch("builtins.input", return_value=approval_challenge(self.case, "P1"))):
            self.assertEqual(main(self.args), 0)
        data = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(inspect(data, DRAFT)["gate"], "SELF_ATTESTED_FIDELITY_ONLY")
        self.assertEqual(data["reconstruction"]["decisions"][0]["attestation"],
                         "interactive_self_attested")

    def test_i02_wrong_confirmation_token_refuses_approval(self):
        with (patch.object(sys.stdin, "isatty", return_value=True),
              patch.object(sys.stdout, "isatty", return_value=True),
              patch("builtins.input", return_value="CONFIRM P1 WRONG")):
            self.assertEqual(main(self.args), 2)
        self.assertFalse(self.output.exists())

    def test_i03_programmatic_noninteractive_mode_refuses_even_correct_token(self):
        with (patch.object(sys.stdin, "isatty", return_value=False),
              patch.object(sys.stdout, "isatty", return_value=False),
              patch("builtins.input", return_value=approval_challenge(self.case, "P1"))):
            self.assertEqual(main(self.args), 2)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
