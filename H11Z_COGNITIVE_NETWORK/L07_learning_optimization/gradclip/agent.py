import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-GRADCLIP"

@dataclass
class GradclipInput:
    gradients: typing.Dict[str, typing.List[float]]
    clip_threshold: float = 1.0
    norm_type: float = 2.0
    error_on_nonfinite: bool = False

@dataclass
class GradclipOutput:
    clipped_gradients: typing.Dict[str, typing.List[float]]
    clipping_factor: float
    total_norm: float

class GradclipException(Exception):
    pass

class GradclipAgent:
    """
    Implements gradient clipping strategies for the H11 Cognitive Substrate.
    Features:
    - Global norm clipping
    - L2/L-infinity norm calculations
    - Non-finite value protection
    """
    def __init__(self):
        self.clip_count = 0

    def process(self, input_data: GradclipInput) -> GradclipOutput:
        if not input_data.gradients:
            raise GradclipException("No gradients to clip.")
            
        total_norm = 0.0
        
        # Calculate total norm
        if input_data.norm_type == math.inf:
            for g_list in input_data.gradients.values():
                for g in g_list:
                    if math.isnan(g) or math.isinf(g):
                        if input_data.error_on_nonfinite:
                            raise GradclipException(f"Non-finite gradient encountered: {g}")
                    total_norm = max(total_norm, abs(g))
        else:
            p = input_data.norm_type
            sum_norm = 0.0
            for g_list in input_data.gradients.values():
                for g in g_list:
                    if math.isnan(g) or math.isinf(g):
                        if input_data.error_on_nonfinite:
                            raise GradclipException(f"Non-finite gradient encountered: {g}")
                    sum_norm += abs(g) ** p
            total_norm = sum_norm ** (1.0 / p)
            
        clip_coef = input_data.clip_threshold / (total_norm + 1e-6)
        clip_coef_clamped = min(1.0, clip_coef)
        
        if clip_coef_clamped < 1.0:
            self.clip_count += 1
            
        clipped = {}
        for k, g_list in input_data.gradients.items():
            clipped[k] = [g * clip_coef_clamped for g in g_list]
            
        return GradclipOutput(
            clipped_gradients=clipped,
            clipping_factor=clip_coef_clamped,
            total_norm=total_norm
        )
