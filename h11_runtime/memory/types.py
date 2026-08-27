"""Memory classification types."""
from enum import Enum


class MemoryType(str, Enum):
    """L10 Memory classifications (v3.0 Section 25)."""
    WORKING = "WORKING"
    SHORTTERM = "SHORTTERM"
    LONGTERM = "LONGTERM"
    EPISODIC = "EPISODIC"
    SEMANTIC = "SEMANTIC"
    PROCEDURAL = "PROCEDURAL"
    RETRIEVAL = "RETRIEVAL"
    CONSOLIDATION = "CONSOLIDATION"
