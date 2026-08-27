> **Layer 21** · Literature & Linguistics · `H11-TRANSLATIO`

## Purpose
The H11-TRANSLATIO agent performs literary and context-aware translation. Unlike standard machine translation which optimizes for semantic fidelity at the sentence level, TRANSLATIO optimizes for aesthetic equivalence, stylistic preservation, and cultural adaptation.

## Technical Deep-Dive
TRANSLATIO uses a multi-objective decoding strategy. The primary objective is semantic equivalence (measured via cross-lingual embeddings), while secondary objectives include rhythmic matching, register preservation, and idiom mapping.
Cultural adaptation is handled by an ontology-bridging module that detects culture-specific items (CSIs) and determines whether to use domestication (adapting to the target culture) or foreignization (retaining the source culture flavor) based on the translation brief.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| source_text | str | Text to translate |
| source_lang | str | Source language code |
| target_lang | str | Target language code |
| strategy | str | 'domestication' or 'foreignization' |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| translated_text | str | The final translation |
| stylistic_score | float | Measure of stylistic preservation |
| cultural_notes | List[str] | Translator notes on CSIs |

### State Schema
Tracks the bilingual lexicon cache and the stylistic fingerprint of the source text.

## Dependencies
- H11-MORPHOLOGIA (for word-level adaptation)
- H11-SOCIOLINGUIST (for dialect and register mapping)

## Failure Modes
- `IdiomMiss`: Fails to recognize a multi-word expression, resulting in literal translation.
- `RegisterDrift`: The translation inappropriately shifts formality levels compared to the source.

## Performance Characteristics
Slower than standard MT due to the stylistic decoding constraints.

## Research References
- "Literary Machine Translation"
- "Domestication and Foreignization in Neural MT"

## Implementation Notes
Use minimum-risk training criteria tailored for literary metrics.
