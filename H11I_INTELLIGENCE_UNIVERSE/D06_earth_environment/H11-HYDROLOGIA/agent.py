"""H11_HYDROLOGIA: Hydrology and Groundwater Processing Engine.

D06_earth_environment - Universe

This module implements the analytical execution engine for H11_HYDROLOGIA.
It calculates steady-state groundwater flow using Darcy's Law and assesses
aquifer transmissivity and hydraulic gradients.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_HYDROLOGIA"

class HydrologiaError(ValueError):
    """Domain-specific error for H11_HYDROLOGIA."""
    pass

class HydrologiaStatus(Enum):
    IDLE = auto()
    STEADY = auto()
    DEPLETING = auto()
    FLOODING = auto()
    FAILED = auto()

@dataclass(frozen=True)
class HydrologiaInput:
    hydraulic_conductivity_k: float  # m/s
    cross_sectional_area_a: float    # m^2
    head_change_dh: float            # m
    flow_length_dl: float            # m
    aquifer_thickness_b: float       # m
    recharge_rate_r: float = 0.0     # m/s

@dataclass(frozen=True)
class HydrologiaOutput:
    agent_id: str
    status: str
    discharge_q: float
    darcy_velocity_v: float
    transmissivity_t: float
    hydraulic_gradient_i: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class HydrologiaAgent:
    """Analytical engine for Hydrology and Groundwater flow."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": HydrologiaStatus.IDLE.name
        }

    def process(self, input_data: Optional[HydrologiaInput] = None) -> HydrologiaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise HydrologiaError("HydrologiaInput data must be provided.")
        if input_data.flow_length_dl <= 0:
            raise HydrologiaError("Flow length (dl) must be greater than zero to prevent division by zero.")
        if input_data.hydraulic_conductivity_k < 0:
            raise HydrologiaError("Hydraulic conductivity (K) cannot be negative.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Hydraulic Gradient (i = -dh/dl)
        gradient_i = - (input_data.head_change_dh / input_data.flow_length_dl)
        
        # Darcy's Law: Q = -K * A * (dh/dl) -> Q = K * A * i
        discharge_q = input_data.hydraulic_conductivity_k * input_data.cross_sectional_area_a * gradient_i
        
        # Darcy Velocity: v = Q / A = K * i
        darcy_v = input_data.hydraulic_conductivity_k * gradient_i
        
        # Transmissivity: T = K * b
        transmissivity_t = input_data.hydraulic_conductivity_k * input_data.aquifer_thickness_b

        # Net balance with recharge
        net_recharge_flux = input_data.recharge_rate_r * input_data.cross_sectional_area_a
        balance = net_recharge_flux - discharge_q

        if balance < -1e-3:
            status = HydrologiaStatus.DEPLETING.name
            diagnostics.append("Aquifer is depleting. Discharge exceeds recharge.")
        elif balance > 1e-3:
            status = HydrologiaStatus.FLOODING.name
            diagnostics.append("Aquifer is accumulating storage. High water table risk.")
        else:
            status = HydrologiaStatus.STEADY.name
            diagnostics.append("Groundwater flow is in steady state.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "net_flux_balance": balance,
            "recharge_flux": net_recharge_flux
        }

        return HydrologiaOutput(
            agent_id=AGENT_ID,
            status=status,
            discharge_q=round(discharge_q, 6),
            darcy_velocity_v=round(darcy_v, 8),
            transmissivity_t=round(transmissivity_t, 6),
            hydraulic_gradient_i=round(gradient_i, 6),
            execution_time_ms=round(elapsed_ms, 4),
            metrics=metrics,
            diagnostics=diagnostics
        )

    def health_check(self) -> Dict[str, Any]:
        return {
            "agent_id": AGENT_ID,
            "status": self.state.get("status", "UNKNOWN"),
            "evaluations_count": self.state.get("evaluations_count", 0)
        }
