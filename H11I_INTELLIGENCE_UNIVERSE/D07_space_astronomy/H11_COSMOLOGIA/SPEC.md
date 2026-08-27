> **Layer 7** · Space & Astronomy · `H11-COSMOLOGIA`

## Purpose

The H11-COSMOLOGIA agent is responsible for cosmological modeling, large-scale structure analysis, and understanding the evolution of the universe. It processes cosmic microwave background (CMB) data, dark matter distributions, and dark energy equations of state to provide macro-level insights into the fabric of spacetime and universal expansion.

This agent operates at the largest possible scales in the H11 substrate, integrating data from distant quasars, galaxy clusters, and primordial radiation to model the universe's past, present, and future state.

## Technical Deep-Dive

H11-COSMOLOGIA employs advanced tensor calculus and general relativistic numerical simulations to model cosmic expansion and large-scale structure formation. It utilizes N-body simulations for dark matter halos and hydrodynamical simulations for baryonic matter, coupling these to analyze the cosmic web.

A core algorithm is the Cosmic Microwave Background Spherical Harmonic Analyzer, which decomposes CMB temperature and polarization maps into multipole moments ($C_\ell$). This allows the agent to extract precise cosmological parameters such as the Hubble constant, baryon density, and dark energy density, utilizing Markov Chain Monte Carlo (MCMC) methods to explore parameter space.

Furthermore, the agent models dark energy utilizing dynamic scalar field theories (quintessence) alongside the standard $\Lambda$CDM model. It assesses the expansion rate history using baryon acoustic oscillations (BAO) as a standard ruler, correlating large-scale galaxy surveys with theoretical predictions.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `cmb_maps` | `List[SphericalHarmonicMap]` | CMB temperature and polarization data |
| `galaxy_surveys` | `RedshiftCatalog` | 3D positions of galaxies and quasars |
| `expansion_data` | `ExpansionMetrics` | Supernovae Ia and BAO distance measurements |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `cosmological_parameters` | `CosmoParams` | Derived parameters (H0, Omega_m, Omega_Lambda, etc.) |
| `large_scale_structure` | `CosmicWebModel` | Modeled distribution of dark and baryonic matter |
| `evolution_forecast` | `ExpansionForecast` | Predictive model of future universal expansion |

### State Schema
- `current_epoch`: Redshift z tracking the current focus of the simulation.
- `parameter_posteriors`: Probability distributions of cosmological parameters.
- `model_tensions`: Identified discrepancies between early and late universe measurements (e.g., Hubble tension).

## Dependencies

### Upstream (depends on)
- `H11-GALACTICA`: Provides statistical data on galaxy distributions and cluster masses.
- `H11-ASTROPHYSICA`: Supplies standardized luminosity data from supernovae.

### Downstream (feeds into)
- `H11-DEEPSPACE`: Informs deep space navigation about metric expansion effects on extreme distances.

## Failure Modes
- `ParameterDegeneracy`: Inability to distinguish between different cosmological models due to overlapping parameter effects.
- `CosmicVarianceLimit`: Statistical uncertainty on the largest scales due to the limited observable volume.
- `TensorDivergence`: Numerical instability in general relativistic simulations leading to non-physical solutions.

## Performance Characteristics
- Highly parallelized N-body simulations requiring extreme GPU/TPU compute.
- Memory-intensive spherical harmonic transforms for high-resolution CMB maps.
- High-latency parameter estimation via nested sampling algorithms.

## Research References
- Planck Collaboration: Cosmological parameters
- Lambda Cold Dark Matter ($\Lambda$CDM) paradigm
- Baryon Acoustic Oscillations in large galaxy surveys

## Implementation Notes
Requires robust precision arithmetic for tensor calculations. MCMC samplers must be optimized for multi-modal posteriors.
