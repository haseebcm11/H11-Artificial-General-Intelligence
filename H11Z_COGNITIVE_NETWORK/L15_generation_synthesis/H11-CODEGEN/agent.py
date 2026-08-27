import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

AGENT_ID = "H11-CODEGEN"

class CodegenStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()
    DEGRADED = auto()
    FAILED = auto()

class CodegenError(ValueError):
    pass

@dataclass(frozen=True)
class CodegenInput:
    target_id: str = "default_target"
    intensity: float = 1.0
    batch_size: int = 32
    tolerance: float = 1e-4
    parameters: Dict[str, float] = field(default_factory=lambda: {"temperature": 0.7, "top_p": 0.9})
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class CodegenOutput:
    agent_id: str
    status: str
    efficiency_score: float
    computed_value: float
    execution_time_ms: float
    metrics: Dict[str, float]
    diagnostics: List[str]

class CodegenAgent:
    """Analytical engine for H11-CODEGEN. Implements autoregressive sampling 
    math including Temperature scaling and Nucleus (top-p) sampling."""
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state: Dict[str, Any] = {"evaluations_count": 0, "status": CodegenStatus.IDLE.name}

    def process(self, input_data: Optional[CodegenInput] = None) -> CodegenOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = CodegenInput()

        temp = float(input_data.parameters.get("temperature", 1.0))
        top_p = float(input_data.parameters.get("top_p", 1.0))
        
        # Simulated raw logits for 5 tokens
        logits = [2.5, 1.0, -1.2, 3.1, 0.4]
        
        # 1. Temperature scaling
        temp = max(1e-5, temp)
        scaled_logits = [l / temp for l in logits]
        
        # 2. Softmax
        max_logit = max(scaled_logits)
        exp_logits = [math.exp(l - max_logit) for l in scaled_logits]
        sum_exp = sum(exp_logits)
        probs = [e / sum_exp for e in exp_logits]
        
        # 3. Nucleus (top-p) sampling
        # Sort probabilities in descending order
        sorted_probs = sorted(probs, reverse=True)
        cumulative = 0.0
        cutoff_prob = 0.0
        for p in sorted_probs:
            cumulative += p
            if cumulative >= top_p:
                cutoff_prob = p
                break
                
        # Zero out probabilities below cutoff and re-normalize
        filtered_probs = [p if p >= cutoff_prob else 0.0 for p in probs]
        sum_filtered = sum(filtered_probs)
        final_probs = [p / sum_filtered for p in filtered_probs]
        
        # Entropy of final distribution
        entropy = -sum(p * math.log2(p) for p in final_probs if p > 0)
        
        efficiency = 1.0 / (1.0 + entropy)

        status = CodegenStatus.OPTIMAL.name if efficiency > 0.8 else CodegenStatus.ACTIVE.name
        self.state["evaluations_count"] = self.state.get("evaluations_count", 0) + 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        return CodegenOutput(
            agent_id=AGENT_ID,
            status=status,
            efficiency_score=efficiency,
            computed_value=entropy,
            execution_time_ms=elapsed_ms,
            metrics={"temperature": temp, "top_p": top_p, "entropy": entropy, "p_max": max(final_probs)},
            diagnostics=["Autoregressive sampling probabilities computed."]
        )
