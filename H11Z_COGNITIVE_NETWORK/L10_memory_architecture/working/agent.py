"""working: Working Memory active state manipulation.

Implements Long Short-Term Memory (LSTM) cell forward equations.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "working"

class WorkingError(ValueError): pass

def sigmoid(x: float) -> float:
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def tanh(x: float) -> float:
    return math.tanh(x)

@dataclass
class WorkingInput:
    x_t: List[float]
    h_prev: List[float]
    c_prev: List[float]
    W: List[List[float]] # Combined weight matrix
    b: List[float]       # Combined biases

@dataclass
class WorkingOutput:
    agent_id: str
    h_next: List[float]
    c_next: List[float]
    execution_time_ms: float

class WorkingAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: WorkingInput) -> WorkingOutput:
        start_time = time.perf_counter()
        
        dim = len(input_data.x_t)
        if len(input_data.h_prev) != dim or len(input_data.c_prev) != dim:
            raise WorkingError("Dimension mismatch")
            
        # Concat [h_prev, x_t]
        concat = input_data.h_prev + input_data.x_t
        
        # Matrix multiply: W * concat + b
        z = []
        for i in range(4 * dim):
            val = sum(input_data.W[i][j] * concat[j] for j in range(len(concat))) + input_data.b[i]
            z.append(val)
            
        # Split into i, f, o, g
        i_gate = [sigmoid(z[j]) for j in range(0, dim)]
        f_gate = [sigmoid(z[j]) for j in range(dim, 2*dim)]
        o_gate = [sigmoid(z[j]) for j in range(2*dim, 3*dim)]
        g_gate = [tanh(z[j]) for j in range(3*dim, 4*dim)]
        
        c_next = [f * c + i * g for f, c, i, g in zip(f_gate, input_data.c_prev, i_gate, g_gate)]
        h_next = [o * tanh(c) for o, c in zip(o_gate, c_next)]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return WorkingOutput(
            agent_id=AGENT_ID,
            h_next=h_next,
            c_next=c_next,
            execution_time_ms=elapsed_ms
        )
