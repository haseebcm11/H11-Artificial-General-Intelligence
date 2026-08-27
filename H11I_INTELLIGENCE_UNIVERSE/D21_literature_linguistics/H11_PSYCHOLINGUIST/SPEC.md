> **Layer 21** · Literature & Linguistics · `H11-PSYCHOLINGUIST`

## Purpose
The H11-PSYCHOLINGUIST agent models human cognitive processing of language. It estimates reading times, predicts garden-path sentence parsing difficulties, measures cognitive load, and models language acquisition trajectories. 

## Technical Deep-Dive
PSYCHOLINGUIST uses Surprisal Theory and Dependency Locality Theory (DLT) to calculate the cognitive load of a sentence word-by-word. It maintains a probabilistic incremental parser (e.g., a pushdown automaton with bounded stack depth based on working memory constraints) to simulate human sentence processing.
When the parser's most likely predicted structure is contradicted by incoming tokens, it calculates a reanalysis cost (the garden-path effect), which is exposed as a processing difficulty metric.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sentence | str | Input sentence to process |
| subject_profile | Dict | Cognitive limits (e.g., working memory capacity) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| surprisal_curve | List[float] | Surprisal value per token |
| parse_difficulty | float | Global difficulty score |
| garden_path_indices | List[int] | Indices where reanalysis occurred |

### State Schema
Tracks the active parser stack and the simulated working memory buffer.

## Dependencies
- H11-SEMANTICA (for integration cost)

## Failure Modes
- `StackOverflow`: The simulated working memory limit is exceeded by center-embedding.
- `IrrecoverableParse`: The sentence is so convoluted that the simulated parser fails entirely.

## Performance Characteristics
O(N) processing time per sentence using beam-search incremental parsing.

## Research References
- "Surprisal Theory of Language Processing"
- "Dependency Locality Theory"

## Implementation Notes
Use an N-gram language model or a causal transformer constrained to emit token probabilities sequentially.
