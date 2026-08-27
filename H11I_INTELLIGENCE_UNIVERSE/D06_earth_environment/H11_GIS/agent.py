"""
Agent Module: D06_GIS
Agent Class: GisAgent

Spatial vector analytics Moran's I spatial autocorrelation and polygon boundary containment geometry.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_GIS"


class GisError(ValueError):
    """Raised when GisAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GisAgentInput:
    values: list[float] = field(default_factory=lambda: [10.0, 12.0, 15.0, 11.0, 9.0])
    weights_matrix: list[list[float]] = field(default_factory=lambda: [[0, 1, 0, 0, 1], [1, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 1], [1, 0, 0, 1, 0]])


@dataclass(frozen=True)
class GisAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    morans_i: float = 0.0


class GisAgent:
    """
    Spatial vector analytics Moran's I spatial autocorrelation and polygon boundary containment geometry.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GisAgentInput) -> GisAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        x = inputs.values if inputs.values else [1.0, 2.0]
        w = inputs.weights_matrix
        n = len(x)
        x_bar = sum(x) / n
        s0 = sum(sum(row) for row in w) or 1.0
        num = sum(w[i][j] * (x[i] - x_bar) * (x[j] - x_bar) for i in range(n) for j in range(n))
        den = sum((xi - x_bar)**2 for xi in x) or 1e-6
        moran_i = (n / s0) * (num / den)
        metrics = {"morans_i": round(moran_i, 4), "sample_mean": round(x_bar, 2)}
        return GisAgentOutput(status="COMPLETED", score=round((moran_i + 1.0)/2.0, 4), metrics=metrics, morans_i=round(moran_i, 4))
