"""
Agent Module: D07_DEEPSPACE
Agent Class: DeepspaceAgent

Deep space interstellar trajectory modeling hyperbolic excess velocity v_inf = sqrt(v^2 - 2*mu/r) and gravity assist velocity gain.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_DEEPSPACE"


class DeepspaceError(ValueError):
    """Raised when DeepspaceAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class DeepspaceAgentInput:
    velocity_km_s: float = 15.0
    radius_km: float = 200000.0
    central_mu: float = 398600.4


@dataclass(frozen=True)
class DeepspaceAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    hyperbolic_excess_km_s: float = 0.0


class DeepspaceAgent:
    """
    Deep space interstellar trajectory modeling hyperbolic excess velocity v_inf = sqrt(v^2 - 2*mu/r) and gravity assist velocity gain.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: DeepspaceAgentInput) -> DeepspaceAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        v, r, mu = inputs.velocity_km_s, inputs.radius_km, inputs.central_mu
        v_esc_sq = (2.0 * mu) / max(r, 1.0)
        v_inf_sq = v*v - v_esc_sq
        v_inf = math.sqrt(max(0.0, v_inf_sq))
        metrics = {"hyperbolic_excess_km_s": round(v_inf, 3), "escape_velocity_km_s": round(math.sqrt(v_esc_sq), 3)}
        return DeepspaceAgentOutput(status="COMPLETED", score=round(min(1.0, v_inf/20.0), 4), metrics=metrics, hyperbolic_excess_km_s=round(v_inf, 3))
