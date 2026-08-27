import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-ROOTCAUSE"

@dataclass
class RootcauseInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class RootcauseOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class RootcauseException(Exception):
    pass

class RootcauseAgent:
    """
    Implements H11 ROOTCAUSE math and transformations.
    """
    def process(self, input_data: RootcauseInput) -> RootcauseOutput:
        if not input_data.data_vector:
            raise RootcauseException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x * math.log(x) for x in input_data.data_vector if x > 0)
        is_crit = primary > input_data.threshold
        state = {'entropy': primary}
        
        return RootcauseOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
