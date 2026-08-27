from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-LONGCONTEXT"

class ContextScaleError(Exception):
    """Raised for unsupported scaling parameters."""
    pass

@dataclass
class LongContextInput:
    context_length: int
    base_theta: float = 10000.0
    scaling_factor: float = 8.0
    yarn_alpha: float = 1.0
    yarn_beta: float = 32.0

@dataclass
class LongContextOutput:
    scaled_theta: float
    ramp_factors: List[float]

class LongContextAgent:
    """
    YaRN (Yet another RoPE extensioN) context scaling computation.
    Adjusts base theta and calculates frequency-dependent interpolation ramp.
    """
    def process(self, req: LongContextInput) -> LongContextOutput:
        if req.yarn_alpha >= req.yarn_beta:
            raise ContextScaleError("YaRN alpha must be less than beta")
            
        scaled_theta = req.base_theta * (req.scaling_factor ** (req.context_length / req.yarn_alpha))
        
        D = 128
        ramp = []
        for i in range(0, D, 2):
            freq = scaled_theta ** (-i / D)
            val = (freq * req.context_length - req.yarn_alpha) / (req.yarn_beta - req.yarn_alpha)
            val = max(0.0, min(1.0, val))
            ramp.append(val)
            
        return LongContextOutput(
            scaled_theta=scaled_theta,
            ramp_factors=ramp
        )
