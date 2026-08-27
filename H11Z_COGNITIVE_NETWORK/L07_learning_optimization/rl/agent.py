import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-RL"

@dataclass
class RlInput:
    advantages: typing.List[float]
    action_log_probs: typing.List[float]
    entropy_coef: float = 0.01

@dataclass
class RlOutput:
    policy_loss: float
    entropy_loss: float
    total_loss: float

class RlException(Exception):
    pass

class RlAgent:
    """
    Implements REINFORCE / Policy Gradient objective for the H11 Cognitive Substrate.
    Features:
    - Advantage weighting
    - Entropy regularization
    """
    def __init__(self):
        pass

    def process(self, input_data: RlInput) -> RlOutput:
        if len(input_data.advantages) != len(input_data.action_log_probs):
            raise RlException("Mismatched advantages and log probabilities.")
            
        n = len(input_data.advantages)
        if n == 0:
            return RlOutput(0.0, 0.0, 0.0)
            
        pg_loss = 0.0
        entropy = 0.0
        
        for adv, log_p in zip(input_data.advantages, input_data.action_log_probs):
            # Policy gradient loss: -A * log(pi)
            pg_loss -= adv * log_p
            
            # Approximate entropy: -p * log(p) approx -exp(log_p) * log_p
            p = math.exp(log_p)
            entropy -= p * log_p
            
        pg_loss /= n
        entropy /= n
        
        total = pg_loss - input_data.entropy_coef * entropy
        
        return RlOutput(
            policy_loss=pg_loss,
            entropy_loss=-entropy,
            total_loss=total
        )
