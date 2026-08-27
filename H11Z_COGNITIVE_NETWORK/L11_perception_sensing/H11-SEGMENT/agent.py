"""
Agent Module: L11_SEGMENT
Agent Class: SegmentAgent

Semantic and instance segmentation evaluation computing Dice coefficient 2|A cap B| / (|A| + |B|), Mean IoU, and polygon boundary contour analysis.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L11_SEGMENT"


class SegmentError(ValueError):
    """Raised when SegmentAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SegmentAgentInput:
    mask_gt: list[int] = field(default_factory=lambda: [1, 1, 1, 0, 0, 1, 1, 0])
    mask_pred: list[int] = field(default_factory=lambda: [1, 1, 0, 0, 0, 1, 1, 1])


@dataclass(frozen=True)
class SegmentAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    dice_coefficient: float = 0.0
    iou: float = 0.0


class SegmentAgent:
    """
    Semantic and instance segmentation evaluation computing Dice coefficient 2|A cap B| / (|A| + |B|), Mean IoU, and polygon boundary contour analysis.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SegmentAgentInput) -> SegmentAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        gt, pred = inputs.mask_gt, inputs.mask_pred
        intersection = sum(g & p for g, p in zip(gt, pred))
        sum_gt, sum_pred = sum(gt), sum(pred)
        union = sum_gt + sum_pred - intersection
        dice = (2.0 * intersection) / max(sum_gt + sum_pred, 1e-6)
        iou = intersection / max(union, 1e-6)
        metrics = {"intersection": float(intersection), "union": float(union), "dice": round(dice, 4), "iou": round(iou, 4)}
        return SegmentAgentOutput(status="COMPLETED", score=round(iou, 4), metrics=metrics, dice_coefficient=round(dice, 4), iou=round(iou, 4))
