"""
Agent Module: D06_CARBON
Agent Class: CarbonAgent

Carbon sequestration cycle kinetics and radiative forcing Delta F = 5.35 * ln(C/C_0) atmospheric perturbation model.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_CARBON"


class CarbonError(ValueError):
    """Raised when CarbonAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CarbonAgentInput:
    current_ppm: float = 420.0
    baseline_ppm: float = 280.0
    soil_c_init: float = 100.0
    decay_k: float = 0.05
    years: float = 10.0


@dataclass(frozen=True)
class CarbonAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    radiative_forcing_w_m2: float = 0.0
    retained_soil_carbon: float = 0.0


class CarbonAgent:
    """
    Carbon sequestration cycle kinetics and radiative forcing Delta F = 5.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CarbonAgentInput) -> CarbonAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        c, c0 = inputs.current_ppm, inputs.baseline_ppm
        rf = 5.35 * math.log(c / c0)
        c_retained = inputs.soil_c_init * math.exp(-inputs.decay_k * inputs.years)
        score = max(0.0, 1.0 - rf / 4.0)
        metrics = {"radiative_forcing": round(rf, 3), "soil_carbon_retained": round(c_retained, 2)}
        return CarbonAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, radiative_forcing_w_m2=round(rf, 3), retained_soil_carbon=round(c_retained, 2))
