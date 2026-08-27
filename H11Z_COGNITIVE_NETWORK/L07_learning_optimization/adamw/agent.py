import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-ADAMW"

@dataclass
class AdamwInput:
    gradients: typing.Dict[str, typing.List[float]]
    beta1: float
    beta2: float
    learning_rate: float = 0.001
    weight_decay: float = 0.01
    eps: float = 1e-8
    step: int = 1
    current_weights: typing.Optional[typing.Dict[str, typing.List[float]]] = None

@dataclass
class AdamwOutput:
    weight_updates: typing.Dict[str, typing.List[float]]
    moment_states: typing.Dict[str, float]
    v_states: typing.Dict[str, float]

class AdamwException(Exception):
    pass

class AdamwAgent:
    """
    Implements AdamW optimization algorithm for the H11 Cognitive Substrate.
    Features:
    - Decoupled weight decay
    - First/second moment estimation
    - Bias correction
    - Stability epsilon
    """
    def __init__(self):
        self.m_state = {}
        self.v_state = {}

    def _initialize_states(self, params: typing.List[str], size: int):
        for p in params:
            if p not in self.m_state:
                self.m_state[p] = [0.0] * size
            if p not in self.v_state:
                self.v_state[p] = [0.0] * size

    def _compute_bias_correction(self, m: float, v: float, beta1: float, beta2: float, step: int) -> typing.Tuple[float, float]:
        m_hat = m / (1 - beta1 ** step)
        v_hat = v / (1 - beta2 ** step)
        return m_hat, v_hat

    def process(self, input_data: AdamwInput) -> AdamwOutput:
        if not input_data.gradients:
            raise AdamwException("No gradients provided for AdamW update.")
            
        updates = {}
        out_m_states = {}
        out_v_states = {}
        
        for param, grad in input_data.gradients.items():
            self._initialize_states([param], len(grad))
            param_updates = []
            
            for i, g in enumerate(grad):
                # Update biased first moment estimate
                self.m_state[param][i] = input_data.beta1 * self.m_state[param][i] + (1 - input_data.beta1) * g
                # Update biased second raw moment estimate
                self.v_state[param][i] = input_data.beta2 * self.v_state[param][i] + (1 - input_data.beta2) * (g ** 2)
                
                # Compute bias-corrected estimates
                m_hat, v_hat = self._compute_bias_correction(
                    self.m_state[param][i], 
                    self.v_state[param][i], 
                    input_data.beta1, 
                    input_data.beta2, 
                    input_data.step
                )
                
                # Decoupled weight decay
                w = input_data.current_weights[param][i] if input_data.current_weights and param in input_data.current_weights else 0.0
                decay_term = input_data.weight_decay * w
                
                # Compute update
                update = -input_data.learning_rate * (m_hat / (math.sqrt(v_hat) + input_data.eps) + decay_term)
                param_updates.append(update)
                
            updates[param] = param_updates
            out_m_states[param] = sum(self.m_state[param]) / len(self.m_state[param])
            out_v_states[param] = sum(self.v_state[param]) / len(self.v_state[param])
            
        return AdamwOutput(weight_updates=updates, moment_states=out_m_states, v_states=out_v_states)
