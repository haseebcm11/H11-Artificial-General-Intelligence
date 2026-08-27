import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-APIGATEWAY"

@dataclass
class ApigatewayInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class ApigatewayOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class ApigatewayException(Exception):
    pass

class ApigatewayAgent:
    """
    Implements H11 APIGATEWAY math and transformations.
    """
    def process(self, input_data: ApigatewayInput) -> ApigatewayOutput:
        if not input_data.data_vector:
            raise ApigatewayException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(1 for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'request_count': primary}
        
        return ApigatewayOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
