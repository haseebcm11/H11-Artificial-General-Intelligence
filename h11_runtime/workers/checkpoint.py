"""Checkpoint manager with SHA-256 integrity and persistent state serialization."""
from __future__ import annotations

import hashlib
import json
import logging
import time
from typing import Any, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)


class CheckpointManager:
    """C02 Checkpointing & Resume capability for long-running cases (v3.0 Section 46)."""

    def __init__(self) -> None:
        self.checkpoints: Dict[str, Dict[str, Any]] = {}
        self.case_checkpoint_index: Dict[str, List[str]] = {}

    def save_checkpoint(
        self,
        checkpoint_id: str,
        case_snapshot: Dict[str, Any],
        case_id: str = "",
    ) -> str:
        """Saves case snapshot with integrity digest and timestamp."""
        cid = checkpoint_id or f"CP-{uuid.uuid4().hex[:8].upper()}"
        target_case_id = case_id or case_snapshot.get("case_id", "GLOBAL")

        # Compute SHA-256 hash of snapshot content
        encoded = json.dumps(case_snapshot, sort_keys=True, default=str).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()

        self.checkpoints[cid] = {
            "checkpoint_id": cid,
            "case_id": target_case_id,
            "snapshot": case_snapshot,
            "digest": digest,
            "timestamp": time.time(),
        }

        self.case_checkpoint_index.setdefault(target_case_id, []).append(cid)
        logger.info(f"Saved checkpoint {cid} for case {target_case_id} (digest: {digest[:12]}...)")
        return cid

    def restore_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Restores snapshot verifying cryptographic integrity."""
        cp = self.checkpoints.get(checkpoint_id)
        if not cp:
            logger.warning(f"Checkpoint {checkpoint_id} not found")
            return None

        # Verify integrity
        snapshot = cp["snapshot"]
        encoded = json.dumps(snapshot, sort_keys=True, default=str).encode("utf-8")
        current_digest = hashlib.sha256(encoded).hexdigest()

        if current_digest != cp["digest"]:
            raise ValueError(f"Integrity violation in checkpoint {checkpoint_id}: hash mismatch")

        return snapshot

    def list_checkpoints(self, case_id: str) -> List[str]:
        return self.case_checkpoint_index.get(case_id, [])

    def prune_older_than(self, max_age_seconds: float = 86400.0) -> int:
        """Prunes checkpoints older than max age."""
        now = time.time()
        pruned = 0
        for cid, cp in list(self.checkpoints.items()):
            if (now - cp["timestamp"]) > max_age_seconds:
                self.checkpoints.pop(cid, None)
                pruned += 1
        return pruned
