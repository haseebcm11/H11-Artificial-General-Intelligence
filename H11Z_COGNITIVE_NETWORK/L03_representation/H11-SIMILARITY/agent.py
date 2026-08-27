"""
H11-SIMILARITY: Computes Pairwise Cosine Similarity and L2 Distance matrices.
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-SIMILARITY"

@dataclass
class SimilarityInput:
    embeddings_a: List[List[float]]
    embeddings_b: List[List[float]]

@dataclass
class SimilarityOutput:
    cosine_similarity_matrix: List[List[float]]
    l2_distance_matrix: List[List[float]]

class H11SimilarityAgent:
    def _norm(self, vec: List[float]) -> float:
        return math.sqrt(sum(x*x for x in vec))
        
    def _dot(self, v1: List[float], v2: List[float]) -> float:
        return sum(a*b for a, b in zip(v1, v2))

    def _l2(self, v1: List[float], v2: List[float]) -> float:
        return math.sqrt(sum((a-b)**2 for a, b in zip(v1, v2)))

    def process(self, data: SimilarityInput) -> SimilarityOutput:
        N_a = len(data.embeddings_a)
        N_b = len(data.embeddings_b)
        
        cos_matrix = [[0.0] * N_b for _ in range(N_a)]
        l2_matrix = [[0.0] * N_b for _ in range(N_a)]
        
        norms_a = [self._norm(v) for v in data.embeddings_a]
        norms_b = [self._norm(v) for v in data.embeddings_b]
        
        for i in range(N_a):
            for j in range(N_b):
                if norms_a[i] == 0 or norms_b[j] == 0:
                    cos_matrix[i][j] = 0.0
                else:
                    cos_matrix[i][j] = self._dot(data.embeddings_a[i], data.embeddings_b[j]) / (norms_a[i] * norms_b[j])
                    
                l2_matrix[i][j] = self._l2(data.embeddings_a[i], data.embeddings_b[j])
                
        return SimilarityOutput(
            cosine_similarity_matrix=cos_matrix,
            l2_distance_matrix=l2_matrix
        )
