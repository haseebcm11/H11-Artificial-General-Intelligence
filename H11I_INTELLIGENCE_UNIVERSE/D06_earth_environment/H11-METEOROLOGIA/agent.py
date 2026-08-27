"""H11_METEOROLOGIA: Meteorology and Atmospheric Physics Engine.

D06_earth_environment - Universe

This module implements the analytical execution engine for H11_METEOROLOGIA.
It calculates atmospheric lapse rates, barometric pressure formulas, and
air density scaling.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_METEOROLOGIA"

G = 9.80665            # m/s^2
M = 0.0289644          # Molar mass of Earth's air (kg/mol)
R = 8.3144598          # Universal gas constant (J/(mol*K))
L = 0.0065             # Temperature lapse rate (K/m)

class MeteorologiaError(ValueError):
    """Domain-specific error for H11_METEOROLOGIA."""
    pass

class MeteorologiaStatus(Enum):
    IDLE = auto()
    STABLE = auto()
    UNSTABLE = auto()
    FAILED = auto()

@dataclass(frozen=True)
class MeteorologiaInput:
    altitude_m: float
    base_pressure_pa: float = 101325.0
    base_temp_k: float = 288.15
    humidity_percent: float = 0.0

@dataclass(frozen=True)
class MeteorologiaOutput:
    agent_id: str
    status: str
    temperature_k: float
    pressure_pa: float
    air_density_kg_m3: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class MeteorologiaAgent:
    """Analytical engine for modeling atmospheric state variables."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": MeteorologiaStatus.IDLE.name
        }

    def process(self, input_data: Optional[MeteorologiaInput] = None) -> MeteorologiaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise MeteorologiaError("MeteorologiaInput data must be provided.")
        if input_data.altitude_m < 0:
            raise MeteorologiaError("Altitude must be non-negative.")
        if input_data.base_temp_k <= 0:
            raise MeteorologiaError("Base temperature must be positive (Kelvin).")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Temperature at altitude (Troposphere model)
        temp_at_alt = input_data.base_temp_k - (L * input_data.altitude_m)
        
        if temp_at_alt <= 0:
            raise MeteorologiaError("Calculated temperature fell below absolute zero. Altitude too high for troposphere model.")

        # Barometric formula for pressure
        exponent = (G * M) / (R * L)
        pressure = input_data.base_pressure_pa * math.pow((temp_at_alt / input_data.base_temp_k), exponent)
        
        # Ideal Gas Law for Air Density: rho = P * M / (R * T)
        density = (pressure * M) / (R * temp_at_alt)
        
        # Stability check based on lapse rate and humidity (simplified)
        # Wet adiabatic lapse rate is typically ~5 K/km. Dry is ~9.8 K/km.
        # Environmental lapse rate > 9.8 is absolutely unstable.
        if input_data.humidity_percent > 80.0:
            status = MeteorologiaStatus.UNSTABLE.name
            diagnostics.append("High humidity; potential for convective instability and precipitation.")
        else:
            status = MeteorologiaStatus.STABLE.name
            diagnostics.append("Atmosphere is generally stable.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "temperature_celsius": temp_at_alt - 273.15,
            "pressure_atm": pressure / 101325.0
        }

        return MeteorologiaOutput(
            agent_id=AGENT_ID,
            status=status,
            temperature_k=round(temp_at_alt, 2),
            pressure_pa=round(pressure, 2),
            air_density_kg_m3=round(density, 4),
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
