"""Automated Agent Ablation Benchmark (v3.0 Section 19).

Measures:
- Full System vs Without A vs Without B vs Without C
- Metrics: Execution success, Deliberation consensus count, Verification scores, Latency
- Validates that specialist presence contributes measurably to consensus depth.
"""
from __future__ import annotations

import asyncio
import time
import unittest
from typing import Any, Dict, List

from h11_runtime.agi import H11AGI, AGIResult
from h11_runtime.contracts.envelope import CaseEnvelope, RiskClass


class TestAgentAblationBenchmark(unittest.IsolatedAsyncioTestCase):
    """Systematic ablation experiment quantifying specialist contribution."""

    async def asyncSetUp(self) -> None:
        self.agi = H11AGI(enable_search=False, enable_learning=False)
        await self.agi.initialize()

    async def test_systematic_ablation_matrix(self) -> None:
        query = "Calculate quantum coherence dephasing rate in multi-qubit cavity coupled to thermal bath"
        case_env = CaseEnvelope(
            input_data={"query": query, "symptoms": []},
            objective="Quantum Physics Modeling",
            risk_class=RiskClass.R1_LOW,
        )

        # Baseline: Full System
        t0 = time.time()
        res_full = await self.agi.tick(case_env)
        full_latency = (time.time() - t0) * 1000.0

        full_contributors = list(res_full.contributing_agents)
        self.assertGreaterEqual(len(full_contributors), 2)
        full_consensus_count = len(res_full.deliberation.get("consensus_claims", []))

        ablation_results: Dict[str, Dict[str, Any]] = {
            "FULL_SYSTEM": {
                "contributors_count": len(full_contributors),
                "consensus_count": full_consensus_count,
                "latency_ms": full_latency,
                "verification_status": res_full.verification.get("status"),
            }
        }

        # Ablate each contributing specialist independently against the same
        # baseline planner. Re-wrapping the prior ablation recursively changes
        # multiple variables at once and eventually recurses into itself.
        original_create_plan = self.agi.planner.create_plan
        for specialist in full_contributors[:3]:
            def make_ablated_planner(ablated_ag):
                def ablated_plan(*args, **kwargs):
                    plan = original_create_plan(*args, **kwargs)
                    plan.activated_agents = [ag for ag in plan.activated_agents if ag != ablated_ag]
                    for sg in plan.subgoals:
                        sg.assigned_specialists = [ag for ag in sg.assigned_specialists if ag != ablated_ag]
                    return plan
                return ablated_plan

            self.agi.planner.create_plan = make_ablated_planner(specialist)

            t_start = time.time()
            res_ablated = await self.agi.tick(CaseEnvelope(input_data={"query": query}, risk_class=RiskClass.R1_LOW))
            t_elapsed = (time.time() - t_start) * 1000.0

            ablated_consensus_count = len(res_ablated.deliberation.get("consensus_claims", []))
            self.assertNotIn(specialist, res_ablated.contributing_agents)
            self.assertLess(
                ablated_consensus_count,
                full_consensus_count,
                f"Ablating specialist {specialist} must reduce deliberation consensus claims.",
            )

            ablation_results[f"WITHOUT_{specialist}"] = {
                "contributors_count": len(res_ablated.contributing_agents),
                "consensus_count": ablated_consensus_count,
                "latency_ms": t_elapsed,
                "verification_status": res_ablated.verification.get("status"),
            }

        # Assert full ablation metrics matrix was constructed
        self.assertGreaterEqual(len(ablation_results), 3)
        print("\n=== AGENT ABLATION BENCHMARK RESULTS ===")
        for condition, metrics in ablation_results.items():
            print(f"[{condition}]: Contributors={metrics['contributors_count']}, Consensus Claims={metrics['consensus_count']}, Latency={metrics['latency_ms']:.1f}ms")
        print("========================================")


if __name__ == "__main__":
    unittest.main()
