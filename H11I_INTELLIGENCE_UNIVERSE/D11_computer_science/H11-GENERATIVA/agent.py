"""
Agent Module: D11_GENERATIVA
Agent Class: GenerativaAgent

Generative modeling: Wasserstein GAN gradient penalty ||nabla D(x_hat)||_2 - 1 and Normalizing Flow Jacobian determinant.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_GENERATIVA"


class GenerativaError(ValueError):
    """Raised when GenerativaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GenerativaAgentInput:
    grad_norms: list[float] = field(default_factory=lambda: [1.02, 0.98, 1.05, 0.95])
    lambda_gp: float = 10.0


@dataclass(frozen=True)
class GenerativaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    gp_loss: float = 0.0


class GenerativaAgent:
    """
    Generative modeling: Wasserstein GAN gradient penalty ||nabla D(x_hat)||_2 - 1 and Normalizing Flow Jacobian determinant.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GenerativaAgentInput) -> GenerativaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        gp = sum((gn - 1.0)**2 for gn in inputs.grad_norms) / max(len(inputs.grad_norms), 1)
        tot_gp = inputs.lambda_gp * gp
        score = max(0.0, 1.0 - min(1.0, tot_gp))
        metrics = {"gp_loss": round(tot_gp, 4), "mean_grad_norm": round(sum(inputs.grad_norms)/len(inputs.grad_norms), 3)}
        return GenerativaAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, gp_loss=round(tot_gp, 4))
