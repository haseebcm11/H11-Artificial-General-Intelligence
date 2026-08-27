import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-TOPK"

@dataclass
class TopKInput:
    logits: List[float]
    k: int

@dataclass
class TopKOutput:
    masked_logits: List[float]

class TopKException(Exception):
    pass

class H11TopkAgent:
    """
    Top-K sampling mask. Sets logits outside top-K to -infinity.
    """
    def process(self, input_data: TopKInput) -> TopKOutput:
        if input_data.k <= 0 or input_data.k > len(input_data.logits):
            raise TopKException("Invalid K")
            
        indexed = list(enumerate(input_data.logits))
        indexed.sort(key=lambda x: x[1], reverse=True)
        
        threshold = indexed[input_data.k - 1][1]
        
        masked = [v if v >= threshold else -float('inf') for v in input_data.logits]
        return TopKOutput(masked_logits=masked)
