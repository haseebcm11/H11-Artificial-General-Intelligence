"""H11_ECOLOGIA: Ecology & Ecosystems Processing Engine.

D05_life_sciences - Universe

This module implements the analytical execution engine for H11_ECOLOGIA.
It provides rigorous Lotka-Volterra predator-prey dynamics and Shannon
biodiversity index calculations.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_ECOLOGIA"

class EcologiaError(ValueError):
    """Domain-specific error for H11_ECOLOGIA."""
    pass

class EcologiaStatus(Enum):
    IDLE = auto()
    STABLE = auto()
    EXTINCTION = auto()
    UNSTABLE = auto()

@dataclass(frozen=True)
class SpeciesInput:
    name: str
    population: float

@dataclass(frozen=True)
class EcologiaInput:
    prey_population: float
    predator_population: float
    alpha: float  # Prey growth rate
    beta: float   # Predation rate
    gamma: float  # Predator death rate
    delta: float  # Predator reproduction rate
    time_steps: int = 100
    dt: float = 0.1
    species_counts: List[SpeciesInput] = field(default_factory=list)

@dataclass(frozen=True)
class EcologiaOutput:
    agent_id: str
    status: str
    final_prey: float
    final_predator: float
    shannon_index: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class EcologiaAgent:
    """Analytical engine for modeling ecosystem dynamics and biodiversity."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": EcologiaStatus.IDLE.name}

    def process(self, input_data: Optional[EcologiaInput] = None) -> EcologiaOutput:
        start_time = time.perf_counter()
        if input_data is None:
            raise EcologiaError("Input data is required for ECOLOGIA.")

        # Validate inputs
        if input_data.prey_population < 0 or input_data.predator_population < 0:
            raise EcologiaError("Populations cannot be negative")
        
        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1

        # Lotka-Volterra Integration (Euler method)
        x = input_data.prey_population
        y = input_data.predator_population
        
        for _ in range(input_data.time_steps):
            dx = (input_data.alpha * x - input_data.beta * x * y) * input_data.dt
            dy = (input_data.delta * x * y - input_data.gamma * y) * input_data.dt
            x = max(0.0, x + dx)
            y = max(0.0, y + dy)
            if x == 0 and y == 0:
                break

        # Shannon Biodiversity Index: H = -sum(p_i * ln(p_i))
        shannon_index = 0.0
        if input_data.species_counts:
            total_individuals = sum(s.population for s in input_data.species_counts)
            if total_individuals > 0:
                for s in input_data.species_counts:
                    if s.population > 0:
                        p_i = s.population / total_individuals
                        shannon_index -= p_i * math.log(p_i)

        diagnostics = []
        if x == 0 or y == 0:
            diag_status = EcologiaStatus.EXTINCTION.name
            diagnostics.append("Extinction event occurred in simulation.")
        elif x > input_data.prey_population * 10 or y > input_data.predator_population * 10:
            diag_status = EcologiaStatus.UNSTABLE.name
            diagnostics.append("Population explosion detected.")
        else:
            diag_status = EcologiaStatus.STABLE.name
            diagnostics.append("Ecosystem equilibrium maintained.")

        self.state["status"] = diag_status
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return EcologiaOutput(
            agent_id=AGENT_ID,
            status=diag_status,
            final_prey=round(x, 4),
            final_predator=round(y, 4),
            shannon_index=round(shannon_index, 6),
            execution_time_ms=round(elapsed_ms, 4),
            metrics={"prey_variance": abs(x - input_data.prey_population)},
            diagnostics=diagnostics
        )
