"""
Agent Module: D06_VULCANOLOGIA
Agent Class: VulcanologiaAgent

Volcanic plume height dynamics H = 1.67 * Q^{0.259} and Volcanic Explosivity Index (VEI) eruptive volume scaling.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_VULCANOLOGIA"


class VulcanologiaError(ValueError):
    """Raised when VulcanologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class VulcanologiaAgentInput:
    mass_eruption_rate_kg_s: float = 1e7
    magma_temp_c: float = 1050.0


@dataclass(frozen=True)
class VulcanologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    plume_height_km: float = 0.0
    vei_estimate: int = 0


class VulcanologiaAgent:
    """
    Volcanic plume height dynamics H = 1.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: VulcanologiaAgentInput) -> VulcanologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        mer = inputs.mass_eruption_rate_kg_s
        q_m3 = mer / 2500.0  # density approx 2500 kg/m3
        h_km = 1.67 * (q_m3**0.259)
        vei = 0
        if q_m3 * 3600.0 > 1e11: vei = 7
        elif q_m3 * 3600.0 > 1e10: vei = 6
        elif q_m3 * 3600.0 > 1e9: vei = 5
        elif q_m3 * 3600.0 > 1e8: vei = 4
        elif q_m3 * 3600.0 > 1e7: vei = 3
        elif q_m3 * 3600.0 > 1e6: vei = 2
        else: vei = 1
        metrics = {"plume_height_km": round(h_km, 2), "vei": float(vei), "volume_rate_m3_s": round(q_m3, 1)}
        return VulcanologiaAgentOutput(status="COMPLETED", score=round(vei/8.0, 4), metrics=metrics, plume_height_km=round(h_km, 2), vei_estimate=vei)
