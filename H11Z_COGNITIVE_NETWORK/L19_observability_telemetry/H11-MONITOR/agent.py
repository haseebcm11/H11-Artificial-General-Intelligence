import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-MONITOR"

@dataclass
class MonitorInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class MonitorOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class MonitorException(Exception):
    pass

class MonitorAgent:
    """
    Implements H11 MONITOR math and transformations.
    """
    def process(self, input_data: MonitorInput) -> MonitorOutput:
        if not input_data.data_vector:
            raise MonitorException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x for x in input_data.data_vector if x > input_data.threshold)
        is_crit = primary > 0
        state = {'threshold_exceeded_sum': primary}
        
        return MonitorOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
