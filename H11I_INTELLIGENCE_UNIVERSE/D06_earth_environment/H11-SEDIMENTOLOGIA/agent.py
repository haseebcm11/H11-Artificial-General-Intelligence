"""
Agent Module: D06_SEDIMENTOLOGIA
Agent Class: SedimentologiaAgent

Sediment grain transport via Stokes' Law settling velocity w_s = (rho_s - rho)*g*d^2 / (18*mu) and Folk-Ward phi scale stats.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_SEDIMENTOLOGIA"


class SedimentologiaError(ValueError):
    """Raised when SedimentologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SedimentologiaAgentInput:
    grain_diameter_mm: float = 0.2
    grain_density_kg_m3: float = 2650.0


@dataclass(frozen=True)
class SedimentologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    settling_velocity_m_s: float = 0.0
    phi_size: float = 0.0


class SedimentologiaAgent:
    """
    Sediment grain transport via Stokes' Law settling velocity w_s = (rho_s - rho)*g*d^2 / (18*mu) and Folk-Ward phi scale stats.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SedimentologiaAgentInput) -> SedimentologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        d_m = inputs.grain_diameter_mm / 1000.0
        rho_s, rho, mu, g = inputs.grain_density_kg_m3, 1000.0, 0.001, 9.81
        ws = ((rho_s - rho) * g * (d_m**2)) / (18.0 * mu)
        phi = -math.log2(inputs.grain_diameter_mm)
        metrics = {"settling_velocity_ms": round(ws, 4), "phi_scale": round(phi, 2)}
        return SedimentologiaAgentOutput(status="COMPLETED", score=round(min(1.0, ws * 10.0), 4), metrics=metrics, settling_velocity_m_s=round(ws, 4), phi_size=round(phi, 2))
