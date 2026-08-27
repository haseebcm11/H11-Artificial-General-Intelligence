"""
H11-DECODER: Transformer Decoder
Implements masked self-attention logic for autoregressive generation.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-DECODER"

@dataclass
class DecoderInput:
    seq_length: int
    causal: bool = True

@dataclass
class DecoderOutput:
    attention_mask: list[list[float]]
    total_unmasked: int

class Agent:
    def process(self, input_data: DecoderInput) -> DecoderOutput:
        mask = []
        unmasked = 0
        for i in range(input_data.seq_length):
            row = []
            for j in range(input_data.seq_length):
                if input_data.causal and j > i:
                    row.append(float('-inf'))
                else:
                    row.append(0.0)
                    unmasked += 1
            mask.append(row)
        return DecoderOutput(attention_mask=mask, total_unmasked=unmasked)
