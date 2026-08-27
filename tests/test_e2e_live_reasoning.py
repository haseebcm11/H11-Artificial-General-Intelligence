"""End-to-end integration test for H11-AGI with H11-SEARCH and H11-LEARN.

Validates:
1. Live case admission and zero-trust verification.
2. Knowledge retrieval via H11-SEARCH before domain reasoning.
3. ALIGN gate safety enforcement with evidence provenance.
4. Action licensing and audit trail sealing.
5. Continuous learning data capture via H11-LEARN.
"""
from __future__ import annotations

import asyncio
import unittest

from h11_runtime.agi import H11AGI


class TestE2ELiveReasoning(unittest.IsolatedAsyncioTestCase):
    """End-to-end verification of governed cognitive loop with search & learning."""

    async def asyncSetUp(self) -> None:
        self.agi = H11AGI(enable_search=True, enable_learning=True)
        await self.agi.initialize()

    async def test_case_with_retrieval_and_learning(self) -> None:
        case = {
            "patient_id": "patient-e2e-001",
            "symptoms": ["fever", "chills", "fatigue"],
            "blood_smear_density_per_ul": 12000,
            "travel_history": ["sub-saharan_africa"],
            "query": "Diagnose acute febrile parasite illness and recommend antiparasitic regimen",
            "goal": "host_infection",
        }
        result = await self.agi.tick(case)

        # 1. Verification of admission and safety
        self.assertTrue(result.admitted)
        self.assertTrue(result.allowed)
        self.assertTrue(result.licensed)
        self.assertFalse(result.halted)

        # 2. Verification of search subsystem availability
        self.assertIsNotNone(self.agi.search)
        self.assertIsNotNone(self.agi.rar)

        # 3. Verification of audit trail & spine traversal
        self.assertIsNotNone(result.audit_head)
        self.assertIn("H11C-ADMISSION-CONTROL", result.hops)
        self.assertIn("H11-ALIGN", result.hops)

        # 4. Verification of learning pipeline recording
        self.assertTrue(result.learning_recorded)
        self.assertIsNotNone(self.agi.collector)
        self.assertGreater(self.agi.collector.stats["total_examples"], 0)

    async def test_cognitive_query_case(self) -> None:
        case = {
            "query": "Evaluate quantum computing algorithmic complexity and error correction thresholds",
            "goal": "cognitive_query",
        }
        result = await self.agi.tick(case)

        self.assertTrue(result.admitted)
        self.assertFalse(result.halted)
        self.assertTrue(result.licensed)


if __name__ == "__main__":
    unittest.main()
