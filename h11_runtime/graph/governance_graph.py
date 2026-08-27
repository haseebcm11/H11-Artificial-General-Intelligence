"""6. Governance Graph (Principal -> Capability -> Policy -> Action)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class GovernancePolicy:
    policy_id: str
    principal: str
    target_capability: str
    allowed_actions: Set[str]
    constraints: List[str] = field(default_factory=list)
    risk_ceiling: str = "HIGH"


class GovernanceGraph:
    """6. Governance Graph: Maps Principal -> Capability -> Policy -> Action permissions (C03 Authority)."""

    def __init__(self) -> None:
        self.policies: Dict[str, GovernancePolicy] = {}

    def register_policy(
        self,
        policy_id: str,
        principal: str,
        target_capability: str,
        allowed_actions: Set[str],
        constraints: Optional[List[str]] = None,
        risk_ceiling: str = "HIGH",
    ) -> GovernancePolicy:
        policy = GovernancePolicy(
            policy_id=policy_id,
            principal=principal,
            target_capability=target_capability,
            allowed_actions=set(allowed_actions),
            constraints=constraints or [],
            risk_ceiling=risk_ceiling,
        )
        self.policies[policy_id] = policy
        return policy

    def check_permission(self, principal: str, capability: str, action: str) -> Tuple[bool, str]:
        for policy in self.policies.values():
            if policy.principal in (principal, "*"):
                if policy.target_capability in (capability, "*"):
                    if action in policy.allowed_actions or "*" in policy.allowed_actions:
                        return True, f"Authorized by policy {policy.policy_id}"
        return False, f"Permission denied for principal '{principal}' performing action '{action}' on '{capability}'"
