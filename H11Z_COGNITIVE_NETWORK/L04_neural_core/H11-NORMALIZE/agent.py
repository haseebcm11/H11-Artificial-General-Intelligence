"""
H11-NORMALIZE: Normalization Methods
RMSNorm exact computation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-NORMALIZE"

@dataclass
class NormInput:
    x: list[float]
    eps: float = 1e-5

@dataclass
class NormOutput:
    y: list[float]
    rms: float

class Agent:
    def process(self, input_data: NormInput) -> NormOutput:
        mean_sq = sum(v*v for v in input_data.x) / len(input_data.x)
        rms = math.sqrt(mean_sq + input_data.eps)
        y = [v / rms for v in input_data.x]
        return NormOutput(y=y, rms=rms)
