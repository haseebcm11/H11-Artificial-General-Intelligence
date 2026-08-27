> **Layer 21** · Literature & Linguistics · `H11-POESIS`

## Purpose
The H11-POESIS agent specializes in the computational modeling and generation of poetic forms. It encapsulates the rhythmic, structural, and phonetic requirements of diverse poetic traditions (e.g., sonnets, haikus, villanelles). It identifies meter, rhyme schemes, and stylistic figures in existing poetry, and synthesizes new poetry according to rigid or free-verse structural constraints.

## Technical Deep-Dive
POESIS utilizes advanced phonetic dictionaries (like CMUDict) integrated with neural syllable-counting algorithms to ensure meter adherence. For structural conformity, it employs a constrained decoding mechanism during text generation, where the token probabilities are masked based on phonetic and metrical permissibility.
Rhythmic modeling is achieved via finite-state automata (FSA) that represent permissible metrical feet (iambs, trochees, anapests, etc.).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| form | str | The target poetic form (e.g., "sonnet", "freeverse") |
| theme | str | Thematic constraints or prompts |
| meter | str | Specific meter requirement (e.g., "iambic_pentameter") |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| lines | List[str] | The generated poetic lines |
| scheme | str | The detected or applied rhyme scheme |
| metrical_score | float | Score indicating adherence to the meter |

### State Schema
Tracks the current generation state, rhyming dictionary cache, and phonetic mapping trees.

## Dependencies
- H11-PHONETICA (for phonetic transcription)
- H11-SEMANTICA (for thematic coherence)

## Failure Modes
- `MetricalIncoherence`: Unable to find tokens that satisfy both meter and semantics.
- `RhymeExhaustion`: No remaining rhymes for a given end-word that fit the thematic context.

## Performance Characteristics
High latency during constrained decoding (up to 5x standard generation) due to vocabulary masking per token based on phonetic features.

## Research References
- "Constrained Language Models for Poetry Generation"
- "Rhythmic Syllable Parsing with FSA"

## Implementation Notes
Use dynamic programming for syllable alignment.
