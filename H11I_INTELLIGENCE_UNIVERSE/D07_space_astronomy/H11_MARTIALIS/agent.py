"""
Agent Module: D07_MARTIALIS
Agent Class: MartialisAgent

Martian atmospheric entry, descent, and landing (EDL) density profile rho(z) = rho_0 * exp(-z/H) and ballistic coefficient beta = m/(Cd*A).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_MARTIALIS"


class MartialisError(ValueError):
    """Raised when MartialisAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class MartialisAgentInput:
    vehicle_mass_kg: float = 1000.0
    drag_area_m2: float = 4.5
    drag_coefficient: float = 1.4
    altitude_km: float = 10.0


@dataclass(frozen=True)
class MartialisAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    ballistic_coefficient_kg_m2: float = 0.0
    atmospheric_density_kg_m3: float = 0.0


class MartialisAgent:
    """
    Martian atmospheric entry, descent, and landing (EDL) density profile rho(z) = rho_0 * exp(-z/H) and ballistic coefficient beta = m/(Cd*A).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: MartialisAgentInput) -> MartialisAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        m, a, cd, z = inputs.vehicle_mass_kg, inputs.drag_area_m2, inputs.drag_coefficient, inputs.altitude_km
        beta = m / (cd * a)
        rho0, h_scale = 0.020, 11.1  # Mars surface density (kg/m3) and scale height (km)
        rho = rho0 * math.exp(-z / h_scale)
        v_terminal = math.sqrt((2.0 * m * 3.72) / (cd * a * max(rho, 1e-6)))
        metrics = {"ballistic_coeff": round(beta, 2), "density_kg_m3": round(rho, 6), "terminal_velocity_ms": round(v_terminal, 1)}
        return MartialisAgentOutput(status="COMPLETED", score=round(min(1.0, 500.0/max(v_terminal, 1.0)), 4), metrics=metrics, ballistic_coefficient_kg_m2=round(beta, 2), atmospheric_density_kg_m3=round(rho, 6))
