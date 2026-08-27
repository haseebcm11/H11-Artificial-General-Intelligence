> **Layer 20** · Music & Audio · `H11-FILMSCORE`

## Purpose

The H11-FILMSCORE agent synchronizes musical generation with external visual or narrative timelines. It handles SMPTE timecode, hit points, and adaptive branching for video games (FMOD/Wwise paradigms).

## Technical Deep-Dive

FILMSCORE operates as a temporal constraints solver. Given a set of visual "hit points" (e.g., explosion at 01:02:15:10) and an emotional curve, it calculates optimal tempos and meter changes to align musical downbeats with visual cues using a dynamic programming approach (tempo mapping).
For interactive media, it constructs state machines of audio stems, managing crossfades and parameter interpolations based on game-state variables (e.g., `combat_intensity`).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| timecode_events | List[Event] | SMPTE hit points |
| narrative_arc | List[Float] | Emotional intensity over time |
| is_interactive | Boolean | Linear film vs adaptive game |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| tempo_map | Dict | Time to BPM mappings |
| stems_trigger_logic | Dict | Branching logic for game engines |

### State Schema
- current_smpte: Active timecode frame.
- game_state_vars: Dictionary of interactive variables.

## Dependencies

### Upstream (depends on)
- H11-COMPOSITIO (instructs it what to write)

### Downstream (feeds into)
- H11-MUSICPROD (for final stem mixing)

## Failure Modes
- Unplayable tempo curves (e.g., jumping from 60 to 240 BPM in one beat to catch a hit point).
- Phasing issues during adaptive stem crossfading.

## Performance Characteristics
- High precision timecode parsing required. Low latency response for interactive state changes.

## Research References
- Sweet, M., "Writing Interactive Music for Video Games" (2014)
- Karlin, F., "On the Track: A Guide to Contemporary Film Scoring" (2004)

## Implementation Notes
Tempo maps must resolve to exact sample-accurate positions to prevent drift over long feature films. Always anchor calculations to absolute time (seconds) rather than cumulative beats.
