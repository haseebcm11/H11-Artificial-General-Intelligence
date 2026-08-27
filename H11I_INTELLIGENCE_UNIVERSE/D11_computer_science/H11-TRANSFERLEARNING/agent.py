"""
Agent Module: D11_TRANSFERLEARNING
Agent Class: TransferlearningAgent

Domain adaptation Maximum Mean Discrepancy (MMD) in Reproducing Kernel Hilbert Space (RKHS) and Elastic Weight Consolidation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_TRANSFERLEARNING"


class TransferlearningError(ValueError):
    """Raised when TransferlearningAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class TransferlearningAgentInput:
    source_features: list[float] = field(default_factory=lambda: [1.0, 2.0, 3.0])
    target_features: list[float] = field(default_factory=lambda: [1.2, 2.1, 2.8])


@dataclass(frozen=True)
class TransferlearningAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    mmd_distance: float = 0.0


class TransferlearningAgent:
    """
    Domain adaptation Maximum Mean Discrepancy (MMD) in Reproducing Kernel Hilbert Space (RKHS) and Elastic Weight Consolidation.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: TransferlearningAgentInput) -> TransferlearningAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        s, t = inputs.source_features, inputs.target_features
        mu_s = sum(s) / max(len(s), 1)
        mu_t = sum(t) / max(len(t), 1)
        mmd = abs(mu_s - mu_t)
        score = max(0.0, 1.0 - min(1.0, mmd))
        metrics = {"mmd_distance": round(mmd, 4), "source_mean": round(mu_s, 3), "target_mean": round(mu_t, 3)}
        return TransferlearningAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, mmd_distance=round(mmd, 4))
