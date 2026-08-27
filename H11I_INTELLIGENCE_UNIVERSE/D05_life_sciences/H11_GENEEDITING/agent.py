"""
Agent Module: D05_GENEEDITING
Agent Class: GeneeditingAgent

CRISPR-Cas9 Cutting Frequency Determination (CFD) off-target penalty score and Doench on-target guide RNA cleavage efficiency.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D05_GENEEDITING"


class GeneeditingError(ValueError):
    """Raised when GeneeditingAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class GeneeditingAgentInput:
    guide_seq: str = 'GACGTAACCGTGATCGATCG'
    mismatch_positions: list[int] = field(default_factory=lambda: [3, 12])
    has_canonical_pam: bool = True


@dataclass(frozen=True)
class GeneeditingAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    cfd_score: float = 0.0


class GeneeditingAgent:
    """
    CRISPR-Cas9 Cutting Frequency Determination (CFD) off-target penalty score and Doench on-target guide RNA cleavage efficiency.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: GeneeditingAgentInput) -> GeneeditingAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        pam_factor = 1.0 if inputs.has_canonical_pam else 0.15
        cfd = pam_factor
        for pos in inputs.mismatch_positions:
            pen = 0.5 + 0.02 * min(pos, 20)  # PAM-proximal seeds penalize more
            cfd *= max(0.01, min(1.0, 1.0 - pen))
        gc_content = sum(1 for c in inputs.guide_seq if c in 'GCgc') / max(len(inputs.guide_seq), 1)
        on_target = max(0.0, 1.0 - abs(gc_content - 0.5) * 2.0)
        metrics = {"cfd_score": round(cfd, 4), "gc_content": round(gc_content, 4), "on_target_efficiency": round(on_target, 4)}
        return GeneeditingAgentOutput(status="COMPLETED", score=round(cfd, 4), metrics=metrics, cfd_score=round(cfd, 4))
