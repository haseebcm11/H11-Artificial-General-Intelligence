# H11-SEARCH: Search & Exploration Agent

## Overview
H11-SEARCH implements algorithms for state-space exploration, heuristic search, and decision-time planning. It is designed to navigate complex search spaces in reasoning, theorem proving, and game-theoretic scenarios.

## Capabilities
- **Uninformed Search**: BFS, DFS, Iterative Deepening.
- **Informed Search**: A*, IDA*, Best-First Search.
- **Probabilistic/Heuristic Exploration**: Monte Carlo Tree Search (MCTS), Beam Search.
- **Search Space Pruning**: Alpha-beta pruning, state memoization, and semantic deduplication.

## Architecture
- `SearchProblem`: Protocol defining states, actions, and goal tests.
- `AStarEngine`: Heuristic-driven shortest-path search.
- `MCTSEngine`: Upper Confidence Bound applied to Trees (UCT) for probabilistic search.
- `BeamSearchEngine`: Width-restricted breadth-first search for NLP/LLM decoding scenarios.

## References
1. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths.
2. Kocsis, L., & Szepesvári, C. (2006). Bandit Based Monte-Carlo Planning.
