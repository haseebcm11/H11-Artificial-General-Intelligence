import math
from dataclasses import dataclass

AGENT_ID = "H11-ASIC"

@dataclass
class ASICInput:
    gate_count: int
    tech_node_nm: float
    target_freq_mhz: float
    activity_factor: float
    wire_length_mm_per_gate: float

@dataclass
class ASICOutput:
    estimated_area_mm2: float
    estimated_power_w: float
    power_density_w_mm2: float

class ASICException(Exception):
    pass

class ASICAgent:
    """
    Computes ASIC area-power tradeoff.
    Uses basic technology node scaling laws for standard cell area and power.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: ASICInput) -> ASICOutput:
        if input_data.gate_count <= 0 or input_data.tech_node_nm <= 0:
            raise ASICException("Gate count and tech node must be positive.")
            
        # Area scales roughly quadratically with tech node
        # Baseline: 1 gate at 28nm is ~ 0.5 um^2
        ref_node = 28.0
        ref_area_um2 = 0.5
        
        scaling_factor = (input_data.tech_node_nm / ref_node) ** 2
        gate_area_um2 = ref_area_um2 * scaling_factor
        
        # Add wire routing overhead
        routing_overhead = 1.0 + (input_data.wire_length_mm_per_gate * 0.1)
        total_area_um2 = input_data.gate_count * gate_area_um2 * routing_overhead
        
        total_area_mm2 = total_area_um2 / 1e6
        
        # Power estimation
        # Baseline dynamic power per gate at 28nm, 1MHz = ~0.005 uW
        ref_power_uw_mhz = 0.005
        
        # Voltage scales roughly linearly with node (simplified)
        vdd_scale = input_data.tech_node_nm / ref_node
        # Power ~ C * V^2 * f -> roughly scales with node
        gate_power_uw = ref_power_uw_mhz * scaling_factor * (vdd_scale**2) * input_data.target_freq_mhz
        
        total_dynamic_power_w = (gate_power_uw * input_data.gate_count * input_data.activity_factor) / 1e6
        
        # Add static leakage (exponentially worse at smaller nodes, simplified here)
        leakage_factor = math.exp(ref_node / input_data.tech_node_nm) * 0.01
        total_power_w = total_dynamic_power_w * (1 + leakage_factor)
        
        power_density = total_power_w / total_area_mm2 if total_area_mm2 > 0 else 0
        
        return ASICOutput(
            estimated_area_mm2=total_area_mm2,
            estimated_power_w=total_power_w,
            power_density_w_mm2=power_density
        )
