import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-SELFREFINE"

@dataclass
class SelfrefineInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class SelfrefineOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class SelfrefineException(Exception):
    pass

class SelfrefineAgent:
    """
    Implements H11 SELFREFINE math and transformations.
    """
    def process(self, input_data: SelfrefineInput) -> SelfrefineOutput:
        if not input_data.data_vector:
            raise SelfrefineException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x**0.5 for x in input_data.data_vector if x > 0)
        is_crit = primary > input_data.threshold
        state = {'refinement_level': primary}
        
        return SelfrefineOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
