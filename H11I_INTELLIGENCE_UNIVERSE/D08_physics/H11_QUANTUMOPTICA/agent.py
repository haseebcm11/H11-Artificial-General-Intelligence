"""
Agent Module: D08_QUANTUMOPTICA
Agent Class: QuantumopticaAgent

Quantum optics Mandel Q-parameter Q = (Var(n) - E[n]) / E[n] and second-order coherence g^(2)(0).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_QUANTUMOPTICA"


class QuantumopticaError(ValueError):
    """Raised when QuantumopticaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class QuantumopticaAgentInput:
    mean_photons: float = 4.0
    variance_photons: float = 2.0


@dataclass(frozen=True)
class QuantumopticaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    mandel_q: float = 0.0
    g2_zero: float = 0.0


class QuantumopticaAgent:
    """
    Quantum optics Mandel Q-parameter Q = (Var(n) - E[n]) / E[n] and second-order coherence g^(2)(0).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: QuantumopticaAgentInput) -> QuantumopticaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n, var_n = max(inputs.mean_photons, 1e-6), inputs.variance_photons
        q = (var_n - n) / n
        # g2(0) = 1 + (var_n - n) / n^2
        g2 = 1.0 + (var_n - n) / (n * n)
        metrics = {"mandel_q": round(q, 4), "g2_zero": round(g2, 4), "is_sub_poissonian": 1.0 if q < 0 else 0.0}
        return QuantumopticaAgentOutput(status="COMPLETED", score=round(max(0.0, min(1.0, 1.0 - q)), 4), metrics=metrics, mandel_q=round(q, 4), g2_zero=round(g2, 4))
