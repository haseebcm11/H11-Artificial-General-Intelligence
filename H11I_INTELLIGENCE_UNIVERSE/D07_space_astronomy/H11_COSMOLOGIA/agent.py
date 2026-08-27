"""H11_COSMOLOGIA: Cosmology and Universe Expansion Engine.

D07_space_astronomy - Universe

This module implements the analytical execution engine for H11_COSMOLOGIA.
It evaluates large scale structure kinematics, Hubble's Law (v = H0 * d),
and cosmological redshift equations.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_COSMOLOGIA"
SPEED_OF_LIGHT_KM_S = 299792.458

class CosmologiaError(ValueError):
    """Domain-specific error for H11_COSMOLOGIA."""
    pass

class CosmologiaStatus(Enum):
    IDLE = auto()
    NOMINAL = auto()
    RELATIVISTIC = auto()
    UNOBSERVABLE = auto()
    FAILED = auto()

@dataclass(frozen=True)
class CosmologiaInput:
    distance_mpc: float
    hubble_constant: float = 70.0  # km/s/Mpc
    omega_matter: float = 0.3
    omega_lambda: float = 0.7

@dataclass(frozen=True)
class CosmologiaOutput:
    agent_id: str
    status: str
    recession_velocity_km_s: float
    redshift_z: float
    lookback_time_gyr: float
    critical_density_kg_m3: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class CosmologiaAgent:
    """Analytical engine for modeling cosmological expansion and distances."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": CosmologiaStatus.IDLE.name
        }

    def process(self, input_data: Optional[CosmologiaInput] = None) -> CosmologiaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise CosmologiaError("CosmologiaInput data must be provided.")
        if input_data.distance_mpc < 0:
            raise CosmologiaError("Distance cannot be negative.")
        if input_data.hubble_constant <= 0:
            raise CosmologiaError("Hubble constant must be strictly positive.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Hubble's Law: v = H0 * d
        velocity = input_data.hubble_constant * input_data.distance_mpc
        
        # Redshift (z): Relativistic doppler effect 1+z = sqrt((1+v/c)/(1-v/c))
        # Valid if v < c. If v >= c, we use cosmological redshift strictly from scale factor
        if velocity < SPEED_OF_LIGHT_KM_S:
            beta = velocity / SPEED_OF_LIGHT_KM_S
            redshift = math.sqrt((1 + beta) / (1 - beta)) - 1.0
        else:
            # Superluminal recession (common in high-z cosmology due to metric expansion)
            # z ~ v/c approximation breaks down; purely a scale factor relation. 
            # We approximate linearly for the sake of the engine template.
            redshift = velocity / SPEED_OF_LIGHT_KM_S
        
        # Critical density: rho_c = 3 H0^2 / (8 pi G)
        # H0 in SI units (s^-1)
        h0_si = input_data.hubble_constant * 1000 / (3.086e22)
        G = 6.67430e-11
        rho_c = (3 * h0_si**2) / (8 * math.pi * G)
        
        # Simplified lookback time linear approximation (d = c * t)
        lookback_time_s = (input_data.distance_mpc * 3.086e22) / SPEED_OF_LIGHT_KM_S
        lookback_gyr = lookback_time_s / (365.25 * 24 * 3600) / 1e9

        if redshift > 10:
            status = CosmologiaStatus.UNOBSERVABLE.name
            diagnostics.append("Target is highly redshifted, potentially beyond observable horizon.")
        elif velocity > SPEED_OF_LIGHT_KM_S * 0.1:
            status = CosmologiaStatus.RELATIVISTIC.name
            diagnostics.append("Recession velocity is highly relativistic.")
        else:
            status = CosmologiaStatus.NOMINAL.name
            diagnostics.append("Cosmological parameters calculated nominally.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "beta_fraction": velocity / SPEED_OF_LIGHT_KM_S,
            "omega_total": input_data.omega_matter + input_data.omega_lambda
        }

        return CosmologiaOutput(
            agent_id=AGENT_ID,
            status=status,
            recession_velocity_km_s=round(velocity, 2),
            redshift_z=round(redshift, 6),
            lookback_time_gyr=round(lookback_gyr, 4),
            critical_density_kg_m3=rho_c,
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
