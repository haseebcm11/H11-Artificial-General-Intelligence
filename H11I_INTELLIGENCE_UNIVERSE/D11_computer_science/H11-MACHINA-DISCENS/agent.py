"""
Agent Module: D11_MACHINA_DISCENS
Agent Class: MachinaDiscensAgent

Statistical machine learning: Support Vector Machine dual quadratic objective and Decision Tree Gini impurity gain.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_MACHINA_DISCENS"


class MachinaDiscensError(ValueError):
    """Raised when MachinaDiscensAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class MachinaDiscensAgentInput:
    class_counts: list[int] = field(default_factory=lambda: [40, 60])


@dataclass(frozen=True)
class MachinaDiscensAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    gini_impurity: float = 0.0


class MachinaDiscensAgent:
    """
    Statistical machine learning: Support Vector Machine dual quadratic objective and Decision Tree Gini impurity gain.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: MachinaDiscensAgentInput) -> MachinaDiscensAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        cnts = inputs.class_counts if inputs.class_counts else [1, 1]
        tot = sum(cnts) or 1
        gini = 1.0 - sum((c/tot)**2 for c in cnts)
        score = max(0.0, 1.0 - gini * 2.0)
        metrics = {"gini_impurity": round(gini, 4), "total_samples": float(tot)}
        return MachinaDiscensAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, gini_impurity=round(gini, 4))
