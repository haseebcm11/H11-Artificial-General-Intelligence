> **Layer 6** · Narrative Architect · `H11-CONTENT`

## Purpose
H11-CONTENT acts as the semantic engine for the Media & Communication domain. It manages the lifecycle of intellectual capital, transforming raw data, insights, and strategic goals into structured narrative architectures. It dictates *what* is said, *when* it is said, and *how* it connects to the broader cognitive substrate's objectives.

## Technical Deep-Dive
The core mechanism is a Directed Acyclic Graph (DAG) representing the "Content Ontology." Each node is a discrete unit of information (a thesis, a fact, a claim). H11-CONTENT utilizes Graph Neural Networks (GNNs) to traverse this ontology and construct coherent logical paths (narratives).

To maintain engagement over time, it employs a Markov Decision Process (MDP) to sequence content drops, optimizing for the "Narrative Tension" metric. The agent models the audience's knowledge state and probabilistically calculates the optimal next piece of information to reveal to maximize curiosity and retention.

Natural Language Generation is heavily constrained by the parameters received from H11-BRANDING, utilizing specialized decoding strategies (like nucleus sampling with dynamically adjusted temperature) to balance creativity with brand safety.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `strategic_objective` | `str` | High-level goal (e.g., "Establish thought leadership in AGI"). |
| `brand_constraints` | `BrandState` | Output from H11-BRANDING. |
| `raw_data_sources` | `List[DataPointer]` | References to internal databases. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `content_dag` | `NarrativeGraph` | Sequence of content pieces. |
| `drafts` | `List[ContentDraft]` | Raw generated text. |

### State Schema
Maintains the `GlobalContentOntology`, a massive knowledge graph of all previously published and planned information, ensuring zero contradiction in historical output.

## Dependencies
### Upstream (depends on)
- `H11-BRANDING`: Provides stylistic guardrails.
- `H11-CORE` (Hypothetical): Provides strategic objectives.

### Downstream (feeds into)
- `H11-SEO`: For optimization.
- `H11-PR`: For distribution.
- `H11-VIDEO`: For script generation.

## Failure Modes
- **Ontological Contradiction**: Generating a claim that violates a previously established node in the knowledge graph.
- **Tension Collapse**: MDP fails to sequence properly, dumping all information at once and losing audience engagement.
- **Context Window Exhaustion**: Narrative graphs become too large for the NLG model to maintain coherence.

## Performance Characteristics
- Latency: Can take up to 30 seconds for a deep DAG traversal and long-form draft generation.
- Memory: Requires extensive RAM to hold the Global Content Ontology in memory for fast GNN traversal.

## Research References
- Scarselli, Franco, et al. (2008). "The graph neural network model."
- Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction.

## Implementation Notes
Use `NetworkX` for ontology management and a graph database (e.g., Neo4j) for persistent storage. The NLG backend should support constrained decoding frameworks like `guidance` or `outlines`.
