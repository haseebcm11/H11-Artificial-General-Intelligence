> **Layer 20** · Music & Audio · `H11-AUDIOENG`

## Purpose

The H11-AUDIOENG agent represents the final stage of audio production: mastering and acoustic analysis. It ensures the final output meets broadcast standards, manages loudness compliance (LUFS), and handles format conversions, dithering, and acoustic room correction simulations.

## Technical Deep-Dive

AUDIOENG uses multi-band dynamics and brickwall limiting driven by predictive lookahead algorithms to maximize loudness without introducing inter-sample peaks or clipping. It calculates integrated LUFS, True Peak, and LRA (Loudness Range) according to ITU-R BS.1770-4.
Additionally, it can synthesize impulse responses (IRs) for specific acoustic environments using ray-tracing acoustic models.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| mix_buffer | AudioBuffer | The stereo or surround mix |
| target_spec | String | e.g., "Spotify", "AES Streaming" |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| master_buffer | AudioBuffer | The finalized audio |
| compliance_report | Dict | LUFS, True Peak stats |

### State Schema
- current_true_peak: Max peak detected.
- integrated_lufs: Overall loudness.

## Dependencies

### Upstream (depends on)
- H11-MUSICPROD
- H11-SOUNDDESIGN

### Downstream (feeds into)
- Export / Delivery systems.

## Failure Modes
- Exceeding True Peak limit leading to DAC distortion.
- Pumping artifacts from overly aggressive multi-band limiting.

## Performance Characteristics
- Fast I/O requirements for large uncompressed audio buffers. Lookahead buffers require moderate RAM.

## Research References
- ITU-R BS.1770-4 Standard for Loudness Measurement.
- Katz, B., "Mastering Audio: The Art and the Science" (2007)

## Implementation Notes
Implement true-peak metering using at least 4x oversampling to accurately catch inter-sample peaks.
