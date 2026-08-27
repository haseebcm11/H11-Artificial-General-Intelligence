"""
Agent Module: D11_ARCHITECTURA_SW
Agent Class: ArchitecturaSwAgent

Software architecture metrics: Cyclomatic complexity M = E - N + 2*P and Chidamber-Kemerer Lack of Cohesion in Methods (LCOM).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_ARCHITECTURA_SW"


class ArchitecturaSwError(ValueError):
    """Raised when ArchitecturaSwAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ArchitecturaSwAgentInput:
    edges_e: int = 18
    nodes_n: int = 14
    components_p: int = 1


@dataclass(frozen=True)
class ArchitecturaSwAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    cyclomatic_complexity: int = 6


class ArchitecturaSwAgent:
    """
    Software architecture metrics: Cyclomatic complexity M = E - N + 2*P and Chidamber-Kemerer Lack of Cohesion in Methods (LCOM).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ArchitecturaSwAgentInput) -> ArchitecturaSwAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        m = inputs.edges_e - inputs.nodes_n + 2 * inputs.components_p
        score = max(0.0, 1.0 - min(1.0, m / 20.0))
        metrics = {"cyclomatic_complexity": float(m), "edges": float(inputs.edges_e), "nodes": float(inputs.nodes_n)}
        return ArchitecturaSwAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, cyclomatic_complexity=m)
