import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "CHAOS"

@dataclass
class ChaosInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class ChaosOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class ChaosException(Exception):
    pass

class ChaosAgent:
    """
    Implements chaos math and transformations.
    """
    def process(self, input_data: ChaosInput) -> ChaosOutput:
        if not input_data.data_vector:
            raise ChaosException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(math.sin(x) for x in input_data.data_vector)
        is_crit = abs(primary) > input_data.threshold
        state = {'chaos_index': primary}
        
        return ChaosOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
