from dataclasses import dataclass

AGENT_ID = "H11-SPINTRONIC"

@dataclass
class SpintronicInput:
    resistance_parallel_ohms: float
    resistance_antiparallel_ohms: float
    write_current_ua: float
    critical_current_ua: float
    thermal_stability_factor: float

@dataclass
class SpintronicOutput:
    tmr_ratio: float
    switching_probability: float
    retention_time_years: float

class SpintronicException(Exception):
    pass

class SpintronicAgent:
    """
    Computes Tunnel Magnetoresistance (TMR) ratio and switching characteristics for STT-MRAM.
    TMR = (R_ap - R_p) / R_p
    Switching probability uses thermal activation models.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: SpintronicInput) -> SpintronicOutput:
        if input_data.resistance_parallel_ohms <= 0:
            raise SpintronicException("Parallel resistance must be > 0.")
            
        # TMR ratio calculation
        tmr = (input_data.resistance_antiparallel_ohms - input_data.resistance_parallel_ohms) / input_data.resistance_parallel_ohms
        
        # Switching probability (simplified Sun model for long pulses)
        import math
        
        if input_data.write_current_ua <= 0:
            p_switch = 0.0
        else:
            # Overdrive factor
            i_overdrive = input_data.write_current_ua / input_data.critical_current_ua
            if i_overdrive >= 1.0:
                p_switch = 1.0
            else:
                # Sub-critical switching due to thermal fluctuations
                # P(switch) = 1 - exp(-t/tau) where tau depends on (1 - I/Ic)^2
                # Simplified directly to switching prob given a fixed pulse width approximation
                exponent = -input_data.thermal_stability_factor * (1.0 - i_overdrive)**2
                # If exponent is highly negative, switching probability becomes effectively 0
                rate = math.exp(exponent) if exponent > -100 else 0.0
                p_switch = min(1.0, rate * 1e9) # Scaled arbitrarily for nanosecond pulses
                
        # Retention time: tau_0 * exp(Delta)
        # tau_0 is inverse attempt frequency ~ 1ns
        # 1 year ~ 3.15e7 seconds ~ 3.15e16 ns
        retention_s = 1e-9 * math.exp(input_data.thermal_stability_factor)
        retention_years = retention_s / (365.25 * 24 * 3600)
        
        return SpintronicOutput(
            tmr_ratio=tmr,
            switching_probability=p_switch,
            retention_time_years=retention_years
        )
