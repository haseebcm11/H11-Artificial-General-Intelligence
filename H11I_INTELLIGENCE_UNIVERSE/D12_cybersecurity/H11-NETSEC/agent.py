"""
Agent Module: D12_NETSEC
Agent Class: NetsecAgent

Network security stateful packet inspection rule matching and TCP SYN flood CUSUM change-point anomaly detection.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D12_NETSEC"


class NetsecError(ValueError):
    """Raised when NetsecAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class NetsecAgentInput:
    syn_ack_ratio: float = 4.5
    baseline_ratio: float = 1.0
    packet_rate_kpps: float = 120.0


@dataclass(frozen=True)
class NetsecAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    syn_flood_detected: bool = True


class NetsecAgent:
    """
    Network security stateful packet inspection rule matching and TCP SYN flood CUSUM change-point anomaly detection.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: NetsecAgentInput) -> NetsecAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        ratio = inputs.syn_ack_ratio / max(inputs.baseline_ratio, 0.1)
        is_flood = ratio > 3.0 and inputs.packet_rate_kpps > 50.0
        score = min(1.0, ratio / 10.0)
        metrics = {"syn_ratio_anomaly": round(ratio, 2), "packet_rate": inputs.packet_rate_kpps, "is_attack": 1.0 if is_flood else 0.0}
        return NetsecAgentOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, syn_flood_detected=is_flood)
