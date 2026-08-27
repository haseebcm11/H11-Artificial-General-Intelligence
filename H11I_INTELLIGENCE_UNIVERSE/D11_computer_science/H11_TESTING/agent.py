"""
Agent Module: D11_TESTING
Agent Class: TestingAgent

Software testing mutation score index MS = K / (M - E) * 100% and branch coverage bitmask tracking.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_TESTING"


class TestingError(ValueError):
    """Raised when TestingAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class TestingAgentInput:
    killed_mutants: int = 85
    total_mutants: int = 100
    equivalent_mutants: int = 5
    covered_branches: int = 48
    total_branches: int = 50


@dataclass(frozen=True)
class TestingAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    mutation_score_pct: float = 0.0
    branch_coverage_pct: float = 0.0


class TestingAgent:
    """
    Software testing mutation score index MS = K / (M - E) * 100% and branch coverage bitmask tracking.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: TestingAgentInput) -> TestingAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        k, m, e = inputs.killed_mutants, inputs.total_mutants, inputs.equivalent_mutants
        ms = (k / max(m - e, 1)) * 100.0
        cov = (inputs.covered_branches / max(inputs.total_branches, 1)) * 100.0
        score = (ms + cov) / 200.0
        metrics = {"mutation_score_pct": round(ms, 2), "branch_coverage_pct": round(cov, 2)}
        return TestingAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, mutation_score_pct=round(ms, 2), branch_coverage_pct=round(cov, 2))
