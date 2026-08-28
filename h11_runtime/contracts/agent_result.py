"""Contracts: AgentResult with Metadata, Provenance, Claims, Evidence, and Uncertainty."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class AgentResult:
    """10 — AgentResult: Typed execution result emitted by an active specialist agent (v3.0 Section 19)."""
    agent_id: str
    success: bool
    data: Any = None
    canonical_id: str = ""
    claims: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 1.0
    uncertainty: float = 0.0
    assumptions: List[str] = field(default_factory=list)
    proposed_actions: List[str] = field(default_factory=list)
    execution_metadata: Dict[str, Any] = field(default_factory=dict)
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    evidence_ids: List[str] = field(default_factory=list)
    state_mutations: Dict[str, Any] = field(default_factory=dict)
    provenance_hash: str = ""
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if self.data is not None and not self.claims and isinstance(self.data, dict):
            # Extract claims from data dict if available
            for k in ("claims", "conclusions", "findings", "summary", "diagnosis", "recommendations"):
                val = self.data.get(k)
                if isinstance(val, list):
                    self.claims.extend(map(str, val))
                elif isinstance(val, str) and val:
                    self.claims.append(val)
                elif isinstance(val, dict):
                    self.claims.append(f"{k}: {val}")

            if not self.proposed_actions and self.data.get("action"):
                self.proposed_actions.append(str(self.data["action"]))

        if not self.provenance_hash:
            self.provenance_hash = self.compute_provenance()

    @property
    def output(self) -> Any:
        return self.data

    @property
    def output_data(self) -> Any:
        return self.data

    def compute_provenance(self) -> str:
        """Computes deterministic SHA-256 hash of result output, claims, and confidence."""
        payload = f"{self.agent_id}|{self.canonical_id}|{self.success}|{self.confidence}|{self.uncertainty}|{self.latency_ms}|{str(self.data)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "canonical_id": self.canonical_id or self.agent_id,
            "success": self.success,
            "data": self.data,
            "claims": self.claims,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "uncertainty": self.uncertainty,
            "assumptions": self.assumptions,
            "proposed_actions": self.proposed_actions,
            "execution_metadata": self.execution_metadata,
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
            canonical_id=data.get("canonical_id", ""),
            success=data.get("success", False),
            data=data.get("data"),
            claims=data.get("claims", []),
            evidence=data.get("evidence", []),
            confidence=data.get("confidence", 1.0),
            uncertainty=data.get("uncertainty", 0.0),
            assumptions=data.get("assumptions", []),
            proposed_actions=data.get("proposed_actions", []),
            execution_metadata=data.get("execution_metadata", {}),
            latency_ms=data.get("latency_ms", 0.0),
            error_message=data.get("error_message"),
            evidence_ids=data.get("evidence_ids", []),
            state_mutations=data.get("state_mutations", {}),
            provenance_hash=data.get("provenance_hash", ""),
            timestamp=data.get("timestamp", time.time()),
        )
