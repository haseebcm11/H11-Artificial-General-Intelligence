"""Admission controller."""
from __future__ import annotations

from typing import Tuple

from ..contracts import CaseEnvelope


class AdmissionController:
    """10 — H11C-ADMISSION-CONTROL: Schema validation and admission filtering."""

    def evaluate_admission(self, envelope: CaseEnvelope) -> Tuple[bool, str]:
        if not envelope.case_id or not envelope.objective:
            return False, "ADMISSION_REJECT: Missing case_id or objective"
        return True, "ADMITTED"
