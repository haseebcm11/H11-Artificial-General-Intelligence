"""
Agent Module: D12_INCIDENT
Agent Class: IncidentAgent

Incident response metrics: Mean Time to Detect (MTTD), Mean Time to Remediate (MTTR), and Cyber Kill Chain progression phase scoring.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D12_INCIDENT"


class IncidentError(ValueError):
    """Raised when IncidentAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class IncidentAgentInput:
    mttd_minutes: float = 15.0
    mttr_minutes: float = 45.0
    kill_chain_stage: int = 3


@dataclass(frozen=True)
class IncidentAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    incident_severity_score: float = 0.0


class IncidentAgent:
    """
    Incident response metrics: Mean Time to Detect (MTTD), Mean Time to Remediate (MTTR), and Cyber Kill Chain progression phase scoring.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: IncidentAgentInput) -> IncidentAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        stage_weight = inputs.kill_chain_stage / 7.0
        time_penalty = min(1.0, (inputs.mttd_minutes + inputs.mttr_minutes) / 120.0)
        sev = (stage_weight * 0.6 + time_penalty * 0.4)
        metrics = {"severity_score": round(sev, 3), "kill_chain_progress": round(stage_weight, 3)}
        return IncidentAgentOutput(status="COMPLETED", score=round(sev, 4), metrics=metrics, incident_severity_score=round(sev, 3))
