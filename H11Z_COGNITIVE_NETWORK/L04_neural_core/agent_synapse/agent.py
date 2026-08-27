import json
import logging
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import random

logger = logging.getLogger(__name__)

class PlasticityRule(Enum):
    STATIC = auto()
    HEBBIAN = auto()
    OJA = auto()
    STDP = auto()

@dataclass
class Synapse:
    synapse_id: str
    pre_neuron_id: str
    post_neuron_id: str
    weight: float
    eligibility_trace: float = 0.0
    age: int = 0
    is_active: bool = True

class H11SynapseAgent:
    """
    H11-SYNAPSE Agent: Manages synaptic connections, weights, pruning, and localized plasticity.
    """
    
    def __init__(self, config_path: str = None):
        self.synapses: Dict[str, Synapse] = {}
        # Indexed by pre and post for fast lookup
        self.pre_index: Dict[str, List[str]] = {}
        self.post_index: Dict[str, List[str]] = {}
        
        self.rule = PlasticityRule.STATIC
        self.pruning_threshold = 1e-4
        self.learning_rate = 0.001
        self.sparsity_target = 0.9
        
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        try:
            with open(config_path, 'r') as f:
                cfg = json.load(f)
            rule_str = cfg.get("plasticity_rule", "static").upper()
            self.rule = getattr(PlasticityRule, rule_str, PlasticityRule.STATIC)
            self.pruning_threshold = cfg.get("pruning_threshold", 1e-4)
            self.learning_rate = cfg.get("learning_rate", 0.001)
            self.sparsity_target = cfg.get("sparsity_target", 0.9)
            logger.info(f"Synapse config loaded: Rule={self.rule}")
        except Exception as e:
            logger.error(f"Failed to load synapse config: {e}")

    def create_synapse(self, pre_id: str, post_id: str, init_weight: float) -> str:
        syn_id = f"{pre_id}->{post_id}"
        if syn_id in self.synapses:
            return syn_id
            
        self.synapses[syn_id] = Synapse(syn_id, pre_id, post_id, init_weight)
        
        if pre_id not in self.pre_index:
            self.pre_index[pre_id] = []
        self.pre_index[pre_id].append(syn_id)
        
        if post_id not in self.post_index:
            self.post_index[post_id] = []
        self.post_index[post_id].append(syn_id)
        
        return syn_id

    def get_weight(self, pre_id: str, post_id: str) -> float:
        syn_id = f"{pre_id}->{post_id}"
        if syn_id in self.synapses and self.synapses[syn_id].is_active:
            return self.synapses[syn_id].weight
        return 0.0

    def update_plasticity(self, pre_activations: Dict[str, float], post_activations: Dict[str, float]):
        """
        Applies local learning rules based on pre and post synaptic activity.
        """
        if self.rule == PlasticityRule.STATIC:
            return
            
        for syn_id, syn in self.synapses.items():
            if not syn.is_active:
                continue
                
            pre_act = pre_activations.get(syn.pre_neuron_id, 0.0)
            post_act = post_activations.get(syn.post_neuron_id, 0.0)
            
            if self.rule == PlasticityRule.HEBBIAN:
                dw = self.learning_rate * pre_act * post_act
                syn.weight += dw
            elif self.rule == PlasticityRule.OJA:
                # Oja's rule prevents unbounded weight growth
                dw = self.learning_rate * post_act * (pre_act - post_act * syn.weight)
                syn.weight += dw
            elif self.rule == PlasticityRule.STDP:
                # Simplified STDP without explicit spike times, using eligibility traces
                syn.eligibility_trace = 0.9 * syn.eligibility_trace + pre_act
                dw = self.learning_rate * syn.eligibility_trace * post_act
                syn.weight += dw

            syn.age += 1

    def apply_global_update(self, pre_id: str, post_id: str, gradient: float):
        """
        Applies an external gradient update (e.g. from backprop).
        """
        syn_id = f"{pre_id}->{post_id}"
        if syn_id in self.synapses:
            self.synapses[syn_id].weight -= self.learning_rate * gradient

    def prune_synapses(self) -> int:
        """
        Removes synapses with weights below the pruning threshold to enforce sparsity.
        """
        pruned_count = 0
        for syn in self.synapses.values():
            if syn.is_active and abs(syn.weight) < self.pruning_threshold:
                syn.is_active = False
                syn.weight = 0.0
                pruned_count += 1
        return pruned_count

    def get_active_synapses(self) -> List[Synapse]:
        return [s for s in self.synapses.values() if s.is_active]

if __name__ == "__main__":
    agent = H11SynapseAgent()
    agent.create_synapse("A", "B", 0.5)
    agent.rule = PlasticityRule.HEBBIAN
    agent.update_plasticity({"A": 1.0}, {"B": 0.8})
    print(agent.get_weight("A", "B"))
