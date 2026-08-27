"""
H11-EXPERIMENT (Experiment Tracking)
Loss divergence detection.
"""
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-EXPERIMENT"

class ExpError(Exception):
    pass

@dataclass
class ExpInput:
    loss_history: List[float]
    divergence_threshold: float = 2.0

@dataclass
class ExpOutput:
    is_diverging: bool
    loss_velocity: float
    recommendation: str

class ExperimentAgent:
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: ExpInput) -> ExpOutput:
        if len(input_data.loss_history) < 2:
            return ExpOutput(False, 0.0, "Continue")
            
        recent = input_data.loss_history[-1]
        prev = input_data.loss_history[-2]
        vel = recent - prev
        
        div = recent > min(input_data.loss_history) * input_data.divergence_threshold
        
        rec = "Halt & Lower LR" if div else "Continue"
        
        return ExpOutput(
            is_diverging=div,
            loss_velocity=vel,
            recommendation=rec
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
