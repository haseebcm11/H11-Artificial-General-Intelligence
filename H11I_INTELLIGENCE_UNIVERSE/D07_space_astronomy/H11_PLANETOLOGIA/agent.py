"""
Agent Module: D07_PLANETOLOGIA
Agent Class: PlanetologiaAgent

Planetary structure hydrostatic equilibrium dP/dr = -rho*g, scale height H = kB*T/(mu*g), and escape velocity v_esc = sqrt(2GM/R).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_PLANETOLOGIA"


class PlanetologiaError(ValueError):
    """Raised when PlanetologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class PlanetologiaAgentInput:
    planet_mass_kg: float = 5.972e24
    planet_radius_m: float = 6.371e6
    temp_k: float = 288.0
    mean_molecular_weight_g_mol: float = 28.97


@dataclass(frozen=True)
class PlanetologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    surface_gravity_m_s2: float = 0.0
    escape_velocity_km_s: float = 0.0
    scale_height_km: float = 0.0


class PlanetologiaAgent:
    """
    Planetary structure hydrostatic equilibrium dP/dr = -rho*g, scale height H = kB*T/(mu*g), and escape velocity v_esc = sqrt(2GM/R).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: PlanetologiaAgentInput) -> PlanetologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        m, r, t, mw = inputs.planet_mass_kg, inputs.planet_radius_m, inputs.temp_k, inputs.mean_molecular_weight_g_mol
        g_const = 6.6743e-11
        g_surf = (g_const * m) / (r**2)
        v_esc = math.sqrt(2.0 * g_const * m / r) / 1000.0
        r_gas = 8.314
        mu_kg = mw / 1000.0
        h_scale_km = (r_gas * t) / (mu_kg * g_surf) / 1000.0
        metrics = {"surface_gravity": round(g_surf, 2), "escape_velocity_km_s": round(v_esc, 2), "scale_height_km": round(h_scale_km, 2)}
        return PlanetologiaAgentOutput(status="COMPLETED", score=round(min(1.0, g_surf/20.0), 4), metrics=metrics, surface_gravity_m_s2=round(g_surf, 2), escape_velocity_km_s=round(v_esc, 2), scale_height_km=round(h_scale_km, 2))
