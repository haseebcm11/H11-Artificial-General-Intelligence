from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-TRANSISTOR"

@dataclass
class TransistorInput:
    vdd_volts: float
    frequency_hz: float
    load_capacitance_f: float
    static_leakage_a: float
    activity_factor: float
    threshold_voltage_v: float
    carrier_velocity_ms: float
    channel_length_nm: float

@dataclass
class TransistorOutput:
    dynamic_power_w: float
    static_power_w: float
    total_power_w: float
    intrinsic_delay_ps: float

class TransistorException(Exception):
    pass

class TransistorAgent:
    """
    Computes generic CMOS power and gate delay.
    Formulas:
    P_dynamic = alpha * C * V^2 * f
    P_static = V * I_leak
    Delay ~ (L_channel) / (v_carrier)  (Simplified transit time)
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: TransistorInput) -> TransistorOutput:
        if input_data.vdd_volts <= 0:
            raise TransistorException("VDD must be positive.")
            
        # Dynamic power: alpha * C * V^2 * f
        p_dyn = (input_data.activity_factor * 
                 input_data.load_capacitance_f * 
                 (input_data.vdd_volts ** 2) * 
                 input_data.frequency_hz)
                 
        # Static power: V * I_leak
        p_stat = input_data.vdd_volts * input_data.static_leakage_a
        
        p_tot = p_dyn + p_stat
        
        # Intrinsic delay estimation based on carrier transit time
        l_m = input_data.channel_length_nm * 1e-9
        if input_data.carrier_velocity_ms <= 0:
            raise TransistorException("Carrier velocity must be positive.")
            
        t_transit_s = l_m / input_data.carrier_velocity_ms
        delay_ps = t_transit_s * 1e12
        
        return TransistorOutput(
            dynamic_power_w=p_dyn,
            static_power_w=p_stat,
            total_power_w=p_tot,
            intrinsic_delay_ps=delay_ps
        )
