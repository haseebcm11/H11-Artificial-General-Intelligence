"""H11_EVOBIO: Evolutionary Biology Engine.

D05_life_sciences - Universe

This module implements the analytical execution engine for H11_EVOBIO.
It provides rigorous computation for population genetics, including
Hardy-Weinberg equilibrium equations (p^2 + 2pq + q^2 = 1), directional 
selection, and genetic drift variance models.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_EVOBIO"

class EvobioError(ValueError):
    """Domain-specific error for H11_EVOBIO."""
    pass

class EvobioStatus(Enum):
    IDLE = auto()
    EQUILIBRIUM = auto()
    EVOLVING = auto()
    BOTTLENECK = auto()
    FAILED = auto()

@dataclass(frozen=True)
class EvobioInput:
    allele_p_freq: float
    population_size: int
    mutation_rate: float = 1e-6
    selection_coefficient: float = 0.0
    generations: int = 1
    inbreeding_coefficient: float = 0.0

@dataclass(frozen=True)
class EvobioOutput:
    agent_id: str
    status: str
    freq_p2: float
    freq_2pq: float
    freq_q2: float
    equilibrium_delta: float
    drift_variance: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class EvobioAgent:
    """Analytical engine for modeling evolutionary dynamics and population genetics."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {
            "evaluations_count": 0, 
            "status": EvobioStatus.IDLE.name,
            "last_equilibrium_delta": 0.0
        }

    def process(self, input_data: Optional[EvobioInput] = None) -> EvobioOutput:
        start_time = time.perf_counter()
        
        if input_data is None:
            raise EvobioError("EvobioInput data must be provided.")
        if not (0.0 <= input_data.allele_p_freq <= 1.0):
            raise EvobioError("Allele frequency must be strictly between 0.0 and 1.0")
        if input_data.population_size < 1:
            raise EvobioError("Population size must be at least 1")

        self.state["evaluations_count"] = int(self.state.get("evaluations_count", 0)) + 1
        diagnostics = []

        # Initialization
        p = input_data.allele_p_freq
        q = 1.0 - p
        n_e = input_data.population_size
        s = input_data.selection_coefficient
        F = input_data.inbreeding_coefficient
        
        # Generational loop for selection and mutation
        for _ in range(input_data.generations):
            # Selection against homozygous recessive (q^2)
            w_bar = p**2 + 2*p*q + q**2 * (1 - s)
            if w_bar == 0:
                p_prime = p
            else:
                p_prime = (p**2 + p*q) / w_bar
            
            # Forward and backward mutation
            mu = input_data.mutation_rate
            nu = input_data.mutation_rate * 0.5  # Assuming reverse mutation is half
            p_prime = p_prime * (1 - mu) + (1 - p_prime) * nu
            
            p = p_prime
            q = 1.0 - p

        # Hardy-Weinberg Frequencies with Inbreeding (Wright's F-statistics)
        p2 = p**2 + F*p*q
        pq2 = 2*p*q * (1 - F)
        q2 = q**2 + F*p*q
        
        total = p2 + pq2 + q2
        delta = abs(1.0 - total) + abs(input_data.allele_p_freq - p)
        
        # Genetic drift variance: Var(p) = pq / (2Ne)
        drift_var = (p * q) / (2 * n_e) if n_e > 0 else 0.0

        if n_e < 500:
            status = EvobioStatus.BOTTLENECK.name
            diagnostics.append("Population bottleneck detected. High risk of genetic drift.")
        elif delta < 1e-5 and F < 1e-4:
            status = EvobioStatus.EQUILIBRIUM.name
            diagnostics.append("Population is in strict Hardy-Weinberg equilibrium.")
        else:
            status = EvobioStatus.EVOLVING.name
            diagnostics.append(f"Population is evolving. Shift delta: {delta:.6e}")

        self.state["status"] = status
        self.state["last_equilibrium_delta"] = delta
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metrics = {
            "final_p": p,
            "final_q": q,
            "mean_fitness_w": w_bar,
            "inbreeding_f": F
        }

        return EvobioOutput(
            agent_id=AGENT_ID,
            status=status,
            freq_p2=round(p2, 6),
            freq_2pq=round(pq2, 6),
            freq_q2=round(q2, 6),
            equilibrium_delta=round(delta, 8),
            drift_variance=round(drift_var, 8),
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
