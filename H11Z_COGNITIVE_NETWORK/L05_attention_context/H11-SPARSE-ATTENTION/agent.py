import math
from typing import List, Tuple
from dataclasses import dataclass

AGENT_ID = "H11-SPARSE-ATTENTION"

class SparseAttentionException(Exception):
    pass

@dataclass
class SparseAttentionInput:
    attention_scores: List[List[float]]
    top_k: int

@dataclass
class SparseAttentionOutput:
    sparse_scores: List[List[float]]
    retained_mass: float

class SparseAttentionAgent:
    """
    H11-SPARSE-ATTENTION
    Implements Top-K selection for block-sparse attention patterns.
    Zeros out non-top-K scores and measures retained probability mass.
    """
    def __init__(self):
        pass

    def process(self, input_data: SparseAttentionInput) -> SparseAttentionOutput:
        scores = input_data.attention_scores
        k = input_data.top_k
        
        if not scores:
            raise SparseAttentionException("Empty scores")
            
        out_scores = []
        total_mass = 0.0
        seq_len = len(scores)
        
        for i in range(seq_len):
            row = scores[i]
            
            # Apply softmax first to get mass
            max_s = max(row)
            exps = [math.exp(s - max_s) for s in row]
            s_exp = sum(exps)
            probs = [e / s_exp for e in exps]
            
            # Find top-k indices
            indexed_probs = list(enumerate(probs))
            indexed_probs.sort(key=lambda x: x[1], reverse=True)
            top_indices = {idx for idx, val in indexed_probs[:k]}
            
            retained_row_mass = sum(probs[idx] for idx in top_indices)
            total_mass += retained_row_mass
            
            # Zero out non-top-k (in logit space, -1e9)
            sparse_row = [row[j] if j in top_indices else -1e9 for j in range(len(row))]
            out_scores.append(sparse_row)
            
        avg_mass = total_mass / seq_len if seq_len > 0 else 0.0
        
        return SparseAttentionOutput(
            sparse_scores=out_scores,
            retained_mass=avg_mass
        )
