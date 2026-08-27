import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-RLHF"

@dataclass
class RlhfInput:
    policy_logits: typing.List[float]
    reference_logits: typing.List[float]
    advantages: typing.List[float]
    clip_epsilon: float = 0.2

@dataclass
class RlhfOutput:
    clipped_loss: float
    kl_divergence: float
    clip_fraction: float

class RlhfException(Exception):
    pass

class RlhfAgent:
    """
    Implements PPO Clipping Objective for RLHF in the H11 Cognitive Substrate.
    Features:
    - Surrogate objective clipping
    - KL divergence tracking
    - Clip fraction monitoring
    """
    def __init__(self):
        pass

    def process(self, input_data: RlhfInput) -> RlhfOutput:
        n = len(input_data.policy_logits)
        if n == 0 or len(input_data.reference_logits) != n or len(input_data.advantages) != n:
            raise RlhfException("Mismatched or empty inputs.")
            
        loss_sum = 0.0
        kl_sum = 0.0
        clip_count = 0
        eps = input_data.clip_epsilon
        
        for p_log, r_log, adv in zip(input_data.policy_logits, input_data.reference_logits, input_data.advantages):
            # Probability ratio r_t(theta) = pi_theta / pi_ref = exp(log_pi_theta - log_pi_ref)
            ratio = math.exp(p_log - r_log)
            
            # Surrogate objectives
            surr1 = ratio * adv
            
            clipped_ratio = min(max(ratio, 1.0 - eps), 1.0 + eps)
            surr2 = clipped_ratio * adv
            
            # PPO objective: minimize negative of min(surr1, surr2)
            step_loss = -min(surr1, surr2)
            loss_sum += step_loss
            
            # KL approx: (log_pi_ref - log_pi_theta) or via ratio
            # Approx KL = log(ratio) - ratio + 1 ? Typically just log_pi_ref - log_pi_theta if comparing logprobs
            kl = r_log - p_log
            kl_sum += kl
            
            if abs(ratio - 1.0) > eps:
                clip_count += 1
                
        avg_loss = loss_sum / n
        avg_kl = kl_sum / n
        frac = clip_count / n
        
        return RlhfOutput(
            clipped_loss=avg_loss,
            kl_divergence=avg_kl,
            clip_fraction=frac
        )
