"""
Agent Module: D06_PETROLOGIA
Agent Class: PetrologiaAgent

Igneous petrology CIPW norm oxide weight normalization and ternary AFM coordinate geochemical classification.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_PETROLOGIA"


class PetrologiaError(ValueError):
    """Raised when PetrologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class PetrologiaAgentInput:
    sio2: float = 52.0
    al2o3: float = 16.0
    feot: float = 10.0
    mgo: float = 8.0
    cao: float = 9.0
    na2o: float = 3.0
    k2o: float = 1.0


@dataclass(frozen=True)
class PetrologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    total_alkali_silica: float = 0.0
    afm_a: float = 0.0


class PetrologiaAgent:
    """
    Igneous petrology CIPW norm oxide weight normalization and ternary AFM coordinate geochemical classification.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: PetrologiaAgentInput) -> PetrologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        tas_alkali = inputs.na2o + inputs.k2o
        tot_afm = inputs.na2o + inputs.k2o + inputs.feot + inputs.mgo
        a = (inputs.na2o + inputs.k2o) / max(tot_afm, 1e-6) * 100.0
        f = inputs.feot / max(tot_afm, 1e-6) * 100.0
        m = inputs.mgo / max(tot_afm, 1e-6) * 100.0
        metrics = {"total_alkali": round(tas_alkali, 2), "sio2": inputs.sio2, "afm_a": round(a, 2), "afm_f": round(f, 2), "afm_m": round(m, 2)}
        return PetrologiaAgentOutput(status="COMPLETED", score=round(min(1.0, inputs.sio2/100.0), 4), metrics=metrics, total_alkali_silica=round(tas_alkali, 2), afm_a=round(a, 2))
