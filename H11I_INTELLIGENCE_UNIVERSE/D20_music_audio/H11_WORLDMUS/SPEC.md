> **Layer 20** · Music & Audio · `H11-WORLDMUS`

## Purpose

The H11-WORLDMUS agent specializes in non-Western tuning systems, microtonal scales, and rhythmic cycles (Talas, Maqams, Ragas). It prevents the substrate from being confined exclusively to 12-tone equal temperament (12-TET) and 4/4 western time signatures.

## Technical Deep-Dive

WORLDMUS utilizes dynamic tuning tables (Scala format, MTS) to map pitches to exact frequency ratios (e.g., Just Intonation, Pythagorean, Slendro/Pelog). It employs grammar-based generation for modal improvisation, adhering to strict rules of ascent (arohana) and descent (avarohana) characteristic of Indian Ragas or Arabic Maqams.
Rhythmically, it models cyclical time (e.g., a 16-beat Tintal) using circular arrays rather than linear timelines.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| tradition | String | e.g., "Hindustani", "Gamelan" |
| base_frequency | Float | Concert pitch (e.g., 432Hz or 440Hz) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| tuning_map | Dict | MIDI note to Frequency map |
| stylized_events | List[Note] | Culturally accurate performance |

### State Schema
- active_scale: The current microtonal scale ratios.
- rhythmic_cycle: The active cyclical meter.

## Dependencies

### Upstream (depends on)
- H11-COMPOSITIO (for base structural intent)

### Downstream (feeds into)
- H11-ORCHESTRATIO

## Failure Modes
- Pitch quantization errors if downstream synths force 12-TET.
- Cultural misappropriation via incorrect mapping of ornaments (e.g., playing a Gamaka incorrectly).

## Performance Characteristics
- Low memory, but requires high-precision floating point math for exact cent calculations.

## Research References
- Daniélou, A., "Musical Scales of the World" (1968)
- Touma, H. H., "The Music of the Arabs" (1996)

## Implementation Notes
Use MIDI Pitch Bend or MPE (MIDI Polyphonic Expression) to transmit microtonal information to downstream sound engines that do not natively support Scala tuning files.
