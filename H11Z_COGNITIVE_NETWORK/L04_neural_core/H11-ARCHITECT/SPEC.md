# H11-ARCHITECT: Architecture Search

## Overview
The H11-ARCHITECT agent implements Neural Architecture Search (NAS) routines to discover optimal network topologies. It explores the search space using gradient-based, evolutionary, or RL methods to find Pareto-optimal models.

## Capabilities
- **Search Space Definition**: Defines macro and micro structures for the supernet.
- **DARTS (Differentiable Architecture Search)**: Continuous relaxation of architecture representation.
- **Evolutionary NAS**: Mutation, crossover, and population management for architecture strings.
- **One-Shot Supernet**: Training a single large model with path dropout to evaluate subnetworks.
