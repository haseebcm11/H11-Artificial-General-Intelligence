import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-SLIDING"

class SlidingException(Exception):
    pass

@dataclass
class SlidingInput:
    seq_length: int
    window_size: int

@dataclass
class SlidingOutput:
    mask: List[List[bool]]
    sparsity_ratio: float

class SlidingAgent:
    """
    H11-SLIDING
    Generates local attention masks based on a sliding window size.
    Limits context per token, achieving O(N*W) complexity natively.
    """
    def __init__(self):
        pass

    def process(self, input_data: SlidingInput) -> SlidingOutput:
        N = input_data.seq_length
        W = input_data.window_size
        
        if N <= 0 or W <= 0:
            raise SlidingException("Invalid bounds")
            
        mask = [[False for _ in range(N)] for _ in range(N)]
        allowed = 0
        total = N * N
        
        for i in range(N):
            for j in range(N):
                # Allowed if within causal and window limits
                if j <= i and i - j < W:
                    mask[i][j] = False
                    allowed += 1
                else:
                    mask[i][j] = True
                    
        sparsity_ratio = (total - allowed) / total if total > 0 else 0.0
        
        return SlidingOutput(
            mask=mask,
            sparsity_ratio=sparsity_ratio
        )
