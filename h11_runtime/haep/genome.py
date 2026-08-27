"""H11-AGI Enhancement Protocol v3.0 — System Genome v3 & Evolution Trajectory.

Sections 40, 54, 55: Canonical 8-graph System Genome representation,
Evolution Trajectory logger, and State Transition operator Φ.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Set

from .protocol import SystemState, SystemStateVector


@dataclass
class TrajectoryPoint:
    timestamp: float
    version: str
    capability: float
    reliability: float
    safety: float
    efficiency: float
    complexity: float


@dataclass
class ArchitectureDifferential:
    """Section 27: Explicit differential between system versions S(t) and S(t+1)."""
    parent_version: str
    target_version: str
    added_components: List[str] = field(default_factory=list)
    removed_components: List[str] = field(default_factory=list)
    changed_components: List[str] = field(default_factory=list)
    changed_dependencies: Dict[str, List[str]] = field(default_factory=dict)
    changed_policies: List[str] = field(default_factory=list)
    behavior_delta_summary: str = ""

    def to_json(self) -> str:
        return json.dumps({
            "parent_version": self.parent_version,
            "target_version": self.target_version,
            "added": self.added_components,
            "removed": self.removed_components,
            "changed": self.changed_components,
            "dependency_deltas": self.changed_dependencies,
            "policy_deltas": self.changed_policies,
            "summary": self.behavior_delta_summary,
        }, indent=2)


class SystemGenomeManager:
    """Section 40: Manages the canonical 8-Graph H11 System Genome v3."""

    def __init__(self, initial_version: str = "1.0.0") -> None:
        self.current_state = SystemState(version=initial_version)
        self.state_history: Dict[str, SystemState] = {self.current_state.state_id: self.current_state}
        self.genome_descriptors: Dict[str, Dict[str, Any]] = {}
        self.evolution_trajectory: List[TrajectoryPoint] = []
        self._init_base_genome()

    def _init_base_genome(self) -> None:
        base_desc = {
            "version": "1.0.0",
            "pillars": {
                "H11Z_COGNITIVE_NETWORK": 400,
                "H11I_INTELLIGENCE_UNIVERSE": 475,
                "H11C_CONTROL_PLANE": 125,
            },
            "total_agents": 1000,
            "policies": ["ALIGN_V1", "ZERO_TRUST_HOP", "SCHEMA_FIREWALL", "ACTION_LICENSE"],
            "timestamp": time.time(),
        }
        raw = json.dumps(base_desc, sort_keys=True)
        self.current_state.genome_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        self.genome_descriptors[self.current_state.state_id] = base_desc
        self.record_trajectory_point("1.0.0", 0.90, 0.95, 1.0, 0.90, 0.10)

    def record_trajectory_point(
        self,
        version: str,
        capability: float,
        reliability: float,
        safety: float,
        efficiency: float,
        complexity: float,
    ) -> None:
        """Section 55: Records evolution trajectory data points."""
        self.evolution_trajectory.append(TrajectoryPoint(
            timestamp=time.time(),
            version=version,
            capability=capability,
            reliability=reliability,
            safety=safety,
            efficiency=efficiency,
            complexity=complexity,
        ))

    def compute_differential(
        self,
        target_version: str,
        changed_components: List[str],
        added_components: Optional[List[str]] = None,
        removed_components: Optional[List[str]] = None,
        changed_policies: Optional[List[str]] = None,
        summary: str = "",
    ) -> ArchitectureDifferential:
        return ArchitectureDifferential(
            parent_version=self.current_state.version,
            target_version=target_version,
            added_components=added_components or [],
            removed_components=removed_components or [],
            changed_components=changed_components,
            changed_policies=changed_policies or [],
            behavior_delta_summary=summary or f"Evolution transition to {target_version}",
        )

    def transition_state(
        self,
        diff: ArchitectureDifferential,
        new_version: str,
    ) -> SystemState:
        """Section 2: S(t+1) = Φ(S(t), O(t), H(t), G(t))."""
        new_desc = dict(self.genome_descriptors.get(self.current_state.state_id, {}))
        new_desc["version"] = new_version
        new_desc["last_diff"] = json.loads(diff.to_json())
        new_desc["timestamp"] = time.time()

        raw = json.dumps(new_desc, sort_keys=True)
        new_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        next_state = SystemState(
            version=new_version,
            genome_hash=new_hash,
            active_agent_count=self.current_state.active_agent_count + len(diff.added_components) - len(diff.removed_components),
            parent_state_id=self.current_state.state_id,
            lineage_depth=self.current_state.lineage_depth + 1,
        )

        self.state_history[next_state.state_id] = next_state
        self.genome_descriptors[next_state.state_id] = new_desc
        self.current_state = next_state
        self.record_trajectory_point(new_version, 0.96, 0.98, 1.0, 0.94, 0.12)
        return next_state
