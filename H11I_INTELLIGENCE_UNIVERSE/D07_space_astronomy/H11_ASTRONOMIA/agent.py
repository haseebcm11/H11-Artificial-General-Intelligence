"""
Agent Module: D07_ASTRONOMIA
Agent Class: AstronomiaAgent

Astronomical observation optics calculating stellar absolute magnitude M = m - 5*log10(d/10) and Rayleigh diffraction limit theta = 1.22*lambda/D.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_ASTRONOMIA"


class AstronomiaError(ValueError):
    """Raised when AstronomiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class AstronomiaAgentInput:
    apparent_magnitude: float = 4.5
    distance_parsecs: float = 32.6
    telescope_diam_m: float = 2.4
    wavelength_nm: float = 550.0


@dataclass(frozen=True)
class AstronomiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    absolute_magnitude: float = 0.0
    angular_resolution_arcsec: float = 0.0


class AstronomiaAgent:
    """
    Astronomical observation optics calculating stellar absolute magnitude M = m - 5*log10(d/10) and Rayleigh diffraction limit theta = 1.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: AstronomiaAgentInput) -> AstronomiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        m, d, d_tel, lam_nm = inputs.apparent_magnitude, inputs.distance_parsecs, inputs.telescope_diam_m, inputs.wavelength_nm
        m_abs = m - 5.0 * (math.log10(max(d, 0.1)) - 1.0)
        theta_rad = 1.22 * (lam_nm * 1e-9) / max(d_tel, 0.01)
        theta_arcsec = math.degrees(theta_rad) * 3600.0
        metrics = {"absolute_magnitude": round(m_abs, 2), "angular_resolution_arcsec": round(theta_arcsec, 4), "distance_modulus": round(m - m_abs, 2)}
        return AstronomiaAgentOutput(status="COMPLETED", score=round(min(1.0, 1.0/max(theta_arcsec, 0.01)), 4), metrics=metrics, absolute_magnitude=round(m_abs, 2), angular_resolution_arcsec=round(theta_arcsec, 4))
