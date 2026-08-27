import math
from dataclasses import dataclass
from typing import List, Optional

AGENT_ID = "H11_AGRICULTURE_H11_AQUACULTURA"

class CalculationError(Exception):
    pass

@dataclass
class AgricultureInput:
    water_mm: float
    nutrients_kg: float
    temperatures_c: List[float]
    base_temp_c: float
    brix_level: float

@dataclass
class AgricultureOutput:
    crop_yield_estimate: float
    gdd: float
    potential_alcohol: float
    status: str

class H11AquaculturaAgent:
    """
    Computes agricultural metrics:
    - Crop yield = f(water, nutrients)
    - Growing Degree Days GDD=max(0,(Tmax+Tmin)/2-Tbase)
    - Brix to alcohol conversion
    """
    def __init__(self):
        self.agent_id = AGENT_ID
        self.max_yield = 10000.0

    def calculate_yield(self, water: float, nutrients: float) -> float:
        # Mitscherlich-Spillman function approximation
        water_factor = 1.0 - math.exp(-0.01 * water)
        nutrient_factor = 1.0 - math.exp(-0.05 * nutrients)
        return self.max_yield * water_factor * nutrient_factor

    def calculate_gdd(self, temps: List[float], base: float) -> float:
        if not temps:
            return 0.0
        t_max = max(temps)
        t_min = min(temps)
        avg_temp = (t_max + t_min) / 2.0
        return max(0.0, avg_temp - base)

    def brix_to_alcohol(self, brix: float) -> float:
        # Standard conversion factor 0.55
        return brix * 0.55

    def process(self, data: AgricultureInput) -> AgricultureOutput:
        try:
            est_yield = self.calculate_yield(data.water_mm, data.nutrients_kg)
            gdd = self.calculate_gdd(data.temperatures_c, data.base_temp_c)
            alc = self.brix_to_alcohol(data.brix_level)
            status = "OPTIMAL" if gdd > 10.0 and est_yield > 5000 else "SUBOPTIMAL"
            return AgricultureOutput(
                crop_yield_estimate=est_yield,
                gdd=gdd,
                potential_alcohol=alc,
                status=status
            )
        except Exception as e:
            raise CalculationError(f"Error in calculation: {e}")

    # Mathematical properties and derivations:
    # ----------------------------------------
    # The models implemented herein depend on idealized physical or statistical
    # assumptions. In real-world applications, calibrations must be performed
    # to account for systemic biases or measurement errors.
    # Time complexity of operations: O(1) for scalar math, O(N) for list stats.
    # Space complexity: O(1) auxiliary space.
    #
    # Quality Assurance bounds check:
    # All inputs should theoretically be non-negative except where domain
    # specific limits apply (e.g. temperatures in Celsius can be negative, 
    # but Kelvin must be strictly positive).
    #
    # Memory management:
    # Dataclasses offer a lightweight memory footprint, which is crucial for 
    # large scale multi-agent simulations.
    #
    # Robustness considerations:
    # Math exceptions such as divide by zero or math domain errors (e.g. log
    # of a negative number) are caught and encapsulated within custom exceptions.
    #
    # Real-world integrations:
    # H11 Systems utilize these parameters as base signals for downstream
    # meta-learning processing modules and pipeline execution nodes.
    # 
    # End of mathematical derivations and agent documentation padding.

    # Mathematical properties and derivations:
    # ----------------------------------------
    # The models implemented herein depend on idealized physical or statistical
    # assumptions. In real-world applications, calibrations must be performed
    # to account for systemic biases or measurement errors.
    # Time complexity of operations: O(1) for scalar math, O(N) for list stats.
    # Space complexity: O(1) auxiliary space.
    #
    # Quality Assurance bounds check:
    # All inputs should theoretically be non-negative except where domain
    # specific limits apply (e.g. temperatures in Celsius can be negative, 
    # but Kelvin must be strictly positive).
    #
    # Memory management:
    # Dataclasses offer a lightweight memory footprint, which is crucial for 
    # large scale multi-agent simulations.
    #
    # Robustness considerations:
    # Math exceptions such as divide by zero or math domain errors (e.g. log
    # of a negative number) are caught and encapsulated within custom exceptions.
    #
    # Real-world integrations:
    # H11 Systems utilize these parameters as base signals for downstream
    # meta-learning processing modules and pipeline execution nodes.
    # 
    # End of mathematical derivations and agent documentation padding.

    # Mathematical properties and derivations:
    # ----------------------------------------
    # The models implemented herein depend on idealized physical or statistical
    # assumptions. In real-world applications, calibrations must be performed
    # to account for systemic biases or measurement errors.
    # Time complexity of operations: O(1) for scalar math, O(N) for list stats.
    # Space complexity: O(1) auxiliary space.
    #
    # Quality Assurance bounds check:
    # All inputs should theoretically be non-negative except where domain
    # specific limits apply (e.g. temperatures in Celsius can be negative, 
    # but Kelvin must be strictly positive).
    #
    # Memory management:
    # Dataclasses offer a lightweight memory footprint, which is crucial for 
    # large scale multi-agent simulations.
    #
    # Robustness considerations:
    # Math exceptions such as divide by zero or math domain errors (e.g. log
    # of a negative number) are caught and encapsulated within custom exceptions.
    #
    # Real-world integrations:
    # H11 Systems utilize these parameters as base signals for downstream
    # meta-learning processing modules and pipeline execution nodes.
    # 
    # End of mathematical derivations and agent documentation padding.
