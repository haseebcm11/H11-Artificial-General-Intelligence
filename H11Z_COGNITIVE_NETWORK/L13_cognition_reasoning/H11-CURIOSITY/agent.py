import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import math
import uuid

class ExplorationMode(Enum):
    NOVELTY_SEEKING = "novelty_seeking"
    SURPRISE_BASED = "surprise_based"
    INFORMATION_GAIN = "information_gain"

@dataclass
class Observation:
    state_vector: np.ndarray
    timestamp: float
    metadata: Dict[str, any] = field(default_factory=dict)
    
@dataclass
class CuriosityResponse:
    intrinsic_reward: float
    surprise_level: float
    novelty_score: float
    generated_questions: List[str]
    suggested_action: Optional[str] = None

class PredictionModel:
    """Simple linear prediction model for computing prediction error (surprise)."""
    def __init__(self, state_dim: int, learning_rate: float = 0.01):
        self.state_dim = state_dim
        self.learning_rate = learning_rate
        # Predicts next state based on current state (simplified, ignores action for now)
        self.weights = np.random.randn(state_dim, state_dim) * 0.1
        self.bias = np.zeros(state_dim)

    def predict(self, state: np.ndarray) -> np.ndarray:
        return np.dot(self.weights, state) + self.bias

    def update(self, state: np.ndarray, next_state: np.ndarray) -> float:
        prediction = self.predict(state)
        error = next_state - prediction
        loss = np.mean(error ** 2)
        
        # Simple gradient descent
        grad_w = -2 * np.outer(error, state) / self.state_dim
        grad_b = -2 * error / self.state_dim
        
        self.weights -= self.learning_rate * grad_w
        self.bias -= self.learning_rate * grad_b
        
        return float(loss)

class EpisodicMemory:
    """Maintains a buffer of past states to compute novelty (e.g., KNN distance)."""
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.buffer: List[np.ndarray] = []

    def add(self, state: np.ndarray):
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append(state)

    def compute_novelty(self, state: np.ndarray, k: int = 3) -> float:
        if not self.buffer:
            return 1.0
        
        distances = [np.linalg.norm(state - b) for b in self.buffer]
        distances.sort()
        
        # Average distance to k nearest neighbors
        k_nearest = distances[:min(k, len(distances))]
        avg_dist = sum(k_nearest) / len(k_nearest)
        
        # Normalize roughly (assuming unit norm states for simplicity or scaling)
        novelty = 1.0 - math.exp(-avg_dist)
        return novelty

class CuriosityAgent:
    """
    H11-CURIOSITY Agent
    Drives exploration using intrinsic motivation (surprise and novelty).
    """
    def __init__(self, state_dim: int, config: Dict[str, any]):
        self.state_dim = state_dim
        self.config = config
        self.prediction_model = PredictionModel(
            state_dim=state_dim, 
            learning_rate=config.get("prediction_learning_rate", 0.01)
        )
        self.memory = EpisodicMemory(capacity=config.get("memory_capacity", 1000))
        self.last_observation: Optional[np.ndarray] = None
        self.exploration_mode = ExplorationMode(config.get("default_mode", "surprise_based"))

    def process_observation(self, obs: Observation) -> CuriosityResponse:
        """Processes a new observation and computes intrinsic motivation signals."""
        state = obs.state_vector
        novelty = self.memory.compute_novelty(state)
        self.memory.add(state)
        
        surprise = 0.0
        if self.last_observation is not None:
            surprise = self.prediction_model.update(self.last_observation, state)
            
        self.last_observation = state
        
        intrinsic_reward = self._compute_intrinsic_reward(surprise, novelty)
        questions = self._generate_questions(surprise, novelty, obs.metadata)
        
        return CuriosityResponse(
            intrinsic_reward=intrinsic_reward,
            surprise_level=surprise,
            novelty_score=novelty,
            generated_questions=questions
        )

    def _compute_intrinsic_reward(self, surprise: float, novelty: float) -> float:
        w_s = self.config.get("weight_surprise", 0.5)
        w_n = self.config.get("weight_novelty", 0.5)
        return w_s * surprise + w_n * novelty

    def _generate_questions(self, surprise: float, novelty: float, metadata: Dict[str, any]) -> List[str]:
        questions = []
        if surprise > self.config.get("surprise_threshold", 0.5):
            context = metadata.get("context", "this outcome")
            questions.append(f"Why did {context} deviate so significantly from expectations?")
            questions.append("What hidden variables might be influencing this state?")
            
        if novelty > self.config.get("novelty_threshold", 0.7):
            concept = metadata.get("concept_name", "this new state")
            questions.append(f"What are the core properties of {concept}?")
            questions.append(f"How does {concept} relate to previously known entities?")
            
        return questions

    def get_status(self) -> Dict[str, any]:
        return {
            "memory_size": len(self.memory.buffer),
            "prediction_weights_norm": float(np.linalg.norm(self.prediction_model.weights)),
            "current_mode": self.exploration_mode.value
        }

if __name__ == "__main__":
    agent = CuriosityAgent(state_dim=16, config={
        "prediction_learning_rate": 0.05,
        "weight_surprise": 0.6,
        "weight_novelty": 0.4,
        "surprise_threshold": 0.1,
        "novelty_threshold": 0.5
    })
    
    # Simulate a sequence of observations
    for i in range(5):
        state = np.random.randn(16)
        obs = Observation(state_vector=state, timestamp=float(i), metadata={"context": f"Step {i}"})
        response = agent.process_observation(obs)
        print(f"Step {i} | Surprise: {response.surprise_level:.4f} | Novelty: {response.novelty_score:.4f} | Reward: {response.intrinsic_reward:.4f}")
        for q in response.generated_questions:
            print(f"  ? {q}")
