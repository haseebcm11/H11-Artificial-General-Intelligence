> **Layer 20** · Music & Audio · `H11-ELECTRONICA-MUS`

## Purpose

The H11-ELECTRONICA-MUS agent specializes in synthesized sound generation, complex modulation matrices, and sequencer-driven beatmaking. It acts as a virtual modular synthesizer and sequencer, focused on timbral exploration and heavily quantized, loop-based musical forms.

## Technical Deep-Dive

ELECTRONICA-MUS utilizes differentiable DSP graphs to synthesize sounds from scratch (Wavetable, FM, Additive, and Granular synthesis). It employs recurrent models to generate evolving parameter automation (LFOs, envelopes) that create motion within the sound. 
Beat generation relies on cellular automata and Euclidean rhythms specifically tailored for the grid-based quantization of dance music genres (Techno, House, IDM).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| genre | String | e.g., "Techno", "Ambient" |
| tempo | Float | BPM |
| timbral_seed | List[Float] | Latent vector for synth design |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| synth_patches | List[Patch] | Synthesizer parameters |
| sequences | List[MIDIClip] | Note and automation data |

### State Schema
- global_swing: Current MPC-style swing percentage.
- active_oscillators: Number of voices currently synthesized.

## Dependencies

### Upstream (depends on)
- H11-RHYTHMUS (for underlying grid math)

### Downstream (feeds into)
- H11-MUSICPROD

## Failure Modes
- Aliasing from un-bandlimited oscillator generation.
- Chaotic modulation feedback loops resulting in DC offset.

## Performance Characteristics
- High CPU demand for real-time differentiable DSP rendering.

## Research References
- Engel et al., "DDSP: Differentiable Digital Signal Processing" (2020)
- Collins, N., "Introduction to Computer Music" (2009)

## Implementation Notes
Implement internal anti-aliasing via oversampling in the oscillator generation phase before decimation to the target sample rate.
