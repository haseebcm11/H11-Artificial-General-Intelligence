"""H11-MULTIMODAL: Late-fusion and modality combination.

Implements softmax-weighted late fusion for disparate perception streams.
"""
from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-MULTIMODAL"

class MultimodalError(ValueError): pass

@dataclass
class MultimodalInput:
    modality_logits: Dict[str, List[float]] # Modality name to logits array
    modality_weights: Dict[str, float]

@dataclass
class MultimodalOutput:
    agent_id: str
    fused_probabilities: List[float]
    entropy: float
    execution_time_ms: float

class MultimodalAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        
    def _softmax(self, logits: List[float]) -> List[float]:
        max_l = max(logits)
        exps = [math.exp(l - max_l) for l in logits]
        sum_e = sum(exps)
        return [e / sum_e for e in exps]

    def process(self, input_data: MultimodalInput) -> MultimodalOutput:
        start_time = time.perf_counter()
        
        if not input_data.modality_logits:
            raise MultimodalError("Empty logits")
            
        dim = len(next(iter(input_data.modality_logits.values())))
        fused = [0.0] * dim
        weight_sum = 0.0
        
        for mod, logits in input_data.modality_logits.items():
            probs = self._softmax(logits)
            w = input_data.modality_weights.get(mod, 1.0)
            weight_sum += w
            
            for i in range(dim):
                fused[i] += probs[i] * w
                
        if weight_sum > 0:
            fused = [f / weight_sum for f in fused]
            
        # Final entropy
        entropy = -sum(p * math.log2(p) for p in fused if p > 0)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return MultimodalOutput(
            agent_id=AGENT_ID,
            fused_probabilities=fused,
            entropy=entropy,
            execution_time_ms=elapsed_ms
        )
