import numpy as np
import random
from typing import List, Tuple, Dict
from dataclasses import dataclass

@dataclass
class Experience:
    state: np.ndarray
    action: int
    reward: float

class ExperienceReplay:
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.buffer: List[Experience] = []
        self.position = 0

    def add(self, experience: Experience):
        if len(self.buffer) < self.max_size:
            self.buffer.append(experience)
        else:
            self.buffer[self.position] = experience
            self.position = (self.position + 1) % self.max_size

    def sample(self, batch_size: int) -> List[Experience]:
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))

class DistributionShiftDetector:
    def __init__(self, baseline_data: np.ndarray, threshold: float = 0.05):
        self.baseline_mean = np.mean(baseline_data, axis=0)
        self.baseline_std = np.std(baseline_data, axis=0) + 1e-8
        self.threshold = threshold

    def detect(self, incoming_data: np.ndarray) -> Tuple[bool, float]:
        """
        A highly simplified MMD-like heuristic using standardized distance.
        """
        incoming_mean = np.mean(incoming_data, axis=0)
        distance = np.linalg.norm((incoming_mean - self.baseline_mean) / self.baseline_std)
        shift_score = float(distance / len(self.baseline_mean))
        return shift_score > self.threshold, shift_score

class EWCManager:
    def __init__(self, ewc_lambda: float = 400.0):
        self.ewc_lambda = ewc_lambda
        self.fisher_diagonals: Dict[str, np.ndarray] = {}
        self.optimal_weights: Dict[str, np.ndarray] = {}

    def compute_fisher(self, task_name: str, data: np.ndarray, current_weights: np.ndarray):
        """
        Simulate computing the empirical Fisher Information Matrix diagonal.
        """
        # In reality, this requires gradients of the log likelihood.
        # We simulate it with variance of the data features mapped to weights.
        pseudo_fisher = np.var(data, axis=0) * np.abs(current_weights)
        self.fisher_diagonals[task_name] = pseudo_fisher
        self.optimal_weights[task_name] = np.copy(current_weights)

    def calculate_penalty(self, current_weights: np.ndarray) -> float:
        penalty = 0.0
        for task_name in self.fisher_diagonals:
            fisher = self.fisher_diagonals[task_name]
            opt_w = self.optimal_weights[task_name]
            penalty += np.sum(fisher * (current_weights - opt_w) ** 2)
        return (self.ewc_lambda / 2) * penalty

class ContinualLearner:
    def __init__(self, input_dim: int):
        self.weights = np.random.randn(input_dim) * 0.1
        self.replay = ExperienceReplay()
        self.ewc = EWCManager()
        self.step_count = 0

    def online_update(self, data_x: np.ndarray, data_y: np.ndarray, task_name: str):
        self.step_count += 1
        
        # Simulate gradient computation
        predictions = np.dot(data_x, self.weights)
        errors = predictions - data_y
        base_gradient = np.dot(data_x.T, errors) / len(data_y)
        
        # Add EWC penalty gradient
        ewc_grad = np.zeros_like(self.weights)
        for t_name in self.ewc.fisher_diagonals:
            if t_name != task_name:
                fisher = self.ewc.fisher_diagonals[t_name]
                opt_w = self.ewc.optimal_weights[t_name]
                ewc_grad += self.ewc.ewc_lambda * fisher * (self.weights - opt_w)
                
        total_gradient = base_gradient + ewc_grad
        self.weights -= 0.01 * total_gradient
        
        # Update EWC matrices post-task (simplified trigger)
        if self.step_count % 100 == 0:
            self.ewc.compute_fisher(task_name, data_x, self.weights)
