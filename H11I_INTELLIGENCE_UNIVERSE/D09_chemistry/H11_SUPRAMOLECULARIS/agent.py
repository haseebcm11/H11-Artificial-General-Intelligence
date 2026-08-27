"""
Agent Module: D09_SUPRAMOLECULARIS
Agent Class: SupramolecularisAgent

Host-guest binding association constant K_a = [HG] / ([H]*[G]) and Scatchard binding isotherm analytics.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_SUPRAMOLECULARIS"


class SupramolecularisError(ValueError):
    """Raised when SupramolecularisAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SupramolecularisAgentInput:
    host_conc_total: float = 1e-3
    guest_conc_total: float = 1e-3
    binding_constant_ka: float = 5000.0


@dataclass(frozen=True)
class SupramolecularisAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    complex_conc_m: float = 0.0
    fraction_bound: float = 0.0


class SupramolecularisAgent:
    """
    Host-guest binding association constant K_a = [HG] / ([H]*[G]) and Scatchard binding isotherm analytics.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SupramolecularisAgentInput) -> SupramolecularisAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        h0, g0, ka = inputs.host_conc_total, inputs.guest_conc_total, inputs.binding_constant_ka
        # [HG]^2 - (H0 + G0 + 1/Ka)[HG] + H0*G0 = 0
        b = -(h0 + g0 + 1.0 / max(ka, 1.0))
        c = h0 * g0
        hg = (-b - math.sqrt(max(0.0, b*b - 4.0*c))) / 2.0
        fb = hg / max(h0, 1e-9)
        metrics = {"complex_conc_m": round(hg, 7), "fraction_bound": round(fb, 4)}
        return SupramolecularisAgentOutput(status="COMPLETED", score=round(fb, 4), metrics=metrics, complex_conc_m=round(hg, 7), fraction_bound=round(fb, 4))
