"""Typed, statically critiqued tool-plan synthesis for bounded goals."""
from __future__ import annotations

import ast
import dataclasses
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..tools import GovernedToolRegistry


@dataclass
class PlanCritique:
    valid: bool
    score: float
    issues: List[str] = field(default_factory=list)
    estimated_tool_calls: int = 0


@dataclass
class ToolPlanCandidate:
    candidate_id: str
    source: str
    expression: str
    plan: List[Dict[str, Any]]
    expectations: List[Dict[str, Any]]
    rationale: str
    critique: PlanCritique

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass
class AutonomousPlanResult:
    status: str
    selected: Optional[ToolPlanCandidate]
    candidates: List[ToolPlanCandidate] = field(default_factory=list)
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "selected_candidate_id": self.selected.candidate_id if self.selected else None,
            "selected_plan": self.selected.plan if self.selected else [],
            "selected_expectations": self.selected.expectations if self.selected else [],
            "reason": self.reason,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
        }


class AutonomousToolPlanner:
    """Generates and critiques typed capability DAGs without evaluating code."""

    _OPERATIONS = {
        ast.Add: ("math.add", "values"),
        ast.Sub: ("math.subtract", None),
        ast.Mult: ("math.multiply", "values"),
        ast.Div: ("math.divide", None),
        ast.Pow: ("math.power", None),
    }

    def __init__(self, registry: GovernedToolRegistry, max_plan_steps: int = 12) -> None:
        self.registry = registry
        self.max_plan_steps = max_plan_steps

    def synthesize(self, goal: str, case_context: Mapping[str, Any]) -> AutonomousPlanResult:
        expressions: List[Tuple[str, str]] = []
        explicit = case_context.get("objective_expression")
        if isinstance(explicit, str) and explicit.strip():
            expressions.append(("objective_expression", explicit.strip()))
        inferred = self._infer_expression(goal)
        if inferred and all(expression != inferred for _, expression in expressions):
            expressions.append(("natural_language", inferred))
        candidates: List[ToolPlanCandidate] = []
        for index, (source, expression) in enumerate(expressions):
            try:
                plan = self._compile_expression(expression, case_context)
                expectations = self._expectations(case_context)
                critique = self.critique(plan, case_context)
                candidate = ToolPlanCandidate(
                    candidate_id=f"AUTO-PLAN-{index + 1}",
                    source=source,
                    expression=expression,
                    plan=plan,
                    expectations=expectations,
                    rationale=f"Compiled a typed arithmetic DAG from {source}.",
                    critique=critique,
                )
            except (SyntaxError, ValueError, TypeError) as exc:
                candidate = ToolPlanCandidate(
                    candidate_id=f"AUTO-PLAN-{index + 1}",
                    source=source,
                    expression=expression,
                    plan=[],
                    expectations=[],
                    rationale=f"Rejected {source} during safe AST compilation.",
                    critique=PlanCritique(False, 0.0, [str(exc)], 0),
                )
            candidates.append(candidate)

        capability_candidate = self._compile_capability_goal(
            goal=goal,
            case_context=case_context,
            candidate_id=f"AUTO-PLAN-{len(candidates) + 1}",
        )
        if capability_candidate is not None:
            candidates.append(capability_candidate)
        if not candidates:
            return AutonomousPlanResult("UNSUPPORTED", None, reason="no supported capability grammar matched the goal")

        valid = [candidate for candidate in candidates if candidate.critique.valid]
        if not valid:
            return AutonomousPlanResult("REJECTED", None, candidates, "all candidate plans failed static critique")
        selected = max(valid, key=lambda candidate: candidate.critique.score)
        return AutonomousPlanResult("PLANNED", selected, candidates, "selected highest-scoring safe candidate")

    def _compile_capability_goal(
        self,
        goal: str,
        case_context: Mapping[str, Any],
        candidate_id: str,
    ) -> Optional[ToolPlanCandidate]:
        text = goal.lower()
        wants_research = any(
            phrase in text
            for phrase in ("research", "find evidence", "find sources", "search for", "look up", "latest evidence")
        )
        wants_specialists = any(
            phrase in text
            for phrase in ("consult specialists", "consult experts", "route specialists", "which specialists", "select experts")
        )
        if not wants_research and not wants_specialists:
            return None

        query = str(case_context.get("research_query") or case_context.get("query") or goal).strip()
        plan: List[Dict[str, Any]] = []
        expectations: List[Dict[str, Any]] = []
        capabilities: List[str] = []
        if wants_research:
            plan.append({
                "call_id": "research",
                "tool": "knowledge.search",
                "arguments": {"query": query},
                "save_as": "research",
                "max_attempts": 2,
            })
            expectations.append({"path": "research.results", "operator": "nonempty", "value": None})
            capabilities.append("knowledge.search")
        if wants_specialists:
            plan.append({
                "call_id": "specialists",
                "tool": "agents.route",
                "arguments": {"query": query},
                "save_as": "specialists",
                "max_attempts": 1,
            })
            expectations.append({"path": "specialists.selected_agent_ids", "operator": "nonempty", "value": None})
            capabilities.append("agents.route")
        critique = self.critique(plan, case_context)
        return ToolPlanCandidate(
            candidate_id=candidate_id,
            source="capability_grammar",
            expression="",
            plan=plan,
            expectations=expectations,
            rationale="Compiled goal into typed capabilities: " + ", ".join(capabilities),
            critique=critique,
        )

    def critique(self, plan: Sequence[Mapping[str, Any]], case_context: Mapping[str, Any]) -> PlanCritique:
        issues: List[str] = []
        available_outputs: set[str] = set()
        if not plan:
            issues.append("plan is empty")
        if len(plan) > self.max_plan_steps:
            issues.append(f"plan exceeds {self.max_plan_steps}-step limit")
        for index, call in enumerate(plan):
            tool_name = str(call.get("tool") or "")
            spec = self.registry.get(tool_name)
            if spec is None:
                issues.append(f"step {index + 1}: unknown tool {tool_name}")
                continue
            if not spec.side_effect_free:
                issues.append(f"step {index + 1}: side-effecting tool is not eligible for autonomous planning")
            arguments = call.get("arguments")
            if not isinstance(arguments, Mapping):
                issues.append(f"step {index + 1}: arguments must be an object")
                continue
            missing = [name for name in spec.required_arguments if name not in arguments]
            if missing:
                issues.append(f"step {index + 1}: missing arguments {', '.join(missing)}")
            for reference in self._references(arguments):
                root, _, path = reference.partition(".")
                if root == "case":
                    if not path or not self._path_exists(case_context, path):
                        issues.append(f"step {index + 1}: unresolved case reference {reference}")
                elif root not in available_outputs:
                    issues.append(f"step {index + 1}: forward or unresolved reference {reference}")
            available_outputs.add(str(call.get("save_as") or call.get("call_id") or f"tool-step-{index + 1}"))
        valid = not issues
        efficiency = max(0.0, 1.0 - (len(plan) / max(1, self.max_plan_steps)) * 0.25)
        return PlanCritique(valid, round(efficiency if valid else 0.0, 4), issues, len(plan))

    def _compile_expression(self, expression: str, case_context: Mapping[str, Any]) -> List[Dict[str, Any]]:
        if len(expression) > 256:
            raise ValueError("expression exceeds 256-character safety limit")
        tree = ast.parse(expression, mode="eval")
        plan: List[Dict[str, Any]] = []

        def compile_node(node: ast.AST) -> Any:
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return node.value
            if isinstance(node, ast.Name):
                value = case_context.get(node.id)
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(f"expression variable is absent or non-numeric: {node.id}")
                return f"${{case.{node.id}}}"
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
                operand = compile_node(node.operand)
                if not isinstance(operand, (int, float)):
                    raise ValueError("unary operators are allowed only on numeric literals")
                return -operand if isinstance(node.op, ast.USub) else operand
            if not isinstance(node, ast.BinOp) or type(node.op) not in self._OPERATIONS:
                raise ValueError(f"unsupported expression node: {type(node).__name__}")
            left = compile_node(node.left)
            right = compile_node(node.right)
            tool_name, aggregate_arg = self._OPERATIONS[type(node.op)]
            save_as = f"auto_step_{len(plan) + 1}"
            if aggregate_arg:
                arguments = {aggregate_arg: [left, right]}
            elif isinstance(node.op, ast.Sub):
                arguments = {"left": left, "right": right}
            elif isinstance(node.op, ast.Div):
                arguments = {"numerator": left, "denominator": right}
            else:
                arguments = {"base": left, "exponent": right}
            plan.append({
                "call_id": save_as,
                "tool": tool_name,
                "arguments": arguments,
                "save_as": save_as,
                "max_attempts": 1,
            })
            return f"${{{save_as}}}"

        final_reference = compile_node(tree.body)
        if not plan:
            raise ValueError("expression must contain at least one operation")
        old_name = plan[-1]["save_as"]
        plan[-1]["save_as"] = "answer"
        plan[-1]["call_id"] = "answer"
        if final_reference != f"${{{old_name}}}":
            raise ValueError("internal plan terminal mismatch")
        return plan

    @staticmethod
    def _expectations(case_context: Mapping[str, Any]) -> List[Dict[str, Any]]:
        expected = case_context.get("expected_result")
        if isinstance(expected, (int, float)) and not isinstance(expected, bool):
            return [{"path": "answer", "operator": "approx", "value": expected, "tolerance": 1e-9}]
        return [{"path": "answer", "operator": "is_number", "value": None}]

    @staticmethod
    def _infer_expression(goal: str) -> str:
        text = " ".join(goal.lower().strip().split())
        number = r"([-+]?\d+(?:\.\d+)?)"
        patterns = [
            (rf"add {number} (?:and|to) {number},? then multiply (?:the )?(?:result )?by {number}", lambda m: f"({m[1]}+{m[2]})*{m[3]}"),
            (rf"multiply {number} (?:and|by) {number},? then add {number}", lambda m: f"({m[1]}*{m[2]})+{m[3]}"),
            (rf"divide {number} by {number}", lambda m: f"{m[1]}/{m[2]}"),
            (rf"subtract {number} from {number}", lambda m: f"{m[2]}-{m[1]}"),
            (rf"add {number} (?:and|to) {number}", lambda m: f"{m[1]}+{m[2]}"),
            (rf"multiply {number} (?:and|by) {number}", lambda m: f"{m[1]}*{m[2]}"),
        ]
        for pattern, builder in patterns:
            match = re.search(pattern, text)
            if match:
                return builder(match)
        calculate = re.search(r"(?:calculate|compute|evaluate)\s+([0-9+\-*/(). ^]+)", text)
        if calculate:
            return calculate.group(1).strip().replace("^", "**")
        return ""

    @classmethod
    def _references(cls, value: Any) -> List[str]:
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            return [value[2:-1]]
        if isinstance(value, Mapping):
            return [ref for item in value.values() for ref in cls._references(item)]
        if isinstance(value, list):
            return [ref for item in value for ref in cls._references(item)]
        return []

    @staticmethod
    def _path_exists(value: Any, path: str) -> bool:
        current = value
        for part in path.split("."):
            if not isinstance(current, Mapping) or part not in current:
                return False
            current = current[part]
        return True
