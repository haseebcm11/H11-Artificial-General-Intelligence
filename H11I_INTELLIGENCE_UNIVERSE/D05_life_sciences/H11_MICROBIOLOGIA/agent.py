"""
Agent Module: D05_MICROBIOLOGIA
Agent Class: MicrobiologiaAgent

Microbial growth kinetics via Monod equation mu = mu_max * S / (Ks + S) and doubling time td = ln(2)/mu.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_MICROBIOLOGIA"


class MicrobiologiaError(ValueError):
    """Raised when MicrobiologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class MicrobiologiaAgentInput:
    substrate_conc: float = 5.0
    mu_max: float = 0.8
    ks: float = 1.2
    initial_cfu: float = 1000.0
    time_hours: float = 4.0


@dataclass(frozen=True)
class MicrobiologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    specific_growth_rate: float = 0.0
    final_cfu: float = 0.0


class MicrobiologiaAgent:
    """
    Microbial growth kinetics via Monod equation mu = mu_max * S / (Ks + S) and doubling time td = ln(2)/mu.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: MicrobiologiaAgentInput) -> MicrobiologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        s, mu_m, ks = inputs.substrate_conc, inputs.mu_max, inputs.ks
        mu = (mu_m * s) / (ks + s)
        td = math.log(2.0) / max(mu, 1e-6)
        cfu_final = inputs.initial_cfu * math.exp(mu * inputs.time_hours)
        score = min(1.0, round(mu / mu_m, 4))
        metrics = {"specific_growth_rate": round(mu, 4), "doubling_time_hours": round(td, 2), "final_cfu": round(cfu_final, 1)}
        return MicrobiologiaAgentOutput(status="COMPLETED", score=score, metrics=metrics, specific_growth_rate=round(mu, 4), final_cfu=round(cfu_final, 1))
