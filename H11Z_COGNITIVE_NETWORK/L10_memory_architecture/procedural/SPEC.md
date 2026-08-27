> **Layer 10** · Memory Architecture · `H11-PROCEDURAL`

## Purpose
The H11-PROCEDURAL agent isolates and governs non-declarative, implicit memory—specifically skill memory, cognitive motor programs, and automated habit formation. While other memory layers deal with "knowing that," this agent is exclusively concerned with "knowing how." It translates repeated explicit sequences into compiled, low-latency procedural macros.

## Technical Deep-Dive
Proceduralization is modeled as a transition from declarative knowledge representation (slow, explicit, associative) to compiled action chunks (fast, implicit, sequence-optimized). The agent utilizes a Hierarchical Chunking mechanism akin to ACT-R's production compilation.
Skill acquisition progresses through Fitts' three stages: Cognitive, Associative, and Autonomous. Habit strength is computed using an exponential decay learning curve, where reward prediction error (RPE) modulates the learning rate.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `sequence` | `List[str]` | The sequence of cognitive actions. |
| `success_rate` | `float` | Reward or success probability of the execution. |
| `context_id` | `str` | State descriptor for habit triggering. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `compiled_macro` | `str` | A compressed reference to the action chunk. |
| `habit_strength` | `float` | Current automaticity score [0.0, 1.0]. |

### State Schema
The agent maintains a `SkillTrie` for fast prefix matching of action sequences, alongside a `HabitStrengthMatrix` mapping contexts to optimal macros.

## Dependencies
### Upstream
- `H11-EPISODIC`: Provides recent successful action sequences for proceduralization.
### Downstream
- `H11-ACTION`: Consumes compiled macros for fast execution.

## Failure Modes
- **Negative Transfer**: Incorrect application of a compiled macro in a slightly altered context.
- **Skill Degradation**: Loss of habit strength due to lack of reinforcement (though typically slower than declarative decay).
- **Over-automatization**: Inability to interrupt a triggered macro due to high habit strength.

## Performance Characteristics
- Execution Latency: <5ms for macro retrieval (vs >100ms for declarative planning).
- Memory: Highly compressed, storing only successful state-action pairs.

## Research References
- Fitts, P. M. (1964). Perceptual-motor skill learning.
- Anderson, J. R. (1982). Acquisition of cognitive skill (ACT-R theory).

## Implementation Notes
Implement with a Trie-based sequence compressor. Habit strength updating must follow a standard temporal difference (TD) learning rule.
