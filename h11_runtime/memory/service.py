"""Memory service."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .record import MemoryRecord


class MemoryService:
    """15 — L10 Hierarchical Memory Services (Working, Episodic, Semantic, Procedural)."""

    def __init__(self) -> None:
        self.working_memory: Dict[str, Any] = {}
        self.episodic_store: List[MemoryRecord] = []
        self.semantic_store: Dict[str, MemoryRecord] = []
        self.procedural_store: Dict[str, Any] = {}

    def store_working(self, key: str, value: Any) -> None:
        self.working_memory[key] = value

    def recall_working(self, key: str) -> Optional[Any]:
        return self.working_memory.get(key)

    def store_episodic(self, content: Any, importance: float = 0.8) -> MemoryRecord:
        rec = MemoryRecord(
            memory_id=f"EPISODE-{len(self.episodic_store) + 1}",
            content=content,
            category="EPISODIC",
            importance=importance,
        )
        self.episodic_store.append(rec)
        return rec
