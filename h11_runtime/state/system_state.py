"""Unified system state connecting the three pillars to HAEP v5.0 and telemetry."""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import Any, Dict, List, Optional

from .budget import ResourceBudget


@dataclass
class H11SystemState:
    """Unified system state connecting the three pillars to HAEP v5.0 (v3.0 Section 51-52)."""
    system_version: str = "4.0.0"
    runtime_state: str = "OPERATIONAL"  # OPERATIONAL, EVOLVING, DEGRADED, HALTED
    case_state: Dict[str, Any] = field(default_factory=dict)
    cognitive_state: Dict[str, Any] = field(default_factory=dict)  # H11Z / C02
    agent_state: Dict[str, str] = field(default_factory=dict)      # Agent status map (ID -> STATUS)
    domain_state: Dict[str, Any] = field(default_factory=dict)     # H11I
    memory_state: Dict[str, Any] = field(default_factory=dict)     # L10
    evidence_state: Dict[str, Any] = field(default_factory=dict)   # Evidence metrics
    resource_budget: ResourceBudget = field(default_factory=ResourceBudget)
    security_state: Dict[str, Any] = field(default_factory=dict)   # C03 / L20
    governance_state: Dict[str, Any] = field(default_factory=dict) # C03 / L17
    alignment_state: Dict[str, Any] = field(default_factory=dict)
    evolution_state: Dict[str, Any] = field(default_factory=dict)  # L21 / H11-OPT / H11-EVO
    active_incidents: List[str] = field(default_factory=list)
    state_fingerprint: str = ""
    last_updated: float = field(default_factory=time.time)

    def update_timestamp(self) -> None:
        self.last_updated = time.time()
        self.state_fingerprint = self.compute_fingerprint()

    def set_agent_status(self, agent_id: str, status: str) -> None:
        self.agent_state[agent_id] = status
        self.update_timestamp()

    def raise_incident(self, incident: str) -> None:
        self.active_incidents.append(incident)
        if len(self.active_incidents) >= 3:
            self.runtime_state = "DEGRADED"
        self.update_timestamp()

    def clear_incident(self, incident: str) -> None:
        if incident in self.active_incidents:
            self.active_incidents.remove(incident)
        if not self.active_incidents and self.runtime_state == "DEGRADED":
            self.runtime_state = "OPERATIONAL"
        self.update_timestamp()

    def compute_fingerprint(self) -> str:
        """Computes SHA-256 fingerprint of current system state."""
        manifest = {
            "version": self.system_version,
            "runtime_state": self.runtime_state,
            "active_incidents": len(self.active_incidents),
            "agents_tracked": len(self.agent_state),
            "budget": self.resource_budget.to_dict(),
        }
        encoded = json.dumps(manifest, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "system_version": self.system_version,
            "runtime_state": self.runtime_state,
            "agent_count": len(self.agent_state),
            "active_incidents": self.active_incidents,
            "resource_budget": self.resource_budget.to_dict(),
            "fingerprint": self.state_fingerprint or self.compute_fingerprint(),
            "last_updated": self.last_updated,
        }
