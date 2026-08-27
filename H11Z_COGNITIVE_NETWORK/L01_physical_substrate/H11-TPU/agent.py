from dataclasses import dataclass

AGENT_ID = "H11-TPU"

@dataclass
class TPUInput:
    array_height: int
    array_width: int
    clock_freq_mhz: float
    bytes_per_weight: int
    bytes_per_activation: int
    utilization_factor: float

@dataclass
class TPUOutput:
    peak_tops: float
    effective_tops: float
    weight_bandwidth_gbps_required: float
    activation_bandwidth_gbps_required: float

class TPUException(Exception):
    pass

class TPUAgent:
    """
    Computes Systolic Array Throughput for TPU architectures.
    Assumes MACs per cycle = array_height * array_width.
    Calculates TOPS and required bandwidth to feed the array.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: TPUInput) -> TPUOutput:
        if input_data.array_height <= 0 or input_data.array_width <= 0:
            raise TPUException("Array dimensions must be positive.")
            
        # 1 MAC = 2 Operations (Multiply and Accumulate)
        ops_per_cycle = input_data.array_height * input_data.array_width * 2
        
        # Peak TOPS = ops/cycle * clock (MHz) / 1,000,000 to get TOPS
        peak_tops = (ops_per_cycle * input_data.clock_freq_mhz * 1e6) / 1e12
        
        effective_tops = peak_tops * input_data.utilization_factor
        
        # Bandwidth required to feed the systolic array fully
        # Weights stream into the array (one per row/col per cycle depending on dataflow)
        # Assuming Weight Stationary: weights are preloaded, activations flow.
        # Required activation BW: height * bytes_per_act * clock
        act_bw_gbps = (input_data.array_height * input_data.bytes_per_activation * input_data.clock_freq_mhz * 1e6) / 1e9
        
        # Required weight BW (if streaming weights, e.g., output stationary)
        weight_bw_gbps = (input_data.array_width * input_data.bytes_per_weight * input_data.clock_freq_mhz * 1e6) / 1e9
        
        return TPUOutput(
            peak_tops=peak_tops,
            effective_tops=effective_tops,
            weight_bandwidth_gbps_required=weight_bw_gbps,
            activation_bandwidth_gbps_required=act_bw_gbps
        )
