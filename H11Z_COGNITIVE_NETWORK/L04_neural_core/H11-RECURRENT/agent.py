"""
H11-RECURRENT: RNN Gating
LSTM continuous state update math.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-RECURRENT"

@dataclass
class RecurrentInput:
    forget_gate: float
    input_gate: float
    cell_candidate: float
    prev_cell: float

@dataclass
class RecurrentOutput:
    next_cell: float

class Agent:
    def process(self, input_data: RecurrentInput) -> RecurrentOutput:
        def sigmoid(x):
            return 1.0 / (1.0 + math.exp(-max(min(x, 20), -20)))
        def tanh(x):
            return math.tanh(x)
            
        f = sigmoid(input_data.forget_gate)
        i = sigmoid(input_data.input_gate)
        c_tilde = tanh(input_data.cell_candidate)
        
        next_c = f * input_data.prev_cell + i * c_tilde
        return RecurrentOutput(next_cell=next_c)
