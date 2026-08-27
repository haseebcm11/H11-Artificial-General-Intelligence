"""The central Case object."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional

from ..contracts import ActionLicense, ActionProposal, CaseEnvelope
from .blackboard import Blackboard
from .state import CaseState


@dataclass
class Case:
    """The central case object driving the cognitive trajectory (v3.0 Section 6)."""
    envelope: CaseEnvelope
    state: CaseState = CaseState.NEW
    blackboard: Blackboard = field(init=False)
    active_agents: List[str] = field(default_factory=list)
    action_proposals: List[ActionProposal] = field(default_factory=list)
    action_licenses: List[ActionLicense] = field(default_factory=list)
    final_output: Optional[Dict[str, Any]] = None
    halt_reason: Optional[str] = None
    state_history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.blackboard = Blackboard(case_id=self.envelope.case_id)
        self.transition_to(CaseState.NEW, "Initialized case instance")

    def transition_to(self, new_state: CaseState, reason: str = "") -> None:
        self.state_history.append({
            "from_state": self.state.value,
            "to_state": new_state.value,
            "timestamp": time.time(),
            "reason": reason,
        })
        self.state = new_state
        self.envelope.state = new_state.value
