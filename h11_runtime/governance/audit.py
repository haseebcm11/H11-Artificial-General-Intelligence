"""Audit chain & cryptographic tamper-evident logging."""
from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Dict, List


class AuditChain:
    """14 — H11C-AUDIT-CHAIN & H11C-WITNESS-LOG: Tamper-evident cryptographic ledger."""

    def __init__(self) -> None:
        self.chain: List[Dict[str, Any]] = []
        self.last_block_hash: str = "GENESIS_ROOT_HASH"

    def record_event(
        self,
        case_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        ts = time.time()
        raw = f"{self.last_block_hash}:{case_id}:{event_type}:{ts}:{json.dumps(payload, sort_keys=True)}"
        block_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        entry = {
            "index": len(self.chain),
            "case_id": case_id,
            "event_type": event_type,
            "payload": payload,
            "prev_hash": self.last_block_hash,
            "hash": block_hash,
            "timestamp": ts,
        }
        self.chain.append(entry)
        self.last_block_hash = block_hash
        return entry

    def verify_chain_integrity(self) -> bool:
        prev = "GENESIS_ROOT_HASH"
        for entry in self.chain:
            raw = f"{prev}:{entry['case_id']}:{entry['event_type']}:{entry['timestamp']}:{json.dumps(entry['payload'], sort_keys=True)}"
            expected = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if entry["hash"] != expected:
                return False
            prev = entry["hash"]
        return True


TamperEvidentLog = AuditChain
WitnessLog = AuditChain
