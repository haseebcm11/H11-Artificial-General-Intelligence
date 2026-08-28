"""Independent Verification Layer: Factual Support, Logical Consistency, and Rejection Boundaries."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from ..deliberation.deliberator import SynthesisCandidate
from ..evidence.ledger import EvidenceLedger

logger = logging.getLogger(__name__)


@dataclass
class VerificationReport:
    """Independent verification assessment of a deliberated synthesis candidate."""
    passed: bool
    status: str  # "PASSED", "REJECTED", "CONDITIONALLY_PASSED"
    confidence_score: float
    factual_support_score: float
    logical_consistency_score: float
    policy_compliance: bool
    violations: List[str] = field(default_factory=list)
    rejection_reasons: List[str] = field(default_factory=list)
    recommended_replan_actions: List[str] = field(default_factory=list)
    verifier_signature: str = ""


class IndependentVerifier:
    """09 — IndependentVerifier: Rigorous verification stage capable of rejecting synthesis (v3.0 Section 9)."""

    def __init__(
        self,
        min_factual_score: float = 0.50,
        min_consistency_score: float = 0.60,
        max_uncertainty: float = 0.60,
    ) -> None:
        self.min_factual_score = min_factual_score
        self.min_consistency_score = min_consistency_score
        self.max_uncertainty = max_uncertainty

    def verify(
        self,
        synthesis: SynthesisCandidate,
        evidence_ledger: Optional[EvidenceLedger] = None,
        safety_policy_check: bool = True,
    ) -> VerificationReport:
        """Independently verifies synthesis against facts, logic, and governance."""
        violations: List[str] = []
        rejection_reasons: List[str] = []
        replan_actions: List[str] = []

        # 1. Contradiction Check
        consistency_score = 1.0
        if synthesis.contradictions:
            consistency_score -= 0.3 * len(synthesis.contradictions)
            rejection_reasons.append(f"Found {len(synthesis.contradictions)} unresolvable contradiction(s).")
            replan_actions.append("ACTIVATE_ARBITER_SPECIALISTS")

        # 2. Factual Grounding Check
        factual_score = 1.0
        if synthesis.unsupported_claims:
            ratio = len(synthesis.unsupported_claims) / max(1, len(synthesis.consensus_claims) + len(synthesis.unsupported_claims))
            factual_score -= ratio * 0.5
            if ratio > 0.5:
                rejection_reasons.append(f"High ratio of unsupported claims ({len(synthesis.unsupported_claims)}).")
                replan_actions.append("TRIGGER_LSE_EVIDENCE_EXPANSION")

        # 3. Uncertainty Threshold Check
        if synthesis.uncertainty_score > self.max_uncertainty:
            rejection_reasons.append(f"Uncertainty ({synthesis.uncertainty_score:.2f}) exceeds maximum threshold ({self.max_uncertainty}).")
            replan_actions.append("DEEPEN_COGNITIVE_DECOMPOSITION")

        # 4. Policy Compliance Check
        policy_ok = True
        if safety_policy_check:
            harmful_keywords = ["exploit", "unauthorized_override", "bypass_align", "disable_safety"]
            for claim in synthesis.consensus_claims:
                if any(kw in claim.lower() for kw in harmful_keywords):
                    policy_ok = False
                    violations.append(f"Policy safety violation in claim: {claim}")
                    rejection_reasons.append("Safety policy violation detected.")
                    replan_actions.append("HALT_DANGEROUS_ACTION")

        # Final Verification Decision
        factual_score = max(0.0, factual_score)
        consistency_score = max(0.0, consistency_score)
        passed = (
            policy_ok
            and consistency_score >= self.min_consistency_score
            and factual_score >= self.min_factual_score
            and len(rejection_reasons) == 0
        )

        status = "PASSED" if passed else "REJECTED"
        logger.info(f"Verification {status}: Factual={factual_score:.2f}, Consistency={consistency_score:.2f}, PolicyOK={policy_ok}")

        return VerificationReport(
            passed=passed,
            status=status,
            confidence_score=synthesis.overall_confidence,
            factual_support_score=factual_score,
            logical_consistency_score=consistency_score,
            policy_compliance=policy_ok,
            violations=violations,
            rejection_reasons=rejection_reasons,
            recommended_replan_actions=replan_actions,
            verifier_signature="H11-INDEPENDENT-VERIFIER-V1",
        )
