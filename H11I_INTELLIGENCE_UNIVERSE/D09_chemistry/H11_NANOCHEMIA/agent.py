"""
Agent Module: D09_NANOCHEMIA
Agent Class: NanochemiaAgent

Nanomaterial Gibbs-Thomson melting point depression delta Tm = T_bulk * (2*gamma*v / (delta_Hf * r)) and surface area scaling.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_NANOCHEMIA"


class NanochemiaError(ValueError):
    """Raised when NanochemiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class NanochemiaAgentInput:
    radius_nm: float = 5.0
    bulk_melting_temp_k: float = 1337.0
    surface_energy_j_m2: float = 1.4
    molar_volume_m3_mol: float = 1e-5
    heat_of_fusion_j_mol: float = 12500.0


@dataclass(frozen=True)
class NanochemiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    melting_depression_k: float = 0.0
    nanoparticle_melting_temp_k: float = 0.0


class NanochemiaAgent:
    """
    Nanomaterial Gibbs-Thomson melting point depression delta Tm = T_bulk * (2*gamma*v / (delta_Hf * r)) and surface area scaling.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: NanochemiaAgentInput) -> NanochemiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        r_m = inputs.radius_nm * 1e-9
        tb, gam, v, hf = inputs.bulk_melting_temp_k, inputs.surface_energy_j_m2, inputs.molar_volume_m3_mol, inputs.heat_of_fusion_j_mol
        dt_m = tb * (2.0 * gam * v) / (hf * max(r_m, 1e-10))
        t_nano = max(0.0, tb - dt_m)
        metrics = {"melting_depression_k": round(dt_m, 2), "nano_melting_k": round(t_nano, 2)}
        return NanochemiaAgentOutput(status="COMPLETED", score=round(min(1.0, t_nano/tb), 4), metrics=metrics, melting_depression_k=round(dt_m, 2), nanoparticle_melting_temp_k=round(t_nano, 2))
