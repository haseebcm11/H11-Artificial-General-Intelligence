> **Layer 10** · Memory Architecture · `H11-RECALL`

## Purpose
While H11-RETRIEVAL handles the mechanical extraction of indexed data, H11-RECALL models the psychological process of cue-dependent, reconstructive memory. It manages priming effects, context-dependent memory, and associative spread, assembling fragmented data into cohesive subjective recall.

## Technical Deep-Dive
Human memory is not a hard drive; it is reconstructive. This agent implements Spreading Activation Networks (SAN) where nodes are concepts and edges are association strengths. A query acts as an initial stimulus, activating nodes. Activation spreads via a decay function.
To handle the LLM phenomenon analogous to human false memories, H11-RECALL includes a Confabulation Detection mechanism, evaluating the entropy of the reconstructed memory trace against cryptographic source hashes or foundational axioms.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `cue` | `str` | The environmental or internal stimulus. |
| `context_state` | `Dict` | The current emotional/environmental state. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `reconstructed_trace` | `str` | The final assembled memory. |
| `confabulation_risk` | `float` | Estimated probability of hallucination [0,1]. |

### State Schema
Maintains transient `PrimingActivations` which decay rapidly over short timescales (seconds/minutes), biasing subsequent recalls.

## Dependencies
### Upstream
- `H11-RETRIEVAL`: Raw chunks that form the basis of the reconstruction.
- `H11-EMOTION`: Provides affective state for mood-congruent memory recall.
### Downstream
- `H11-CONSCIOUSNESS`: Places the recalled thought into the global workspace.

## Failure Modes
- **Confabulation**: High-confidence generation of false connections between retrieved facts.
- **Tip-of-the-Tongue State**: Activation threshold reached for neighbors, but target node remains sub-threshold.
- **Priming Bias**: Prior unrelated queries strongly skewing current recall out of context.

## Performance Characteristics
- Latency: Designed for sub-100ms associative spread.
- Memory: Requires large in-memory graph representation (NetworkX equivalent) of recent concepts.

## Research References
- Collins, A. M., & Loftus, E. F. (1975). A spreading-activation theory of semantic processing.
- Schacter, D. L. (1999). The seven sins of memory: Insights from psychology and cognitive neuroscience.
