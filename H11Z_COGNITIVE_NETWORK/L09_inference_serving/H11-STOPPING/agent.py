import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-STOPPING"

@dataclass
class StoppingInput:
    current_length: int
    max_length: int
    eos_prob: float
    eos_threshold: float

@dataclass
class StoppingOutput:
    should_stop: bool
    reason: str

class StoppingException(Exception):
    pass

class H11StoppingAgent:
    """
    Evaluates early stopping criteria.
    """
    def process(self, input_data: StoppingInput) -> StoppingOutput:
        if input_data.current_length >= input_data.max_length:
            return StoppingOutput(True, "max_length_reached")
            
        if input_data.eos_prob >= input_data.eos_threshold:
            return StoppingOutput(True, "eos_threshold_met")
            
        return StoppingOutput(False, "continue")
