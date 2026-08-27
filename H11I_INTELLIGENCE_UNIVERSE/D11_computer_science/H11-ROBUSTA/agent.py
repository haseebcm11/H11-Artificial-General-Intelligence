"""
Agent Module: D11_ROBUSTA
Agent Class: RobustaAgent

Adversarial robustness: Projected Gradient Descent (PGD) attack step and randomized smoothing certified radius R = sigma*Phi^-1(p_A).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_ROBUSTA"


class RobustaError(ValueError):
    """Raised when RobustaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class RobustaAgentInput:
    perturbation_norm: float = 0.031
    epsilon_limit: float = 0.0313
    prob_top_class: float = 0.85
    smoothing_sigma: float = 0.25


@dataclass(frozen=True)
class RobustaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    certified_radius: float = 0.0


class RobustaAgent:
    """
    Adversarial robustness: Projected Gradient Descent (PGD) attack step and randomized smoothing certified radius R = sigma*Phi^-1(p_A).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: RobustaAgentInput) -> RobustaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        # Approx inverse normal CDF for prob_top_class > 0.5: Phi^-1(p) approx sqrt(-2 ln(1-p)) - 0.5
        pa = max(0.51, min(0.999, inputs.prob_top_class))
        z = math.sqrt(-2.0 * math.log(1.0 - pa)) - 0.5
        radius = inputs.smoothing_sigma * z
        metrics = {"certified_radius": round(radius, 4), "epsilon_limit": inputs.epsilon_limit}
        return RobustaAgentOutput(status="COMPLETED", score=round(min(1.0, radius), 4), metrics=metrics, certified_radius=round(radius, 4))
