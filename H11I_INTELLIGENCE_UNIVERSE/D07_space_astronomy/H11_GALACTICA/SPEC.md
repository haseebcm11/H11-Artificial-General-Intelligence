> **Layer 7** · Space & Astronomy · `H11-GALACTICA`

## Purpose
Simulates galactic dynamics, spiral arm density waves, and dark matter halos. It maps out galactic structures and handles N-body simulations of galactic mergers and Active Galactic Nuclei (AGN) feedback.

## Technical Deep-Dive
Implements N-body tree codes (Barnes-Hut) for collisionless stellar dynamics and SPH (Smoothed Particle Hydrodynamics) for interstellar gas. Calculates Navarro-Frenk-White (NFW) dark matter profiles to match observed flat rotation curves.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| galaxy_mass | float | Baryonic mass in solar masses |
| dark_matter_fraction | float | Ratio of DM to baryonic |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| rotation_curve | List[Tuple] | Radius vs Velocity |
| morphological_type | str | Hubble classification |

### State Schema
Holds the octree structure for current N-body dynamics step.
