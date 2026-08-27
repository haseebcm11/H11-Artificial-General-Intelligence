"""H11_SEISMOLOGIA: Seismology & Earthquakes Engine.

D06_earth_environment - Universe

This module implements deterministic calculation of earthquake magnitudes,
seismic moment, and energy release.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_SEISMOLOGIA"

class SeismologiaError(ValueError):
    """Domain-specific error for H11_SEISMOLOGIA."""
    pass

class SeismologiaStatus(Enum):
    IDLE = auto()
    NORMAL = auto()
    WARNING = auto()
    CRITICAL = auto()

@dataclass(frozen=True)
class SeismologiaInput:
    amplitude_mm: float      # Maximum amplitude of seismic waves
    distance_km: float       # Distance to epicenter
    fault_area_m2: float     # Fault rupture area
    slip_m: float            # Average slip along fault
    shear_modulus_pa: float = 3.0e10  # Rock shear modulus (default ~30 GPa)

@dataclass(frozen=True)
class SeismologiaOutput:
    agent_id: str
    status: str
    richter_magnitude: float
    seismic_moment_nm: float
    moment_magnitude: float
    energy_joules: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class SeismologiaAgent:
    """Analytical engine for Earthquakes & Seismology."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": SeismologiaStatus.IDLE.name}

    def process(self, input_data: Optional[SeismologiaInput] = None) -> SeismologiaOutput:
        start_time = time.perf_counter()
        if input_data is None:
            raise SeismologiaError("Input data required.")

        if input_data.amplitude_mm <= 0 or input_data.distance_km <= 0:
            raise SeismologiaError("Amplitude and distance must be positive.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1

        # Richter Magnitude: M_L = log10(A) + 3*log10(8 * delta_t) - 2.92
        # Simplified empirical: M_L = log10(A) + 1.6 * log10(D) - 0.15
        richter_mag = math.log10(input_data.amplitude_mm) + 1.6 * math.log10(input_data.distance_km) - 0.15

        # Seismic Moment: M_0 = mu * A * D
        m0 = input_data.shear_modulus_pa * input_data.fault_area_m2 * input_data.slip_m

        # Moment Magnitude: M_w = 2/3 * log10(M_0) - 6.0 (for M_0 in N*m)
        moment_mag = (2.0 / 3.0) * math.log10(m0) - 6.0 if m0 > 0 else 0.0

        # Energy Release (Gutenberg-Richter): log10(E) = 4.8 + 1.5 * M_w
        energy = math.pow(10, 4.8 + 1.5 * moment_mag)

        diagnostics = []
        if moment_mag > 7.0:
            diag_status = SeismologiaStatus.CRITICAL.name
            diagnostics.append("Major earthquake detected. High tsunami risk if oceanic.")
        elif moment_mag > 5.0:
            diag_status = SeismologiaStatus.WARNING.name
            diagnostics.append("Moderate earthquake. Potential structural damage.")
        else:
            diag_status = SeismologiaStatus.NORMAL.name
            diagnostics.append("Minor seismic activity. Background stress relief.")

        self.state["status"] = diag_status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "richter_magnitude": round(richter_mag, 2),
            "moment_magnitude": round(moment_mag, 2)
        }

        return SeismologiaOutput(
            agent_id=AGENT_ID,
            status=diag_status,
            richter_magnitude=round(richter_mag, 2),
            seismic_moment_nm=m0,
            moment_magnitude=round(moment_mag, 2),
            energy_joules=energy,
            execution_time_ms=round(elapsed_ms, 4),
            metrics=metrics,
            diagnostics=diagnostics
        )
