import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11_CLIENT"

@dataclass
class ClientInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class ClientOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class ClientException(Exception):
    pass

class ClientAgent:
    """
    Implements H11 CLIENT math and transformations.
    """
    def process(self, input_data: ClientInput) -> ClientOutput:
        if not input_data.data_vector:
            raise ClientException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'client_errors': primary}
        
        return ClientOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
