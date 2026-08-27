"""
Agent Module: D05_BOTANICA
Agent Class: BotanicaAgent

Farquhar-von Caemmerer-Berry (FvCB) model of C3 photosynthesis calculating Rubisco-limited Ac and RuBP-regeneration limited Aj assimilation rates.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_BOTANICA"


class BotanicaError(ValueError):
    """Raised when BotanicaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class BotanicaAgentInput:
    vcmax: float = 80.0
    jmax: float = 140.0
    ci: float = 250.0
    gamma_star: float = 42.0
    rd: float = 1.5


@dataclass(frozen=True)
class BotanicaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    net_assimilation: float = 0.0


class BotanicaAgent:
    """
    Farquhar-von Caemmerer-Berry (FvCB) model of C3 photosynthesis calculating Rubisco-limited Ac and RuBP-regeneration limited Aj assimilation rates.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: BotanicaAgentInput) -> BotanicaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        vc, jm, ci, gs, rd = inputs.vcmax, inputs.jmax, inputs.ci, inputs.gamma_star, inputs.rd
        kc, ko, oi = 404.0, 248.0, 210.0
        km = kc * (1.0 + oi / ko)
        ac = vc * (ci - gs) / (ci + km)
        aj = (jm / 4.0) * (ci - gs) / (ci + 2.0 * gs)
        a_net = max(0.0, min(ac, aj) - rd)
        score = min(1.0, round(a_net / 30.0, 4))
        metrics = {"ac_rubisco_rate": round(ac, 4), "aj_light_rate": round(aj, 4), "net_assimilation": round(a_net, 4)}
        return BotanicaAgentOutput(status="COMPLETED", score=score, metrics=metrics, net_assimilation=round(a_net, 4))
