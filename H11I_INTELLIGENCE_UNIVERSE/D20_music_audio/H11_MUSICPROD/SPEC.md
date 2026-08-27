> **Layer 20** · Music & Audio · `H11-MUSICPROD`

## Purpose

The H11-MUSICPROD agent operates as the virtual producer and mixing engineer. It translates orchestrated tracks into a polished, sonically balanced product by applying EQ, compression, spatialization (panning, reverb), and saturation strategies based on stylistic reference profiles.

## Technical Deep-Dive

MUSICPROD uses a combination of psychoacoustic models (e.g., masking threshold analysis) and deep neural networks trained on multitrack datasets (like MUSDB18) to automate mixing decisions. It constructs an audio processing graph (DAG) where nodes represent DSP units.
It calculates spectral density to identify masking conflicts and applies dynamic EQ and sidechain compression to resolve them. Spatial placement is determined via a multi-dimensional panning matrix ensuring mono-compatibility.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| multitrack | List[AudioBuffer] | Raw stems or rendered tracks |
| genre_profile | String | e.g., "EDM", "LoFi", "Pop" |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| mix_bus | AudioBuffer | Final mixed stereo/atmos file |
| processing_chain | Dict | DSP settings per track |

### State Schema
- master_lufs: Current loudness metric.
- dsp_graph: Current routing structure.

## Dependencies

### Upstream (depends on)
- H11-ORCHESTRATIO
- H11-ELECTRONICA-MUS

### Downstream (feeds into)
- H11-AUDIOENG (Mastering)

## Failure Modes
- Over-compression leading to pumping and loss of transient detail.
- Phase cancellation from improper stereo widening.

## Performance Characteristics
- High GPU/CPU utilization for running multiple DSP effect simulations simultaneously.

## Research References
- Roebel, A., "Spectral Processing of Audio" (2010)
- Martinez-Ramirez et al., "Deep Learning for Audio Effects" (2019)

## Implementation Notes
Ensure phase coherence when applying parallel processing in the DSP graph. Use linear-phase EQs when splitting bands.
