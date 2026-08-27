import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-ORDER"

class OrderDimensionError(Exception):
    """Raised for invalid rotary embedding dimensions."""
    pass

@dataclass
class OrderInput:
    positions: List[int]
    dim: int = 64
    base: float = 10000.0

@dataclass
class OrderOutput:
    sin_enc: List[List[float]]
    cos_enc: List[List[float]]

class OrderAgent:
    """
    Computes Rotary Positional Encodings (RoPE).
    theta_i = base^(-2i/d)
    """
    def process(self, req: OrderInput) -> OrderOutput:
        if req.dim % 2 != 0:
            raise OrderDimensionError("RoPE dimension must be even")
            
        sin_enc, cos_enc = [], []
        
        for pos in req.positions:
            s_row, c_row = [], []
            for i in range(req.dim // 2):
                theta = pos * (req.base ** (-2.0 * i / req.dim))
                s_row.append(math.sin(theta))
                c_row.append(math.cos(theta))
            sin_enc.append(s_row)
            cos_enc.append(c_row)
            
        return OrderOutput(
            sin_enc=sin_enc,
            cos_enc=cos_enc
        )
