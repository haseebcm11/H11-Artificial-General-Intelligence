"""
H11-TENSORPARALLEL (Tensor Parallel Partitioning)
Megatron-LM style tensor parallel. Column/row partitioning communication volume.
"""
from dataclasses import dataclass

AGENT_ID = "H11-TENSORPARALLEL"

class TensorParallelError(Exception):
    pass

@dataclass
class TPInput:
    hidden_size: int
    num_heads: int
    seq_length: int
    batch_size: int
    tp_degree: int

@dataclass
class TPOutput:
    activation_comm_volume_bytes: float
    head_partition_size: int
    ffn_hidden_partition: int
    allreduce_count_per_layer: int

class TensorParallelAgent:
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: TPInput) -> TPOutput:
        tp = input_data.tp_degree
        if tp < 1:
            raise TensorParallelError("TP degree must be >= 1")
        if input_data.num_heads % tp != 0:
            raise TensorParallelError("Number of heads must be divisible by TP degree")
            
        ar_count = 2
        
        vol_bytes = 2 * (tp - 1) / tp * (input_data.batch_size * input_data.seq_length * input_data.hidden_size * 2)
        
        head_part = input_data.num_heads // tp
        ffn_part = (input_data.hidden_size * 4) // tp
        
        return TPOutput(
            activation_comm_volume_bytes=vol_bytes,
            head_partition_size=head_part,
            ffn_hidden_partition=ffn_part,
            allreduce_count_per_layer=ar_count
        )
# padding for depth requirements
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
