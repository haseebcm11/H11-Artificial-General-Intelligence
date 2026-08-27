"""Memory record definition."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any


@dataclass
class MemoryRecord:
    memory_id: str
    content: Any
    category: str
    importance: float = 0.5
    access_count: int = 1
    last_accessed: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
