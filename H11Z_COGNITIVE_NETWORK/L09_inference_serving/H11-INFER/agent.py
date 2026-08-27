import math
from dataclasses import dataclass

AGENT_ID = "H11-INFER"

@dataclass
class InferInput:
    batch_size: int
    seq_len: int
    vocab_size: int
    hidden_size: int

@dataclass
class InferOutput:
    logits_flops: int
    memory_bandwidth_bytes: int

class InferException(Exception):
    pass

class H11InferAgent:
    """
    Base autoregressive inference engine calculations.
    Logits FLOPs = 2 * batch * seq_len * hidden * vocab
    """
    def process(self, input_data: InferInput) -> InferOutput:
        flops = 2 * input_data.batch_size * input_data.seq_len * input_data.hidden_size * input_data.vocab_size
        
        # Read hidden states and embedding weights
        bytes_read = (input_data.hidden_size * input_data.vocab_size + 
                     input_data.batch_size * input_data.seq_len * input_data.hidden_size) * 2 # FP16
                     
        return InferOutput(
            logits_flops=flops,
            memory_bandwidth_bytes=bytes_read
        )
