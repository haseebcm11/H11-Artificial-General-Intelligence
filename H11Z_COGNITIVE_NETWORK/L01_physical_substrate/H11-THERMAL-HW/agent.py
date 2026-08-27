from dataclasses import dataclass

AGENT_ID = "H11-THERMAL-HW"

@dataclass
class ThermalHWInput:
    power_dissipation_w: float
    ambient_temp_c: float
    r_theta_jc_c_w: float  # Junction-to-case thermal resistance
    r_theta_ca_c_w: float  # Case-to-ambient thermal resistance (heatsink)

@dataclass
class ThermalHWOutput:
    junction_temp_c: float
    case_temp_c: float
    is_throttling: bool
    thermal_margin_c: float
    throttle_temp_limit_c: float = 105.0

class ThermalHWException(Exception):
    pass

class ThermalHWAgent:
    """
    Computes component junction temperature based on thermal resistances.
    T_j = T_a + P * (R_jc + R_ca)
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: ThermalHWInput) -> ThermalHWOutput:
        if input_data.power_dissipation_w < 0:
            raise ThermalHWException("Power dissipation cannot be negative.")
            
        case_temp = input_data.ambient_temp_c + (input_data.power_dissipation_w * input_data.r_theta_ca_c_w)
        junction_temp = case_temp + (input_data.power_dissipation_w * input_data.r_theta_jc_c_w)
        
        throttle_limit = 105.0 # Default limit
        
        is_throttling = junction_temp >= throttle_limit
        margin = throttle_limit - junction_temp
        
        return ThermalHWOutput(
            junction_temp_c=junction_temp,
            case_temp_c=case_temp,
            is_throttling=is_throttling,
            thermal_margin_c=margin,
            throttle_temp_limit_c=throttle_limit
        )
