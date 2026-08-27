import math
from dataclasses import dataclass

AGENT_ID = "H11-CLUSTER"

@dataclass
class ClusterInput:
    num_nodes: int
    data_size_mb: float
    network_bandwidth_gbps: float
    network_latency_ms: float
    algorithm: str # "ring" or "tree"

@dataclass
class ClusterOutput:
    all_reduce_time_ms: float
    total_data_transferred_mb: float
    efficiency_factor: float

class ClusterException(Exception):
    pass

class ClusterAgent:
    """
    Computes all-reduce time for distributed clusters.
    Compares Ring All-Reduce vs Tree All-Reduce models.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: ClusterInput) -> ClusterOutput:
        if input_data.num_nodes <= 1:
            raise ClusterException("Cluster must have > 1 nodes for all-reduce.")
            
        N = input_data.num_nodes
        S = input_data.data_size_mb * 8e6 # bits
        BW = input_data.network_bandwidth_gbps * 1e9 # bits/s
        L = input_data.network_latency_ms
        
        algo = input_data.algorithm.lower()
        
        if algo == "ring":
            # Ring All-Reduce
            # 2 * (N-1) steps, data sent per step is S/N
            # Time = 2 * (N-1) * (L + (S/N) / BW)
            transfer_time_ms = (S / N) / BW * 1000.0
            total_time_ms = 2 * (N - 1) * (L + transfer_time_ms)
            data_tx_mb = 2 * (N - 1) * (input_data.data_size_mb / N)
            
        elif algo == "tree":
            # Tree All-Reduce
            # 2 * log2(N) steps, data sent per step is S
            steps = math.ceil(math.log2(N))
            transfer_time_ms = (S / BW) * 1000.0
            total_time_ms = 2 * steps * (L + transfer_time_ms)
            data_tx_mb = 2 * steps * input_data.data_size_mb
            
        else:
            raise ClusterException(f"Unknown algorithm: {algo}")
            
        # Ideal bandwidth bound time: 2 * S / BW
        ideal_time_ms = (2 * S / BW) * 1000.0
        efficiency = ideal_time_ms / total_time_ms if total_time_ms > 0 else 1.0
        
        return ClusterOutput(
            all_reduce_time_ms=total_time_ms,
            total_data_transferred_mb=data_tx_mb,
            efficiency_factor=efficiency
        )
