"""H11-CAUSAL-MODEL: Structural Causal Models and interventions.

Implements Directed Acyclic Graph (DAG) logic and simple interventional counterfactuals.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-CAUSAL-MODEL"

class CausalError(ValueError): pass

@dataclass
class CausalInput:
    variables: Dict[str, float]
    interventions: Dict[str, float] # do(X = x)

@dataclass
class CausalOutput:
    agent_id: str
    post_intervention_state: Dict[str, float]
    execution_time_ms: float

class CausalAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        # Hardcoded simple structural causal model: Z -> X, Z -> Y, X -> Y
        # X = 2*Z + U_x
        # Y = 3*X - Z + U_y

    def process(self, input_data: CausalInput) -> CausalOutput:
        start_time = time.perf_counter()
        
        # Base values (acting as noise terms if not intervened)
        Z = input_data.variables.get('Z', 0.0)
        U_x = input_data.variables.get('U_x', 0.0)
        U_y = input_data.variables.get('U_y', 0.0)
        
        # Interventional logic (do-calculus)
        # If intervened, the structural equation is severed
        if 'Z' in input_data.interventions:
            Z_val = input_data.interventions['Z']
        else:
            Z_val = Z
            
        if 'X' in input_data.interventions:
            X_val = input_data.interventions['X']
        else:
            X_val = 2.0 * Z_val + U_x
            
        if 'Y' in input_data.interventions:
            Y_val = input_data.interventions['Y']
        else:
            Y_val = 3.0 * X_val - Z_val + U_y

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return CausalOutput(
            agent_id=AGENT_ID,
            post_intervention_state={'Z': Z_val, 'X': X_val, 'Y': Y_val},
            execution_time_ms=elapsed_ms
        )
