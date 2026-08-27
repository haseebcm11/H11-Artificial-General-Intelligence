"""H11_ELECTROCHEMIA: Domain-specific agent for Electrochemistry.

D09_chemistry - Universe

Implements Arrhenius equation, Nernst equation, and Henderson-Hasselbalch equation.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

AGENT_ID = "H11_ELECTROCHEMIA"
R = 8.314  # Ideal gas constant J/(mol·K)
F = 96485.332  # Faraday constant C/mol

class ElectrochemiaError(ValueError):
    """Domain-specific error for H11_ELECTROCHEMIA."""
    pass

@dataclass(frozen=True)
class ArrheniusParams:
    A: float  # Pre-exponential factor
    Ea: float # Activation energy in J/mol
    T: float  # Temperature in Kelvin

@dataclass(frozen=True)
class NernstParams:
    E0: float # Standard cell potential
    n: int    # Number of moles of electrons transferred
    T: float  # Temperature in Kelvin
    Q: float  # Reaction quotient

@dataclass(frozen=True)
class HendersonHasselbalchParams:
    pKa: float
    A_minus: float # Concentration of conjugate base
    HA: float      # Concentration of acid

@dataclass(frozen=True)
class ElectrochemiaInput:
    arrhenius: Optional[ArrheniusParams] = None
    nernst: Optional[NernstParams] = None
    henderson: Optional[HendersonHasselbalchParams] = None

@dataclass(frozen=True)
class ElectrochemiaOutput:
    agent_id: str
    status: str
    k_arrhenius: Optional[float]
    e_nernst: Optional[float]
    ph_henderson: Optional[float]
    execution_time_ms: float

class ElectrochemiaAgent:
    """Agent for computing electrochemical and thermodynamic properties."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: ElectrochemiaInput) -> ElectrochemiaOutput:
        start_time = time.perf_counter()
        
        k_arrhenius = None
        e_nernst = None
        ph_henderson = None
        
        try:
            if input_data.arrhenius:
                a_params = input_data.arrhenius
                if a_params.T <= 0:
                    raise ElectrochemiaError("Temperature must be positive.")
                # k = A * exp(-Ea / RT)
                k_arrhenius = a_params.A * math.exp(-a_params.Ea / (R * a_params.T))
                
            if input_data.nernst:
                n_params = input_data.nernst
                if n_params.T <= 0:
                    raise ElectrochemiaError("Temperature must be positive.")
                if n_params.n <= 0:
                    raise ElectrochemiaError("Electrons transferred must be positive.")
                if n_params.Q <= 0:
                    raise ElectrochemiaError("Reaction quotient must be positive.")
                # E = E0 - (RT / nF) * ln(Q)
                e_nernst = n_params.E0 - ((R * n_params.T) / (n_params.n * F)) * math.log(n_params.Q)
                
            if input_data.henderson:
                h_params = input_data.henderson
                if h_params.A_minus < 0 or h_params.HA <= 0:
                    raise ElectrochemiaError("Concentrations must be valid.")
                # pH = pKa + log([A-] / [HA])
                ph_henderson = h_params.pKa + math.log10(h_params.A_minus / h_params.HA)
                
            status = "SUCCESS"
        except Exception as e:
            raise ElectrochemiaError(f"Computation failed: {str(e)}")

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ElectrochemiaOutput(
            agent_id=AGENT_ID,
            status=status,
            k_arrhenius=k_arrhenius,
            e_nernst=e_nernst,
            ph_henderson=ph_henderson,
            execution_time_ms=round(elapsed_ms, 4)
        )
