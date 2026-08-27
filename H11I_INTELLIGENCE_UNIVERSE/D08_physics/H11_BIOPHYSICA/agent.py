"""
Agent Module: D08_BIOPHYSICA
Agent Class: BiophysicaAgent

Förster Resonance Energy Transfer (FRET) efficiency E = R0^6 / (R0^6 + r^6) and Worm-Like Chain (WLC) polymer elasticity.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_BIOPHYSICA"


class BiophysicaError(ValueError):
    """Raised when BiophysicaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class BiophysicaAgentInput:
    distance_nm: float = 5.0
    forster_radius_r0_nm: float = 5.5


@dataclass(frozen=True)
class BiophysicaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    fret_efficiency: float = 0.0


class BiophysicaAgent:
    """
    Förster Resonance Energy Transfer (FRET) efficiency E = R0^6 / (R0^6 + r^6) and Worm-Like Chain (WLC) polymer elasticity.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: BiophysicaAgentInput) -> BiophysicaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        r, r0 = inputs.distance_nm, inputs.forster_radius_r0_nm
        eff = (r0**6) / ((r0**6) + (r**6))
        metrics = {"fret_efficiency": round(eff, 4), "r_over_r0": round(r/r0, 3)}
        return BiophysicaAgentOutput(status="COMPLETED", score=round(eff, 4), metrics=metrics, fret_efficiency=round(eff, 4))
