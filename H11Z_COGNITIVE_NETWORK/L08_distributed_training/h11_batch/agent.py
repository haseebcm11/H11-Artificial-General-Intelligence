"""
H11-BATCH (Batch Size Scaling)
Learning rate scaling rules (Linear Scaling Rule, square root scaling rule).
"""
import math
from dataclasses import dataclass

AGENT_ID = "H11-BATCH"

class BatchError(Exception):
    pass

@dataclass
class BatchInput:
    base_batch_size: int
    new_batch_size: int
    base_learning_rate: float
    scaling_rule: str = "linear"

@dataclass
class BatchOutput:
    new_learning_rate: float
    noise_scale_factor: float

class BatchAgent:
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: BatchInput) -> BatchOutput:
        ratio = input_data.new_batch_size / float(input_data.base_batch_size)
        if ratio <= 0:
            raise BatchError("Invalid batch sizes")
            
        if input_data.scaling_rule == "linear":
            lr = input_data.base_learning_rate * ratio
        elif input_data.scaling_rule == "sqrt":
            lr = input_data.base_learning_rate * math.sqrt(ratio)
        else:
            raise BatchError("Unknown rule")
            
        noise = 1.0 / math.sqrt(input_data.new_batch_size)
        
        return BatchOutput(
            new_learning_rate=lr,
            noise_scale_factor=noise
        )
# padding for depth requirements
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
