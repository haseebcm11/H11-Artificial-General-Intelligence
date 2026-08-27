"""5. State Graph."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Set


@dataclass
class StateTransition:
    from_state: str
    to_state: str
    timestamp: float
    trigger: str
    context: Dict[str, Any] = field(default_factory=dict)


class StateGraph:
    """5. State Graph: Tracks case and system lifecycle progression and permitted transitions."""

    def __init__(self, initial_state: str = "NEW") -> None:
        self.current_state = initial_state
        self.history: List[StateTransition] = []
        self.allowed_transitions: Dict[str, Set[str]] = {
            "NEW": {"ADMITTED", "REJECTED"},
            "ADMITTED": {"CONTEXTUALIZED", "HALTED", "REJECTED"},
            "CONTEXTUALIZED": {"MAPPED", "HALTED"},
            "MAPPED": {"COMPOSED", "HALTED"},
            "COMPOSED": {"READY", "HALTED"},
            "READY": {"EXECUTING", "HALTED"},
            "EXECUTING": {"INTEGRATING", "RETRYING", "DEGRADED", "HALTED"},
            "RETRYING": {"EXECUTING", "DEGRADED", "HALTED"},
            "DEGRADED": {"INTEGRATING", "HALTED"},
            "INTEGRATING": {"VERIFYING", "HALTED"},
            "VERIFYING": {"ALIGNING", "HALTED"},
            "ALIGNING": {"RELEASED", "HALTED"},
            "RELEASED": {"MEMORIZED", "HALTED"},
            "MEMORIZED": {"CLOSED"},
            "HALTED": {"ROLLED_BACK", "CLOSED"},
            "ROLLED_BACK": {"CLOSED"},
            "REJECTED": {"CLOSED"},
            "CLOSED": set(),
        }

    def transition(self, target_state: str, trigger: str = "", context: Optional[Dict[str, Any]] = None) -> bool:
        allowed = self.allowed_transitions.get(self.current_state, set())
        if target_state not in allowed and target_state != "HALTED":
            return False
        
        t = StateTransition(
            from_state=self.current_state,
            to_state=target_state,
            timestamp=time.time(),
            trigger=trigger,
            context=context or {},
        )
        self.history.append(t)
        self.current_state = target_state
        return True
