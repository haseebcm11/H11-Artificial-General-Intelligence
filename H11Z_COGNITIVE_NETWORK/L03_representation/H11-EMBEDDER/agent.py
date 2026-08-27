"""
H11-EMBEDDER: Word2Vec Skip-Gram with Negative Sampling Loss.
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-EMBEDDER"

@dataclass
class EmbedderInput:
    center_word_vec: List[float] = None
    context_word_vecs: List[List[float]] = None
    negative_word_vecs: List[List[float]] = None
    tokens: List[str] = None
    dim: int = 16

@dataclass
class EmbedderOutput:
    loss: float
    gradients_center: List[float]

class H11EmbedderAgent:
    def _sigmoid(self, x: float) -> float:
        if x < -700:
            return 0.0
        return 1.0 / (1.0 + math.exp(-x))

    def _dot(self, v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    def process(self, data: Any) -> Any:
        if hasattr(data, "tokens") and hasattr(data, "dim"):
            tokens = getattr(data, "tokens", [])
            dim = getattr(data, "dim", 16)
            # Deterministic hash vector
            vec = [0.0] * dim
            for tok in tokens:
                for idx, ch in enumerate(tok):
                    vec[idx % dim] += ord(ch) * 0.01
            class EmbedOutput:
                vector = [round(v, 4) for v in vec]
            return EmbedOutput()

        loss = 0.0
        D = len(data.center_word_vec)
        grad_center = [0.0] * D

        # Positive pairs
        for ctx_vec in data.context_word_vecs:
            z = self._dot(data.center_word_vec, ctx_vec)
            p = self._sigmoid(z)
            loss -= math.log(p + 1e-9)
            for i in range(D):
                grad_center[i] += (p - 1.0) * ctx_vec[i]

        # Negative pairs
        for neg_vec in data.negative_word_vecs:
            z = self._dot(data.center_word_vec, neg_vec)
            p = self._sigmoid(z)
            loss -= math.log(1.0 - p + 1e-9)
            for i in range(D):
                grad_center[i] += p * neg_vec[i]

        return EmbedderOutput(
            loss=loss,
            gradients_center=grad_center
        )


# Backwards compatibility alias
EmbedderAgent = H11EmbedderAgent
