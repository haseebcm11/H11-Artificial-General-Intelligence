"""priority: Exponential Aging Priority.

L18_orchestration_control - Substrate

This module implements the analytical execution engine for priority.
It provides mathematically rigorous domain calculations.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "priority"

class PriorityError(ValueError):
    pass

class PriorityStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()

@dataclass(frozen=True)
class PriorityInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    base_pri: float=5.0
    wait_time: float=10.0
    aging_rate: float=0.5

@dataclass(frozen=True)
class PriorityOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, Any]

class PriorityAgent:
    """Analytical engine for Exponential Aging Priority."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": PriorityStatus.IDLE.name}

    def process(self, input_data: Optional[PriorityInput] = None) -> PriorityOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = PriorityInput()

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1

        # Domain specific computation
        ep = input_data.base_pri + input_data.wait_time * input_data.aging_rate
        computed = ep
        efficiency = min(1.0, ep / 20.0)

        if efficiency > 0.8:
            diag_status = PriorityStatus.OPTIMAL.name
        elif efficiency > 0.4:
            diag_status = PriorityStatus.ACTIVE.name
        else:
            diag_status = PriorityStatus.DEGRADED.name

        self.state["status"] = diag_status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "computed_value": round(computed, 6),
            "efficiency": round(efficiency, 6),
            "execution_ms": round(elapsed_ms, 4)
        }

        return PriorityOutput(
            agent_id=AGENT_ID,
            status=diag_status,
            efficiency_score=round(efficiency, 6),
            computed_value=round(computed, 6),
            execution_time_ms=round(elapsed_ms, 4),
            metrics=metrics
        )
