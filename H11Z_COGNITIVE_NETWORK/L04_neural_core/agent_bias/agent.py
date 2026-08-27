import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class BiasParameter:
    name: str
    values: List[float]
    running_mean: List[float]
    running_var: List[float]

class H11BiasAgent:
    """
    H11-BIAS Agent: Handles bias parameter initialization, batch norm folding, and dynamic shifts.
    """
    def __init__(self, config_path: str = None):
        self.biases: Dict[str, BiasParameter] = {}
        self.init_value = 0.01
        self.dynamic_shifting = True
        self.momentum = 0.1
        
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        try:
            with open(config_path, 'r') as f:
                cfg = json.load(f)
            self.init_value = cfg.get("init_value", 0.01)
            self.dynamic_shifting = cfg.get("dynamic_shifting", True)
            self.momentum = cfg.get("momentum", 0.1)
        except Exception as e:
            logger.error(f"Config error: {e}")

    def initialize_bias(self, name: str, size: int) -> BiasParameter:
        # Initialize slightly positive to avoid dead ReLUs
        values = [self.init_value] * size
        mean = [0.0] * size
        var = [1.0] * size
        bp = BiasParameter(name, values, mean, var)
        self.biases[name] = bp
        return bp

    def update_statistics(self, name: str, batch_mean: List[float], batch_var: List[float]):
        """
        Updates running mean and variance for dynamic shifting / normalization.
        """
        if not self.dynamic_shifting or name not in self.biases:
            return
            
        bp = self.biases[name]
        for i in range(len(bp.values)):
            bp.running_mean[i] = (1 - self.momentum) * bp.running_mean[i] + self.momentum * batch_mean[i]
            bp.running_var[i] = (1 - self.momentum) * bp.running_var[i] + self.momentum * batch_var[i]

    def fold_batch_norm(self, name: str, gamma: List[float], beta: List[float], eps: float = 1e-5) -> List[float]:
        """
        Folds batch normalization parameters into the bias for inference optimization.
        b_folded = gamma * (b - mean) / sqrt(var + eps) + beta
        """
        if name not in self.biases:
            return []
            
        bp = self.biases[name]
        folded_bias = []
        for i in range(len(bp.values)):
            std = (bp.running_var[i] + eps) ** 0.5
            val = gamma[i] * (bp.values[i] - bp.running_mean[i]) / std + beta[i]
            folded_bias.append(val)
            
        return folded_bias

if __name__ == "__main__":
    agent = H11BiasAgent()
    bp = agent.initialize_bias("conv1_bias", 64)
    print(f"Initialized with: {bp.values[0]}")
