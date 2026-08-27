# H11-DECOMPOSE: Task Decomposition Agent

## Overview
The H11-DECOMPOSE agent is responsible for breaking down complex, high-level problems into smaller, manageable sub-tasks. It utilizes principles from "Least-to-Most Prompting" and recursive divide-and-conquer algorithms to generate directed acyclic graphs (DAGs) of task dependencies.

## Core Capabilities
- **Recursive Decomposition**: Iteratively breaks down tasks until a minimum granularity threshold is reached.
- **Dependency Analysis**: Identifies prerequisites and sequential constraints among sub-tasks.
- **Task Graph Generation**: Constructs a `graphlib.TopologicalSorter` compatible DAG for execution scheduling.
- **Strategy Selection**: Dynamically switches between Least-to-Most, Breadth-First, and Depth-First decomposition based on problem complexity.

## Theoretical Foundations
- **Least-to-Most Prompting**: Zhou et al. (2022) - Breaking problems into sequential sub-problems and solving them sequentially.
- **Task Network Models**: Hierarchical Task Network (HTN) planning.

## Architecture
- `TaskNode`: Represents an individual sub-task.
- `DecompositionEngine`: Applies decomposition heuristics.
- `DependencyResolver`: Validates and structures task dependencies to prevent circular loops.
