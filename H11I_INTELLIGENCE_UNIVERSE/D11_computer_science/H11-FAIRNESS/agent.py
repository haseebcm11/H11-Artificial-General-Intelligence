"""
Agent Module: D11_FAIRNESS
Agent Class: FairnessAgent

Algorithmic fairness Demographic Parity difference |P(Y_hat=1|A=0) - P(Y_hat=1|A=1)| and Equalized Odds violations.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_FAIRNESS"


class FairnessError(ValueError):
    """Raised when FairnessAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class FairnessAgentInput:
    acceptance_rate_group0: float = 0.72
    acceptance_rate_group1: float = 0.68
    tpr_group0: float = 0.85
    tpr_group1: float = 0.82


@dataclass(frozen=True)
class FairnessAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    demographic_parity_diff: float = 0.0
    equal_opportunity_diff: float = 0.0


class FairnessAgent:
    """
    Algorithmic fairness Demographic Parity difference |P(Y_hat=1|A=0) - P(Y_hat=1|A=1)| and Equalized Odds violations.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: FairnessAgentInput) -> FairnessAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        dp_diff = abs(inputs.acceptance_rate_group0 - inputs.acceptance_rate_group1)
        eo_diff = abs(inputs.tpr_group0 - inputs.tpr_group1)
        fair_score = max(0.0, 1.0 - (dp_diff + eo_diff))
        metrics = {"dp_diff": round(dp_diff, 4), "eo_diff": round(eo_diff, 4), "fairness_score": round(fair_score, 4)}
        return FairnessAgentOutput(status="COMPLETED", score=round(fair_score, 4), metrics=metrics, demographic_parity_diff=round(dp_diff, 4), equal_opportunity_diff=round(eo_diff, 4))
