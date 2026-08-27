import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-GRADIENT"

@dataclass
class GradientInput:
    mini_batch_gradients: typing.Dict[str, typing.List[float]]
    accumulation_steps: int = 1
    current_step: int = 1
    zero_grad: bool = False

@dataclass
class GradientOutput:
    accumulated_gradients: typing.Dict[str, typing.List[float]]
    is_update_step: bool
    effective_batch_multiplier: int

class GradientException(Exception):
    pass

class GradientAgent:
    """
    Implements gradient accumulation and moving averages for the H11 Cognitive Substrate.
    Features:
    - Micro-batch accumulation
    - Step tracking
    - Gradient zeroing
    """
    def __init__(self):
        self.buffer = {}
        self.steps_accumulated = 0

    def process(self, input_data: GradientInput) -> GradientOutput:
        if input_data.zero_grad:
            self.buffer = {}
            self.steps_accumulated = 0
            
        if not input_data.mini_batch_gradients:
            return GradientOutput(self.buffer, False, self.steps_accumulated)
            
        # Accumulate
        for k, g_list in input_data.mini_batch_gradients.items():
            if k not in self.buffer:
                self.buffer[k] = [0.0] * len(g_list)
            for i, g in enumerate(g_list):
                # Scale by accumulation steps to maintain expected loss magnitude
                self.buffer[k][i] += g / input_data.accumulation_steps
                
        self.steps_accumulated += 1
        
        is_update = False
        out_grads = {}
        if self.steps_accumulated >= input_data.accumulation_steps:
            is_update = True
            out_grads = {k: list(v) for k, v in self.buffer.items()}
            # Reset happens on next call if zero_grad is true, or we can auto-reset
            self.buffer = {}
            self.steps_accumulated = 0
            
        return GradientOutput(
            accumulated_gradients=out_grads,
            is_update_step=is_update,
            effective_batch_multiplier=input_data.accumulation_steps
        )
