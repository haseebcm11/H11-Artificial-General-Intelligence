import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-QUERY"

class QueryException(Exception):
    pass

@dataclass
class QueryInput:
    hidden_states: List[List[float]]
    w_q: List[List[float]] # [d_model, d_k]

@dataclass
class QueryOutput:
    queries: List[List[float]]
    query_norm: float

class QueryAgent:
    """
    H11-QUERY
    Projects hidden states to the Query subspace Q = X * W_Q.
    Measures the L2 norm of the resulting queries to track projection magnitude.
    """
    def __init__(self):
        pass

    def process(self, input_data: QueryInput) -> QueryOutput:
        X = input_data.hidden_states
        W = input_data.w_q
        
        if not X or not W:
            raise QueryException("Empty inputs")
            
        seq_len = len(X)
        d_model = len(X[0])
        d_k = len(W[0])
        
        if len(W) != d_model:
            raise QueryException("Dimension mismatch")
            
        Q = [[0.0 for _ in range(d_k)] for _ in range(seq_len)]
        total_sq_norm = 0.0
        
        for i in range(seq_len):
            for j in range(d_k):
                val = sum(X[i][d] * W[d][j] for d in range(d_model))
                Q[i][j] = val
                total_sq_norm += val * val
                
        query_norm = math.sqrt(total_sq_norm / (seq_len * d_k))
        
        return QueryOutput(
            queries=Q,
            query_norm=query_norm
        )
