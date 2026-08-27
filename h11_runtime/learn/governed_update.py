from __future__ import annotations
import uuid
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any
from .evaluator import EvaluationReport

logger = logging.getLogger(__name__)

class GovernanceViolation(Exception):
    pass

@dataclass
class UpdateProposal:
    proposal_id: str
    model_path: str
    evaluation_report: EvaluationReport
    proposed_by: str
    proposed_at: datetime
    status: str  # 'PENDING', 'CANARY', 'APPROVED', 'REJECTED', 'ROLLED_BACK'

@dataclass
class CanaryResult:
    proposal_id: str
    canary_traffic_pct: float
    success_rate: float
    latency_p99_ms: float
    safety_violations: int
    passed: bool

class GovernedUpdater:
    def __init__(self):
        self.protected_components = {"C03", "ALIGN", "control_plane"}

    def _check_safety_invariant(self, model_path: str) -> None:
        # Check if the update attempts to touch protected governance rules
        if any(comp in model_path for comp in self.protected_components):
            raise GovernanceViolation(f"Update attempts to modify protected component in {model_path}")

    def propose_update(self, model_path: str, evaluation_report: EvaluationReport) -> UpdateProposal:
        try:
            self._check_safety_invariant(model_path)
        except GovernanceViolation as e:
            logger.error(f"Proposal rejected: {e}")
            raise

        proposal = UpdateProposal(
            proposal_id=str(uuid.uuid4()),
            model_path=model_path,
            evaluation_report=evaluation_report,
            proposed_by="system",
            proposed_at=datetime.utcnow(),
            status="PENDING"
        )
        logger.info(f"Created update proposal {proposal.proposal_id}")
        return proposal

    async def run_canary(self, proposal: UpdateProposal, test_cases: List[Dict[str, Any]], traffic_pct: float = 0.05) -> CanaryResult:
        logger.info(f"Running canary for proposal {proposal.proposal_id} at {traffic_pct*100}% traffic")
        proposal.status = "CANARY"
        
        # Simulated canary testing
        success_rate = 0.99
        latency = 120.5
        violations = 0
        
        passed = success_rate >= 0.95 and latency < 200 and violations == 0
        
        return CanaryResult(
            proposal_id=proposal.proposal_id,
            canary_traffic_pct=traffic_pct,
            success_rate=success_rate,
            latency_p99_ms=latency,
            safety_violations=violations,
            passed=passed
        )

    def approve(self, proposal: UpdateProposal, canary_result: CanaryResult) -> bool:
        try:
            self._check_safety_invariant(proposal.model_path)
        except GovernanceViolation:
            return False

        if canary_result.passed and proposal.evaluation_report.overall_pass and canary_result.safety_violations == 0:
            proposal.status = "APPROVED"
            logger.info(f"Proposal {proposal.proposal_id} APPROVED.")
            return True
        else:
            self.reject(proposal, "Failed evaluation or canary requirements.")
            return False

    def reject(self, proposal: UpdateProposal, reason: str) -> None:
        proposal.status = "REJECTED"
        logger.warning(f"Proposal {proposal.proposal_id} REJECTED: {reason}")

    def rollback(self, proposal: UpdateProposal) -> bool:
        if proposal.status == "APPROVED":
            proposal.status = "ROLLED_BACK"
            logger.info(f"Proposal {proposal.proposal_id} ROLLED BACK.")
            return True
        return False
