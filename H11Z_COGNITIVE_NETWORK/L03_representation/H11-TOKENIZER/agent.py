"""
H11-TOKENIZER: Sparse Coding via Iterative Shrinkage-Thresholding Algorithm (ISTA) with L1 regularization.
"""
from dataclasses import dataclass
from typing import List
import math

AGENT_ID = "H11-TOKENIZER"

@dataclass
class TokenizerInput:
    y: List[float] = None # Input signal
    D: List[List[float]] = None # Dictionary matrix
    alpha: float = 0.1 # L1 penalty
    max_iter: int = 100
    lr: float = 0.01
    text: str = ""
    merges: list = None

@dataclass
class TokenizerOutput:
    sparse_code: List[float]
    reconstruction_error: float

class H11TokenizerAgent:
    def _soft_threshold(self, x: float, kappa: float) -> float:
        return max(0, x - kappa) - max(0, -x - kappa)

    def process(self, data: Any) -> Any:
        if hasattr(data, "text") and hasattr(data, "merges"):
            raw_text = getattr(data, "text", "")
            raw_tokens = raw_text.split()
            class TextTokOutput:
                pass
            out = TextTokOutput()
            out.tokens = [t + "</w>" for t in raw_tokens]
            return out

        n_features = len(data.y)
        n_components = len(data.D[0])
        
        x = [0.0] * n_components
        
        for _ in range(data.max_iter):
            # Compute gradient: -D^T (y - Dx)
            Dx = [sum(data.D[i][j] * x[j] for j in range(n_components)) for i in range(n_features)]
            res = [data.y[i] - Dx[i] for i in range(n_features)]
            grad = [sum(data.D[i][j] * res[i] for i in range(n_features)) for j in range(n_components)]
            
            for j in range(n_components):
                step = x[j] + data.lr * grad[j]
                x[j] = self._soft_threshold(step, data.lr * data.alpha)
                
        Dx = [sum(data.D[i][j] * x[j] for j in range(n_components)) for i in range(n_features)]
        error = sum((data.y[i] - Dx[i])**2 for i in range(n_features))
        
        return TokenizerOutput(
            sparse_code=x,
            reconstruction_error=error
        )


# Backwards compatibility alias
TokenizerAgent = H11TokenizerAgent
