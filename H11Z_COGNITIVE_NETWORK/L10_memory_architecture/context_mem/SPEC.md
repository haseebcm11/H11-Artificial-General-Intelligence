> **Layer 10** · Memory Architecture · `H11-CONTEXT-MEM`

## Purpose
H11-CONTEXT-MEM is responsible for maintaining, mutating, and projecting the active conversational and situational context over multi-turn interactions. Unlike static key-value stores, context is a fluid entity that requires rapid switching, ambient awareness of peripheral topics, and graceful degradation of stale information.

This agent ensures that the AI substrate intuitively understands the "room" it is in. It tracks entities under discussion, implicit pronouns, and conversational framing. When the topic shifts abruptly, H11-CONTEXT-MEM preserves the previous context as an "ambient" state, allowing seamless resumption if the user reverts to the prior topic.

## Technical Deep-Dive
The agent implements a Hierarchical Recurrent State Tracker (HRST) coupled with a Transformer-based Context Condensation mechanism. 
1. **Short-Term Turn Buffer**: Maintains the exact tokens of the last $k$ turns.
2. **Entity-Relation Sub-Graph**: Extracts and dynamically links entities discussed in the active window, resolving anaphora (e.g., mapping "it" to "the deployment script").
3. **Ambient Context Pool**: Older contexts are compressed into summary embeddings using an auto-regressive condensation phase. These compressed contexts inhabit the ambient pool. 

When an input arrives, a Context Switch Predictor (CSP) — a lightweight attention head — calculates the divergence between the current input and the active entity sub-graph. If divergence exceeds a threshold, a context switch is triggered: the active context is shunted to the ambient pool, and either a new context is initialized or a matching dormant context from the ambient pool is reactivated via cosine similarity.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `turn_utterance` | `str` | The latest raw text from user/system |
| `extracted_entities` | `List[Entity]` | Named entities parsed by upstream NER |
| `force_switch` | `bool` | Explicit signal to reset the active context |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `active_context_summary` | `str` | Condensed text representing current context |
| `resolved_anaphora` | `Dict[str, str]` | Mapping of pronouns to entities |
| `ambient_topics` | `List[str]` | Titles of dormant contexts |
| `switch_occurred` | `bool` | True if the topic shifted |

### State Schema
A dynamic tri-partite state: `[Active Window Buffer (FIFO)]`, `[Entity Sub-Graph (Graph)]`, and `[Ambient Pool (LRU Cache of Embeddings)]`.

## Dependencies
### Upstream (depends on)
- `H11-NER`: Provides extracted entities per turn.
- `H11-EMBEDDING-ENGINE`: Used to compress contexts.
### Downstream (feeds into)
- `H11-GENERATOR`: Uses `active_context_summary` to condition LLM generation.
- `H11-SESSION`: Persists the final ambient pool at session teardown.

## Failure Modes
- **Context Bleed**: Aggressive condensation merges two distinct topics, causing the agent to hallucinate connections between unrelated user intents.
- **Anaphora Misdirection**: Incorrectly resolving a pronoun to the wrong entity in the sub-graph, poisoning subsequent generative responses.
- **Thrashing**: Rapid oscillations between contexts on consecutive turns due to a hyper-sensitive Context Switch Predictor.

## Performance Characteristics
- Latency: < 20ms for update and retrieval; < 100ms during a context condensation event.
- Memory: Highly optimized. The ambient pool caps at 100 contexts, ejecting oldest via LRU.

## Research References
- Rae, J. W., et al. (2019). Compressive Transformers for Long-Range Sequence Modelling.
- Su, H., et al. (2019). Improving Multi-turn Dialogue Modelling with Utterance ReWriter.

## Implementation Notes
Implement the Context Switch Predictor using a fast dot-product attention against the centroids of the entity embeddings in the active graph. Condensation operations should be executed asynchronously to avoid blocking the critical response path.
