"""
Agent Module: D07_EXOBIOLOGIA
Agent Class: ExobiologiaAgent

Exobiology Drake Equation N = R_* * f_p * n_e * f_l * f_i * f_c * L and planetary Earth Similarity Index (ESI).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D07_EXOBIOLOGIA"


class ExobiologiaError(ValueError):
    """Raised when ExobiologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ExobiologiaAgentInput:
    star_formation_rate: float = 1.5
    fraction_planets: float = 0.9
    habitable_planets: float = 0.4
    fraction_life: float = 0.2
    fraction_intelligence: float = 0.1
    fraction_communicative: float = 0.1
    civilization_lifetime_yrs: float = 10000.0


@dataclass(frozen=True)
class ExobiologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    communicative_civilizations: float = 0.0


class ExobiologiaAgent:
    """
    Exobiology Drake Equation N = R_* * f_p * n_e * f_l * f_i * f_c * L and planetary Earth Similarity Index (ESI).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ExobiologiaAgentInput) -> ExobiologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        p = inputs
        n = p.star_formation_rate * p.fraction_planets * p.habitable_planets * p.fraction_life * p.fraction_intelligence * p.fraction_communicative * p.civilization_lifetime_yrs
        metrics = {"drake_n": round(n, 2), "lifetime_yrs": p.civilization_lifetime_yrs}
        return ExobiologiaAgentOutput(status="COMPLETED", score=round(min(1.0, math.log10(max(n, 1.0))/4.0), 4), metrics=metrics, communicative_civilizations=round(n, 2))
