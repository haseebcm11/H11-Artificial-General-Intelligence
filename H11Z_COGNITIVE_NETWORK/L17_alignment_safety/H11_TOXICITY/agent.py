from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
import math

class ToxicityAxis(Enum):
    INSULT = "insult"
    PROFANITY = "profanity"
    THREAT = "threat"
    HARASSMENT = "harassment"
    MICROAGGRESSION = "microaggression"

@dataclass
class ToxicityScore:
    axis: ToxicityAxis
    raw_score: float
    confidence: float
    trigger_tokens: List[str] = field(default_factory=list)

@dataclass
class AnalysisResult:
    is_toxic: bool
    overall_score: float
    breakdown: Dict[ToxicityAxis, ToxicityScore]
    context_adjusted: bool

class H11ToxicityAgent:
    """
    H11-TOXICITY: Context-aware multi-dimensional toxicity filtering agent.
    """
    def __init__(self, thresholds: Dict[ToxicityAxis, float]):
        self.thresholds = thresholds
        self.history_buffer: List[str] = []
        self.weights = {"ngram": 0.3, "transformer": 0.7}

    def _ngram_heuristic(self, text: str) -> Dict[ToxicityAxis, float]:
        # Dummy n-gram logic
        scores = {axis: 0.01 for axis in ToxicityAxis}
        if "hate" in text.lower():
            scores[ToxicityAxis.INSULT] = 0.4
        if "kill" in text.lower():
            scores[ToxicityAxis.THREAT] = 0.8
        return scores

    def _transformer_inference(self, text: str, context: List[str]) -> Dict[ToxicityAxis, float]:
        # Dummy transformer logic simulating context awareness
        base = 0.1 * (len(context) + 1)
        return {
            ToxicityAxis.INSULT: min(1.0, base + 0.1),
            ToxicityAxis.PROFANITY: 0.05,
            ToxicityAxis.THREAT: 0.1,
            ToxicityAxis.HARASSMENT: min(1.0, base),
            ToxicityAxis.MICROAGGRESSION: 0.2
        }

    def analyze_utterance(self, text: str, update_history: bool = True) -> AnalysisResult:
        ngram_scores = self._ngram_heuristic(text)
        trans_scores = self._transformer_inference(text, self.history_buffer)

        breakdown = {}
        overall_score = 0.0
        is_toxic = False

        for axis in ToxicityAxis:
            combined = (ngram_scores[axis] * self.weights["ngram"]) + \
                       (trans_scores.get(axis, 0.0) * self.weights["transformer"])
            
            trigger = []
            if combined > 0.5:
                trigger = ["synthetic_trigger"]

            breakdown[axis] = ToxicityScore(
                axis=axis,
                raw_score=combined,
                confidence=0.85, # Simulated
                trigger_tokens=trigger
            )

            if combined > self.thresholds.get(axis, 1.0):
                is_toxic = True
            
            overall_score += combined

        overall_score = overall_score / len(ToxicityAxis)

        if update_history:
            self.history_buffer.append(text)
            if len(self.history_buffer) > 5:
                self.history_buffer.pop(0)

        return AnalysisResult(
            is_toxic=is_toxic,
            overall_score=overall_score,
            breakdown=breakdown,
            context_adjusted=len(self.history_buffer) > 0
        )

    def clear_context(self):
        self.history_buffer.clear()
