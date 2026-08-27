import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-MQA"

class MQAException(Exception):
    pass

@dataclass
class MQAInput:
    q_heads: List[List[List[float]]] # [num_heads, seq_len, d_k]
    k_shared: List[List[float]] # [seq_len, d_k]
    v_shared: List[List[float]] # [seq_len, d_k]

@dataclass
class MQAOutput:
    mqa_output: List[List[List[float]]]
    memory_savings: float

class MQAAgent:
    """
    H11-MQA (Multi-Query Attention)
    Shares a single K and V head across all Q heads.
    Reduces memory bandwidth during decoding significantly.
    """
    def __init__(self):
        pass

    def process(self, input_data: MQAInput) -> MQAOutput:
        q_heads = input_data.q_heads
        k_shared = input_data.k_shared
        v_shared = input_data.v_shared
        
        num_heads = len(q_heads)
        if num_heads == 0 or not k_shared:
            raise MQAException("Invalid inputs")
            
        seq_len = len(q_heads[0])
        d_k = len(q_heads[0][0])
        scale = 1.0 / math.sqrt(d_k)
        
        out_heads = []
        
        for h in range(num_heads):
            q_head = q_heads[h]
            head_out = []
            
            for q_idx in range(seq_len):
                scores = []
                for kv_idx in range(len(k_shared)):
                    dot = sum(q_head[q_idx][d] * k_shared[kv_idx][d] for d in range(d_k))
                    scores.append(dot * scale)
                    
                max_s = max(scores)
                exps = [math.exp(s - max_s) for s in scores]
                sum_exp = sum(exps)
                probs = [e / sum_exp for e in exps]
                
                out_vec = [0.0 for _ in range(d_k)]
                for kv_idx in range(len(v_shared)):
                    for d in range(d_k):
                        out_vec[d] += probs[kv_idx] * v_shared[kv_idx][d]
                head_out.append(out_vec)
                
            out_heads.append(head_out)
            
        memory_savings = float(num_heads - 1) / num_heads # proportion of KV heads saved
        
        return MQAOutput(
            mqa_output=out_heads,
            memory_savings=memory_savings
        )
