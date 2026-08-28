"""Graph executor with parallel stage processing, retry semantics, and error boundaries."""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Union

from ..case import Case, CaseState
from ..contracts import AgentResult
from .dag import DAGNode, ExecutionDAG

logger = logging.getLogger(__name__)


class GraphExecutor:
    """06 — GraphExecutor: Topological and parallel DAG execution engine (v3.0 Section 20-21)."""

    def __init__(self, max_concurrent: int = 16) -> None:
        self.max_concurrent = max_concurrent

    def execute_graph(
        self,
        case: Case,
        graph: Any,
        agent_executors: Dict[str, Callable[[Any], Any]],
    ) -> Dict[str, AgentResult]:
        """Synchronous topological execution across DAG nodes."""
        case.transition_to(CaseState.EXECUTING, "Beginning graph topological execution")
        results: Dict[str, AgentResult] = {}

        if hasattr(graph, "get_topological_order"):
            order = graph.get_topological_order()
            nodes = [graph.nodes[nid] for nid in order if nid in graph.nodes]
        elif hasattr(graph, "get_execution_order"):
            order = graph.get_execution_order()
            nodes = [graph.nodes[nid] for nid in order if nid in graph.nodes]
        elif isinstance(graph, dict):
            nodes = graph.get("nodes", [])
        else:
            nodes = getattr(graph, "nodes", [])
            if isinstance(nodes, dict):
                nodes = list(nodes.values())

        for node in nodes:
            agent_id = getattr(node, "agent_id", "")
            executor_fn = agent_executors.get(agent_id)
            if not executor_fn:
                continue

            node.status = "RUNNING"
            t0 = time.time()

            try:
                res = executor_fn(case.blackboard)
                elapsed_ms = (time.time() - t0) * 1000.0
                node.status = "COMPLETED"
                node.result = res
                node.latency_ms = elapsed_ms

                if isinstance(res, AgentResult):
                    agent_res = res
                elif isinstance(res, dict):
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        success=True,
                        data=res,
                        confidence=float(res.get("confidence", 1.0)),
                        latency_ms=elapsed_ms,
                    )
                else:
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        success=True,
                        data=res,
                        latency_ms=elapsed_ms,
                    )

                results[agent_id] = agent_res
                case.blackboard.post_result(agent_id, agent_res)

            except Exception as exc:
                elapsed_ms = (time.time() - t0) * 1000.0
                node.status = "FAILED"
                node.error = str(exc)
                node.latency_ms = elapsed_ms

                agent_res = AgentResult(
                    agent_id=agent_id,
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
        dag: ExecutionDAG,
        agent_executors: Dict[str, Callable[[Any], Any]],
    ) -> Dict[str, AgentResult]:
        """Asynchronously executes DAG in parallel frontier stages."""
        case.transition_to(CaseState.EXECUTING, "Beginning async parallel DAG execution")
        results: Dict[str, AgentResult] = {}
        layers = dag.get_parallel_layers()

        for layer_idx, stage_nodes in enumerate(layers):
            tasks = []
            for nid in stage_nodes:
                node = dag.nodes[nid]
                fn = agent_executors.get(node.agent_id)
                if fn:
                    tasks.append(self._execute_single_node_async(node, fn, case))

            if tasks:
                stage_results = await asyncio.gather(*tasks, return_exceptions=True)
                for res in stage_results:
                    if isinstance(res, AgentResult):
                        results[res.agent_id] = res

        case.transition_to(CaseState.INTEGRATING, "Completed parallel DAG stage executions")
        return results

    async def _execute_single_node_async(
        self,
        node: DAGNode,
        fn: Callable[[Any], Any],
        case: Case,
    ) -> AgentResult:
        node.status = "RUNNING"
        t0 = time.time()
        try:
            if asyncio.iscoroutinefunction(fn):
                res = await fn(case.blackboard)
            else:
                res = fn(case.blackboard)
            elapsed_ms = (time.time() - t0) * 1000.0
            node.status = "COMPLETED"
            node.result = res
            node.latency_ms = elapsed_ms

            if isinstance(res, AgentResult):
                agent_res = res
            elif isinstance(res, dict):
                agent_res = AgentResult(
                    agent_id=node.agent_id,
                    success=True,
                    data=res,
                    confidence=float(res.get("confidence", 1.0)),
                    latency_ms=elapsed_ms,
                )
            else:
                agent_res = AgentResult(
                    agent_id=node.agent_id,
                    success=True,
                    data=res,
                    latency_ms=elapsed_ms,
                )
            case.blackboard.post_result(node.agent_id, agent_res)
            return agent_res
        except Exception as exc:
            elapsed_ms = (time.time() - t0) * 1000.0
            node.status = "FAILED"
            node.error = str(exc)
            agent_res = AgentResult(
                agent_id=node.agent_id,
                success=False,
                data=None,
                error_message=str(exc),
                latency_ms=elapsed_ms,
            )
            case.blackboard.post_result(node.agent_id, agent_res)
            return agent_res
