> **Layer 20** · Music & Audio · `H11-HARMONIA`

## Purpose

The H11-HARMONIA agent processes melodic and structural representations to yield complex, context-aware harmonic progressions. It enforces rules of voice leading, functional harmony, and chromatic alteration, translating abstract emotional goals into concrete chordal structures.

## Technical Deep-Dive

HARMONIA utilizes a Neo-Riemannian graph combined with probabilistic hidden Markov models (HMMs) for chord transitions. Voice leading is solved as an optimal transport problem, minimizing the parallel fifths and octaves while satisfying the chord constraints.
By traversing tonal spaces (Tonnetz), it can fluidly modulate between distant keys, providing both tonal and post-tonal harmonic landscapes.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| melody | List[Note] | Melody to harmonize |
| complexity | Float | 0.0 (triads) to 1.0 (clusters/extensions) |
| target_key | String | e.g., "C_major" |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| chord_progression | List[Chord] | Generated harmonic sequence |
| voice_led_lines | List[List[Note]] | Individual voice parts |

### State Schema
- current_tonality: The active key center.
- recent_chords: Buffer of recent progressions for context.

## Dependencies

### Upstream (depends on)
- H11-COMPOSITIO

### Downstream (feeds into)
- H11-ORCHESTRATIO
- H11-MUSICPROD

## Failure Modes
- Voice leading violations (unintended parallel fifths).
- Tonal ambiguity in inappropriate contexts.

## Performance Characteristics
- Computationally heavy during voice-leading optimization (combinatorial constraints).

## Research References
- Tymoczko, D., "A Geometry of Music" (2011)
- Cohn, R., "Audacious Euphony" (2012)

## Implementation Notes
Implement dynamic programming (Viterbi) for optimal chord sequences over melodies.
