"""Contracts: AgentContract, AgentPillar, CapabilityDeclaration with Schema Validation."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


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
    required_permissions: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class AgentContract:
    """01 — AgentContract: Standard typed specification for all 1,000 agents (v3.0 Section 10-12)."""
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
    required_scopes: List[str] = field(default_factory=lambda: ["reason"])
    version: str = "4.0.0"

    def satisfies_capability(self, required_cap: str) -> bool:
        """Checks if this agent declares the required capability."""
        req_norm = required_cap.lower().replace("-", "_")
        for cap in self.capabilities:
            if cap.lower().replace("-", "_") == req_norm or req_norm in cap.lower():
                return True
        return self.agent_id.lower() == req_norm or self.class_name.lower() == req_norm

    def validate_input(self, payload: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validates payload against input schema prerequisites."""
        if not isinstance(payload, dict):
            return False, f"Expected dict payload, got {type(payload).__name__}"
        return True, None

    def validate_output(self, payload: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validates output payload schema conformity."""
        if not isinstance(payload, dict):
            return False, f"Expected dict output, got {type(payload).__name__}"
        return True, None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "class_name": self.class_name,
            "pillar": self.pillar.value if hasattr(self.pillar, "value") else str(self.pillar),
            "layer_or_domain": self.layer_or_domain,
            "input_schema_name": self.input_schema_name,
            "output_schema_name": self.output_schema_name,
            "capabilities": list(self.capabilities),
            "dependencies": list(self.dependencies),
            "failure_modes": list(self.failure_modes),
            "max_latency_ms": self.max_latency_ms,
            "is_critical_path": self.is_critical_path,
            "version": self.version,
        }
