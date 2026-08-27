import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "THREAT"

@dataclass
class ThreatInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class ThreatOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class ThreatException(Exception):
    pass

class ThreatAgent:
    """
    Implements threat math and transformations.
    """
    def process(self, input_data: ThreatInput) -> ThreatOutput:
        if not input_data.data_vector:
            raise ThreatException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x * math.log(abs(x)+1) for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'threat_level': primary}
        
        return ThreatOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
