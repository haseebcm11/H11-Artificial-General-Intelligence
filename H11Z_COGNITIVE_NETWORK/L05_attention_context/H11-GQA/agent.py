import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-GQA"

class GQAException(Exception):
    pass

@dataclass
class GQAInput:
    q_heads: List[List[List[float]]] # [num_q_heads, seq_len, d_k]
    kv_heads: List[List[List[float]]] # [num_kv_heads, seq_len, d_k]
    num_q_heads: int
    num_kv_heads: int

@dataclass
class GQAOutput:
    gqa_output: List[List[List[float]]]
    compression_ratio: float

class GQAAgent:
    """
    H11-GQA (Grouped-Query Attention)
    Interpolates between MHA and MQA by assigning a group of query heads to each KV head.
    """
    def __init__(self):
        pass

    def process(self, input_data: GQAInput) -> GQAOutput:
        num_q = input_data.num_q_heads
        num_kv = input_data.num_kv_heads
        
        if num_kv == 0 or num_q % num_kv != 0:
            raise GQAException("num_q_heads must be divisible by num_kv_heads")
            
        group_size = num_q // num_kv
        
        out_heads = []
        for g in range(num_kv):
            k_head = input_data.kv_heads[g] # Using K and V as same for simplicity in this structural code
            v_head = input_data.kv_heads[g]
            
            for i in range(group_size):
                q_head = input_data.q_heads[g * group_size + i]
                seq_len = len(q_head)
                d_k = len(q_head[0])
                
                scale = 1.0 / math.sqrt(d_k)
                head_out = []
                for q_idx in range(seq_len):
                    scores = []
                    for kv_idx in range(len(k_head)):
                        dot = sum(q_head[q_idx][d] * k_head[kv_idx][d] for d in range(d_k))
                        scores.append(dot * scale)
                        
                    max_s = max(scores)
                    exps = [math.exp(s - max_s) for s in scores]
                    sum_exp = sum(exps)
                    probs = [e / sum_exp for e in exps]
                    
                    out_vec = [0.0 for _ in range(d_k)]
                    for kv_idx in range(len(v_head)):
                        for d in range(d_k):
                            out_vec[d] += probs[kv_idx] * v_head[kv_idx][d]
                    head_out.append(out_vec)
                out_heads.append(head_out)
                
        compression_ratio = float(num_q) / num_kv
        
        return GQAOutput(
            gqa_output=out_heads,
            compression_ratio=compression_ratio
        )
