"""
H11-DIFFUSION-NET: Diffusion Process
DDPM forward process computations.
"""
from dataclasses import dataclass
import math

AGENT_ID = "H11-DIFFUSION-NET"

@dataclass
class DiffInput:
    t: int
    beta_start: float = 0.0001
    beta_end: float = 0.02
    num_timesteps: int = 1000

@dataclass
class DiffOutput:
    beta_t: float
    alpha_t: float
    alpha_bar_t: float

class Agent:
    def process(self, input_data: DiffInput) -> DiffOutput:
        beta_t = input_data.beta_start + (input_data.t / input_data.num_timesteps) * (input_data.beta_end - input_data.beta_start)
        alpha_t = 1.0 - beta_t
        
        alpha_bar_t = 1.0
        for i in range(1, input_data.t + 1):
            b = input_data.beta_start + (i / input_data.num_timesteps) * (input_data.beta_end - input_data.beta_start)
            alpha_bar_t *= (1.0 - b)
            
        return DiffOutput(beta_t=beta_t, alpha_t=alpha_t, alpha_bar_t=alpha_bar_t)
