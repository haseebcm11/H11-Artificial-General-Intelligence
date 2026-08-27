"""
Agent Module: D06_POLLUTIO
Agent Class: PollutioAgent

Gaussian plume atmospheric pollutant dispersion C(x,y,z) modeling and Air Quality Index (AQI) boundary conversions.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_POLLUTIO"


class PollutioError(ValueError):
    """Raised when PollutioAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class PollutioAgentInput:
    emission_rate_g_s: float = 100.0
    wind_speed_m_s: float = 4.0
    downwind_dist_m: float = 1000.0
    crosswind_dist_m: float = 50.0
    stack_height_m: float = 30.0


@dataclass(frozen=True)
class PollutioAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    ground_level_conc_mg_m3: float = 0.0


class PollutioAgent:
    """
    Gaussian plume atmospheric pollutant dispersion C(x,y,z) modeling and Air Quality Index (AQI) boundary conversions.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: PollutioAgentInput) -> PollutioAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        q, u, x, y, h = inputs.emission_rate_g_s, max(inputs.wind_speed_m_s, 0.5), inputs.downwind_dist_m, inputs.crosswind_dist_m, inputs.stack_height_m
        # Pasquill-Gifford stability class D dispersion coefficients
        sig_y = 0.08 * x * (1.0 + 0.0001 * x)**(-0.5)
        sig_z = 0.06 * x * (1.0 + 0.0015 * x)**(-0.5)
        c = (q / (2.0 * math.pi * u * sig_y * sig_z)) * math.exp(-(y**2)/(2.0 * sig_y**2)) * (2.0 * math.exp(-(h**2)/(2.0 * sig_z**2)))
        c_mg = c * 1000.0
        score = max(0.0, 1.0 - min(1.0, c_mg / 10.0))
        metrics = {"conc_mg_m3": round(c_mg, 4), "sigma_y": round(sig_y, 2), "sigma_z": round(sig_z, 2)}
        return PollutioAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, ground_level_conc_mg_m3=round(c_mg, 4))
