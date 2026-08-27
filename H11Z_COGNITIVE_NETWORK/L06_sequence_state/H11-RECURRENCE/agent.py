import math
from dataclasses import dataclass
from typing import List, Dict, Optional

AGENT_ID = "H11-RECURRENCE"

class RecurrenceExplosionError(Exception):
    """Raised when gradient explosion is detected in RNN."""
    pass

@dataclass
class RecurrenceInput:
    sequential_input: List[List[float]]
    reset_state: bool
    detach_gradients: bool
    w_h: float = 0.8
    w_x: float = 0.5
    b: float = -0.1

@dataclass
class RecurrenceOutput:
    hidden_activations: List[List[float]]
    state_snapshot: Dict[str, List[float]]
    gradient_norm: float
    vanishing_warning: bool

class RecurrenceAgent:
    """
    Implements standard RNN non-linear transitions: h_t = tanh(W_h*h_{t-1} + W_x*x_t + b)
    Includes simulated gradient tracking for vanishing gradient analysis (TBPTT approximation).
    """
    def __init__(self):
        self.state_h: List[float] = []

    def process(self, req: RecurrenceInput) -> RecurrenceOutput:
        if not req.sequential_input:
            raise ValueError("Empty sequence")
        
        seq_len = len(req.sequential_input)
        dim = len(req.sequential_input[0])
        
        if req.reset_state or not self.state_h:
            self.state_h = [0.0 for _ in range(dim)]
            
        activations = []
        grad_norm = 1.0
        
        for t in range(seq_len):
            x_t = req.sequential_input[t]
            h_t = []
            jacobian_norm = 0.0
            
            for i in range(dim):
                z = req.w_h * self.state_h[i] + req.w_x * x_t[i] + req.b
                val = math.tanh(z)
                h_t.append(val)
                dz = 1.0 - val**2
                jacobian_norm += abs(req.w_h * dz)
            
            jacobian_norm /= dim
            grad_norm *= jacobian_norm
            self.state_h = h_t
            activations.append(h_t)
            
            if grad_norm > 1e4:
                raise RecurrenceExplosionError("Gradient explosion detected.")
            
        if req.detach_gradients:
            grad_norm = 1.0
            
        return RecurrenceOutput(
            hidden_activations=activations,
            state_snapshot={"h_T": self.state_h.copy()},
            gradient_norm=grad_norm,
            vanishing_warning=grad_norm < 1e-4
        )
