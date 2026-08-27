import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-SOFTMAX"

class SoftmaxException(Exception):
    pass

@dataclass
class SoftmaxInput:
    logits: List[float]

@dataclass
class SoftmaxOutput:
    probabilities: List[float]
    max_logit: float
    sum_exp: float

class SoftmaxAgent:
    """
    H11-SOFTMAX
    Numerically stable softmax computation using max subtraction trick.
    Calculates exact distributions over logits.
    """
    def __init__(self):
        pass

    def process(self, input_data: SoftmaxInput) -> SoftmaxOutput:
        logits = input_data.logits
        if not logits:
            raise SoftmaxException("Empty logits")
            
        max_val = max(logits)
        exps = [math.exp(x - max_val) for x in logits]
        sum_exp = sum(exps)
        probs = [x / sum_exp for x in exps]
        
        return SoftmaxOutput(
            probabilities=probs,
            max_logit=max_val,
            sum_exp=sum_exp
        )
