from dataclasses import dataclass

AGENT_ID = "H11-DATACENTER"

@dataclass
class DatacenterInput:
    it_equipment_power_kw: float
    cooling_power_kw: float
    power_distribution_loss_kw: float
    lighting_and_misc_power_kw: float
    num_racks: int

@dataclass
class DatacenterOutput:
    pue: float
    total_facility_power_kw: float
    average_rack_power_kw: float

class DatacenterException(Exception):
    pass

class DatacenterAgent:
    """
    Computes Datacenter Power Usage Effectiveness (PUE) and rack power metrics.
    PUE = Total Facility Power / IT Equipment Power
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: DatacenterInput) -> DatacenterOutput:
        if input_data.it_equipment_power_kw <= 0:
            raise DatacenterException("IT equipment power must be positive to calculate PUE.")
            
        total_power = (input_data.it_equipment_power_kw + 
                       input_data.cooling_power_kw + 
                       input_data.power_distribution_loss_kw + 
                       input_data.lighting_and_misc_power_kw)
                       
        pue = total_power / input_data.it_equipment_power_kw
        
        rack_power = 0.0
        if input_data.num_racks > 0:
            rack_power = input_data.it_equipment_power_kw / input_data.num_racks
            
        return DatacenterOutput(
            pue=pue,
            total_facility_power_kw=total_power,
            average_rack_power_kw=rack_power
        )
