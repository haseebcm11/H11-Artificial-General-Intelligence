> **Layer 21** · Literature & Linguistics · `H11-CRITICA-LIT`

## Purpose
The H11-CRITICA-LIT agent applies literary theory frameworks (e.g., Marxist, Feminist, Post-Colonial, Psychoanalytic, Formalist) to analyze texts. It extracts thematic elements, uncovers ideological subtexts, and evaluates the aesthetic and rhetorical qualities of the writing.

## Technical Deep-Dive
CRITICA-LIT utilizes a multi-lens interpretive pipeline. It maps textual features (character interactions, word choice, focalization) into a high-dimensional vector space representing theoretical concepts. By projecting the text's embeddings onto the canonical vectors of a given theoretical framework, it quantifies alignment and devises critical arguments.
It employs argument-mining models to construct logically sound critical essays, identifying thesis statements, supporting evidence from the text, and counter-arguments.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| text | str | The literary text to analyze |
| framework | str | Theoretical lens to apply |
| depth | float | Depth of analysis (0.0 to 1.0) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| critique | str | The generated critical essay/analysis |
| extracted_themes | List[str] | Key themes identified |
| theoretical_alignment | float | How strongly the text aligns with the lens |

### State Schema
Tracks the current theoretical lens weights and the argument tree being constructed.

## Dependencies
- H11-SEMANTICA (for thematic extraction)
- H11-NARRATIO (for structural breakdown)

## Failure Modes
- `LensOverfit`: Forcing a theoretical interpretation that lacks textual evidence.
- `ArgumentCollapse`: The generated critique contradicts its own thesis.

## Performance Characteristics
Compute-intensive during the projection phase of high-dimensional textual embeddings onto theoretical manifolds.

## Research References
- "Computational Literary Criticism"
- "Vector Space Models for Literary Theory"

## Implementation Notes
Ensure the framework canonical vectors are pre-computed during initialization.
