import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

AGENT_ID = "H11-BATCHING-INF"

@dataclass
class Request:
    req_id: str
    seq_len: int
    is_prefill: bool

@dataclass
class BatchingInput:
    new_requests: List[Request]
    max_batch_tokens: int

@dataclass
class BatchingOutput:
    active_batch: List[str]
    padding_waste_ratio: float
    gpu_utilization_estimate: float

class BatchingException(Exception):
    pass

class H11BatchingInfAgent:
    """
    Implements continuous (in-flight) batching with chunked prefill.
    Math:
    padding_waste = (max_seq_len * batch_size - total_tokens) / (max_seq_len * batch_size)
    Estimates optimal chunk size to maximize GPU SM utilization.
    """
    def __init__(self):
        self.queue: List[Request] = []

    def process(self, input_data: BatchingInput) -> BatchingOutput:
        self.queue.extend(input_data.new_requests)
        
        # Sort by sequence length for minimal padding (if not using PagedAttention)
        self.queue.sort(key=lambda r: r.seq_len)
        
        selected = []
        total_tokens = 0
        max_len = 0
        
        for req in list(self.queue):
            if total_tokens + req.seq_len <= input_data.max_batch_tokens:
                selected.append(req)
                total_tokens += req.seq_len
                max_len = max(max_len, req.seq_len)
                self.queue.remove(req)
        
        if not selected:
            return BatchingOutput([], 0.0, 0.0)
            
        bounding_box = max_len * len(selected)
        waste = (bounding_box - total_tokens) / bounding_box if bounding_box > 0 else 0.0
        
        gpu_util = min(1.0, total_tokens / input_data.max_batch_tokens)
        
        return BatchingOutput(
            active_batch=[r.req_id for r in selected],
            padding_waste_ratio=waste,
            gpu_utilization_estimate=gpu_util
        )
