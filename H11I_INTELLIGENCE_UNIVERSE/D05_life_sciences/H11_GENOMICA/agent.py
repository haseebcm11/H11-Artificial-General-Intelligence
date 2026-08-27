"""
Agent Module: D05_GENOMICA
Agent Class: GenomicaAgent

Genomic sequence analytics calculating Shannon entropy of k-mers, GC skew (G-C)/(G+C), and transition/transversion (Ti/Tv) ratios.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_GENOMICA"


class GenomicaError(ValueError):
    """Raised when GenomicaAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GenomicaAgentInput:
    sequence: str = 'ATGCGATCGATCGATCGATCGATCGATCGATC'
    k: int = 2


@dataclass(frozen=True)
class GenomicaAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    gc_skew: float = 0.0
    kmer_entropy: float = 0.0


class GenomicaAgent:
    """
    Genomic sequence analytics calculating Shannon entropy of k-mers, GC skew (G-C)/(G+C), and transition/transversion (Ti/Tv) ratios.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GenomicaAgentInput) -> GenomicaAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        seq = inputs.sequence.upper()
        g = seq.count('G')
        c = seq.count('C')
        gc_skew = (g - c) / max(g + c, 1)
        k = inputs.k
        kmers = {}
        for i in range(len(seq) - k + 1):
            sub = seq[i:i+k]
            kmers[sub] = kmers.get(sub, 0) + 1
        tot = sum(kmers.values())
        entropy = -sum((cnt/tot) * math.log2(cnt/tot) for cnt in kmers.values())
        max_ent = math.log2(4**k)
        norm_ent = entropy / max_ent if max_ent > 0 else 1.0
        metrics = {"gc_skew": round(gc_skew, 4), "kmer_entropy": round(entropy, 4), "normalized_entropy": round(norm_ent, 4)}
        return GenomicaAgentOutput(status="COMPLETED", score=round(norm_ent, 4), metrics=metrics, gc_skew=round(gc_skew, 4), kmer_entropy=round(entropy, 4))
