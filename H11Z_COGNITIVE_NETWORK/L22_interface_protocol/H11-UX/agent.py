import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-UX"

@dataclass
class UxInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class UxOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class UxException(Exception):
    pass

class UxAgent:
    """
    Implements H11 UX math and transformations.
    """
    def process(self, input_data: UxInput) -> UxOutput:
        if not input_data.data_vector:
            raise UxException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(math.log(x+1) for x in input_data.data_vector if x > 0)
        is_crit = primary > input_data.threshold
        state = {'ux_friction': primary}
        
        return UxOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
