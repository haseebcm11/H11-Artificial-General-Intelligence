"""Capability Registry with Fuzzy Matching, Composite Resolution, and Fallbacks."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set

from .agent_registry import AgentRegistry

logger = logging.getLogger(__name__)


class CapabilityRegistry:
    """04 — CapabilityRegistry: Maps semantic capabilities to specialist agents (v3.0 Section 14)."""

    def __init__(self, agent_registry: Optional[AgentRegistry] = None) -> None:
        self.cap_to_agents: Dict[str, Set[str]] = {}
        self.agent_to_caps: Dict[str, Set[str]] = {}
        self.capability_descriptions: Dict[str, str] = {}
        self.capability_hierarchy: Dict[str, List[str]] = {}  # Parent -> [Children]

        if agent_registry:
            self.index_agent_registry(agent_registry)

    def index_agent_registry(self, agent_registry: AgentRegistry) -> None:
        """Indexes all agents and declared capabilities from an AgentRegistry."""
        for agent_id, agent_obj in agent_registry.agents.items():
            caps = getattr(agent_obj, "capabilities", [])
            for c in caps:
                self.register_capability(c, agent_id)

    def register_capability(
        self,
        capability: str,
        provider_agent_id: str,
        description: str = "",
    ) -> None:
        norm_cap = capability.lower().strip()
        self.cap_to_agents.setdefault(norm_cap, set()).add(provider_agent_id)
        self.agent_to_caps.setdefault(provider_agent_id, set()).add(norm_cap)
        if description:
            self.capability_descriptions[norm_cap] = description

    def resolve_providers(self, capability: str) -> List[str]:
        """Resolves direct and hierarchical providers for a capability."""
        norm_cap = capability.lower().strip()
        providers = set(self.cap_to_agents.get(norm_cap, set()))

        # Check children capabilities in hierarchy
        for child_cap in self.capability_hierarchy.get(norm_cap, []):
            providers.update(self.cap_to_agents.get(child_cap, set()))

        # Fuzzy substring match fallback if no exact providers found
        if not providers:
            for cap, ags in self.cap_to_agents.items():
                if norm_cap in cap or cap in norm_cap:
                    providers.update(ags)

        return sorted(list(providers))

    def resolve_composite(self, required_capabilities: List[str]) -> Dict[str, List[str]]:
        """Resolves providers for a set of required capabilities simultaneously."""
        return {cap: self.resolve_providers(cap) for cap in required_capabilities}

    def list_all_capabilities(self) -> List[str]:
        return sorted(list(self.cap_to_agents.keys()))
