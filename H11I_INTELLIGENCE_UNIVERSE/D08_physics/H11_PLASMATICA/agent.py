"""
Agent Module: D08_PLASMATICA
Agent Class: PlasmaticaAgent

Plasma physics Debye screening length lambda_D = sqrt(eps0*kB*Te / (ne*e^2)) and electron plasma frequency omega_pe.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_PLASMATICA"


class PlasmaticaError(ValueError):
    """Raised when PlasmaticaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class PlasmaticaAgentInput:
    electron_density_m3: float = 1e20
    electron_temp_ev: float = 100.0


@dataclass(frozen=True)
class PlasmaticaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    debye_length_um: float = 0.0
    plasma_freq_ghz: float = 0.0


class PlasmaticaAgent:
    """
    Plasma physics Debye screening length lambda_D = sqrt(eps0*kB*Te / (ne*e^2)) and electron plasma frequency omega_pe.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: PlasmaticaAgentInput) -> PlasmaticaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        ne, te_ev = inputs.electron_density_m3, inputs.electron_temp_ev
        eps0, q, m_e = 8.854e-12, 1.602e-19, 9.109e-31
        te_j = te_ev * q
        lam_d = math.sqrt((eps0 * te_j) / (ne * (q**2)))
        omega_pe = math.sqrt((ne * (q**2)) / (eps0 * m_e))
        f_pe_ghz = (omega_pe / (2.0 * math.pi)) / 1e9
        metrics = {"debye_length_um": round(lam_d * 1e6, 3), "plasma_frequency_ghz": round(f_pe_ghz, 2)}
        return PlasmaticaAgentOutput(status="COMPLETED", score=round(min(1.0, f_pe_ghz/100.0), 4), metrics=metrics, debye_length_um=round(lam_d * 1e6, 3), plasma_freq_ghz=round(f_pe_ghz, 2))
