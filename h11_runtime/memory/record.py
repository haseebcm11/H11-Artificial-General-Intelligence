"""Memory record definition with Decay Modeling and Semantic Embeddings."""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import time
from typing import Any, Dict, List, Optional
import uuid

from .types import MemoryType


@dataclass
class MemoryRecord:
    """Structured memory entry across L10 hierarchical memory strata (v3.0 Section 25)."""
    memory_id: str = field(default_factory=lambda: f"MEM-{uuid.uuid4().hex[:8].upper()}")
    content: Any = None
    category: str = "WORKING"  # WORKING, EPISODIC, SEMANTIC, PROCEDURAL
    importance: float = 0.5
    access_count: int = 1
    embedding: Optional[List[float]] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    half_life_seconds: float = 86400.0  # 24-hour decay half-life default
    last_accessed: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)

    def access(self) -> None:
        """Records memory access and refreshes decay baseline."""
        self.access_count += 1
        self.last_accessed = time.time()

    def compute_current_strength(self) -> float:
        """Computes time-decayed memory retention strength: S(t) = S0 * exp(-dt / tau)."""
        dt = max(0.0, time.time() - self.last_accessed)
        tau = self.half_life_seconds / math.log(2.0)
        decay = math.exp(-dt / tau)
        # Boost retention with repetition/access count
        frequency_boost = min(2.0, 1.0 + 0.1 * math.log(1.0 + self.access_count))
        return min(1.0, self.importance * decay * frequency_boost)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "content": self.content,
            "category": self.category,
            "importance": self.importance,
            "current_strength": self.compute_current_strength(),
            "access_count": self.access_count,
            "tags": self.tags,
            "metadata": self.metadata,
            "last_accessed": self.last_accessed,
            "created_at": self.created_at,
        }
