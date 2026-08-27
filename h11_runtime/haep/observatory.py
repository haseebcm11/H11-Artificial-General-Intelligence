"""H11-AGI Enhancement Protocol v4.0 — Emergence Observatory & Stabilization.

Sections 38, 39, 40, 41, 42, 43: Dedicated emergence monitoring, surprise/anomaly detection,
and 6-stage emergent capability stabilization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Tuple

from .protocol import EmergenceClass


@dataclass
class StabilizedEmergenceRecord:
    emergence_id: str
    name: str
    classification: EmergenceClass
    stabilization_stage: str  # DISCOVERED, OBSERVED, REPRODUCED, UNDERSTOOD, GOVERNED, REGISTERED
    specialists: List[str]
    reliability: float = 0.95
    is_trusted: bool = False
    timestamp: float = field(default_factory=time.time)


class EmergenceObservatory:
    """Section 40: Master Emergence Observatory."""

    def __init__(self) -> None:
        self.stabilized_registry: Dict[str, StabilizedEmergenceRecord] = {}
        self.anomalies: List[Dict[str, Any]] = []

    def record_emergence(
        self,
        name: str,
        specialists: List[str],
        classification: EmergenceClass = EmergenceClass.DESIRABLE,
    ) -> StabilizedEmergenceRecord:
        rec = StabilizedEmergenceRecord(
            emergence_id=f"EMERG-{len(self.stabilized_registry) + 1}",
            name=name,
            classification=classification,
            stabilization_stage="DISCOVERED",
            specialists=specialists,
        )
        self.stabilized_registry[rec.emergence_id] = rec
        return rec

    def advance_stabilization(self, emergence_id: str) -> Tuple[bool, str]:
        """Section 42: Advances through DISCOVERED -> OBSERVED -> REPRODUCED -> UNDERSTOOD -> GOVERNED -> REGISTERED."""
        if emergence_id not in self.stabilized_registry:
            return False, "UNKNOWN_EMERGENCE_ID"

        rec = self.stabilized_registry[emergence_id]
        stages = ["DISCOVERED", "OBSERVED", "REPRODUCED", "UNDERSTOOD", "GOVERNED", "REGISTERED"]
        curr_idx = stages.index(rec.stabilization_stage)
        if curr_idx < len(stages) - 1:
            rec.stabilization_stage = stages[curr_idx + 1]
            if rec.stabilization_stage == "REGISTERED":
                rec.is_trusted = True
            return True, f"STABILIZATION_ADVANCED_TO_{rec.stabilization_stage}"
        return True, "ALREADY_REGISTERED"

    def detect_surprise(self, predicted_score: float, observed_score: float, threshold: float = 0.15) -> bool:
        """Section 38: Generates EVOLUTION_SURPRISE if delta exceeds threshold."""
        return abs(observed_score - predicted_score) > threshold
