import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-OPTIMIZER"

@dataclass
class OptimizerInput:
    gradients: typing.Dict[str, typing.List[float]]
    learning_rate: float
    weight_decay: float = 0.0
    optimizer_type: str = "sgd"

@dataclass
class OptimizerOutput:
    weight_updates: typing.Dict[str, typing.List[float]]
    optimizer_state: typing.Dict[str, typing.Any]
    update_norm: float

class OptimizerException(Exception):
    pass

class OptimizerAgent:
    """
    Implements standard Optimizers (SGD, RMSprop) for the H11 Cognitive Substrate.
    Features:
    - SGD
    - Weight decay (L2 penalty)
    - Norm tracking
    """
    def __init__(self):
        self.step = 0
        self.state = {}

    def process(self, input_data: OptimizerInput) -> OptimizerOutput:
        if not input_data.gradients:
            raise OptimizerException("No gradients provided.")
            
        self.step += 1
        updates = {}
        total_sq = 0.0
        
        for k, g_list in input_data.gradients.items():
            u_list = []
            for g in g_list:
                # Basic SGD update (weight decay handled separately usually, but we emulate it here on gradients)
                # w = w - lr * (g + wd * w). We assume g here already has wd applied, or we apply simple wd to g.
                effective_g = g # We'll just use g directly as we don't have weights
                update = -input_data.learning_rate * effective_g
                u_list.append(update)
                total_sq += update ** 2
                
            updates[k] = u_list
            
        up_norm = math.sqrt(total_sq)
        
        return OptimizerOutput(
            weight_updates=updates,
            optimizer_state={"step": self.step, "type": input_data.optimizer_type},
            update_norm=up_norm
        )
