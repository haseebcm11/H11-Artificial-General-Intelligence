"""
Agent Module: D11_DEEPLEARNING
Agent Class: DeeplearningAgent

Deep neural network backpropagation gradient norm propagation and Adam moment vector updates.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_DEEPLEARNING"


class DeeplearningError(ValueError):
    """Raised when DeeplearningAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class DeeplearningAgentInput:
    gradients: list[float] = field(default_factory=lambda: [0.1, -0.2, 0.05, 0.4])
    beta1: float = 0.9
    beta2: float = 0.999


@dataclass(frozen=True)
class DeeplearningAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    grad_norm: float = 0.0


class DeeplearningAgent:
    """
    Deep neural network backpropagation gradient norm propagation and Adam moment vector updates.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: DeeplearningAgentInput) -> DeeplearningAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        g = inputs.gradients if inputs.gradients else [0.0]
        norm_g = math.sqrt(sum(x*x for x in g))
        m = [inputs.beta1 * 0.0 + (1.0 - inputs.beta1) * x for x in g]
        v = [inputs.beta2 * 0.0 + (1.0 - inputs.beta2) * (x**2) for x in g]
        score = max(0.0, 1.0 - min(1.0, norm_g))
        metrics = {"grad_norm": round(norm_g, 4), "layer_dim": float(len(g))}
        return DeeplearningAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, grad_norm=round(norm_g, 4))
