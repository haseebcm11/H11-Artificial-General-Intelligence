"""
Agent Module: D05_ZOOLOGIA
Agent Class: ZoologiaAgent

Comparative zoology scaling laws: Kleiber's Law basal metabolic rate B = 70 * M^{0.75} and Encephalization Quotient (EQ).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_ZOOLOGIA"


class ZoologiaError(ValueError):
    """Raised when ZoologiaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ZoologiaAgentInput:
    body_mass_kg: float = 70.0
    brain_mass_g: float = 1400.0


@dataclass(frozen=True)
class ZoologiaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    bmr_kcal_day: float = 0.0
    encephalization_quotient: float = 0.0


class ZoologiaAgent:
    """
    Comparative zoology scaling laws: Kleiber's Law basal metabolic rate B = 70 * M^{0.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ZoologiaAgentInput) -> ZoologiaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        m_b, m_br = inputs.body_mass_kg, inputs.brain_mass_g
        bmr = 70.0 * (m_b**0.75)
        # Predicted mammalian brain mass = 0.12 * (body_mass_g)^0.67
        m_bg = m_b * 1000.0
        pred_brain = 0.12 * (m_bg**0.67)
        eq = m_br / max(pred_brain, 1e-6)
        score = min(1.0, round(eq / 7.0, 4))
        metrics = {"bmr_kcal_day": round(bmr, 1), "eq": round(eq, 3), "predicted_brain_g": round(pred_brain, 1)}
        return ZoologiaAgentOutput(status="COMPLETED", score=score, metrics=metrics, bmr_kcal_day=round(bmr, 1), encephalization_quotient=round(eq, 3))
