from dataclasses import dataclass

AGENT_ID = "H11-VRAM"

@dataclass
class VRAMInput:
    total_bandwidth_gbps: float
    num_banks: int
    page_size_bytes: int
    memory_access_pattern_stride_bytes: int
    requests_per_second: float
    bytes_per_request: int

@dataclass
class VRAMOutput:
    bank_conflict_rate: float
    effective_bandwidth_gbps: float
    bandwidth_utilization: float

class VRAMException(Exception):
    pass

class VRAMAgent:
    """
    Computes VRAM bandwidth utilization and bank conflict probabilities.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: VRAMInput) -> VRAMOutput:
        if input_data.num_banks <= 0 or input_data.total_bandwidth_gbps <= 0:
            raise VRAMException("Banks and Bandwidth must be positive.")
            
        # Simplistic model of bank conflicts based on stride
        # If stride is a multiple of page_size * num_banks, all requests hit the same bank
        stride = input_data.memory_access_pattern_stride_bytes
        bank_interleave = input_data.page_size_bytes
        
        if stride == 0:
            conflict_rate = 0.0
        else:
            # Hash-based distribution proxy
            # Ideal stride for 0 conflicts traverses banks sequentially
            # Worst case stride maps to same bank
            gcd_val = self._gcd(stride, bank_interleave * input_data.num_banks)
            conflict_factor = gcd_val / (bank_interleave * input_data.num_banks)
            # Normalize to somewhat realistic [0,1]
            conflict_rate = min(1.0, conflict_factor * input_data.num_banks)

        # Efficiency penalty from conflicts (linear penalty assumption)
        efficiency = 1.0 - (conflict_rate * 0.8) # up to 80% penalty for full conflicts
        
        effective_bw = input_data.total_bandwidth_gbps * efficiency
        
        requested_bw_gbps = (input_data.requests_per_second * input_data.bytes_per_request) / 1e9
        
        utilization = requested_bw_gbps / effective_bw if effective_bw > 0 else 1.0
        utilization = min(1.0, utilization)
        
        return VRAMOutput(
            bank_conflict_rate=conflict_rate,
            effective_bandwidth_gbps=effective_bw,
            bandwidth_utilization=utilization
        )
        
    def _gcd(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a
