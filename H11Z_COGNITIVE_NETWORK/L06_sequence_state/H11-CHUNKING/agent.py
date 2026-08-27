from dataclasses import dataclass
from typing import List, Tuple

AGENT_ID = "H11-CHUNKING"

class ChunkingConfigurationError(Exception):
    """Raised for invalid chunking parameters."""
    pass

@dataclass
class ChunkingInput:
    sequence: List[int]
    chunk_size: int = 512
    overlap: int = 64

@dataclass
class ChunkingOutput:
    chunks: List[List[int]]
    boundaries: List[Tuple[int, int]]
    efficiency: float

class ChunkingAgent:
    """
    Overlapping window chunking for long-context sequences.
    efficiency = total_unique_tokens / total_processed_tokens
    """
    def process(self, req: ChunkingInput) -> ChunkingOutput:
        seq_len = len(req.sequence)
        if seq_len == 0:
            return ChunkingOutput(chunks=[], boundaries=[], efficiency=1.0)
            
        step = req.chunk_size - req.overlap
        if step <= 0:
            raise ChunkingConfigurationError("Overlap must be strictly less than chunk_size")
            
        chunks = []
        bounds = []
        
        for i in range(0, seq_len, step):
            end = min(i + req.chunk_size, seq_len)
            chunks.append(req.sequence[i:end])
            bounds.append((i, end))
            if end == seq_len:
                break
                
        processed = sum(len(c) for c in chunks)
        efficiency = seq_len / processed if processed > 0 else 1.0
        
        return ChunkingOutput(
            chunks=chunks,
            boundaries=bounds,
            efficiency=efficiency
        )
