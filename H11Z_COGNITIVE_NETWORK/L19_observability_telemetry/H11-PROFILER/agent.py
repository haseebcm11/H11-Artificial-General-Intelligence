import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-PROFILER"

@dataclass
class ProfilerInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class ProfilerOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class ProfilerException(Exception):
    pass

class ProfilerAgent:
    """
    Implements H11 PROFILER math and transformations.
    """
    def process(self, input_data: ProfilerInput) -> ProfilerOutput:
        if not input_data.data_vector:
            raise ProfilerException("Empty input data vector")
            
        # Domain specific math logic
        primary = max(input_data.data_vector) - min(input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'range': primary, 'variance': sum((x - sum(input_data.data_vector)/len(input_data.data_vector))**2 for x in input_data.data_vector)/len(input_data.data_vector)}
        
        return ProfilerOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
