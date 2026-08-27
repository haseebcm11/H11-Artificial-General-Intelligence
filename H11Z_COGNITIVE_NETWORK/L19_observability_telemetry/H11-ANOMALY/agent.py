import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-ANOMALY"

@dataclass
class AnomalyInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class AnomalyOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class AnomalyException(Exception):
    pass

class AnomalyAgent:
    """
    Implements H11 ANOMALY math and transformations.
    """
    def process(self, input_data: AnomalyInput) -> AnomalyOutput:
        if not input_data.data_vector:
            raise AnomalyException("Empty input data vector")
            
        # Domain specific math logic
        median = sorted(input_data.data_vector)[len(input_data.data_vector)//2]
        mad = sorted([abs(x - median) for x in input_data.data_vector])[len(input_data.data_vector)//2]
        sigma = mad * 1.4826
        primary = sigma
        is_crit = any(abs(x - median) > input_data.threshold * sigma for x in input_data.data_vector) if sigma > 0 else False
        state = {'median': median, 'mad': mad, 'estimated_sigma': sigma}
        
        return AnomalyOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
