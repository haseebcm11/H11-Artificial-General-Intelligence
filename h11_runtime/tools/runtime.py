"""Governed observe-act-recover tool runtime for bounded autonomous tasks."""
from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

from ..case.blackboard import Blackboard
from ..case.world_model import WorldModel
from ..evidence.item import EvidenceItem
from ..evidence.ledger import EvidenceLedger
from ..state.budget import ResourceBudget


ToolCallable = Callable[..., Any]
ToolAuthorizer = Callable[[str], bool]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    handler: ToolCallable
    required_arguments: Sequence[str] = field(default_factory=tuple)
    side_effect_free: bool = True
    timeout_seconds: float = 2.0
    retryable_exceptions: tuple[type[BaseException], ...] = (TimeoutError, ConnectionError)


class GovernedToolRegistry:
    """Explicit allowlist of trusted callables; unknown names fail closed."""

    def __init__(self, include_builtins: bool = True) -> None:
        self._tools: Dict[str, ToolSpec] = {}
        if include_builtins:
            self._register_builtins()

    def register(self, spec: ToolSpec) -> None:
        if not spec.name or spec.name.startswith("_"):
            raise ValueError("tool name must be a public identifier")
        if not callable(spec.handler):
            raise TypeError("tool handler must be callable")
        if spec.name in self._tools:
            raise ValueError(f"tool already registered: {spec.name}")
        self._tools[spec.name] = spec

    def get(self, name: str) -> Optional[ToolSpec]:
        return self._tools.get(name)

    def names(self) -> List[str]:
        return sorted(self._tools)

    def _register_builtins(self) -> None:
        self.register(ToolSpec("math.add", "Add a numeric sequence.", _math_add, ("values",)))
        self.register(ToolSpec("math.subtract", "Subtract one number from another.", _math_subtract, ("left", "right")))
        self.register(ToolSpec("math.multiply", "Multiply a numeric sequence.", _math_multiply, ("values",)))
        self.register(ToolSpec("math.divide", "Divide one number by another.", _math_divide, ("numerator", "denominator")))
        self.register(ToolSpec("math.power", "Raise a number to a bounded power.", _math_power, ("base", "exponent")))
        self.register(ToolSpec("logic.compare", "Compare two JSON-compatible values.", _compare, ("left", "operator", "right")))
        self.register(ToolSpec("data.select", "Select a value from an admitted mapping.", _select, ("data", "path")))


@dataclass
class ToolCall:
    call_id: str
    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    save_as: str = ""
    max_attempts: int = 1

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], index: int) -> "ToolCall":
        return cls(
            call_id=str(data.get("call_id") or f"tool-step-{index + 1}"),
            tool_name=str(data.get("tool") or data.get("tool_name") or ""),
            arguments=dict(data.get("arguments") or {}),
            save_as=str(data.get("save_as") or data.get("call_id") or f"tool-step-{index + 1}"),
            max_attempts=max(1, min(3, int(data.get("max_attempts") or 1))),
        )


@dataclass
class ToolObservation:
    call_id: str
    tool_name: str
    status: str
    attempts: int
    arguments: Dict[str, Any]
    output: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    provenance_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "call_id": self.call_id,
            "tool_name": self.tool_name,
            "status": self.status,
            "attempts": self.attempts,
            "arguments": self.arguments,
            "output": self.output,
            "error": self.error,
            "latency_ms": self.latency_ms,
            "provenance_hash": self.provenance_hash,
        }


@dataclass
class EvaluationCheck:
    path: str
    operator: str
    expected: Any
    actual: Any
    passed: bool


@dataclass
class TaskEvaluation:
    passed: bool
    score: float
    checks: List[EvaluationCheck] = field(default_factory=list)
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "score": self.score,
            "reason": self.reason,
            "checks": [check.__dict__ for check in self.checks],
        }


@dataclass
class ToolLoopResult:
    status: str
    observations: List[ToolObservation]
    outputs: Dict[str, Any]
    evaluation: TaskEvaluation
    budget: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "observations": [observation.to_dict() for observation in self.observations],
            "outputs": self.outputs,
            "evaluation": self.evaluation.to_dict(),
            "budget": self.budget,
        }


class AutonomousToolLoop:
    """Executes a bounded plan, observes state, recovers, and evaluates success."""

    def __init__(
        self,
        registry: Optional[GovernedToolRegistry] = None,
        authorizer: Optional[ToolAuthorizer] = None,
    ) -> None:
        self.registry = registry or GovernedToolRegistry()
        self.authorizer = authorizer or (lambda name: name in self.registry.names())

    async def run(
        self,
        plan: Sequence[Mapping[str, Any]],
        expectations: Sequence[Mapping[str, Any]],
        case_context: Mapping[str, Any],
        blackboard: Blackboard,
        world_model: WorldModel,
        evidence_ledger: EvidenceLedger,
        budget: Optional[ResourceBudget] = None,
    ) -> ToolLoopResult:
        active_budget = budget or ResourceBudget(max_tool_calls=max(1, len(plan) * 3))
        observations: List[ToolObservation] = []
        outputs: Dict[str, Any] = {}

        for index, raw_call in enumerate(plan):
            call = ToolCall.from_dict(raw_call, index)
            spec = self.registry.get(call.tool_name)
            if spec is None or not self.authorizer(call.tool_name):
                observation = self._observation(call, "DENIED", 0, {}, error="tool is not allowlisted")
                observations.append(observation)
                self._record_observation(observation, blackboard, world_model, evidence_ledger)
                break
            if not spec.side_effect_free:
                observation = self._observation(call, "DENIED", 0, {}, error="side-effecting tools require a separate action license")
                observations.append(observation)
                self._record_observation(observation, blackboard, world_model, evidence_ledger)
                break

            try:
                arguments = self._resolve_references(call.arguments, outputs, case_context)
            except (KeyError, ValueError) as exc:
                observation = self._observation(call, "BLOCKED", 0, {}, error=str(exc))
                observations.append(observation)
                self._record_observation(observation, blackboard, world_model, evidence_ledger)
                break
            missing = [name for name in spec.required_arguments if name not in arguments]
            if missing:
                observation = self._observation(
                    call, "BLOCKED", 0, arguments,
                    error="missing tool arguments: " + ", ".join(missing),
                )
                observations.append(observation)
                self._record_observation(observation, blackboard, world_model, evidence_ledger)
                break

            observation = await self._execute_with_recovery(call, spec, arguments, active_budget)
            observations.append(observation)
            self._record_observation(observation, blackboard, world_model, evidence_ledger)
            if observation.status != "COMPLETED":
                break
            outputs[call.save_as] = observation.output

        evaluation = self._evaluate(expectations, outputs, observations)
        status = "COMPLETED" if evaluation.passed else "INCOMPLETE"
        return ToolLoopResult(status, observations, outputs, evaluation, active_budget.to_dict())

    async def _execute_with_recovery(
        self,
        call: ToolCall,
        spec: ToolSpec,
        arguments: Dict[str, Any],
        budget: ResourceBudget,
    ) -> ToolObservation:
        started = time.perf_counter()
        last_error: Optional[str] = None
        attempts = 0
        while attempts < call.max_attempts:
            if not budget.can_call_tool():
                return self._observation(call, "BUDGET_EXHAUSTED", attempts, arguments, error="tool-call budget exhausted")
            attempts += 1
            budget.consume_tool_call()
            try:
                if inspect.iscoroutinefunction(spec.handler):
                    result = await asyncio.wait_for(spec.handler(**arguments), timeout=spec.timeout_seconds)
                else:
                    result = await asyncio.wait_for(
                        asyncio.to_thread(spec.handler, **arguments), timeout=spec.timeout_seconds
                    )
                return self._observation(
                    call, "COMPLETED", attempts, arguments, output=result,
                    latency_ms=(time.perf_counter() - started) * 1000.0,
                )
            except spec.retryable_exceptions as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempts >= call.max_attempts:
                    break
            except Exception as exc:
                return self._observation(
                    call, "FAILED", attempts, arguments,
                    error=f"{type(exc).__name__}: {exc}",
                    latency_ms=(time.perf_counter() - started) * 1000.0,
                )
        return self._observation(
            call, "FAILED", attempts, arguments, error=last_error or "retry limit reached",
            latency_ms=(time.perf_counter() - started) * 1000.0,
        )

    def _record_observation(
        self,
        observation: ToolObservation,
        blackboard: Blackboard,
        world_model: WorldModel,
        evidence_ledger: EvidenceLedger,
    ) -> None:
        payload = observation.to_dict()
        world_model.add_observation(f"TOOL:{observation.tool_name}", payload)
        blackboard.post_fact(
            f"tool:{observation.call_id}", payload,
            source_agent=f"TOOL:{observation.tool_name}",
        )
        evidence_ledger.append(EvidenceItem(
            claim=f"Tool {observation.tool_name} returned status {observation.status}",
            source=f"tool://{observation.tool_name}",
            provenance=observation.provenance_hash,
            confidence=1.0 if observation.status == "COMPLETED" else 0.0,
            metadata={"call_id": observation.call_id, "observation": payload},
        ))

    @staticmethod
    def _observation(
        call: ToolCall,
        status: str,
        attempts: int,
        arguments: Dict[str, Any],
        output: Any = None,
        error: Optional[str] = None,
        latency_ms: float = 0.0,
    ) -> ToolObservation:
        manifest = json.dumps(
            {"call_id": call.call_id, "tool": call.tool_name, "arguments": arguments, "output": output, "status": status},
            sort_keys=True,
            default=str,
        )
        return ToolObservation(
            call_id=call.call_id,
            tool_name=call.tool_name,
            status=status,
            attempts=attempts,
            arguments=arguments,
            output=output,
            error=error,
            latency_ms=round(latency_ms, 3),
            provenance_hash=hashlib.sha256(manifest.encode("utf-8")).hexdigest(),
        )

    @classmethod
    def _resolve_references(
        cls,
        value: Any,
        outputs: Mapping[str, Any],
        case_context: Mapping[str, Any],
    ) -> Any:
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            expression = value[2:-1]
            root, _, path = expression.partition(".")
            if root == "case":
                return cls._read_path(case_context, path)
            if root not in outputs:
                raise KeyError(f"unresolved tool reference: {expression}")
            return cls._read_path(outputs[root], path) if path else outputs[root]
        if isinstance(value, list):
            return [cls._resolve_references(item, outputs, case_context) for item in value]
        if isinstance(value, Mapping):
            return {key: cls._resolve_references(item, outputs, case_context) for key, item in value.items()}
        return value

    @staticmethod
    def _read_path(value: Any, path: str) -> Any:
        current = value
        if not path:
            return current
        for part in path.split("."):
            if isinstance(current, Mapping) and part in current:
                current = current[part]
            elif isinstance(current, Sequence) and not isinstance(current, (str, bytes)) and part.isdigit():
                current = current[int(part)]
            else:
                raise KeyError(f"path not found: {path}")
        return current

    @classmethod
    def _evaluate(
        cls,
        expectations: Sequence[Mapping[str, Any]],
        outputs: Mapping[str, Any],
        observations: Sequence[ToolObservation],
    ) -> TaskEvaluation:
        if not expectations:
            passed = bool(observations) and all(obs.status == "COMPLETED" for obs in observations)
            return TaskEvaluation(passed, 1.0 if passed else 0.0, reason="all planned calls completed" if passed else "tool plan incomplete")
        checks: List[EvaluationCheck] = []
        for expectation in expectations:
            path = str(expectation.get("path") or "")
            operator = str(expectation.get("operator") or "eq")
            expected = expectation.get("value")
            try:
                actual = cls._read_path(outputs, path)
                passed = _evaluate_operator(actual, operator, expected, float(expectation.get("tolerance") or 1e-9))
            except (KeyError, TypeError, ValueError):
                actual = None
                passed = False
            checks.append(EvaluationCheck(path, operator, expected, actual, passed))
        score = sum(check.passed for check in checks) / len(checks)
        return TaskEvaluation(all(check.passed for check in checks), score, checks, f"{sum(c.passed for c in checks)}/{len(checks)} checks passed")


def _numbers(values: Sequence[Any]) -> List[float]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise TypeError("values must be a non-empty numeric sequence")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric")
    return [float(value) for value in values]


def _math_add(values: Sequence[Any]) -> float:
    return sum(_numbers(values))


def _math_multiply(values: Sequence[Any]) -> float:
    return math.prod(_numbers(values))


def _math_subtract(left: Any, right: Any) -> float:
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in (left, right)):
        raise TypeError("left and right must be numeric")
    return float(left) - float(right)


def _math_divide(numerator: Any, denominator: Any) -> float:
    if isinstance(numerator, bool) or isinstance(denominator, bool):
        raise TypeError("numerator and denominator must be numeric")
    if not isinstance(numerator, (int, float)) or not isinstance(denominator, (int, float)):
        raise TypeError("numerator and denominator must be numeric")
    if denominator == 0:
        raise ZeroDivisionError("denominator cannot be zero")
    return float(numerator) / float(denominator)


def _math_power(base: Any, exponent: Any) -> float:
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in (base, exponent)):
        raise TypeError("base and exponent must be numeric")
    if abs(float(exponent)) > 12:
        raise ValueError("absolute exponent exceeds safe bound of 12")
    result = float(base) ** float(exponent)
    if not math.isfinite(result):
        raise ValueError("power result is not finite")
    return result


def _compare(left: Any, operator: str, right: Any) -> bool:
    return _evaluate_operator(left, operator, right, 1e-9)


def _select(data: Mapping[str, Any], path: str) -> Any:
    if not isinstance(data, Mapping):
        raise TypeError("data must be an object")
    return AutonomousToolLoop._read_path(data, path)


def _evaluate_operator(actual: Any, operator: str, expected: Any, tolerance: float) -> bool:
    if operator == "eq":
        return actual == expected
    if operator == "approx":
        return isinstance(actual, (int, float)) and isinstance(expected, (int, float)) and abs(actual - expected) <= tolerance
    if operator == "gt":
        return actual > expected
    if operator == "gte":
        return actual >= expected
    if operator == "lt":
        return actual < expected
    if operator == "lte":
        return actual <= expected
    if operator == "contains":
        return expected in actual
    if operator == "is_number":
        return isinstance(actual, (int, float)) and not isinstance(actual, bool) and math.isfinite(float(actual))
    if operator == "nonempty":
        return actual is not None and hasattr(actual, "__len__") and len(actual) > 0
    raise ValueError(f"unsupported evaluation operator: {operator}")
