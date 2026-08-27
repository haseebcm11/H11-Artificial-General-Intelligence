"""
Agent Module: D07_GALACTICA
Agent Class: GalacticaAgent

Galactic dynamics and dark matter Navarro-Frenk-White (NFW) density profile rho(r) = rho_0 / ((r/rs)*(1+r/rs)^2) rotation curves.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_GALACTICA"


class GalacticaError(ValueError):
    """Raised when GalacticaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GalacticaAgentInput:
    radius_kpc: float = 8.0
    scale_radius_rs: float = 16.0
    rho_0_msun_kpc3: float = 1e7


@dataclass(frozen=True)
class GalacticaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    dark_matter_density: float = 0.0
    circular_velocity_km_s: float = 0.0


class GalacticaAgent:
    """
    Galactic dynamics and dark matter Navarro-Frenk-White (NFW) density profile rho(r) = rho_0 / ((r/rs)*(1+r/rs)^2) rotation curves.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GalacticaAgentInput) -> GalacticaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        r, rs, rho0 = inputs.radius_kpc, inputs.scale_radius_rs, inputs.rho_0_msun_kpc3
        x = r / rs
        rho = rho0 / (x * ((1.0 + x)**2))
        # Enclosed mass M(r) = 4 pi rho0 rs^3 [ln(1+x) - x/(1+x)]
        m_enc = 4.0 * math.pi * rho0 * (rs**3) * (math.log(1.0 + x) - x/(1.0 + x))
        g = 4.30091e-6  # kpc (km/s)^2 / Msun
        v_circ = math.sqrt(g * m_enc / max(r, 0.1))
        metrics = {"dm_density": round(rho, 2), "enclosed_mass_msun": round(m_enc, 1), "v_circ_km_s": round(v_circ, 1)}
        return GalacticaAgentOutput(status="COMPLETED", score=round(min(1.0, v_circ/300.0), 4), metrics=metrics, dark_matter_density=round(rho, 2), circular_velocity_km_s=round(v_circ, 1))
