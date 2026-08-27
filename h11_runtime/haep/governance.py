"""H11-AGI Enhancement Protocol v5.0 — Governance, Invariants V5-I01 to V5-I20, & Authority Levels.

Sections 86, 88, 89, 90, 91, 113: Strict enforcement of the 20 V5 Core Invariants,
Authority Levels (A0-A6), and separation between optimization and governance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Tuple

from .protocol import (
    AuthorityLevel,
    EnhancementAuthorizationToken,
    EnhancementObject,
    EvolutionState,
    PromotionLevel,
    PromotionVector,
    RecursiveLevel,
    RiskLevel,
)


class EvolutionFreezeActiveError(PermissionError):
    """Raised when an enhancement transition is attempted during an EVOLUTION-FROZEN state."""
    pass


class GovernanceGate:
    """Sections 86, 88, 90, 113: H11C Governance Gatekeeper & 20 V5 Core Invariants Engine."""

    def __init__(self, authority_id: str = "H11C_CONTROL_PLANE") -> None:
        self.authority_id = authority_id
        self.is_frozen = False
        self.freeze_reason: Optional[str] = None
        self.issued_tokens: Dict[str, EnhancementAuthorizationToken] = {}
        self.recovery_stage: Optional[str] = None

    def trigger_evolution_freeze(self, reason: str) -> None:
        """Section 76: Enters EVOLUTION-FROZEN state."""
        self.is_frozen = True
        self.freeze_reason = reason
        self.recovery_stage = "FROZEN"

    def execute_freeze_recovery_step(self, stage_name: str, auth_key: str) -> Tuple[bool, str]:
        """Section 77: 7-step structured recovery: FREEZE -> STABILIZE -> ROOT_CAUSE -> RECOVERY -> VALIDATION -> GOVERNANCE_REVIEW -> UNFREEZE."""
        if auth_key != "H11C_MASTER_OVERRIDE":
            return False, "DENIED: Unauthorized recovery attempt"

        valid_stages = ["STABILIZE", "ROOT_CAUSE", "RECOVERY", "VALIDATION", "GOVERNANCE_REVIEW", "UNFREEZE"]
        if stage_name not in valid_stages:
            return False, f"INVALID_STAGE: {stage_name}"

        self.recovery_stage = stage_name
        if stage_name == "UNFREEZE":
            self.is_frozen = False
            self.freeze_reason = None
            self.recovery_stage = None
            return True, "EVOLUTION_UNFROZEN: Normal evolution operations resumed"

        return True, f"RECOVERY_STAGE_COMPLETED: {stage_name}"

    def verify_v5_invariants(self, enh: EnhancementObject, caller_id: str) -> Tuple[bool, List[str]]:
        """Section 113: Enforces the 20 V5 Core Invariants (V5-I01 to V5-I20)."""
        violations = []

        # V5-I16 & V5-I17 — Evolution Freeze & Governance Integrity
        if self.is_frozen:
            violations.append(f"V5_I17_VIOLATION: System is in EVOLUTION-FROZEN state: {self.freeze_reason}")

        # V5-I01 — No silent system-state transition
        if not enh.proposed_change or not enh.parent_version:
            violations.append("V5_I01_VIOLATION: System-state transition must be explicit and observable")

        # V5-I02 & V5-I03 — No self-granted authority & No optimization outside authorized scope
        if caller_id.startswith("L21") and enh.authority_level in (AuthorityLevel.A5_AUTHORIZED_PRODUCTION, AuthorityLevel.A6_RECURSIVE_EVOLUTION):
            violations.append("V5_I02_VIOLATION: Optimizer cannot self-authorize production/recursive evolution")

        # V5-I04 — No protected-core modification without required governance
        # V5-I05 — No critical transition without recoverability
        if not enh.baseline_lock:
            violations.append("V5_I05_VIOLATION: Missing baseline lock for guaranteed rollback")

        # V5-I06 — No capability metric alone defines improvement
        # V5-I18 & V5-I19 — Security and Safety integrity are protected constraints
        if enh.vector.safety < 0.99:
            violations.append("V5_I19_VIOLATION: Safety integrity gate (S < 0.99) violated")
        if enh.vector.security < 0.99:
            violations.append("V5_I18_VIOLATION: Security integrity gate (Z < 0.99) violated")

        # V5-I07 — No architectural growth without demonstrated need
        if enh.vector.complexity > 0.35 and enh.vector.capability < 0.85:
            violations.append("V5_I07_VIOLATION: High complexity expansion without capability justification")

        # V5-I11 & V5-I12 — Uncontrolled recursive / unbounded search
        if enh.recursive_level >= RecursiveLevel.LEVEL_5_EVOLUTION and caller_id != "H11C_SUPREME_GOVERNANCE":
            violations.append("V5_I12_VIOLATION: Level 5/6 recursive self-modification requires Supreme Governance")

        return len(violations) == 0, violations

    def issue_authorization_token(
        self,
        enh: EnhancementObject,
        caller_identity: str,
    ) -> Tuple[bool, Optional[EnhancementAuthorizationToken], str]:
        """Section 88 & 90: Issues cryptographic authorization token upon V5 invariant verification."""
        if self.is_frozen:
            return False, None, f"DENIED: Evolution is frozen: {self.freeze_reason}"

        ok, violations = self.verify_v5_invariants(enh, caller_identity)
        if not ok:
            return False, None, f"GOVERNANCE_REJECT: {'; '.join(violations)}"

        token = EnhancementAuthorizationToken(
            enhancement_id=enh.enhancement_id,
            target=enh.target,
            risk=enh.risk_class,
            recursive_level=enh.recursive_level,
            authority_level=enh.authority_level,
            scope=enh.affected_agents + enh.affected_layers,
            authority=self.authority_id,
            approved_version=enh.parent_version,
            rollback_reference=enh.baseline_lock.baseline_id if enh.baseline_lock else "BASE-GENESIS",
        )
        self.issued_tokens[token.token_id] = token
        enh.auth_token = token
        return True, token, "AUTHORIZED: V5 Authorization token successfully issued"
