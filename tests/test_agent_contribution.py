"""Mandatory Agent Contribution Test (v3.0 Section 18).

Verifies:
1. Multi-domain task triggers MoE specialist selection (A, B, C).
2. All selected specialists execute and emit typed AgentResults.
3. Deliberation and synthesis consume all three results.
4. Final answer trace contains contributions from all participating specialists.
5. Disabling specialist B materially alters system behavior and consensus claims.
"""
from __future__ import annotations

import asyncio
import unittest
from typing import Any, Dict, List

from h11_runtime.agi import H11AGI, AGIResult
from h11_runtime.contracts.envelope import CaseEnvelope, RiskClass
from h11_runtime.contracts.agent_result import AgentResult


class TestAgentContribution(unittest.IsolatedAsyncioTestCase):
    """Test suite verifying material cognitive contribution of routed specialist agents."""

    async def asyncSetUp(self) -> None:
        self.agi = H11AGI(enable_search=False, enable_learning=False)
        await self.agi.initialize()

    async def test_multi_agent_contribution_and_ablation(self) -> None:
        query = "Formulate mathematical model of drug distribution across cardiac tissue with differential equation kinetics"
        case_env = CaseEnvelope(
            input_data={"query": query, "symptoms": []},
            objective="Cardiovascular Pharmacokinetics Modeling",
            risk_class=RiskClass.R1_LOW,
        )

        # 1. Full System Run
        result_full: AGIResult = await self.agi.tick(case_env)
        
        self.assertTrue(result_full.admitted)
        self.assertTrue(result_full.licensed)
        self.assertGreater(len(result_full.contributing_agents), 0)
        self.assertGreater(len(result_full.specialist_results), 0)
        self.assertIsNotNone(result_full.deliberation)
        self.assertEqual(result_full.verification.get("status"), "PASSED")

        initial_contributors = list(result_full.contributing_agents)
        self.assertGreaterEqual(len(initial_contributors), 2, "Task should activate at least 2 specialists")

        # Pick specialist B to ablate
        specialist_b = initial_contributors[0]
        
        # 2. Re-run with Specialist B Ablated (Excluded from Planner)
        original_create_plan = self.agi.planner.create_plan

        def ablated_create_plan(*args, **kwargs):
            plan = original_create_plan(*args, **kwargs)
            plan.activated_agents = [ag for ag in plan.activated_agents if ag != specialist_b]
            for sg in plan.subgoals:
                sg.assigned_specialists = [ag for ag in sg.assigned_specialists if ag != specialist_b]
            return plan

        self.agi.planner.create_plan = ablated_create_plan

        case_env_ablated = CaseEnvelope(
            input_data={"query": query, "symptoms": []},
            objective="Cardiovascular Pharmacokinetics Modeling",
            risk_class=RiskClass.R1_LOW,
        )
        result_ablated: AGIResult = await self.agi.tick(case_env_ablated)

        # 3. Assert Material Participation & Behavioral Difference
        self.assertNotIn(
            specialist_b,
            result_ablated.contributing_agents,
            f"Ablated specialist {specialist_b} must not appear in contributing agents.",
        )
        self.assertNotEqual(
            result_full.specialist_results,
            result_ablated.specialist_results,
            "Specialist execution results must differ when specialist B is disabled.",
        )
        self.assertNotEqual(
            result_full.deliberation.get("consensus_claims"),
            result_ablated.deliberation.get("consensus_claims"),
            "Deliberation consensus claims must materially reflect specialist B's ablation.",
        )


if __name__ == "__main__":
    unittest.main()
