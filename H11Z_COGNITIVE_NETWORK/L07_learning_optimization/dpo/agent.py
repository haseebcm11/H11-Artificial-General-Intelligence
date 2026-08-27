import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-DPO"

@dataclass
class DpoInput:
    policy_chosen_logps: typing.List[float]
    policy_rejected_logps: typing.List[float]
    ref_chosen_logps: typing.List[float]
    ref_rejected_logps: typing.List[float]
    beta: float = 0.1
    label_smoothing: float = 0.0

@dataclass
class DpoOutput:
    preference_loss: float
    chosen_rewards: typing.List[float]
    rejected_rewards: typing.List[float]
    reward_margins: typing.List[float]

class DpoException(Exception):
    pass

class DpoAgent:
    """
    Implements Direct Preference Optimization (DPO) for the H11 Cognitive Substrate.
    Features:
    - Bradley-Terry model loss
    - Implicit reward modeling
    - KL penalty via beta coefficient
    """
    def __init__(self):
        self.margin_history = []

    def _sigmoid(self, x: float) -> float:
        if x >= 0:
            return 1.0 / (1.0 + math.exp(-x))
        else:
            z = math.exp(x)
            return z / (1.0 + z)

    def process(self, input_data: DpoInput) -> DpoOutput:
        n = len(input_data.policy_chosen_logps)
        if not n:
            raise DpoException("Input lists cannot be empty.")
            
        beta = input_data.beta
        losses = []
        chosen_rewards = []
        rejected_rewards = []
        margins = []
        
        for i in range(n):
            pi_w = input_data.policy_chosen_logps[i]
            pi_l = input_data.policy_rejected_logps[i]
            ref_w = input_data.ref_chosen_logps[i]
            ref_l = input_data.ref_rejected_logps[i]
            
            # Implicit rewards
            r_chosen = beta * (pi_w - ref_w)
            r_rejected = beta * (pi_l - ref_l)
            
            chosen_rewards.append(r_chosen)
            rejected_rewards.append(r_rejected)
            
            diff = r_chosen - r_rejected
            margins.append(diff)
            
            # DPO Loss: -log(sigmoid(r_chosen - r_rejected))
            loss = -math.log(self._sigmoid(diff) + 1e-10)
            losses.append(loss)
            
        avg_loss = sum(losses) / n
        self.margin_history.extend(margins)
        
        return DpoOutput(
            preference_loss=avg_loss,
            chosen_rewards=chosen_rewards,
            rejected_rewards=rejected_rewards,
            reward_margins=margins
        )
