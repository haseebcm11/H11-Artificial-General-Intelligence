import math
from dataclasses import dataclass

AGENT_ID = "H11-SERVING"

@dataclass
class ServingInput:
    arrival_rate: float  # lambda
    service_rate: float  # mu

@dataclass
class ServingOutput:
    utilization: float   # rho
    expected_response_time: float # W
    queue_length: float  # Lq

class ServingException(Exception):
    pass

class H11ServingAgent:
    """
    M/M/1 Queue serving math.
    rho = lambda / mu
    W = 1 / (mu - lambda)
    Lq = rho^2 / (1 - rho)
    """
    def process(self, input_data: ServingInput) -> ServingOutput:
        if input_data.service_rate <= input_data.arrival_rate:
            raise ServingException("System unstable: service rate <= arrival rate")
            
        rho = input_data.arrival_rate / input_data.service_rate
        w = 1.0 / (input_data.service_rate - input_data.arrival_rate)
        lq = (rho * rho) / (1.0 - rho)
        
        return ServingOutput(
            utilization=rho,
            expected_response_time=w,
            queue_length=lq
        )
