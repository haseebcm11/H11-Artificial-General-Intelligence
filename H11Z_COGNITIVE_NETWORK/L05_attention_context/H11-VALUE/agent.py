import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-VALUE"

class ValueException(Exception):
    pass

@dataclass
class ValueInput:
    hidden_states: List[List[float]]
    w_v: List[List[float]] # [d_model, d_v]

@dataclass
class ValueOutput:
    values: List[List[float]]
    value_variance: float

class ValueAgent:
    """
    H11-VALUE
    Projects hidden states to the Value subspace V = X * W_V.
    Measures the variance of the resulting values to track informational spread.
    """
    def __init__(self):
        pass

    def process(self, input_data: ValueInput) -> ValueOutput:
        X = input_data.hidden_states
        W = input_data.w_v
        
        if not X or not W:
            raise ValueException("Empty inputs")
            
        seq_len = len(X)
        d_model = len(X[0])
        d_v = len(W[0])
        
        if len(W) != d_model:
            raise ValueException("Dimension mismatch")
            
        V = [[0.0 for _ in range(d_v)] for _ in range(seq_len)]
        total = 0.0
        total_sq = 0.0
        count = seq_len * d_v
        
        for i in range(seq_len):
            for j in range(d_v):
                val = sum(X[i][d] * W[d][j] for d in range(d_model))
                V[i][j] = val
                total += val
                total_sq += val * val
                
        mean = total / count
        variance = (total_sq / count) - (mean * mean)
        
        return ValueOutput(
            values=V,
            value_variance=variance
        )
