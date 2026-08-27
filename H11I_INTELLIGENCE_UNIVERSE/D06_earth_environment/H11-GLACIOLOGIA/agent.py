"""H11_GLACIOLOGIA: Glaciology and Ice Deformation Engine.

D06_earth_environment - Universe

This module implements the analytical execution engine for H11_GLACIOLOGIA.
It assesses glacier flow dynamics using Glen's Flow Law and computes
basal shear stress.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_GLACIOLOGIA"

RHO_ICE = 917.0      # kg/m^3
G = 9.80665          # m/s^2

class GlaciologiaError(ValueError):
    """Domain-specific error for H11_GLACIOLOGIA."""
    pass

class GlaciologiaStatus(Enum):
    IDLE = auto()
    STAGNANT = auto()
    FLOWING = auto()
    SURGING = auto()
    FAILED = auto()

@dataclass(frozen=True)
class GlaciologiaInput:
    ice_thickness_m: float
    surface_slope_deg: float
    ice_temperature_k: float = 263.15
    glen_n: float = 3.0
    basal_sliding_velocity_m_yr: float = 0.0

@dataclass(frozen=True)
class GlaciologiaOutput:
    agent_id: str
    status: str
    basal_shear_stress_pa: float
    deformation_velocity_m_yr: float
    total_surface_velocity_m_yr: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class GlaciologiaAgent:
    """Analytical engine for modeling glacier flow and ice rheology."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": GlaciologiaStatus.IDLE.name
        }

    def process(self, input_data: Optional[GlaciologiaInput] = None) -> GlaciologiaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise GlaciologiaError("GlaciologiaInput data must be provided.")
        if input_data.ice_thickness_m <= 0:
            raise GlaciologiaError("Ice thickness must be positive.")
        if not (0 <= input_data.surface_slope_deg <= 90):
            raise GlaciologiaError("Slope must be between 0 and 90 degrees.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Convert slope to radians
        alpha_rad = math.radians(input_data.surface_slope_deg)
        
        # Basal Shear Stress: tau_b = rho * g * h * sin(alpha)
        tau_b = RHO_ICE * G * input_data.ice_thickness_m * math.sin(alpha_rad)
        
        # Temperature dependent creep parameter A (simplified Arrhenius relation)
        # Standard value A ~ 2.4e-24 Pa^-3 s^-1 at -5 C (268 K)
        # For simplicity, using a static A for standard cold ice
        A_creep = 2.4e-24  
        seconds_in_year = 31536000.0

        # Glen's Flow Law integrated for surface deformation velocity: 
        # Ud = (2 * A / (n + 1)) * (tau_b)^n * h
        n = input_data.glen_n
        u_d_s = (2.0 * A_creep / (n + 1)) * (tau_b ** n) * input_data.ice_thickness_m
        u_d_yr = u_d_s * seconds_in_year

        # Total Velocity = Deformation + Basal Sliding
        u_total = u_d_yr + input_data.basal_sliding_velocity_m_yr

        if u_total > 100.0:
            status = GlaciologiaStatus.SURGING.name
            diagnostics.append("High flow velocity. Glacier may be surging.")
        elif u_total > 1.0:
            status = GlaciologiaStatus.FLOWING.name
            diagnostics.append("Normal viscous flow dynamics observed.")
        else:
            status = GlaciologiaStatus.STAGNANT.name
            diagnostics.append("Ice mass is effectively stagnant.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "flow_law_exponent": n,
            "creep_parameter_a": A_creep
        }

        return GlaciologiaOutput(
            agent_id=AGENT_ID,
            status=status,
            basal_shear_stress_pa=round(tau_b, 2),
            deformation_velocity_m_yr=round(u_d_yr, 4),
            total_surface_velocity_m_yr=round(u_total, 4),
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
