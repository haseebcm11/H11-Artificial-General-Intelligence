import json
import random
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LayerConfig:
    name: str
    in_features: int
    out_features: int
    is_residual: bool
    drop_path_rate: float

class H11LayerAgent:
    """
    H11-LAYER Agent: Orchestrates layer compositions, residual scaling, and stochastic depth.
    """
    def __init__(self, config_path: str = None):
        self.layers: List[LayerConfig] = []
        
        self.use_residual = True
        self.stochastic_depth_prob = 0.1
        self.layer_scale_init = 1e-4
        
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        try:
            with open(config_path, 'r') as f:
                cfg = json.load(f)
            self.use_residual = cfg.get("use_residual", True)
            self.stochastic_depth_prob = cfg.get("stochastic_depth_prob", 0.1)
            self.layer_scale_init = cfg.get("layer_scale_init", 1e-4)
        except Exception as e:
            logger.error(f"Config error: {e}")

    def add_layer(self, name: str, in_feat: int, out_feat: int, is_res: bool = None) -> None:
        is_res = is_res if is_res is not None else self.use_residual
        # Residual implies in_feat == out_feat usually, but let's just record it
        self.layers.append(LayerConfig(name, in_feat, out_feat, is_res, self.stochastic_depth_prob))

    def validate_stack(self) -> bool:
        """
        Validates that dimensions align across the sequential stack.
        """
        if not self.layers:
            return True
            
        current_dim = self.layers[0].in_features
        for idx, layer in enumerate(self.layers):
            if layer.in_features != current_dim:
                logger.error(f"Mismatch at {layer.name}: expected {current_dim}, got {layer.in_features}")
                return False
            current_dim = layer.out_features
            
        return True

    def forward_stochastic(self, layer_idx: int, x: List[float], f_x: List[float], is_training: bool) -> List[float]:
        """
        Applies stochastic depth and residual connection.
        y = x + DropPath(f(x))
        """
        layer = self.layers[layer_idx]
        if not layer.is_residual or len(x) != len(f_x):
            return f_x # Cannot apply residual
            
        drop_rate = layer.drop_path_rate
        
        if is_training:
            if random.random() < drop_rate:
                # Drop path
                return x
            else:
                # Scale by 1/(1-p) during training? Often done to keep expected value
                scale = 1.0 / (1.0 - drop_rate)
                return [a + scale * b for a, b in zip(x, f_x)]
        else:
            # Inference: just add
            return [a + b for a, b in zip(x, f_x)]

    def compute_layer_scale(self, f_x: List[float], gamma: List[float]) -> List[float]:
        """
        Applies LayerScale (Touvron et al.) to the residual branch.
        """
        if len(f_x) != len(gamma):
            return f_x
        return [val * g for val, g in zip(f_x, gamma)]

if __name__ == "__main__":
    agent = H11LayerAgent()
    agent.add_layer("l1", 64, 64)
    agent.add_layer("l2", 64, 128)
    print(f"Stack valid: {agent.validate_stack()}")
