import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-LEARNINGRATE"

@dataclass
class LearningrateInput:
    current_step: int
    total_steps: int
    base_lr: float = 0.001
    warmup_ratio: float = 0.1
    min_lr: float = 1e-6
    schedule_type: str = "cosine"

@dataclass
class LearningrateOutput:
    current_learning_rate: float
    scheduler_state: typing.Dict[str, typing.Any]
    phase: str

class LearningrateException(Exception):
    pass

class LearningrateAgent:
    """
    Implements Learning Rate Schedules for the H11 Cognitive Substrate.
    Features:
    - Linear warmup
    - Cosine annealing
    - OneCycleLR / Linear decay
    """
    def __init__(self):
        self.last_lr = 0.0

    def process(self, input_data: LearningrateInput) -> LearningrateOutput:
        if input_data.total_steps <= 0:
            raise LearningrateException("Total steps must be > 0.")
            
        warmup_steps = int(input_data.total_steps * input_data.warmup_ratio)
        step = input_data.current_step
        
        if step < warmup_steps:
            # Linear warmup
            lr = input_data.base_lr * (step / max(1, warmup_steps))
            phase = "warmup"
        else:
            progress = (step - warmup_steps) / max(1, input_data.total_steps - warmup_steps)
            progress = min(1.0, max(0.0, progress))
            
            if input_data.schedule_type == "cosine":
                # Cosine annealing
                lr = input_data.min_lr + 0.5 * (input_data.base_lr - input_data.min_lr) * (1 + math.cos(math.pi * progress))
            elif input_data.schedule_type == "linear":
                # Linear decay
                lr = input_data.base_lr - (input_data.base_lr - input_data.min_lr) * progress
            else:
                lr = input_data.base_lr
                
            phase = "decay"
            
        self.last_lr = lr
        
        return LearningrateOutput(
            current_learning_rate=lr,
            scheduler_state={"step": step, "progress": progress if step >= warmup_steps else (step/warmup_steps)},
            phase=phase
        )
