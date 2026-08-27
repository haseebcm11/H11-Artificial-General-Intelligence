import math
from dataclasses import dataclass
from typing import List, Optional

AGENT_ID = "H11-SILICON"

@dataclass
class SiliconInput:
    wafer_diameter_mm: float
    die_area_mm2: float
    defect_density_cm2: float
    cluster_parameter_alpha: float = 2.0  # Negative binomial clustering parameter
    edge_exclusion_mm: float = 5.0

@dataclass
class SiliconOutput:
    gross_dies_per_wafer: int
    yield_percentage: float
    good_dies_per_wafer: int
    wafer_utilization: float

class SiliconException(Exception):
    pass

class SiliconAgent:
    """
    Computes Wafer Yield using the Negative Binomial Yield Model.
    Accounts for edge exclusion and defect clustering (alpha parameter).
    Formulas:
    Gross DPW = floor(pi * (r - edge)^2 / die_area - pi * (r - edge) / sqrt(die_area/2))
    Yield = (1 + (D0 * A) / alpha) ^ (-alpha)
    where D0 is defect density per unit area (converted to mm2), A is die area.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: SiliconInput) -> SiliconOutput:
        if input_data.wafer_diameter_mm <= 0 or input_data.die_area_mm2 <= 0:
            raise SiliconException("Wafer diameter and die area must be positive.")
        
        radius_mm = input_data.wafer_diameter_mm / 2.0
        effective_radius = radius_mm - input_data.edge_exclusion_mm
        
        if effective_radius <= 0:
            raise SiliconException("Edge exclusion is too large for the given wafer diameter.")

        effective_area = math.pi * (effective_radius ** 2)
        
        # Gross Dies Per Wafer (DPW) approximation
        term1 = effective_area / input_data.die_area_mm2
        term2 = math.pi * effective_radius / math.sqrt(input_data.die_area_mm2 / 2.0)
        gross_dpw_calc = term1 - term2
        gross_dpw = max(0, int(math.floor(gross_dpw_calc)))
        
        # Defect density conversion: cm^-2 to mm^-2
        d0_mm2 = input_data.defect_density_cm2 / 100.0
        
        # Negative Binomial Yield Model
        alpha = input_data.cluster_parameter_alpha
        lambda_val = d0_mm2 * input_data.die_area_mm2
        
        if alpha > 0:
            yield_percentage = (1.0 + lambda_val / alpha) ** (-alpha)
        else:
            # Limit as alpha -> infinity is Poisson yield
            yield_percentage = math.exp(-lambda_val)
            
        good_dpw = int(math.floor(gross_dpw * yield_percentage))
        wafer_util = (gross_dpw * input_data.die_area_mm2) / (math.pi * radius_mm ** 2)
        
        return SiliconOutput(
            gross_dies_per_wafer=gross_dpw,
            yield_percentage=yield_percentage,
            good_dies_per_wafer=good_dpw,
            wafer_utilization=wafer_util
        )
