"""
Agent Module: D12_CLOUDSEC
Agent Class: CloudsecAgent

Cloud security IAM policy evaluation decision matrix and Cloud Security Posture Management (CSPM) compliance scoring.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D12_CLOUDSEC"


class CloudsecError(ValueError):
    """Raised when CloudsecAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CloudsecAgentInput:
    allowed_actions_count: int = 14
    excess_permissions_count: int = 3
    total_resources: int = 50


@dataclass(frozen=True)
class CloudsecAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    least_privilege_index: float = 0.0


class CloudsecAgent:
    """
    Cloud security IAM policy evaluation decision matrix and Cloud Security Posture Management (CSPM) compliance scoring.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CloudsecAgentInput) -> CloudsecAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        excess_ratio = inputs.excess_permissions_count / max(inputs.allowed_actions_count, 1)
        lp_index = max(0.0, 1.0 - excess_ratio)
        metrics = {"least_privilege_index": round(lp_index, 3), "excess_ratio": round(excess_ratio, 3)}
        return CloudsecAgentOutput(status="COMPLETED", score=round(lp_index, 4), metrics=metrics, least_privilege_index=round(lp_index, 3))
