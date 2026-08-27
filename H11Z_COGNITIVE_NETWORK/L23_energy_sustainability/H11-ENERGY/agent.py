import math
from dataclasses import dataclass

AGENT_ID = "H11-ENERGY"

@dataclass
class EnergyInput:
    it_equipment_power_w: float
    total_facility_power_w: float
    carbon_intensity_gco2_kwh: float
    solar_irradiance_w_m2: float
    solar_area_m2: float
    battery_capacity_wh: float
    current_charge_wh: float

@dataclass
class EnergyOutput:
    pue: float
    emissions_gco2: float
    battery_soc_percent: float
    solar_yield_w: float

class SustainabilityException(Exception):
    pass

class EnergyAgent:
    """
    Implements PUE calculation, carbon intensity mapping, battery State of Charge,
    and solar irradiance conversion.
    """
    def process(self, input_data: EnergyInput) -> EnergyOutput:
        if input_data.it_equipment_power_w <= 0:
            raise SustainabilityException("IT Power must be positive")
            
        pue = input_data.total_facility_power_w / input_data.it_equipment_power_w
        
        # Solar Yield = Irradiance * Area * Efficiency (assumed 20%)
        solar_yield = input_data.solar_irradiance_w_m2 * input_data.solar_area_m2 * 0.20
        
        net_grid_power_w = max(0.0, input_data.total_facility_power_w - solar_yield)
        
        emissions = (net_grid_power_w / 1000.0) * input_data.carbon_intensity_gco2_kwh
        
        if input_data.battery_capacity_wh <= 0:
            raise SustainabilityException("Battery capacity must be positive")
            
        soc = (input_data.current_charge_wh / input_data.battery_capacity_wh) * 100.0
        
        return EnergyOutput(
            pue=pue,
            emissions_gco2=emissions,
            battery_soc_percent=soc,
            solar_yield_w=solar_yield
        )
