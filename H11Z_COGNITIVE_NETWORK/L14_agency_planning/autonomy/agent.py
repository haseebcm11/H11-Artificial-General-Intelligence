import uuid
import math
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

class AutonomyLevel(Enum):
    MANUAL = 0
    ASSISTED = 1
    SUPERVISED = 2
    HIGHLY_AUTONOMOUS = 3
    FULLY_AUTONOMOUS = 4

@dataclass
class ActionProposal:
    action_id: str
    domain: str
    impact_score: float  # 0.0 to 1.0
    irreversibility: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    cost_estimate: float
    description: str

class DecisionType(Enum):
    APPROVED = "APPROVED"
    ESCALATED = "ESCALATED"
    DENIED = "DENIED"

@dataclass
class AutonomyDecision:
    decision_type: DecisionType
    gate_id: Optional[str]
    reason: str
    risk_score: float
    trust_margin: float

@dataclass
class DomainTrust:
    domain_name: str
    trust_score: float = 0.5  # Initial neutral trust
    total_actions: int = 0
    successful_actions: int = 0
    alpha: float = 0.15  # Base learning rate

    def update_trust(self, success: bool, impact: float):
        """
        Dynamic trust calibration.
        Failures have a much higher impact on trust than successes.
        """
        target = 1.0 if success else 0.0
        
        # High impact failures decrease trust significantly faster
        learning_rate = self.alpha
        if not success:
            learning_rate = min(1.0, self.alpha * (2.0 + 3.0 * impact))
            
        self.trust_score = (1.0 - learning_rate) * self.trust_score + learning_rate * target
        self.trust_score = max(0.01, min(0.99, self.trust_score))
        
        self.total_actions += 1
        if success:
            self.successful_actions += 1

class EscalationEngine:
    def __init__(self, global_level: AutonomyLevel):
        self.global_level = global_level
        self.domain_trusts: Dict[str, DomainTrust] = {}
        self.pending_gates: Dict[str, ActionProposal] = {}

    def _get_trust(self, domain: str) -> DomainTrust:
        if domain not in self.domain_trusts:
            self.domain_trusts[domain] = DomainTrust(domain_name=domain)
        return self.domain_trusts[domain]

    def _calculate_risk(self, proposal: ActionProposal) -> float:
        """
        Computes a non-linear risk score based on proposal factors.
        """
        base_risk = (proposal.impact_score * 0.6) + (proposal.irreversibility * 0.4)
        uncertainty_penalty = (1.0 - proposal.confidence) * 0.5
        cost_penalty = min(1.0, proposal.cost_estimate / 1000.0) * 0.2
        
        # Exponential compounding if impact and irreversibility are both high
        compounding = 0.0
        if proposal.impact_score > 0.7 and proposal.irreversibility > 0.7:
            compounding = 0.3
            
        return min(1.0, base_risk + uncertainty_penalty + cost_penalty + compounding)

    def evaluate_proposal(self, proposal: ActionProposal) -> AutonomyDecision:
        if self.global_level == AutonomyLevel.MANUAL:
            return self._escalate(proposal, "Global policy is MANUAL. All actions require approval.", 1.0, 0.0)
            
        risk = self._calculate_risk(proposal)
        trust = self._get_trust(proposal.domain).trust_score
        
        # Allowed risk thresholds based on Autonomy Level
        base_thresholds = {
            AutonomyLevel.ASSISTED: 0.15,
            AutonomyLevel.SUPERVISED: 0.45,
            AutonomyLevel.HIGHLY_AUTONOMOUS: 0.75,
            AutonomyLevel.FULLY_AUTONOMOUS: 1.0
        }
        
        level_threshold = base_thresholds.get(self.global_level, 0.0)
        
        # Effective threshold is modulated by domain trust
        # Trust scales the threshold between 0.5x (low trust) and 1.5x (high trust)
        trust_modifier = 0.5 + trust
        effective_threshold = min(1.0, level_threshold * trust_modifier)
        
        trust_margin = effective_threshold - risk
        
        if self.global_level == AutonomyLevel.FULLY_AUTONOMOUS:
            # In fully autonomous, only deny if extremely dangerous and trust is ruined
            if risk > 0.95 and trust < 0.2:
                return AutonomyDecision(DecisionType.DENIED, None, "Critical risk with broken domain trust.", risk, trust_margin)
            return AutonomyDecision(DecisionType.APPROVED, None, "Fully autonomous execution authorized.", risk, trust_margin)

        if trust_margin >= 0:
            return AutonomyDecision(DecisionType.APPROVED, None, f"Risk {risk:.2f} within trusted boundaries.", risk, trust_margin)
        else:
            return self._escalate(proposal, f"Risk {risk:.2f} exceeds effective trust boundary {effective_threshold:.2f}", risk, trust_margin)

    def _escalate(self, proposal: ActionProposal, reason: str, risk: float, margin: float) -> AutonomyDecision:
        gate_id = f"gate-{uuid.uuid4().hex[:8]}"
        self.pending_gates[gate_id] = proposal
        return AutonomyDecision(DecisionType.ESCALATED, gate_id, reason, risk, margin)

    def resolve_gate(self, gate_id: str, approved: bool, override_level: bool = False) -> Optional[ActionProposal]:
        """
        Human resolves an escalation gate.
        """
        if gate_id in self.pending_gates:
            proposal = self.pending_gates.pop(gate_id)
            if approved:
                return proposal
        return None

    def feedback_loop(self, domain: str, success: bool, impact: float):
        trust = self._get_trust(domain)
        trust.update_trust(success, impact)

class AutonomyAgent:
    def __init__(self, initial_level: AutonomyLevel = AutonomyLevel.SUPERVISED):
        self.escalation_engine = EscalationEngine(global_level=initial_level)

    def set_autonomy_level(self, level: AutonomyLevel):
        self.escalation_engine.global_level = level

    def propose_action(self, action_id: str, domain: str, impact: float, irreversibility: float, confidence: float, cost: float, desc: str) -> AutonomyDecision:
        proposal = ActionProposal(
            action_id=action_id,
            domain=domain,
            impact_score=impact,
            irreversibility=irreversibility,
            confidence=confidence,
            cost_estimate=cost,
            description=desc
        )
        return self.escalation_engine.evaluate_proposal(proposal)

    def human_approval(self, gate_id: str, approved: bool) -> bool:
        proposal = self.escalation_engine.resolve_gate(gate_id, approved)
        return proposal is not None

    def report_execution_result(self, domain: str, success: bool, impact: float):
        """
        Closes the loop by updating trust based on execution outcomes.
        """
        self.escalation_engine.feedback_loop(domain, success, impact)
        
    def get_autonomy_status(self) -> Dict:
        return {
            "global_level": self.escalation_engine.global_level.name,
            "domains": {
                name: {
                    "trust_score": round(dt.trust_score, 3),
                    "success_rate": round(dt.successful_actions / max(1, dt.total_actions), 3)
                }
                for name, dt in self.escalation_engine.domain_trusts.items()
            },
            "pending_escalations": len(self.escalation_engine.pending_gates)
        }
