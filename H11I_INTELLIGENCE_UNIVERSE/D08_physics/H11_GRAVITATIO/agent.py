"""H11_GRAVITATIO: Gravitational Physics Engine.

D08_physics - Universe

This module implements the analytical execution engine for H11_GRAVITATIO.
It resolves Newton's Law of Universal Gravitation, escape velocities,
and gravitational potential energy.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_GRAVITATIO"
G_CONST = 6.67430e-11

class GravitatioError(ValueError):
    """Domain-specific error for H11_GRAVITATIO."""
    pass

class GravitatioStatus(Enum):
    IDLE = auto()
    WEAK_FIELD = auto()
    STRONG_FIELD = auto()
    BLACK_HOLE = auto()
    FAILED = auto()

@dataclass(frozen=True)
class GravitatioInput:
    mass_1_kg: float
    mass_2_kg: float
    distance_m: float
    radius_body_1_m: float

@dataclass(frozen=True)
class GravitatioOutput:
    agent_id: str
    status: str
    gravitational_force_n: float
    escape_velocity_1_m_s: float
    potential_energy_j: float
    surface_gravity_1_m_s2: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class GravitatioAgent:
    """Analytical engine for classical and extreme gravitational metrics."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": GravitatioStatus.IDLE.name
        }

    def process(self, input_data: Optional[GravitatioInput] = None) -> GravitatioOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise GravitatioError("GravitatioInput data must be provided.")
        if input_data.distance_m <= 0:
            raise GravitatioError("Distance must be greater than zero.")
        if input_data.mass_1_kg < 0 or input_data.mass_2_kg < 0:
            raise GravitatioError("Masses cannot be negative.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Universal Gravitation: F = G * m1 * m2 / r^2
        force = G_CONST * input_data.mass_1_kg * input_data.mass_2_kg / (input_data.distance_m ** 2)
        
        # Gravitational Potential Energy: U = -G * m1 * m2 / r
        potential = -G_CONST * input_data.mass_1_kg * input_data.mass_2_kg / input_data.distance_m
        
        # Escape Velocity from body 1: v_e = sqrt(2 * G * M / R)
        if input_data.radius_body_1_m > 0:
            escape_vel = math.sqrt(2.0 * G_CONST * input_data.mass_1_kg / input_data.radius_body_1_m)
            surface_gravity = G_CONST * input_data.mass_1_kg / (input_data.radius_body_1_m ** 2)
        else:
            escape_vel = float('inf')
            surface_gravity = float('inf')

        c = 299792458.0
        if escape_vel >= c:
            status = GravitatioStatus.BLACK_HOLE.name
            diagnostics.append("Body 1 constitutes a Black Hole; escape velocity exceeds c.")
        elif surface_gravity > 100.0:
            status = GravitatioStatus.STRONG_FIELD.name
            diagnostics.append("Strong gravitational field detected.")
        else:
            status = GravitatioStatus.WEAK_FIELD.name
            diagnostics.append("Weak field gravity. Newtonian approximations hold firmly.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "schwarzschild_radius_1_m": 2.0 * G_CONST * input_data.mass_1_kg / (c**2)
        }

        return GravitatioOutput(
            agent_id=AGENT_ID,
            status=status,
            gravitational_force_n=round(force, 4),
            escape_velocity_1_m_s=round(escape_vel, 2) if escape_vel != float('inf') else -1.0,
            potential_energy_j=round(potential, 4),
            surface_gravity_1_m_s2=round(surface_gravity, 4) if surface_gravity != float('inf') else -1.0,
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
