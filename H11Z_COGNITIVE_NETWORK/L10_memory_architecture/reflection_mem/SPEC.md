> **Layer 10** · Memory Architecture · `H11-REFLECTION-MEM`

## Purpose
The H11-REFLECTION-MEM agent provides meta-cognitive oversight. Instead of storing *what* happened, it stores *why* things succeeded or failed. It implements continuous self-evaluation and rule extraction, generalizing from past experiences to build a persistent database of operational heuristics.

By analyzing historical trajectories and identifying systematic errors (e.g., repeating a failed tool call, hallucinating API formats), this agent updates the system's "Self-Correction Guidelines." This closely mirrors the Reflexion architecture, enabling the agentic system to iteratively improve its behavior across episodes without updating model weights.

## Technical Deep-Dive
The core algorithm involves Trajectory Analysis and Heuristic Induction. 
When an episodic sequence is completed (especially if flagged as a failure or inefficient), the agent processes the Action-Observation pairs. It applies a Counterfactual Reasoning technique: "If the system had done X instead of Y, would the outcome have improved?"

The agent extracts formal `Heuristic` records, which include pre-conditions, the identified anti-pattern, and the recommended corrective action. To manage the growth of the reflection database, the agent uses a Differentiable Rule Merging approach, semantically clustering similar rules and generating a generalized super-rule using contrastive learning embeddings. 

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `episode_trajectory` | `list[Step]` | Sequence of actions, thoughts, and environment observations. |
| `outcome_metric` | `float` | Score indicating success (1.0) or failure (0.0). |
| `task_description` | `string` | The original goal. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `extracted_heuristics` | `list[Heuristic]` | New rules derived from the trajectory. |
| `critique_summary` | `string` | A meta-analysis of the agent's performance. |

### State Schema
- `heuristic_database`: A vector store mapping task contexts to relevant behavioral rules.
- `rule_confidence_scores`: Bayesian updates tracking how often a heuristic successfully prevents a failure.

## Dependencies
### Upstream (depends on)
- `H11-EPISODIC-MEM`: Provides the raw event trajectories.
- `H11-SCRATCHPAD`: Provides the discarded reasoning branches for error analysis.
### Downstream (feeds into)
- `H11-SYSTEM-PROMPT-MANAGER` (Layer 9): Feeds active heuristics into the system prompt for future tasks.

## Failure Modes
- **Over-generalization**: Extracting a rule that is too broad, constraining the agent inappropriately in future novel situations.
- **Rule Conflict**: Generating contradictory heuristics (e.g., "Always verify thoroughly" vs "Prioritize speed over redundant checks").
- **Stale Reflections**: Maintaining heuristics for external environments (like APIs) that have since been updated or deprecated.

## Performance Characteristics
- Computation: Background batch processing (low latency requirement).
- Storage: Requires vector indexing for semantic retrieval of rules.

## Research References
- Shinn, N., et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning."
- Madaan, A., et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback."

## Implementation Notes
Store heuristics with an explicit "context window" embedding. During retrieval, use Maximum Marginal Relevance (MMR) to fetch diverse rules to prevent contradictory rules from dominating the prompt.
