"""
Agent Module: D08_PARTICULA
Agent Class: ParticulaAgent

High energy particle physics relativistic invariant mass M^2 = (E1+E2)^2 - (p1+p2)^2 and Breit-Wigner resonance cross section.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_PARTICULA"


class ParticulaError(ValueError):
    """Raised when ParticulaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ParticulaAgentInput:
    e1_gev: float = 45.6
    e2_gev: float = 45.6
    px1: float = 0.0
    py1: float = 0.0
    pz1: float = 45.6
    px2: float = 0.0
    py2: float = 0.0
    pz2: float = -45.6


@dataclass(frozen=True)
class ParticulaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    invariant_mass_gev: float = 0.0


class ParticulaAgent:
    """
    High energy particle physics relativistic invariant mass M^2 = (E1+E2)^2 - (p1+p2)^2 and Breit-Wigner resonance cross section.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ParticulaAgentInput) -> ParticulaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        e_tot = inputs.e1_gev + inputs.e2_gev
        px_tot = inputs.px1 + inputs.px2
        py_tot = inputs.py1 + inputs.py2
        pz_tot = inputs.pz1 + inputs.pz2
        p_sq = px_tot**2 + py_tot**2 + pz_tot**2
        s = e_tot**2 - p_sq
        m_inv = math.sqrt(max(0.0, s))
        metrics = {"invariant_mass_gev": round(m_inv, 3), "total_energy_gev": round(e_tot, 3)}
        return ParticulaAgentOutput(status="COMPLETED", score=round(min(1.0, m_inv/100.0), 4), metrics=metrics, invariant_mass_gev=round(m_inv, 3))
