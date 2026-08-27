import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "INTRUSION"

@dataclass
class IntrusionInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class IntrusionOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class IntrusionException(Exception):
    pass

class IntrusionAgent:
    """
    Implements intrusion math and transformations.
    """
    def process(self, input_data: IntrusionInput) -> IntrusionOutput:
        if not input_data.data_vector:
            raise IntrusionException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x**3 for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'anomaly_cube': primary}
        
        return IntrusionOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
