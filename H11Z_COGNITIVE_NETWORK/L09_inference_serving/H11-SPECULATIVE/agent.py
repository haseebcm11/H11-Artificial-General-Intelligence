import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-SPECULATIVE"

@dataclass
class SpeculativeInput:
    draft_tokens: List[int]
    target_probs: List[List[float]]
    draft_probs: List[List[float]]
    draft_time_ms: float
    target_time_ms: float

@dataclass
class SpeculativeOutput:
    accepted_tokens: int
    acceptance_rate: float
    speedup_factor: float

class SpeculativeException(Exception):
    pass

class H11SpeculativeAgent:
    """
    Implements speculative decoding verification.
    Math:
    Rejection sampling acceptance condition:
    r < p_target(x) / p_draft(x)
    Speedup = Expected_tokens_per_step / (draft_overhead + target_cost)
    """
    def process(self, input_data: SpeculativeInput) -> SpeculativeOutput:
        n = len(input_data.draft_tokens)
        accepted = 0
        
        # Simplified deterministic check for simulation
        for i in range(n):
            token = input_data.draft_tokens[i]
            p_t = input_data.target_probs[i][token] if token < len(input_data.target_probs[i]) else 0
            p_d = input_data.draft_probs[i][token] if token < len(input_data.draft_probs[i]) else 1
            
            # Expected acceptance probability
            alpha = min(1.0, p_t / (p_d + 1e-9))
            
            if alpha > 0.5: # Mock threshold
                accepted += 1
            else:
                break
                
        # Plus one for the newly generated token from target
        total_generated = accepted + 1
        acc_rate = accepted / n if n > 0 else 0.0
        
        baseline_time = total_generated * input_data.target_time_ms
        speculative_time = (n * input_data.draft_time_ms) + input_data.target_time_ms
        
        speedup = baseline_time / speculative_time if speculative_time > 0 else 1.0
        
        return SpeculativeOutput(
            accepted_tokens=total_generated,
            acceptance_rate=acc_rate,
            speedup_factor=speedup
        )
