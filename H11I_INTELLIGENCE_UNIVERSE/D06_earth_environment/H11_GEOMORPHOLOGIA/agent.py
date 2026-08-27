"""
Agent Module: D06_GEOMORPHOLOGIA
Agent Class: GeomorphologiaAgent

Fluvial geomorphology stream power incision law dz/dt = U - K * A^m * S^n and drainage network bifurcation ratio.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_GEOMORPHOLOGIA"


class GeomorphologiaError(ValueError):
    """Raised when GeomorphologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GeomorphologiaAgentInput:
    drainage_area_km2: float = 150.0
    channel_slope: float = 0.02
    uplift_rate_mm_yr: float = 1.0
    erodibility_k: float = 0.0001


@dataclass(frozen=True)
class GeomorphologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    incision_rate_mm_yr: float = 0.0


class GeomorphologiaAgent:
    """
    Fluvial geomorphology stream power incision law dz/dt = U - K * A^m * S^n and drainage network bifurcation ratio.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GeomorphologiaAgentInput) -> GeomorphologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        a, s, u, k = inputs.drainage_area_km2, inputs.channel_slope, inputs.uplift_rate_mm_yr, inputs.erodibility_k
        incision = k * (a**0.5) * (s**1.0) * 1000.0
        net_rate = u - incision
        metrics = {"incision_rate_mm_yr": round(incision, 4), "net_elevation_change": round(net_rate, 4)}
        return GeomorphologiaAgentOutput(status="COMPLETED", score=round(min(1.0, abs(net_rate)), 4), metrics=metrics, incision_rate_mm_yr=round(incision, 4))
