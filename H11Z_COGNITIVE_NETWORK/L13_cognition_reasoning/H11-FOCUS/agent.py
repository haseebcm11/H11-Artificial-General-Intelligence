import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time

@dataclass
class Stimulus:
    id: str
    feature_vector: np.ndarray
    intensity: float
    relevance_tags: List[str]
    is_task_relevant: bool = False
    
@dataclass
class GoalState:
    id: str
    target_tags: List[str]
    priority: float

@dataclass
class AttentionAllocation:
    stimulus_id: str
    allocated_capacity: float
    salience_score: float

class FocusAgent:
    """
    H11-FOCUS Agent
    Manages the attentional bottleneck, computing salience and allocating cognitive capacity.
    """
    def __init__(self, config: Dict[str, any]):
        self.capacity = config.get("max_attention_capacity", 100.0)
        self.w_top_down = config.get("top_down_weight", 0.6)
        self.w_bottom_up = config.get("bottom_up_weight", 0.4)
        self.inhibition_rate = config.get("distractor_inhibition_rate", 0.2)
        
        self.current_goals: List[GoalState] = []
        self.sustained_focus_target: Optional[str] = None
        self.focus_duration: float = 0.0
        self._last_update_time = time.time()

    def set_goals(self, goals: List[GoalState]):
        self.current_goals = sorted(goals, key=lambda x: x.priority, reverse=True)

    def _compute_bottom_up_salience(self, stimulus: Stimulus) -> float:
        """Intrinsic prominence based on intensity or physical contrast."""
        # In a real model, this would use center-surround differences on the feature_vector.
        return stimulus.intensity * np.linalg.norm(stimulus.feature_vector)

    def _compute_top_down_salience(self, stimulus: Stimulus) -> float:
        """Relevance to current goals."""
        if not self.current_goals:
            return 0.0
            
        max_relevance = 0.0
        for goal in self.current_goals:
            # Overlap between stimulus tags and goal tags
            overlap = set(stimulus.relevance_tags).intersection(set(goal.target_tags))
            relevance = (len(overlap) / max(1, len(goal.target_tags))) * goal.priority
            if relevance > max_relevance:
                max_relevance = relevance
                
        return max_relevance

    def filter_and_allocate(self, stimuli: List[Stimulus]) -> List[AttentionAllocation]:
        """
        Processes a field of stimuli, computes overall salience, and allocates the limited capacity.
        """
        allocations = []
        salience_map = {}
        
        # 1. Compute Salience
        for stim in stimuli:
            bu = self._compute_bottom_up_salience(stim)
            td = self._compute_top_down_salience(stim)
            
            # Inhibition of Return / Distractor inhibition
            inhibition = 0.0
            if not stim.is_task_relevant and stim.id != self.sustained_focus_target:
                inhibition = self.inhibition_rate * bu
                
            overall_salience = (self.w_bottom_up * bu) + (self.w_top_down * td) - inhibition
            salience_map[stim.id] = max(0.0, overall_salience)

        # 2. Sort by salience
        sorted_stimuli = sorted(stimuli, key=lambda x: salience_map[x.id], reverse=True)

        # 3. Allocate Capacity (Attentional Bottleneck)
        remaining_capacity = self.capacity
        for stim in sorted_stimuli:
            salience = salience_map[stim.id]
            if salience <= 0 or remaining_capacity <= 0:
                break
                
            # Non-linear allocation based on salience relative to capacity
            allocation = min(remaining_capacity, salience * 10.0) # Scaling factor
            remaining_capacity -= allocation
            
            allocations.append(AttentionAllocation(
                stimulus_id=stim.id,
                allocated_capacity=allocation,
                salience_score=salience
            ))
            
        # Update sustained focus tracking
        if allocations:
            primary_target = allocations[0].stimulus_id
            now = time.time()
            if primary_target == self.sustained_focus_target:
                self.focus_duration += (now - self._last_update_time)
            else:
                self.sustained_focus_target = primary_target
                self.focus_duration = 0.0
            self._last_update_time = now

        return allocations

if __name__ == "__main__":
    agent = FocusAgent({"max_attention_capacity": 50.0})
    
    agent.set_goals([
        GoalState(id="find_food", target_tags=["food", "edible"], priority=1.0),
        GoalState(id="avoid_predators", target_tags=["danger", "movement"], priority=0.8)
    ])
    
    env_stimuli = [
        Stimulus("apple", np.array([1.0, 0.0]), intensity=2.0, relevance_tags=["food", "red"], is_task_relevant=True),
        Stimulus("loud_noise", np.array([0.0, 1.0]), intensity=9.0, relevance_tags=["sound"], is_task_relevant=False),
        Stimulus("tiger", np.array([1.0, 1.0]), intensity=5.0, relevance_tags=["danger", "movement", "animal"], is_task_relevant=True)
    ]
    
    allocs = agent.filter_and_allocate(env_stimuli)
    print("Attention Allocation:")
    for a in allocs:
        print(f"Target: {a.stimulus_id:12} | Capacity: {a.allocated_capacity:.1f} | Salience: {a.salience_score:.2f}")
    
    print(f"Sustained Focus Target: {agent.sustained_focus_target}, Duration: {agent.focus_duration:.2f}s")
