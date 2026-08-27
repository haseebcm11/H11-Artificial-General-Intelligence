"""Runtime event definition."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict
import uuid


@dataclass
class RuntimeEvent:
    """Runtime event passing through H11C-EVENT-BUS (v3.0 Section 40-41)."""
    event_id: str = field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8].upper()}")
    event_name: str = ""
    topic: str = "CASE"  # CASE, AGENT, MEMORY, TOOL, VERIFICATION, ALIGNMENT, SECURITY, EVOLUTION
    case_id: str = ""
    source: str = "KERNEL"
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if not self.event_name and self.topic:
            self.event_name = self.topic
        elif not self.topic and self.event_name:
            self.topic = self.event_name
