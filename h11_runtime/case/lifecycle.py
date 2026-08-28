"""Case lifecycle manager coordinating valid state transitions and checkpointing."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from ..contracts import CaseEnvelope, RiskClass
from .case import Case
from .state import CaseState

logger = logging.getLogger(__name__)


class CaseLifecycleManager:
    """Coordinates state transitions, validation, and lifecycle invariants (v3.0 Section 6)."""

    # Legal state transition matrix
    _VALID_TRANSITIONS = {
        CaseState.NEW: [CaseState.ADMITTED, CaseState.REJECTED, CaseState.HALTED],
        CaseState.ADMITTED: [CaseState.CONTEXTUALIZED, CaseState.QUARANTINED, CaseState.HALTED],
        CaseState.CONTEXTUALIZED: [CaseState.MAPPED, CaseState.HALTED],
        CaseState.MAPPED: [CaseState.COMPOSED, CaseState.HALTED],
        CaseState.COMPOSED: [CaseState.READY, CaseState.EXECUTING, CaseState.HALTED],
        CaseState.READY: [CaseState.EXECUTING, CaseState.HALTED],
        CaseState.EXECUTING: [CaseState.INTEGRATING, CaseState.HALTED],
        CaseState.INTEGRATING: [CaseState.VERIFYING, CaseState.ALIGNING, CaseState.HALTED],
        CaseState.VERIFYING: [CaseState.ALIGNING, CaseState.HALTED],
        CaseState.ALIGNING: [CaseState.RELEASED, CaseState.HALTED, CaseState.ROLLED_BACK],
        CaseState.RELEASED: [CaseState.MEMORIZED, CaseState.CLOSED],
        CaseState.MEMORIZED: [CaseState.CLOSED],
        CaseState.CLOSED: [],
        CaseState.HALTED: [CaseState.ROLLED_BACK, CaseState.CLOSED],
        CaseState.ROLLED_BACK: [CaseState.CLOSED],
        CaseState.REJECTED: [CaseState.CLOSED],
        CaseState.QUARANTINED: [CaseState.CLOSED],
    }

    def __init__(self) -> None:
        self.active_cases: Dict[str, Case] = {}
        self.closed_cases: Dict[str, Case] = {}

    def create_case(
        self,
        objective: str,
        input_data: Any,
        requested_capabilities: Optional[List[str]] = None,
        risk_class: RiskClass = RiskClass.R1_LOW,
        principal_id: str = "SYSTEM_USER",
    ) -> Case:
        env = CaseEnvelope(
            objective=objective,
            input_data=input_data,
            requested_capabilities=requested_capabilities or [],
            risk_class=risk_class,
            principal_id=principal_id,
        )
        case = Case(envelope=env)
        self.active_cases[case.case_id] = case
        return case

    def advance(self, case: Case, target_state: CaseState, reason: str = "") -> bool:
        """Enforces state transition rules against the canonical transition matrix."""
        allowed_targets = self._VALID_TRANSITIONS.get(case.state, [])
        if target_state not in allowed_targets and target_state != CaseState.HALTED:
            logger.warning(
                f"Illegal state transition requested for {case.case_id}: "
                f"{case.state.value} -> {target_state.value}"
            )
            return False

        case.transition_to(target_state, reason)
        if target_state in (CaseState.CLOSED, CaseState.REJECTED):
            if case.case_id in self.active_cases:
                self.closed_cases[case.case_id] = self.active_cases.pop(case.case_id)
        return True

    def get_case(self, case_id: str) -> Optional[Case]:
        return self.active_cases.get(case_id) or self.closed_cases.get(case_id)

    def close_all(self, reason: str = "KERNEL_SHUTDOWN") -> int:
        count = 0
        for case in list(self.active_cases.values()):
            self.advance(case, CaseState.CLOSED, reason)
            count += 1
        return count
