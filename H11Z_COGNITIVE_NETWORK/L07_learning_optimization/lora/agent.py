import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-LORA"

@dataclass
class LoraInput:
    base_weight_shape: typing.Tuple[int, int]
    rank: int = 8
    alpha: float = 16.0
    dropout: float = 0.05
    init_type: str = "normal"

@dataclass
class LoraOutput:
    a_matrix: typing.List[typing.List[float]]
    b_matrix: typing.List[typing.List[float]]
    scaling_factor: float
    trainable_params: int

class LoraException(Exception):
    pass

class LoraAgent:
    """
    Implements Low-Rank Adaptation (LoRA) mechanisms for the H11 Cognitive Substrate.
    Features:
    - Rank-decomposition matrices A and B
    - Alpha scaling
    - Parameter count tracking
    """
    def __init__(self):
        import random
        self.rng = random.Random(42)

    def _init_normal(self, rows: int, cols: int, std: float = 0.02) -> typing.List[typing.List[float]]:
        # Box-Muller transform for normal distribution
        matrix = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                u1 = self.rng.random()
                u2 = self.rng.random()
                z0 = math.sqrt(-2.0 * math.log(max(1e-9, u1))) * math.cos(2.0 * math.pi * u2)
                row.append(z0 * std)
            matrix.append(row)
        return matrix

    def process(self, input_data: LoraInput) -> LoraOutput:
        in_features, out_features = input_data.base_weight_shape
        r = input_data.rank
        
        if r <= 0:
            raise LoraException("LoRA rank must be positive.")
            
        # B is initialized to zero
        b_matrix = [[0.0] * r for _ in range(out_features)]
        
        # A is initialized with normal distribution
        a_matrix = self._init_normal(r, in_features, std=1.0/math.sqrt(in_features))
        
        scaling = input_data.alpha / r
        
        num_params = (in_features * r) + (r * out_features)
        
        return LoraOutput(
            a_matrix=a_matrix,
            b_matrix=b_matrix,
            scaling_factor=scaling,
            trainable_params=num_params
        )
