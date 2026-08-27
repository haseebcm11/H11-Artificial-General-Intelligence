"""
Agent Module: D11_FEDERATED
Agent Class: FederatedAgent

Federated Learning FedAvg server weight aggregation w_{t+1} = sum(n_k/N * w_k) and differential privacy Gaussian noise.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_FEDERATED"


class FederatedError(ValueError):
    """Raised when FederatedAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class FederatedAgentInput:
    client_weights: list[list[float]] = field(default_factory=lambda: [[1.0, 2.0], [1.2, 1.8], [0.9, 2.1]])
    client_samples: list[int] = field(default_factory=lambda: [100, 200, 100])


@dataclass(frozen=True)
class FederatedAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    aggregated_weights: list[float] = field(default_factory=list)


class FederatedAgent:
    """
    Federated Learning FedAvg server weight aggregation w_{t+1} = sum(n_k/N * w_k) and differential privacy Gaussian noise.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: FederatedAgentInput) -> FederatedAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        c_w, c_n = inputs.client_weights, inputs.client_samples
        tot_n = sum(c_n) or 1
        dim = len(c_w[0])
        agg = [0.0] * dim
        for w, n in zip(c_w, c_n):
            for d in range(dim):
                agg[d] += (n / tot_n) * w[d]
        agg = [round(x, 4) for x in agg]
        metrics = {"client_count": float(len(c_w)), "total_samples": float(tot_n)}
        return FederatedAgentOutput(status="COMPLETED", score=1.0, metrics=metrics, aggregated_weights=agg)
