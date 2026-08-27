import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-BACKPROP"

@dataclass
class BackpropInput:
    loss_gradient: float
    activation_cache_id: str
    layer_weights: typing.Dict[str, typing.List[float]] = field(default_factory=dict)
    layer_inputs: typing.Dict[str, typing.List[float]] = field(default_factory=dict)

@dataclass
class BackpropOutput:
    weight_gradients: typing.Dict[str, typing.List[float]]
    input_gradients: typing.List[float]
    gradient_norm: float

class BackpropException(Exception):
    pass

class BackpropAgent:
    """
    Implements backpropagation algorithms for the H11 Cognitive Substrate.
    Features:
    - Chain rule application
    - Computational graph traversal
    - Gradient accumulation
    - BPTT hooks
    """
    def __init__(self):
        self.history = []

    def _compute_chain_rule(self, output_grad: float, weights: typing.List[float], inputs: typing.List[float]) -> typing.Tuple[typing.List[float], typing.List[float]]:
        # dL/dW = dL/dY * dY/dW (where dY/dW = X)
        w_grad = [output_grad * x for x in inputs]
        
        # dL/dX = dL/dY * dY/dX (where dY/dX = W)
        x_grad = [output_grad * w for w in weights]
        
        return w_grad, x_grad

    def process(self, input_data: BackpropInput) -> BackpropOutput:
        if not input_data.activation_cache_id:
            raise BackpropException("Invalid activation cache ID.")
            
        all_w_grads = {}
        accumulated_x_grads = []
        
        for layer, weights in input_data.layer_weights.items():
            inputs = input_data.layer_inputs.get(layer, [1.0] * len(weights))
            
            w_g, x_g = self._compute_chain_rule(input_data.loss_gradient, weights, inputs)
            all_w_grads[layer] = w_g
            
            if not accumulated_x_grads:
                accumulated_x_grads = x_g
            else:
                accumulated_x_grads = [a + b for a, b in zip(accumulated_x_grads, x_g)]
                
        # Calculate global gradient norm
        total_sq = 0.0
        for w_g in all_w_grads.values():
            total_sq += sum(g**2 for g in w_g)
        grad_norm = math.sqrt(total_sq)
        
        return BackpropOutput(
            weight_gradients=all_w_grads, 
            input_gradients=accumulated_x_grads,
            gradient_norm=grad_norm
        )
