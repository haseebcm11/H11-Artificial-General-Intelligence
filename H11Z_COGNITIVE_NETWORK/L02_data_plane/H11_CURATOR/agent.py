"""H11_CURATOR: Data Selection with Importance Resampling (DSIR).

Computes importance weights to match a target distribution.
Math: w(x) = P_{target}(x) / P_{source}(x)
Resamples the source pool based on normalized importance weights.
"""
import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_CURATOR"

class CuratorError(ValueError):
    """Domain-specific error for H11_CURATOR."""

class CuratorStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class DocumentStats:
    doc_id: str
    target_log_prob: float
    source_log_prob: float

@dataclass(frozen=True)
class CuratorInput:
    documents: List[DocumentStats] = field(default_factory=list)
    target_sample_size: int = 100
    temperature: float = 1.0

@dataclass(frozen=True)
class CuratorOutput:
    agent_id: str
    status: str
    selected_doc_ids: List[str]
    importance_weights: Dict[str, float]
    execution_time_ms: float
    diagnostics: Dict[str, float]

class CuratorAgent:
    """Analytical engine for Importance Resampling (DSIR)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: Optional[CuratorInput] = None) -> CuratorOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = CuratorInput()

        docs = input_data.documents
        if not docs:
            raise CuratorError("No documents provided for curation.")

        weights = {}
        max_log_w = -float('inf')
        
        # Calculate log weights: log(w(x)) = (log P_t(x) - log P_s(x)) / T
        log_weights = []
        for doc in docs:
            lw = (doc.target_log_prob - doc.source_log_prob) / input_data.temperature
            log_weights.append((doc.doc_id, lw))
            if lw > max_log_w:
                max_log_w = lw

        # Stable softmax-like normalization
        sum_w = 0.0
        exp_weights = []
        for doc_id, lw in log_weights:
            w = math.exp(lw - max_log_w)
            exp_weights.append((doc_id, w))
            sum_w += w

        normalized_weights = {doc_id: w / sum_w for doc_id, w in exp_weights}
        
        # Systematic Resampling (more stable than pure multinomial)
        selected = []
        n = input_data.target_sample_size
        
        if n > 0:
            step = 1.0 / n
            r = random.uniform(0, step)
            c = 0.0
            idx = 0
            doc_items = list(normalized_weights.items())
            
            for i in range(n):
                u = r + i * step
                while c < u and idx < len(doc_items):
                    c += doc_items[idx][1]
                    idx += 1
                if idx > 0:
                    selected.append(doc_items[idx-1][0])

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return CuratorOutput(
            agent_id=AGENT_ID,
            status=CuratorStatus.OPTIMAL.name,
            selected_doc_ids=selected,
            importance_weights={k: round(v, 6) for k, v in normalized_weights.items()},
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "effective_sample_size": 1.0 / sum(w*w for w in normalized_weights.values()),
                "total_documents": len(docs)
            }
        )
