"""
H11-RWKV: RWKV Attention
WKV linear attention computation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-RWKV"

@dataclass
class RWKVInput:
    r: float
    k: float
    v: float
    w: float
    u: float
    num: float
    den: float

@dataclass
class RWKVOutput:
    wkv: float
    next_num: float
    next_den: float

class Agent:
    def process(self, input_data: RWKVInput) -> RWKVOutput:
        wkv = (input_data.num + math.exp(input_data.u + input_data.k) * input_data.v) / (input_data.den + math.exp(input_data.u + input_data.k) + 1e-8)
        next_num = math.exp(input_data.w) * input_data.num + math.exp(input_data.k) * input_data.v
        next_den = math.exp(input_data.w) * input_data.den + math.exp(input_data.k)
        
        return RWKVOutput(wkv=wkv, next_num=next_num, next_den=next_den)
