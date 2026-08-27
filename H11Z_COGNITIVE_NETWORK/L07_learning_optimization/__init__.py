"""
Layer 7: Learning & Optimization
H11 Cognitive Substrate
"""

from .forward import ForwardAgent
from .loss import LossAgent
from .backprop import BackpropAgent
from .gradient import GradientAgent
from .autograd import AutogradAgent
from .optimizer import OptimizerAgent
from .adamw import AdamwAgent
from .learningrate import LearningrateAgent
from .momentum import MomentumAgent
from .regularization import RegularizationAgent
from .gradclip import GradclipAgent
from .mixedprecision import MixedprecisionAgent
from .curriculum import CurriculumAgent
from .selfplay import SelfplayAgent
from .rl import RlAgent
from .rlhf import RlhfAgent
from .dpo import DpoAgent
from .reward import RewardAgent
from .finetune import FinetuneAgent
from .lora import LoraAgent
from .pretrain import PretrainAgent
from .distillation import DistillationAgent

__all__ = [
    'ForwardAgent', 'LossAgent', 'BackpropAgent', 'GradientAgent', 'AutogradAgent', 'OptimizerAgent', 'AdamwAgent', 'LearningrateAgent', 'MomentumAgent', 'RegularizationAgent', 'GradclipAgent', 'MixedprecisionAgent', 'CurriculumAgent', 'SelfplayAgent', 'RlAgent', 'RlhfAgent', 'DpoAgent', 'RewardAgent', 'FinetuneAgent', 'LoraAgent', 'PretrainAgent', 'DistillationAgent'
]
