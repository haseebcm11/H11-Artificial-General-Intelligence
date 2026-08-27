"""
Agent Module: L10_SESSION
Agent Class: SessionAgent

Working session memory manager implementing FIFO sliding context window, token budget degradation, and TTL expiry eviction policy.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L10_SESSION"


class SessionError(ValueError):
    """Raised when SessionAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SessionAgentInput:
    max_token_budget: int = 1000
    session_items: list[dict] = field(default_factory=lambda: [{'tokens': 120, 'ttl': 5, 'priority': 1}, {'tokens': 300, 'ttl': 2, 'priority': 3}, {'tokens': 180, 'ttl': 8, 'priority': 4}])


@dataclass(frozen=True)
class SessionAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    retained_items: list[dict] = field(default_factory=list)


class SessionAgent:
    """
    Working session memory manager implementing FIFO sliding context window, token budget degradation, and TTL expiry eviction policy.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SessionAgentInput) -> SessionAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        max_tokens = int(inputs.max_token_budget)
        items = inputs.session_items if inputs.session_items else []
        valid_items = [it for it in items if it.get("ttl", 1) > 0]
        valid_items.sort(key=lambda x: x.get("priority", 0), reverse=True)
        retained, used_tokens = [], 0
        for it in valid_items:
            t = it.get("tokens", 0)
            if used_tokens + t <= max_tokens:
                retained.append(it)
                used_tokens += t
        utilization = used_tokens / max(max_tokens, 1)
        metrics = {"initial_items": float(len(items)), "retained_items": float(len(retained)), "tokens_used": float(used_tokens), "budget_utilization": round(utilization, 4)}
        return SessionAgentOutput(status="COMPLETED", score=round(utilization, 4), metrics=metrics, retained_items=retained)
