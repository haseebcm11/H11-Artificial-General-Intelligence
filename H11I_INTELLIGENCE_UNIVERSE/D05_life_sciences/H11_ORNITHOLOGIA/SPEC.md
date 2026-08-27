> **Layer 5** · Ornithology & Birds · `H11-18`

## Purpose
The Ornithologia Agent computes and simulates avian population ecology, migration flyways, aerodynamic flocking behaviors, and vocalization spectrogram analytics. It provides insights into how global climate shifts affect avian migratory timing and range expansion.

## Technical Deep-Dive
Implements the Boids algorithm for flocking physics, hidden Markov models (HMM) for analyzing bioacoustic song patterns, and spatial interpolation for mapping migratory routes based on satellite telemetry.

## Architecture (Input Contract, Output Contract, State Schema)
- **Input**: Telemetry tracking data, audio acoustic recordings, wind sheer data.
- **Output**: Migration route probabilities, flock aerodynamic efficiency, song dialect classifications.
- **State**: Boid position/velocity vectors, flyway geofences.

## Dependencies
- numpy, scipy, librosa (for acoustic processing)
- geopandas for migration maps

## Failure Modes
- Boid simulations can collapse into singular points if separation weights are too low.
- Acoustic interference in bioacoustic inputs can lead to misclassification.

## Performance Characteristics
Flocking `O(N^2)` naive, optimized to `O(N log N)` using KD-Trees for nearest neighbor lookups.

## Research References
- Reynolds, C. W. (1987). Flocks, herds and schools: A distributed behavioral model.
- Catchpole, C. K., & Slater, P. J. B. (2008). Bird Song: Biological Themes and Variations.

## Implementation Notes
Includes hooks for KD-Tree implementations to keep large flock simulations performant.
