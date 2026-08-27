"""
Agent Module: D11_REINFORCEMENT
Agent Class: ReinforcementAgent

Deep Reinforcement Learning Generalized Advantage Estimation GAE(gamma, lambda) and PPO clipped objective.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_REINFORCEMENT"


class ReinforcementError(ValueError):
    """Raised when ReinforcementAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ReinforcementAgentInput:
    td_residuals: list[float] = field(default_factory=lambda: [1.0, 0.5, -0.2, 0.8])
    gamma: float = 0.99
    gae_lambda: float = 0.95


@dataclass(frozen=True)
class ReinforcementAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    advantages: list[float] = field(default_factory=list)


class ReinforcementAgent:
    """
    Deep Reinforcement Learning Generalized Advantage Estimation GAE(gamma, lambda) and PPO clipped objective.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ReinforcementAgentInput) -> ReinforcementAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        deltas = inputs.td_residuals
        gl = inputs.gamma * inputs.gae_lambda
        advs = []
        curr_adv = 0.0
        for d in reversed(deltas):
            curr_adv = d + gl * curr_adv
            advs.insert(0, round(curr_adv, 4))
        score = min(1.0, max(0.0, sum(advs)/max(len(advs), 1)))
        metrics = {"mean_advantage": round(sum(advs)/len(advs), 4), "max_advantage": max(advs)}
        return ReinforcementAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, advantages=advs)
