"""Capability Registry."""
from __future__ import annotations

from typing import Dict, List, Optional, Set

from .agent_registry import AgentRegistry


class CapabilityRegistry:
    """04 — CapabilityRegistry: Maps capabilities to provider agents."""

    def __init__(self, agent_registry: Optional[AgentRegistry] = None) -> None:
        self.cap_to_agents: Dict[str, Set[str]] = {}
        if agent_registry:
            for agent_id, agent_obj in agent_registry.agents.items():
                caps = getattr(agent_obj, "capabilities", [])
                for c in caps:
                    self.register_capability(c, agent_id)

    def register_capability(self, capability: str, provider_agent_id: str) -> None:
        if capability not in self.cap_to_agents:
            self.cap_to_agents[capability] = set()
        self.cap_to_agents[capability].add(provider_agent_id)

    def resolve_providers(self, capability: str) -> List[str]:
        return sorted(list(self.cap_to_agents.get(capability, set())))
