"""statemachine: Agent for Finite State Machines and Path Optimization.

L18_orchestration_control - Substrate

Implements a deterministic State Machine router. Computes the optimal transition
path through an FSM/HSM using Dijkstra's algorithm over a composite edge weight
defined by operational cost and transition probability negative log-likelihood.
"""
from __future__ import annotations

import math
import time
import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set, Any

AGENT_ID = "H11-STATEMACHINE"


class StateMachineError(ValueError):
    """Domain-specific error for statemachine."""
    pass


@dataclass(frozen=True)
class Transition:
    source: str
    target: str
    event: str
    cost: float
    probability: float = 1.0  # Must be in (0, 1]


@dataclass(frozen=True)
class StateMachineInput:
    states: List[str]
    transitions: List[Transition]
    initial_state: str
    target_state: str


@dataclass(frozen=True)
class StateMachineOutput:
    agent_id: str
    path: List[str]
    events: List[str]
    total_cost: float
    success_probability: float
    execution_time_ms: float


class StatemachineAgent:
    """Analytical engine for State Machine Optimization."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def process(self, input_data: Optional[StateMachineInput] = None) -> StateMachineOutput:
        start_time = time.perf_counter()
        if input_data is None:
            raise StateMachineError("Input data cannot be None")

        if input_data.initial_state not in input_data.states:
            raise StateMachineError(f"Initial state {input_data.initial_state} not in states")
        if input_data.target_state not in input_data.states:
            raise StateMachineError(f"Target state {input_data.target_state} not in states")

        # Build adjacency list: source -> list of (target, event, weight, prob)
        adj: Dict[str, List[Tuple[str, str, float, float]]] = {s: [] for s in input_data.states}
        for t in input_data.transitions:
            if not (0.0 < t.probability <= 1.0):
                raise StateMachineError(f"Invalid probability {t.probability} for event {t.event}")
            
            # Composite weight: cost + penalty for low probability
            weight = t.cost - math.log(t.probability)
            if t.source in adj:
                adj[t.source].append((t.target, t.event, weight, t.probability))

        # Dijkstra's algorithm to find optimal path
        # Priority queue stores: (accumulated_weight, current_state)
        pq = [(0.0, input_data.initial_state)]
        
        # dist stores min weight to reach a state
        dist: Dict[str, float] = {s: float('inf') for s in input_data.states}
        dist[input_data.initial_state] = 0.0
        
        # parent stores (prev_state, event_used, probability_of_edge, edge_cost)
        parent: Dict[str, Tuple[str, str, float, float]] = {}

        while pq:
            d, u = heapq.heappop(pq)
            
            if d > dist[u]:
                continue
                
            if u == input_data.target_state:
                break
                
            for v, event, weight, prob in adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = (u, event, prob, weight)
                    heapq.heappush(pq, (dist[v], v))

        if dist[input_data.target_state] == float('inf'):
            raise StateMachineError(f"No valid path from {input_data.initial_state} to {input_data.target_state}")

        # Reconstruct path
        path = []
        events = []
        total_prob = 1.0
        actual_cost = 0.0
        
        curr = input_data.target_state
        while curr != input_data.initial_state:
            path.append(curr)
            prev, evt, p, w = parent[curr]
            events.append(evt)
            total_prob *= p
            actual_cost += (w + math.log(p)) # w = cost - log(p) => cost = w + log(p)
            curr = prev
            
        path.append(input_data.initial_state)
        
        path.reverse()
        events.reverse()

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return StateMachineOutput(
            agent_id=AGENT_ID,
            path=path,
            events=events,
            total_cost=round(actual_cost, 6),
            success_probability=round(total_prob, 6),
            execution_time_ms=round(elapsed_ms, 4)
        )
