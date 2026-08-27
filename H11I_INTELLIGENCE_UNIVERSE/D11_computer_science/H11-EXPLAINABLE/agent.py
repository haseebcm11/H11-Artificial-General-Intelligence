"""
Agent Module: D11_EXPLAINABLE
Agent Class: ExplainableAgent

Explainable AI (XAI) Integrated Gradients attribution IG_i(x) = (x_i - x'_i) * integral(dF/dx) and KernelSHAP weighting.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_EXPLAINABLE"


class ExplainableError(ValueError):
    """Raised when ExplainableAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ExplainableAgentInput:
    feature_values: list[float] = field(default_factory=lambda: [2.0, 5.0, -1.0])
    baselines: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    grad_samples: list[float] = field(default_factory=lambda: [0.3, 0.8, -0.2])


@dataclass(frozen=True)
class ExplainableAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    attributions: list[float] = field(default_factory=list)


class ExplainableAgent:
    """
    Explainable AI (XAI) Integrated Gradients attribution IG_i(x) = (x_i - x'_i) * integral(dF/dx) and KernelSHAP weighting.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ExplainableAgentInput) -> ExplainableAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        x, x0, grads = inputs.feature_values, inputs.baselines, inputs.grad_samples
        attrs = [round((xi - x0i) * g, 4) for xi, x0i, g in zip(x, x0, grads)]
        tot_attr = sum(attrs)
        metrics = {"total_attribution": round(tot_attr, 4), "max_attribution": max(attrs, default=0.0)}
        return ExplainableAgentOutput(status="COMPLETED", score=round(min(1.0, abs(tot_attr)/5.0), 4), metrics=metrics, attributions=attrs)
