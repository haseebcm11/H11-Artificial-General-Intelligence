import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-FORWARD"

@dataclass
class ForwardInput:
    input_tensor: typing.List[float]
    weights: typing.List[typing.List[float]]
    biases: typing.List[float]
    activation_fn: str = "relu"
    layer_name: str = "hidden_0"

@dataclass
class ForwardOutput:
    output_activations: typing.List[float]
    forward_cache_id: str
    activation_statistics: typing.Dict[str, float]

class ForwardException(Exception):
    pass

class ForwardAgent:
    """
    Implements Forward Pass execution for the H11 Cognitive Substrate.
    Features:
    - Matrix multiplication
    - Activation functions
    - Activation statistics (mean/var)
    """
    def __init__(self):
        self.call_count = 0

    def _relu(self, x: float) -> float:
        return max(0.0, x)
        
    def _gelu(self, x: float) -> float:
        # GELU approximation: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
        return 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)))

    def process(self, input_data: ForwardInput) -> ForwardOutput:
        if not input_data.input_tensor or not input_data.weights:
            raise ForwardException("Inputs or weights missing.")
            
        outputs = []
        for i, row in enumerate(input_data.weights):
            dot_prod = sum(x * w for x, w in zip(input_data.input_tensor, row))
            dot_prod += input_data.biases[i] if i < len(input_data.biases) else 0.0
            
            if input_data.activation_fn == "relu":
                out = self._relu(dot_prod)
            elif input_data.activation_fn == "gelu":
                out = self._gelu(dot_prod)
            else:
                out = dot_prod
                
            outputs.append(out)
            
        mean = sum(outputs) / len(outputs)
        var = sum((x - mean)**2 for x in outputs) / len(outputs)
        
        self.call_count += 1
        cache_id = f"cache_{input_data.layer_name}_{self.call_count}"
        
        return ForwardOutput(
            output_activations=outputs,
            forward_cache_id=cache_id,
            activation_statistics={"mean": mean, "variance": var}
        )
