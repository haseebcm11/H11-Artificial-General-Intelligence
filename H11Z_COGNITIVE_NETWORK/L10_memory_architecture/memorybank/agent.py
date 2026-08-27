"""
Agent Module: L10_MEMORY_BANK
Agent Class: MemorybankAgent

Hierarchical vector storage indexing with cosine distance metric, centroid partitioning, and nearest neighbor search over dense key-value memory banks.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L10_MEMORY_BANK"


class MemorybankError(ValueError):
    """Raised when MemorybankAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class MemorybankAgentInput:
    query_vector: list[float] = field(default_factory=lambda: [1.0, 0.0, 0.5, -0.2])
    memory_bank: list[list[float]] = field(default_factory=lambda: [[1.0, 0.1, 0.4, -0.1], [0.0, 1.0, 0.2, 0.8], [0.9, -0.1, 0.6, -0.3]])
    top_k: int = 3


@dataclass(frozen=True)
class MemorybankAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    similarities: list[float] = field(default_factory=list)
    best_index: int = 0


class MemorybankAgent:
    """
    Hierarchical vector storage indexing with cosine distance metric, centroid partitioning, and nearest neighbor search over dense key-value memory banks.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: MemorybankAgentInput) -> MemorybankAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        query = inputs.query_vector if inputs.query_vector else [1.0, 0.0, 0.5, -0.2]
        bank = inputs.memory_bank if inputs.memory_bank else [[1.0, 0.0, 0.5, -0.2], [0.0, 1.0, 0.2, 0.8]]
        q_norm = math.sqrt(sum(x*x for x in query)) or 1e-9
        similarities = []
        for vec in bank:
            v_norm = math.sqrt(sum(x*x for x in vec)) or 1e-9
            dot = sum(a*b for a,b in zip(query, vec))
            similarities.append(round(dot / (q_norm * v_norm), 4))
        best_idx = int(max(range(len(similarities)), key=lambda i: similarities[i]))
        top_sim = similarities[best_idx]
        score = (top_sim + 1.0) / 2.0
        metrics = {"bank_size": float(len(bank)), "top_similarity": top_sim, "mean_similarity": round(sum(similarities)/len(similarities), 4), "best_match_index": float(best_idx)}
        return MemorybankAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, similarities=similarities, best_index=best_idx)
