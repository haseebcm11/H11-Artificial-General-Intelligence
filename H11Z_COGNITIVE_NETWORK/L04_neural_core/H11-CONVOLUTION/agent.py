"""
H11-CONVOLUTION: Convolutional Math
Calculates exact output dimensions and receptive fields.
"""
from dataclasses import dataclass

AGENT_ID = "H11-CONVOLUTION"

@dataclass
class ConvInput:
    in_size: int
    kernel_size: int
    stride: int
    padding: int
    dilation: int = 1

@dataclass
class ConvOutput:
    out_size: int
    receptive_field: int

class Agent:
    def process(self, input_data: ConvInput) -> ConvOutput:
        effective_k = (input_data.kernel_size - 1) * input_data.dilation + 1
        out_size = (input_data.in_size + 2 * input_data.padding - effective_k) // input_data.stride + 1
        
        # Base receptive field calculation
        receptive_field = effective_k
        return ConvOutput(out_size=out_size, receptive_field=receptive_field)
