"""
Agent Module: D08_CONDENSATA
Agent Class: CondensataAgent

Condensed matter Drude conductivity sigma = n*e^2*tau/m and Fermi-Dirac thermal distribution f(E) = 1/(exp((E-EF)/kBT)+1).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_CONDENSATA"


class CondensataError(ValueError):
    """Raised when CondensataAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CondensataAgentInput:
    carrier_density_m3: float = 8.5e28
    relaxation_time_s: float = 2.5e-14
    fermi_energy_ev: float = 7.0
    energy_ev: float = 7.05
    temp_k: float = 300.0


@dataclass(frozen=True)
class CondensataAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    drude_conductivity_s_m: float = 0.0
    fermi_dirac_prob: float = 0.0


class CondensataAgent:
    """
    Condensed matter Drude conductivity sigma = n*e^2*tau/m and Fermi-Dirac thermal distribution f(E) = 1/(exp((E-EF)/kBT)+1).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CondensataAgentInput) -> CondensataAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n, tau, ef, e, t = inputs.carrier_density_m3, inputs.relaxation_time_s, inputs.fermi_energy_ev, inputs.energy_ev, inputs.temp_k
        q, m_e, kb_ev = 1.602e-19, 9.109e-31, 8.617e-5
        sigma = (n * (q**2) * tau) / m_e
        arg = (e - ef) / (kb_ev * max(t, 1e-6))
        arg = max(-50.0, min(50.0, arg))
        f_fd = 1.0 / (math.exp(arg) + 1.0)
        metrics = {"conductivity_sm": round(sigma, 1), "fermi_prob": round(f_fd, 4)}
        return CondensataAgentOutput(status="COMPLETED", score=round(f_fd, 4), metrics=metrics, drude_conductivity_s_m=round(sigma, 1), fermi_dirac_prob=round(f_fd, 4))
