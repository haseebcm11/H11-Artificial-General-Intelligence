import math
from dataclasses import dataclass

AGENT_ID = "H11-POWER"

@dataclass
class PowerInput:
    input_voltage_v: float
    output_voltage_v: float
    load_current_a: float
    switching_freq_khz: float
    inductor_dcr_ohms: float
    fet_rds_on_ohms: float
    output_capacitance_uf: float

@dataclass
class PowerOutput:
    vrm_efficiency: float
    power_loss_w: float
    voltage_ripple_mv: float

class PowerException(Exception):
    pass

class PowerAgent:
    """
    Computes VRM (Voltage Regulator Module) efficiency and ripple.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: PowerInput) -> PowerOutput:
        if input_data.output_voltage_v >= input_data.input_voltage_v:
            raise PowerException("Buck converter output voltage must be < input voltage.")
            
        duty_cycle = input_data.output_voltage_v / input_data.input_voltage_v
        
        # Conduction losses (simplified)
        p_cond_inductor = (input_data.load_current_a ** 2) * input_data.inductor_dcr_ohms
        p_cond_fet = (input_data.load_current_a ** 2) * input_data.fet_rds_on_ohms * duty_cycle
        
        # Switching losses (approximate)
        # P_sw = 0.5 * V_in * I_load * (t_rise + t_fall) * f_sw
        # Assume t_rise + t_fall ~ 10ns for typical modern FETs
        t_trans = 10e-9
        p_sw = 0.5 * input_data.input_voltage_v * input_data.load_current_a * t_trans * (input_data.switching_freq_khz * 1000)
        
        total_loss = p_cond_inductor + p_cond_fet + p_sw
        output_power = input_data.output_voltage_v * input_data.load_current_a
        
        efficiency = output_power / (output_power + total_loss) if (output_power + total_loss) > 0 else 0.0
        
        # Ripple voltage estimation
        # delta_I = V_out * (1 - D) / (L * f_sw)
        # Assume L = 1uH for simplicity in this model if not provided
        L_henries = 1e-6
        f_sw_hz = input_data.switching_freq_khz * 1000.0
        delta_i = (input_data.output_voltage_v * (1.0 - duty_cycle)) / (L_henries * f_sw_hz)
        
        # delta_V = delta_I / (8 * C * f_sw) + delta_I * ESR
        # Ignoring ESR for pure capacitance ripple
        c_farads = input_data.output_capacitance_uf * 1e-6
        ripple_v = delta_i / (8.0 * c_farads * f_sw_hz)
        ripple_mv = ripple_v * 1000.0
        
        return PowerOutput(
            vrm_efficiency=efficiency,
            power_loss_w=total_loss,
            voltage_ripple_mv=ripple_mv
        )
