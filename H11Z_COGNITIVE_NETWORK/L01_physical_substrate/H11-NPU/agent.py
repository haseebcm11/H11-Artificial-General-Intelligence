from dataclasses import dataclass

AGENT_ID = "H11-NPU"

@dataclass
class NPUInput:
    num_mac_units: int
    clock_freq_mhz: float
    sparsity_acceleration_ratio: float
    precision_bits: int
    batch_size: int

@dataclass
class NPUOutput:
    dense_tops: float
    sparse_tops: float
    efficiency_tops_per_w: float

class NPUException(Exception):
    pass

class NPUAgent:
    """
    Computes Neural Processing Unit inference TOPS.
    Factors in sparsity acceleration and precision scaling.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: NPUInput) -> NPUOutput:
        if input_data.num_mac_units <= 0:
            raise NPUException("MAC units must be positive.")
            
        # 1 MAC = 2 Operations
        ops_per_cycle = input_data.num_mac_units * 2
        
        # Base dense TOPS
        dense_tops = (ops_per_cycle * input_data.clock_freq_mhz * 1e6) / 1e12
        
        # Sparsity increases effective TOPS
        sparse_tops = dense_tops * input_data.sparsity_acceleration_ratio
        
        # Dummy power estimation based on precision
        # Lower precision -> higher efficiency (TOPS/W)
        base_power_w = (input_data.num_mac_units * input_data.clock_freq_mhz) / 1e5
        power_w = base_power_w * (input_data.precision_bits / 8.0)
        
        eff = sparse_tops / power_w if power_w > 0 else 0.0
        
        return NPUOutput(
            dense_tops=dense_tops,
            sparse_tops=sparse_tops,
            efficiency_tops_per_w=eff
        )
