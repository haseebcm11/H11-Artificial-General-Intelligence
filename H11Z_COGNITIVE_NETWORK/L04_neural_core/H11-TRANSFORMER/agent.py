"""
H11-TRANSFORMER: Core Transformer Logic
Scaled dot-product attention calculation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-TRANSFORMER"

@dataclass
class TransInput:
    q: list[float]
    k: list[float]
    v: list[float]

@dataclass
class TransOutput:
    attention: list[float]

class Agent:
    def process(self, input_data: TransInput) -> TransOutput:
        d = len(input_data.q)
        dot = sum(qi*ki for qi, ki in zip(input_data.q, input_data.k))
        scaled = dot / math.sqrt(d)
        
        score = math.exp(scaled)
        
        out = [vi * score for vi in input_data.v]
        return TransOutput(attention=out)
