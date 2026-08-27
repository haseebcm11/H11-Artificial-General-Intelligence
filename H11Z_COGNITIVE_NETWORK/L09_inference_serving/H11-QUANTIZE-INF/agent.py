import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-QUANTIZE-INF"

@dataclass
class QuantizeInput:
    weights: List[float]
    bits: int

@dataclass
class QuantizeOutput:
    quantized_weights: List[int]
    scale: float
    zero_point: int
    quantization_error: float

class QuantizeException(Exception):
    pass

class H11QuantizeInfAgent:
    """
    Applies weight-only quantization.
    Formulas:
    scale = (max - min) / (2^bits - 1)
    zero_point = round(-min / scale)
    q = round(w / scale) + zero_point
    """
    def process(self, input_data: QuantizeInput) -> QuantizeOutput:
        w = input_data.weights
        if not w:
            raise QuantizeException("Empty weights")
            
        w_min, w_max = min(w), max(w)
        q_max = (1 << input_data.bits) - 1
        
        scale = (w_max - w_min) / q_max if q_max > 0 and w_max > w_min else 1.0
        zero_point = max(0, min(q_max, int(round(-w_min / scale))))
        
        q_weights = []
        mse = 0.0
        
        for val in w:
            q_val = int(round(val / scale)) + zero_point
            q_val = max(0, min(q_max, q_val))
            q_weights.append(q_val)
            
            # Dequantize for error calculation
            deq_val = (q_val - zero_point) * scale
            mse += (val - deq_val) ** 2
            
        mse /= len(w)
        
        return QuantizeOutput(
            quantized_weights=q_weights,
            scale=scale,
            zero_point=zero_point,
            quantization_error=mse
        )
