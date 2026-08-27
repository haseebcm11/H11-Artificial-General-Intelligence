import math
from dataclasses import dataclass

AGENT_ID = "H11-FPGA"

@dataclass
class FPGAInput:
    total_luts: int
    used_luts: int
    total_ffs: int
    used_ffs: int
    dsp_slices: int
    used_dsps: int
    bram_blocks: int
    used_brams: int
    routing_congestion_factor: float

@dataclass
class FPGAOutput:
    lut_utilization: float
    ff_utilization: float
    dsp_utilization: float
    bram_utilization: float
    max_achievable_fmax_mhz: float
    routing_failure_probability: float

class FPGAException(Exception):
    pass

class FPGAAgent:
    """
    Computes FPGA utilization and estimates routing congestion impact on Fmax.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: FPGAInput) -> FPGAOutput:
        if input_data.total_luts <= 0 or input_data.total_ffs <= 0:
            raise FPGAException("Total FPGA resources must be positive.")
            
        lut_util = input_data.used_luts / input_data.total_luts
        ff_util = input_data.used_ffs / input_data.total_ffs
        dsp_util = input_data.used_dsps / input_data.dsp_slices if input_data.dsp_slices > 0 else 0.0
        bram_util = input_data.used_brams / input_data.bram_blocks if input_data.bram_blocks > 0 else 0.0
        
        max_util = max(lut_util, ff_util, dsp_util, bram_util)
        
        # Base Fmax of the fabric (arbitrary standard 500MHz)
        base_fmax = 500.0
        
        # Routing delay increases non-linearly with high utilization and congestion
        # congestion_factor roughly [0.0, 1.0]
        eff_congestion = max_util * input_data.routing_congestion_factor
        
        if eff_congestion > 0.8:
            degradation = math.exp(5 * (eff_congestion - 0.8))
        else:
            degradation = 1.0 + eff_congestion
            
        fmax_mhz = base_fmax / degradation
        
        # Rent's rule based routing failure probability heuristic
        if max_util > 0.9:
            fail_prob = 1.0 - math.exp(-20 * (max_util - 0.9) * input_data.routing_congestion_factor)
        else:
            fail_prob = 0.0
            
        return FPGAOutput(
            lut_utilization=lut_util,
            ff_utilization=ff_util,
            dsp_utilization=dsp_util,
            bram_utilization=bram_util,
            max_achievable_fmax_mhz=fmax_mhz,
            routing_failure_probability=fail_prob
        )
