> **Layer 20** · Music & Audio · `H11-ORCHESTRATIO`

## Purpose

The H11-ORCHESTRATIO agent assigns abstract musical lines to specific instruments or sound sources, managing timbre, register, and ensemble dynamics. It acts as a virtual conductor, translating dynamics (p, mf, ff) into continuous MIDI CC curves (expression, modulation, breath).

## Technical Deep-Dive

ORCHESTRATIO models acoustic instrument properties (tessitura, formants, polyphony limits) using knowledge graphs of orchestration treatises (e.g., Rimsky-Korsakov, Adler). 
It employs constrained optimization to map a generic N-voice texture to an M-instrument ensemble, maximizing timbral blend or contrast based on the desired target vector. Continuous controller (CC) data is generated using parameterized Perlin noise and envelope followers to simulate human breath and bowing mechanics.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| score | List[Voice] | Unassigned musical parts |
| ensemble | List[Instrument] | Available instruments |
| style_target | String | e.g., "Hollywood", "Chamber" |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| orchestrated_score | List[Track] | Mapped to specific instruments |
| expression_curves | Dict[int, List] | MIDI CC curves per track |

### State Schema
- active_ensemble: The current instrumentation map.
- dynamic_level: Global ensemble intensity (0.0 - 1.0).

## Dependencies

### Upstream (depends on)
- H11-HARMONIA
- H11-RHYTHMUS

### Downstream (feeds into)
- H11-MUSICPROD

## Failure Modes
- Out-of-range assignments (e.g., asking a flute to play C2).
- Masking: Assigning frequencies that cancel out or muddy the mix pre-production.

## Performance Characteristics
- High memory usage for loading instrument acoustic profiles.

## Research References
- Adler, S., "The Study of Orchestration" (2002)
- Bretos et al., "Acoustics of Orchestral Instruments" (1999)

## Implementation Notes
Include a robust rule engine to prevent impossible instrumental actions (like breathing while playing indefinitely on a wind instrument).
