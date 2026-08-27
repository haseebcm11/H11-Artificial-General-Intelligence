"""Typed message envelope that every spine hop must emit and consume."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

SPINE_SCHEMA_ID = "h11.spine.host_infection_case.v1"

REQUIRED_CASE_KEYS = (
    "case_id",
    "patient_id",
    "travel_history",
    "symptoms",
)


class SchemaError(ValueError):
    """Payload does not satisfy the spine contract."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def hash_embed(text: str, dim: int = 32) -> List[float]:
    """Deterministic hashing-trick embedding so encode/retrieve round-trips."""
    if dim < 1:
        raise SchemaError("dim must be >= 1")
    vec = [0.0] * dim
    h = 2166136261
    for i, ch in enumerate(text):
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
        vec[h % dim] += 1.0
        vec[(h >> 8) % dim] -= 0.35
        vec[(i * 7) % dim] += 0.05
    mag = sum(x * x for x in vec) ** 0.5 or 1.0
    return [x / mag for x in vec]


@dataclass
class Envelope:
    """One hop on the composition bus."""

    trace_id: str
    schema_id: str
    from_agent: str
    to_agent: str
    payload: Dict[str, Any]
    events: List[str] = field(default_factory=list)
    error: Optional[str] = None
    ts: str = field(default_factory=utc_now)

    def require(self, *keys: str) -> None:
        missing = [k for k in keys if k not in self.payload]
        if missing:
            raise SchemaError(f"{self.from_agent}->{self.to_agent} missing {missing}")

    def child(self, from_agent: str, to_agent: str, payload: Dict[str, Any], events: Optional[List[str]] = None) -> "Envelope":
        return Envelope(
            trace_id=self.trace_id,
            schema_id=self.schema_id,
            from_agent=from_agent,
            to_agent=to_agent,
            payload=payload,
            events=list(events or []),
        )


def validate_case(payload: Dict[str, Any]) -> None:
    missing = [k for k in REQUIRED_CASE_KEYS if k not in payload]
    if missing:
        raise SchemaError(f"case missing {missing}")
    if not isinstance(payload["travel_history"], list):
        raise SchemaError("travel_history must be a list")
    if not isinstance(payload["symptoms"], list):
        raise SchemaError("symptoms must be a list")
