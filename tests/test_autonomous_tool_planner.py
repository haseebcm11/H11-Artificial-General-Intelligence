from __future__ import annotations

import unittest

from h11_runtime import H11AGI
from h11_runtime.planning import AutonomousToolPlanner
from h11_runtime.tools import GovernedToolRegistry, ToolSpec


class AutonomousToolPlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.planner = AutonomousToolPlanner(GovernedToolRegistry())

    def test_natural_language_goal_compiles_to_typed_dag(self) -> None:
        result = self.planner.synthesize(
            "Add 2 and 3, then multiply the result by 4",
            {"expected_result": 20},
        )

        self.assertEqual(result.status, "PLANNED")
        self.assertEqual([step["tool"] for step in result.selected.plan], ["math.add", "math.multiply"])
        self.assertEqual(result.selected.plan[1]["arguments"]["values"][0], "${auto_step_1}")
        self.assertTrue(result.selected.critique.valid)

    def test_safe_candidate_wins_when_explicit_candidate_is_unsafe(self) -> None:
        result = self.planner.synthesize(
            "Add 2 and 3",
            {"objective_expression": "__import__('os').system('bad')", "expected_result": 5},
        )

        self.assertEqual(result.status, "PLANNED")
        self.assertEqual(result.selected.source, "natural_language")
        self.assertFalse(result.candidates[0].critique.valid)

    def test_plan_over_static_step_budget_is_rejected(self) -> None:
        expression = "+".join(str(value) for value in range(14))
        result = self.planner.synthesize("unsupported prose", {"objective_expression": expression})

        self.assertEqual(result.status, "REJECTED")
        self.assertIn("12-step limit", result.candidates[0].critique.issues[0])

    def test_capability_plan_is_selected_only_when_tools_are_available(self) -> None:
        unavailable = self.planner.synthesize("Research and find evidence about malaria", {})
        self.assertEqual(unavailable.status, "REJECTED")
        self.assertIn("unknown tool knowledge.search", unavailable.candidates[0].critique.issues[0])

        registry = GovernedToolRegistry()
        registry.register(ToolSpec("knowledge.search", "test search", lambda query: {"results": [query]}, ("query",)))
        registry.register(ToolSpec("agents.route", "test router", lambda query: {"selected_agent_ids": [query]}, ("query",)))
        planner = AutonomousToolPlanner(registry)
        available = planner.synthesize("Research sources and consult specialists about malaria", {})

        self.assertEqual(available.status, "PLANNED")
        self.assertEqual(
            [step["tool"] for step in available.selected.plan],
            ["knowledge.search", "agents.route"],
        )


class AutonomousPlannerAGIIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_natural_language_plan_executes_and_releases(self) -> None:
        agi = H11AGI(enable_search=False, enable_learning=False)
        result = await agi.tick({
            "query": "Add 2 and 3, then multiply the result by 4",
            "goal": "solve the arithmetic task",
            "auto_tools": True,
            "expected_result": 20,
        })

        self.assertEqual(result.tool_planning["status"], "PLANNED")
        self.assertEqual(result.tool_loop["outputs"]["answer"], 20.0)
        self.assertTrue(result.tool_loop["evaluation"]["passed"])
        self.assertTrue(result.allowed)
        self.assertTrue(result.licensed)

    async def test_unsupported_autonomous_goal_fails_closed(self) -> None:
        agi = H11AGI(enable_search=False, enable_learning=False)
        result = await agi.tick({
            "query": "Invent an entirely new scientific discipline",
            "goal": "open-ended invention",
            "auto_tools": True,
        })

        self.assertEqual(result.tool_planning["status"], "UNSUPPORTED")
        self.assertIsNone(result.tool_loop)
        self.assertFalse(result.allowed)
        self.assertFalse(result.licensed)
        self.assertIn("autonomous_tool_plan_unavailable", result.events)

    async def test_autonomous_research_is_grounded_and_released(self) -> None:
        agi = H11AGI(enable_search=True, enable_learning=False)
        result = await agi.tick({
            "query": "Research and find evidence about malaria treatment",
            "goal": "evidence-grounded research",
            "auto_tools": True,
        })

        self.assertEqual(result.tool_planning["status"], "PLANNED")
        self.assertTrue(result.tool_loop["evaluation"]["passed"])
        self.assertTrue(result.tool_loop["outputs"]["research"]["results"])
        self.assertTrue(result.payload["retrieved_evidence"])
        self.assertIn("autonomous_research_grounded_8", result.events)
        self.assertTrue(result.licensed)

    async def test_research_goal_without_search_capability_fails_closed(self) -> None:
        agi = H11AGI(enable_search=False, enable_learning=False)
        result = await agi.tick({
            "query": "Research and find evidence about malaria treatment",
            "goal": "evidence-grounded research",
            "auto_tools": True,
        })

        self.assertEqual(result.tool_planning["status"], "REJECTED")
        self.assertFalse(result.allowed)
        self.assertFalse(result.licensed)


if __name__ == "__main__":
    unittest.main()
