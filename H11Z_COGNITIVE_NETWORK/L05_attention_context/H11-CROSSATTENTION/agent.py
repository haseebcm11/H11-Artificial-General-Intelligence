import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-CROSSATTENTION"

class CrossAttentionException(Exception):
    pass

@dataclass
class CrossAttentionInput:
    encoder_states: List[List[float]]
    decoder_states: List[List[float]]
    d_model: int

@dataclass
class CrossAttentionOutput:
    cross_output: List[List[float]]
    alignment_score: float

class CrossAttentionAgent:
    """
    H11-CROSSATTENTION
    Cross-attention between encoder outputs (K, V) and decoder states (Q).
    Calculates exact mapping and alignment distributions.
    """
    def __init__(self):
        self.cross_state = {}

    def process(self, input_data: CrossAttentionInput) -> CrossAttentionOutput:
        q = input_data.decoder_states
        k = input_data.encoder_states
        v = input_data.encoder_states
        d_k = input_data.d_model
        
        if not q or not k:
            raise CrossAttentionException("Empty states provided")
            
        scale = 1.0 / math.sqrt(d_k)
        out = []
        alignment_sum = 0.0
        
        for i in range(len(q)):
            scores = []
            for j in range(len(k)):
                dot = sum(q[i][d] * k[j][d] for d in range(d_k))
                scores.append(dot * scale)
                
            max_s = max(scores)
            exps = [math.exp(s - max_s) for s in scores]
            sum_exp = sum(exps)
            probs = [e / sum_exp for e in exps]
            
            # Max probability indicates alignment peak
            alignment_sum += max(probs)
            
            out_vec = [0.0 for _ in range(d_k)]
            for j in range(len(k)):
                for d in range(d_k):
                    out_vec[d] += probs[j] * v[j][d]
            out.append(out_vec)
            
        avg_alignment = alignment_sum / len(q)
        
        return CrossAttentionOutput(
            cross_output=out,
            alignment_score=avg_alignment
        )
