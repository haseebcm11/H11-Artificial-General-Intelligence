"""
Agent Module: D11_DEVOPS
Agent Class: DevopsAgent

DevOps DORA metrics: Lead Time for Changes, Deployment Frequency Poisson rate, and Mean Time to Recovery (MTTR).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_DEVOPS"


class DevopsError(ValueError):
    """Raised when DevopsAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class DevopsAgentInput:
    deployments_per_week: float = 14.0
    lead_time_hours: float = 4.5
    mttr_hours: float = 0.75
    change_failure_rate: float = 0.03


@dataclass(frozen=True)
class DevopsAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    dora_performance_index: float = 0.0


class DevopsAgent:
    """
    DevOps DORA metrics: Lead Time for Changes, Deployment Frequency Poisson rate, and Mean Time to Recovery (MTTR).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: DevopsAgentInput) -> DevopsAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        dora_idx = (min(1.0, inputs.deployments_per_week / 20.0) + max(0.0, 1.0 - inputs.lead_time_hours/24.0) + max(0.0, 1.0 - inputs.mttr_hours/4.0) + max(0.0, 1.0 - inputs.change_failure_rate*5.0)) / 4.0
        metrics = {"dora_index": round(dora_idx, 3), "deploys_week": inputs.deployments_per_week, "cfr": inputs.change_failure_rate}
        return DevopsAgentOutput(status="COMPLETED", score=round(dora_idx, 4), metrics=metrics, dora_performance_index=round(dora_idx, 3))
