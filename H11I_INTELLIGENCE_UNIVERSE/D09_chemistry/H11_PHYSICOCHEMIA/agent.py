"""
Agent Module: D09_PHYSICOCHEMIA
Agent Class: PhysicochemiaAgent

Chemical thermodynamics Clausius-Clapeyron equation ln(P2/P1) = -(Delta H_vap / R)*(1/T2 - 1/T1) and Gibbs free energy Delta G = Delta H - T*Delta S.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_PHYSICOCHEMIA"


class PhysicochemiaError(ValueError):
    """Raised when PhysicochemiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class PhysicochemiaAgentInput:
    t1_k: float = 373.15
    p1_bar: float = 1.013
    delta_h_vap_kj_mol: float = 40.66
    t2_k: float = 393.15


@dataclass(frozen=True)
class PhysicochemiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    p2_bar: float = 0.0


class PhysicochemiaAgent:
    """
    Chemical thermodynamics Clausius-Clapeyron equation ln(P2/P1) = -(Delta H_vap / R)*(1/T2 - 1/T1) and Gibbs free energy Delta G = Delta H - T*Delta S.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: PhysicochemiaAgentInput) -> PhysicochemiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        r = 8.314e-3  # kJ/(mol K)
        dh = inputs.delta_h_vap_kj_mol
        t1, t2, p1 = inputs.t1_k, inputs.t2_k, inputs.p1_bar
        ln_ratio = -(dh / r) * (1.0 / t2 - 1.0 / t1)
        p2 = p1 * math.exp(ln_ratio)
        metrics = {"vapor_pressure_bar": round(p2, 3), "temp_k": t2}
        return PhysicochemiaAgentOutput(status="COMPLETED", score=round(min(1.0, p2/5.0), 4), metrics=metrics, p2_bar=round(p2, 3))
