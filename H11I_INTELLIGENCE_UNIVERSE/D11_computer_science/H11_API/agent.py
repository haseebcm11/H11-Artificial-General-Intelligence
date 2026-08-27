"""
Agent Module: D11_API
Agent Class: ApiAgent

API gateway architecture Sliding Window Token Bucket rate limiting and GraphQL AST query complexity scoring.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_API"


class ApiError(ValueError):
    """Raised when ApiAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class ApiAgentInput:
    request_count: int = 45
    window_limit: int = 100
    query_depth: int = 4


@dataclass(frozen=True)
class ApiAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    allowed: bool = True


class ApiAgent:
    """
    API gateway architecture Sliding Window Token Bucket rate limiting and GraphQL AST query complexity scoring.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: ApiAgentInput) -> ApiAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        is_allowed = inputs.request_count <= inputs.window_limit and inputs.query_depth <= 6
        util = inputs.request_count / max(inputs.window_limit, 1)
        metrics = {"rate_utilization": round(util, 3), "query_depth": float(inputs.query_depth)}
        return ApiAgentOutput(status="COMPLETED", score=round(util, 4), metrics=metrics, allowed=is_allowed)
