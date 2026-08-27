from dataclasses import dataclass

AGENT_ID = "H11-GPU"

@dataclass
class GPUInput:
    sm_count: int
    cores_per_sm: int
    clock_freq_ghz: float
    ops_per_cycle: int
    mem_bus_width_bits: int
    mem_clock_ghz: float
    data_transfer_rate_multi: int # e.g. 2 for DDR, 4 for QDR
    operational_intensity_flops_per_byte: float

@dataclass
class GPUOutput:
    peak_tflops: float
    peak_bandwidth_gbps: float
    roofline_bound: str
    achievable_tflops: float

class GPUException(Exception):
    pass

class GPUAgent:
    """
    Computes GPU performance using the Roofline Model.
    Calculates Peak FLOPS, Memory Bandwidth, and Achievable FLOPS given an operational intensity.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: GPUInput) -> GPUOutput:
        if input_data.sm_count <= 0 or input_data.clock_freq_ghz <= 0:
            raise GPUException("Invalid SM count or clock frequency.")
            
        # Peak compute throughput in TFLOPS
        # FLOPS = SMs * cores/SM * ops/cycle * clock
        peak_gflops = (input_data.sm_count * 
                       input_data.cores_per_sm * 
                       input_data.ops_per_cycle * 
                       input_data.clock_freq_ghz)
        peak_tflops = peak_gflops / 1000.0
        
        # Peak memory bandwidth in GB/s
        # BW = (Bus Width / 8) * Mem Clock * Data Rate Multi
        peak_bw_gbps = (input_data.mem_bus_width_bits / 8) * input_data.mem_clock_ghz * input_data.data_transfer_rate_multi
        
        # Roofline calculation
        ridge_point_intensity = (peak_tflops * 1000.0) / peak_bw_gbps  # FLOPS/Byte
        
        if input_data.operational_intensity_flops_per_byte < ridge_point_intensity:
            roofline_bound = "Memory-Bound"
            achievable_flops_gpbs = peak_bw_gbps * input_data.operational_intensity_flops_per_byte
            achievable_tflops = achievable_flops_gpbs / 1000.0
        else:
            roofline_bound = "Compute-Bound"
            achievable_tflops = peak_tflops
            
        return GPUOutput(
            peak_tflops=peak_tflops,
            peak_bandwidth_gbps=peak_bw_gbps,
            roofline_bound=roofline_bound,
            achievable_tflops=achievable_tflops
        )
