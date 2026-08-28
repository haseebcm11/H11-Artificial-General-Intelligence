"""Cross-Domain AGI Multi-Specialist and Replanning Benchmark (v3.0 Section 20).

Tests:
1. Multi-domain problem spanning physics, pharmacology, and formal mathematics.
2. Goal decomposition into multi-stage ExecutionGraph with 3+ independent specialists.
3. Live LSE evidence acquisition and Merkle provenance binding.
4. Independent verification and recursive replanning loop upon simulated contradiction/rejection.
5. Sovereign H11C governance, action licensing, and cryptographic audit witness.
"""
from __future__ import annotations

import asyncio
import unittest
from typing import Any, Dict, List

from h11_runtime.agi import H11AGI, AGIResult
from h11_runtime.contracts.envelope import CaseEnvelope, RiskClass
from h11_runtime.deliberation.deliberator import SynthesisCandidate
from h11_runtime.verification.verifier import VerificationReport


class TestCrossDomainAGI(unittest.IsolatedAsyncioTestCase):
    """Cross-Domain recursive cognitive integration benchmark."""

    async def asyncSetUp(self) -> None:
        self.agi = H11AGI(enable_search=True, enable_learning=True)
        await self.agi.initialize()

    async def test_cross_domain_reasoning_and_replanning_cycle(self) -> None:
        complex_query = (
            "Model electromagnetic nanoparticle drug delivery in targeted oncology, "
            "optimizing magnetic field gradient tensor and bio-distribution clearance equations"
        )
        case_env = CaseEnvelope(
            input_data={"query": complex_query, "symptoms": []},
            objective="Cross-Domain Nanomedicine & Applied Physics",
            risk_class=RiskClass.R1_LOW,
        )

        result: AGIResult = await self.agi.tick(case_env)

        # 1. Verification of Canonical Cognitive Loop Trajectory
        expected_states = ["NEW", "ADMITTED", "CONTEXTUALIZED", "MAPPED", "COMPOSED", "PLANNING", "EXECUTING", "DELIBERATING", "VERIFYING", "INTEGRATING", "ALIGNING", "RELEASED", "OBSERVING", "MEMORIZED", "CLOSED"]
        for expected in ["ADMITTED", "PLANNING", "EXECUTING", "DELIBERATING", "VERIFYING", "ALIGNING", "RELEASED"]:
            self.assertIn(expected, result.state_progression, f"Cognitive trajectory must pass through {expected}")

        # 2. Multi-Specialist Execution (at least 3 specialists from distinct domains)
        self.assertGreaterEqual(len(result.contributing_agents), 3, "Cross-domain task must execute at least 3 specialists")
        
        # 3. Deliberation & Verification
        self.assertIsNotNone(result.deliberation)
        self.assertGreater(len(result.deliberation.get("consensus_claims", [])), 0)
        self.assertEqual(result.verification.get("status"), "PASSED")
        self.assertTrue(result.verification.get("policy_compliance"))

        # 4. H11C Zero-Trust Licensing & Audit Witness
        self.assertTrue(result.licensed)
        self.assertTrue(result.allowed)
        self.assertFalse(result.halted)
        self.assertIsNotNone(result.audit_head)
        self.assertEqual(len(result.audit_head), 64, "Audit head must be a valid SHA-256 hash")

        # 5. Continuous Learning Recording
        self.assertTrue(result.learning_recorded, "Non-simulated experience must be logged into H11-LEARN")

    async def test_recursive_replanning_on_verification_failure(self) -> None:
        """Simulates an initial verification rejection and confirms autonomous recursive replanning."""
        complex_query = "Calculate relativistic plasma wakefield acceleration threshold with conflicting field assumptions"
        case_env = CaseEnvelope(
            input_data={"query": complex_query, "symptoms": []},
            objective="Plasma Physics Verification",
            risk_class=RiskClass.R1_LOW,
        )

        original_verifier = self.agi.verifier.verify
        call_count = 0

        def rejecting_first_verifier(synthesis, evidence_ledger=None):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # Reject first iteration to trigger replanner
                return VerificationReport(
                    passed=False,
                    status="REJECTED",
                    confidence_score=0.4,
                    factual_support_score=0.3,
                    logical_consistency_score=0.4,
                    policy_compliance=True,
                    rejection_reasons=["Contradictory plasma density assumptions detected."],
                    recommended_replan_actions=["ACTIVATE_ARBITER_SPECIALISTS"],
                )
            # Second iteration passes after replanning
            return original_verifier(synthesis, evidence_ledger)

        self.agi.verifier.verify = rejecting_first_verifier

        result: AGIResult = await self.agi.tick(case_env)

        self.assertIn("REPLANNING", result.state_progression, "State progression must record REPLANNING stage")
        self.assertIn("replanning_triggered", result.events, "Events must log replanning trigger")
        self.assertTrue(result.cognitive_plan.get("is_replanned"), "Cognitive plan must be marked as replanned")
        self.assertGreaterEqual(result.cognitive_plan.get("iteration"), 2, "Plan iteration must advance")
        self.assertEqual(result.verification.get("status"), "PASSED", "Final verification after replan must pass")


if __name__ == "__main__":
    unittest.main()
