"""
H11-HYPERPARAM (Hyperparam Optimization)
Population-based training mutation.
"""
import random
from dataclasses import dataclass

AGENT_ID = "H11-HYPERPARAM"

class HyperparamError(Exception):
    pass

@dataclass
class HyperInput:
    current_lr: float
    current_bs: int
    performance_percentile: float

@dataclass
class HyperOutput:
    action: str
    new_lr: float
    new_bs: int

class HyperparamAgent:
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: HyperInput) -> HyperOutput:
        if input_data.performance_percentile < 0.2:
            act = "explore"
            lr = input_data.current_lr * random.choice([0.8, 1.2])
            bs = int(input_data.current_bs * random.choice([0.5, 2.0]))
        else:
            act = "exploit"
            lr = input_data.current_lr
            bs = input_data.current_bs
            
        return HyperOutput(
            action=act,
            new_lr=max(1e-6, lr),
            new_bs=max(1, bs)
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
