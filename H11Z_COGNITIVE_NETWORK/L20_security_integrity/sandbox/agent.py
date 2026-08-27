import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "SANDBOX"

@dataclass
class SandboxInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class SandboxOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class SandboxException(Exception):
    pass

class SandboxAgent:
    """
    Implements sandbox math and transformations.
    """
    def process(self, input_data: SandboxInput) -> SandboxOutput:
        if not input_data.data_vector:
            raise SandboxException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x for x in input_data.data_vector)
        is_crit = primary > input_data.threshold
        state = {'resource_usage': primary}
        
        return SandboxOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
