import math
from typing import List, Tuple
from dataclasses import dataclass

AGENT_ID = "H11-CONTEXT-WINDOW"

class ContextWindowException(Exception):
    pass

@dataclass
class ContextWindowInput:
    sequence_length: int
    window_size: int
    overlap: int

@dataclass
class ContextWindowOutput:
    chunks: List[Tuple[int, int]]
    stride_efficiency: float

class ContextWindowAgent:
    """
    H11-CONTEXT-WINDOW
    Chunked processing and sliding stride optimization.
    Calculates window boundaries for efficient context processing, ensuring
    minimal overlap waste while preserving context integrity.
    """
    def __init__(self):
        self.window_state = {}

    def process(self, input_data: ContextWindowInput) -> ContextWindowOutput:
        seq_len = input_data.sequence_length
        win_size = input_data.window_size
        overlap = input_data.overlap
        
        if win_size <= overlap:
            raise ContextWindowException("Window size must be strictly greater than overlap")
        if seq_len <= 0:
            raise ContextWindowException("Sequence length must be positive")
            
        stride = win_size - overlap
        chunks = []
        current_start = 0
        
        while current_start < seq_len:
            current_end = min(current_start + win_size, seq_len)
            chunks.append((current_start, current_end))
            if current_end == seq_len:
                break
            current_start += stride
            
        total_processed_tokens = sum(end - start for start, end in chunks)
        stride_efficiency = seq_len / total_processed_tokens if total_processed_tokens > 0 else 0.0
        
        return ContextWindowOutput(
            chunks=chunks,
            stride_efficiency=stride_efficiency
        )
