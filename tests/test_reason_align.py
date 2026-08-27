from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from h11_runtime.agi import H11AGI
from h11_runtime.loader import load_module


class UniqueKernelTests(unittest.TestCase):
    def test_auction_is_vickrey_not_a_counter(self):
        mod = load_module("H11-AUCTION", "L16_multiagent_society/h11_auction/agent.py")
        out = mod.AUCTIONAgent().process(
            {"bids": [{"bidder": "a", "amount": 10}, {"bidder": "b", "amount": 7}]}
        )
        self.assertEqual(out["winner"], "a")
        self.assertEqual(out["price"], 7)
        self.assertEqual(out["mechanism"], "vickrey")

    def test_dermatologia_abcde_refers_when_evolving(self):
        mod = load_module(
            "H11-DERMATOLOGIA",
            "H11I_INTELLIGENCE_UNIVERSE/D01_medicine_health/H11-DERMATOLOGIA/agent.py",
        )
        out = mod.DERMATOLOGIAAgent().process({"asymmetry": 1, "evolving": 1, "diameter_mm": 8})
        self.assertGreaterEqual(out["abcde"], 2.0)
        self.assertTrue(out["refer"])


class ReasonKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        mod = load_module("H11-REASON", "L13_cognition_reasoning/H11-REASON/agent.py")
        self.agent = mod.H11ReasonAgent("TEST")

    def _run(self, problem: str, premises: list) -> dict:
        return json.loads(
            self.agent.process(
                json.dumps(
                    {
                        "problem_statement": problem,
                        "premises": premises,
                        "reasoning_mode": "deduction",
                    }
                )
            )
        )

    def test_modus_ponens_socrates(self):
        out = self._run("Is Socrates mortal?", ["All men are mortal.", "Socrates is a man."])
        self.assertIn("Socrates is mortal", out["conclusion"])
        self.assertEqual(out["action"], "ANSWER")
        self.assertTrue(out["quality_assessment"]["is_sound"])

    def test_treat_when_protocol_and_vitals_hold(self):
        out = self._run(
            "Should the host case proceed with Artemether-Lumefantrine given current vitals?",
            [
                "Identified parasite is Plasmodium falciparum.",
                "Recommended antiparasitic is Artemether-Lumefantrine.",
                "Diagnostic confidence is 0.96.",
                "Mean arterial pressure is 81.0 mmHg.",
            ],
        )
        self.assertTrue(out["conclusion"].startswith("TREAT"))
        self.assertIn("Plasmodium falciparum", out["conclusion"])
        self.assertEqual(out["action"], "TREAT")

    def test_withhold_critical_hypotension(self):
        out = self._run(
            "Should the host case proceed with Artemether-Lumefantrine given current vitals?",
            [
                "Identified parasite is Plasmodium falciparum.",
                "Recommended antiparasitic is Artemether-Lumefantrine.",
                "Diagnostic confidence is 0.96.",
                "Mean arterial pressure is 38.0 mmHg.",
            ],
        )
        self.assertTrue(out["conclusion"].startswith("WITHHOLD"))
        self.assertEqual(out["action"], "WITHHOLD")
        self.assertIn("38.0", out["conclusion"])


class AlignKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        mod = load_module("H11-ALIGN", "L17_alignment_safety/H11-ALIGN/agent.py")
        self.agent = mod.H11AlignOrchestrator()

    def test_treat_allowed_when_constraints_hold(self):
        out = self.agent.evaluate_case(
            {
                "would_treat": True,
                "confidence": 0.96,
                "map_mmhg": 81.0,
                "named_protocol": True,
            }
        )
        self.assertTrue(out["allowed"])
        self.assertEqual(out["violations"], [])

    def test_treat_halted_below_confidence_floor(self):
        out = self.agent.evaluate_case(
            {
                "would_treat": True,
                "confidence": 0.4,
                "map_mmhg": 81.0,
                "named_protocol": True,
            }
        )
        self.assertFalse(out["allowed"])
        self.assertTrue(any("non_maleficence" in v for v in out["violations"]))


class CognitiveTickTests(unittest.IsolatedAsyncioTestCase):
    async def test_socrates_query_is_licensed(self):
        agi = H11AGI()
        result = await agi.tick(
            {
                "query": "Is Socrates mortal?",
                "premises": ["All men are mortal.", "Socrates is a man."],
            }
        )
        self.assertTrue(result.admitted)
        self.assertEqual(result.pipeline_id, "cognitive_loop")
        self.assertTrue(result.allowed)
        self.assertTrue(result.licensed)
        self.assertFalse(result.halted)
        self.assertIn("Socrates is mortal", result.payload["reason"]["conclusion"])
        self.assertIn("H11-ALIGN", result.hops)

    async def test_follow_up_recalls_prior_diagnosis(self):
        agi = H11AGI()
        first = await agi.tick(
            {
                "patient_id": "P-1001",
                "travel_history": ["Kenya"],
                "symptoms": ["fever", "chills"],
                "blood_smear_density_per_ul": 5200.0,
            }
        )
        self.assertTrue(first.licensed)
        self.assertEqual(first.action, "TREAT")
        second = await agi.tick(
            {
                "patient_id": "P-1001",
                "query": "what parasite was identified?",
            }
        )
        self.assertEqual(second.pipeline_id, "cognitive_loop")
        self.assertTrue(second.allowed)
        self.assertTrue(second.licensed)
        self.assertIn("Plasmodium falciparum", second.payload["reason"]["conclusion"])
        self.assertNotEqual(second.action, "TREAT")


if __name__ == "__main__":
    unittest.main()
