"""Contracts: ActionProposal."""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Dict, Optional
import uuid

from .envelope import RiskClass


@dataclass
class ActionProposal:
    """Action proposal awaiting alignment evaluation and licensing."""
    proposal_id: str = field(default_factory=lambda: f"ACT-PROP-{uuid.uuid4().hex[:6].upper()}")
    originating_agent: str = ""
    action_type: str = "TOOL_CALL"
    target_resource: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    payload: Dict[str, Any] = field(default_factory=dict)
    risk_class: RiskClass = RiskClass.R1_LOW
    rationale: str = ""
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if self.payload and not self.parameters:
            self.parameters = self.payload
        elif self.parameters and not self.payload:
            self.payload = self.parameters
