import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-TELEMETRY"

@dataclass
class TelemetryInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class TelemetryOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class TelemetryException(Exception):
    pass

class TelemetryAgent:
    """
    Implements H11 TELEMETRY math and transformations.
    """
    def process(self, input_data: TelemetryInput) -> TelemetryOutput:
        if not input_data.data_vector:
            raise TelemetryException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(math.exp(-x) for x in input_data.data_vector)
        is_crit = primary < input_data.threshold
        state = {'decay_sum': primary}
        
        return TelemetryOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
