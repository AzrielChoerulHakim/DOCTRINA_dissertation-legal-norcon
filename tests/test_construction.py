"""Synthetic negative controls; no empirical validation of legal reasoning."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_construction import audit, impacted
from doctrina_core import new_case, validate

def ledger():
    def node(i, kind, parent=None, deps=None):
        return {"id":i,"kind":kind,"statement":"Synthetic "+i,
                "parents":[{"id":parent,"relation":"supports"}] if parent else [],
                "depends_on":deps or [],"status":"supported"}
    return {"object":{"type":"judgment","locus":"synthetic case","jurisdiction":"hypothetical","timeframe":"hypothetical"},
            "question":"Synthetic question","novelty_direction":"interpretative",
            "method":{"route":"symbolic","warrant":"synthetic warrant"},
            "nodes":[node("I","idea"),node("A","core","I",["C"]),node("SA","subargument","A",["D"]),
                     node("D","development","SA"),node("C","intermediate","SA",["SA"]),node("S","synthesis","A",["A"])],
            "searches":[{"id":"R1","target":"D","question":"which text?","expected_evidence":"original judgment","stop_criterion":"relevant reasons inspected or unavailable"}]}

class ConstructionTests(unittest.TestCase):
    def codes(self, x):
        return {v["code"] for v in audit(x)}
    def test_valid_synthetic(self):
        self.assertEqual(audit(ledger()), [])
    def test_judgment_core_intake(self):
        x = new_case("Synthetic", "judgment", "Synthetic judgment")
        codes = {v["code"] for v in validate(x)}
        self.assertNotIn("OBJECT_OUT_OF_SCOPE", codes)
        self.assertIn("JUDGMENT_SOURCE_MISSING", codes)
    def test_theory_rejected(self):
        x=ledger(); x["object"]["type"]="theory"
        self.assertIn("OBJECT_INVALID", self.codes(x))
    def test_orphan(self):
        x=ledger(); x["nodes"][3]["parents"]=[]
        self.assertIn("UNLINKED_TO_CORE", self.codes(x))
    def test_cycle(self):
        x=ledger(); x["nodes"][3]["depends_on"]=["A"]
        self.assertIn("CYCLE", self.codes(x))
    def test_unbounded_search(self):
        x=ledger(); x["searches"][0]["stop_criterion"]=""
        self.assertIn("SEARCH_UNBOUNDED", self.codes(x))
    def test_unlinked_search(self):
        x=ledger(); x["searches"][0]["target"]="not a node"
        self.assertIn("SEARCH_UNLINKED", self.codes(x))
    def test_combination_handoff(self):
        x=ledger(); x["method"]["route"]="combined"
        self.assertIn("METHOD_HANDOFF_MISSING", self.codes(x))
    def test_rejected_premise(self):
        x=ledger(); x["nodes"][3]["status"]="rejected"
        self.assertIn("STALE_DEPENDENT", self.codes(x))
        self.assertEqual(impacted(x, ["D"]), ["A","C","S","SA"])
    def test_malformed_node_dependency(self):
        x=ledger(); x["nodes"][3]["depends_on"]=[{}]
        self.assertIn("DEPENDENCY_INVALID", self.codes(x))
    def test_conclusion_needs_dependency(self):
        x=ledger(); x["nodes"][4]["depends_on"]=[]
        self.assertIn("CONCLUSION_WITHOUT_DEPENDENCIES", self.codes(x))

if __name__ == "__main__":
    unittest.main()
