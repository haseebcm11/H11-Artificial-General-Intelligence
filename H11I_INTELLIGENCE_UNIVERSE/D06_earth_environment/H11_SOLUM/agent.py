"""
Agent Module: D06_SOLUM
Agent Class: SolumAgent

Soil physics and hydrology modeling van Genuchten water retention curve theta(h) and USDA textural classification.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_SOLUM"


class SolumError(ValueError):
    """Raised when SolumAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SolumAgentInput:
    sand_percent: float = 40.0
    silt_percent: float = 40.0
    clay_percent: float = 20.0
    suction_head_cm: float = 100.0


@dataclass(frozen=True)
class SolumAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    volumetric_water_content: float = 0.0
    soil_class: str = 'Loam'


class SolumAgent:
    """
    Soil physics and hydrology modeling van Genuchten water retention curve theta(h) and USDA textural classification.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SolumAgentInput) -> SolumAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        sand, silt, clay = inputs.sand_percent, inputs.silt_percent, inputs.clay_percent
        s_class = "Loam"
        if clay >= 40: s_class = "Clay"
        elif sand >= 70: s_class = "Sand"
        elif silt >= 80: s_class = "Silt"
        # van Genuchten approx parameters for loam: theta_r=0.078, theta_s=0.43, alpha=0.036, n=1.56
        tr, ts, a, n = 0.078, 0.43, 0.036, 1.56
        m = 1.0 - 1.0/n
        h = inputs.suction_head_cm
        theta = tr + (ts - tr) / ((1.0 + (a * h)**n)**m)
        metrics = {"volumetric_water": round(theta, 4), "sand": sand, "silt": silt, "clay": clay}
        return SolumAgentOutput(status="COMPLETED", score=round(theta, 4), metrics=metrics, volumetric_water_content=round(theta, 4), soil_class=s_class)
