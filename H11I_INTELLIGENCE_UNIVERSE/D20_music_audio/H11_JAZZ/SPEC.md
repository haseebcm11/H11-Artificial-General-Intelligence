> **Layer 20** · Music & Audio · `H11-JAZZ`

## Purpose

The H11-JAZZ agent models the highly adaptive, real-time nature of jazz improvisation, chord-scale theory, and reharmonization. It generates solos over complex chord changes and injects idiomatic syncopation and substitutions (e.g., tritone subs, Coltrane changes).

## Technical Deep-Dive

JAZZ employs a reinforcement learning agent trained on transcribed solos from the jazz idiom (Parker, Coltrane, Davis). It maps chords to an allowed scale matrix (Chord-Scale Theory) and uses a Markov chain for navigating the "bebop vocabulary" (enclosures, chromatic approaches).
It dynamically re-evaluates the harmonic progression to substitute chords (e.g., ii-V-I becomes ii-bII7-I) without violating the melody.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| chord_changes | List[String] | e.g., ["Dm7", "G7", "Cmaj7"] |
| style | String | e.g., "Bebop", "Modal" |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| solo_line | List[Note] | The improvised melody |
| substituted_chords | List[String] | The reharmonized changes |

### State Schema
- current_chord: The chord currently being played over.
- tension_level: Measure of chromaticism vs diatonicism.

## Dependencies

### Upstream (depends on)
- H11-HARMONIA (for base changes)

### Downstream (feeds into)
- H11-RHYTHMUS (for swing injection)

## Failure Modes
- Overuse of chromatic enclosures leading to atonal noise.
- Losing track of the form (playing the wrong changes).

## Performance Characteristics
- High speed required for real-time generative solos.

## Research References
- Levine, M., "The Jazz Theory Book" (1995)
- Simon, I. et al., "Learning to Generate Jazz Melodies" (2018)

## Implementation Notes
Implement "guide tone" targeting (3rds and 7ths) on strong beats to ensure the generated lines clearly outline the underlying harmony.
