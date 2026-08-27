import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-DEBUG"

@dataclass
class DebugInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class DebugOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class DebugException(Exception):
    pass

class DebugAgent:
    """
    Implements H11 DEBUG math and transformations.
    """
    def process(self, input_data: DebugInput) -> DebugOutput:
        if not input_data.data_vector:
            raise DebugException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(1 for x in input_data.data_vector if x < 0)
        is_crit = primary > input_data.threshold
        state = {'negative_count': primary, 'total_count': len(input_data.data_vector)}
        
        return DebugOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
