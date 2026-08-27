"""Contracts: AgentResult."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, List, Optional


@dataclass
class AgentResult:
    """Agent execution result object with typed metadata."""
    agent_id: str
    success: bool
    data: Any
    confidence: float = 1.0
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    evidence_ids: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
