"""
Agent Module: L10_TEMPORAL_MEM
Agent Class: TemporalMemAgent

Temporal sequence kernel tracker with power-law recency weighting and Markov state transition probability matrix formulation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L10_TEMPORAL_MEM"


class TemporalMemError(ValueError):
    """Raised when TemporalMemAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class TemporalMemAgentInput:
    sequence: list[str] = field(default_factory=lambda: ['A', 'B', 'A', 'C', 'B', 'A', 'B', 'C'])


@dataclass(frozen=True)
class TemporalMemAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    transition_matrix: dict[str, dict] = field(default_factory=dict)


class TemporalMemAgent:
    """
    Temporal sequence kernel tracker with power-law recency weighting and Markov state transition probability matrix formulation.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: TemporalMemAgentInput) -> TemporalMemAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        seq = inputs.sequence if inputs.sequence else ['A', 'B', 'A']
        transitions = {}
        for i in range(len(seq) - 1):
            src, dst = seq[i], seq[i+1]
            if src not in transitions: transitions[src] = {}
            transitions[src][dst] = transitions[src].get(dst, 0) + 1
        trans_probs = {}
        entropies = []
        for src, dsts in transitions.items():
            tot = sum(dsts.values())
            trans_probs[src] = {d: round(c / tot, 4) for d, c in dsts.items()}
            ent = -sum((c/tot) * math.log2(c/tot) for c in dsts.values() if c > 0)
            entropies.append(ent)
        mean_ent = sum(entropies) / max(len(entropies), 1)
        pred_score = max(0.0, 1.0 - mean_ent / 2.0)
        metrics = {"sequence_length": float(len(seq)), "unique_states": float(len(set(seq))), "mean_entropy": round(mean_ent, 4)}
        return TemporalMemAgentOutput(status="COMPLETED", score=round(pred_score, 4), metrics=metrics, transition_matrix=trans_probs)
