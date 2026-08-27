import math
from dataclasses import dataclass

AGENT_ID = "H11-INTERCONNECT"

@dataclass
class InterconnectInput:
    topology: str  # "mesh", "torus", "fat-tree"
    num_nodes: int
    link_bandwidth_gbps: float
    link_latency_ns: float
    radix: int = 4

@dataclass
class InterconnectOutput:
    bisection_bandwidth_gbps: float
    average_hop_count: float
    worst_case_latency_ns: float

class InterconnectException(Exception):
    pass

class InterconnectAgent:
    """
    Computes interconnect bisection bandwidth and hop latency for various topologies.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: InterconnectInput) -> InterconnectOutput:
        N = input_data.num_nodes
        if N <= 1:
            raise InterconnectException("Number of nodes must be > 1")
            
        topo = input_data.topology.lower()
        
        if topo == "mesh":
            # 2D Mesh
            side = math.sqrt(N)
            bisect_links = side
            avg_hops = (2 * side) / 3
            max_hops = 2 * (side - 1)
        elif topo == "torus":
            # 2D Torus
            side = math.sqrt(N)
            bisect_links = 2 * side
            avg_hops = side / 2
            max_hops = side
        elif topo == "fat-tree":
            # K-ary N-tree (Fat Tree) approximation
            bisect_links = N / 2
            # Height of tree = log_k(N)
            # hops up and down
            try:
                height = math.ceil(math.log(N, input_data.radix))
            except ValueError:
                height = 1
            avg_hops = 2 * height - 1 # rough approx
            max_hops = 2 * height
        else:
            raise InterconnectException(f"Unknown topology: {topo}")
            
        bisection_bw = bisect_links * input_data.link_bandwidth_gbps
        worst_latency = max_hops * input_data.link_latency_ns
        
        return InterconnectOutput(
            bisection_bandwidth_gbps=bisection_bw,
            average_hop_count=avg_hops,
            worst_case_latency_ns=worst_latency
        )
