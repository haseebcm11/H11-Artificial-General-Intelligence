"""Memory service coordinating Working, Episodic, Semantic, and Procedural Memory."""
from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, List, Optional

from .record import MemoryRecord
from .types import MemoryType

logger = logging.getLogger(__name__)


class MemoryService:
    """15 — L10 Hierarchical Memory Services (Working, Episodic, Semantic, Procedural) (v3.0 Section 25)."""

    def __init__(self, max_working_entries: int = 1000, max_episodic_entries: int = 50000) -> None:
        self.working_memory: Dict[str, Any] = {}
        self.working_ttls: Dict[str, float] = {}
        self.episodic_store: List[MemoryRecord] = []
        self.semantic_store: Dict[str, MemoryRecord] = {}
        self.procedural_store: Dict[str, Any] = {}
        self.max_working_entries = max_working_entries
        self.max_episodic_entries = max_episodic_entries

    def store_working(self, key: str, value: Any, ttl_seconds: float = 3600.0) -> None:
        """Stores short-term working context with expiration."""
        self.working_memory[key] = value
        self.working_ttls[key] = time.time() + ttl_seconds

    def recall_working(self, key: str) -> Optional[Any]:
        """Recalls working context if unexpired."""
        if key not in self.working_memory:
            return None
        if time.time() > self.working_ttls.get(key, 0.0):
            self.working_memory.pop(key, None)
            self.working_ttls.pop(key, None)
            return None
        return self.working_memory.get(key)

    def store_episodic(
        self,
        content: Any,
        importance: float = 0.8,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryRecord:
        """Stores episodic case experience with importance score."""
        rec = MemoryRecord(
            memory_id=f"EPISODE-{len(self.episodic_store) + 1}",
            content=content,
            category=MemoryType.EPISODIC.value,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {},
        )
        self.episodic_store.append(rec)
        if len(self.episodic_store) > self.max_episodic_entries:
            # Evict weakest decayed record
            self.episodic_store.sort(key=lambda r: r.compute_current_strength(), reverse=True)
            self.episodic_store = self.episodic_store[:self.max_episodic_entries]
        return rec

    def store_semantic(
        self,
        concept: str,
        definition_or_fact: Any,
        importance: float = 0.9,
        tags: Optional[List[str]] = None,
    ) -> MemoryRecord:
        """Stores persistent semantic knowledge indexed by concept identifier."""
        rec = MemoryRecord(
            memory_id=f"SEM-{concept.lower().replace(' ', '_')}",
            content=definition_or_fact,
            category=MemoryType.SEMANTIC.value,
            importance=importance,
            tags=tags or [],
            half_life_seconds=86400.0 * 365.0,  # 1-year half-life for semantic facts
        )
        self.semantic_store[concept] = rec
        return rec

    def recall_semantic(self, concept: str) -> Optional[Any]:
        """Recalls semantic fact and boosts retention."""
        rec = self.semantic_store.get(concept)
        if rec:
            rec.access()
            return rec.content
        return None

    def store_procedural(self, skill_name: str, routine: Callable[..., Any]) -> None:
        """Stores executable procedural skill routine."""
        self.procedural_store[skill_name] = routine

    def execute_procedural(self, skill_name: str, *args, **kwargs) -> Any:
        """Executes stored procedural routine."""
        routine = self.procedural_store.get(skill_name)
        if not routine:
            raise KeyError(f"Procedural skill '{skill_name}' not registered in memory.")
        return routine(*args, **kwargs)

    def consolidate(self, min_importance_for_semantic: float = 0.85) -> int:
        """Runs L10 memory consolidation pass: distills recurring episodic patterns to semantic store."""
        promoted = 0
        for ep in self.episodic_store:
            if ep.compute_current_strength() >= min_importance_for_semantic and ep.access_count >= 3:
                concept_key = f"CONSOLIDATED_{ep.memory_id}"
                if concept_key not in self.semantic_store:
                    self.store_semantic(concept_key, ep.content, importance=ep.importance)
                    promoted += 1
        logger.info(f"Memory consolidation pass promoted {promoted} episodic records to semantic knowledge.")
        return promoted
