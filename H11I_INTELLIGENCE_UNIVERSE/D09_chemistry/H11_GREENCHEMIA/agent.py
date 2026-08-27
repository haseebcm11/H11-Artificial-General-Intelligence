"""
Agent Module: D09_GREENCHEMIA
Agent Class: GreenchemiaAgent

Green chemistry metrics Atom Economy AE = (MW_product / sum(MW_reactants))*100% and Sheldon Environmental E-Factor.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D09_GREENCHEMIA"


class GreenchemiaError(ValueError):
    """Raised when GreenchemiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GreenchemiaAgentInput:
    mw_product: float = 180.16
    sum_mw_reactants: float = 240.2
    waste_mass_kg: float = 12.0
    product_mass_kg: float = 50.0


@dataclass(frozen=True)
class GreenchemiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    atom_economy_percent: float = 0.0
    e_factor: float = 0.0


class GreenchemiaAgent:
    """
    Green chemistry metrics Atom Economy AE = (MW_product / sum(MW_reactants))*100% and Sheldon Environmental E-Factor.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GreenchemiaAgentInput) -> GreenchemiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        ae = (inputs.mw_product / max(inputs.sum_mw_reactants, 1e-6)) * 100.0
        e_fac = inputs.waste_mass_kg / max(inputs.product_mass_kg, 1e-6)
        score = min(1.0, ae / 100.0)
        metrics = {"atom_economy_pct": round(ae, 2), "e_factor": round(e_fac, 3)}
        return GreenchemiaAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, atom_economy_percent=round(ae, 2), e_factor=round(e_fac, 3))
