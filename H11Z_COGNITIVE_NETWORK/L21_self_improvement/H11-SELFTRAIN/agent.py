import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-SELFTRAIN"

@dataclass
class SelftrainInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class SelftrainOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class SelftrainException(Exception):
    pass

class SelftrainAgent:
    """
    Implements H11 SELFTRAIN math and transformations.
    """
    def process(self, input_data: SelftrainInput) -> SelftrainOutput:
        if not input_data.data_vector:
            raise SelftrainException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'training_loss': primary}
        
        return SelftrainOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
