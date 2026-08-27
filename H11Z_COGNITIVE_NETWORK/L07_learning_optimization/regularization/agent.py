import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-REGULARIZATION"

@dataclass
class RegularizationInput:
    parameters: typing.Dict[str, typing.List[float]]
    l1_ratio: float = 0.01
    l2_ratio: float = 0.01
    elastic_net: bool = True

@dataclass
class RegularizationOutput:
    regularization_loss: float
    penalty_gradients: typing.Dict[str, typing.List[float]]

class RegularizationException(Exception):
    pass

class RegularizationAgent:
    """
    Implements L1/L2 and Elastic Net Regularization for the H11 Cognitive Substrate.
    Features:
    - L1 sparsity penalty
    - L2 weight decay
    - Combined Elastic Net
    """
    def __init__(self):
        pass

    def process(self, input_data: RegularizationInput) -> RegularizationOutput:
        if not input_data.parameters:
            raise RegularizationException("No parameters provided.")
            
        total_loss = 0.0
        reg_grads = {}
        
        l1 = input_data.l1_ratio
        l2 = input_data.l2_ratio
        
        for k, p_list in input_data.parameters.items():
            g_list = []
            for p in p_list:
                # L1 Loss: l1 * |p|
                # L2 Loss: l2 * p^2 (sometimes 0.5 * l2 * p^2)
                loss_val = l1 * abs(p) + 0.5 * l2 * (p ** 2)
                total_loss += loss_val
                
                # Gradient: l1 * sign(p) + l2 * p
                sign_p = 1.0 if p > 0 else (-1.0 if p < 0 else 0.0)
                grad = l1 * sign_p + l2 * p
                g_list.append(grad)
                
            reg_grads[k] = g_list
            
        return RegularizationOutput(
            regularization_loss=total_loss,
            penalty_gradients=reg_grads
        )
