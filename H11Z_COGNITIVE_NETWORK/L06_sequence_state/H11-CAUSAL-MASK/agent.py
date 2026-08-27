from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-CAUSAL-MASK"

class MaskDimensionError(Exception):
    """Raised when mask dimensions are invalid."""
    pass

@dataclass
class CausalMaskInput:
    seq_len: int
    num_heads: int = 8
    use_alibi: bool = True

@dataclass
class CausalMaskOutput:
    masks: List[List[List[float]]] # [head][i][j]

class CausalMaskAgent:
    """
    Computes strict autoregressive causal masks and ALiBi (Attention with Linear Biases).
    ALiBi slope for head h: 2^(-8 * h / H)
    """
    def process(self, req: CausalMaskInput) -> CausalMaskOutput:
        if req.seq_len <= 0 or req.num_heads <= 0:
            raise MaskDimensionError("Invalid dimensions for causal mask")
            
        masks = []
        for h in range(1, req.num_heads + 1):
            head_mask = []
            slope = 2 ** (-8.0 * h / req.num_heads) if req.use_alibi else 0.0
            
            for i in range(req.seq_len):
                row = []
                for j in range(req.seq_len):
                    if j > i:
                        row.append(float('-inf'))
                    else:
                        bias = (j - i) * slope if req.use_alibi else 0.0
                        row.append(bias)
                head_mask.append(row)
            masks.append(head_mask)
            
        return CausalMaskOutput(masks=masks)
