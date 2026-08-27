"""
Agent Module: D11_METALEARNING
Agent Class: MetalearningAgent

Model-Agnostic Meta-Learning (MAML) inner-loop gradient adaptation theta' = theta - alpha*grad(L_task) and meta-update step.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_METALEARNING"


class MetalearningError(ValueError):
    """Raised when MetalearningAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class MetalearningAgentInput:
    initial_params: list[float] = field(default_factory=lambda: [1.0, -0.5])
    task_gradients: list[float] = field(default_factory=lambda: [0.2, 0.1])
    inner_lr: float = 0.01


@dataclass(frozen=True)
class MetalearningAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    adapted_params: list[float] = field(default_factory=list)


class MetalearningAgent:
    """
    Model-Agnostic Meta-Learning (MAML) inner-loop gradient adaptation theta' = theta - alpha*grad(L_task) and meta-update step.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: MetalearningAgentInput) -> MetalearningAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        p, g, lr = inputs.initial_params, inputs.task_gradients, inputs.inner_lr
        adapted = [round(pi - lr * gi, 4) for pi, gi in zip(p, g)]
        score = min(1.0, 1.0 / (1.0 + sum(gi*gi for gi in g)))
        metrics = {"grad_norm": round(math.sqrt(sum(gi*gi for gi in g)), 4)}
        return MetalearningAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, adapted_params=adapted)
