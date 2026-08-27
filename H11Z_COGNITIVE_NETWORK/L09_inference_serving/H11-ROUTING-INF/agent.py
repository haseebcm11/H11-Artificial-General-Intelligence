import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-ROUTING-INF"

@dataclass
class RoutingInput:
    expert_scores: List[float]
    top_k: int

@dataclass
class RoutingOutput:
    selected_experts: List[int]
    routing_weights: List[float]

class RoutingException(Exception):
    pass

class H11RoutingInfAgent:
    """
    MoE Router math. Softmax over expert scores, select top K, renormalize.
    """
    def process(self, input_data: RoutingInput) -> RoutingOutput:
        if not input_data.expert_scores:
            raise RoutingException("No scores")
            
        max_s = max(input_data.expert_scores)
        exp_s = [math.exp(s - max_s) for s in input_data.expert_scores]
        sum_exp = sum(exp_s)
        probs = [e / sum_exp for e in exp_s]
        
        indexed = list(enumerate(probs))
        indexed.sort(key=lambda x: x[1], reverse=True)
        
        top = indexed[:input_data.top_k]
        top_sum = sum(x[1] for x in top)
        
        return RoutingOutput(
            selected_experts=[x[0] for x in top],
            routing_weights=[x[1]/top_sum for x in top] if top_sum > 0 else []
        )
