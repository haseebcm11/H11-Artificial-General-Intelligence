from __future__ import annotations

import unittest

from h11_runtime import H11AGI
from h11_runtime.case.blackboard import Blackboard
from h11_runtime.case.world_model import WorldModel
from h11_runtime.evidence.ledger import EvidenceLedger
from h11_runtime.state.budget import ResourceBudget
from h11_runtime.tools import AutonomousToolLoop, GovernedToolRegistry, ToolSpec


class AutonomousToolLoopTests(unittest.IsolatedAsyncioTestCase):
    async def test_multi_step_plan_resolves_observations_and_evaluates_goal(self) -> None:
        board = Blackboard("CASE-TOOLS")
        world = WorldModel("CASE-TOOLS")
        ledger = EvidenceLedger()
        budget = ResourceBudget(max_tool_calls=4)
        result = await AutonomousToolLoop().run(
            plan=[
                {"call_id": "sum", "tool": "math.add", "arguments": {"values": [2, 3]}, "save_as": "sum"},
                {
                    "call_id": "scaled",
                    "tool": "math.multiply",
                    "arguments": {"values": ["${sum}", "${case.scale}"]},
                    "save_as": "scaled",
                },
            ],
            expectations=[{"path": "scaled", "operator": "eq", "value": 20.0}],
            case_context={"scale": 4},
            blackboard=board,
            world_model=world,
            evidence_ledger=ledger,
            budget=budget,
        )

        self.assertEqual(result.status, "COMPLETED")
        self.assertTrue(result.evaluation.passed)
        self.assertEqual(result.outputs["scaled"], 20.0)
        self.assertEqual(result.budget["used_tool_calls"], 2)
        self.assertEqual(len(world.observations), 2)
        self.assertEqual(len(ledger.items), 2)
        self.assertTrue(all(obs.provenance_hash for obs in result.observations))

    async def test_recoverable_failure_is_retried_within_budget(self) -> None:
        attempts = {"count": 0}

        def flaky(value: int) -> int:
            attempts["count"] += 1
            if attempts["count"] == 1:
                raise ConnectionError("temporary failure")
            return value * 2

        registry = GovernedToolRegistry(include_builtins=False)
        registry.register(ToolSpec("test.flaky", "Fails once.", flaky, ("value",)))
        result = await AutonomousToolLoop(registry).run(
            plan=[{"tool": "test.flaky", "arguments": {"value": 6}, "save_as": "answer", "max_attempts": 2}],
            expectations=[{"path": "answer", "operator": "eq", "value": 12}],
            case_context={},
            blackboard=Blackboard("CASE-RETRY"),
            world_model=WorldModel("CASE-RETRY"),
            evidence_ledger=EvidenceLedger(),
            budget=ResourceBudget(max_tool_calls=2),
        )

        self.assertTrue(result.evaluation.passed)
        self.assertEqual(result.observations[0].attempts, 2)
        self.assertEqual(result.budget["used_tool_calls"], 2)

    async def test_unknown_tool_fails_closed(self) -> None:
        result = await AutonomousToolLoop().run(
            plan=[{"tool": "shell.execute", "arguments": {"command": "anything"}}],
            expectations=[],
            case_context={},
            blackboard=Blackboard("CASE-DENIED"),
            world_model=WorldModel("CASE-DENIED"),
            evidence_ledger=EvidenceLedger(),
        )

        self.assertEqual(result.status, "INCOMPLETE")
        self.assertEqual(result.observations[0].status, "DENIED")
        self.assertEqual(result.budget["used_tool_calls"], 0)

    async def test_full_agi_tick_releases_only_satisfied_tool_goal(self) -> None:
        agi = H11AGI(enable_search=False, enable_learning=False)
        result = await agi.tick({
            "query": "Add two values and scale the result",
            "goal": "mathematical reasoning",
            "scale": 4,
            "tool_plan": [
                {"tool": "math.add", "arguments": {"values": [2, 3]}, "save_as": "sum"},
                {"tool": "math.multiply", "arguments": {"values": ["${sum}", "${case.scale}"]}, "save_as": "answer"},
            ],
            "tool_expectations": [{"path": "answer", "operator": "eq", "value": 20.0}],
        })

        self.assertIsNotNone(result.tool_loop)
        self.assertTrue(result.tool_loop["evaluation"]["passed"])
        self.assertEqual(result.payload["tool_results"]["answer"], 20.0)
        self.assertTrue(result.licensed)

    async def test_full_agi_tick_halts_when_tool_goal_is_not_satisfied(self) -> None:
        agi = H11AGI(enable_search=False, enable_learning=False)
        result = await agi.tick({
            "query": "Verify the calculated value before release",
            "goal": "mathematical reasoning",
            "tool_plan": [
                {"tool": "math.add", "arguments": {"values": [2, 3]}, "save_as": "answer"},
            ],
            "tool_expectations": [{"path": "answer", "operator": "eq", "value": 999}],
        })

        self.assertFalse(result.tool_loop["evaluation"]["passed"])
        self.assertFalse(result.allowed)
        self.assertFalse(result.licensed)
        self.assertIn("tool_goal_not_satisfied", result.events)


if __name__ == "__main__":
    unittest.main()
