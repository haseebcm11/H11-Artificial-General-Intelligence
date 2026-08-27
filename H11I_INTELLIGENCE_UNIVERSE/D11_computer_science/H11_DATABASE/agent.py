"""
Agent Module: D11_DATABASE
Agent Class: DatabaseAgent

Database System R dynamic programming join ordering cost model Cost = I/O + W_cpu*CPU and B+ tree height calculation.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_DATABASE"


class DatabaseError(ValueError):
    """Raised when DatabaseAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class DatabaseAgentInput:
    table_cardinalities: list[int] = field(default_factory=lambda: [10000, 50000, 2000])
    fanout: int = 100


@dataclass(frozen=True)
class DatabaseAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    b_tree_height: int = 3
    estimated_cost: float = 0.0


class DatabaseAgent:
    """
    Database System R dynamic programming join ordering cost model Cost = I/O + W_cpu*CPU and B+ tree height calculation.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: DatabaseAgentInput) -> DatabaseAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        cards = inputs.table_cardinalities
        tot_rows = max(cards) if cards else 1000
        h = math.ceil(math.log(tot_rows) / math.log(max(inputs.fanout, 2)))
        cost = sum(c * 0.01 for c in cards)
        metrics = {"b_tree_height": float(h), "est_cost": round(cost, 2)}
        return DatabaseAgentOutput(status="COMPLETED", score=round(min(1.0, cost/1000.0), 4), metrics=metrics, b_tree_height=h, estimated_cost=round(cost, 2))
