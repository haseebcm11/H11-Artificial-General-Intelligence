"""Resource budget state with Token, Compute, Cost, and Activation Boundaries."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional


@dataclass
class ResourceBudget:
    """Explicit resource boundaries bounding cognitive execution (v3.0 Section 53-54)."""
    compute_budget_sec: float = 60.0
    memory_budget_mb: float = 2048.0
    time_budget_sec: float = 45.0
    token_budget: int = 128_000
    cost_budget_usd: float = 1.00
    concurrency_limit: int = 16
    max_tool_calls: int = 50
    max_agent_activations: int = 30
    
    # Consumed metrics
    used_compute_sec: float = 0.0
    used_tokens: int = 0
    used_cost_usd: float = 0.0
    used_tool_calls: int = 0
    used_agent_activations: int = 0
    start_time: float = field(default_factory=time.time)

    def can_activate_agent(self) -> bool:
        if self.is_time_exhausted():
            return False
        return self.used_agent_activations < self.max_agent_activations

    def can_call_tool(self) -> bool:
        if self.is_time_exhausted():
            return False
        return self.used_tool_calls < self.max_tool_calls

    def can_consume_tokens(self, tokens: int) -> bool:
        return (self.used_tokens + tokens) <= self.token_budget

    def consume_agent_activation(self, count: int = 1) -> None:
        self.used_agent_activations += count

    def consume_tool_call(self, count: int = 1) -> None:
        self.used_tool_calls += count

    def consume_tokens(self, tokens: int, cost_per_1k: float = 0.002) -> None:
        self.used_tokens += tokens
        self.used_cost_usd += (tokens / 1000.0) * cost_per_1k

    def is_time_exhausted(self) -> bool:
        return (time.time() - self.start_time) >= self.time_budget_sec

    def compute_headroom_pct(self) -> float:
        """Computes minimum remaining resource headroom percentage."""
        ratios = [
            (self.max_agent_activations - self.used_agent_activations) / max(1, self.max_agent_activations),
            (self.max_tool_calls - self.used_tool_calls) / max(1, self.max_tool_calls),
            (self.token_budget - self.used_tokens) / max(1, self.token_budget),
            max(0.0, (self.time_budget_sec - (time.time() - self.start_time))) / max(1.0, self.time_budget_sec),
        ]
        return max(0.0, min(ratios)) * 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compute_budget_sec": self.compute_budget_sec,
            "memory_budget_mb": self.memory_budget_mb,
            "time_budget_sec": self.time_budget_sec,
            "token_budget": self.token_budget,
            "used_tokens": self.used_tokens,
            "used_cost_usd": round(self.used_cost_usd, 4),
            "used_tool_calls": self.used_tool_calls,
            "used_agent_activations": self.used_agent_activations,
            "headroom_pct": round(self.compute_headroom_pct(), 2),
            "time_exhausted": self.is_time_exhausted(),
        }
