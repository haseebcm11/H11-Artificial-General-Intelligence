"""4. Execution Graph (Typed DAG)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set
import uuid

from .types import EdgeType


@dataclass
class ExecutionNode:
    node_id: str
    agent_id: str
    capability: str = ""
    input_contract: str = ""
    output_contract: str = ""
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED, SKIPPED
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class ExecutionEdge:
    source_node: str
    target_node: str
    edge_type: EdgeType = EdgeType.DATA
    schema: Optional[str] = None
    transform_fn: Optional[Callable[[Any], Any]] = None


class ExecutionGraph:
    """4. Execution Graph: Typed DAG representing the active case execution plan."""

    def __init__(self, case_id: str = "", graph_id: str = "") -> None:
        self.case_id = case_id
        self.graph_id = graph_id or f"GRAPH-{uuid.uuid4().hex[:8]}"
        self.nodes: Dict[str, ExecutionNode] = {}
        self.edges: List[ExecutionEdge] = []
        self.in_edges: Dict[str, List[ExecutionEdge]] = {}
        self.out_edges: Dict[str, List[ExecutionEdge]] = {}

    def add_node(
        self,
        agent_id: str,
        node_id: str = "",
        capability: str = "",
        input_contract: str = "",
        output_contract: str = "",
    ) -> ExecutionNode:
        actual_node_id = node_id or f"NODE-{agent_id}"
        node = ExecutionNode(
            node_id=actual_node_id,
            agent_id=agent_id,
            capability=capability or agent_id,
            input_contract=input_contract,
            output_contract=output_contract,
        )
        self.nodes[actual_node_id] = node
        self.in_edges[actual_node_id] = []
        self.out_edges[actual_node_id] = []
        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: EdgeType = EdgeType.DATA,
        schema: Optional[str] = None,
        transform_fn: Optional[Callable[[Any], Any]] = None,
    ) -> ExecutionEdge:
        edge = ExecutionEdge(
            source_node=source_id,
            target_node=target_id,
            edge_type=edge_type,
            schema=schema,
            transform_fn=transform_fn,
        )
        self.edges.append(edge)
        if source_id not in self.out_edges:
            self.out_edges[source_id] = []
        if target_id not in self.in_edges:
            self.in_edges[target_id] = []
        self.out_edges[source_id].append(edge)
        self.in_edges[target_id].append(edge)
        return edge

    def get_prerequisites(self, node_id: str) -> List[str]:
        return [e.source_node for e in self.in_edges.get(node_id, [])]

    def get_dependents(self, node_id: str) -> List[str]:
        return [e.target_node for e in self.out_edges.get(node_id, [])]

    def get_execution_order(self) -> List[str]:
        """Topological sort returning node_ids in dependency order."""
        nodes = set(self.nodes.keys())
        in_degree: Dict[str, int] = {n: 0 for n in nodes}
        dependents: Dict[str, List[str]] = {n: [] for n in nodes}

        for edge in self.edges:
            if edge.source_node in nodes and edge.target_node in nodes:
                in_degree[edge.target_node] += 1
                dependents[edge.source_node].append(edge.target_node)

        queue = [n for n, deg in in_degree.items() if deg == 0]
        order: List[str] = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for dep in dependents.get(curr, []):
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)

        return order if len(order) == len(nodes) else list(self.nodes.keys())
