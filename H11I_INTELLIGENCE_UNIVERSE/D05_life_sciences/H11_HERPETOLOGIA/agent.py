"""
Agent Module: D05_HERPETOLOGIA
Agent Class: HerpetologiaAgent

Herpetological thermal biology modeling thermal performance curves P(T) = exp(-((T-T_opt)/2sigma)^2) and Thermal Safety Margins (TSM).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_HERPETOLOGIA"


class HerpetologiaError(ValueError):
    """Raised when HerpetologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class HerpetologiaAgentInput:
    body_temp: float = 28.0
    opt_temp: float = 30.0
    ct_max: float = 38.0
    sigma: float = 4.0


@dataclass(frozen=True)
class HerpetologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    performance_index: float = 0.0
    thermal_safety_margin: float = 0.0


class HerpetologiaAgent:
    """
    Herpetological thermal biology modeling thermal performance curves P(T) = exp(-((T-T_opt)/2sigma)^2) and Thermal Safety Margins (TSM).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: HerpetologiaAgentInput) -> HerpetologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        tb, to, ct, sig = inputs.body_temp, inputs.opt_temp, inputs.ct_max, inputs.sigma
        perf = math.exp(-((tb - to) / (2.0 * sig))**2)
        tsm = ct - tb
        score = round(perf, 4)
        metrics = {"performance_index": round(perf, 4), "thermal_safety_margin": round(tsm, 2), "critical_thermal_max": ct}
        return HerpetologiaAgentOutput(status="COMPLETED", score=score, metrics=metrics, performance_index=round(perf, 4), thermal_safety_margin=round(tsm, 2))
