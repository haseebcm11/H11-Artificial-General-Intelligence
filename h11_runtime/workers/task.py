"""Worker task data structure with priorities and cancellation tokens."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
import uuid


@dataclass
class WorkerTask:
    """Individual computational task dispatched to C02 WorkerPool (v3.0 Section 45)."""
    task_id: str = field(default_factory=lambda: f"TSK-{uuid.uuid4().hex[:8].upper()}")
    node_id: str = ""
    agent_id: str = ""
    name: str = ""
    func: Optional[Callable[..., Any]] = None
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5  # 1 (highest) to 10 (lowest)
    status: str = "PENDING"  # PENDING, QUEUED, RUNNING, COMPLETED, FAILED, CANCELLED
    result: Optional[Any] = None
    error: Optional[str] = None
    timeout_seconds: float = 60.0
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None

    @property
    def latency_ms(self) -> float:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at) * 1000.0
        return 0.0

    def cancel(self, reason: str = "USER_CANCELLED") -> None:
        if self.status in ("PENDING", "QUEUED"):
            self.status = "CANCELLED"
            self.error = reason
            self.completed_at = time.time()
