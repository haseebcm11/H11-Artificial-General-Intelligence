"""
Agent Module: D07_HELIOPHYSICA
Agent Class: HeliophysicaAgent

Solar wind magnetohydrodynamics Parker spiral magnetic field topology B_phi/B_r = -Omega*r / v_sw and space weather flares.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_HELIOPHYSICA"


class HeliophysicaError(ValueError):
    """Raised when HeliophysicaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class HeliophysicaAgentInput:
    solar_wind_speed_km_s: float = 450.0
    heliocentric_dist_au: float = 1.0
    solar_rotation_rad_s: float = 2.87e-6


@dataclass(frozen=True)
class HeliophysicaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    spiral_angle_degrees: float = 0.0


class HeliophysicaAgent:
    """
    Solar wind magnetohydrodynamics Parker spiral magnetic field topology B_phi/B_r = -Omega*r / v_sw and space weather flares.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: HeliophysicaAgentInput) -> HeliophysicaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        v_sw, r_au, omega = inputs.solar_wind_speed_km_s, inputs.heliocentric_dist_au, inputs.solar_rotation_rad_s
        r_km = r_au * 1.496e8
        tan_psi = (omega * r_km) / max(v_sw, 1.0)
        psi_deg = math.degrees(math.atan(tan_psi))
        metrics = {"spiral_angle_deg": round(psi_deg, 2), "solar_wind_km_s": v_sw, "distance_au": r_au}
        return HeliophysicaAgentOutput(status="COMPLETED", score=round(psi_deg/90.0, 4), metrics=metrics, spiral_angle_degrees=round(psi_deg, 2))
