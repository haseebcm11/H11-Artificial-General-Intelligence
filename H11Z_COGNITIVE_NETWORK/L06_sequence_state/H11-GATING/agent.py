import math
from dataclasses import dataclass
from typing import List, Optional

AGENT_ID = "H11-GATING"

class GatingSaturationError(Exception):
    """Raised when gates are saturated."""
    pass

@dataclass
class GatingInput:
    primary_features: List[float]
    gating_signals: List[float]
    gate_type: str  # 'lstm', 'swiglu'

@dataclass
class GatingOutput:
    modulated_output: List[float]
    gate_activations: List[float]
    cell_state: Optional[List[float]] = None

class GatingAgent:
    """
    Computes rigorous gating mechanics.
    LSTM: C_t = f_t*C_{t-1} + i_t*tanh(W_c*[h,x]+b_c)
    SwiGLU: x * (x * sigmoid(beta * x))
    """
    def __init__(self):
        self.c_t: List[float] = []
        
    def _sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + math.exp(-max(min(x, 20.0), -20.0)))
        
    def process(self, req: GatingInput) -> GatingOutput:
        dim = len(req.primary_features)
        
        if req.gate_type == "lstm":
            if not self.c_t or len(self.c_t) != dim:
                self.c_t = [0.0] * dim
            f_t = [self._sigmoid(g) for g in req.gating_signals[0:dim]]
            i_t = [self._sigmoid(g) for g in req.gating_signals[dim:2*dim]]
            o_t = [self._sigmoid(g) for g in req.gating_signals[2*dim:3*dim]]
            g_t = [math.tanh(g) for g in req.gating_signals[3*dim:4*dim]]
            
            modulated = []
            for j in range(dim):
                self.c_t[j] = f_t[j] * self.c_t[j] + i_t[j] * g_t[j]
                h_t = o_t[j] * math.tanh(self.c_t[j])
                modulated.append(h_t)
            return GatingOutput(modulated_output=modulated, gate_activations=f_t, cell_state=self.c_t.copy())
            
        elif req.gate_type == "swiglu":
            modulated = []
            gates = []
            for x, g in zip(req.primary_features, req.gating_signals):
                swish = g * self._sigmoid(g)
                modulated.append(x * swish)
                gates.append(swish)
            return GatingOutput(modulated_output=modulated, gate_activations=gates)
            
        raise ValueError(f"Unknown gate_type: {req.gate_type}")
