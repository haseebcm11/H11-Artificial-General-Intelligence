"""
Agent Module: D06_CLIMATOLOGIA
Agent Class: ClimatologiaAgent

Planetary radiative equilibrium temperature T_e = ((S_0*(1-alpha))/(4*sigma))^0.25 and climate feedback sensitivity delta T = lambda * delta F.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_CLIMATOLOGIA"


class ClimatologiaError(ValueError):
    """Raised when ClimatologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ClimatologiaAgentInput:
    solar_constant: float = 1361.0
    albedo: float = 0.3
    greenhouse_warming_k: float = 33.0


@dataclass(frozen=True)
class ClimatologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    effective_temp_k: float = 0.0
    surface_temp_k: float = 0.0


class ClimatologiaAgent:
    """
    Planetary radiative equilibrium temperature T_e = ((S_0*(1-alpha))/(4*sigma))^0.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ClimatologiaAgentInput) -> ClimatologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        s0, alpha = inputs.solar_constant, inputs.albedo
        sigma = 5.670374e-8
        t_eff = ((s0 * (1.0 - alpha)) / (4.0 * sigma))**0.25
        t_surf = t_eff + inputs.greenhouse_warming_k
        metrics = {"effective_temp_k": round(t_eff, 2), "surface_temp_k": round(t_surf, 2), "surface_temp_c": round(t_surf - 273.15, 2)}
        return ClimatologiaAgentOutput(status="COMPLETED", score=round(min(1.0, t_eff/300.0), 4), metrics=metrics, effective_temp_k=round(t_eff, 2), surface_temp_k=round(t_surf, 2))
