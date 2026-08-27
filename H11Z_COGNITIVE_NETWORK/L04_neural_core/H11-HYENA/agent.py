"""
H11-HYENA: Hyena Filter
Implicit long convolution parameterization.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-HYENA"

@dataclass
class HyenaInput:
    t: int
    omega: float
    alpha: float

@dataclass
class HyenaOutput:
    filter_val: float

class Agent:
    def process(self, input_data: HyenaInput) -> HyenaOutput:
        window = math.exp(-input_data.alpha * input_data.t)
        val = window * math.sin(input_data.omega * input_data.t)
        return HyenaOutput(filter_val=val)
