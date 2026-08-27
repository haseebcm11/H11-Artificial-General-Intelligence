"""
Agent Module: D06_MINERALOGIA
Agent Class: MineralogiaAgent

Crystallography and X-ray diffraction via Bragg's Law n*lambda = 2*d*sin(theta) and interplanar lattice spacing d_{hkl}.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_MINERALOGIA"


class MineralogiaError(ValueError):
    """Raised when MineralogiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class MineralogiaAgentInput:
    lattice_constant_a: float = 5.43
    miller_indices: list[int] = field(default_factory=lambda: [1, 1, 1])
    xray_lambda: float = 1.5406


@dataclass(frozen=True)
class MineralogiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    d_spacing_angstrom: float = 0.0
    bragg_angle_deg: float = 0.0


class MineralogiaAgent:
    """
    Crystallography and X-ray diffraction via Bragg's Law n*lambda = 2*d*sin(theta) and interplanar lattice spacing d_{hkl}.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: MineralogiaAgentInput) -> MineralogiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        a = inputs.lattice_constant_a
        h, k, l = inputs.miller_indices if len(inputs.miller_indices) >= 3 else [1, 0, 0]
        d = a / math.sqrt(h*h + k*k + l*l)
        sin_theta = inputs.xray_lambda / (2.0 * d)
        theta_deg = math.degrees(math.asin(max(-1.0, min(1.0, sin_theta)))) if abs(sin_theta) <= 1.0 else 0.0
        metrics = {"d_spacing": round(d, 4), "theta_deg": round(theta_deg, 3), "two_theta_deg": round(2 * theta_deg, 3)}
        return MineralogiaAgentOutput(status="COMPLETED", score=round(min(1.0, d/10.0), 4), metrics=metrics, d_spacing_angstrom=round(d, 4), bragg_angle_deg=round(theta_deg, 3))
