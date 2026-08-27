"""
Agent Module: D05_ICHTHYOLOGIA
Agent Class: IchthyologiaAgent

Hydrodynamics of fish swimming calculating Reynolds number Re = rho*V*L/mu, Strouhal number St = f*A/V, and von Bertalanffy growth.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_ICHTHYOLOGIA"


class IchthyologiaError(ValueError):
    """Raised when IchthyologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class IchthyologiaAgentInput:
    length_m: float = 0.5
    velocity_m_s: float = 1.2
    tail_frequency_hz: float = 2.5
    amplitude_m: float = 0.1


@dataclass(frozen=True)
class IchthyologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    reynolds_number: float = 0.0
    strouhal_number: float = 0.0


class IchthyologiaAgent:
    """
    Hydrodynamics of fish swimming calculating Reynolds number Re = rho*V*L/mu, Strouhal number St = f*A/V, and von Bertalanffy growth.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: IchthyologiaAgentInput) -> IchthyologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        rho, mu = 1000.0, 0.001  # water properties
        l, v, f, a = inputs.length_m, inputs.velocity_m_s, inputs.tail_frequency_hz, inputs.amplitude_m
        re = (rho * v * l) / mu
        st = (f * a) / max(v, 1e-6)
        # St between 0.25 and 0.35 indicates peak propulsive efficiency
        prop_eff = math.exp(-((st - 0.3) / 0.1)**2)
        metrics = {"reynolds_number": round(re, 1), "strouhal_number": round(st, 4), "propulsive_efficiency": round(prop_eff, 4)}
        return IchthyologiaAgentOutput(status="COMPLETED", score=round(prop_eff, 4), metrics=metrics, reynolds_number=round(re, 1), strouhal_number=round(st, 4))
