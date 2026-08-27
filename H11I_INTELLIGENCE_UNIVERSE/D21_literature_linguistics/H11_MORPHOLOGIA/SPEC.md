> **Layer 21** · Literature & Linguistics · `H11-MORPHOLOGIA`

## Purpose
The H11-MORPHOLOGIA agent analyzes internal word structure. It handles inflectional and derivational morphology, tokenizes text into morphemes, and synthesizes correctly affixed words from lemma structures.

## Technical Deep-Dive
MORPHOLOGIA employs a two-level morphological model (Koskenniemi) implemented via composed finite-state transducers (FSTs). The lexical tape contains underlying morphemes, while the surface tape contains the orthographic realization.
For agglutinative or polysynthetic languages, it uses recurrent neural networks over character sequences to predict morpheme boundaries where strict FST coverage fails. It maintains a lattice of morphological parses to handle ambiguity (e.g., "runs" as noun vs. verb).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| words | List[str] | Surface forms to parse |
| operation | str | "analyze" or "generate" |
| features | Dict | Features for generation (if applicable) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| parses | List[List[Morpheme]] | Morphological parses |
| surface_forms | List[str] | Generated words |
| ambiguity_score | float | Measure of parse uncertainty |

### State Schema
Tracks transducer composition graphs and a cache of frequent word parses.

## Dependencies
- H11-SEMANTICA (for disambiguating parses based on context)

## Failure Modes
- `TransducerDeadEnd`: No valid path exists in the FST for the given surface form.
- `Overgeneration`: Synthesizing a theoretically valid but practically non-existent word.

## Performance Characteristics
Microsecond latency per word via FST determinization and minimization.

## Research References
- "Two-Level Morphology"
- "Neural Morphological Tagging and Parsing"

## Implementation Notes
Rely on OpenFST or similar optimized libraries for graph operations.
