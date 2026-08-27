"""
Agent Module: D12_THREATINTEL
Agent Class: ThreatintelAgent

Threat intelligence STIX 2.1 JSON relationship scoring and Diamond Model attribution vector cosine similarity.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D12_THREATINTEL"


class ThreatintelError(ValueError):
    """Raised when ThreatintelAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ThreatintelAgentInput:
    actor_ttp_vector: list[float] = field(default_factory=lambda: [1.0, 0.0, 1.0, 1.0, 0.0])
    known_threat_group_vector: list[float] = field(default_factory=lambda: [1.0, 0.0, 1.0, 0.0, 0.0])


@dataclass(frozen=True)
class ThreatintelAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    attribution_confidence: float = 0.0


class ThreatintelAgent:
    """
    Threat intelligence STIX 2.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ThreatintelAgentInput) -> ThreatintelAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        v1, v2 = inputs.actor_ttp_vector, inputs.known_threat_group_vector
        dot = sum(a*b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a*a for a in v1)) or 1e-9
        n2 = math.sqrt(sum(b*b for b in v2)) or 1e-9
        sim = dot / (n1 * n2)
        metrics = {"attribution_confidence": round(sim, 3), "common_ttps": float(dot)}
        return ThreatintelAgentOutput(status="COMPLETED", score=round(sim, 4), metrics=metrics, attribution_confidence=round(sim, 3))
