"""
Agent Module: D10_COMBINATORIA
Agent Class: CombinatoriaAgent

Enumerative combinatorics Stirling numbers of the second kind S(n,k) and Catalan sequence C_n = (2n)! / ((n+1)! * n!).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D10_COMBINATORIA"


class CombinatoriaError(ValueError):
    """Raised when CombinatoriaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class CombinatoriaAgentInput:
    n: int = 6
    k: int = 3


@dataclass(frozen=True)
class CombinatoriaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    stirling_s2: int = 90
    catalan_number: int = 132


class CombinatoriaAgent:
    """
    Enumerative combinatorics Stirling numbers of the second kind S(n,k) and Catalan sequence C_n = (2n)! / ((n+1)! * n!).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: CombinatoriaAgentInput) -> CombinatoriaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        n, k = inputs.n, inputs.k
        # Stirling S(n,k) = (1/k!) sum (-1)^(k-j) (k choose j) j^n
        s2 = 0
        for j in range(k + 1):
            c = math.comb(k, j)
            term = ((-1)**(k - j)) * c * (j**n)
            s2 += term
        s2 //= math.factorial(k)
        cat = math.comb(2*n, n) // (n + 1)
        metrics = {"stirling_s2": float(s2), "catalan_n": float(cat)}
        return CombinatoriaAgentOutput(status="COMPLETED", score=round(min(1.0, s2/1000.0), 4), metrics=metrics, stirling_s2=s2, catalan_number=cat)
