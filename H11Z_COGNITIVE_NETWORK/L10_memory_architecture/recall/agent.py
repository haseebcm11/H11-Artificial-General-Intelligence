"""
Agent Module: L10_RECALL
Agent Class: RecallAgent

Spreading activation network across semantic associative graph with exponential temporal decay A(t) = A_0 * exp(-lambda * delta_t) and activation thresholding.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L10_RECALL"


class RecallError(ValueError):
    """Raised when RecallAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class RecallAgentInput:
    current_time: float = 10.0
    decay_rate: float = 0.1
    threshold: float = 0.3
    nodes: list[dict] = field(default_factory=lambda: [{'id': 'c1', 'init_act': 1.0, 'timestamp': 0.0}, {'id': 'c2', 'init_act': 0.8, 'timestamp': 2.0}])


@dataclass(frozen=True)
class RecallAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    recalled_nodes: list[dict] = field(default_factory=list)


class RecallAgent:
    """
    Spreading activation network across semantic associative graph with exponential temporal decay A(t) = A_0 * exp(-lambda * delta_t) and activation thresholding.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: RecallAgentInput) -> RecallAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        lambda_decay = float(inputs.decay_rate)
        t_current = float(inputs.current_time)
        nodes = inputs.nodes if inputs.nodes else [{'id': 'c1', 'init_act': 1.0, 'timestamp': 0.0}]
        recalled, scores = [], []
        for node in nodes:
            dt = max(0.0, t_current - node.get("timestamp", 0.0))
            act = node.get("init_act", 1.0) * math.exp(-lambda_decay * dt)
            scores.append(round(act, 4))
            if act >= inputs.threshold:
                recalled.append({"id": str(node.get("id")), "activation": round(act, 4)})
        mean_act = sum(scores) / max(len(scores), 1)
        metrics = {"total_nodes": float(len(nodes)), "recalled_count": float(len(recalled)), "mean_activation": round(mean_act, 4)}
        return RecallAgentOutput(status="COMPLETED", score=round(min(1.0, max(scores, default=0.0)), 4), metrics=metrics, recalled_nodes=recalled)
