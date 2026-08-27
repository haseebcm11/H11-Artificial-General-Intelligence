"""Evidence ledger."""
from __future__ import annotations

from typing import Dict, List, Optional

from .item import EvidenceItem


class EvidenceLedger:
    """Append-only evidence provenance ledger."""

    def __init__(self) -> None:
        self.items: Dict[str, EvidenceItem] = {}

    def add_evidence(
        self,
        claim: str,
        source: str,
        confidence: float = 1.0,
        provenance: str = "",
        relationship: str = "PRIMARY_FACT",
    ) -> EvidenceItem:
        item = EvidenceItem(
            claim=claim,
            source=source,
            provenance=provenance,
            confidence=confidence,
            relationship_to_case=relationship,
        )
        self.items[item.evidence_id] = item
        return item

    def get_evidence(self, evidence_id: str) -> Optional[EvidenceItem]:
        return self.items.get(evidence_id)
