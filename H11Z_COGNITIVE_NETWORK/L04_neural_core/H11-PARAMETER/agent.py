"""
H11-PARAMETER: Parameter Initialization
Xavier and He initialization variances.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-PARAMETER"

@dataclass
class ParamInput:
    fan_in: int
    fan_out: int

@dataclass
class ParamOutput:
    he_variance: float
    xavier_variance: float

class Agent:
    def process(self, input_data: ParamInput) -> ParamOutput:
        he_var = 2.0 / input_data.fan_in
        xavier_var = 2.0 / (input_data.fan_in + input_data.fan_out)
        return ParamOutput(he_variance=he_var, xavier_variance=xavier_var)
