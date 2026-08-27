"""H11_LABELER: Active learning and weak supervision labeling.

Implements Shannon Entropy for active learning uncertainty sampling 
and Krippendorff's Alpha for inter-annotator reliability.
Math: H(Y|X) = - \\sum P(y_i|x) log(P(y_i|x)). 
Alpha = 1 - (D_o / D_e) where D_o is observed disagreement.
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_LABELER"

class LabelerError(ValueError):
    """Domain-specific error for H11_LABELER."""

class LabelerStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class PredictionState:
    record_id: str
    class_probabilities: List[float]

@dataclass(frozen=True)
class LabelerInput:
    predictions: List[PredictionState] = field(default_factory=list)
    # annotator_matrix: lists of annotations per item (None = missing)
    annotator_matrix: List[List[Optional[int]]] = field(default_factory=list)
    active_learning_top_k: int = 5

@dataclass(frozen=True)
class LabelerOutput:
    agent_id: str
    status: str
    active_learning_queries: List[str]
    krippendorff_alpha: float
    execution_time_ms: float
    diagnostics: Dict[str, float]

class LabelerAgent:
    """Analytical engine for active learning and agreement scoring."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _shannon_entropy(self, probs: List[float]) -> float:
        """Calculate Shannon entropy for a probability distribution."""
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * math.log(p, 2)
        return entropy

    def _krippendorff_alpha(self, matrix: List[List[Optional[int]]]) -> float:
        """Nominal Krippendorff's alpha approximation for sparse matrices."""
        if not matrix or not matrix[0]: return 1.0
        
        # Count pairwise disagreements
        n_items = len(matrix)
        total_pairs = 0
        observed_disagreement = 0.0
        
        value_counts: Dict[int, int] = {}
        total_values = 0
        
        for item in matrix:
            valid_votes = [v for v in item if v is not None]
            if len(valid_votes) < 2: continue
            
            pairs = len(valid_votes) * (len(valid_votes) - 1)
            total_pairs += pairs
            
            # Count internal disagreement for this item
            item_counts: Dict[int, int] = {}
            for v in valid_votes:
                item_counts[v] = item_counts.get(v, 0) + 1
                value_counts[v] = value_counts.get(v, 0) + 1
                total_values += 1
                
            for v, c in item_counts.items():
                # number of pairs that disagree involving 'v'
                observed_disagreement += c * (len(valid_votes) - c)
                
        if total_pairs == 0: return 1.0
        d_obs = observed_disagreement / total_pairs
        
        # Expected disagreement
        d_exp = 0.0
        if total_values > 1:
            for v, c in value_counts.items():
                d_exp += c * (total_values - c)
            d_exp /= (total_values * (total_values - 1))
            
        if d_exp == 0.0: return 1.0
        return 1.0 - (d_obs / d_exp)

    def process(self, input_data: Optional[LabelerInput] = None) -> LabelerOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = LabelerInput()

        # 1. Active Learning Uncertainty Sampling
        entropies = []
        for pred in input_data.predictions:
            e = self._shannon_entropy(pred.class_probabilities)
            entropies.append((e, pred.record_id))
            
        entropies.sort(reverse=True, key=lambda x: x[0])
        queries = [r_id for _, r_id in entropies[:input_data.active_learning_top_k]]

        # 2. Inter-annotator Agreement
        alpha = self._krippendorff_alpha(input_data.annotator_matrix)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return LabelerOutput(
            agent_id=AGENT_ID,
            status=LabelerStatus.OPTIMAL.name,
            active_learning_queries=queries,
            krippendorff_alpha=round(alpha, 4),
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "mean_entropy": round(sum(e for e, _ in entropies)/len(entropies) if entropies else 0, 4),
                "total_annotated_items": len(input_data.annotator_matrix)
            }
        )
