"""H11_ELECTROMAGNETICA: Electromagnetism & Field Theory Engine.

D08_physics - Universe

This module implements the analytical execution engine for H11_ELECTROMAGNETICA.
It calculates electrostatic forces using Coulomb's Law and determines
electric field strength and potentials.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_ELECTROMAGNETICA"

K_E = 8.9875517923e9  # Coulomb's constant N m^2 / C^2
EPSILON_0 = 8.8541878128e-12 # Vacuum permittivity

class ElectromagneticaError(ValueError):
    """Domain-specific error for H11_ELECTROMAGNETICA."""
    pass

class ElectromagneticaStatus(Enum):
    IDLE = auto()
    ATTRACTIVE = auto()
    REPULSIVE = auto()
    NEUTRAL = auto()
    FAILED = auto()

@dataclass(frozen=True)
class ElectromagneticaInput:
    charge_1_c: float
    charge_2_c: float
    distance_m: float
    medium_dielectric_constant: float = 1.0

@dataclass(frozen=True)
class ElectromagneticaOutput:
    agent_id: str
    status: str
    electrostatic_force_n: float
    electric_field_1_at_2_v_m: float
    electric_potential_energy_j: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class ElectromagneticaAgent:
    """Analytical engine for classical electrostatics and field vectors."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": ElectromagneticaStatus.IDLE.name
        }

    def process(self, input_data: Optional[ElectromagneticaInput] = None) -> ElectromagneticaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise ElectromagneticaError("ElectromagneticaInput data must be provided.")
        if input_data.distance_m <= 0:
            raise ElectromagneticaError("Distance must be greater than zero.")
        if input_data.medium_dielectric_constant < 1.0:
            raise ElectromagneticaError("Dielectric constant cannot be less than 1.0 (vacuum).")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        q1 = input_data.charge_1_c
        q2 = input_data.charge_2_c
        r = input_data.distance_m
        k = K_E / input_data.medium_dielectric_constant

        # Coulomb's Law: F = k * |q1*q2| / r^2
        force_magnitude = k * abs(q1 * q2) / (r ** 2)
        
        # Electric Field from q1 at distance r: E = k * |q1| / r^2
        e_field_1 = k * abs(q1) / (r ** 2)
        
        # Electric Potential Energy: U = k * q1 * q2 / r
        potential_energy = k * q1 * q2 / r

        if q1 == 0 or q2 == 0:
            status = ElectromagneticaStatus.NEUTRAL.name
            diagnostics.append("One or both charges are neutral. No electrostatic force.")
        elif q1 * q2 < 0:
            status = ElectromagneticaStatus.ATTRACTIVE.name
            diagnostics.append("Charges are opposite. Force is attractive.")
        else:
            status = ElectromagneticaStatus.REPULSIVE.name
            diagnostics.append("Charges are alike. Force is repulsive.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "permittivity_medium": EPSILON_0 * input_data.medium_dielectric_constant,
            "coulomb_constant_eff": k
        }

        return ElectromagneticaOutput(
            agent_id=AGENT_ID,
            status=status,
            electrostatic_force_n=force_magnitude,
            electric_field_1_at_2_v_m=e_field_1,
            electric_potential_energy_j=potential_energy,
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
