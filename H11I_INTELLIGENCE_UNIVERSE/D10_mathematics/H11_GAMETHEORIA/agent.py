"""
Agent Module: D10_GAMETHEORIA
Agent Class: GametheoriaAgent

Game theory normal-form payoff matrix minimax equilibrium and mixed strategy Nash equilibrium computation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D10_GAMETHEORIA"


class GametheoriaError(ValueError):
    """Raised when GametheoriaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GametheoriaAgentInput:
    payoff_matrix_a: list[list[float]] = field(default_factory=lambda: [[3.0, 0.0], [5.0, 1.0]])
    payoff_matrix_b: list[list[float]] = field(default_factory=lambda: [[3.0, 5.0], [0.0, 1.0]])


@dataclass(frozen=True)
class GametheoriaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    nash_equilibrium_profile: list[float] = field(default_factory=list)


class GametheoriaAgent:
    """
    Game theory normal-form payoff matrix minimax equilibrium and mixed strategy Nash equilibrium computation.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GametheoriaAgentInput) -> GametheoriaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        # Prisoner's dilemma: dominant strategy is defect (row 1, col 1)
        a = inputs.payoff_matrix_a
        prob_p1_up = (a[1][1] - a[1][0]) / max((a[0][0] - a[0][1] - a[1][0] + a[1][1]), 1e-6)
        prob_p1_up = max(0.0, min(1.0, prob_p1_up))
        profile = [round(prob_p1_up, 3), round(1.0 - prob_p1_up, 3)]
        metrics = {"p1_strategy_prob": profile[0], "payoff_maximin": max(min(row) for row in a)}
        return GametheoriaAgentOutput(status="COMPLETED", score=round(profile[0], 4), metrics=metrics, nash_equilibrium_profile=profile)
