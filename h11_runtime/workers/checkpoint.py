"""Checkpoint manager."""
from __future__ import annotations

import time
from typing import Any, Dict, Optional


class CheckpointManager:
    """C02 Checkpointing & Resume capability for long-running cases (Section 46)."""

    def __init__(self) -> None:
        self.checkpoints: Dict[str, Dict[str, Any]] = {}

    def save_checkpoint(self, checkpoint_id: str, case_snapshot: Dict[str, Any]) -> str:
        self.checkpoints[checkpoint_id] = {
            "snapshot": case_snapshot,
            "timestamp": time.time(),
        }
        return checkpoint_id

    def restore_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        cp = self.checkpoints.get(checkpoint_id)
        return cp["snapshot"] if cp else None
