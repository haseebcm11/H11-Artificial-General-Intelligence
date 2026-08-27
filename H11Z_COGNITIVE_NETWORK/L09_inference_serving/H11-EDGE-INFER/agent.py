import math
from dataclasses import dataclass

AGENT_ID = "H11-EDGE-INFER"

@dataclass
class EdgeInput:
    original_nodes: int
    fused_nodes: int
    fp32_memory_mb: float

@dataclass
class EdgeOutput:
    optimization_ratio: float
    int8_memory_mb: float

class EdgeException(Exception):
    pass

class H11EdgeInferAgent:
    """
    Graph optimization passes for Edge inference.
    Estimates memory savings for INT8 vs FP32.
    """
    def process(self, input_data: EdgeInput) -> EdgeOutput:
        if input_data.original_nodes <= 0:
            raise EdgeException("Invalid graph size")
            
        opt_ratio = (input_data.original_nodes - input_data.fused_nodes) / input_data.original_nodes
        
        # INT8 takes roughly 1/4 the memory of FP32
        int8_mem = input_data.fp32_memory_mb * 0.25
        
        return EdgeOutput(
            optimization_ratio=opt_ratio,
            int8_memory_mb=int8_mem
        )
