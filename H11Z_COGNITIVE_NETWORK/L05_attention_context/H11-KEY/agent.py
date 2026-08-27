import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-KEY"

class KeyException(Exception):
    pass

@dataclass
class KeyInput:
    hidden_states: List[List[float]]
    w_k: List[List[float]] # [d_model, d_k]

@dataclass
class KeyOutput:
    keys: List[List[float]]
    key_norm: float

class KeyAgent:
    """
    H11-KEY
    Projects hidden states to the Key subspace K = X * W_K.
    Measures the L2 norm of the resulting keys to track representational span.
    """
    def __init__(self):
        pass

    def process(self, input_data: KeyInput) -> KeyOutput:
        X = input_data.hidden_states
        W = input_data.w_k
        
        if not X or not W:
            raise KeyException("Empty inputs")
            
        seq_len = len(X)
        d_model = len(X[0])
        d_k = len(W[0])
        
        if len(W) != d_model:
            raise KeyException("Dimension mismatch")
            
        K = [[0.0 for _ in range(d_k)] for _ in range(seq_len)]
        total_sq_norm = 0.0
        
        for i in range(seq_len):
            for j in range(d_k):
                val = sum(X[i][d] * W[d][j] for d in range(d_model))
                K[i][j] = val
                total_sq_norm += val * val
                
        key_norm = math.sqrt(total_sq_norm / (seq_len * d_k))
        
        return KeyOutput(
            keys=K,
            key_norm=key_norm
        )
