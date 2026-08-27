"""resource: Knapsack DP Resource Allocation.

L18_orchestration_control - Substrate

This module implements the analytical execution engine for resource.
It provides mathematically rigorous domain calculations.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "resource"

class ResourceError(ValueError):
    pass

class ResourceStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()

@dataclass(frozen=True)
class ResourceInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    cap: int=10
    weights: str="2,3,4"
    vals: str="3,4,5"

@dataclass(frozen=True)
class ResourceOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, Any]

class ResourceAgent:
    """Analytical engine for Knapsack DP Resource Allocation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": ResourceStatus.IDLE.name}

    def process(self, input_data: Optional[ResourceInput] = None) -> ResourceOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = ResourceInput()

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1

        # Domain specific computation
        w = [int(x) for x in input_data.weights.split(",")]
        v = [float(x) for x in input_data.vals.split(",")]
        dp = [0.0] * (input_data.cap + 1)
        for i in range(len(w)):
            for j in range(input_data.cap, w[i]-1, -1):
                dp[j] = max(dp[j], dp[j-w[i]] + v[i])
        computed = dp[input_data.cap]
        efficiency = min(1.0, computed / 20.0)

        if efficiency > 0.8:
            diag_status = ResourceStatus.OPTIMAL.name
        elif efficiency > 0.4:
            diag_status = ResourceStatus.ACTIVE.name
        else:
            diag_status = ResourceStatus.DEGRADED.name

        self.state["status"] = diag_status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "computed_value": round(computed, 6),
            "efficiency": round(efficiency, 6),
            "execution_ms": round(elapsed_ms, 4)
        }

        return ResourceOutput(
            agent_id=AGENT_ID,
            status=diag_status,
            efficiency_score=round(efficiency, 6),
            computed_value=round(computed, 6),
            execution_time_ms=round(elapsed_ms, 4),
            metrics=metrics
        )
