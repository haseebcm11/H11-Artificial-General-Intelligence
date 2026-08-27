"""Join barrier synchronization."""
from typing import Any, List


class JoinBarrier:
    """C02 Join Barrier: Synchronizes parallel cognitive executions before merge (Section 42-43)."""

    def __init__(self, expected_branches: int) -> None:
        self.expected_branches = expected_branches
        self.arrived_results: List[Any] = []

    def arrive(self, result: Any) -> bool:
        self.arrived_results.append(result)
        return len(self.arrived_results) >= self.expected_branches

    def is_complete(self) -> bool:
        return len(self.arrived_results) >= self.expected_branches
