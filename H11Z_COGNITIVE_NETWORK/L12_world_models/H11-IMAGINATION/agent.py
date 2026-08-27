"""
Agent Module: L12_IMAGINATION
Agent Class: ImaginationAgent

Latent world model rollout simulation computing discounted cumulative return R = sum(gamma^t * r_t) across imagined search trees.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L12_IMAGINATION"


class ImaginationError(ValueError):
    """Raised when ImaginationAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ImaginationAgentInput:
    gamma: float = 0.95
    rollout_rewards: list[list[float]] = field(default_factory=lambda: [[1.0, 0.5, 0.2], [0.8, 0.9, 0.7], [0.2, 0.1, 0.0]])


@dataclass(frozen=True)
class ImaginationAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    trajectory_returns: list[float] = field(default_factory=list)


class ImaginationAgent:
    """
    Latent world model rollout simulation computing discounted cumulative return R = sum(gamma^t * r_t) across imagined search trees.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ImaginationAgentInput) -> ImaginationAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        gamma = inputs.gamma
        trajs = inputs.rollout_rewards if inputs.rollout_rewards else [[1.0, 0.5]]
        returns = [round(sum(r * (gamma**t) for t, r in enumerate(r_list)), 4) for r_list in trajs]
        best_ret = max(returns, default=0.0)
        metrics = {"trajectory_count": float(len(trajs)), "best_return": best_ret, "mean_return": round(sum(returns)/max(len(returns), 1), 4)}
        return ImaginationAgentOutput(status="COMPLETED", score=round(min(1.0, max(0.0, best_ret / 3.0)), 4), metrics=metrics, trajectory_returns=returns)
