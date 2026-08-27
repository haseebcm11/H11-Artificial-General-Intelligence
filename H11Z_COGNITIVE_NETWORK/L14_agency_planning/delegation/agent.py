import math
import heapq
import dataclasses
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum

class CapabilityDimension(Enum):
    COMPUTE = "compute"
    MEMORY = "memory"
    REASONING = "reasoning"
    IO_BOUND = "io_bound"
    CREATIVITY = "creativity"
    CODE_GEN = "code_gen"
    DATA_PROCESSING = "data_processing"
    VISION = "vision"

@dataclasses.dataclass
class CapabilityVector:
    dimensions: Dict[CapabilityDimension, float]
    
    def distance_to(self, other: 'CapabilityVector') -> float:
        """
        Calculates a weighted, asymmetric distance between this capability requirement
        and another agent's capability profile.
        Penalizes heavily if the agent is missing required capabilities, but 
        less so if the agent has excess capabilities.
        """
        dist = 0.0
        for dim, req_val in self.dimensions.items():
            agent_val = other.dimensions.get(dim, 0.0)
            diff = req_val - agent_val
            # If the requirement is higher than capability, high penalty.
            # If capability is higher, negligible penalty.
            dist += diff**2 if diff > 0 else (diff * 0.1)**2
        return math.sqrt(dist)

@dataclasses.dataclass
class TaskRequirement:
    task_id: str
    description: str
    required_capabilities: CapabilityVector
    estimated_complexity: float
    dependencies: List[str] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class DelegateeProfile:
    agent_id: str
    capabilities: CapabilityVector
    max_capacity: float
    current_load: float = 0.0
    reliability_score: float = 1.0

@dataclasses.dataclass
class DelegationAssignment:
    task_id: str
    assigned_agent: str
    estimated_duration: float
    confidence_score: float

class DelegationPolicy(Enum):
    STRICT_CAPABILITY = "strict_capability"
    LOAD_BALANCED = "load_balanced"
    HIGH_RELIABILITY = "high_reliability"

class TaskDependencyGraph:
    """
    Manages task dependencies and execution topologies for multi-step delegations.
    """
    def __init__(self, tasks: List[TaskRequirement]):
        self.tasks = {t.task_id: t for t in tasks}
        self.edges = {t.task_id: set(t.dependencies) for t in tasks}
        self.reverse_edges = {t.task_id: set() for t in tasks}
        
        for t_id, deps in self.edges.items():
            for d in deps:
                if d in self.reverse_edges:
                    self.reverse_edges[d].add(t_id)

    def topological_sort(self) -> List[List[TaskRequirement]]:
        """
        Returns tasks grouped by independent execution layers (parallel execution stages).
        Ensures dependencies are resolved before subsequent stages execute.
        """
        in_degree = {t: len(deps) for t, deps in self.edges.items()}
        queue = [t for t, deg in in_degree.items() if deg == 0]
        
        layers = []
        while queue:
            next_queue = []
            layer_tasks = []
            for t_id in queue:
                layer_tasks.append(self.tasks[t_id])
                for dependent in self.reverse_edges[t_id]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_queue.append(dependent)
            layers.append(layer_tasks)
            queue = next_queue
            
        if sum(len(layer) for layer in layers) != len(self.tasks):
            raise ValueError("Cycle detected in task dependencies preventing delegation")
            
        return layers

class TaskDelegator:
    """
    Core delegation system mapping tasks to agents using bipartite matching 
    modified for capacity constraints and multi-dimensional capability distance.
    """
    def __init__(self, policy: DelegationPolicy = DelegationPolicy.LOAD_BALANCED):
        self.policy = policy
        self.registry: Dict[str, DelegateeProfile] = {}
        self.active_assignments: Dict[str, DelegationAssignment] = {}
        
    def register_delegatee(self, profile: DelegateeProfile):
        """Register a sub-agent for potential delegation."""
        self.registry[profile.agent_id] = profile
        
    def _calculate_fitness_score(self, task: TaskRequirement, delegatee: DelegateeProfile) -> float:
        """
        Calculates fitness score [0, 1] for a task given a delegatee's profile.
        Takes into account the chosen delegation policy.
        """
        dist = task.required_capabilities.distance_to(delegatee.capabilities)
        # Normalize capability distance to a [0, 1] scale score using negative exponential
        capability_score = math.exp(-dist)
        
        load_ratio = delegatee.current_load / max(1e-5, delegatee.max_capacity)
        capacity_score = 1.0 - load_ratio if load_ratio < 1.0 else -10.0
        
        if self.policy == DelegationPolicy.STRICT_CAPABILITY:
            return capability_score * 0.8 + capacity_score * 0.2
        elif self.policy == DelegationPolicy.LOAD_BALANCED:
            return capability_score * 0.4 + capacity_score * 0.6
        elif self.policy == DelegationPolicy.HIGH_RELIABILITY:
            return capability_score * 0.4 + capacity_score * 0.2 + delegatee.reliability_score * 0.4
        
        return capability_score
        
    def plan_delegation_chain(self, tasks: List[TaskRequirement]) -> List[List[DelegationAssignment]]:
        """
        Uses the TaskDependencyGraph to plan a multi-tier delegation strategy.
        """
        graph = TaskDependencyGraph(tasks)
        layers = graph.topological_sort()
        
        delegation_plan = []
        for layer in layers:
            assignments = self._route_layer(layer)
            delegation_plan.append(assignments)
            
        return delegation_plan

    def _route_layer(self, tasks: List[TaskRequirement]) -> List[DelegationAssignment]:
        """
        Routes a batch of parallel tasks to optimal agents using a greedy assignment 
        strategy optimized by a max-heap of fitness scores.
        """
        assignments = []
        
        # Priority Queue for assignments: (-score, task_id, agent_id)
        # Max-heap via negative scores
        pq: List[Tuple[float, str, str]] = []
        
        for task in tasks:
            for agent_id, delegatee in self.registry.items():
                if delegatee.current_load >= delegatee.max_capacity:
                    continue
                score = self._calculate_fitness_score(task, delegatee)
                if score > 0:
                    heapq.heappush(pq, (-score, task.task_id, agent_id))
                    
        assigned_tasks: Set[str] = set()
        
        # Extract best assignments
        while pq and len(assigned_tasks) < len(tasks):
            neg_score, t_id, a_id = heapq.heappop(pq)
            if t_id in assigned_tasks:
                continue
                
            delegatee = self.registry[a_id]
            # Verify capacity dynamically
            task = next(t for t in tasks if t.task_id == t_id)
            load_impact = task.estimated_complexity
            
            if delegatee.current_load + load_impact <= delegatee.max_capacity:
                delegatee.current_load += load_impact
                assigned_tasks.add(t_id)
                
                estimated_duration = load_impact / max(0.1, delegatee.reliability_score)
                assignment = DelegationAssignment(
                    task_id=t_id,
                    assigned_agent=a_id,
                    estimated_duration=estimated_duration,
                    confidence_score=-neg_score
                )
                assignments.append(assignment)
                self.active_assignments[t_id] = assignment
                
        # Handle unassigned tasks due to capacity limits or strict constraints
        for task in tasks:
            if task.task_id not in assigned_tasks:
                raise RuntimeError(f"Capacity exhaustion or capability deficit for task: {task.task_id}")
                
        return assignments

    def monitor_delegatees(self) -> Dict[str, str]:
        """
        Monitors assigned delegatees and identifies stragglers or failures.
        Returns a map of task_id -> status
        """
        status_map = {}
        for task_id, assignment in self.active_assignments.items():
            agent = self.registry.get(assignment.assigned_agent)
            if not agent:
                status_map[task_id] = "ORPHANED_AGENT_LOST"
                continue
                
            # Simulated telemetry/progress check based on reliability
            if agent.reliability_score < 0.5:
                status_map[task_id] = "AT_RISK_DEGRADED"
            elif agent.current_load > agent.max_capacity * 0.9:
                status_map[task_id] = "THROTTLED"
            else:
                status_map[task_id] = "ON_TRACK"
                
        return status_map

    def aggregate_results(self, partial_results: Dict[str, any]) -> Dict[str, any]:
        """
        Map-reduce aggregation for completed task delegations.
        Releases load from agents once tasks finish.
        """
        aggregated = {"status": "success", "results": {}}
        for t_id, result in partial_results.items():
            if t_id in self.active_assignments:
                aggregated["results"][t_id] = result
                
                # Release load from the assigned agent
                a_id = self.active_assignments[t_id].assigned_agent
                if a_id in self.registry:
                    # Subtract load, ensure it doesn't drop below 0
                    freed_load = self.registry[a_id].current_load - 1.0 # placeholder reduction
                    self.registry[a_id].current_load = max(0.0, freed_load)
                
                del self.active_assignments[t_id]
                
        return aggregated
