> **Layer 10** · Memory Architecture · `H11-SCRATCHPAD`

## Purpose
The H11-SCRATCHPAD agent provides an ephemeral, highly structured working memory space designed specifically for intermediate reasoning, chain-of-thought (CoT) unrolling, and hypothesis generation. Unlike persistent semantic or episodic memory, the scratchpad serves as a "hidden" cognitive workspace where the system can execute multi-step logic, hold temporary variables, and draft outputs before finalizing them.

By offloading intermediate computation to the scratchpad, the system reduces the cognitive load on the primary context window and minimizes the risk of hallucination caused by premature commitment to an output. It functions analogously to the human phonological loop and visuospatial sketchpad.

## Technical Deep-Dive
The architecture of H11-SCRATCHPAD relies on a Tree-of-Thought (ToT) data structure combined with a structured semantic parsing engine. The scratchpad is not merely a flat text buffer; it represents reasoning steps as a directed acyclic graph (DAG). Each node in the DAG represents a distinct logical proposition, calculation, or hypothesis. 

When reasoning branches out (e.g., exploring multiple solutions), the scratchpad forks its state. The system uses a specialized heuristic evaluation metric to prune unpromising branches, maintaining a compact set of active hypotheses. Furthermore, it integrates a "hidden scratchpad" mechanism where raw token generation occurs off-policy, and only the finalized, synthesized conclusions are injected back into the main prompt flow. This is inspired by the "Quiet-STaR" and "Pause Tokens" methodologies, allowing the LLM extra compute time to reason without cluttering the final output space.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `task_context` | `string` | The overarching goal or problem being solved. |
| `initial_propositions` | `list[Proposition]` | Seed facts or assumptions to populate the root node. |
| `branching_factor` | `int` | Maximum allowed parallel reasoning paths (default: 3). |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `synthesized_conclusion` | `string` | The final derived answer or plan. |
| `reasoning_trace` | `list[ThoughtNode]` | The winning path through the reasoning DAG. |
| `discarded_hypotheses` | `list[string]` | Explanations of why alternative paths were rejected. |

### State Schema
- `reasoning_tree`: A DAG of `ThoughtNode` objects.
- `active_frontiers`: Pointers to the leaf nodes currently being expanded.
- `variable_bindings`: A key-value store for temporary computational results (e.g., `X = 42`).

## Dependencies
### Upstream (depends on)
- `H11-ROUTER` (Layer 9): Receives complex tasks requiring multi-step reasoning.
### Downstream (feeds into)
- `H11-REFLECTION-MEM`: Failed branches are sent for meta-cognitive analysis.
- `H11-WORKING-MEM`: Final conclusions are integrated into the active session context.

## Failure Modes
- **Combinatorial Explosion**: If the branching factor is unconstrained, the DAG grows exponentially, exhausting memory.
- **Premature Convergence**: Heuristic pruning might aggressively cut off a valid reasoning path too early.
- **Variable Collisions**: Namespace clashes in the temporary variable bindings during parallel branch execution.

## Performance Characteristics
- Latency: Medium-to-High (due to iterative internal expansion).
- Memory: Highly volatile; peaks during wide branching, drops after pruning.

## Research References
- Yao, S., et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models."
- Zelikman, E., et al. (2024). "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking."
- Goyal, A., et al. (2023). "Think Before You Speak: Training Language Models With Pause Tokens."

## Implementation Notes
Use an asynchronous task queue for expanding frontier nodes to maximize parallel API utilization. Implement garbage collection for pruned branches to keep the context size within token limits.
