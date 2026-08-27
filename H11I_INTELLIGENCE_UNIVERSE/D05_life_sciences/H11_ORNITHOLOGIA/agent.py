"""
Agent Module: D05_ORNITHOLOGIA
Agent Class: OrnithologiaAgent

Avian aerodynamics and flight energetics calculating induced power, parasite power, profile power, and minimum power velocity Vmp.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_ORNITHOLOGIA"


class OrnithologiaError(ValueError):
    """Raised when OrnithologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class OrnithologiaAgentInput:
    mass_kg: float = 0.3
    wingspan_m: float = 0.8
    wing_area_m2: float = 0.06
    velocity_m_s: float = 12.0


@dataclass(frozen=True)
class OrnithologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    total_power_watts: float = 0.0


class OrnithologiaAgent:
    """
    Avian aerodynamics and flight energetics calculating induced power, parasite power, profile power, and minimum power velocity Vmp.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: OrnithologiaAgentInput) -> OrnithologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        m, b, s, v = inputs.mass_kg, inputs.wingspan_m, inputs.wing_area_m2, inputs.velocity_m_s
        rho, g = 1.225, 9.81
        weight = m * g
        # Induced power = 2 k W^2 / (pi rho V b^2)
        p_ind = (2.0 * 1.2 * (weight**2)) / (math.pi * rho * max(v, 1e-6) * (b**2))
        # Parasite power = 0.5 rho V^3 S_body C_par
        p_par = 0.5 * rho * (v**3) * (s * 0.05)
        # Profile power = 0.5 rho V^3 S C_pro
        p_pro = 0.5 * rho * (v**3) * s * 0.02
        p_tot = p_ind + p_par + p_pro
        v_mp = math.sqrt((2.0 * weight) / (rho * math.sqrt(math.pi * (b**2) * s * 0.05)))
        metrics = {"induced_power_w": round(p_ind, 2), "parasite_power_w": round(p_par, 2), "total_power_w": round(p_tot, 2), "min_power_velocity_ms": round(v_mp, 2)}
        return OrnithologiaAgentOutput(status="COMPLETED", score=round(min(1.0, 50.0/max(p_tot, 1.0)), 4), metrics=metrics, total_power_watts=round(p_tot, 2))
