"""Case lifecycle states."""
from enum import Enum


class CaseState(str, Enum):
    """Case lifecycle state machine (v3.0 Section 5)."""
    # 13 Canonical progression states
    NEW = "NEW"
    ADMITTED = "ADMITTED"
    CONTEXTUALIZED = "CONTEXTUALIZED"
    MAPPED = "MAPPED"
    COMPOSED = "COMPOSED"
    READY = "READY"
    EXECUTING = "EXECUTING"
    INTEGRATING = "INTEGRATING"
    VERIFYING = "VERIFYING"
    ALIGNING = "ALIGNING"
    RELEASED = "RELEASED"
    MEMORIZED = "MEMORIZED"
    CLOSED = "CLOSED"

    # Exceptional & Control states
    REJECTED = "REJECTED"
    HALTED = "HALTED"
    WAITING = "WAITING"
    RETRYING = "RETRYING"
    DEGRADED = "DEGRADED"
    QUARANTINED = "QUARANTINED"
    ROLLED_BACK = "ROLLED_BACK"

    # Backwards compatibility aliases
    CREATED = "NEW"
    CONTEXT_PACKED = "CONTEXTUALIZED"
    CAPABILITIES_MAPPED = "MAPPED"
    AGENTS_BOUND = "COMPOSED"
    GRAPH_BUILT = "READY"
    MERGED = "INTEGRATING"
    LICENSED = "RELEASED"
    COMMITTED = "MEMORIZED"
    COMPLETED = "CLOSED"
