> **Layer 20** · Music & Audio · `H11-CLASSICA-MUS`

## Purpose

The H11-CLASSICA-MUS agent specializes in the highly structured forms, counterpoint rules, and historical performance practices of Western Classical Music (Baroque through Late Romantic). It enforces strict idiomatic constraints that general composition agents might overlook.

## Technical Deep-Dive

CLASSICA-MUS employs symbolic constraint-solving (using SAT solvers) to strictly enforce Fuxian species counterpoint and Bach-style chorale rules (no parallel fifths, correct resolution of leading tones, preparation of dissonances). 
It also contains knowledge graphs defining period-specific instrumentation (e.g., Harpsichord vs. Fortepiano) and idiomatic trill/ornamentation realizations (starts on upper vs. lower neighbor).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| raw_score | ScoreData | Unstylized score |
| period | String | e.g., "Baroque", "Classical" |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| stylized_score | ScoreData | Articulations and ornaments added |
| counterpoint_errors | List[Error] | Any strict rule violations |

### State Schema
- active_period: The historical era currently being emulated.

## Dependencies

### Upstream (depends on)
- H11-COMPOSITIO

### Downstream (feeds into)
- H11-ORCHESTRATIO

## Failure Modes
- SAT solver timeout on extremely dense polyphonic textures.
- Anachronistic instrument mapping (e.g., adding a saxophone to a Mozart piece).

## Performance Characteristics
- Computationally intensive logic programming layer for constraint solving.

## Research References
- Fux, J. J., "Gradus ad Parnassum" (1725)
- Gjerdingen, R., "Music in the Galant Style" (2007)

## Implementation Notes
Implement ornamentation as macro-expansions that occur right before performance rendering, preserving the clean symbolic score.
