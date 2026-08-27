import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-TOPP"

@dataclass
class TopPInput:
    probs: List[float]
    p: float

@dataclass
class TopPOutput:
    retained_indices: List[int]
    cdf_mass: float

class TopPException(Exception):
    pass

class H11ToppAgent:
    """
    Top-P (Nucleus) sampling.
    Retains smallest set of tokens whose cumulative probability >= p.
    """
    def process(self, input_data: TopPInput) -> TopPOutput:
        if not (0 < input_data.p <= 1.0):
            raise TopPException("p must be in (0, 1]")
            
        indexed = list(enumerate(input_data.probs))
        indexed.sort(key=lambda x: x[1], reverse=True)
        
        cdf = 0.0
        retained = []
        
        for idx, prob in indexed:
            retained.append(idx)
            cdf += prob
            if cdf >= input_data.p:
                break
                
        return TopPOutput(retained_indices=retained, cdf_mass=cdf)
