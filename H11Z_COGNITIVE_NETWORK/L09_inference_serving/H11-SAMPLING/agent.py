import math
import random
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-SAMPLING"

@dataclass
class SamplingInput:
    logits: List[float]
    temperature: float

@dataclass
class SamplingOutput:
    sampled_index: int
    gumbel_max_val: float

class SamplingException(Exception):
    pass

class H11SamplingAgent:
    """
    Gumbel-max trick for categorical sampling.
    g = -log(-log(u)), argmax(logits/T + g)
    """
    def process(self, input_data: SamplingInput) -> SamplingOutput:
        best_idx = 0
        best_val = -float('inf')
        
        T = max(input_data.temperature, 1e-5)
        
        for i, logit in enumerate(input_data.logits):
            u = random.random()
            g = -math.log(-math.log(u + 1e-9) + 1e-9)
            val = (logit / T) + g
            if val > best_val:
                best_val = val
                best_idx = i
                
        return SamplingOutput(sampled_index=best_idx, gumbel_max_val=best_val)
