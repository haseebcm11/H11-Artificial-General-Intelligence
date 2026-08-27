"""
Agent Module: D11_OS
Agent Class: OsAgent

Operating system Completely Fair Scheduler (CFS) virtual runtime vruntime = runtime * (1024/weight) and Banker's safety state.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_OS"


class OsError(ValueError):
    """Raised when OsAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class OsAgentInput:
    execution_time_ms: float = 20.0
    process_nice: int = 0


@dataclass(frozen=True)
class OsAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    vruntime_ms: float = 0.0


class OsAgent:
    """
    Operating system Completely Fair Scheduler (CFS) virtual runtime vruntime = runtime * (1024/weight) and Banker's safety state.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: OsAgentInput) -> OsAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        # CFS weight mapping approx: weight = 1024 / (1.25^nice)
        weight = 1024.0 / (1.25**inputs.process_nice)
        vruntime = inputs.execution_time_ms * (1024.0 / weight)
        metrics = {"vruntime_ms": round(vruntime, 2), "cfs_weight": round(weight, 1)}
        return OsAgentOutput(status="COMPLETED", score=round(min(1.0, 50.0/max(vruntime, 1.0)), 4), metrics=metrics, vruntime_ms=round(vruntime, 2))
