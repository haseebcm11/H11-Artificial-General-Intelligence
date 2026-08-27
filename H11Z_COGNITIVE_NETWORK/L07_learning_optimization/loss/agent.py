import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-LOSS"

@dataclass
class LossInput:
    predictions: typing.List[float]
    targets: typing.List[float]
    loss_type: str = "cross_entropy"
    label_smoothing: float = 0.0
    delta: float = 1.0 # for Huber loss

@dataclass
class LossOutput:
    loss_value: float
    loss_gradients: typing.List[float]
    metrics: typing.Dict[str, float]

class LossException(Exception):
    pass

class LossAgent:
    """
    Implements core Loss Functions for the H11 Cognitive Substrate.
    Features:
    - Cross Entropy with Label Smoothing
    - MSE / Huber loss
    - Gradient derivation
    """
    def __init__(self):
        pass

    def _cross_entropy(self, preds: typing.List[float], targets: typing.List[float], smoothing: float) -> typing.Tuple[float, typing.List[float]]:
        # Softmax
        max_p = max(preds)
        exps = [math.exp(p - max_p) for p in preds]
        sum_exp = sum(exps)
        probs = [e / sum_exp for e in exps]
        
        k = len(preds)
        loss = 0.0
        grads = []
        for p, t in zip(probs, targets):
            smooth_t = t * (1 - smoothing) + smoothing / k
            loss -= smooth_t * math.log(p + 1e-12)
            grads.append(p - smooth_t)
            
        return loss, grads
        
    def _mse(self, preds: typing.List[float], targets: typing.List[float]) -> typing.Tuple[float, typing.List[float]]:
        loss = sum((p - t)**2 for p, t in zip(preds, targets)) / len(preds)
        grads = [2 * (p - t) / len(preds) for p, t in zip(preds, targets)]
        return loss, grads

    def process(self, input_data: LossInput) -> LossOutput:
        if len(input_data.predictions) != len(input_data.targets):
            raise LossException("Predictions and targets must have same length.")
            
        if input_data.loss_type == "cross_entropy":
            l_val, l_grads = self._cross_entropy(input_data.predictions, input_data.targets, input_data.label_smoothing)
        elif input_data.loss_type == "mse":
            l_val, l_grads = self._mse(input_data.predictions, input_data.targets)
        else:
            raise LossException(f"Unsupported loss type: {input_data.loss_type}")
            
        # compute basic metrics (e.g. accuracy if one-hot)
        pred_class = input_data.predictions.index(max(input_data.predictions))
        targ_class = input_data.targets.index(max(input_data.targets)) if sum(input_data.targets) > 0 else -1
        acc = 1.0 if pred_class == targ_class else 0.0
        
        return LossOutput(
            loss_value=l_val,
            loss_gradients=l_grads,
            metrics={"accuracy": acc}
        )
