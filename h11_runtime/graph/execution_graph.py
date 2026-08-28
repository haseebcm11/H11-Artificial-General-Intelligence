"""4. Execution Graph (Typed DAG with Validation, Cycle Detection, and Parallel Layering)."""
from __future__ import annotations

import collections
from dataclasses import dataclass, field
import enum
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import uuid

from .types import EdgeType


class CycleDetectedError(Exception):
    """Raised when an illegal cycle is detected in an ExecutionGraph."""
    pass


class ValidationError(Exception):
    """Raised when node schemas or dependencies fail validation."""
    pass


@dataclass
class ExecutionNode:
    """Executable node in an active ExecutionGraph."""
    node_id: str
    agent_id: str
    canonical_id: str = ""
    capability: str = ""
    input_contract: Dict[str, Any] = field(default_factory=dict)
    output_contract: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    status: str = "PENDING"  # PENDING, QUEUED, RUNNING, COMPLETED, FAILED, SKIPPED
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    latency_ms: float = 0.0

    @property
    def is_finished(self) -> bool:
        return self.status in ("COMPLETED", "FAILED", "SKIPPED")


@dataclass
class ExecutionEdge:
    """Explicitly typed directed edge in an ExecutionGraph."""
    source_node: str
    target_node: str
    edge_type: EdgeType = EdgeType.DATA  # DATA, DEPENDENCY, CONTROL, GOVERNANCE
    schema: Optional[str] = None
    transform_fn: Optional[Callable[[Any], Any]] = None
    data_payload: Optional[Any] = None


class ExecutionGraph:
    """4. Execution Graph: Authoritative Typed DAG representing the active cognitive execution plan."""

    def __init__(self, case_id: str = "", graph_id: str = "") -> None:
        self.case_id = case_id
        self.graph_id = graph_id or f"GRAPH-{uuid.uuid4().hex[:8].upper()}"
        self.nodes: Dict[str, ExecutionNode] = {}
        self.edges: List[ExecutionEdge] = []
        self.in_edges: Dict[str, List[ExecutionEdge]] = {}
        self.out_edges: Dict[str, List[ExecutionEdge]] = {}
        self.allow_cycles: bool = False

    def add_node(
        self,
        agent_id: str,
        node_id: str = "",
        canonical_id: str = "",
        capability: str = "",
        input_contract: Optional[Dict[str, Any]] = None,
        output_contract: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[str]] = None,
    ) -> ExecutionNode:
        actual_node_id = node_id or f"NODE-{agent_id.replace(':', '_')}"
        node = ExecutionNode(
            node_id=actual_node_id,
            agent_id=agent_id,
            canonical_id=canonical_id or agent_id,
            capability=capability or agent_id,
            input_contract=input_contract or {},
            output_contract=output_contract or {},
            dependencies=dependencies or [],
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

        # Record explicit dependency on target node
        if target_id in self.nodes and source_id not in self.nodes[target_id].dependencies:
            self.nodes[target_id].dependencies.append(source_id)

        return edge

    def get_prerequisites(self, node_id: str) -> List[str]:
        return [e.source_node for e in self.in_edges.get(node_id, [])]

    def get_dependents(self, node_id: str) -> List[str]:
        return [e.target_node for e in self.out_edges.get(node_id, [])]

    def validate_graph(self) -> bool:
        """Validates all nodes, schemas, and detects cycles."""
        for nid, node in self.nodes.items():
            if not node.agent_id:
                raise ValidationError(f"Node {nid} has empty agent_id")
            for prereq in node.dependencies:
                if prereq not in self.nodes:
                    raise ValidationError(f"Node {nid} depends on unknown node {prereq}")

        # Kahn's Cycle Detection
        in_degrees = {nid: len(self.in_edges.get(nid, [])) for nid in self.nodes}
        queue = [nid for nid, deg in in_degrees.items() if deg == 0]
        visited = 0

        while queue:
            curr = queue.pop(0)
            visited += 1
            for edge in self.out_edges.get(curr, []):
                tgt = edge.target_node
                in_degrees[tgt] -= 1
                if in_degrees[tgt] == 0:
                    queue.append(tgt)

        if visited != len(self.nodes) and not self.allow_cycles:
            raise CycleDetectedError(f"Illegal cycle detected in ExecutionGraph {self.graph_id} (visited {visited}/{len(self.nodes)} nodes)")

        return True

    def get_execution_order(self) -> List[str]:
        """Topological sort returning node_ids in strict dependency order."""
        self.validate_graph()
        in_degrees = {nid: len(self.in_edges.get(nid, [])) for nid in self.nodes}
        dependents = {nid: [e.target_node for e in self.out_edges.get(nid, [])] for nid in self.nodes}

        queue = [nid for nid, deg in in_degrees.items() if deg == 0]
        order: List[str] = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for dep in dependents.get(curr, []):
                in_degrees[dep] -= 1
                if in_degrees[dep] == 0:
                    queue.append(dep)

        return order

    def get_parallel_stages(self) -> List[List[str]]:
        """Extracts parallel frontier layers of independent nodes that can execute concurrently."""
        self.validate_graph()
        in_degrees = {nid: len(self.in_edges.get(nid, [])) for nid in self.nodes}
        dependents = {nid: [e.target_node for e in self.out_edges.get(nid, [])] for nid in self.nodes}

        current_frontier = [nid for nid, deg in in_degrees.items() if deg == 0]
        stages: List[List[str]] = []

        while current_frontier:
            stages.append(list(current_frontier))
            next_frontier = []
            for nid in current_frontier:
                for dep in dependents.get(nid, []):
                    in_degrees[dep] -= 1
                    if in_degrees[dep] == 0:
                        next_frontier.append(dep)
            current_frontier = next_frontier

        return stages

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "case_id": self.case_id,
            "nodes_count": len(self.nodes),
            "edges_count": len(self.edges),
            "nodes": {nid: {"agent_id": n.agent_id, "status": n.status, "latency_ms": n.latency_ms} for nid, n in self.nodes.items()},
            "edges": [{"source": e.source_node, "target": e.target_node, "type": e.edge_type.name} for e in self.edges],
        }
