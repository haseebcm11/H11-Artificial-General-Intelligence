# H11-COLLABORATION Agent Specification

## Overview
The `H11-COLLABORATION` agent orchestrates distributed multi-agent systems using a hybrid architecture that combines a **Stochastic Blackboard System** for shared knowledge representation, the **Contract Net Protocol (CNP)** for decentralized task allocation, and a **Lightweight Paxos Consensus Mechanism** for conflict resolution over shared resources.

## Architectural Components

### 1. Stochastic Blackboard System
The Blackboard serves as a central repository for shared state and partial solutions. Instead of a simple key-value store, it utilizes stochastic confidence decay. Knowledge Sources (KS) post `KnowledgeEntry` objects that contain confidence metrics.
- **Entry Structure**: `(Topic, Payload, Author, BaseConfidence, HalfLife)`
- **Retrieval**: Agents query the blackboard, which returns entries whose time-adjusted confidence exceeds a given threshold.

### 2. Contract Net Protocol (CNP) for Role Assignment
When a complex task needs delegation, the agent acts as a Manager:
1. **Call For Proposals (CFP)**: Broadcasts task requirements (required capabilities, max cost, deadline).
2. **Bidding**: Sub-agents evaluate their utility functions and submit `Bid`s (cost, time, quality estimates).
3. **Evaluation & Award**: The manager uses a multi-criteria decision analysis (MCDA) function to rank bids and emits an `Award` message to the optimal contractor.

### 3. Paxos-lite Consensus for Conflict Resolution
When multiple agents attempt to modify conflicting plan nodes or resource allocations simultaneously, the agent enacts a Paxos-based consensus round.
- **Phase 1 (Prepare/Promise)**: Proposer requests a lease with sequence number `N`. Acceptors promise not to accept proposals `< N`.
- **Phase 2 (Accept/Accepted)**: Proposer broadcasts the state change. Acceptors commit if the sequence number is valid.

## Integration in H11-AGI
This module sits at L14 (Agency Planning), enabling the Cognitive Substrate to divide complex cognitive workloads among specialized sub-agents while guaranteeing eventual consistency and optimal task routing.
