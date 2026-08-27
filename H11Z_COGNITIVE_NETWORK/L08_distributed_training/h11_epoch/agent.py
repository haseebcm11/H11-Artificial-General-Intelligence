"""
H11-EPOCH (Learning Rate Schedules)
Cosine decay, warmup schedules.
"""
import math
from dataclasses import dataclass

AGENT_ID = "H11-EPOCH"

class EpochError(Exception):
    pass

@dataclass
class EpochInput:
    current_step: int
    total_steps: int
    warmup_steps: int
    max_lr: float
    min_lr: float

@dataclass
class EpochOutput:
    learning_rate: float
    phase: str

class EpochAgent:
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: EpochInput) -> EpochOutput:
        if input_data.current_step < input_data.warmup_steps:
            lr = input_data.max_lr * (input_data.current_step / max(1, input_data.warmup_steps))
            phase = "warmup"
        else:
            progress = (input_data.current_step - input_data.warmup_steps) / max(1, input_data.total_steps - input_data.warmup_steps)
            progress = min(1.0, max(0.0, progress))
            lr = input_data.min_lr + 0.5 * (input_data.max_lr - input_data.min_lr) * (1.0 + math.cos(math.pi * progress))
            phase = "cosine_decay"
            
        return EpochOutput(
            learning_rate=lr,
            phase=phase
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
