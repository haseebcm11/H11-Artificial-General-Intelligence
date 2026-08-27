import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-SOLAR-AI"

@dataclass
class SolarAiInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class SolarAiOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class SolarAiException(Exception):
    pass

class SolarAiAgent:
    """
    Implements H11 SOLAR AI math and transformations.
    """
    def process(self, input_data: SolarAiInput) -> SolarAiOutput:
        if not input_data.data_vector:
            raise SolarAiException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x * 0.22 for x in input_data.data_vector)
        is_crit = primary < input_data.threshold
        state = {'solar_generation_kwh': primary}
        
        return SolarAiOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
