"""Contracts: AgentResult with Metadata, Provenance, and Metrics."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class AgentResult:
    """10 — AgentResult: Typed execution result emitted by an active specialist agent."""
    agent_id: str
    success: bool
    data: Any
    confidence: float = 1.0
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    evidence_ids: List[str] = field(default_factory=list)
    state_mutations: Dict[str, Any] = field(default_factory=dict)
    provenance_hash: str = ""
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if not self.provenance_hash:
            self.provenance_hash = self.compute_provenance()

    @property
    def output_data(self) -> Any:
        return self.data

    def compute_provenance(self) -> str:
        """Computes deterministic SHA-256 hash of result output and confidence."""
        payload = f"{self.agent_id}|{self.success}|{self.confidence}|{self.latency_ms}|{str(self.data)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "success": self.success,
            "data": self.data,
            "confidence": self.confidence,
            "latency_ms": self.latency_ms,
            "error_message": self.error_message,
            "evidence_ids": self.evidence_ids,
            "state_mutations": self.state_mutations,
            "provenance_hash": self.provenance_hash,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AgentResult:
        return cls(
            agent_id=data.get("agent_id", ""),
            success=data.get("success", False),
            data=data.get("data"),
            confidence=data.get("confidence", 1.0),
            latency_ms=data.get("latency_ms", 0.0),
            error_message=data.get("error_message"),
            evidence_ids=data.get("evidence_ids", []),
            state_mutations=data.get("state_mutations", {}),
            provenance_hash=data.get("provenance_hash", ""),
            timestamp=data.get("timestamp", time.time()),
        )
