import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-SELFATTENTION"

class SelfAttentionException(Exception):
    pass

@dataclass
class SelfAttentionInput:
    qkv: List[List[float]] # [seq_len, d_model * 3]
    d_model: int
    num_heads: int

@dataclass
class SelfAttentionOutput:
    output: List[List[float]]
    attention_entropy: float

class SelfAttentionAgent:
    """
    H11-SELFATTENTION
    Orchestrates the full multi-head self-attention module.
    Splits QKV, applies heads, concatenates, and projects.
    """
    def __init__(self):
        pass

    def process(self, input_data: SelfAttentionInput) -> SelfAttentionOutput:
        qkv = input_data.qkv
        d_model = input_data.d_model
        num_heads = input_data.num_heads
        
        if not qkv or d_model % num_heads != 0:
            raise SelfAttentionException("Invalid inputs for self-attention")
            
        seq_len = len(qkv)
        d_k = d_model // num_heads
        
        # Split Q, K, V
        Q = [[[qkv[i][j] for j in range(h*d_k, (h+1)*d_k)] for i in range(seq_len)] for h in range(num_heads)]
        K = [[[qkv[i][d_model + j] for j in range(h*d_k, (h+1)*d_k)] for i in range(seq_len)] for h in range(num_heads)]
        V = [[[qkv[i][2*d_model + j] for j in range(h*d_k, (h+1)*d_k)] for i in range(seq_len)] for h in range(num_heads)]
        
        head_outputs = []
        total_entropy = 0.0
        
        scale = 1.0 / math.sqrt(d_k)
        for h in range(num_heads):
            out = []
            for i in range(seq_len):
                scores = []
                for j in range(seq_len):
                    if j > i: # causal mask
                        scores.append(-1e9)
                    else:
                        dot = sum(Q[h][i][d] * K[h][j][d] for d in range(d_k))
                        scores.append(dot * scale)
                        
                max_s = max(scores)
                exps = [math.exp(s - max_s) for s in scores]
                sum_exp = sum(exps)
                probs = [e / sum_exp for e in exps]
                
                entropy = -sum(p * math.log(p + 1e-12) for p in probs if p > 0)
                total_entropy += entropy
                
                vec = [0.0 for _ in range(d_k)]
                for j in range(seq_len):
                    for d in range(d_k):
                        vec[d] += probs[j] * V[h][j][d]
                out.append(vec)
            head_outputs.append(out)
            
        # Concat
        final_out = [[0.0 for _ in range(d_model)] for _ in range(seq_len)]
        for i in range(seq_len):
            for h in range(num_heads):
                for d in range(d_k):
                    final_out[i][h*d_k + d] = head_outputs[h][i][d]
                    
        avg_entropy = total_entropy / (num_heads * seq_len)
        
        return SelfAttentionOutput(
            output=final_out,
            attention_entropy=avg_entropy
        )
