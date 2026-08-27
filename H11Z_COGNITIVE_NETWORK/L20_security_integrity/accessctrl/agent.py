import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "ACCESSCTRL"

@dataclass
class AccessctrlInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class AccessctrlOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class AccessctrlException(Exception):
    pass

class AccessctrlAgent:
    """
    Implements accessctrl math and transformations.
    """
    def process(self, input_data: AccessctrlInput) -> AccessctrlOutput:
        if not input_data.data_vector:
            raise AccessctrlException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(1 for x in input_data.data_vector if int(x) & 1)
        is_crit = primary > input_data.threshold
        state = {'read_access_count': primary}
        
        return AccessctrlOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
