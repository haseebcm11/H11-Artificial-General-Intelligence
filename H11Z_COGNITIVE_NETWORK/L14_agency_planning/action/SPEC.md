# H11-ACTION: Parameterized Action execution and DAG Sequencer

## 1. Architectural Overview
H11-ACTION implements a Parameterized Action Markov Decision Process (PAMDP) executor integrated with Saga-based compensating transaction logic. This structure is designed to handle hybrid discrete-continuous action spaces, verify preconditions, execute concurrent action sequences via a Directed Acyclic Graph (DAG), and guarantee system safety through automatic rollback (compensation).

## 2. Mathematical Foundations
The system operates on an action space defined as:
`A = {(d, θ_d) | d ∈ D, θ_d ∈ Θ_d}`
Where:
- `D` is a finite set of discrete action types.
- `Θ_d` is the continuous/discrete parameter space specific to action `d`.

A Feasibility Function `F: S x A -> {True, False}` checks if action `a` is valid in state `s` based on preconditions `P(a, s)` and parameter bounds `B(θ_d)`.

## 3. Core Mechanisms
- **Action Space Definition & Feasibility:** Parameters are strictly typed with boundaries. Preconditions are evaluated against the current state tensor/dictionary before any execution sequence begins.
- **Concurrent Execution DAG:** Actions are vertices in a DAG, where directed edges represent sequential dependencies. Independent branches are executed in parallel using non-blocking asynchronous workers.
- **Saga Pattern Rollback:** If action `A_i` fails, the execution halts (no new nodes started). A compensation phase triggers, executing the inverse actions `C_i` for all completed nodes in the reverse topological order of the DAG, ensuring the environment is returned to a safe state.

## 4. Components
- `ActionTemplate`: Defines parameter bounds, required preconditions, execution logic, and compensation logic.
- `FeasibilityChecker`: Engine that applies boundary checks and condition matching.
- `SagaDAGExecutor`: The concurrent orchestrator managing the state machine of each action node (PENDING -> RUNNING -> COMPLETED/FAILED).
