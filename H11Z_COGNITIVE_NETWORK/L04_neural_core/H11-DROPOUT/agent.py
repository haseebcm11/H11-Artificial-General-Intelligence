"""
H11-DROPOUT: Dropout Layer
Inverted dropout scaling and variance preservation.
"""
from dataclasses import dataclass

AGENT_ID = "H11-DROPOUT"

@dataclass
class DropoutInput:
    prob: float
    features: list[float]
    training: bool = True

@dataclass
class DropoutOutput:
    scaled_features: list[float]
    expected_active: float

class Agent:
    def process(self, input_data: DropoutInput) -> DropoutOutput:
        if not input_data.training or input_data.prob == 0:
            return DropoutOutput(scaled_features=input_data.features, expected_active=len(input_data.features))
            
        scale = 1.0 / (1.0 - input_data.prob)
        expected_active = len(input_data.features) * (1.0 - input_data.prob)
        scaled = [f * scale * (1.0 - input_data.prob) for f in input_data.features]
        return DropoutOutput(scaled_features=scaled, expected_active=expected_active)
