import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-MOMENTUM"

@dataclass
class MomentumInput:
    gradients: typing.Dict[str, typing.List[float]]
    momentum_factor: float = 0.9
    nesterov: bool = True
    learning_rate: float = 0.01

@dataclass
class MomentumOutput:
    updated_velocity: typing.Dict[str, typing.List[float]]
    momentum_gradients: typing.Dict[str, typing.List[float]]

class MomentumException(Exception):
    pass

class MomentumAgent:
    """
    Implements Nesterov and standard Momentum tracking for the H11 Cognitive Substrate.
    Features:
    - Velocity moving average
    - Nesterov lookahead correction
    """
    def __init__(self):
        self.velocities = {}

    def process(self, input_data: MomentumInput) -> MomentumOutput:
        if not input_data.gradients:
            raise MomentumException("No gradients provided for momentum calculation.")
            
        out_vel = {}
        out_grad = {}
        mu = input_data.momentum_factor
        
        for k, g_list in input_data.gradients.items():
            if k not in self.velocities:
                self.velocities[k] = [0.0] * len(g_list)
                
            v_new = []
            g_new = []
            
            for i, g in enumerate(g_list):
                # Update velocity: v = mu * v + g
                v = mu * self.velocities[k][i] + g
                v_new.append(v)
                
                # Nesterov or standard
                if input_data.nesterov:
                    # g_nesterov = g + mu * v
                    g_n = g + mu * v
                    g_new.append(g_n)
                else:
                    g_new.append(v)
                    
            self.velocities[k] = v_new
            out_vel[k] = v_new
            out_grad[k] = g_new
            
        return MomentumOutput(
            updated_velocity=out_vel,
            momentum_gradients=out_grad
        )
