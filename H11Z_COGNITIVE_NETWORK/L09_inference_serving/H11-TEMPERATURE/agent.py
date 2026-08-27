import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-TEMPERATURE"

@dataclass
class TemperatureInput:
    logits: List[float]
    temperature: float

@dataclass
class TemperatureOutput:
    scaled_probs: List[float]
    entropy: float

class TemperatureException(Exception):
    pass

class H11TemperatureAgent:
    """
    Softmax with temperature scaling.
    p_i = exp(z_i / T) / sum(exp(z_j / T))
    H = -sum(p * log(p))
    """
    def process(self, input_data: TemperatureInput) -> TemperatureOutput:
        T = max(input_data.temperature, 1e-5)
        scaled_logits = [z / T for z in input_data.logits]
        max_z = max(scaled_logits)
        
        exps = [math.exp(z - max_z) for z in scaled_logits]
        sum_exps = sum(exps)
        probs = [e / sum_exps for e in exps]
        
        entropy = -sum(p * math.log(p + 1e-9) for p in probs if p > 0)
        
        return TemperatureOutput(scaled_probs=probs, entropy=entropy)
