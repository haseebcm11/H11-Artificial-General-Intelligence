import math
from dataclasses import dataclass

AGENT_ID = "H11-KV-OPT"

@dataclass
class KVOptInput:
    num_layers: int
    num_heads: int
    head_dim: int
    seq_len: int
    batch_size: int
    dtype_bytes: int

@dataclass
class KVOptOutput:
    total_kv_memory_bytes: int
    blocks_needed: int
    block_size_tokens: int = 16

class KVOptException(Exception):
    pass

class H11KvOptAgent:
    """
    Calculates KV Cache memory footprint.
    Math:
    Memory = 2 (K & V) * layers * heads * head_dim * seq_len * batch * bytes_per_elem
    Blocks = ceil(seq_len / block_size) * batch
    """
    def process(self, input_data: KVOptInput) -> KVOptOutput:
        # 2 is for Key and Value
        memory = (
            2 * 
            input_data.num_layers * 
            input_data.num_heads * 
            input_data.head_dim * 
            input_data.seq_len * 
            input_data.batch_size * 
            input_data.dtype_bytes
        )
        
        block_size = 16
        blocks = math.ceil(input_data.seq_len / block_size) * input_data.batch_size
        
        return KVOptOutput(
            total_kv_memory_bytes=memory,
            blocks_needed=blocks,
            block_size_tokens=block_size
        )
