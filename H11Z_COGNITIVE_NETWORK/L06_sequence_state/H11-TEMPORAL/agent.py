from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-TEMPORAL"

class TemporalInstabilityError(Exception):
    """Raised when invalid temporal sequences are encountered."""
    pass

@dataclass
class TemporalInput:
    sequence: List[float]
    kernel_size: int = 2
    num_layers: int = 4

@dataclass
class TemporalOutput:
    conv_output: List[float]
    receptive_field: int

class TemporalAgent:
    """
    Temporal causal convolution with dilations.
    receptive field = sum(2^i * (k-1)) + 1
    """
    def process(self, req: TemporalInput) -> TemporalOutput:
        seq_len = len(req.sequence)
        if seq_len == 0:
            raise TemporalInstabilityError("Empty sequence provided")
            
        rf = 1
        for i in range(req.num_layers):
            rf += (2**i) * (req.kernel_size - 1)
            
        current_seq = req.sequence.copy()
        
        for i in range(req.num_layers):
            dilation = 2**i
            next_seq = []
            for t in range(seq_len):
                val = 0.0
                for k in range(req.kernel_size):
                    idx = t - k * dilation
                    if idx >= 0:
                        val += current_seq[idx] / req.kernel_size
                next_seq.append(val)
            current_seq = next_seq
            
        return TemporalOutput(
            conv_output=current_seq,
            receptive_field=rf
        )
