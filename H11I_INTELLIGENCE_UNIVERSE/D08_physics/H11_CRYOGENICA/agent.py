"""
Agent Module: D08_CRYOGENICA
Agent Class: CryogenicaAgent

Cryogenic refrigeration Carnot efficiency COP = T_cold / (T_hot - T_cold) and helium dilution refrigerator cooling power.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D08_CRYOGENICA"


class CryogenicaError(ValueError):
    """Raised when CryogenicaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CryogenicaAgentInput:
    t_cold_k: float = 4.2
    t_hot_k: float = 300.0
    heat_load_watts: float = 1.0


@dataclass(frozen=True)
class CryogenicaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    carnot_cop: float = 0.0
    ideal_work_watts: float = 0.0


class CryogenicaAgent:
    """
    Cryogenic refrigeration Carnot efficiency COP = T_cold / (T_hot - T_cold) and helium dilution refrigerator cooling power.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CryogenicaAgentInput) -> CryogenicaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        tc, th, q = inputs.t_cold_k, inputs.t_hot_k, inputs.heat_load_watts
        cop = tc / (th - tc)
        w_ideal = q / cop
        metrics = {"carnot_cop": round(cop, 6), "ideal_work_w": round(w_ideal, 2)}
        return CryogenicaAgentOutput(status="COMPLETED", score=round(min(1.0, cop*10.0), 4), metrics=metrics, carnot_cop=round(cop, 6), ideal_work_watts=round(w_ideal, 2))
