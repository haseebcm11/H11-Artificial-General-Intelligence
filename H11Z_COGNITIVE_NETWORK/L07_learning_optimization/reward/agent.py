import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-REWARD"

@dataclass
class RewardInput:
    trajectory_rewards: typing.List[float]
    value_estimates: typing.List[float]
    gamma: float = 0.99
    lam: float = 0.95

@dataclass
class RewardOutput:
    advantages: typing.List[float]
    returns: typing.List[float]
    mean_advantage: float

class RewardException(Exception):
    pass

class RewardAgent:
    """
    Implements Generalized Advantage Estimation (GAE) for the H11 Cognitive Substrate.
    Features:
    - Reward discounting
    - GAE-lambda calculation
    - Return calculation
    """
    def __init__(self):
        pass

    def process(self, input_data: RewardInput) -> RewardOutput:
        n = len(input_data.trajectory_rewards)
        if n == 0 or len(input_data.value_estimates) != n:
            raise RewardException("Invalid input lengths.")
            
        adv = [0.0] * n
        ret = [0.0] * n
        
        last_gae = 0.0
        # Iterate backwards
        for i in reversed(range(n)):
            r = input_data.trajectory_rewards[i]
            v = input_data.value_estimates[i]
            
            # Next value (0 if at end of trajectory)
            next_v = input_data.value_estimates[i+1] if i + 1 < n else 0.0
            
            # TD Error: delta = r + gamma * V(s') - V(s)
            delta = r + input_data.gamma * next_v - v
            
            # GAE: adv = delta + gamma * lam * next_adv
            last_gae = delta + input_data.gamma * input_data.lam * last_gae
            adv[i] = last_gae
            
            # Return = Advantage + Value
            ret[i] = last_gae + v
            
        mean_adv = sum(adv) / max(1, n)
        
        return RewardOutput(
            advantages=adv,
            returns=ret,
            mean_advantage=mean_adv
        )
