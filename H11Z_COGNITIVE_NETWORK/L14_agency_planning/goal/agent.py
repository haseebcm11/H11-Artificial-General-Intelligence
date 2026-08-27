import uuid
import time
import math
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto

class GoalType(Enum):
    TERMINAL = auto()
    INSTRUMENTAL = auto()

class GoalState(Enum):
    PENDING = auto()
    ACTIVE = auto()
    SUSPENDED = auto()
    COMPLETED = auto()
    FAILED = auto()
    ABANDONED = auto()

@dataclass
class SmartMetrics:
    specific_score: float
    measurable_score: float
    achievable_score: float
    relevant_score: float
    time_bound_score: float

    @property
    def is_smart(self) -> bool:
        return all(v > 0.5 for v in [
            self.specific_score, 
            self.measurable_score, 
            self.achievable_score,
            self.relevant_score, 
            self.time_bound_score
        ])

@dataclass
class GoalNode:
    description: str
    goal_type: GoalType
    intrinsic_utility: float
    deadline: Optional[float] = None
    goal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: GoalState = GoalState.PENDING
    smart_metrics: Optional[SmartMetrics] = None
    
    # Internal metrics for hierarchy
    computed_priority: float = 0.0
    created_at: float = field(default_factory=time.time)
    
    def evaluate_smartness(self, context_entropy: float, measurement_capability: float) -> None:
        """Heuristic evaluation of SMART criteria."""
        # Simple heuristic mappings for illustration
        specific = 1.0 - min(context_entropy, 1.0)
        measurable = measurement_capability
        achievable = 1.0 if self.goal_type == GoalType.INSTRUMENTAL else 0.8
        relevant = self.intrinsic_utility
        time_bound = 1.0 if self.deadline is not None else 0.1
        
        self.smart_metrics = SmartMetrics(
            specific_score=specific,
            measurable_score=measurable,
            achievable_score=achievable,
            relevant_score=relevant,
            time_bound_score=time_bound
        )

class GoalHierarchy:
    """Manages goals as a DAG of instrumental dependencies."""
    def __init__(self, discount_factor: float = 0.9):
        self.goals: Dict[str, GoalNode] = {}
        # adjacency list for edges: parent -> children (parent depends on children)
        self.dependencies: Dict[str, Set[str]] = {}
        # reverse lookup: child -> parents (child supports parents)
        self.supports: Dict[str, Set[str]] = {}
        self.discount_factor = discount_factor

    def add_goal(self, goal: GoalNode) -> None:
        self.goals[goal.goal_id] = goal
        self.dependencies[goal.goal_id] = set()
        self.supports[goal.goal_id] = set()

    def add_dependency(self, parent_id: str, child_id: str) -> None:
        if parent_id not in self.goals or child_id not in self.goals:
            raise ValueError("Both goals must exist in hierarchy.")
        if self._would_create_cycle(parent_id, child_id):
            raise ValueError("Adding dependency would create a cycle.")
        
        self.dependencies[parent_id].add(child_id)
        self.supports[child_id].add(parent_id)

    def _would_create_cycle(self, start_id: str, target_id: str) -> bool:
        # DFS to detect cycle
        visited = set()
        stack = [target_id]
        while stack:
            curr = stack.pop()
            if curr == start_id:
                return True
            if curr not in visited:
                visited.add(curr)
                stack.extend(self.dependencies.get(curr, set()))
        return False

    def remove_goal(self, goal_id: str) -> None:
        if goal_id not in self.goals:
            return
        
        # Cleanup dependencies
        for child_id in list(self.dependencies[goal_id]):
            self.supports[child_id].remove(goal_id)
        for parent_id in list(self.supports[goal_id]):
            self.dependencies[parent_id].remove(goal_id)
            
        del self.dependencies[goal_id]
        del self.supports[goal_id]
        del self.goals[goal_id]

    def update_priorities(self) -> None:
        """
        Backpropagates utility from terminal/parent goals down to instrumental leaves.
        P(child) = U(child) + gamma * sum(P(parent)) over all parents supported.
        """
        # Reset priorities to intrinsic
        for g in self.goals.values():
            g.computed_priority = g.intrinsic_utility

        # Topological sort for priority propagation (parents before children)
        # We need a reverse topological sort: starting from nodes with 0 in-degree in supports (terminal goals)
        in_degree = {gid: len(parents) for gid, parents in self.supports.items()}
        queue = [gid for gid, deg in in_degree.items() if deg == 0]
        
        topo_order = []
        while queue:
            curr = queue.pop(0)
            topo_order.append(curr)
            for child in self.dependencies[curr]:
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    queue.append(child)

        # Propagate priority
        for gid in topo_order:
            curr_goal = self.goals[gid]
            for child_id in self.dependencies[gid]:
                self.goals[child_id].computed_priority += (self.discount_factor * curr_goal.computed_priority)

class GoalManager:
    def __init__(self):
        self.hierarchy = GoalHierarchy()
        
    def submit_goal(self, 
                    description: str, 
                    goal_type: GoalType, 
                    utility: float, 
                    deadline: Optional[float] = None,
                    parent_ids: Optional[List[str]] = None) -> str:
        goal = GoalNode(
            description=description,
            goal_type=goal_type,
            intrinsic_utility=utility,
            deadline=deadline
        )
        goal.evaluate_smartness(context_entropy=0.2, measurement_capability=0.9)
        self.hierarchy.add_goal(goal)
        
        if parent_ids:
            for pid in parent_ids:
                self.hierarchy.add_dependency(pid, goal.goal_id)
                
        self.hierarchy.update_priorities()
        return goal.goal_id

    def update_goal_state(self, goal_id: str, new_state: GoalState) -> None:
        if goal_id not in self.hierarchy.goals:
            raise KeyError(f"Goal {goal_id} not found.")
        self.hierarchy.goals[goal_id].state = new_state
        
        if new_state in (GoalState.COMPLETED, GoalState.FAILED, GoalState.ABANDONED):
            self._handle_goal_termination(goal_id, new_state)

    def _handle_goal_termination(self, goal_id: str, state: GoalState) -> None:
        """Propagate termination effects."""
        node = self.hierarchy.goals[goal_id]
        if state == GoalState.COMPLETED:
            # Check if any parent goals can now be activated
            parents = self.hierarchy.supports[goal_id]
            for pid in parents:
                parent = self.hierarchy.goals[pid]
                if parent.state == GoalState.PENDING:
                    # check if all dependencies met
                    all_met = all(self.hierarchy.goals[d].state == GoalState.COMPLETED 
                                  for d in self.hierarchy.dependencies[pid])
                    if all_met:
                        parent.state = GoalState.ACTIVE
        elif state in (GoalState.FAILED, GoalState.ABANDONED):
            # Might need to fail parents or trigger replanning (simplified here)
            parents = self.hierarchy.supports[goal_id]
            for pid in parents:
                self.hierarchy.goals[pid].state = GoalState.SUSPENDED

    def get_active_goals_by_priority(self) -> List[GoalNode]:
        """Returns active goals sorted by computed priority."""
        self.hierarchy.update_priorities()
        
        # Apply time penalty for approaching deadlines
        now = time.time()
        active = []
        for g in self.hierarchy.goals.values():
            if g.state in (GoalState.ACTIVE, GoalState.PENDING):
                # Adjust priority if deadline is close
                adjusted_prio = g.computed_priority
                if g.deadline:
                    time_left = max(1.0, g.deadline - now)
                    # urgency multiplier
                    adjusted_prio *= (1.0 + 1000.0 / time_left)
                active.append((adjusted_prio, g))
                
        active.sort(key=lambda x: x[0], reverse=True)
        return [g for _, g in active]

    def resolve_conflicts(self, resource_requirements: Dict[str, Set[str]]) -> Dict[str, str]:
        """
        Identify and resolve resource conflicts between goals.
        Returns a mapping of goal_id -> resolution action (e.g. 'suspend', 'proceed').
        """
        # Sort goals by priority
        prioritized = self.get_active_goals_by_priority()
        allocated_resources = set()
        resolutions = {}
        
        for goal in prioritized:
            reqs = resource_requirements.get(goal.goal_id, set())
            if reqs.intersection(allocated_resources):
                resolutions[goal.goal_id] = "suspend"
                self.update_goal_state(goal.goal_id, GoalState.SUSPENDED)
            else:
                resolutions[goal.goal_id] = "proceed"
                allocated_resources.update(reqs)
                if goal.state == GoalState.PENDING:
                    self.update_goal_state(goal.goal_id, GoalState.ACTIVE)
                    
        return resolutions

if __name__ == "__main__":
    gm = GoalManager()
    t1 = gm.submit_goal("Survive", GoalType.TERMINAL, 1.0)
    i1 = gm.submit_goal("Find Food", GoalType.INSTRUMENTAL, 0.0, parent_ids=[t1])
    i2 = gm.submit_goal("Hunt", GoalType.INSTRUMENTAL, 0.0, parent_ids=[i1], deadline=time.time() + 3600)
    
    print("Prioritized Goals:")
    for g in gm.get_active_goals_by_priority():
        print(f"- {g.description}: P={g.computed_priority:.2f}, State={g.state.name}")
