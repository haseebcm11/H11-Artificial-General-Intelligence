import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-FINETUNE"

@dataclass
class FinetuneInput:
    base_learning_rate: float
    layers: typing.List[str]
    layer_decay: float = 0.95
    freeze_bottom_n: int = 2
    task_adaptation_factor: float = 1.0

@dataclass
class FinetuneOutput:
    layer_learning_rates: typing.Dict[str, float]
    frozen_parameters: typing.List[str]
    effective_capacity: float

class FinetuneException(Exception):
    pass

class FinetuneAgent:
    """
    Implements Fine-Tuning strategies for the H11 Cognitive Substrate.
    Features:
    - Layer-wise learning rate decay
    - Parameter freezing
    - Capacity modulation
    """
    def __init__(self):
        self.state = "initialized"

    def process(self, input_data: FinetuneInput) -> FinetuneOutput:
        if not input_data.layers:
            raise FinetuneException("No layers provided for finetuning.")
            
        lrs = {}
        frozen = []
        
        total_layers = len(input_data.layers)
        
        for i, layer in enumerate(input_data.layers):
            if i < input_data.freeze_bottom_n:
                frozen.append(layer)
                lrs[layer] = 0.0
            else:
                # Layer-wise decay (depth from top)
                depth_from_top = total_layers - i - 1
                decay_factor = input_data.layer_decay ** depth_from_top
                lrs[layer] = input_data.base_learning_rate * decay_factor * input_data.task_adaptation_factor
                
        active_layers = total_layers - len(frozen)
        capacity = active_layers / max(1, total_layers) * 100.0
        
        return FinetuneOutput(
            layer_learning_rates=lrs,
            frozen_parameters=frozen,
            effective_capacity=capacity
        )
