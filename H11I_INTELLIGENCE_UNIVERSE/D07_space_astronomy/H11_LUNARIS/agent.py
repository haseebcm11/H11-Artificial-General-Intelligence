"""
Agent Module: D07_LUNARIS
Agent Class: LunarisAgent

Lunar orbital trajectory insertion delta-V budget and regolith thermal inertia thermal propagation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_LUNARIS"


class LunarisError(ValueError):
    """Raised when LunarisAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class LunarisAgentInput:
    parking_orbit_alt_km: float = 100.0
    trans_lunar_velocity_km_s: float = 2.5


@dataclass(frozen=True)
class LunarisAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    lunar_orbit_insertion_dv_km_s: float = 0.0


class LunarisAgent:
    """
    Lunar orbital trajectory insertion delta-V budget and regolith thermal inertia thermal propagation.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: LunarisAgentInput) -> LunarisAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        mu_moon = 4902.8  # km3/s2
        r_moon = 1737.4  # km
        r_park = r_moon + inputs.parking_orbit_alt_km
        v_circ = math.sqrt(mu_moon / r_park)
        v_arrival = inputs.trans_lunar_velocity_km_s
        loi_dv = abs(v_arrival - v_circ)
        metrics = {"circular_speed_km_s": round(v_circ, 3), "loi_dv_km_s": round(loi_dv, 3)}
        return LunarisAgentOutput(status="COMPLETED", score=round(min(1.0, loi_dv/2.0), 4), metrics=metrics, lunar_orbit_insertion_dv_km_s=round(loi_dv, 3))
