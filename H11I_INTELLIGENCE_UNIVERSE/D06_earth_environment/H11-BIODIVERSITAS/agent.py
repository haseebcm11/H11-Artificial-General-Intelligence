"""
Agent Module: D06_BIODIVERSITAS
Agent Class: BiodiversitasAgent

Ecosystem biodiversity quantification calculating Shannon-Wiener index H' = -sum(p_i * ln(p_i)), Simpson dominance D, and Pielou evenness J'.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D06_BIODIVERSITAS"


class BiodiversitasError(ValueError):
    """Raised when BiodiversitasAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class BiodiversitasAgentInput:
    species_abundances: list[int] = field(default_factory=lambda: [50, 30, 20, 15, 10, 5])


@dataclass(frozen=True)
class BiodiversitasAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    shannon_index: float = 0.0
    simpson_index: float = 0.0
    evenness: float = 0.0


class BiodiversitasAgent:
    """
    Ecosystem biodiversity quantification calculating Shannon-Wiener index H' = -sum(p_i * ln(p_i)), Simpson dominance D, and Pielou evenness J'.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: BiodiversitasAgentInput) -> BiodiversitasAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        abund = inputs.species_abundances if inputs.species_abundances else [10, 10]
        tot = sum(abund)
        props = [c / tot for c in abund if c > 0]
        h_prime = -sum(p * math.log(p) for p in props)
        d_simp = sum(p*p for p in props)
        s = len(props)
        j_even = h_prime / math.log(s) if s > 1 else 1.0
        metrics = {"shannon": round(h_prime, 4), "simpson_dominance": round(d_simp, 4), "pielou_evenness": round(j_even, 4), "species_richness": float(s)}
        return BiodiversitasAgentOutput(status="COMPLETED", score=round(j_even, 4), metrics=metrics, shannon_index=round(h_prime, 4), simpson_index=round(d_simp, 4), evenness=round(j_even, 4))
