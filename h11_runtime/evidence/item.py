"""Evidence item."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any
import uuid


@dataclass
class EvidenceItem:
    """Individual structured evidence datum (v3.0 Section 27)."""
    evidence_id: str = field(default_factory=lambda: f"EVID-{uuid.uuid4().hex[:8].upper()}")
    claim: str = ""
    source: str = ""
    provenance: str = ""
    confidence: float = 1.0
    relationship_to_case: str = "PRIMARY_FACT"
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)
