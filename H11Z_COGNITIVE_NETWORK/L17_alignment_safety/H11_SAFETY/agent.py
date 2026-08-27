import time
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

class EnforcementMode(Enum):
    PERMISSIVE = "permissive"
    STRICT = "strict"
    LOCKDOWN = "lockdown"

class ActionType(Enum):
    ALLOW = "allow"
    REDACT = "redact"
    HALT = "halt"

@dataclass
class PolicyConstraint:
    id: str
    description: str
    concept_vectors: List[List[float]]
    strictness: float

@dataclass
class SafetyIntervention:
    timestamp: float
    triggering_constraint_id: str
    action_taken: ActionType
    confidence: float
    original_text: Optional[str]

class H11SafetyAgent:
    """
    H11-SAFETY: Gatekeeper agent enforcing hard boundaries on AI behavior.
    """
    def __init__(self, mode: EnforcementMode, threshold: float = 0.85):
        self.mode = mode
        self.threshold = threshold
        self.active_policies: Dict[str, PolicyConstraint] = {}
        self.intervention_log: List[SafetyIntervention] = []

    def register_policy(self, policy: PolicyConstraint) -> None:
        self.active_policies[policy.id] = policy

    def _compute_concept_proximity(self, hidden_state: List[float], concept_vectors: List[List[float]]) -> float:
        # Dummy cosine similarity equivalent
        if not hidden_state or not concept_vectors:
            return 0.0
        return sum(hidden_state[:5]) / 5.0 # Simulated value

    def evaluate_state(self, current_text: str, hidden_state: List[float]) -> Tuple[ActionType, Optional[str]]:
        if self.mode == EnforcementMode.LOCKDOWN:
            return ActionType.HALT, None

        max_proximity = 0.0
        violated_policy = None

        for policy in self.active_policies.values():
            proximity = self._compute_concept_proximity(hidden_state, policy.concept_vectors)
            if proximity > max_proximity:
                max_proximity = proximity
                violated_policy = policy.id

        if max_proximity > self.threshold:
            action = ActionType.HALT if self.mode == EnforcementMode.STRICT else ActionType.REDACT
            
            intervention = SafetyIntervention(
                timestamp=time.time(),
                triggering_constraint_id=violated_policy or "unknown",
                action_taken=action,
                confidence=max_proximity,
                original_text=current_text if action == ActionType.REDACT else None
            )
            self.intervention_log.append(intervention)
            
            return action, violated_policy

        return ActionType.ALLOW, None

    def process_stream(self, token: str, hidden_state: List[float]) -> str:
        action, policy_id = self.evaluate_state(token, hidden_state)
        
        if action == ActionType.HALT:
            raise RuntimeError(f"Safety violation triggered halt by policy: {policy_id}")
        elif action == ActionType.REDACT:
            return "[REDACTED]"
            
        return token

    def get_audit_trail(self) -> List[SafetyIntervention]:
        return self.intervention_log
