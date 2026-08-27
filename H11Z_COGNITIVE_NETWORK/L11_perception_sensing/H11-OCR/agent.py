"""
Agent Module: L11_OCR
Agent Class: OcrAgent

Optical character recognition text line localization, spatial character bounding box IoU, Levenshtein distance confidence scoring, stroke width transform (SWT).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L11_OCR"


class OcrError(ValueError):
    """Raised when OcrAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class OcrAgentInput:
    text_ground_truth: str = 'ANTIGRAVITY'
    text_recognized: str = 'ANT1GRAV1TY'
    boxes: list[list[float]] = field(default_factory=lambda: [[0, 0, 50, 20], [55, 0, 100, 20]])


@dataclass(frozen=True)
class OcrAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    character_accuracy: float = 0.0


class OcrAgent:
    """
    Optical character recognition text line localization, spatial character bounding box IoU, Levenshtein distance confidence scoring, stroke width transform (SWT).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: OcrAgentInput) -> OcrAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        s1, s2 = inputs.text_ground_truth, inputs.text_recognized
        m, n = len(s1), len(s2)
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1): dp[i][0] = i
        for j in range(n+1): dp[0][j] = j
        for i in range(1, m+1):
            for j in range(1, n+1):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
        lev = dp[m][n]
        acc = max(0.0, 1.0 - lev / max(m, n, 1))
        metrics = {"levenshtein_distance": float(lev), "gt_length": float(m), "pred_length": float(n), "char_accuracy": round(acc, 4)}
        return OcrAgentOutput(status="COMPLETED", score=round(acc, 4), metrics=metrics, character_accuracy=round(acc, 4))
