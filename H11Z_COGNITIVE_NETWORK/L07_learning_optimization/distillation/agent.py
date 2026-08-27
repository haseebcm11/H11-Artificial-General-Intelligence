import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-DISTILLATION"

@dataclass
class DistillationInput:
    student_logits: typing.List[float]
    teacher_logits: typing.List[float]
    temperature: float = 2.0
    alpha: float = 0.5
    true_labels: typing.List[float] = field(default_factory=list)

@dataclass
class DistillationOutput:
    distillation_loss: float
    gradient_scaling: float
    kl_divergence: float

class DistillationException(Exception):
    pass

class DistillationAgent:
    """
    Implements Knowledge Distillation algorithms for the H11 Cognitive Substrate.
    Features:
    - KL Divergence with temperature scaling
    - Soft target alignment
    - Teacher-student divergence tracking
    """
    def __init__(self):
        self.running_loss = 0.0

    def _softmax_with_temp(self, logits: typing.List[float], t: float) -> typing.List[float]:
        max_l = max(logits)
        exp_l = [math.exp((l - max_l) / t) for l in logits]
        sum_exp = sum(exp_l)
        return [e / sum_exp for e in exp_l]

    def _compute_kl_divergence(self, p: typing.List[float], q: typing.List[float]) -> float:
        # KL(P || Q) = sum(P_i * log(P_i / Q_i))
        kl = 0.0
        for pi, qi in zip(p, q):
            if pi > 0:
                kl += pi * math.log(pi / (qi + 1e-12) + 1e-12)
        return kl

    def process(self, input_data: DistillationInput) -> DistillationOutput:
        if not input_data.student_logits or not input_data.teacher_logits:
            raise DistillationException("Logits cannot be empty.")
            
        t = input_data.temperature
        
        p_teacher = self._softmax_with_temp(input_data.teacher_logits, t)
        p_student = self._softmax_with_temp(input_data.student_logits, t)
        
        kl_div = self._compute_kl_divergence(p_teacher, p_student)
        
        # Soft loss
        soft_loss = (t ** 2) * kl_div
        
        # Total loss combining hard and soft (simulated)
        total_loss = input_data.alpha * soft_loss + (1 - input_data.alpha) * kl_div
        
        self.running_loss = 0.9 * self.running_loss + 0.1 * total_loss
        
        return DistillationOutput(
            distillation_loss=total_loss, 
            gradient_scaling=1.0 / (t + 1e-6),
            kl_divergence=kl_div
        )
