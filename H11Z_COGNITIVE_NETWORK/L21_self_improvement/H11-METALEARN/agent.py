import numpy as np
import uuid
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field

@dataclass
class TaskData:
    task_id: str
    support_set_x: np.ndarray
    support_set_y: np.ndarray
    query_set_x: np.ndarray
    query_set_y: np.ndarray

@dataclass
class MetaParameters:
    weights: np.ndarray
    learning_rate: float
    inner_steps: int

class TaskEmbeddingNetwork:
    """
    Simulates mapping a task into a latent embedding space to modulate meta-learning.
    """
    def __init__(self, embedding_dim: int = 64):
        self.embedding_dim = embedding_dim
        self.projection_matrix = np.random.randn(128, self.embedding_dim) * 0.01

    def embed_task(self, task: TaskData) -> np.ndarray:
        # Dummy embedding based on support set variance
        feature_var = np.var(task.support_set_x, axis=0)
        # Pad or truncate to 128
        feature_vec = np.resize(feature_var, 128)
        embedding = np.dot(feature_vec, self.projection_matrix)
        return embedding / (np.linalg.norm(embedding) + 1e-9)

class FewShotAdapter:
    def __init__(self, meta_params: MetaParameters):
        self.meta_params = meta_params

    def inner_loop_update(self, task: TaskData) -> np.ndarray:
        """
        Simulates the inner loop update (fast adaptation) in MAML.
        """
        adapted_weights = np.copy(self.meta_params.weights)
        
        for _ in range(self.meta_params.inner_steps):
            # Simulated gradient descent step
            predictions = np.dot(task.support_set_x, adapted_weights)
            errors = predictions - task.support_set_y
            gradient = np.dot(task.support_set_x.T, errors) / len(task.support_set_y)
            adapted_weights -= self.meta_params.learning_rate * gradient
            
        return adapted_weights

class MetaLearningController:
    def __init__(self, input_dim: int = 10, meta_lr: float = 0.001):
        self.meta_params = MetaParameters(
            weights=np.random.randn(input_dim) * 0.1,
            learning_rate=0.01,
            inner_steps=5
        )
        self.meta_lr = meta_lr
        self.adapter = FewShotAdapter(self.meta_params)
        self.task_embedder = TaskEmbeddingNetwork()

    def meta_update(self, tasks: List[TaskData]) -> float:
        """
        Outer loop of MAML.
        """
        meta_gradient = np.zeros_like(self.meta_params.weights)
        total_meta_loss = 0.0

        for task in tasks:
            # 1. Fast adaptation
            adapted_w = self.adapter.inner_loop_update(task)
            
            # 2. Evaluate on query set
            predictions = np.dot(task.query_set_x, adapted_w)
            errors = predictions - task.query_set_y
            loss = np.mean(errors ** 2)
            total_meta_loss += loss
            
            # 3. Compute meta-gradient (first-order approximation)
            task_meta_grad = np.dot(task.query_set_x.T, errors) / len(task.query_set_y)
            meta_gradient += task_meta_grad

        # 4. Meta update
        meta_gradient /= len(tasks)
        self.meta_params.weights -= self.meta_lr * meta_gradient
        
        return total_meta_loss / len(tasks)
