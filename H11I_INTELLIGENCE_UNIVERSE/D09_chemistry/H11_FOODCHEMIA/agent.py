"""
Agent Module: D09_FOODCHEMIA
Agent Class: FoodchemiaAgent

Food water activity a_w = p/p_0, Arrhenius Maillard browning rate k = A*exp(-Ea/RT), and lipid oxidation kinetics.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_FOODCHEMIA"


class FoodchemiaError(ValueError):
    """Raised when FoodchemiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class FoodchemiaAgentInput:
    temp_c: float = 80.0
    ea_kj_mol: float = 120.0
    pre_exp_factor: float = 1e11
    water_activity: float = 0.65


@dataclass(frozen=True)
class FoodchemiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    reaction_rate_constant: float = 0.0


class FoodchemiaAgent:
    """
    Food water activity a_w = p/p_0, Arrhenius Maillard browning rate k = A*exp(-Ea/RT), and lipid oxidation kinetics.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: FoodchemiaAgentInput) -> FoodchemiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        t_k = inputs.temp_c + 273.15
        r_gas = 8.314e-3  # kJ/(mol K)
        k = inputs.pre_exp_factor * math.exp(-inputs.ea_kj_mol / (r_gas * t_k))
        metrics = {"rate_constant_s": round(k, 6), "water_activity": inputs.water_activity}
        return FoodchemiaAgentOutput(status="COMPLETED", score=round(min(1.0, k * 100.0), 4), metrics=metrics, reaction_rate_constant=round(k, 6))
