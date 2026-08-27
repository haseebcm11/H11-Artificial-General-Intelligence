"""
Agent Module: D09_INORGANICA
Agent Class: InorganicaAgent

Coordination chemistry Crystal Field Stabilization Energy (CFSE) and spin-only magnetic moment mu_so = sqrt(n*(n+2)) Bohr Magnetons.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_INORGANICA"


class InorganicaError(ValueError):
    """Raised when InorganicaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class InorganicaAgentInput:
    unpaired_electrons: int = 3
    octahedral_splitting_dq: float = 10.0
    pairing_energy_cm: float = 15000.0


@dataclass(frozen=True)
class InorganicaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    spin_only_moment_bm: float = 0.0
    cfse_dq: float = 0.0


class InorganicaAgent:
    """
    Coordination chemistry Crystal Field Stabilization Energy (CFSE) and spin-only magnetic moment mu_so = sqrt(n*(n+2)) Bohr Magnetons.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: InorganicaAgentInput) -> InorganicaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n = inputs.unpaired_electrons
        mu_so = math.sqrt(n * (n + 2))
        # For d3 octahedral: 3 in t2g -> CFSE = -12 Dq
        cfse = -4.0 * min(n, 3) * inputs.octahedral_splitting_dq / 10.0
        metrics = {"spin_only_bm": round(mu_so, 3), "cfse_dq": round(cfse, 2)}
        return InorganicaAgentOutput(status="COMPLETED", score=round(min(1.0, mu_so/6.0), 4), metrics=metrics, spin_only_moment_bm=round(mu_so, 3), cfse_dq=round(cfse, 2))
