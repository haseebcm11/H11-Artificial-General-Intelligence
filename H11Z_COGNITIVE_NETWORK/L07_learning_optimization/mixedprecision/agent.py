import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-MIXEDPRECISION"

@dataclass
class MixedprecisionInput:
    fp32_loss: float
    current_scale: float = 65536.0
    growth_interval: int = 2000
    backoff_factor: float = 0.5
    growth_factor: float = 2.0
    nan_or_inf_found: bool = False

@dataclass
class MixedprecisionOutput:
    scaled_loss: float
    new_scale: float
    skip_update: bool

class MixedprecisionException(Exception):
    pass

class MixedprecisionAgent:
    """
    Implements Dynamic Loss Scaling for Mixed Precision Training in the H11 Cognitive Substrate.
    Features:
    - FP16/BF16 underflow prevention
    - Dynamic scaling adjustments
    - Overflow detection
    """
    def __init__(self):
        self.good_steps = 0

    def process(self, input_data: MixedprecisionInput) -> MixedprecisionOutput:
        scale = input_data.current_scale
        skip = False
        
        if input_data.nan_or_inf_found or math.isnan(input_data.fp32_loss) or math.isinf(input_data.fp32_loss):
            # Overflow condition
            scale *= input_data.backoff_factor
            self.good_steps = 0
            skip = True
            scaled_loss = input_data.fp32_loss # Not useful, will be skipped
        else:
            # Normal condition
            scaled_loss = input_data.fp32_loss * scale
            self.good_steps += 1
            
            if self.good_steps >= input_data.growth_interval:
                scale *= input_data.growth_factor
                self.good_steps = 0
                
        # Guard against scale going to 0
        scale = max(1.0, scale)
        
        return MixedprecisionOutput(
            scaled_loss=scaled_loss,
            new_scale=scale,
            skip_update=skip
        )
