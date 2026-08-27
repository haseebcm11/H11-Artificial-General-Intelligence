from dataclasses import dataclass

AGENT_ID = "H11_EDGE_COMPUTE"

@dataclass
class EdgeComputeInput:
    local_compute_time_ms: float
    cloud_compute_time_ms: float
    data_size_kb: float
    uplink_bandwidth_mbps: float
    downlink_bandwidth_mbps: float
    network_latency_ms: float
    local_power_w: float
    transmission_power_w: float

@dataclass
class EdgeComputeOutput:
    offload_decision: bool
    total_latency_ms: float
    energy_consumed_mj: float

class EdgeComputeException(Exception):
    pass

class EdgeComputeAgent:
    """
    Computes offloading decision for edge compute based on latency and energy constraints.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: EdgeComputeInput) -> EdgeComputeOutput:
        # Local execution costs
        local_latency = input_data.local_compute_time_ms
        local_energy = input_data.local_power_w * (local_latency / 1000.0) * 1000.0 # mJ
        
        # Cloud offloading costs
        tx_time_ms = (input_data.data_size_kb * 8) / (input_data.uplink_bandwidth_mbps * 1000) * 1000
        rx_time_ms = (input_data.data_size_kb * 8 * 0.1) / (input_data.downlink_bandwidth_mbps * 1000) * 1000 # assume 10% response size
        
        cloud_latency = tx_time_ms + input_data.cloud_compute_time_ms + rx_time_ms + (2 * input_data.network_latency_ms)
        cloud_energy = input_data.transmission_power_w * (tx_time_ms + rx_time_ms) / 1000.0 * 1000.0 # mJ
        
        # Simple heuristic: offload if it saves energy AND doesn't violate a 2x latency bound
        offload = cloud_energy < local_energy and cloud_latency < (local_latency * 2)
        
        return EdgeComputeOutput(
            offload_decision=offload,
            total_latency_ms=cloud_latency if offload else local_latency,
            energy_consumed_mj=cloud_energy if offload else local_energy
        )
