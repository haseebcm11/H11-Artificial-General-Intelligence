import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-ROPE"

class RoPEException(Exception):
    pass

@dataclass
class RoPEInput:
    states: List[List[float]]
    base: float = 10000.0

@dataclass
class RoPEOutput:
    rotated_states: List[List[float]]
    max_theta: float

class RoPEAgent:
    """
    H11-ROPE (Rotary Position Embeddings)
    Applies rotation matrices R(theta_m) to complex-paired dimensions.
    Encodes relative position intrinsically without additive embeddings.
    """
    def __init__(self):
        pass

    def process(self, input_data: RoPEInput) -> RoPEOutput:
        states = input_data.states
        base = input_data.base
        
        if not states:
            raise RoPEException("Empty states")
            
        seq_len = len(states)
        d = len(states[0])
        
        if d % 2 != 0:
            raise RoPEException("Dimension must be even for RoPE")
            
        out_states = []
        max_theta_val = 0.0
        
        for m in range(seq_len):
            state = states[m]
            out = [0.0 for _ in range(d)]
            
            for i in range(0, d, 2):
                theta = m * (base ** (-i / d))
                max_theta_val = max(max_theta_val, theta)
                
                cos_t = math.cos(theta)
                sin_t = math.sin(theta)
                
                x1 = state[i]
                x2 = state[i+1]
                
                out[i]   = x1 * cos_t - x2 * sin_t
                out[i+1] = x1 * sin_t + x2 * cos_t
                
            out_states.append(out)
            
        return RoPEOutput(
            rotated_states=out_states,
            max_theta=max_theta_val
        )
