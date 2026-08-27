"""Worker task representation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class WorkerTask:
    task_id: str
    node_id: str
    agent_id: str
    func: Callable[..., Any]
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    status: str = "QUEUED"  # QUEUED, RUNNING, COMPLETED, FAILED
    result: Optional[Any] = None
    error: Optional[str] = None
