# H11-DELEGATION Specification

## Core Role
Responsible for capability-aware routing, workload balancing, and multi-tiered task delegation to specialized sub-agents. 

## Technical Foundation
- **Capability Vector Matching**: Utilizes multi-dimensional embeddings and structural capability vectors to score sub-agent fitness for specific tasks.
- **Stable Assignment via Max-Heap**: Adapts greedy matching algorithms for bipartite mapping between tasks and available sub-agents based on dynamic capability profiles and current workload.
- **Execution Topologies**: Supports parallel, sequential, and recursive delegation chains with automatic topological sorting of task dependencies.
- **Result Aggregation**: Map-reduce paradigms to aggregate results from sub-agent responses.

## Interfaces
- **Input**: Complex task specifications with explicit capability requirements, sub-agent capability registry, current load metrics.
- **Output**: Delegation topology, routing tables, and real-time execution bounds.
