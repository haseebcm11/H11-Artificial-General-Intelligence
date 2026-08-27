"""H11_RELATIVITAS: Special & General Relativity Engine.

D08_physics - Universe

This module implements the analytical execution engine for H11_RELATIVITAS.
It resolves Lorentz transformations, time dilation, and relativistic 
kinetic energy calculations.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_RELATIVITAS"
C_M_S = 299792458.0  # Speed of light in m/s

class RelativitasError(ValueError):
    """Domain-specific error for H11_RELATIVITAS."""
    pass

class RelativitasStatus(Enum):
    IDLE = auto()
    CLASSICAL = auto()
    RELATIVISTIC = auto()
    TACHYONIC = auto()
    FAILED = auto()

@dataclass(frozen=True)
class RelativitasInput:
    velocity_m_s: float
    rest_mass_kg: float
    proper_time_s: float
    proper_length_m: float

@dataclass(frozen=True)
class RelativitasOutput:
    agent_id: str
    status: str
    lorentz_factor: float
    dilated_time_s: float
    contracted_length_m: float
    relativistic_momentum_kg_m_s: float
    kinetic_energy_joules: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class RelativitasAgent:
    """Analytical engine for computing relativistic mechanics and transformations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": RelativitasStatus.IDLE.name
        }

    def process(self, input_data: Optional[RelativitasInput] = None) -> RelativitasOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise RelativitasError("RelativitasInput data must be provided.")
        if input_data.rest_mass_kg < 0:
            raise RelativitasError("Rest mass cannot be negative.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        v = abs(input_data.velocity_m_s)
        if v >= C_M_S:
            status = RelativitasStatus.TACHYONIC.name
            diagnostics.append("Velocity exceeds or equals c. Physics violation in real-space.")
            gamma = float('inf')
            dilated_t = float('inf')
            contracted_l = 0.0
            momentum = float('inf')
            ke = float('inf')
        else:
            # Lorentz Factor: gamma = 1 / sqrt(1 - v^2/c^2)
            beta = v / C_M_S
            gamma = 1.0 / math.sqrt(1.0 - beta**2)
            
            # Time Dilation: t = gamma * t0
            dilated_t = gamma * input_data.proper_time_s
            
            # Length Contraction: L = L0 / gamma
            contracted_l = input_data.proper_length_m / gamma
            
            # Relativistic Momentum: p = gamma * m0 * v
            momentum = gamma * input_data.rest_mass_kg * v
            
            # Relativistic Kinetic Energy: KE = (gamma - 1) * m0 * c^2
            ke = (gamma - 1.0) * input_data.rest_mass_kg * (C_M_S ** 2)
            
            if beta > 0.1:
                status = RelativitasStatus.RELATIVISTIC.name
                diagnostics.append("High relativistic effects detected.")
            else:
                status = RelativitasStatus.CLASSICAL.name
                diagnostics.append("Velocity is within classical Newtonian limits.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "beta": v / C_M_S,
            "rest_energy_joules": input_data.rest_mass_kg * (C_M_S ** 2)
        }

        return RelativitasOutput(
            agent_id=AGENT_ID,
            status=status,
            lorentz_factor=gamma if gamma != float('inf') else -1.0,
            dilated_time_s=dilated_t,
            contracted_length_m=contracted_l,
            relativistic_momentum_kg_m_s=momentum,
            kinetic_energy_joules=ke,
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
