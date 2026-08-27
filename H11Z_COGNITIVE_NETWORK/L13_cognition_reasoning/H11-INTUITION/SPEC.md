# H11-INTUITION: Heuristic Intuition Agent

## Overview
The H11-INTUITION agent implements "System 1" fast-thinking mechanisms. It leverages pattern recognition, historical heuristics, and approximate reasoning to provide rapid, low-latency estimates and gut feelings, which can then guide "System 2" deep reasoning processes.

## Core Capabilities
- **Heuristic Search**: Rapidly pruning search spaces using rules-of-thumb.
- **Pattern-based Shortcuts**: Identifying isomorphic problems and applying cached solutions.
- **Approximate Reasoning**: Satisficing solutions when exact answers are computationally prohibitive.
- **System 1 Simulation**: Emulating intuition to generate fast priors for complex deliberation.

## Theoretical Foundations
- **Dual Process Theory**: Kahneman (2011) - System 1 (fast, instinctive) and System 2 (slow, analytical).
- **Satisficing**: Herbert Simon (1956) - Decision-making strategy that aims for a satisfactory or adequate result.
- **Heuristic Evaluation Functions**: Used in A* search and game theory (e.g., minimax algorithms).

## Architecture
- `PatternMatcher`: Compares current states to historical embeddings.
- `HeuristicEngine`: Applies domain-specific rules-of-thumb to compute fast estimates.
- `IntuitionResult`: Contains the fast guess, confidence, and recommended processing mode (fast vs slow).
