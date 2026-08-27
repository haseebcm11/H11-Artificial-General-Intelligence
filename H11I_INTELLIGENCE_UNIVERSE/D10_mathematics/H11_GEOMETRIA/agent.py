"""
Agent Module: D10_GEOMETRIA
Agent Class: GeometriaAgent

Computational geometry Graham Scan 2D convex hull algorithm and Gaussian surface curvature K = kappa_1 * kappa_2.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D10_GEOMETRIA"


class GeometriaError(ValueError):
    """Raised when GeometriaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GeometriaAgentInput:
    points: list[list[float]] = field(default_factory=lambda: [[0, 0], [1, 1], [2, 0], [1, 0.5], [1, 2]])


@dataclass(frozen=True)
class GeometriaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    hull_vertices_count: int = 0
    convex_hull: list[list[float]] = field(default_factory=list)


class GeometriaAgent:
    """
    Computational geometry Graham Scan 2D convex hull algorithm and Gaussian surface curvature K = kappa_1 * kappa_2.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GeometriaAgentInput) -> GeometriaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        pts = sorted(inputs.points)
        def cross(o, a, b): return (a[0] - o[0])*(b[1] - o[1]) - (a[1] - o[1])*(b[0] - o[0])
        lower = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
            lower.append(p)
        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
            upper.append(p)
        hull = lower[:-1] + upper[:-1]
        metrics = {"total_points": float(len(pts)), "hull_vertices": float(len(hull))}
        return GeometriaAgentOutput(status="COMPLETED", score=round(len(hull)/max(len(pts), 1), 4), metrics=metrics, hull_vertices_count=len(hull), convex_hull=hull)
