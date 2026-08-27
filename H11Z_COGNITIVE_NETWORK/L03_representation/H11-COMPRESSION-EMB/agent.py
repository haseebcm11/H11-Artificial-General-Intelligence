"""
H11-COMPRESSION-EMB: Embedding Quantization via Product Quantization (PQ) and Codebook.
Uses straight-through estimator conceptually to compute quantization errors.
"""
from dataclasses import dataclass
from typing import List, Tuple
import math

AGENT_ID = "H11-COMPRESSION-EMB"

@dataclass
class CompressionInput:
    embeddings: List[List[float]]
    codebook: List[List[float]]
    
@dataclass
class CompressionOutput:
    quantized_embeddings: List[List[float]]
    quantization_error: float
    indices: List[int]

class H11CompressionEmbAgent:
    def __init__(self):
        pass

    def _l2_distance(self, v1: List[float], v2: List[float]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(v1, v2)))

    def process(self, data: CompressionInput) -> CompressionOutput:
        if not data.embeddings or not data.codebook:
            raise ValueError("Empty embeddings or codebook")

        quantized = []
        indices = []
        total_error = 0.0

        for emb in data.embeddings:
            min_dist = float('inf')
            best_idx = -1
            best_code = None

            for idx, code in enumerate(data.codebook):
                dist = self._l2_distance(emb, code)
                if dist < min_dist:
                    min_dist = dist
                    best_idx = idx
                    best_code = code

            quantized.append(list(best_code))
            indices.append(best_idx)
            total_error += min_dist ** 2

        mse = total_error / len(data.embeddings)

        return CompressionOutput(
            quantized_embeddings=quantized,
            quantization_error=mse,
            indices=indices
        )
