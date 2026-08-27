> **Layer 4** · Theoretical Models · `H11-COMPUTABILITAS`

## Purpose

H11-COMPUTABILITAS is the ultimate theoretical boundary-checker for the AGI substrate. Its sole purpose is to analyze mathematical and computational propositions to determine if they are formally computable (decidable), partially computable, or fundamentally undecidable (like the Halting Problem).

Before the substrate invests massive computational resources into solving a complex logic puzzle, optimizing a recursive compiler pass, or proving a theorem, COMPUTABILITAS analyzes the problem space. If a problem reduces to Post's Correspondence Problem or Hilbert's Tenth Problem (Diophantine equations), this agent terminates the execution immediately, preventing infinite loops and wasted resources.

## Technical Deep-Dive

COMPUTABILITAS uses formal logic and proof assistants (e.g., Coq, Lean, Z3 SMT solver) to analyze the structure of input programs or propositions. It relies heavily on Rice's Theorem, asserting that all non-trivial semantic properties of programs are undecidable. To bypass this in practical terms, it enforces strict type systems, total functional programming (where all functions are guaranteed to terminate), and bounded model checking.

When asked to determine if a Turing-complete subsystem will halt, it attempts to find a ranking function (a well-founded mathematical mapping that strictly decreases with each state transition). If a valid ranking function is found, the system is proven to halt. If the state space is too complex, it applies bounded abstraction (e.g., abstract interpretation) to give a probabilistically safe answer.

It maps computational questions directly into the Arithmetic Hierarchy ($\Sigma_n$, $\Pi_n$) to classify exactly *how* unsolvable a problem is.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| computational_model| str | AST, State Machine, or Logic Formula |
| query_type | ComputabilityQuery | HALTING, EQUIVALENCE, REACHABILITY |
| resource_bound | int | Max proof steps for the SMT solver |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| decidability_status| Status | DECIDABLE, UNDECIDABLE, UNKNOWN |
| proof_artifact | Optional[str] | Coq/Lean proof of termination |
| counterexample | Optional[str] | State sequence leading to infinite loop |
| hierarchy_class | str | e.g., Pi_0_1, Sigma_0_1 |

### State Schema
- `proved_theorems`: Cache of previously verified termination proofs.
- `smt_cache`: Memoized Z3 contexts for rapid sub-problem resolution.

## Dependencies

### Upstream (depends on)
- H11-ALGORITHMICA: Identifies the complexity bounds; if bounds are infinite, COMPUTABILITAS engages.
- H11-AUTOMATA: Provides the DFA/Turing machine representation of the logic.

### Downstream (feeds into)
- H11-COMPILER: Refuses to compile undecidable macros or unbounded recursive templates.
- H11-TESTING: Uses the SMT solver to generate fuzzing inputs.

## Failure Modes
- `UndecidabilityTrap`: The agent attempts to prove whether its own proof-checker will halt, leading to a Gödelian paradox and requiring a hard timeout.
- `SMTStateExplosion`: The boolean satisfiability clauses for a Reachability query exceed available memory.
- `FalseCompleteness`: Assuming a program terminates because the bounded model checker didn't find a loop within the maximum depth limit.

## Performance Characteristics
- Latency: Can range from 10ms (simple structural checks) to hours (deep SMT constraint solving).
- Reliability: 100% accurate when returning DECIDABLE with a proof; uses bounded heuristics otherwise.

## Research References
- Sipser, M. (2012). *Introduction to the Theory of Computation*.
- Turing, A. M. (1936). *On Computable Numbers, with an Application to the Entscheidungsproblem*.

## Implementation Notes
Integrates the Z3 Theorem Prover and relies heavily on symbolic execution techniques.
