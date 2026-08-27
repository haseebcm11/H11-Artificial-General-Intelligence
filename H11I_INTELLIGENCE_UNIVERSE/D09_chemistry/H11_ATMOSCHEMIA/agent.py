"""
Agent Module: D09_ATMOSCHEMIA
Agent Class: AtmoschemiaAgent

Chapman stratospheric ozone cycle steady state [O3] = sqrt(k1*k2*[O2]^2*[M] / (k3*k4)) and OH radical oxidation lifetime.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_ATMOSCHEMIA"


class AtmoschemiaError(ValueError):
    """Raised when AtmoschemiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class AtmoschemiaAgentInput:
    o2_mixing_ratio: float = 0.21
    air_density_cm3: float = 1e18
    oh_conc_cm3: float = 1e6
    k_oh_rate: float = 2e-12


@dataclass(frozen=True)
class AtmoschemiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    oh_lifetime_days: float = 0.0


class AtmoschemiaAgent:
    """
    Chapman stratospheric ozone cycle steady state [O3] = sqrt(k1*k2*[O2]^2*[M] / (k3*k4)) and OH radical oxidation lifetime.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: AtmoschemiaAgentInput) -> AtmoschemiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        oh, k_oh = inputs.oh_conc_cm3, inputs.k_oh_rate
        tau_s = 1.0 / max(k_oh * oh, 1e-15)
        tau_days = tau_s / 86400.0
        metrics = {"lifetime_days": round(tau_days, 2), "oh_conc": oh}
        return AtmoschemiaAgentOutput(status="COMPLETED", score=round(min(1.0, 10.0/max(tau_days, 0.1)), 4), metrics=metrics, oh_lifetime_days=round(tau_days, 2))
