"""
Agent Module: L12_UNCERTAINTY
Agent Class: UncertaintyAgent

Epistemic vs aleatoric uncertainty quantification via ensemble variance decomposition sigma_total^2 = E[sigma_i^2] + Var(mu_i).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L12_UNCERTAINTY"


class UncertaintyError(ValueError):
    """Raised when UncertaintyAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class UncertaintyAgentInput:
    ensemble_means: list[float] = field(default_factory=lambda: [2.1, 2.3, 2.0, 2.4, 2.2])
    ensemble_variances: list[float] = field(default_factory=lambda: [0.1, 0.12, 0.09, 0.11, 0.1])


@dataclass(frozen=True)
class UncertaintyAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    epistemic_uncertainty: float = 0.0
    aleatoric_uncertainty: float = 0.0


class UncertaintyAgent:
    """
    Epistemic vs aleatoric uncertainty quantification via ensemble variance decomposition sigma_total^2 = E[sigma_i^2] + Var(mu_i).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: UncertaintyAgentInput) -> UncertaintyAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        means = inputs.ensemble_means if inputs.ensemble_means else [1.0, 1.1]
        vars_ = inputs.ensemble_variances if inputs.ensemble_variances else [0.1, 0.1]
        mean_of_means = sum(means) / len(means)
        epistemic = sum((m - mean_of_means)**2 for m in means) / len(means)
        aleatoric = sum(vars_) / len(vars_)
        score = max(0.0, 1.0 - min(1.0, epistemic + aleatoric))
        metrics = {"epistemic": round(epistemic, 6), "aleatoric": round(aleatoric, 6), "total_variance": round(epistemic + aleatoric, 6)}
        return UncertaintyAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, epistemic_uncertainty=round(epistemic, 6), aleatoric_uncertainty=round(aleatoric, 6))
