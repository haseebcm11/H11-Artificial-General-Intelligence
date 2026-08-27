"""H11_SAMPLER: Statistical sampling and curriculum strategies.

Implements Curriculum learning temperature-based sampling and Reservoir Sampling.
Math: P(x) = exp(-C(x)/T) / Z where C(x) is complexity and T is temperature.
"""
import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_SAMPLER"

class SamplerError(ValueError):
    """Domain-specific error for H11_SAMPLER."""

class SamplerStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class DataItem:
    item_id: str
    complexity_score: float

@dataclass(frozen=True)
class SamplerInput:
    data_stream: List[DataItem] = field(default_factory=list)
    temperature: float = 1.0 # High = uniform, Low = highly skewed to simple
    reservoir_size: int = 100

@dataclass(frozen=True)
class SamplerOutput:
    agent_id: str
    status: str
    sampled_ids: List[str]
    importance_weights: Dict[str, float]
    execution_time_ms: float
    diagnostics: Dict[str, float]

class SamplerAgent:
    """Analytical engine for Curriculum and Reservoir sampling."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.stream_count = 0
        self.reservoir: List[DataItem] = []

    def _curriculum_probabilities(self, items: List[DataItem], T: float) -> Dict[str, float]:
        """Calculates probabilities based on complexity and temperature."""
        if T <= 0:
            raise SamplerError("Temperature must be strictly positive")
            
        unnormalized = {}
        Z = 0.0
        
        # To avoid overflow, find min complexity
        min_c = min(item.complexity_score for item in items) if items else 0.0
        
        for item in items:
            # Shift by min_c for numerical stability
            p = math.exp(-(item.complexity_score - min_c) / T)
            unnormalized[item.item_id] = p
            Z += p
            
        return {k: v / Z for k, v in unnormalized.items()}

    def process(self, input_data: Optional[SamplerInput] = None) -> SamplerOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = SamplerInput()

        stream = input_data.data_stream
        
        # 1. Curriculum probability weighting
        probs = self._curriculum_probabilities(stream, input_data.temperature)
        
        # 2. Reservoir sampling incorporating curriculum weights
        # Algorithm A-Res (Weighted Reservoir Sampling)
        for item in stream:
            self.stream_count += 1
            w = probs[item.item_id]
            # Key = u^(1/w) where u ~ U(0,1)
            u = random.random()
            key = math.pow(u, 1.0 / max(w, 1e-10))
            
            if len(self.reservoir) < input_data.reservoir_size:
                self.reservoir.append((key, item))
                if len(self.reservoir) == input_data.reservoir_size:
                    self.reservoir.sort(key=lambda x: x[0])
            else:
                if key > self.reservoir[0][0]:
                    self.reservoir[0] = (key, item)
                    self.reservoir.sort(key=lambda x: x[0])
                    
        sampled = [x[1].item_id for x in self.reservoir]
        
        # Inverse probability weighting to correct bias downstream
        weights = {}
        for x in self.reservoir:
            p = probs[x[1].item_id]
            weights[x[1].item_id] = 1.0 / max(p * input_data.reservoir_size, 1e-5)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return SamplerOutput(
            agent_id=AGENT_ID,
            status=SamplerStatus.OPTIMAL.name,
            sampled_ids=sampled,
            importance_weights={k: round(v, 4) for k, v in weights.items()},
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "stream_processed": self.stream_count,
                "current_temperature": input_data.temperature
            }
        )
