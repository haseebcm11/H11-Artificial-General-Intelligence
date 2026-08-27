> **Layer 20** · Music & Audio · `H11-SOUNDDESIGN`

## Purpose

The H11-SOUNDDESIGN agent focuses on non-musical audio, environmental soundscapes, UI sounds, and Foley. It synthesizes impacts, whooshes, ambiances, and textural elements without relying on pre-recorded sample libraries.

## Technical Deep-Dive

SOUNDDESIGN employs Procedural Audio techniques. It uses Physical Modeling Synthesis (mass-spring networks, modal synthesis) to simulate the collisions, scrapes, and fractures of materials (wood, glass, metal). Fluid dynamics models are used for wind and water simulation.
For abstract UI sounds, it utilizes FM and Granular synthesis. It heavily leverages noise shaping and envelope followers to create hyper-realistic or hyper-stylized audio elements on demand.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| event_description | String | e.g., "Heavy metal door slamming" |
| stylization | Float | 0.0 (Realistic) to 1.0 (Sci-Fi) |
| duration | Float | Desired length in seconds |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| audio_buffer | AudioBuffer | Rendered sound effect |
| synthesis_params | Dict | The procedural recipe |

### State Schema
- active_models: Current physical models in memory.
- ambient_noise_floor: Baseline environmental noise.

## Dependencies

### Upstream (depends on)
- Text/Event input from external systems or FILMSCORE.

### Downstream (feeds into)
- H11-MUSICPROD (for mixing into the final stem)
- H11-AUDIOENG

## Failure Modes
- Physical model explosion (DSP instability causing infinite gain).
- Uncanny valley audio (sounds *almost* like wood but feels synthetic).

## Performance Characteristics
- Highly parallelizable DSP calculations. Can run on GPU compute shaders.

## Research References
- Farnell, A., "Designing Sound" (2010)
- Bilbao, S., "Numerical Sound Synthesis" (2009)

## Implementation Notes
Implement strict limiting and DC-blocking filters inside physical models to prevent feedback loops from blowing out audio buffers during modal synthesis.
