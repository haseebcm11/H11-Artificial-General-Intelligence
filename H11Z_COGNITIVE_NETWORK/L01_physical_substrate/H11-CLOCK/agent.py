import math
from dataclasses import dataclass

AGENT_ID = "H11-CLOCK"

@dataclass
class ClockInput:
    reference_freq_mhz: float
    multiplier: int
    divider: int
    vco_gain_mhz_v: float
    loop_filter_bw_mhz: float
    phase_noise_dbc_hz: float

@dataclass
class ClockOutput:
    output_freq_mhz: float
    rms_jitter_ps: float
    pll_lock_time_us: float

class ClockException(Exception):
    pass

class ClockAgent:
    """
    Computes PLL output frequency, lock time, and estimates jitter.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: ClockInput) -> ClockOutput:
        if input_data.divider <= 0:
            raise ClockException("Divider must be positive.")
            
        out_freq = (input_data.reference_freq_mhz * input_data.multiplier) / input_data.divider
        
        # PLL lock time ~ 4 / Loop_BW (rule of thumb)
        if input_data.loop_filter_bw_mhz <= 0:
            raise ClockException("Loop filter bandwidth must be positive.")
        lock_time_us = 4.0 / input_data.loop_filter_bw_mhz
        
        # RMS Jitter estimation from phase noise floor (highly simplified)
        # Jitter_rms ~ sqrt(10^(L(f)/10) * Bandwidth) / (2 * pi * f_out)
        # Using a dummy integration bandwidth of 20MHz for the phase noise
        int_bw_hz = 20e6
        noise_power = math.pow(10, input_data.phase_noise_dbc_hz / 10.0) * int_bw_hz
        
        if noise_power < 0:
            noise_power = 1e-15
            
        phase_jitter_rad = math.sqrt(2 * noise_power)
        jitter_s = phase_jitter_rad / (2 * math.pi * out_freq * 1e6)
        jitter_ps = jitter_s * 1e12
        
        return ClockOutput(
            output_freq_mhz=out_freq,
            rms_jitter_ps=jitter_ps,
            pll_lock_time_us=lock_time_us
        )
