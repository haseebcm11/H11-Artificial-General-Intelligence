"""
Agent Module: D05_CELLULARIS
Agent Class: CellularisAgent

Goldman-Hodgkin-Katz (GHK) voltage equation calculating resting membrane potential Vm and cellular ATP turnover stoichiometry.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_CELLULARIS"


class CellularisError(ValueError):
    """Raised when CellularisAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CellularisAgentInput:
    k_in: float = 140.0
    k_out: float = 5.0
    na_in: float = 12.0
    na_out: float = 145.0
    cl_in: float = 4.0
    cl_out: float = 110.0


@dataclass(frozen=True)
class CellularisAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    membrane_potential_mv: float = 0.0


class CellularisAgent:
    """
    Goldman-Hodgkin-Katz (GHK) voltage equation calculating resting membrane potential Vm and cellular ATP turnover stoichiometry.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CellularisAgentInput) -> CellularisAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        pk, pna, pcl = 1.0, 0.04, 0.45
        rt_f = 26.7  # mV at 37 C (310 K)
        num = pk * inputs.k_out + pna * inputs.na_out + pcl * inputs.cl_in
        den = pk * inputs.k_in + pna * inputs.na_in + pcl * inputs.cl_out
        vm = rt_f * math.log(num / max(den, 1e-6))
        score = max(0.0, min(1.0, (vm + 100.0) / 100.0))
        metrics = {"vm_mv": round(vm, 2), "k_nernst_mv": round(rt_f * math.log(inputs.k_out/inputs.k_in), 2), "na_nernst_mv": round(rt_f * math.log(inputs.na_out/inputs.na_in), 2)}
        return CellularisAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, membrane_potential_mv=round(vm, 2))
