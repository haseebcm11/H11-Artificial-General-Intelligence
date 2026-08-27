> **Layer 7** · Space & Astronomy · `H11-PLANETOLOGIA`

## Purpose
Analyzes planetary formation, atmospheric composition, and exoplanet detection methods. It interprets transit light curves and radial velocity measurements to characterize alien worlds.

## Technical Deep-Dive
Implements Mandel & Agol transit models for exoplanet light curve fitting. Uses Keplerian orbital mechanics to decouple multiple planetary signals from radial velocity periodograms. Runs radiative-convective atmospheric models to estimate planetary equilibrium temperatures and potential habitability.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| transit_data | List[float] | Time-series flux dips |
| rv_data | List[float] | Radial velocity shifts |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| planet_radius | float | In Earth radii |
| planet_mass | float | In Earth masses |
| habitability_index | float | 0.0 to 1.0 score |

### State Schema
Tracks known exoplanet catalog and transit ephemerides.

## Dependencies
### Upstream
H11-ASTRONOMIA
### Downstream
H11-EXOBIOLOGIA

## Failure Modes
- False positive transit from eclipsing binaries
- Stellar activity masking RV signals

## Performance Characteristics
Uses MCMC sampling for transit fitting, requiring substantial CPU parallelization.
