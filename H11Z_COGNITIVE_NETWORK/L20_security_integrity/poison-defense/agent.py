import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "POISON-DEFENSE"

@dataclass
class PoisonDefenseInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class PoisonDefenseOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class PoisonDefenseException(Exception):
    pass

class PoisonDefenseAgent:
    """
    Implements poison defense math and transformations.
    """
    def process(self, input_data: PoisonDefenseInput) -> PoisonDefenseOutput:
        if not input_data.data_vector:
            raise PoisonDefenseException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(math.exp(x) for x in input_data.data_vector if x < 0)
        is_crit = primary > input_data.threshold
        state = {'poison_score': primary}
        
        return PoisonDefenseOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
