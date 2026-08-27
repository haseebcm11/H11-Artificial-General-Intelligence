"""
Agent Module: D10_PROBABILITAS
Agent Class: ProbabilitasAgent

Stochastic Poisson process arrival probability P(k) = (lambda*t)^k * exp(-lambda*t) / k! and stationary Markov distributions.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D10_PROBABILITAS"


class ProbabilitasError(ValueError):
    """Raised when ProbabilitasAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ProbabilitasAgentInput:
    rate_lambda: float = 3.0
    time_t: float = 2.0
    k_events: int = 5


@dataclass(frozen=True)
class ProbabilitasAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    poisson_prob: float = 0.0


class ProbabilitasAgent:
    """
    Stochastic Poisson process arrival probability P(k) = (lambda*t)^k * exp(-lambda*t) / k! and stationary Markov distributions.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ProbabilitasAgentInput) -> ProbabilitasAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        lam, t, k = inputs.rate_lambda, inputs.time_t, inputs.k_events
        mu = lam * t
        prob = (mu**k) * math.exp(-mu) / math.factorial(k)
        metrics = {"poisson_prob": round(prob, 5), "mean_events": mu}
        return ProbabilitasAgentOutput(status="COMPLETED", score=round(prob, 4), metrics=metrics, poisson_prob=round(prob, 5))
