import math
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "BACKUP"

@dataclass
class BackupInput:
    data_vector: List[float]
    threshold: float
    context_keys: List[str]

@dataclass
class BackupOutput:
    primary_metric: float
    is_critical: bool
    computed_state: Dict[str, float]

class BackupException(Exception):
    pass

class BackupAgent:
    """
    Implements backup math and transformations.
    """
    def process(self, input_data: BackupInput) -> BackupOutput:
        if not input_data.data_vector:
            raise BackupException("Empty input data vector")
            
        # Domain specific math logic
        primary = sum(x for x in input_data.data_vector) * 1.5
        is_crit = primary < input_data.threshold
        state = {'redundancy_score': primary}
        
        return BackupOutput(
            primary_metric=primary,
            is_critical=is_crit,
            computed_state=state
        )
