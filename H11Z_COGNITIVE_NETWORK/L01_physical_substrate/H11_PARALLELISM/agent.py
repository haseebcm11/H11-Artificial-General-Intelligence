from dataclasses import dataclass

AGENT_ID = "H11_PARALLELISM"

@dataclass
class ParallelismInput:
    serial_fraction: float
    num_processors: int
    workload_scaling: bool = False

@dataclass
class ParallelismOutput:
    speedup: float
    efficiency: float
    law_used: str

class ParallelismException(Exception):
    pass

class ParallelismAgent:
    """
    Computes maximum theoretical speedup using Amdahl's Law or Gustafson's Law.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: ParallelismInput) -> ParallelismOutput:
        if input_data.serial_fraction < 0.0 or input_data.serial_fraction > 1.0:
            raise ParallelismException("Serial fraction must be between 0 and 1.")
        if input_data.num_processors < 1:
            raise ParallelismException("Number of processors must be at least 1.")
            
        p = input_data.num_processors
        s = input_data.serial_fraction
        
        if not input_data.workload_scaling:
            # Amdahl's Law: Fixed workload
            law = "Amdahl"
            speedup = 1.0 / (s + (1.0 - s) / p)
        else:
            # Gustafson's Law: Scaled workload
            law = "Gustafson"
            speedup = s + p * (1.0 - s)
            
        efficiency = speedup / p
        
        return ParallelismOutput(
            speedup=speedup,
            efficiency=efficiency,
            law_used=law
        )
