"""Action licensing issuer with cryptographic signing and revocation tracking."""
from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional, Set, Tuple

from ..case import Case, CaseState
from ..contracts import ActionLicense, ActionProposal

logger = logging.getLogger(__name__)


class ActionLicenseIssuer:
    """12 — H11C-ACTION-LICENSE: Issues and manages cryptographic, time-bounded action licenses (v3.0 Section 36)."""

    def __init__(self, default_ttl_sec: float = 300.0, secret_key: str = "H11_ALIGN_SECRET_KEY") -> None:
        self.default_ttl_sec = default_ttl_sec
        self.secret_key = secret_key
        self.issued_licenses: Dict[str, ActionLicense] = {}
        self.revoked_license_ids: Set[str] = set()

    def issue_license(
        self,
        case: Case,
        proposal: ActionProposal,
        ttl_sec: Optional[float] = None,
        scopes: Optional[List[str]] = None,
    ) -> Tuple[bool, Optional[ActionLicense], str]:
        """Issues single-use cryptographic ActionLicense if case state is valid."""
        if case.state in (CaseState.HALTED, CaseState.REJECTED, CaseState.QUARANTINED):
            return False, None, f"DENIED: Case is in non-executable state ({case.state.value})"

        actual_ttl = ttl_sec if ttl_sec is not None else self.default_ttl_sec
        now = time.time()

        license_obj = ActionLicense(
            proposal_id=proposal.proposal_id,
            case_id=case.case_id,
            authorized_action=proposal.action_type,
            target_resource=proposal.target_resource,
            authority_id="H11C_ALIGN_ENFORCE",
            scopes=scopes or ["execute"],
            issued_at=now,
            expires_at=now + actual_ttl,
        )
        license_obj.signature = license_obj.compute_signature(self.secret_key)

        self.issued_licenses[license_obj.license_id] = license_obj
        case.bind_license(license_obj)
        case.transition_to(CaseState.LICENSED, f"Issued license {license_obj.license_id}")
        proposal.evaluated = True
        proposal.evaluation_decision = "LICENSED"

        logger.info(f"Issued ActionLicense {license_obj.license_id} for proposal {proposal.proposal_id}")
        return True, license_obj, "ACTION_LICENSED"

    def verify_and_consume(self, license_id: str) -> Tuple[bool, str]:
        """Verifies license validity, signature, expiration, and consumes one use."""
        if license_id in self.revoked_license_ids:
            return False, "REVOKED: License was revoked prior to execution"

        lic = self.issued_licenses.get(license_id)
        if not lic:
            return False, "NOT_FOUND: License ID does not exist in registry"

        if not lic.verify(self.secret_key):
            return False, "SIGNATURE_INVALID: License cryptographic signature failed verification"

        if not lic.consume():
            return False, "EXPIRED_OR_EXHAUSTED: License expired or max use count reached"

        return True, "CONSUMED_OK"

    def revoke_license(self, license_id: str, reason: str = "") -> bool:
        """Revokes an active license immediately."""
        if license_id in self.issued_licenses:
            self.revoked_license_ids.add(license_id)
            logger.warning(f"Revoked ActionLicense {license_id}: {reason}")
            return True
        return False
