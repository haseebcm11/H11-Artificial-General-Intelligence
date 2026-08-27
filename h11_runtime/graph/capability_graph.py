"""2. Capability Graph (Cap A -> Cap B -> Cap C)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set


@dataclass
class CapabilityNode:
    capability_name: str
    description: str
    required_preconditions: Set[str] = field(default_factory=set)
    produced_effects: Set[str] = field(default_factory=set)


class CapabilityGraph:
    """2. Capability Graph: Maps which capabilities depend on or enable other capabilities."""

    def __init__(self) -> None:
        self.nodes: Dict[str, CapabilityNode] = {}
        self.dependencies: Dict[str, Set[str]] = {}

    def add_capability(
        self,
        name: str,
        description: str = "",
        requires: Optional[Set[str]] = None,
        produces: Optional[Set[str]] = None,
    ) -> CapabilityNode:
        node = CapabilityNode(
            capability_name=name,
            description=description,
            required_preconditions=requires or set(),
            produced_effects=produces or set(),
        )
        self.nodes[name] = node
        self.dependencies[name] = set(requires or set())
        return node

    def resolve_capability_closure(self, required_capabilities: Set[str]) -> Set[str]:
        """Compute complete transitive dependency closure for given capabilities."""
        closure = set(required_capabilities)
        added = True
        while added:
            current_len = len(closure)
            for cap in list(closure):
                deps = self.dependencies.get(cap, set())
                closure.update(deps)
            added = len(closure) > current_len
        return closure
