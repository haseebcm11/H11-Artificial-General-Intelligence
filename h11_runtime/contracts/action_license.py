"""Contracts: ActionLicense."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
import uuid


@dataclass
class ActionLicense:
    """12 — ActionLicense: Authoritative cryptographic action token."""
    license_id: str = field(default_factory=lambda: f"LIC-{uuid.uuid4().hex[:8].upper()}")
    proposal_id: str = ""
    case_id: str = ""
    authorized_action: str = ""
    target_resource: str = ""
    authority_id: str = "H11C_ALIGN_ENFORCE"
    issued_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    signature: str = ""

    def is_valid(self) -> bool:
        return self.expires_at > time.time()
