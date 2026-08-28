"""Contracts: ActionLicense with Cryptographic Verification and Nonce Tracking."""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class ActionLicense:
    """12 — ActionLicense: Authoritative cryptographic action token (v3.0 Section 36-37)."""
    license_id: str = field(default_factory=lambda: f"LIC-{uuid.uuid4().hex[:8].upper()}")
    proposal_id: str = ""
    case_id: str = ""
    authorized_action: str = ""
    target_resource: str = ""
    authority_id: str = "H11C_ALIGN_ENFORCE"
    scopes: List[str] = field(default_factory=lambda: ["execute"])
    constraints: Dict[str, Any] = field(default_factory=dict)
    issued_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    nonce: str = field(default_factory=lambda: uuid.uuid4().hex)
    max_uses: int = 1
    use_count: int = 0
    signature: str = ""
    merkle_proof: Optional[str] = None

    def __post_init__(self) -> None:
        if self.expires_at == 0.0:
            self.expires_at = self.issued_at + 300.0  # 5-minute default TTL
        if not self.signature:
            self.signature = self.compute_signature("H11_ALIGN_SECRET_KEY")

    def compute_signature(self, secret_key: str = "H11_ALIGN_SECRET_KEY") -> str:
        """Computes HMAC-SHA256 signature over license invariants."""
        payload = f"{self.license_id}|{self.proposal_id}|{self.case_id}|{self.authorized_action}|{self.target_resource}|{self.issued_at}|{self.expires_at}|{self.nonce}"
        return hmac.new(secret_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

    def verify(self, secret_key: str = "H11_ALIGN_SECRET_KEY") -> bool:
        """Verifies signature authenticity, expiration, and use limits."""
        if not self.is_valid():
            return False
        expected_sig = self.compute_signature(secret_key)
        return hmac.compare_digest(self.signature, expected_sig)

    def is_valid(self, clock_skew_sec: float = 5.0) -> bool:
        """Checks whether the license is currently valid and unexpired."""
        now = time.time()
        if now > (self.expires_at + clock_skew_sec):
            return False
        if now < (self.issued_at - clock_skew_sec):
            return False
        if self.use_count >= self.max_uses:
            return False
        return True

    def consume(self) -> bool:
        """Consumes one use of the license token. Returns True if execution allowed."""
        if not self.is_valid():
            return False
        self.use_count += 1
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "license_id": self.license_id,
            "proposal_id": self.proposal_id,
            "case_id": self.case_id,
            "authorized_action": self.authorized_action,
            "target_resource": self.target_resource,
            "authority_id": self.authority_id,
            "scopes": self.scopes,
            "constraints": self.constraints,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "nonce": self.nonce,
            "max_uses": self.max_uses,
            "use_count": self.use_count,
            "signature": self.signature,
            "merkle_proof": self.merkle_proof,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ActionLicense:
        return cls(
            license_id=data.get("license_id", ""),
            proposal_id=data.get("proposal_id", ""),
            case_id=data.get("case_id", ""),
            authorized_action=data.get("authorized_action", ""),
            target_resource=data.get("target_resource", ""),
            authority_id=data.get("authority_id", "H11C_ALIGN_ENFORCE"),
            scopes=data.get("scopes", ["execute"]),
            constraints=data.get("constraints", {}),
            issued_at=data.get("issued_at", time.time()),
            expires_at=data.get("expires_at", 0.0),
            nonce=data.get("nonce", ""),
            max_uses=data.get("max_uses", 1),
            use_count=data.get("use_count", 0),
            signature=data.get("signature", ""),
            merkle_proof=data.get("merkle_proof"),
        )
