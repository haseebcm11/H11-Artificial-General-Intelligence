"""
H11-MOE: Mixture of Experts
Top-k routing capacity factor and load balancing math.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-MOE"

@dataclass
class MOEInput:
    router_logits: list[float]
    capacity_factor: float
    top_k: int
    tokens_per_batch: int

@dataclass
class MOEOutput:
    expert_capacity: int
    routing_probs: list[float]

class Agent:
    def process(self, input_data: MOEInput) -> MOEOutput:
        max_l = max(input_data.router_logits)
        exp_l = [math.exp(l - max_l) for l in input_data.router_logits]
        sum_exp = sum(exp_l)
        probs = [el / sum_exp for el in exp_l]
        
        num_experts = len(input_data.router_logits)
        capacity = math.ceil(input_data.tokens_per_batch * input_data.top_k * input_data.capacity_factor / num_experts)
        
        return MOEOutput(expert_capacity=capacity, routing_probs=probs)
