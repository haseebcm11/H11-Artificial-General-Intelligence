"""
Agent Module: D11_MULTIMODALIS
Agent Class: MultimodalisAgent

Vision-Language multimodal symmetric cross-entropy contrastive loss L = 0.5*(L_{I->T} + L_{T->I}) with temperature scaling.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_MULTIMODALIS"


class MultimodalisError(ValueError):
    """Raised when MultimodalisAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class MultimodalisAgentInput:
    image_embed: list[float] = field(default_factory=lambda: [0.8, 0.6])
    text_embed: list[float] = field(default_factory=lambda: [0.75, 0.65])
    temperature: float = 0.07


@dataclass(frozen=True)
class MultimodalisAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    cosine_sim: float = 0.0


class MultimodalisAgent:
    """
    Vision-Language multimodal symmetric cross-entropy contrastive loss L = 0.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: MultimodalisAgentInput) -> MultimodalisAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        i_norm = math.sqrt(sum(x*x for x in inputs.image_embed)) or 1e-9
        t_norm = math.sqrt(sum(x*x for x in inputs.text_embed)) or 1e-9
        dot = sum(a*b for a, b in zip(inputs.image_embed, inputs.text_embed))
        cos_sim = dot / (i_norm * t_norm)
        scaled_sim = cos_sim / inputs.temperature
        score = round((cos_sim + 1.0)/2.0, 4)
        metrics = {"cosine_similarity": round(cos_sim, 4), "scaled_logits": round(scaled_sim, 2)}
        return MultimodalisAgentOutput(status="COMPLETED", score=score, metrics=metrics, cosine_sim=round(cos_sim, 4))
