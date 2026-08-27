"""
Agent Module: D07_SATELLITIS
Agent Class: SatellitisAgent

Satellite orbital perturbations J2 nodal precession rate dot(Omega) = -1.5*J2*(R_E/p)^2 * n * cos(i) and orbital period.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_SATELLITIS"


class SatellitisError(ValueError):
    """Raised when SatellitisAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SatellitisAgentInput:
    altitude_km: float = 700.0
    inclination_deg: float = 98.2


@dataclass(frozen=True)
class SatellitisAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    orbital_period_minutes: float = 0.0
    nodal_precession_deg_day: float = 0.0


class SatellitisAgent:
    """
    Satellite orbital perturbations J2 nodal precession rate dot(Omega) = -1.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SatellitisAgentInput) -> SatellitisAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        r_earth = 6378.137
        mu = 398600.4418
        j2 = 1.08263e-3
        a = r_earth + inputs.altitude_km
        period_s = 2.0 * math.pi * math.sqrt(a**3 / mu)
        period_min = period_s / 60.0
        n = 2.0 * math.pi / period_s
        inc_rad = math.radians(inputs.inclination_deg)
        prec_rad_s = -1.5 * j2 * ((r_earth / a)**2) * n * math.cos(inc_rad)
        prec_deg_day = math.degrees(prec_rad_s) * 86400.0
        metrics = {"period_min": round(period_min, 2), "precession_deg_day": round(prec_deg_day, 4)}
        return SatellitisAgentOutput(status="COMPLETED", score=round(min(1.0, period_min/120.0), 4), metrics=metrics, orbital_period_minutes=round(period_min, 2), nodal_precession_deg_day=round(prec_deg_day, 4))
