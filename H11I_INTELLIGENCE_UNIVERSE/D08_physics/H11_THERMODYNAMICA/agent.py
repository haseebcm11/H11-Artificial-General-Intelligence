"""H11_THERMODYNAMICA: Models thermodynamics and heat transfer.

D08_physics - Universe

This module implements deterministic calculations for Carnot efficiency,
ideal gas laws, and entropy changes.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_THERMODYNAMICA"
IDEAL_GAS_CONSTANT = 8.314  # J/(mol*K)

class ThermodynamicaError(ValueError):
    """Domain-specific error for H11_THERMODYNAMICA."""
    pass

class ThermodynamicaStatus(Enum):
    IDLE = auto()
    NOMINAL = auto()
    IRREVERSIBLE = auto()
    VIOLATION = auto()

@dataclass(frozen=True)
class ThermodynamicaInput:
    temp_hot_k: float
    temp_cold_k: float
    moles: float
    volume_initial_m3: float
    volume_final_m3: float
    heat_added_j: float

@dataclass(frozen=True)
class ThermodynamicaOutput:
    agent_id: str
    status: str
    carnot_efficiency: float
    work_done_j: float
    entropy_change_j_k: float
    final_pressure_pa: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class ThermodynamicaAgent:
    """Analytical engine for Thermodynamics."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": ThermodynamicaStatus.IDLE.name}

    def process(self, input_data: Optional[ThermodynamicaInput] = None) -> ThermodynamicaOutput:
        start_time = time.perf_counter()
        if input_data is None:
            raise ThermodynamicaError("Input data required.")

        if input_data.temp_hot_k <= 0 or input_data.temp_cold_k <= 0:
            raise ThermodynamicaError("Temperatures must be in Kelvin (>0).")
        if input_data.volume_initial_m3 <= 0 or input_data.volume_final_m3 <= 0:
            raise ThermodynamicaError("Volumes must be positive.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1

        # Carnot Efficiency: eta = 1 - (Tc / Th)
        if input_data.temp_cold_k > input_data.temp_hot_k:
            carnot_eff = 0.0
            diagnostics = ["Cold reservoir is hotter than hot reservoir! Heat pump mode."]
            diag_status = ThermodynamicaStatus.VIOLATION.name
        else:
            carnot_eff = 1.0 - (input_data.temp_cold_k / input_data.temp_hot_k)
            diagnostics = []
            diag_status = ThermodynamicaStatus.NOMINAL.name

        # Ideal Gas Law PV = nRT -> Isothermal expansion work: W = nRT * ln(Vf/Vi)
        work_done = input_data.moles * IDEAL_GAS_CONSTANT * input_data.temp_hot_k * math.log(input_data.volume_final_m3 / input_data.volume_initial_m3)
        
        # Final Pressure: P = nRT / V
        final_pressure = (input_data.moles * IDEAL_GAS_CONSTANT * input_data.temp_hot_k) / input_data.volume_final_m3

        # Entropy change for isothermal expansion: dS = nR * ln(Vf/Vi) 
        # Entropy change from heat added: dS = dQ / Th
        entropy_change = (input_data.heat_added_j / input_data.temp_hot_k) + (input_data.moles * IDEAL_GAS_CONSTANT * math.log(input_data.volume_final_m3 / input_data.volume_initial_m3))

        if entropy_change < 0:
            diagnostics.append("Local entropy decreased, ensure environment entropy increases to not violate 2nd Law.")
        elif entropy_change > 0:
            diag_status = ThermodynamicaStatus.IRREVERSIBLE.name
            diagnostics.append("Process is irreversible.")

        self.state["status"] = diag_status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "carnot_efficiency": round(carnot_eff, 4),
            "pressure_pa": round(final_pressure, 2)
        }

        return ThermodynamicaOutput(
            agent_id=AGENT_ID,
            status=diag_status,
            carnot_efficiency=round(carnot_eff, 4),
            work_done_j=round(work_done, 2),
            entropy_change_j_k=round(entropy_change, 4),
            final_pressure_pa=round(final_pressure, 2),
            execution_time_ms=round(elapsed_ms, 4),
            metrics=metrics,
            diagnostics=diagnostics
        )
