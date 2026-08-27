"""Unified system state."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict

from .budget import ResourceBudget


@dataclass
class H11SystemState:
    """Unified system state connecting the three pillars to HAEP v5.0 (Section 51-52)."""
    system_version: str = "3.0"
    runtime_state: str = "OPERATIONAL"  # OPERATIONAL, EVOLVING, DEGRADED, HALTED
    case_state: Dict[str, Any] = field(default_factory=dict)
    cognitive_state: Dict[str, Any] = field(default_factory=dict)  # H11Z / C02
    agent_state: Dict[str, str] = field(default_factory=dict)      # Agent status map
    domain_state: Dict[str, Any] = field(default_factory=dict)     # H11I
    memory_state: Dict[str, Any] = field(default_factory=dict)     # L10
    evidence_state: Dict[str, Any] = field(default_factory=dict)
    resource_budget: ResourceBudget = field(default_factory=ResourceBudget)
    security_state: Dict[str, Any] = field(default_factory=dict)   # C03 / L20
    governance_state: Dict[str, Any] = field(default_factory=dict) # C03 / L17
    alignment_state: Dict[str, Any] = field(default_factory=dict)
    evolution_state: Dict[str, Any] = field(default_factory=dict)  # L21 / H11-OPT / H11-EVO
    last_updated: float = field(default_factory=time.time)

    def update_timestamp(self) -> None:
        self.last_updated = time.time()
