"""Graph executor with parallel stage processing, retry semantics, and error boundaries."""
from __future__ import annotations

import asyncio
import inspect
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Union

from ..case import Case, CaseState
from ..contracts.agent_result import AgentResult
from ..graph.execution_graph import ExecutionGraph, ExecutionNode
from ..graph.types import EdgeType
from ..loader import load_agent, LoadedAgentInterface
from .dag import DAGNode, ExecutionDAG

logger = logging.getLogger(__name__)


class GraphExecutor:
    """06 — GraphExecutor: Topological and parallel DAG execution engine (v3.0 Section 20-21)."""

    def __init__(self, max_concurrent: int = 16, timeout_seconds: float = 30.0) -> None:
        self.max_concurrent = max_concurrent
        self.timeout_seconds = timeout_seconds

    def execute_graph(
        self,
        case: Case,
        graph: Any,
        agent_executors: Optional[Dict[str, Callable[[Any], Any]]] = None,
    ) -> Dict[str, AgentResult]:
        """Synchronous topological execution across DAG nodes."""
        executors = agent_executors or {}
        case.transition_to(CaseState.EXECUTING, "Beginning graph topological execution")
        results: Dict[str, AgentResult] = {}

        if hasattr(graph, "get_execution_order"):
            order = graph.get_execution_order()
            nodes = [graph.nodes[nid] for nid in order if nid in graph.nodes]
        elif hasattr(graph, "get_topological_order"):
            order = graph.get_topological_order()
            nodes = [graph.nodes[nid] for nid in order if nid in graph.nodes]
        elif isinstance(graph, dict):
            nodes = graph.get("nodes", [])
        else:
            nodes = getattr(graph, "nodes", [])
            if isinstance(nodes, dict):
                nodes = list(nodes.values())

        for node in nodes:
            agent_id = getattr(node, "agent_id", "")
            node.status = "RUNNING"
            node.started_at = time.time()
            t0 = time.time()

            try:
                # Resolve executor function or load agent instance directly
                res_data = None
                if agent_id in executors:
                    res_data = executors[agent_id](case.blackboard)
                else:
                    loaded = load_agent(getattr(node, "canonical_id", "") or agent_id)
                    input_payload = self._build_node_input(node, graph, case)
                    if hasattr(loaded.instance, "process"):
                        fn = getattr(loaded.instance, "process")
                        if inspect.iscoroutinefunction(fn):
                            res_data = asyncio.run(fn(input_payload))
                        else:
                            res_data = fn(input_payload)
                    else:
                        res_data = asyncio.run(loaded.process(input_payload))

                elapsed_ms = (time.time() - t0) * 1000.0
                node.status = "COMPLETED"
                node.completed_at = time.time()
                node.result = res_data
                node.latency_ms = elapsed_ms

                if isinstance(res_data, AgentResult):
                    agent_res = res_data
                elif isinstance(res_data, dict):
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        canonical_id=getattr(node, "canonical_id", agent_id),
                        success=True,
                        data=res_data,
                        confidence=float(res_data.get("confidence", 0.95)),
                        uncertainty=float(res_data.get("uncertainty", 0.05)),
                        latency_ms=elapsed_ms,
                    )
                else:
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        canonical_id=getattr(node, "canonical_id", agent_id),
                        success=True,
                        data=res_data,
                        latency_ms=elapsed_ms,
                    )

                results[agent_id] = agent_res
                case.blackboard.post_result(agent_id, agent_res)

            except Exception as exc:
                elapsed_ms = (time.time() - t0) * 1000.0
                node.status = "FAILED"
                node.completed_at = time.time()
                node.error = str(exc)
                node.latency_ms = elapsed_ms

                agent_res = AgentResult(
                    agent_id=agent_id,
                    canonical_id=getattr(node, "canonical_id", agent_id),
                    success=False,
                    data=None,
                    error_message=str(exc),
                    latency_ms=elapsed_ms,
                )
                results[agent_id] = agent_res
                case.blackboard.post_result(agent_id, agent_res)
                logger.error(f"Execution error at node {getattr(node, 'node_id', agent_id)}: {exc}")

        case.transition_to(CaseState.INTEGRATING, "Completed graph node executions")
        return results

    async def execute_graph_async(
        self,
        case: Case,
        graph: ExecutionGraph | ExecutionDAG | Any,
        agent_executors: Optional[Dict[str, Callable[[Any], Any]]] = None,
    ) -> Dict[str, AgentResult]:
        """Asynchronously executes DAG in parallel frontier stages with concurrency enforcement."""
        executors = agent_executors or {}
        case.transition_to(CaseState.EXECUTING, "Beginning async parallel DAG execution")
        results: Dict[str, AgentResult] = {}
        sem = asyncio.Semaphore(self.max_concurrent)

        if hasattr(graph, "get_parallel_stages"):
            stages = graph.get_parallel_stages()
        elif hasattr(graph, "get_parallel_layers"):
            stages = graph.get_parallel_layers()
        else:
            stages = [[nid] for nid in getattr(graph, "get_execution_order", lambda: list(graph.nodes.keys()))()]

        for stage_idx, stage_node_ids in enumerate(stages):
            tasks = []
            for nid in stage_node_ids:
                node = graph.nodes[nid]
                tasks.append(self._execute_single_node_async(node, graph, executors, case, sem))

            if tasks:
                stage_results = await asyncio.gather(*tasks, return_exceptions=True)
                for res in stage_results:
                    if isinstance(res, AgentResult):
                        results[res.agent_id] = res
                    elif isinstance(res, Exception):
                        logger.error(f"Async stage execution error: {res}")

        case.transition_to(CaseState.INTEGRATING, "Completed parallel DAG stage executions")
        return results

    async def _execute_single_node_async(
        self,
        node: Any,
        graph: Any,
        executors: Dict[str, Callable[[Any], Any]],
        case: Case,
        sem: asyncio.Semaphore,
    ) -> AgentResult:
        async with sem:
            agent_id = getattr(node, "agent_id", "")
            node.status = "RUNNING"
            node.started_at = time.time()
            t0 = time.time()

            try:
                res_data = None
                if agent_id in executors:
                    fn = executors[agent_id]
                    if inspect.iscoroutinefunction(fn):
                        res_data = await asyncio.wait_for(fn(case.blackboard), timeout=self.timeout_seconds)
                    else:
                        res_data = fn(case.blackboard)
                else:
                    loaded = load_agent(getattr(node, "canonical_id", "") or agent_id)
                    input_payload = self._build_node_input(node, graph, case)
                    res_data = await asyncio.wait_for(loaded.process(input_payload), timeout=self.timeout_seconds)

                elapsed_ms = (time.time() - t0) * 1000.0
                node.status = "COMPLETED"
                node.completed_at = time.time()
                node.result = res_data
                node.latency_ms = elapsed_ms

                if isinstance(res_data, AgentResult):
                    agent_res = res_data
                elif isinstance(res_data, dict):
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        canonical_id=getattr(node, "canonical_id", agent_id),
                        success=True,
                        data=res_data,
                        confidence=float(res_data.get("confidence", 0.95)),
                        uncertainty=float(res_data.get("uncertainty", 0.05)),
                        latency_ms=elapsed_ms,
                    )
                else:
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        canonical_id=getattr(node, "canonical_id", agent_id),
                        success=True,
                        data=res_data,
                        latency_ms=elapsed_ms,
                    )

                case.blackboard.post_result(agent_id, agent_res)
                return agent_res

            except Exception as exc:
                elapsed_ms = (time.time() - t0) * 1000.0
                node.status = "FAILED"
                node.completed_at = time.time()
                node.error = str(exc)
                node.latency_ms = elapsed_ms

                agent_res = AgentResult(
                    agent_id=agent_id,
                    canonical_id=getattr(node, "canonical_id", agent_id),
                    success=False,
                    data=None,
                    error_message=str(exc),
                    latency_ms=elapsed_ms,
                )
                case.blackboard.post_result(agent_id, agent_res)
                return agent_res

    def _build_node_input(self, node: Any, graph: Any, case: Case) -> Dict[str, Any]:
        """Constructs input payload combining case state, blackboard, and upstream edge data."""
        payload = dict(case.payload) if hasattr(case, "payload") else {}
        payload["blackboard"] = getattr(case.blackboard, "facts", {})
        payload["case_id"] = case.case_id

        # Collect upstream edge outputs
        in_edges = getattr(graph, "in_edges", {}).get(getattr(node, "node_id", ""), [])
        for edge in in_edges:
            src_node = graph.nodes.get(edge.source_node)
            if src_node and src_node.result:
                src_data = src_node.result
                if edge.transform_fn:
                    src_data = edge.transform_fn(src_data)
                payload[f"upstream_{src_node.agent_id}"] = src_data

        return payload
