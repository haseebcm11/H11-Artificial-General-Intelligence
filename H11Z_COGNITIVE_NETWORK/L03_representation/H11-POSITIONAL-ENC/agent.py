"""
H11-POSITIONAL-ENC: Transformers Sinusoidal Positional Encoding.
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-POSITIONAL-ENC"

@dataclass
class PositionalInput:
    seq_len: int
    d_model: int
    base: float = 10000.0

@dataclass
class PositionalOutput:
    encoding: List[List[float]]

class H11PositionalEncAgent:
    def process(self, data: PositionalInput) -> PositionalOutput:
        encoding = []
        for pos in range(data.seq_len):
            pos_enc = []
            for i in range(data.d_model):
                # 2i/d_model
                exp = (2 * (i // 2)) / data.d_model
                div_term = math.pow(data.base, exp)
                if i % 2 == 0:
                    pos_enc.append(math.sin(pos / div_term))
                else:
                    pos_enc.append(math.cos(pos / div_term))
            encoding.append(pos_enc)
            
        return PositionalOutput(encoding=encoding)
