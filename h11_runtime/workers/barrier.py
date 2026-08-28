"""Join barrier synchronization with Async Wait and Partial Resolution Policies."""
from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional


class JoinBarrier:
    """C02 Join Barrier: Synchronizes parallel cognitive executions before branch merge (v3.0 Section 42)."""

    def __init__(
        self,
        expected_branches: int,
        barrier_id: str = "",
        policy: str = "WAIT_ALL",  # WAIT_ALL, WAIT_MAJORITY, WAIT_FIRST
        timeout_seconds: float = 30.0,
    ) -> None:
        self.expected_branches = expected_branches
        self.barrier_id = barrier_id or f"BARRIER-{time.time()}"
        self.policy = policy
        self.timeout_seconds = timeout_seconds
        self.arrived_results: List[Any] = []
        self.branch_metadata: Dict[str, Any] = {}
        self._event = asyncio.Event()
        self.created_at = time.time()
        self.completed_at: Optional[float] = None

    def arrive(self, result: Any, branch_id: str = "") -> bool:
        """Records arrival of a branch result. Returns True if barrier threshold reached."""
        self.arrived_results.append(result)
        if branch_id:
            self.branch_metadata[branch_id] = {"arrived_at": time.time(), "result": result}

        threshold = self._get_threshold()
        if len(self.arrived_results) >= threshold:
            self.completed_at = time.time()
            self._event.set()
            return True
        return False

    def is_complete(self) -> bool:
        return len(self.arrived_results) >= self._get_threshold()

    def _get_threshold(self) -> int:
        if self.policy == "WAIT_FIRST":
            return 1
        elif self.policy == "WAIT_MAJORITY":
            return (self.expected_branches // 2) + 1
        return self.expected_branches

    async def wait(self) -> List[Any]:
        """Asynchronously waits for the barrier to trip or timeout."""
        if self.is_complete():
            return self.arrived_results

        try:
            await asyncio.wait_for(self._event.wait(), timeout=self.timeout_seconds)
        except asyncio.TimeoutError:
            pass  # Return whatever arrived before timeout

        return self.arrived_results
