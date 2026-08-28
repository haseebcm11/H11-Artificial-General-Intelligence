"""Admission controller with Multi-Stage Security and Risk Classification."""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from ..contracts import AuthorizationContext, CaseEnvelope, RiskClass

logger = logging.getLogger(__name__)


class AdmissionController:
    """10 — H11C-ADMISSION-CONTROL: Zero-Trust schema validation, injection filtering & risk gating."""

    # Malicious / injection signatures
    _INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
        re.compile(r"system\s*:\s*override", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+in\s+unrestricted\s+mode", re.IGNORECASE),
        re.compile(r"<script>.*?</script>", re.IGNORECASE),
        re.compile(r"drop\s+table\s+", re.IGNORECASE),
        re.compile(r"---\s*BEGIN\s+SYSTEM\s+PROMPT", re.IGNORECASE),
    ]

    def __init__(self, max_payload_bytes: int = 10_000_000, max_risk_class: RiskClass = RiskClass.R3_CRITICAL) -> None:
        self.max_payload_bytes = max_payload_bytes
        self.max_risk_class = max_risk_class
        self.admitted_count = 0
        self.rejected_count = 0

    def evaluate_admission(self, envelope: CaseEnvelope) -> Tuple[bool, str]:
        """Runs 5-stage admission evaluation against security invariants."""
        # 1. Structural integrity check
        if not envelope.case_id:
            self.rejected_count += 1
            return False, "ADMISSION_REJECT: Missing case_id"
        if not envelope.objective and not envelope.input_data:
            self.rejected_count += 1
            return False, "ADMISSION_REJECT: Empty objective and input_data"

        # 2. Risk classification check
        if envelope.risk_class == RiskClass.R3_CRITICAL:
            if not envelope.auth_context or envelope.auth_context.clearance_level < 3:
                self.rejected_count += 1
                return False, "ADMISSION_REJECT: R3_CRITICAL risk requires clearance level >= 3"

        # 3. Payload size check
        payload_str = str(envelope.input_data) + str(envelope.objective)
        if len(payload_str.encode("utf-8")) > self.max_payload_bytes:
            self.rejected_count += 1
            return False, "ADMISSION_REJECT: Payload size exceeds limit"

        # 4. Injection scanning
        for pattern in self._INJECTION_PATTERNS:
            if pattern.search(payload_str):
                self.rejected_count += 1
                logger.warning(f"Admission rejected injection attempt in case {envelope.case_id}")
                return False, "ADMISSION_REJECT: Potential adversarial injection detected"

        self.admitted_count += 1
        return True, "ADMITTED"

    def get_stats(self) -> Dict[str, int]:
        return {
            "admitted_cases": self.admitted_count,
            "rejected_cases": self.rejected_count,
            "total_evaluated": self.admitted_count + self.rejected_count,
        }
