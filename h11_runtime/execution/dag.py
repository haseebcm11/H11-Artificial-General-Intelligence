"""Execution Directed Acyclic Graph (DAG) with Topological Ordering and Layering."""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import uuid


@dataclass
class DAGNode:
    node_id: str
    agent_id: str
    capability: str = ""
    status: str = "PENDING"  # PENDING, READY, RUNNING, COMPLETED, FAILED, SKIPPED
    result: Optional[Any] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    critical_path: bool = False
    retry_count: int = 0
    max_retries: int = 2


@dataclass
class DAGEdge:
    source: str
    target: str
    edge_type: str = "DATA"  # DATA, CONTROL, DEPENDENCY, GOVERNANCE
    schema: Optional[str] = None
    transform_fn: Optional[Callable[[Any], Any]] = None


class ExecutionDAG:
    """Directed Acyclic Graph orchestrating multi-agent execution topology (v3.0 Section 20)."""

    def __init__(self, dag_id: str = "") -> None:
        self.dag_id = dag_id or f"DAG-{uuid.uuid4().hex[:8].upper()}"
        self.nodes: Dict[str, DAGNode] = {}
        self.edges: List[DAGEdge] = []
        self._in_degree: Dict[str, int] = {}
        self._adj: Dict[str, List[str]] = {}
        self._rev_adj: Dict[str, List[str]] = {}

    def add_node(
        self,
        agent_id: str,
        node_id: str = "",
        capability: str = "",
        max_retries: int = 2,
    ) -> DAGNode:
        actual_id = node_id or f"NODE-{agent_id}"
        node = DAGNode(
            node_id=actual_id,
            agent_id=agent_id,
            capability=capability or agent_id,
            max_retries=max_retries,
        )
        self.nodes[actual_id] = node
        self._adj.setdefault(actual_id, [])
        self._rev_adj.setdefault(actual_id, [])
        self._in_degree[actual_id] = 0
        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str = "DATA",
        schema: Optional[str] = None,
    ) -> DAGEdge:
        if source_id not in self.nodes:
            self.add_node(agent_id=source_id, node_id=source_id)
        if target_id not in self.nodes:
            self.add_node(agent_id=target_id, node_id=target_id)

        edge = DAGEdge(source=source_id, target=target_id, edge_type=edge_type, schema=schema)
        self.edges.append(edge)
        self._adj[source_id].append(target_id)
        self._rev_adj[target_id].append(source_id)
        self._in_degree[target_id] = self._in_degree.get(target_id, 0) + 1
        return edge

    def has_cycle(self) -> bool:
        """Kahn's cycle detection algorithm."""
        in_deg = dict(self._in_degree)
        queue = [n for n, deg in in_deg.items() if deg == 0]
        visited_count = 0

        while queue:
            node = queue.pop(0)
            visited_count += 1
            for neighbor in self._adj.get(node, []):
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count != len(self.nodes)

    def get_topological_order(self) -> List[str]:
        """Returns node IDs sorted topologically in valid dependency order."""
        if self.has_cycle():
            raise ValueError(f"Cycle detected in ExecutionDAG {self.dag_id}")

        in_deg = dict(self._in_degree)
        queue = [n for n, deg in in_deg.items() if deg == 0]
        order = []

        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in self._adj.get(node, []):
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        return order

    def get_parallel_layers(self) -> List[List[str]]:
        """Partitions DAG into successive parallel execution stages (frontiers)."""
        if self.has_cycle():
            raise ValueError(f"Cycle detected in ExecutionDAG {self.dag_id}")

        in_deg = dict(self._in_degree)
        current_layer = [n for n, deg in in_deg.items() if deg == 0]
        layers = []

        while current_layer:
            layers.append(current_layer)
            next_layer = []
            for node in current_layer:
                for neighbor in self._adj.get(node, []):
                    in_deg[neighbor] -= 1
                    if in_deg[neighbor] == 0:
                        next_layer.append(neighbor)
            current_layer = next_layer

        return layers

    def get_prerequisites(self, node_id: str) -> List[str]:
        return self._rev_adj.get(node_id, [])

    def get_dependents(self, node_id: str) -> List[str]:
        return self._adj.get(node_id, [])

    def compute_fingerprint(self) -> str:
        """Computes deterministic SHA-256 hash of DAG structure."""
        manifest = {
            "nodes": sorted([{"id": n.node_id, "agent": n.agent_id} for n in self.nodes.values()], key=lambda x: x["id"]),
            "edges": sorted([{"s": e.source, "t": e.target, "type": e.edge_type} for e in self.edges], key=lambda x: (x["s"], x["t"])),
        }
        encoded = json.dumps(manifest, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
