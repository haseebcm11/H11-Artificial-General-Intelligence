import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-SSM-CORE"

class SSMDiscretizationError(Exception):
    """Raised when NaN propagation occurs during discretization."""
    pass

@dataclass
class SSMInput:
    sequence: List[float]
    dt: float = 0.01
    n_dim: int = 16

@dataclass
class SSMOutput:
    ssm_outputs: List[float]
    final_state: List[float]
    a_bar_diag: List[float]

class SSMCoreAgent:
    """
    Continuous-time SSM discretization using Zero-Order Hold.
    A_bar = exp(dt * A)
    Utilizes simplified diagonal HiPPO matrix approximation.
    """
    def process(self, req: SSMInput) -> SSMOutput:
        A_diag = [- (i ** 0.5) for i in range(1, req.n_dim + 1)]
        B = [math.sqrt(2 * i + 1) for i in range(req.n_dim)]
        C = [1.0 / (i + 1) for i in range(req.n_dim)]
        
        try:
            A_bar = [math.exp(req.dt * a) for a in A_diag]
        except OverflowError:
            raise SSMDiscretizationError("dt projection overflow")
            
        B_bar = []
        for i in range(req.n_dim):
            if abs(A_diag[i]) > 1e-6:
                val = (A_bar[i] - 1.0) / A_diag[i] * B[i]
            else:
                val = req.dt * B[i]
            B_bar.append(val)
            
        state = [0.0] * req.n_dim
        outputs = []
        
        for x in req.sequence:
            y = 0.0
            for i in range(req.n_dim):
                state[i] = A_bar[i] * state[i] + B_bar[i] * x
                y += C[i] * state[i]
            outputs.append(y)
            
        return SSMOutput(
            ssm_outputs=outputs,
            final_state=state,
            a_bar_diag=A_bar
        )
