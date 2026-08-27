"""H11-AGI Enhancement Protocol v1.0 — Append-Only Ledger & Evolutionary Memory Graph.

Sections 28, 36, 37: Immutable evolutionary record preserving what worked,
what failed, and why.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import time
from typing import Any, Dict, List, Optional

from .protocol import EnhancementObject, EnhancementState, PromotionLevel


@dataclass
class LedgerRecord:
    enhancement_id: str
    parent_version: str
    candidate_version: str
    target: str
    author: str
    authority: str
    reason: str
    change_type: str
    risk: str
    validation_summary: str
    decision: str
    outcome: str
    timestamp: float = field(default_factory=time.time)
    previous_hash: str = ""
    record_hash: str = ""

    def compute_hash(self) -> str:
        payload = f"{self.enhancement_id}|{self.parent_version}|{self.candidate_version}|{self.target}|{self.decision}|{self.outcome}|{self.timestamp}|{self.previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class EnhancementLedger:
    """Section 28: Append-only cryptographic ledger of all H11 enhancements."""

    def __init__(self) -> None:
        self.records: List[LedgerRecord] = []
        self._genesis_hash = "H11_GENESIS_ROOT_00000000000000000000000000000000000000000000000000000000"

    def record_outcome(
        self,
        enhancement: EnhancementObject,
        candidate_version: str,
        authority: str,
        decision: str,
        outcome: str,
        validation_summary: str = "Passed all pipeline gates",
    ) -> LedgerRecord:
        prev_hash = self.records[-1].record_hash if self.records else self._genesis_hash
        rec = LedgerRecord(
            enhancement_id=enhancement.enhancement_id,
            parent_version=enhancement.parent_version,
            candidate_version=candidate_version,
            target=enhancement.target,
            author=enhancement.created_by,
            authority=authority,
            reason=enhancement.problem,
            change_type=enhancement.change_type.value,
            risk=enhancement.risk_class.value,
            validation_summary=validation_summary,
            decision=decision,
            outcome=outcome,
            previous_hash=prev_hash,
        )
        rec.record_hash = rec.compute_hash()
        self.records.append(rec)
        return rec

    def verify_integrity(self) -> bool:
        """Verify unbroken cryptographic hash chain across the ledger."""
        for i, rec in enumerate(self.records):
            expected_prev = self.records[i - 1].record_hash if i > 0 else self._genesis_hash
            if rec.previous_hash != expected_prev:
                return False
            if rec.record_hash != rec.compute_hash():
                return False
        return True


class EvolutionaryMemoryGraph:
    """Section 37: Knowledge graph of problems, causes, solutions, and anti-patterns."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, str]] = []  # {src, dst, relation}

    def add_problem(self, problem_id: str, description: str, category: str) -> None:
        self.nodes[problem_id] = {"type": "PROBLEM", "description": description, "category": category}

    def add_cause(self, cause_id: str, root_cause: str) -> None:
        self.nodes[cause_id] = {"type": "CAUSE", "root_cause": root_cause}

    def add_enhancement(self, enh_id: str, change: str, outcome: str) -> None:
        self.nodes[enh_id] = {"type": "ENHANCEMENT", "change": change, "outcome": outcome}

    def link(self, src: str, dst: str, relation: str) -> None:
        """Relations: CAUSED_BY, ADDRESSED_BY, FAILED_BECAUSE, IMPROVED_BY, SUPERSEDED_BY."""
        self.edges.append({"src": src, "dst": dst, "relation": relation})

    def has_failed_pattern(self, target: str, strategy: str) -> bool:
        """Section 36: Check if strategy previously failed to avoid rediscovery."""
        for edge in self.edges:
            if edge["relation"] == "FAILED_BECAUSE":
                node = self.nodes.get(edge["src"], {})
                if node.get("change") == strategy:
                    return True
        return False
