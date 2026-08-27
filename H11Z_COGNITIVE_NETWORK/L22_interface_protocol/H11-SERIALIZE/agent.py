import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-SERIALIZE"

@dataclass
class SerializeInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class SerializeOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class SerializeException(Exception):
    pass

class SerializeAgent:
    """
    Implements H11 SERIALIZE math and transformations.
    """
    def process(self, input_data: SerializeInput) -> SerializeOutput:
        if not input_data.data_vector:
            raise SerializeException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(len(str(x)) for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'payload_size': primary}
        
        return SerializeOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
