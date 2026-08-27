"""
Agent Module: D06_PALEONTOLOGIA
Agent Class: PaleontologiaAgent

Biostratigraphic fossil record survivorship curve N(t) = N_0 * exp(-lambda * t) and extinction rate analytics.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_PALEONTOLOGIA"


class PaleontologiaError(ValueError):
    """Raised when PaleontologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class PaleontologiaAgentInput:
    initial_taxa: int = 100
    extinction_rate_per_myr: float = 0.05
    duration_myr: float = 20.0


@dataclass(frozen=True)
class PaleontologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    surviving_taxa: float = 0.0
    half_life_myr: float = 0.0


class PaleontologiaAgent:
    """
    Biostratigraphic fossil record survivorship curve N(t) = N_0 * exp(-lambda * t) and extinction rate analytics.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: PaleontologiaAgentInput) -> PaleontologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n0, lam, t = inputs.initial_taxa, inputs.extinction_rate_per_myr, inputs.duration_myr
        surv = n0 * math.exp(-lam * t)
        half_life = math.log(2.0) / max(lam, 1e-6)
        metrics = {"surviving_taxa": round(surv, 1), "extinction_fraction": round(1.0 - surv/n0, 4), "half_life_myr": round(half_life, 2)}
        return PaleontologiaAgentOutput(status="COMPLETED", score=round(surv/n0, 4), metrics=metrics, surviving_taxa=round(surv, 1), half_life_myr=round(half_life, 2))
