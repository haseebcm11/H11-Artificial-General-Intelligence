"""Governed execution of MoE-selected specialist agents.

Selection is not execution.  This coordinator loads only explicitly routed
repository agents, constructs inputs from declared Python signatures, enforces
timeouts, and records skipped/failed nodes without manufacturing outputs.
"""
from __future__ import annotations

import asyncio
import dataclasses
import inspect
import time
from dataclasses import dataclass, field
from enum import Enum
from types import ModuleType
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from ..case.blackboard import Blackboard
from ..contracts import AgentResult
from ..graph.execution_graph import ExecutionGraph, ExecutionNode
from ..loader import load_module
from .contract_compiler import ContractCompilationError, SpecialistContractCompiler


@dataclass
class SpecialistExecutionRecord:
    agent_id: str
    status: str
    output: Optional[Any] = None
    error: Optional[str] = None
    missing_inputs: List[str] = field(default_factory=list)
    input_fields: List[str] = field(default_factory=list)
    latency_ms: float = 0.0
    schema_note: str = "python_signature"
    contract_diagnostics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


class InputUnavailable(ValueError):
    def __init__(self, missing: Sequence[str]) -> None:
        self.missing = list(missing)
        super().__init__("missing required specialist inputs: " + ", ".join(self.missing))


def _json_safe(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {k: _json_safe(v) for k, v in dataclasses.asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "__dict__"):
        return {k: _json_safe(v) for k, v in vars(value).items() if not k.startswith("_")}
    return str(value)


class SpecialistExecutionCoordinator:
    """Executes a bounded specialist collective with fail-closed input binding."""

    EXECUTION_METHODS = ("process", "process_request", "run", "execute")

    def __init__(self, timeout_seconds: float = 2.0, max_concurrent: int = 6) -> None:
        self.timeout_seconds = timeout_seconds
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self.contract_compiler = SpecialistContractCompiler()

    async def execute(
        self,
        selected_agent_ids: Sequence[str],
        metadata: Mapping[str, Any],
        case: Dict[str, Any],
        graph: ExecutionGraph,
        blackboard: Blackboard,
    ) -> List[SpecialistExecutionRecord]:
        tasks = []
        for routed_id in selected_agent_ids:
            meta = metadata.get(routed_id)
            node = self._find_node(graph, routed_id)
            tasks.append(self._execute_one(routed_id, meta, case, node, blackboard))
        return list(await asyncio.gather(*tasks)) if tasks else []

    @staticmethod
    def _find_node(graph: ExecutionGraph, routed_id: str) -> Optional[ExecutionNode]:
        return next((node for node in graph.nodes.values() if node.agent_id == routed_id), None)

    async def _execute_one(
        self,
        routed_id: str,
        meta: Any,
        case: Dict[str, Any],
        node: Optional[ExecutionNode],
        blackboard: Blackboard,
    ) -> SpecialistExecutionRecord:
        started = time.perf_counter()
        if node:
            node.status = "RUNNING"
            node.started_at = time.time()
        try:
            if meta is None or not getattr(meta, "relative_path", None):
                raise InputUnavailable(["agent_metadata"])
            module = load_module(f"specialist_{routed_id}", meta.relative_path)
            instance, method = self._resolve_executable(module, getattr(meta, "agent_id", routed_id))
            compiled = self.contract_compiler.compile(
                method=method,
                case=case,
                blackboard=blackboard,
                relative_agent_path=meta.relative_path,
            )
            async with self._semaphore:
                result = await asyncio.wait_for(
                    self._invoke(method, compiled.args, compiled.kwargs),
                    timeout=self.timeout_seconds,
                )
            normalized = _json_safe(result)
            if isinstance(normalized, dict) and normalized.get("error"):
                raise RuntimeError(str(normalized["error"]))
            record = SpecialistExecutionRecord(
                agent_id=routed_id,
                status="COMPLETED",
                output=normalized,
                input_fields=compiled.diagnostics.bound_fields,
                contract_diagnostics=compiled.diagnostics.to_dict(),
            )
        except ContractCompilationError as exc:
            record = SpecialistExecutionRecord(
                agent_id=routed_id,
                status="SKIPPED",
                error=str(exc),
                missing_inputs=exc.missing,
                contract_diagnostics=exc.diagnostics.to_dict() if exc.diagnostics else {},
            )
        except InputUnavailable as exc:
            record = SpecialistExecutionRecord(
                agent_id=routed_id,
                status="SKIPPED",
                error=str(exc),
                missing_inputs=exc.missing,
            )
        except asyncio.TimeoutError:
            record = SpecialistExecutionRecord(
                agent_id=routed_id,
                status="TIMED_OUT",
                error=f"specialist exceeded {self.timeout_seconds:.2f}s timeout",
            )
        except Exception as exc:
            record = SpecialistExecutionRecord(
                agent_id=routed_id,
                status="FAILED",
                error=f"{type(exc).__name__}: {exc}",
            )

        record.latency_ms = round((time.perf_counter() - started) * 1000.0, 3)
        if node:
            node.status = record.status
            node.result = record.output
            node.error = record.error
            node.completed_at = time.time()
            node.latency_ms = record.latency_ms

        agent_result = AgentResult(
            agent_id=routed_id,
            success=record.status == "COMPLETED",
            data=record.output,
            error_message=record.error,
            latency_ms=record.latency_ms,
        )
        blackboard.post_result(routed_id, agent_result)
        if record.status == "COMPLETED":
            blackboard.post_fact(
                f"specialist:{routed_id}",
                record.output,
                source_agent=routed_id,
            )
        return record

    def _resolve_executable(self, module: ModuleType, agent_id: str) -> Tuple[Any, Callable[..., Any]]:
        candidates = [
            cls for _, cls in inspect.getmembers(module, inspect.isclass)
            if cls.__module__ == module.__name__
            and any(callable(getattr(cls, name, None)) for name in self.EXECUTION_METHODS)
        ]
        if not candidates:
            raise InputUnavailable(["executable_agent_class"])
        candidates.sort(key=lambda cls: (not cls.__name__.lower().endswith("agent"), cls.__name__))
        last_error: Optional[Exception] = None
        for cls in candidates:
            try:
                init_sig = inspect.signature(cls)
                init_kwargs: Dict[str, Any] = {}
                missing = []
                for param in init_sig.parameters.values():
                    if param.name == "agent_id":
                        init_kwargs[param.name] = agent_id
                    elif param.default is inspect.Parameter.empty and param.kind not in (
                        inspect.Parameter.VAR_POSITIONAL,
                        inspect.Parameter.VAR_KEYWORD,
                    ):
                        missing.append(param.name)
                if missing:
                    continue
                instance = cls(**init_kwargs)
                for method_name in self.EXECUTION_METHODS:
                    method = getattr(instance, method_name, None)
                    if callable(method):
                        return instance, method
            except Exception as exc:
                last_error = exc
        if last_error:
            raise RuntimeError(f"could not instantiate specialist: {last_error}")
        raise InputUnavailable(["constructible_agent_class"])

    @staticmethod
    async def _invoke(method: Callable[..., Any], args: List[Any], kwargs: Dict[str, Any]) -> Any:
        if inspect.iscoroutinefunction(method):
            return await method(*args, **kwargs)
        return await asyncio.to_thread(method, *args, **kwargs)
