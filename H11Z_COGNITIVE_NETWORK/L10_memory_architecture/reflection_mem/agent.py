"""
Agent Module: L10_REFLECTION_MEM
Agent Class: ReflectionMemAgent

Episodic memory consolidation and abstraction engine evaluating salience, recency, and Shannon surprise score S = -log P(event).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L10_REFLECTION_MEM"


class ReflectionMemError(ValueError):
    """Raised when ReflectionMemAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ReflectionMemAgentInput:
    episodes: list[dict] = field(default_factory=lambda: [{'recency': 0.9, 'salience': 0.8, 'prob': 0.05}, {'recency': 0.2, 'salience': 0.9, 'prob': 0.01}])
    consolidation_threshold: float = 0.6


@dataclass(frozen=True)
class ReflectionMemAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    importances: list[float] = field(default_factory=list)


class ReflectionMemAgent:
    """
    Episodic memory consolidation and abstraction engine evaluating salience, recency, and Shannon surprise score S = -log P(event).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ReflectionMemAgentInput) -> ReflectionMemAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        episodes = inputs.episodes if inputs.episodes else [{'recency': 0.9, 'salience': 0.8, 'prob': 0.05}]
        w_r, w_s, w_u = 0.3, 0.4, 0.3
        importances = []
        for ep in episodes:
            p = max(ep.get("prob", 0.1), 1e-6)
            surprise = -math.log(p) / 5.0
            imp = w_r * ep.get("recency", 0.5) + w_s * ep.get("salience", 0.5) + w_u * min(1.0, surprise)
            importances.append(round(imp, 4))
        mean_imp = sum(importances) / max(len(importances), 1)
        insights_count = sum(1 for i in importances if i > inputs.consolidation_threshold)
        metrics = {"episodes_processed": float(len(episodes)), "high_salience_insights": float(insights_count), "mean_importance": round(mean_imp, 4)}
        return ReflectionMemAgentOutput(status="COMPLETED", score=round(mean_imp, 4), metrics=metrics, importances=importances)
