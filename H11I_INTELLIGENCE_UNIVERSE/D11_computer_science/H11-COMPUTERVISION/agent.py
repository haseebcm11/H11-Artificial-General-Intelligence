"""
Agent Module: D11_COMPUTERVISION
Agent Class: ComputervisionAgent

Computer vision feature extraction SIFT Difference-of-Gaussians and Harris corner detection matrix response R = det(M) - k*(Tr M)^2.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_COMPUTERVISION"


class ComputervisionError(ValueError):
    """Raised when ComputervisionAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ComputervisionAgentInput:
    ix_sq: float = 120.0
    iy_sq: float = 95.0
    ix_iy: float = 40.0
    k: float = 0.04


@dataclass(frozen=True)
class ComputervisionAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    harris_response: float = 0.0


class ComputervisionAgent:
    """
    Computer vision feature extraction SIFT Difference-of-Gaussians and Harris corner detection matrix response R = det(M) - k*(Tr M)^2.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ComputervisionAgentInput) -> ComputervisionAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        det_m = inputs.ix_sq * inputs.iy_sq - (inputs.ix_iy**2)
        tr_m = inputs.ix_sq + inputs.iy_sq
        r = det_m - inputs.k * (tr_m**2)
        score = min(1.0, max(0.0, r / 10000.0))
        metrics = {"harris_response": round(r, 2), "det_m": round(det_m, 2), "trace_m": round(tr_m, 2)}
        return ComputervisionAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, harris_response=round(r, 2))
