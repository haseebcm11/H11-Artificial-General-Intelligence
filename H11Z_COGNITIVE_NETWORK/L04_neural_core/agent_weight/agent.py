import json
import math
import random
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum, auto

logger = logging.getLogger(__name__)

class InitStrategy(Enum):
    XAVIER_UNIFORM = auto()
    KAIMING_NORMAL = auto()
    ORTHOGONAL = auto()
    SPARSE = auto()

class SoupStrategy(Enum):
    UNIFORM = auto()
    GREEDY = auto()

@dataclass
class TensorDef:
    name: str
    shape: Tuple[int, ...]
    data: List[float]
    mask: Optional[List[float]] = None

class H11WeightAgent:
    """
    H11-WEIGHT Agent: Handles tensor initializations, model soups, and lottery ticket pruning.
    """
    
    def __init__(self, config_path: str = None):
        self.tensors: Dict[str, TensorDef] = {}
        self.initial_states: Dict[str, List[float]] = {} # For lottery ticket
        
        self.init_strategy = InitStrategy.KAIMING_NORMAL
        self.soup_strategy = SoupStrategy.UNIFORM
        self.pruning_rate = 0.2
        
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        try:
            with open(config_path, 'r') as f:
                cfg = json.load(f)
            init_str = cfg.get("init_strategy", "kaiming_normal").upper()
            self.init_strategy = getattr(InitStrategy, init_str, InitStrategy.KAIMING_NORMAL)
            
            soup_str = cfg.get("soup_strategy", "uniform").upper()
            self.soup_strategy = getattr(SoupStrategy, soup_str, SoupStrategy.UNIFORM)
            
            self.pruning_rate = cfg.get("lottery_ticket_pruning_rate", 0.2)
        except Exception as e:
            logger.error(f"Config error: {e}")

    def _get_fan_in_out(self, shape: Tuple[int, ...]) -> Tuple[int, int]:
        if len(shape) == 2:
            fan_in, fan_out = shape[1], shape[0]
        elif len(shape) > 2:
            receptive_field_size = 1
            for s in shape[2:]:
                receptive_field_size *= s
            fan_in = shape[1] * receptive_field_size
            fan_out = shape[0] * receptive_field_size
        else:
            fan_in = fan_out = shape[0]
        return fan_in, fan_out

    def initialize_tensor(self, name: str, shape: Tuple[int, ...]) -> TensorDef:
        fan_in, fan_out = self._get_fan_in_out(shape)
        size = 1
        for s in shape:
            size *= s
            
        data = []
        if self.init_strategy == InitStrategy.XAVIER_UNIFORM:
            limit = math.sqrt(6.0 / (fan_in + fan_out))
            data = [random.uniform(-limit, limit) for _ in range(size)]
        elif self.init_strategy == InitStrategy.KAIMING_NORMAL:
            std = math.sqrt(2.0 / fan_in)
            data = [random.gauss(0, std) for _ in range(size)]
        elif self.init_strategy == InitStrategy.SPARSE:
            std = 0.01
            sparsity = 0.1
            data = [random.gauss(0, std) if random.random() < sparsity else 0.0 for _ in range(size)]
        else:
            # Fallback uniform
            data = [random.uniform(-0.1, 0.1) for _ in range(size)]
            
        tensor = TensorDef(name, shape, data, mask=[1.0]*size)
        self.tensors[name] = tensor
        self.initial_states[name] = list(data)
        return tensor

    def identify_lottery_ticket(self, name: str) -> None:
        """
        Prunes the smallest weights according to the pruning rate and resets the remaining weights
        to their initial values (Lottery Ticket Hypothesis).
        """
        if name not in self.tensors:
            return
            
        tensor = self.tensors[name]
        initial = self.initial_states[name]
        
        # Sort indices by absolute magnitude
        indexed_data = [(abs(val), idx) for idx, val in enumerate(tensor.data)]
        indexed_data.sort(key=lambda x: x[0])
        
        prune_count = int(len(tensor.data) * self.pruning_rate)
        
        # Update mask
        for i in range(prune_count):
            idx = indexed_data[i][1]
            tensor.mask[idx] = 0.0
            
        # Reset to initial
        for i in range(len(tensor.data)):
            if tensor.mask[i] > 0.0:
                tensor.data[i] = initial[i]
            else:
                tensor.data[i] = 0.0

    def combine_model_soups(self, name: str, state_dicts: List[List[float]]) -> None:
        """
        Combines multiple checkpoints of a tensor into a single 'soup'.
        """
        if not state_dicts or name not in self.tensors:
            return
            
        size = len(self.tensors[name].data)
        avg_data = [0.0] * size
        
        if self.soup_strategy == SoupStrategy.UNIFORM:
            n = len(state_dicts)
            for state in state_dicts:
                for i in range(size):
                    avg_data[i] += state[i] / n
            self.tensors[name].data = avg_data

if __name__ == "__main__":
    agent = H11WeightAgent()
    tensor = agent.initialize_tensor("fc1", (10, 10))
    agent.identify_lottery_ticket("fc1")
    print(f"Mask zeros: {tensor.mask.count(0.0)}")
