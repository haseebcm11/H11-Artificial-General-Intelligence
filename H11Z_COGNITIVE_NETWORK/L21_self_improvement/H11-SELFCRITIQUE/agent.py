import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-SELFCRITIQUE"

@dataclass
class SelfcritiqueInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class SelfcritiqueOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class SelfcritiqueException(Exception):
    pass

class SelfcritiqueAgent:
    """
    Implements H11 SELFCRITIQUE math and transformations.
    """
    def process(self, input_data: SelfcritiqueInput) -> SelfcritiqueOutput:
        if not input_data.data_vector:
            raise SelfcritiqueException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x * 2.0 for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'critique_score': primary}
        
        return SelfcritiqueOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
