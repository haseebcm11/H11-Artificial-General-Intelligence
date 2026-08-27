"""
Agent Module: D12_APPSEC
Agent Class: AppsecAgent

Application security CVSS v3.1 Base Score formula Score = min(10, 1.08 * (Impact + Exploitability)) and taint flow propagation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D12_APPSEC"


class AppsecError(ValueError):
    """Raised when AppsecAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class AppsecAgentInput:
    impact_subscore: float = 5.8
    exploitability_subscore: float = 3.9


@dataclass(frozen=True)
class AppsecAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    cvss_score: float = 0.0


class AppsecAgent:
    """
    Application security CVSS v3.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: AppsecAgentInput) -> AppsecAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        cvss = min(10.0, 1.08 * (inputs.impact_subscore + inputs.exploitability_subscore))
        score = round(cvss / 10.0, 4)
        metrics = {"cvss_base": round(cvss, 1), "impact": inputs.impact_subscore, "exploitability": inputs.exploitability_subscore}
        return AppsecAgentOutput(status="COMPLETED", score=score, metrics=metrics, cvss_score=round(cvss, 1))
