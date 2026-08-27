> **Layer 21** · Literature & Linguistics · `H11-ETYMOLOGIA`

## Purpose
The H11-ETYMOLOGIA agent reconstructs linguistic history, models language change over time, and maps cognate relationships across language families. It traces the semantic drift and phonetic shifts of lexical items from proto-languages to their modern forms.

## Technical Deep-Dive
ETYMOLOGIA utilizes phylogenetic trees to represent language families (e.g., Indo-European). It applies the comparative method algorithmically, using dynamic time warping (DTW) on articulatory feature sequences to find regular sound correspondences between sister languages.
Semantic drift is modeled via diachronic word embeddings, tracking how a word's vector representation moves through semantic space over centuries, enabling it to explain how a word like "nice" shifted from meaning "foolish" to "pleasant".

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| word | str | The target word |
| language | str | The language of the word |
| target_depth | str | E.g., "PIE" (Proto-Indo-European) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| proto_form | str | Reconstructed ancestor form |
| cognates | List[Dict] | Related words in other languages |
| semantic_trajectory | List[str] | Historical meanings |

### State Schema
Caches historical corpora embeddings and established sound laws (e.g., Grimm's Law).

## Dependencies
- H11-PHONETICA (for historical sound shifts)
- H11-SEMANTICA (for diachronic semantic vectors)

## Failure Modes
- `ReconstructionFailure`: The word is an isolate or a recent coinage with no deep etymology.
- `FalseCognate`: Matching words based on chance phonetic similarity rather than shared ancestry.

## Performance Characteristics
Tree traversal over the language phylogenetic graph scales O(V+E) per query.

## Research References
- "Computational Historical Linguistics"
- "Diachronic Word Embeddings Reveal Statistical Laws of Semantic Change"

## Implementation Notes
Implement sound laws as ordered rewrite rules (FSTs) that run in reverse for reconstruction.
