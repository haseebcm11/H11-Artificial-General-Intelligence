"""Contracts: AgentContract, AgentPillar, CapabilityDeclaration."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class AgentPillar(str, Enum):
    H11Z_COGNITIVE_NETWORK = "H11Z_COGNITIVE_NETWORK"
    H11I_INTELLIGENCE_UNIVERSE = "H11I_INTELLIGENCE_UNIVERSE"
    H11C_CONTROL_PLANE = "H11C_CONTROL_PLANE"


@dataclass(frozen=True)
class CapabilityDeclaration:
    name: str
    description: str
    input_type: str
    output_type: str
    deterministic: bool = True
    purity: bool = True


@dataclass(frozen=True)
class AgentContract:
    """01 — AgentContract: Standard typed specification for all 1,000 agents."""
    agent_id: str
    class_name: str
    pillar: AgentPillar
    layer_or_domain: str
    input_schema_name: str
    output_schema_name: str
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    max_latency_ms: float = 1000.0
    is_critical_path: bool = False
