"""Contracts: CaseEnvelope, Modality, RiskClass, AuthorizationContext."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import time
from typing import Any, List, Optional
import uuid


class Modality(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    CODE = "CODE"
    EMBEDDING = "EMBEDDING"
    STRUCTURED = "STRUCTURED"


class RiskClass(str, Enum):
    R0_INFORMATIONAL = "R0_INFORMATIONAL"
    R1_LOW = "R1_LOW"
    R2_MODERATE = "R2_MODERATE"
    R2_SIGNIFICANT = "R2_SIGNIFICANT"
    R3_CRITICAL = "R3_CRITICAL"


@dataclass(frozen=True)
class AuthorizationContext:
    principal_id: str = "SYSTEM_USER"
    roles: List[str] = field(default_factory=lambda: ["STANDARD_USER"])
    clearance_level: int = 1
    session_id: str = field(default_factory=lambda: f"SESS-{uuid.uuid4().hex[:8]}")
    timestamp: float = field(default_factory=time.time)


@dataclass
class CaseEnvelope:
    """02 — CaseEnvelope: The schema-checked foundation of the H11 runtime."""
    case_id: str = field(default_factory=lambda: f"CASE-{uuid.uuid4().hex[:8].upper()}")
    principal_id: str = "SYSTEM_USER"
    input_data: Any = None
    modalities: List[Modality] = field(default_factory=lambda: [Modality.TEXT])
    objective: str = ""
    constraints: List[str] = field(default_factory=list)
    requested_capabilities: List[str] = field(default_factory=list)
    risk_class: RiskClass = RiskClass.R1_LOW
    auth_context: AuthorizationContext = field(default_factory=AuthorizationContext)
    state: str = "CREATED"
    created_at: float = field(default_factory=time.time)
