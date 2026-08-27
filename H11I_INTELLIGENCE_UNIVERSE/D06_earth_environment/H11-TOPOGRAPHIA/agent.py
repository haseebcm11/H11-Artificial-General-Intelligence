"""
Agent Module: D06_TOPOGRAPHIA
Agent Class: TopographiaAgent

Digital Elevation Model (DEM) terrain analytics calculating gradient slope, aspect angle, and Topographic Wetness Index (TWI).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_TOPOGRAPHIA"


class TopographiaError(ValueError):
    """Raised when TopographiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class TopographiaAgentInput:
    dz_dx: float = 0.15
    dz_dy: float = -0.1
    upslope_area_m2: float = 5000.0


@dataclass(frozen=True)
class TopographiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    slope_degrees: float = 0.0
    twi: float = 0.0


class TopographiaAgent:
    """
    Digital Elevation Model (DEM) terrain analytics calculating gradient slope, aspect angle, and Topographic Wetness Index (TWI).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: TopographiaAgentInput) -> TopographiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        fx, fy = inputs.dz_dx, inputs.dz_dy
        slope_rad = math.atan(math.sqrt(fx*fx + fy*fy))
        slope_deg = math.degrees(slope_rad)
        aspect_deg = (math.degrees(math.atan2(fy, -fx)) + 360.0) % 360.0
        tan_b = max(math.tan(slope_rad), 0.001)
        twi = math.log(inputs.upslope_area_m2 / tan_b)
        metrics = {"slope_deg": round(slope_deg, 2), "aspect_deg": round(aspect_deg, 2), "twi": round(twi, 2)}
        return TopographiaAgentOutput(status="COMPLETED", score=round(min(1.0, twi/15.0), 4), metrics=metrics, slope_degrees=round(slope_deg, 2), twi=round(twi, 2))
