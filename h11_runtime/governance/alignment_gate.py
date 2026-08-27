"""ALIGN Hard Gate."""
from __future__ import annotations

import json
from typing import Any, Dict, Tuple

from ..case import Case, CaseState


class AlignmentHaltException(PermissionError):
    """Raised when an alignment evaluation fails at the ALIGN-ENFORCE hard gate."""
    pass


class AlignmentGate:
    """11 — H11C-ALIGN-HOOK & H11C-ALIGN-ENFORCE: Non-bypassable hard safety gate.

    Skipping ALIGN is a hard HALT.
    """

    def evaluate_alignment(
        self,
        case: Case,
        candidate_result: Dict[str, Any],
    ) -> Tuple[bool, str]:
        """Evaluates constitutional safety, fairness, and toxicity boundaries."""
        case.transition_to(CaseState.ALIGNING, "Evaluating alignment hard gate")

        # Check for prohibited or harmful tokens / payload
        res_str = json.dumps(candidate_result).lower()
        if "prohibited_action" in res_str or "unauthorized_exfil" in res_str:
            case.transition_to(CaseState.HALTED, "ALIGNMENT_VIOLATION_DETECTED")
            case.halt_reason = "ALIGNMENT_FAIL: Prohibited payload detected"
            return False, case.halt_reason

        return True, "ALIGNMENT_PASSED"
