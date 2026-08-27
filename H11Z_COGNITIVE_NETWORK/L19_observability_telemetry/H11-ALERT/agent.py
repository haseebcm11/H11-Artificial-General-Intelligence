import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-ALERT"

@dataclass
class AlertInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class AlertOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class AlertException(Exception):
    pass

class AlertAgent:
    """
    Implements H11 ALERT math and transformations.
    """
    def process(self, input_data: AlertInput) -> AlertOutput:
        if not input_data.data_vector:
            raise AlertException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x**2 for x in input_data.data_vector) ** 0.5
        is_crit = primary > input_data.threshold
        state = {'l2_norm': primary, 'variance': sum((x - primary/len(input_data.data_vector))**2 for x in input_data.data_vector)/len(input_data.data_vector)}
        
        return AlertOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
