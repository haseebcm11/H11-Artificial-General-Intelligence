from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-SCAN"

class ScanComputeError(Exception):
    """Raised for scanning issues."""
    pass

@dataclass
class ScanInput:
    array: List[float]

@dataclass
class ScanOutput:
    prefix_sum: List[float]
    total_sum: float

class ScanAgent:
    """
    Parallel associative scan (Blelloch algorithm simulation) for Mamba/SSM parallelization.
    Computes exclusive prefix sum efficiently.
    """
    def process(self, req: ScanInput) -> ScanOutput:
        n = len(req.array)
        if n == 0:
            return ScanOutput([], 0.0)
            
        p2 = 1
        while p2 < n:
            p2 *= 2
            
        tree = req.array.copy() + [0.0] * (p2 - n)
        
        d = 1
        while d < p2:
            for i in range(0, p2, d * 2):
                tree[i + d * 2 - 1] += tree[i + d - 1]
            d *= 2
            
        total = tree[p2 - 1]
        tree[p2 - 1] = 0.0
        
        d = p2 // 2
        while d > 0:
            for i in range(0, p2, d * 2):
                t = tree[i + d - 1]
                tree[i + d - 1] = tree[i + d * 2 - 1]
                tree[i + d * 2 - 1] += t
            d //= 2
            
        return ScanOutput(
            prefix_sum=tree[:n],
            total_sum=total
        )
