> **Layer 21** · Literature & Linguistics · `H11-SEMANTICA`

## Purpose
The H11-SEMANTICA agent models lexical and compositional semantics. It determines word senses, resolves polysemy, maps predicate-argument structures (semantic roles), and constructs meaning representations of sentences.

## Technical Deep-Dive
SEMANTICA uses Abstract Meaning Representation (AMR) parsing to build rooted, directed graphs where nodes represent concepts and edges represent relations (e.g., ARG0 for agent, ARG1 for patient).
It maps words to senses in a robust ontology (like WordNet or BabelNet) using contextualized word embeddings. For compositional semantics, it applies Montague grammar principles mapped to continuous spaces (Tensor Product Representations) to bind roles to fillers algebraically without losing discrete structural properties.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sentence | str | Input sentence |
| domain | str | Specific domain for sense disambiguation |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| amr_graph | Dict | AMR representation |
| word_senses | Dict[str, str] | Token to synset mapping |
| semantic_roles | List[Dict] | Extracted predicate-arguments |

### State Schema
Tracks the current discourse referents and ontology cache.

## Dependencies
- H11-MORPHOLOGIA (for base lemmas)

## Failure Modes
- `SenseAmbiguity`: Unable to resolve a polysemous word due to insufficient context.
- `RoleBindingFailure`: Predicate argument requirements are violated by the parsed arguments.

## Performance Characteristics
AMR parsing is O(N^3) in the worst case using standard graph parsers, optimized here via transition-based shift-reduce algorithms to O(N).

## Research References
- "Abstract Meaning Representation (AMR) for Semantic Parsing"
- "Tensor Product Representations for Compositional Semantics"

## Implementation Notes
Use smatch score for internal validation of generated AMR graphs.
