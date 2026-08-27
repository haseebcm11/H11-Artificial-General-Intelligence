import math
from typing import Any, List, Optional
from dataclasses import dataclass

AGENT_ID = "H11-ATTENTION-HEAD"

class AttentionHeadException(Exception):
    pass

@dataclass
class AttentionHeadInput:
    q_states: List[List[float]]
    k_states: List[List[float]]
    v_states: List[List[float]]
    head_dim: int

@dataclass
class AttentionHeadOutput:
    concatenated_output: List[List[float]]
    head_entropy: float
    importance_score: float

class AttentionHeadAgent:
    """
    H11-ATTENTION-HEAD
    Manages parallel attention heads, including head pruning, importance routing, and heterogeneous head dimensioning.
    Computes QK^T / sqrt(d_k) and calculates Shannon entropy of the attention distribution to assess head importance.
    """
    def __init__(self):
        self.active_heads = []

    def compute_scaled_dot_product(self, q: List[List[float]], k: List[List[float]], v: List[List[float]], d_k: int) -> tuple:
        seq_len_q = len(q)
        seq_len_k = len(k)
        if seq_len_k == 0 or seq_len_q == 0:
            raise AttentionHeadException("Empty sequence")
        
        scale = 1.0 / math.sqrt(d_k)
        scores = [[0.0 for _ in range(seq_len_k)] for _ in range(seq_len_q)]
        
        # Q K^T
        for i in range(seq_len_q):
            for j in range(seq_len_k):
                val = sum(q[i][d] * k[j][d] for d in range(d_k))
                scores[i][j] = val * scale
                
        # Softmax
        attention_weights = []
        for i in range(seq_len_q):
            max_val = max(scores[i])
            exp_vals = [math.exp(x - max_val) for x in scores[i]]
            sum_exp = sum(exp_vals)
            attention_weights.append([x / sum_exp for x in exp_vals])
            
        # Context vectors (Attention * V)
        output = [[0.0 for _ in range(d_k)] for _ in range(seq_len_q)]
        for i in range(seq_len_q):
            for d in range(d_k):
                output[i][d] = sum(attention_weights[i][j] * v[j][d] for j in range(seq_len_k))
                
        return output, attention_weights

    def compute_entropy(self, attention_weights: List[List[float]]) -> float:
        total_entropy = 0.0
        for weights in attention_weights:
            entropy = -sum(w * math.log(w + 1e-12) for w in weights if w > 0)
            total_entropy += entropy
        return total_entropy / len(attention_weights)

    def process(self, input_data: AttentionHeadInput) -> AttentionHeadOutput:
        d_k = input_data.head_dim
        output, weights = self.compute_scaled_dot_product(
            input_data.q_states, 
            input_data.k_states, 
            input_data.v_states, 
            d_k
        )
        entropy = self.compute_entropy(weights)
        
        # Importance score inversely proportional to entropy (high entropy -> uniform -> less specialized)
        importance_score = 1.0 / (entropy + 1e-6)
        
        return AttentionHeadOutput(
            concatenated_output=output,
            head_entropy=entropy,
            importance_score=importance_score
        )
