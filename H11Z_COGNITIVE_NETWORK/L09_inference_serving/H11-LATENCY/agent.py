import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-LATENCY"

@dataclass
class LatencyInput:
    ttft_samples: List[float]
    itl_samples: List[float]
    arrival_rate_lambda: float

@dataclass
class LatencyOutput:
    ttft_p50: float
    ttft_p99: float
    expected_queue_length: float
    littles_law_wait_time: float

class LatencyException(Exception):
    pass

class H11LatencyAgent:
    """
    Analyzes Time-to-First-Token and Inter-Token Latency.
    Computes percentiles and applies Little's Law: L = lambda * W
    """
    def process(self, input_data: LatencyInput) -> LatencyOutput:
        if not input_data.ttft_samples:
            raise LatencyException("No TTFT samples")
            
        sorted_ttft = sorted(input_data.ttft_samples)
        n = len(sorted_ttft)
        
        p50_idx = int(n * 0.5)
        p99_idx = int(n * 0.99)
        
        p50 = sorted_ttft[p50_idx]
        p99 = sorted_ttft[min(p99_idx, n - 1)]
        
        # Average wait time (W) is roughly average TTFT for queueing
        avg_w = sum(input_data.ttft_samples) / n
        
        # Little's Law: L = lambda * W
        l = input_data.arrival_rate_lambda * avg_w
        
        return LatencyOutput(
            ttft_p50=p50,
            ttft_p99=p99,
            expected_queue_length=l,
            littles_law_wait_time=avg_w
        )
