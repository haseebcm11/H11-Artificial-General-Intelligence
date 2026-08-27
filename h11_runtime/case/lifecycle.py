"""Case lifecycle manager."""
from __future__ import annotations

from typing import Any, List, Optional

from ..contracts import CaseEnvelope, RiskClass
from .case import Case


class CaseLifecycleManager:
    """Coordinates state transitions and invariants across case lifecycles."""

    def create_case(
        self,
        objective: str,
        input_data: Any,
        requested_capabilities: Optional[List[str]] = None,
        risk_class: RiskClass = RiskClass.R1_LOW,
    ) -> Case:
        env = CaseEnvelope(
            objective=objective,
            input_data=input_data,
            requested_capabilities=requested_capabilities or [],
            risk_class=risk_class,
        )
        return Case(envelope=env)
