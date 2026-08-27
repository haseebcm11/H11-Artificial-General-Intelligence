import math
from typing import Any, List
from dataclasses import dataclass

AGENT_ID = "H11-ATTENTION-MAP"

class AttentionMapException(Exception):
    pass

@dataclass
class AttentionMapInput:
    queries: List[List[float]]
    keys: List[List[float]]
    mask: List[List[bool]]
    scale_factor: float

@dataclass
class AttentionMapOutput:
    attention_scores: List[List[float]]
    density: float

class AttentionMapAgent:
    """
    H11-ATTENTION-MAP
    Computes the core N x N attention matrix mapping Q to K with masked scaling.
    Applies precise causal or structural masking and numerical stability improvements.
    """
    def __init__(self):
        self.map_density = 0.0

    def process(self, input_data: AttentionMapInput) -> AttentionMapOutput:
        q = input_data.queries
        k = input_data.keys
        mask = input_data.mask
        scale = input_data.scale_factor
        
        n_q = len(q)
        n_k = len(k)
        
        if n_q == 0 or n_k == 0:
            raise AttentionMapException("Query or Key sequences are empty")
            
        dim = len(q[0])
        scores = [[0.0 for _ in range(n_k)] for _ in range(n_q)]
        
        active_elements = 0
        total_elements = n_q * n_k
        
        for i in range(n_q):
            for j in range(n_k):
                if mask[i][j]:
                    scores[i][j] = -1e9 # Masked out
                else:
                    dot = sum(q[i][d] * k[j][d] for d in range(dim))
                    scores[i][j] = dot * scale
                    active_elements += 1
                    
        self.map_density = active_elements / total_elements if total_elements > 0 else 0.0
        
        return AttentionMapOutput(
            attention_scores=scores,
            density=self.map_density
        )
