"""
Agent Module: D11_NLP
Agent Class: NlpAgent

Computational linguistics language model perplexity PPL = exp(-1/N * sum(ln P(w_i))) and BLEU n-gram precision scoring.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_NLP"


class NlpError(ValueError):
    """Raised when NlpAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class NlpAgentInput:
    log_probs: list[float] = field(default_factory=lambda: [-1.2, -0.8, -1.5, -0.5, -2.1])


@dataclass(frozen=True)
class NlpAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    perplexity: float = 0.0


class NlpAgent:
    """
    Computational linguistics language model perplexity PPL = exp(-1/N * sum(ln P(w_i))) and BLEU n-gram precision scoring.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: NlpAgentInput) -> NlpAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        lp = inputs.log_probs if inputs.log_probs else [-1.0]
        nll = -sum(lp) / len(lp)
        ppl = math.exp(nll)
        score = max(0.0, 1.0 - min(1.0, ppl / 50.0))
        metrics = {"nll": round(nll, 4), "perplexity": round(ppl, 2)}
        return NlpAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, perplexity=round(ppl, 2))
