"""Contracts: ActionProposal with Dynamic Risk Scoring and Safety Verification."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid

from .envelope import RiskClass


@dataclass
class ActionProposal:
    """11 — ActionProposal: Structured candidate action submitted to H11C-ALIGN-ENFORCE."""
    proposal_id: str = field(default_factory=lambda: f"ACT-PROP-{uuid.uuid4().hex[:8].upper()}")
    case_id: str = ""
    originating_agent: str = ""
    action_type: str = "TOOL_CALL"  # TOOL_CALL, STATE_MUTATION, NETWORK_EGRESS, PERSIST_RECORD, EMIT_RESULT
    target_resource: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    payload: Dict[str, Any] = field(default_factory=dict)
    risk_class: RiskClass = RiskClass.R1_LOW
    rationale: str = ""
    prerequisites: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    evaluated: bool = False
    evaluation_decision: Optional[str] = None
    proposal_hash: str = ""

    def __post_init__(self) -> None:
        if self.payload and not self.parameters:
            self.parameters = self.payload
        elif self.parameters and not self.payload:
            self.payload = self.parameters
        if not self.proposal_hash:
            self.proposal_hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Generates deterministic SHA-256 fingerprint for proposal deduplication and auditing."""
        norm_dict = {
            "origin": self.originating_agent,
            "type": self.action_type,
            "target": self.target_resource,
            "params": self.parameters,
        }
        encoded = json.dumps(norm_dict, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def compute_risk_score(self) -> float:
        """Computes continuous risk score [0.0 - 1.0] across sensitive action patterns."""
        score = 0.1
        if self.action_type in ("STATE_MUTATION", "PERSIST_RECORD"):
            score += 0.25
        elif self.action_type == "NETWORK_EGRESS":
            score += 0.45

        # Check for sensitive parameter keywords
        param_str = json.dumps(self.parameters).lower()
        sensitive_keywords = ["delete", "drop", "grant", "exec", "sudo", "secret", "override", "bypass", "token"]
        for kw in sensitive_keywords:
            if kw in param_str:
                score += 0.15

        if self.risk_class == RiskClass.R3_CRITICAL:
            score = max(score, 0.9)
        elif self.risk_class in (RiskClass.R2_MODERATE, RiskClass.R2_SIGNIFICANT):
            score = max(score, 0.5)

        return min(1.0, score)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "case_id": self.case_id,
            "originating_agent": self.originating_agent,
            "action_type": self.action_type,
            "target_resource": self.target_resource,
            "parameters": self.parameters,
            "payload": self.payload,
            "risk_class": self.risk_class.value if hasattr(self.risk_class, "value") else str(self.risk_class),
            "risk_score": self.compute_risk_score(),
            "rationale": self.rationale,
            "prerequisites": self.prerequisites,
            "side_effects": self.side_effects,
            "timestamp": self.timestamp,
            "evaluated": self.evaluated,
            "evaluation_decision": self.evaluation_decision,
            "proposal_hash": self.proposal_hash,
        }
