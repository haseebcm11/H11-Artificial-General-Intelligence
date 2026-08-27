"""Resource budget state."""
from dataclasses import dataclass


@dataclass
class ResourceBudget:
    """Explicit resource boundaries bounding cognitive execution (Section 53-54)."""
    compute_budget_sec: float = 60.0
    memory_budget_mb: float = 1024.0
    time_budget_sec: float = 30.0
    concurrency_limit: int = 16
    max_tool_calls: int = 50
    max_agent_activations: int = 25
    used_compute_sec: float = 0.0
    used_tool_calls: int = 0
    used_agent_activations: int = 0

    def can_activate_agent(self) -> bool:
        return self.used_agent_activations < self.max_agent_activations

    def can_call_tool(self) -> bool:
        return self.used_tool_calls < self.max_tool_calls
