"""
Agent Module: D08_STRINGTHEORIA
Agent Class: StringtheoriaAgent

Superstring Regge slope alpha_prime, string tension T = 1/(2*pi*alpha_prime), and T-duality radius duality R <-> alpha'/R.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_STRINGTHEORIA"


class StringtheoriaError(ValueError):
    """Raised when StringtheoriaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class StringtheoriaAgentInput:
    alpha_prime: float = 0.95
    compact_radius_r: float = 2.0


@dataclass(frozen=True)
class StringtheoriaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    string_tension: float = 0.0
    dual_radius: float = 0.0


class StringtheoriaAgent:
    """
    Superstring Regge slope alpha_prime, string tension T = 1/(2*pi*alpha_prime), and T-duality radius duality R <-> alpha'/R.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: StringtheoriaAgentInput) -> StringtheoriaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        ap, r = inputs.alpha_prime, inputs.compact_radius_r
        tension = 1.0 / (2.0 * math.pi * ap)
        r_dual = ap / max(r, 1e-6)
        metrics = {"string_tension": round(tension, 4), "dual_radius": round(r_dual, 4)}
        return StringtheoriaAgentOutput(status="COMPLETED", score=round(min(1.0, tension), 4), metrics=metrics, string_tension=round(tension, 4), dual_radius=round(r_dual, 4))
