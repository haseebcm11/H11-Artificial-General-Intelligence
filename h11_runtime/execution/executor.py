"""Graph executor."""
from __future__ import annotations

from typing import Any, Callable, Dict, List

from ..case import Case, CaseState
from ..contracts import AgentResult


class GraphExecutor:
    """06 — GraphExecutor: Topological DAG executor."""

    def execute_graph(
        self,
        case: Case,
        graph: Any,
        agent_executors: Dict[str, Callable[[Any], Any]],
    ) -> Dict[str, AgentResult]:
        case.transition_to(CaseState.EXECUTING, "Beginning graph topological execution")
        results: Dict[str, AgentResult] = {}

        if hasattr(graph, "get_execution_order"):
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

            try:
                res = executor_fn(case.blackboard)
                node.status = "COMPLETED"
                node.result = res

                if isinstance(res, dict):
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        success=True,
                        data=res,
                        confidence=res.get("confidence", 1.0),
                    )
                elif isinstance(res, AgentResult):
                    agent_res = res
                else:
                    agent_res = AgentResult(
                        agent_id=agent_id,
                        success=True,
                        data=res,
                    )

                results[agent_id] = agent_res
                case.blackboard.post_result(agent_id, agent_res)

            except Exception as e:
                node.status = "FAILED"
                agent_res = AgentResult(
                    agent_id=agent_id,
                    success=False,
                    data=None,
                    error_message=str(e),
                )
                results[agent_id] = agent_res
                case.blackboard.post_result(agent_id, agent_res)

        case.transition_to(CaseState.INTEGRATING, "Completed graph node executions")
        return results
