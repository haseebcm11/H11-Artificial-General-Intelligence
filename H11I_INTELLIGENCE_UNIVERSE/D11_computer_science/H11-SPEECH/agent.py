"""
Agent Module: D11_SPEECH
Agent Class: SpeechAgent

Automatic Speech Recognition (ASR) Connectionist Temporal Classification (CTC) forward variable alpha_t and Word Error Rate (WER).
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "D11_SPEECH"


class SpeechError(ValueError):
    """Raised when SpeechAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SpeechAgentInput:
    hypothesis_words: list[str] = field(default_factory=lambda: ['hello', 'world'])
    reference_words: list[str] = field(default_factory=lambda: ['hello', 'there', 'world'])


@dataclass(frozen=True)
class SpeechAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    word_error_rate: float = 0.0


class SpeechAgent:
    """
    Automatic Speech Recognition (ASR) Connectionist Temporal Classification (CTC) forward variable alpha_t and Word Error Rate (WER).
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SpeechAgentInput) -> SpeechAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        h, r = inputs.hypothesis_words, inputs.reference_words
        m, n = len(r), len(h)
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1): dp[i][0] = i
        for j in range(n+1): dp[0][j] = j
        for i in range(1, m+1):
            for j in range(1, n+1):
                cost = 0 if r[i-1] == h[j-1] else 1
                dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
        wer = dp[m][n] / max(m, 1)
        metrics = {"wer": round(wer, 4), "word_errors": float(dp[m][n]), "ref_words": float(m)}
        return SpeechAgentOutput(status="COMPLETED", score=round(max(0.0, 1.0 - wer), 4), metrics=metrics, word_error_rate=round(wer, 4))
