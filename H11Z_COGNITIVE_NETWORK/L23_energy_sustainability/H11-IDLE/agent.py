import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-IDLE"

@dataclass
class IdleInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class IdleOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class IdleException(Exception):
    pass

class IdleAgent:
    """
    Implements H11 IDLE math and transformations.
    """
    def process(self, input_data: IdleInput) -> IdleOutput:
        if not input_data.data_vector:
            raise IdleException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'idle_time_s': primary}
        
        return IdleOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
