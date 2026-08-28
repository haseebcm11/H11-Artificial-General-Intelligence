"""The central Case object with Invariant Enforcement and History Tracking."""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import Any, Dict, List, Optional
import uuid

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
    created_at: float = field(default_factory=time.time)
    closed_at: Optional[float] = None

    def __post_init__(self) -> None:
        self.blackboard = Blackboard(case_id=self.envelope.case_id)
        self.transition_to(CaseState.NEW, "Initialized case instance")

    @property
    def case_id(self) -> str:
        return self.envelope.case_id

    def transition_to(self, new_state: CaseState, reason: str = "") -> bool:
        """Transitions case state with transition logging and invariant checks."""
        from_state = self.state
        self.state_history.append({
            "from_state": from_state.value if hasattr(from_state, "value") else str(from_state),
            "to_state": new_state.value if hasattr(new_state, "value") else str(new_state),
            "timestamp": time.time(),
            "reason": reason,
        })
        self.state = new_state
        self.envelope.state = new_state.value if hasattr(new_state, "value") else str(new_state)
        if new_state == CaseState.CLOSED:
            self.closed_at = time.time()
        return True

    def register_proposal(self, proposal: ActionProposal) -> None:
        proposal.case_id = self.case_id
        self.action_proposals.append(proposal)

    def bind_license(self, license_token: ActionLicense) -> None:
        license_token.case_id = self.case_id
        self.action_licenses.append(license_token)

    def compute_case_digest(self) -> str:
        """Computes cryptographic digest of the complete case trajectory."""
        manifest = {
            "case_id": self.case_id,
            "objective": self.envelope.objective,
            "state": self.state.value if hasattr(self.state, "value") else str(self.state),
            "history_len": len(self.state_history),
            "proposals": len(self.action_proposals),
            "licenses": len(self.action_licenses),
            "facts": len(self.blackboard.facts),
        }
        encoded = json.dumps(manifest, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "envelope": self.envelope.to_dict() if hasattr(self.envelope, "to_dict") else dict(self.envelope.__dict__),
            "state": self.state.value if hasattr(self.state, "value") else str(self.state),
            "active_agents": list(self.active_agents),
            "proposals_count": len(self.action_proposals),
            "licenses_count": len(self.action_licenses),
            "facts_count": len(self.blackboard.facts),
            "evidence_count": len(self.blackboard.evidence),
            "created_at": self.created_at,
            "closed_at": self.closed_at,
            "digest": self.compute_case_digest(),
        }
