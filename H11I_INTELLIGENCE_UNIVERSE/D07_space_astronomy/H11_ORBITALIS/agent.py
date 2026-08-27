"""H11_ORBITALIS: Orbital Mechanics Engine.

D07_space_astronomy - Universe

This module implements the analytical execution engine for H11_ORBITALIS.
It solves Kepler's Third Law, Vis-viva equation, and orbital periods for 
spacecraft and celestial bodies.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_ORBITALIS"
G_CONST = 6.67430e-11

class OrbitalisError(ValueError):
    """Domain-specific error for H11_ORBITALIS."""
    pass

class OrbitalisStatus(Enum):
    IDLE = auto()
    CIRCULAR = auto()
    ELLIPTICAL = auto()
    ESCAPE = auto()
    FAILED = auto()

@dataclass(frozen=True)
class OrbitalisInput:
    central_body_mass_kg: float
    semi_major_axis_m: float
    eccentricity: float
    current_radius_m: float

@dataclass(frozen=True)
class OrbitalisOutput:
    agent_id: str
    status: str
    orbital_period_s: float
    current_velocity_m_s: float
    periapsis_m: float
    apoapsis_m: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class OrbitalisAgent:
    """Analytical engine for orbital mechanics calculations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": OrbitalisStatus.IDLE.name
        }

    def process(self, input_data: Optional[OrbitalisInput] = None) -> OrbitalisOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise OrbitalisError("OrbitalisInput data must be provided.")
        if input_data.central_body_mass_kg <= 0:
            raise OrbitalisError("Central body mass must be positive.")
        if input_data.semi_major_axis_m <= 0:
            raise OrbitalisError("Semi-major axis must be positive.")
        if input_data.eccentricity < 0:
            raise OrbitalisError("Eccentricity cannot be negative.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        mu = G_CONST * input_data.central_body_mass_kg
        a = input_data.semi_major_axis_m
        e = input_data.eccentricity
        r = input_data.current_radius_m

        # Kepler's Third Law: T = 2 * pi * sqrt(a^3 / mu)
        period = 2.0 * math.pi * math.sqrt((a ** 3) / mu)

        # Vis-viva Equation: v^2 = mu * (2/r - 1/a)
        # Note: if e >= 1, orbit is parabolic/hyperbolic, and 'a' might be treated differently,
        # but for this engine we assume closed orbits unless handled specifically.
        velocity_sq = mu * ((2.0 / r) - (1.0 / a))
        if velocity_sq < 0:
            raise OrbitalisError("Current radius is impossible for this orbit geometry.")
        velocity = math.sqrt(velocity_sq)

        # Periapsis and Apoapsis
        periapsis = a * (1.0 - e)
        if e < 1.0:
            apoapsis = a * (1.0 + e)
        else:
            apoapsis = float('inf')

        if e >= 1.0:
            status = OrbitalisStatus.ESCAPE.name
            diagnostics.append("Orbit is on an escape trajectory (parabolic/hyperbolic).")
        elif e > 0.05:
            status = OrbitalisStatus.ELLIPTICAL.name
            diagnostics.append("Orbit is elliptical.")
        else:
            status = OrbitalisStatus.CIRCULAR.name
            diagnostics.append("Orbit is near-circular.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "specific_orbital_energy": (velocity**2)/2.0 - (mu/r),
            "mean_motion_rad_s": 2.0 * math.pi / period if period > 0 else 0
        }

        return OrbitalisOutput(
            agent_id=AGENT_ID,
            status=status,
            orbital_period_s=round(period, 2),
            current_velocity_m_s=round(velocity, 2),
            periapsis_m=round(periapsis, 2),
            apoapsis_m=round(apoapsis, 2),
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
