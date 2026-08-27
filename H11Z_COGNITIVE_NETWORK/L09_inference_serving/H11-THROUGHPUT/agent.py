import math
from dataclasses import dataclass

AGENT_ID = "H11-THROUGHPUT"

@dataclass
class ThroughputInput:
    total_tokens: int
    total_requests: int
    duration_seconds: float
    gpu_theoretical_flops: float
    actual_flops: float

@dataclass
class ThroughputOutput:
    tokens_per_sec: float
    reqs_per_sec: float
    mfu_utilization: float

class ThroughputException(Exception):
    pass

class H11ThroughputAgent:
    """
    Calculates system throughput metrics.
    Formulas:
    TPS = tokens / duration
    RPS = requests / duration
    MFU (Model FLOPs Utilization) = actual_flops / (gpu_theoretical_flops * duration)
    """
    def process(self, input_data: ThroughputInput) -> ThroughputOutput:
        if input_data.duration_seconds <= 0:
            raise ThroughputException("Duration must be > 0")
            
        tps = input_data.total_tokens / input_data.duration_seconds
        rps = input_data.total_requests / input_data.duration_seconds
        
        # Model FLOPs Utilization
        theoretical_max = input_data.gpu_theoretical_flops * input_data.duration_seconds
        mfu = input_data.actual_flops / theoretical_max if theoretical_max > 0 else 0.0
        
        return ThroughputOutput(
            tokens_per_sec=tps,
            reqs_per_sec=rps,
            mfu_utilization=mfu
        )
