"""1. Agent Graph (Agent -> Capability)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class AgentNode:
    agent_id: str
    pillar: str  # H11Z, H11I, H11C
    layer_or_domain: str
    capabilities: Set[str] = field(default_factory=set)
    input_schema: Optional[str] = None
    output_schema: Optional[str] = None
    status: str = "AVAILABLE"  # AVAILABLE, BUSY, DEGRADED, FAILED, QUARANTINED, DISABLED


class AgentGraph:
    """1. Agent Graph: Maps who exists and what they provide (Agent -> Capability)."""

    def __init__(self) -> None:
        self.nodes: Dict[str, AgentNode] = {}
        self.capability_to_agents: Dict[str, Set[str]] = {}

    def register_agent(
        self,
        agent_id: str,
        pillar: str,
        layer_or_domain: str,
        capabilities: Set[str],
        input_schema: Optional[str] = None,
        output_schema: Optional[str] = None,
    ) -> AgentNode:
        node = AgentNode(
            agent_id=agent_id,
            pillar=pillar,
            layer_or_domain=layer_or_domain,
            capabilities=set(capabilities),
            input_schema=input_schema,
            output_schema=output_schema,
        )
        self.nodes[agent_id] = node
        for cap in capabilities:
            if cap not in self.capability_to_agents:
                self.capability_to_agents[cap] = set()
            self.capability_to_agents[cap].add(agent_id)
        return node

    def get_providers_for_capability(self, capability: str) -> List[AgentNode]:
        agent_ids = self.capability_to_agents.get(capability, set())
        return [self.nodes[aid] for aid in agent_ids if aid in self.nodes]

    def set_agent_status(self, agent_id: str, status: str) -> None:
        if agent_id in self.nodes:
            self.nodes[agent_id].status = status
