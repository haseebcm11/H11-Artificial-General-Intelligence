"""
H11-FEEDFORWARD: Activation Math
Implements exact GELU and SiLU functions.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-FEEDFORWARD"

@dataclass
class FFInput:
    x: float

@dataclass
class FFOutput:
    relu: float
    silu: float
    gelu: float

class Agent:
    def process(self, input_data: FFInput) -> FFOutput:
        x = input_data.x
        relu = max(0.0, x)
        silu = x / (1.0 + math.exp(-x))
        gelu = 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0/math.pi) * (x + 0.044715 * x**3)))
        return FFOutput(relu=relu, silu=silu, gelu=gelu)
