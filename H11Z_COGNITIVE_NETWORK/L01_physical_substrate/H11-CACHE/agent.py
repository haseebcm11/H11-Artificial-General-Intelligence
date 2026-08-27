from dataclasses import dataclass

AGENT_ID = "H11-CACHE"

@dataclass
class CacheInput:
    l1_hit_rate: float
    l1_hit_latency_ns: float
    l2_hit_rate: float
    l2_hit_latency_ns: float
    memory_access_latency_ns: float

@dataclass
class CacheOutput:
    l1_miss_rate: float
    l2_miss_rate: float
    amat_ns: float
    memory_stall_cycles_per_instruction: float
    processor_clock_freq_ghz: float = 3.0

class CacheException(Exception):
    pass

class CacheAgent:
    """
    Computes Average Memory Access Time (AMAT).
    AMAT = HitTime_L1 + MissRate_L1 * MissPenalty_L1
    MissPenalty_L1 = HitTime_L2 + MissRate_L2 * MissPenalty_L2
    MissPenalty_L2 = MainMemoryLatency
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: CacheInput) -> CacheOutput:
        if not (0 <= input_data.l1_hit_rate <= 1.0) or not (0 <= input_data.l2_hit_rate <= 1.0):
            raise CacheException("Hit rates must be between 0 and 1.")
            
        l1_miss_rate = 1.0 - input_data.l1_hit_rate
        l2_miss_rate = 1.0 - input_data.l2_hit_rate
        
        miss_penalty_l2 = input_data.memory_access_latency_ns
        miss_penalty_l1 = input_data.l2_hit_latency_ns + (l2_miss_rate * miss_penalty_l2)
        amat_ns = input_data.l1_hit_latency_ns + (l1_miss_rate * miss_penalty_l1)
        
        # Example memory stall cycles calculation
        # Assuming 1 memory access per instruction for simplicity in this metric
        # Stalls = Misses per Instruction * Miss Penalty
        # Here we just convert AMAT to cycles minus base hit time
        clock_period_ns = 1.0 / 3.0  # using default 3GHz
        stall_time_ns = amat_ns - input_data.l1_hit_latency_ns
        stall_cycles = stall_time_ns / clock_period_ns
        
        return CacheOutput(
            l1_miss_rate=l1_miss_rate,
            l2_miss_rate=l2_miss_rate,
            amat_ns=amat_ns,
            memory_stall_cycles_per_instruction=stall_cycles
        )
