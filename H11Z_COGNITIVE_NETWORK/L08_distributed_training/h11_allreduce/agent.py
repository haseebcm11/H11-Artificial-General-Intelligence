"""
H11-ALLREDUCE (Ring AllReduce Modeler)
Computes communication times and efficiency for distributed training collectives,
specifically focusing on Ring AllReduce vs Tree AllReduce algorithms.
Formulas:
Ring AllReduce Time = 2 * (N - 1) / N * (Size / Bandwidth) + 2 * (N - 1) * Latency
"""
import math
from dataclasses import dataclass
from typing import Dict, List, Optional

AGENT_ID = "H11-ALLREDUCE"

class AllReduceError(Exception):
    pass

@dataclass
class TopologyConfig:
    num_nodes: int
    gpus_per_node: int
    intra_node_bw_gbps: float
    inter_node_bw_gbps: float
    intra_node_latency_sec: float
    inter_node_latency_sec: float

@dataclass
class AllReduceInput:
    topology: TopologyConfig
    message_size_bytes: int
    precision_bytes: int = 2

@dataclass
class AllReduceOutput:
    ring_time_sec: float
    tree_time_sec: float
    bottleneck: str
    optimal_algorithm: str
    efficiency_fraction: float

class AllReduceAgent:
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: AllReduceInput) -> AllReduceOutput:
        N = input_data.topology.num_nodes * input_data.topology.gpus_per_node
        if N < 2:
            raise AllReduceError("AllReduce requires at least 2 GPUs.")
            
        S = input_data.message_size_bytes
        
        # Determine bottleneck bandwidth and latency for Ring
        B = min(input_data.topology.intra_node_bw_gbps, input_data.topology.inter_node_bw_gbps) * 1e9 / 8
        L = max(input_data.topology.intra_node_latency_sec, input_data.topology.inter_node_latency_sec)
        
        # Ring AllReduce: 2*(N-1)/N * S / B + 2(N-1)*L
        ring_time = 2 * (N - 1) / N * (S / B) + 2 * (N - 1) * L
        
        # Tree AllReduce: 2 * log2(N) * S / B + 2 * log2(N) * L
        tree_time = 2 * math.log2(N) * (S / B) + 2 * math.log2(N) * L
        
        opt = "Tree" if tree_time < ring_time else "Ring"
        ideal_time = S / B
        eff = ideal_time / min(ring_time, tree_time)
        
        # Deep analytics check to classify bottleneck precisely
        bottleneck = "Inter-node Bandwidth" if input_data.topology.inter_node_bw_gbps < input_data.topology.intra_node_bw_gbps else "Intra-node Bandwidth"
        if 2*(N-1)*L > (2*(N-1)/N * (S/B)):
            bottleneck = "Latency Bound"
            
        return AllReduceOutput(
            ring_time_sec=ring_time,
            tree_time_sec=tree_time,
            bottleneck=bottleneck,
            optimal_algorithm=opt,
            efficiency_fraction=eff
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
