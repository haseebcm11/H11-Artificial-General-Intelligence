"""context_mem: Context gating and situational binding.

Implements Sigmoid Attention for contextual filtering.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "context_mem"

class ContextError(ValueError): pass

@dataclass
class ContextInput:
    state_vector: List[float]
    context_weights: List[float]
    bias: float = -0.5

@dataclass
class ContextOutput:
    agent_id: str
    gating_factor: float
    gated_vector: List[float]
    execution_time_ms: float

class ContextAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: ContextInput) -> ContextOutput:
        start_time = time.perf_counter()
        
        if len(input_data.state_vector) != len(input_data.context_weights):
            raise ContextError("Vector and weight dimensions must match")
            
        dot_prod = sum(x * w for x, w in zip(input_data.state_vector, input_data.context_weights))
        
        # Sigmoid gating
        z = dot_prod + input_data.bias
        try:
            gate = 1.0 / (1.0 + math.exp(-z))
        except OverflowError:
            gate = 0.0 if z < 0 else 1.0
            
        gated_vec = [x * gate for x in input_data.state_vector]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ContextOutput(
            agent_id=AGENT_ID,
            gating_factor=gate,
            gated_vector=gated_vec,
            execution_time_ms=elapsed_ms
        )
