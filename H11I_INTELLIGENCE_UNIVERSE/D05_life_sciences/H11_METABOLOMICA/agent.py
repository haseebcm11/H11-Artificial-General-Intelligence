"""H11_METABOLOMICA: Metabolomics & Enzyme Kinetics Engine.

D05_life_sciences - Universe

This module implements the analytical execution engine for H11_METABOLOMICA.
It computes reaction velocities using Michaelis-Menten kinetics,
Lineweaver-Burk transformations, and catalytic efficiencies.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_METABOLOMICA"

class MetabolomicaError(ValueError):
    """Domain-specific error for H11_METABOLOMICA."""
    pass

class MetabolomicaStatus(Enum):
    IDLE = auto()
    UNSATURATED = auto()
    SATURATED = auto()
    FAILED = auto()

@dataclass(frozen=True)
class MetabolomicaInput:
    substrate_concentration_s: float
    v_max: float
    km_michaelis_constant: float
    enzyme_concentration_e0: float = 1.0

@dataclass(frozen=True)
class MetabolomicaOutput:
    agent_id: str
    status: str
    reaction_velocity_v: float
    catalytic_rate_kcat: float
    catalytic_efficiency: float
    lineweaver_burk_x: float
    lineweaver_burk_y: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class MetabolomicaAgent:
    """Analytical engine for enzyme kinetics and metabolic fluxes."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": MetabolomicaStatus.IDLE.name
        }

    def process(self, input_data: Optional[MetabolomicaInput] = None) -> MetabolomicaOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise MetabolomicaError("MetabolomicaInput data must be provided.")
        if input_data.substrate_concentration_s < 0:
            raise MetabolomicaError("Substrate concentration cannot be negative.")
        if input_data.v_max <= 0 or input_data.km_michaelis_constant <= 0:
            raise MetabolomicaError("Vmax and Km must be strictly positive.")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Michaelis-Menten Equation: v = (Vmax * [S]) / (Km + [S])
        s = input_data.substrate_concentration_s
        v_max = input_data.v_max
        km = input_data.km_michaelis_constant
        e0 = input_data.enzyme_concentration_e0

        velocity = (v_max * s) / (km + s)
        
        # Catalytic Rate Constant (Turnover Number): kcat = Vmax / [E]T
        kcat = v_max / e0 if e0 > 0 else 0.0
        
        # Catalytic Efficiency: kcat / Km
        efficiency = kcat / km if km > 0 else 0.0

        # Lineweaver-Burk Double Reciprocal Plot coordinates
        lwb_x = 1.0 / s if s > 0 else float('inf')
        lwb_y = 1.0 / velocity if velocity > 0 else float('inf')

        if s >= 10 * km:
            status = MetabolomicaStatus.SATURATED.name
            diagnostics.append("Enzyme is fully saturated with substrate (zero-order kinetics).")
        elif s < km:
            status = MetabolomicaStatus.UNSATURATED.name
            diagnostics.append("Enzyme is unsaturated (first-order kinetics region).")
        else:
            status = MetabolomicaStatus.UNSATURATED.name
            diagnostics.append("Enzyme is partially saturated.")

        self.state["status"] = status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "saturation_fraction": velocity / v_max,
            "specificity_constant": efficiency
        }

        return MetabolomicaOutput(
            agent_id=AGENT_ID,
            status=status,
            reaction_velocity_v=round(velocity, 6),
            catalytic_rate_kcat=round(kcat, 4),
            catalytic_efficiency=round(efficiency, 4),
            lineweaver_burk_x=lwb_x,
            lineweaver_burk_y=lwb_y,
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
