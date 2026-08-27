"""H11_PROPULSIO: Spacecraft Propulsion Engine.

D07_space_astronomy - Universe

This module implements deterministic calculation of spacecraft propulsion
mechanics, including Tsiolkovsky rocket equation and thrust profiles.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_PROPULSIO"
G0 = 9.80665  # Standard gravity (m/s^2)

class PropulsioError(ValueError):
    """Domain-specific error for H11_PROPULSIO."""
    pass

class PropulsioStatus(Enum):
    IDLE = auto()
    NOMINAL = auto()
    MARGINAL = auto()
    FAILURE = auto()

@dataclass(frozen=True)
class PropulsioInput:
    initial_mass_kg: float
    final_mass_kg: float
    specific_impulse_s: float
    mass_flow_rate_kg_s: float
    ambient_pressure_pa: float = 0.0
    nozzle_exit_area_m2: float = 1.0
    exhaust_pressure_pa: float = 0.0

@dataclass(frozen=True)
class PropulsioOutput:
    agent_id: str
    status: str
    delta_v_m_s: float
    thrust_n: float
    burn_time_s: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class PropulsioAgent:
    """Analytical engine for spacecraft propulsion systems."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": PropulsioStatus.IDLE.name}

    def process(self, input_data: Optional[PropulsioInput] = None) -> PropulsioOutput:
        start_time = time.perf_counter()
        if input_data is None:
            raise PropulsioError("Input data required.")

        if input_data.initial_mass_kg <= input_data.final_mass_kg:
            raise PropulsioError("Initial mass must be greater than final mass.")
        if input_data.specific_impulse_s <= 0 or input_data.mass_flow_rate_kg_s <= 0:
            raise PropulsioError("Isp and mass flow rate must be strictly positive.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1

        # Tsiolkovsky Rocket Equation: delta_v = I_sp * g0 * ln(m0 / mf)
        effective_exhaust_velocity = input_data.specific_impulse_s * G0
        mass_ratio = input_data.initial_mass_kg / input_data.final_mass_kg
        delta_v = effective_exhaust_velocity * math.log(mass_ratio)

        # Thrust: F = m_dot * v_e + (p_e - p_a) * A_e
        momentum_thrust = input_data.mass_flow_rate_kg_s * effective_exhaust_velocity
        pressure_thrust = (input_data.exhaust_pressure_pa - input_data.ambient_pressure_pa) * input_data.nozzle_exit_area_m2
        total_thrust = momentum_thrust + pressure_thrust

        # Burn Time
        propellant_mass = input_data.initial_mass_kg - input_data.final_mass_kg
        burn_time = propellant_mass / input_data.mass_flow_rate_kg_s

        diagnostics = []
        if total_thrust <= 0:
            diag_status = PropulsioStatus.FAILURE.name
            diagnostics.append("Thrust is negative or zero. Check ambient pressure.")
        elif mass_ratio > 20:
            diag_status = PropulsioStatus.MARGINAL.name
            diagnostics.append("Structural mass fraction extremely low. Risk of structural failure.")
        else:
            diag_status = PropulsioStatus.NOMINAL.name
            diagnostics.append("Propulsion parameters nominal.")

        self.state["status"] = diag_status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "mass_ratio": round(mass_ratio, 4),
            "effective_exhaust_velocity": round(effective_exhaust_velocity, 2)
        }

        return PropulsioOutput(
            agent_id=AGENT_ID,
            status=diag_status,
            delta_v_m_s=round(delta_v, 2),
            thrust_n=round(total_thrust, 2),
            burn_time_s=round(burn_time, 2),
            execution_time_ms=round(elapsed_ms, 4),
            metrics=metrics,
            diagnostics=diagnostics
        )
