"""
Agent Module: D09_ANALYTICA
Agent Class: AnalyticaAgent

Analytical chemistry Beer-Lambert Law A = eps*b*c and chromatographic resolution R_s = 2*(t2-t1)/(w1+w2).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_ANALYTICA"


class AnalyticaError(ValueError):
    """Raised when AnalyticaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class AnalyticaAgentInput:
    absorbance: float = 0.45
    molar_extinction: float = 1500.0
    path_length_cm: float = 1.0
    retention_t1: float = 4.2
    retention_t2: float = 5.1
    width_w1: float = 0.4
    width_w2: float = 0.5


@dataclass(frozen=True)
class AnalyticaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    concentration_molar: float = 0.0
    resolution: float = 0.0


class AnalyticaAgent:
    """
    Analytical chemistry Beer-Lambert Law A = eps*b*c and chromatographic resolution R_s = 2*(t2-t1)/(w1+w2).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: AnalyticaAgentInput) -> AnalyticaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        a, eps, b = inputs.absorbance, inputs.molar_extinction, inputs.path_length_cm
        conc = a / max(eps * b, 1e-9)
        t1, t2, w1, w2 = inputs.retention_t1, inputs.retention_t2, inputs.width_w1, inputs.width_w2
        rs = 2.0 * (t2 - t1) / max(w1 + w2, 1e-6)
        metrics = {"concentration_m": round(conc, 6), "chromatographic_resolution": round(rs, 3)}
        return AnalyticaAgentOutput(status="COMPLETED", score=round(min(1.0, rs/2.0), 4), metrics=metrics, concentration_molar=round(conc, 6), resolution=round(rs, 3))
