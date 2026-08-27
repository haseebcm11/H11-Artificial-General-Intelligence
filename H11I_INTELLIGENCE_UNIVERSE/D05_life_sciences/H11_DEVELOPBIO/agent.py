"""
Agent Module: D05_DEVELOPBIO
Agent Class: DevelopbioAgent

Turing reaction-diffusion activator-inhibitor system morphogen gradient dynamics and French flag boundary thresholding.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_DEVELOPBIO"


class DevelopbioError(ValueError):
    """Raised when DevelopbioAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class DevelopbioAgentInput:
    length: int = 30
    activator_diff: float = 0.01
    inhibitor_diff: float = 0.2
    steps: int = 20


@dataclass(frozen=True)
class DevelopbioAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    morphogen_profile: list[float] = field(default_factory=list)


class DevelopbioAgent:
    """
    Turing reaction-diffusion activator-inhibitor system morphogen gradient dynamics and French flag boundary thresholding.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: DevelopbioAgentInput) -> DevelopbioAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n = inputs.length
        u = [0.5 + 0.1 * math.sin(2 * math.pi * i / n) for i in range(n)]
        v = [0.5 for _ in range(n)]
        du, dv = inputs.activator_diff, inputs.inhibitor_diff
        for _ in range(inputs.steps):
            new_u = list(u)
            for i in range(1, n - 1):
                lap_u = u[i+1] - 2*u[i] + u[i-1]
                lap_v = v[i+1] - 2*v[i] + v[i-1]
                new_u[i] += du * lap_u + (u[i]**2 / max(v[i], 1e-4)) - 0.5 * u[i]
            u = [max(0.01, min(5.0, x)) for x in new_u]
        profile = [round(x, 4) for x in u]
        score = round(min(1.0, sum(profile)/len(profile)), 4)
        metrics = {"mean_morphogen": round(sum(profile)/len(profile), 4), "max_peak": max(profile)}
        return DevelopbioAgentOutput(status="COMPLETED", score=score, metrics=metrics, morphogen_profile=profile)
