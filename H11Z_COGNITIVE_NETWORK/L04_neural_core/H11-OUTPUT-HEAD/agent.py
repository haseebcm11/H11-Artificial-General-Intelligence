"""
H11-OUTPUT-HEAD: Loss Functions
Cross-Entropy and Focal Loss.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-OUTPUT-HEAD"

@dataclass
class HeadInput:
    logits: list[float]
    target_idx: int
    gamma: float = 2.0

@dataclass
class HeadOutput:
    cross_entropy: float
    focal_loss: float

class Agent:
    def process(self, input_data: HeadInput) -> HeadOutput:
        max_l = max(input_data.logits)
        exp_l = [math.exp(l - max_l) for l in input_data.logits]
        sum_exp = sum(exp_l)
        probs = [el / sum_exp for el in exp_l]
        
        p_t = probs[input_data.target_idx]
        ce = -math.log(p_t + 1e-9)
        fl = (1 - p_t)**input_data.gamma * ce
        
        return HeadOutput(cross_entropy=ce, focal_loss=fl)
