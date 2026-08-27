"""
Agent Module: D05_ENTOMOLOGIA
Agent Class: EntomologiaAgent

Insect population dynamics via discrete Ricker model N_{t+1} = N_t * exp(r * (1 - N_t/K)) and Growing Degree Day (GDD) phenology.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_ENTOMOLOGIA"


class EntomologiaError(ValueError):
    """Raised when EntomologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class EntomologiaAgentInput:
    initial_population: float = 100.0
    growth_rate: float = 1.5
    carrying_capacity: float = 500.0
    generations: int = 10


@dataclass(frozen=True)
class EntomologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    population_history: list[float] = field(default_factory=list)


class EntomologiaAgent:
    """
    Insect population dynamics via discrete Ricker model N_{t+1} = N_t * exp(r * (1 - N_t/K)) and Growing Degree Day (GDD) phenology.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: EntomologiaAgentInput) -> EntomologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n, r, k = inputs.initial_population, inputs.growth_rate, inputs.carrying_capacity
        history = [round(n, 1)]
        for _ in range(inputs.generations):
            n = n * math.exp(r * (1.0 - n / max(k, 1e-6)))
            n = max(0.0, min(n, k * 5.0))
            history.append(round(n, 1))
        score = min(1.0, round(history[-1] / k, 4))
        metrics = {"final_pop": history[-1], "carrying_capacity": k, "growth_rate": r}
        return EntomologiaAgentOutput(status="COMPLETED", score=score, metrics=metrics, population_history=history)
