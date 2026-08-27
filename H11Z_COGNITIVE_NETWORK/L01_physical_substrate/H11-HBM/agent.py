from dataclasses import dataclass

AGENT_ID = "H11-HBM"

@dataclass
class HBMInput:
    num_stacks: int
    dies_per_stack: int
    channels_per_stack: int
    bus_width_per_channel: int
    data_rate_gbps: float
    die_to_die_power_pj_bit: float
    tsv_parasitic_capacitance_pf: float

@dataclass
class HBMOutput:
    total_stack_bandwidth_gbps: float
    die_to_die_power_w: float
    tsv_energy_pj_per_transfer: float

class HBMException(Exception):
    pass

class HBMAgent:
    """
    Computes HBM stack bandwidth and die-to-die power metrics.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: HBMInput) -> HBMOutput:
        if input_data.num_stacks <= 0 or input_data.channels_per_stack <= 0:
            raise HBMException("Stacks and channels must be positive.")
            
        # Total BW = stacks * channels * bus_width * data_rate / 8 (bits to bytes)
        # Assuming data_rate is per pin (e.g., 2.4 Gbps)
        bw_per_stack = (input_data.channels_per_stack * input_data.bus_width_per_channel * input_data.data_rate_gbps) / 8.0
        total_bw_gbps = input_data.num_stacks * bw_per_stack
        
        # Power for die-to-die data movement
        # Power = Bandwidth(bits/s) * Energy/bit
        total_bw_bits_s = total_bw_gbps * 8 * 1e9
        d2d_power_w = (total_bw_bits_s * input_data.die_to_die_power_pj_bit * 1e-12)
        
        # TSV parasitic energy E = C * V^2 (assume ~1V swing for simplicity)
        # Using 1V, E in pJ is just C in pF
        tsv_energy_pj = input_data.tsv_parasitic_capacitance_pf * 1.0**2
        
        return HBMOutput(
            total_stack_bandwidth_gbps=total_bw_gbps,
            die_to_die_power_w=d2d_power_w,
            tsv_energy_pj_per_transfer=tsv_energy_pj
        )
