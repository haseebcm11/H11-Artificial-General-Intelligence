"""association: Hebbian learning and synaptic plasticity.

Implements Long-Term Potentiation (LTP) and Depression (LTD) via Oja's rule.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "association"

class AssociationError(ValueError): pass

@dataclass
class AssociationInput:
    pre_synaptic: List[float]
    post_synaptic: List[float]
    weights: List[List[float]]
    learning_rate: float = 0.01

@dataclass
class AssociationOutput:
    agent_id: str
    updated_weights: List[List[float]]
    weight_delta_norm: float
    execution_time_ms: float

class AssociationAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: AssociationInput) -> AssociationOutput:
        start_time = time.perf_counter()
        
        pre = input_data.pre_synaptic
        post = input_data.post_synaptic
        w = input_data.weights
        lr = input_data.learning_rate
        
        if not pre or not post or not w:
            raise AssociationError("Invalid dimensions for Hebbian update")
            
        new_w = []
        delta_norm_sq = 0.0
        
        # Oja's rule: dW_ij = lr * y_i * (x_j - y_i * W_ij)
        for i, y_i in enumerate(post):
            row = []
            for j, x_j in enumerate(pre):
                old_w = w[i][j]
                delta = lr * y_i * (x_j - y_i * old_w)
                row.append(old_w + delta)
                delta_norm_sq += delta * delta
            new_w.append(row)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return AssociationOutput(
            agent_id=AGENT_ID,
            updated_weights=new_w,
            weight_delta_norm=delta_norm_sq ** 0.5,
            execution_time_ms=elapsed_ms
        )
