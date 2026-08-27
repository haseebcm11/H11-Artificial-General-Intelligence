> **Layer 21** · Literature & Linguistics · `H11-SOCIOLINGUIST`

## Purpose
The H11-SOCIOLINGUIST agent models language variation across social dimensions (class, gender, age, ethnicity) and contextual registers (formal, casual, intimate). It enables dynamic style-shifting and code-switching in generation, and detects socio-demographic signals in text.

## Technical Deep-Dive
SOCIOLINGUIST utilizes a multi-dimensional latent variable model where the generation distribution is conditioned on a vector representing social variables. It leverages sociolinguistic variable rules (e.g., Labovian variable rules) encoded as probabilistic constraints over phonetic, morphological, and syntactic choices.
For style-shifting, it tracks the "audience design" (Bell's framework), adapting the linguistic output to converge with or diverge from the interlocutor based on modeled social distance and power dynamics.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| base_text | str | The underlying message |
| speaker_profile | Dict | Social variables of speaker |
| audience_profile | Dict | Social variables of listener |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| adapted_text | str | Register-adapted text |
| variation_markers | List[str] | Key sociolinguistic variants used |
| social_distance | float | Modeled distance between speaker and audience |

### State Schema
Maintains a network of sociolinguistic variables and current audience accommodation state.

## Dependencies
- H11-PRAGMATICA (for interpersonal context)
- H11-MORPHOLOGIA (for variant realization)

## Failure Modes
- `Hypercorrection`: Over-applying prestige variants leading to unnatural output.
- `RegisterClash`: Mixing highly formal syntax with highly informal lexicon.

## Performance Characteristics
Low latency, implemented via conditioned decoding or fast lexicosyntactic substitution.

## Research References
- "Computational Sociolinguistics"
- "Audience Design in Language Generation"

## Implementation Notes
Use variable rules represented as logistic regression weights over linguistic contexts.
