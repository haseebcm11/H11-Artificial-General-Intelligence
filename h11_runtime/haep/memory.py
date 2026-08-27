"""H11-AGI Enhancement Protocol v2.0 — Evolution Memory, Meta-Learning, & Cascade Protection.

Sections 23, 25, 31, 32, 38, 39, 40, 41: Tracking evolutionary lineage,
calculating prediction errors, detecting oscillations, and preventing runaway cascades.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import time
from typing import Any, Dict, List, Optional, Set, Tuple

from .protocol import (
    EnhancementObject,
    EnhancementOperation,
    EnhancementState,
    PromotionLevel,
)


@dataclass
class LineageNode:
    state_id: str
    version: str
    enhancement_id: Optional[str]
    parent_state_id: Optional[str]
    status: str  # ACTIVE, ROLLED_BACK, REJECTED, SUPERSEDED
    timestamp: float = field(default_factory=time.time)
    children: List[str] = field(default_factory=list)


class EvolutionMemoryManager:
    """Section 23, 25, 32: Evolutionary Memory, Meta-Learning, and Lineage Tree."""

    def __init__(self) -> None:
        self.lineage_tree: Dict[str, LineageNode] = {
            "S0": LineageNode(state_id="S0", version="1.0.0", enhancement_id=None, parent_state_id=None, status="ACTIVE")
        }
        self.recent_transitions: List[Dict[str, Any]] = []
        self.operator_success_stats: Dict[str, Dict[str, int]] = {}  # {op: {success: n, failure: m}}
        self.prediction_errors: List[float] = []

    def record_transition(
        self,
        enh: EnhancementObject,
        new_state_id: str,
        new_version: str,
        is_successful: bool,
    ) -> None:
        parent = enh.baseline_lock.system_state.state_id if enh.baseline_lock else "S0"
        node = LineageNode(
            state_id=new_state_id,
            version=new_version,
            enhancement_id=enh.enhancement_id,
            parent_state_id=parent,
            status="ACTIVE" if is_successful else "ROLLED_BACK",
        )
        self.lineage_tree[new_state_id] = node
        if parent in self.lineage_tree:
            self.lineage_tree[parent].children.append(new_state_id)

        # Record meta-learning stats
        op_name = enh.operation.value
        if op_name not in self.operator_success_stats:
            self.operator_success_stats[op_name] = {"success": 0, "failure": 0}
        if is_successful:
            self.operator_success_stats[op_name]["success"] += 1
        else:
            self.operator_success_stats[op_name]["failure"] += 1

        # Track prediction error (Section 31)
        if enh.observed_outcome > 0.0:
            self.prediction_errors.append(enh.prediction_error)

        self.recent_transitions.append({
            "target": enh.target,
            "operation": enh.operation.value,
            "success": is_successful,
            "timestamp": time.time(),
        })

    def calculate_evolution_stability(self) -> float:
        """Section 38: Evolution Stability ES = stable transitions / total transitions."""
        if not self.recent_transitions:
            return 1.0
        stables = sum(1 for t in self.recent_transitions if t["success"])
        return round(stables / len(self.recent_transitions), 4)

    def detect_oscillation(self, target: str, window: int = 4) -> bool:
        """Section 39: Detects cyclic modifications A -> B -> A -> B on the same target."""
        target_ops = [t["operation"] for t in self.recent_transitions if t["target"] == target][-window:]
        if len(target_ops) >= 4:
            # Check for alternating 2-pattern e.g. [OP1, OP2, OP1, OP2]
            if target_ops[0] == target_ops[2] and target_ops[1] == target_ops[3] and target_ops[0] != target_ops[1]:
                return True
        return False

    def detect_cascade(self, max_chain_depth: int = 4) -> bool:
        """Section 41: Detects runaway automated enhancement cascades."""
        # Look at the last N transitions within a short time window (<60 seconds)
        recent = [t for t in self.recent_transitions if time.time() - t["timestamp"] < 60.0]
        return len(recent) >= max_chain_depth
