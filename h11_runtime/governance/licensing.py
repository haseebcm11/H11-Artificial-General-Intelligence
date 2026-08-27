"""Action licensing issuer."""
from __future__ import annotations

import time
from typing import Optional, Tuple

from ..case import Case, CaseState
from ..contracts import ActionLicense, ActionProposal


class ActionLicenseIssuer:
    """12 — H11C-ACTION-LICENSE: Issues cryptographic, time-bounded action licenses."""

    def issue_license(
        self,
        case: Case,
        proposal: ActionProposal,
    ) -> Tuple[bool, Optional[ActionLicense], str]:
        if case.state == CaseState.HALTED:
            return False, None, "DENIED: Case is in HALTED state"

        license_obj = ActionLicense(
            proposal_id=proposal.proposal_id,
            case_id=case.envelope.case_id,
            authorized_action=proposal.action_type,
            target_resource=proposal.target_resource,
            authority_id="H11C_ALIGN_ENFORCE",
            expires_at=time.time() + 300.0,
        )
        case.action_licenses.append(license_obj)
        case.transition_to(CaseState.LICENSED, f"Issued license {license_obj.license_id}")
        return True, license_obj, "ACTION_LICENSED"
