"""3. Dependency Graph."""
from __future__ import annotations

from typing import Dict, List, Optional, Set


class DependencyGraph:
    """3. Dependency Graph: Resolves what must execute before something else with cycle detection."""

    def __init__(self) -> None:
        self.adjacency: Dict[str, Set[str]] = {}  # target -> dependencies (prerequisites)

    def add_dependency(self, target: str, prerequisite: str) -> None:
        if target not in self.adjacency:
            self.adjacency[target] = set()
        if prerequisite not in self.adjacency:
            self.adjacency[prerequisite] = set()
        self.adjacency[target].add(prerequisite)

    def topological_sort(self, subset: Optional[Set[str]] = None) -> List[str]:
        """Return a valid execution order or raise ValueError on cycle."""
        nodes = set(subset) if subset is not None else set(self.adjacency.keys())
        for n in list(nodes):
            nodes.update(self.adjacency.get(n, set()))

        in_degree: Dict[str, int] = {n: 0 for n in nodes}
        dependents: Dict[str, List[str]] = {n: [] for n in nodes}

        for node in nodes:
            prereqs = self.adjacency.get(node, set()) & nodes
            in_degree[node] = len(prereqs)
            for p in prereqs:
                dependents[p].append(node)

        queue = [n for n, deg in in_degree.items() if deg == 0]
        order: List[str] = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for dep in dependents.get(curr, []):
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)

        if len(order) < len(nodes):
            raise ValueError(f"Dependency cycle detected among nodes: {nodes - set(order)}")
        return order
