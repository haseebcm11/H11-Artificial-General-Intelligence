import logging
import math
import heapq
import random
from typing import List, Dict, Any, Optional, Tuple, Callable, Protocol

logger = logging.getLogger(__name__)

class SearchState(Protocol):
    def is_goal(self) -> bool:
        ...
    def get_successors(self) -> List[Tuple['SearchState', float, Any]]:
        ...
    def __hash__(self) -> int:
        ...
    def __eq__(self, other: Any) -> bool:
        ...

class SearchAlgorithm:
    def search(self, initial_state: SearchState, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

class AStarSearch(SearchAlgorithm):
    def __init__(self, heuristic_fn: Callable[[SearchState], float]):
        self.heuristic = heuristic_fn

    def search(self, initial_state: SearchState, **kwargs) -> Dict[str, Any]:
        open_set = []
        heapq.heappush(open_set, (0.0, id(initial_state), initial_state))
        
        came_from: Dict[SearchState, Tuple[SearchState, Any]] = {}
        g_score: Dict[SearchState, float] = {initial_state: 0.0}
        nodes_expanded = 0
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            
            if current.is_goal():
                return self._reconstruct_path(came_from, current, nodes_expanded)
                
            nodes_expanded += 1
            
            for next_state, cost, action in current.get_successors():
                tentative_g = g_score[current] + cost
                
                if next_state not in g_score or tentative_g < g_score[next_state]:
                    came_from[next_state] = (current, action)
                    g_score[next_state] = tentative_g
                    f_score = tentative_g + self.heuristic(next_state)
                    heapq.heappush(open_set, (f_score, id(next_state), next_state))
                    
        return {"status": "FAILED", "nodes_expanded": nodes_expanded}

    def _reconstruct_path(self, came_from, current, nodes_expanded):
        path = []
        while current in came_from:
            current, action = came_from[current]
            path.append(action)
        path.reverse()
        return {"status": "SUCCESS", "path": path, "nodes_expanded": nodes_expanded}

class MCTSNode:
    def __init__(self, state: SearchState, parent: Optional['MCTSNode'] = None, action: Any = None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children: List['MCTSNode'] = []
        self.visits = 0
        self.value = 0.0
        self.untried_actions = state.get_successors()

class MCTSSearch(SearchAlgorithm):
    def __init__(self, exploration_constant: float = 1.414):
        self.c = exploration_constant

    def search(self, initial_state: SearchState, max_iterations: int = 1000, **kwargs) -> Dict[str, Any]:
        root = MCTSNode(initial_state)
        
        for _ in range(max_iterations):
            node = self._tree_policy(root)
            reward = self._default_policy(node.state)
            self._backpropagate(node, reward)
            
        best_child = max(root.children, key=lambda c: c.visits) if root.children else None
        
        if best_child:
            return {"status": "SUCCESS", "best_action": best_child.action, "visits": root.visits}
        return {"status": "FAILED"}
        
    def _tree_policy(self, node: MCTSNode) -> MCTSNode:
        while not node.state.is_goal():
            if node.untried_actions:
                return self._expand(node)
            else:
                if not node.children:
                    break
                node = self._best_child(node)
        return node
        
    def _expand(self, node: MCTSNode) -> MCTSNode:
        idx = random.randrange(len(node.untried_actions))
        next_state, _, action = node.untried_actions.pop(idx)
        child = MCTSNode(next_state, parent=node, action=action)
        node.children.append(child)
        return child
        
    def _best_child(self, node: MCTSNode) -> MCTSNode:
        return max(
            node.children,
            key=lambda c: (c.value / c.visits) + self.c * math.sqrt(2 * math.log(node.visits) / c.visits)
        )
        
    def _default_policy(self, state: SearchState) -> float:
        # Random rollout until terminal state
        current = state
        depth = 0
        while not current.is_goal() and depth < 100:
            successors = current.get_successors()
            if not successors:
                break
            current, _, _ = random.choice(successors)
            depth += 1
        return 1.0 if current.is_goal() else 0.0

    def _backpropagate(self, node: MCTSNode, reward: float):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

class H11SearchAgent:
    def __init__(self):
        self.algorithms = {
            "A_STAR": AStarSearch(heuristic_fn=lambda s: 0.0),
            "MCTS": MCTSSearch()
        }
        
    def execute_search(self, initial_state: SearchState, algo_name: str, **kwargs) -> Dict[str, Any]:
        if algo_name not in self.algorithms:
            raise ValueError(f"Unknown algorithm {algo_name}")
            
        algo = self.algorithms[algo_name]
        return algo.search(initial_state, **kwargs)

if __name__ == "__main__":
    agent = H11SearchAgent()
    print("H11-SEARCH agent initialized.")
