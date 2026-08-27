import math
import typing
from dataclasses import dataclass, field

AGENT_ID = "H11-CURRICULUM"

@dataclass
class CurriculumInput:
    dataset_samples: typing.List[str]
    model_loss_history: typing.List[float]
    current_epoch: int = 0
    total_epochs: int = 100
    initial_competence: float = 0.01

@dataclass
class CurriculumOutput:
    sample_indices: typing.List[int]
    difficulty_threshold: float
    competence_score: float

class CurriculumException(Exception):
    pass

class CurriculumAgent:
    """
    Implements curriculum learning strategies for the H11 Cognitive Substrate.
    Features:
    - Competence-based curriculum
    - Self-paced learning
    - Data difficulty metrics
    """
    def __init__(self):
        self.competence_history = []

    def _compute_competence(self, step: int, total_steps: int, c0: float) -> float:
        # Competence c(t) = min(1, sqrt(t * (1 - c_0^2) / T + c_0^2))
        if total_steps == 0:
            return 1.0
        c = math.sqrt((step * (1 - c0**2)) / total_steps + c0**2)
        return min(1.0, c)

    def _score_difficulty(self, sample_idx: int) -> float:
        # Pseudo-difficulty scoring based on index (assuming sorted easy-to-hard)
        return (sample_idx % 100) / 100.0

    def process(self, input_data: CurriculumInput) -> CurriculumOutput:
        if not input_data.dataset_samples:
            raise CurriculumException("Empty dataset samples provided.")
            
        step = len(input_data.model_loss_history) + input_data.current_epoch
        competence = self._compute_competence(step, input_data.total_epochs * 100, input_data.initial_competence)
        
        self.competence_history.append(competence)
        
        selected_indices = []
        for i, sample in enumerate(input_data.dataset_samples):
            diff = self._score_difficulty(i)
            if diff <= competence:
                selected_indices.append(i)
                
        # Ensure we always return at least some samples
        if not selected_indices:
            selected_indices = [0]
            
        return CurriculumOutput(
            sample_indices=selected_indices, 
            difficulty_threshold=competence,
            competence_score=competence
        )
