"""H11_ASTROPHYSICA: Stellar Astrophysics Engine.

D07_space_astronomy - Universe

This module implements the analytical execution engine for H11_ASTROPHYSICA.
It models stellar luminosity using Stefan-Boltzmann law and estimates
main-sequence lifespan.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_ASTROPHYSICA"

SIGMA_SB = 5.670374419e-8  # W/(m^2 K^4)
L_SUN = 3.828e26           # Watts
M_SUN = 1.9884e30          # kg

class AstrophysicaError(ValueError):
    """Domain-specific error for H11_ASTROPHYSICA."""
    pass

class AstrophysicaStatus(Enum):
    IDLE = auto()
    MAIN_SEQUENCE = auto()
    GIANT = auto()
    REMNANT = auto()
    FAILED = auto()

@dataclass(frozen=True)
class AstrophysicaInput:
    stellar_mass_kg: float
    effective_temp_k: float
    radius_m: float
    is_main_sequence: bool = True

@dataclass(frozen=True)
class AstrophysicaOutput:
    agent_id: str
    status: str
    luminosity_watts: float
    luminosity_solar: float
    peak_wavelength_nm: float
    estimated_lifespan_gyr: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class AstrophysicaAgent:
    """Analytical engine for modeling stellar radiation and lifecycles."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": AstrophysicaStatus.IDLE.name
        }

    def process(self, input_data: Optional[AstrophysicaInput] = None) -> AstrophysicaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise AstrophysicaError("AstrophysicaInput data must be provided.")
        if input_data.stellar_mass_kg <= 0 or input_data.effective_temp_k <= 0 or input_data.radius_m <= 0:
            raise AstrophysicaError("Mass, temperature, and radius must be positive.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Stefan-Boltzmann Law: L = 4 * pi * R^2 * sigma * T^4
        r = input_data.radius_m
        t = input_data.effective_temp_k
        luminosity = 4.0 * math.pi * (r**2) * SIGMA_SB * (t**4)
        l_solar = luminosity / L_SUN
        
        m_solar = input_data.stellar_mass_kg / M_SUN

        # Wien's Displacement Law: lambda_max = b / T
        b_wien = 2.897771955e-3 # m*K
        peak_wave_m = b_wien / t
        peak_wave_nm = peak_wave_m * 1e9

        # Main-sequence lifespan estimation: t ~ 10^10 * (M/M_sun)^-2.5 years
        if input_data.is_main_sequence:
            lifespan_yrs = 1e10 * (m_solar ** -2.5)
            lifespan_gyr = lifespan_yrs / 1e9
            status = AstrophysicaStatus.MAIN_SEQUENCE.name
            diagnostics.append("Star is burning hydrogen on the main sequence.")
        else:
            lifespan_gyr = 0.0
            if r > 10 * 696340000: # 10 solar radii
                status = AstrophysicaStatus.GIANT.name
                diagnostics.append("Star is in giant/supergiant phase.")
            else:
                status = AstrophysicaStatus.REMNANT.name
                diagnostics.append("Star is a compact remnant (White Dwarf, Neutron Star).")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "mass_solar": m_solar,
            "surface_flux_w_m2": SIGMA_SB * (t**4)
        }

        return AstrophysicaOutput(
            agent_id=AGENT_ID,
            status=status,
            luminosity_watts=luminosity,
            luminosity_solar=l_solar,
            peak_wavelength_nm=round(peak_wave_nm, 2),
            estimated_lifespan_gyr=round(lifespan_gyr, 4),
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
