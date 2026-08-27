import math
from dataclasses import dataclass

AGENT_ID = "H11-NEUROMORPHIC"

@dataclass
class NeuromorphicInput:
    pre_spike_time_ms: float
    post_spike_time_ms: float
    tau_plus_ms: float = 20.0
    tau_minus_ms: float = 20.0
    a_plus: float = 0.01
    a_minus: float = 0.012
    current_weight: float = 0.5

@dataclass
class NeuromorphicOutput:
    delta_t_ms: float
    weight_change: float
    new_weight: float

class NeuromorphicException(Exception):
    pass

class NeuromorphicAgent:
    """
    Computes Spike-Timing-Dependent Plasticity (STDP) for Neuromorphic hardware.
    Formula: 
    if delta_t > 0: delta_w = A+ * exp(-delta_t / tau+)
    if delta_t <= 0: delta_w = -A- * exp(delta_t / tau-)
    where delta_t = t_post - t_pre
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: NeuromorphicInput) -> NeuromorphicOutput:
        delta_t = input_data.post_spike_time_ms - input_data.pre_spike_time_ms
        
        if delta_t > 0:
            # Long-Term Potentiation (LTP)
            delta_w = input_data.a_plus * math.exp(-delta_t / input_data.tau_plus_ms)
        else:
            # Long-Term Depression (LTD)
            # delta_t is <= 0, so we use its true value directly in the exponent 
            # to make it decay as delta_t becomes more negative
            delta_w = -input_data.a_minus * math.exp(delta_t / input_data.tau_minus_ms)
            
        new_w = input_data.current_weight + delta_w
        
        # Clamp weight to [0, 1] range typically used in simulations
        new_w = max(0.0, min(1.0, new_w))
        
        return NeuromorphicOutput(
            delta_t_ms=delta_t,
            weight_change=delta_w,
            new_weight=new_w
        )
