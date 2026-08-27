"""
H11-CONTRASTIVE: Computes InfoNCE loss with temperature scaling for contrastive learning.
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-CONTRASTIVE"

@dataclass
class ContrastiveInput:
    queries: List[List[float]]
    keys: List[List[float]]
    temperature: float

@dataclass
class ContrastiveOutput:
    infonce_loss: float
    similarities: List[List[float]]

class H11ContrastiveAgent:
    def _dot_product(self, v1: List[float], v2: List[float]) -> float:
        return sum(x * y for x, y in zip(v1, v2))

    def _magnitude(self, v: List[float]) -> float:
        return math.sqrt(sum(x * x for x in v))

    def _cosine_sim(self, v1: List[float], v2: List[float]) -> float:
        mag1 = self._magnitude(v1)
        mag2 = self._magnitude(v2)
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return self._dot_product(v1, v2) / (mag1 * mag2)

    def process(self, data: ContrastiveInput) -> ContrastiveOutput:
        N = len(data.queries)
        if N != len(data.keys):
            raise ValueError("Queries and keys must have the same length.")

        similarities = []
        total_loss = 0.0

        for i in range(N):
            sim_row = []
            for j in range(N):
                sim = self._cosine_sim(data.queries[i], data.keys[j])
                sim_row.append(sim)
            similarities.append(sim_row)

            # InfoNCE loss for i-th query
            pos_sim = similarities[i][i]
            exp_pos = math.exp(pos_sim / data.temperature)
            
            sum_exp = 0.0
            for j in range(N):
                sum_exp += math.exp(similarities[i][j] / data.temperature)
                
            loss_i = -math.log(exp_pos / sum_exp)
            total_loss += loss_i

        return ContrastiveOutput(
            infonce_loss=total_loss / N,
            similarities=similarities
        )
