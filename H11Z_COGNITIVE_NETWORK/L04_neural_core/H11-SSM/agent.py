"""
H11-SSM: State Space Models
Zero-order hold continuous-to-discrete conversion.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-SSM"

@dataclass
class SSMInput:
    A: float
    B: float
    dt: float

@dataclass
class SSMOutput:
    A_bar: float
    B_bar: float

class Agent:
    def process(self, input_data: SSMInput) -> SSMOutput:
        A_bar = math.exp(input_data.A * input_data.dt)
        if input_data.A == 0:
            B_bar = input_data.B * input_data.dt
        else:
            B_bar = (A_bar - 1.0) / input_data.A * input_data.B
            
        return SSMOutput(A_bar=A_bar, B_bar=B_bar)
