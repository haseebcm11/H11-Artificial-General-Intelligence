"""
H11-SEMANTIC-EMB: GloVe logic - Co-occurrence matrix weighting and weighted least squares loss.
f(X_ij) = (X_ij / x_max)^alpha if X_ij < x_max else 1
"""
from dataclasses import dataclass
from typing import List, Dict
import math

AGENT_ID = "H11-SEMANTIC-EMB"

@dataclass
class SemanticInput:
    co_occurrences: Dict[int, Dict[int, float]]
    w_i: List[List[float]]
    w_j: List[List[float]]
    b_i: List[float]
    b_j: List[float]
    x_max: float = 100.0
    alpha: float = 0.75

@dataclass
class SemanticOutput:
    loss: float
    weights: List[float]

class H11SemanticEmbAgent:
    def _dot(self, v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    def process(self, data: SemanticInput) -> SemanticOutput:
        total_loss = 0.0
        weights_list = []
        
        for i, targets in data.co_occurrences.items():
            for j, x_ij in targets.items():
                if x_ij == 0:
                    continue
                    
                # Weighting function
                if x_ij < data.x_max:
                    weight = math.pow(x_ij / data.x_max, data.alpha)
                else:
                    weight = 1.0
                    
                weights_list.append(weight)
                
                dot_prod = self._dot(data.w_i[i], data.w_j[j])
                diff = dot_prod + data.b_i[i] + data.b_j[j] - math.log(x_ij)
                
                total_loss += weight * (diff ** 2)
                
        return SemanticOutput(
            loss=0.5 * total_loss,
            weights=weights_list
        )
