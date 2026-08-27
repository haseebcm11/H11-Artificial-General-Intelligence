import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-PRETRAIN"

@dataclass
class PretrainInput:
    masked_predictions: typing.List[float]
    targets: typing.List[float]
    mask_ratio: float = 0.15
    vocab_size: int = 50000

@dataclass
class PretrainOutput:
    pretraining_loss: float
    masking_efficiency: float
    perplexity: float

class PretrainException(Exception):
    pass

class PretrainAgent:
    """
    Implements Pretraining Objectives (MLM) for the H11 Cognitive Substrate.
    Features:
    - Masked Language Modeling loss
    - Perplexity tracking
    """
    def __init__(self):
        pass

    def process(self, input_data: PretrainInput) -> PretrainOutput:
        if len(input_data.masked_predictions) != len(input_data.targets):
            raise PretrainException("Mismatched prediction and target lengths.")
            
        loss = 0.0
        count = 0
        
        for p, t in zip(input_data.masked_predictions, input_data.targets):
            # p represents the probability assigned to the true target token
            # Cross-entropy for the target token: -log(p)
            p = min(max(p, 1e-12), 1.0 - 1e-12)
            loss -= math.log(p)
            count += 1
            
        avg_loss = loss / max(1, count)
        ppl = math.exp(avg_loss) if avg_loss < 20 else float('inf')
        
        # Masking efficiency is a simulated metric of how well the model learned from the mask ratio
        efficiency = 1.0 - math.exp(-avg_loss) 
        
        return PretrainOutput(
            pretraining_loss=avg_loss,
            masking_efficiency=efficiency,
            perplexity=ppl
        )
