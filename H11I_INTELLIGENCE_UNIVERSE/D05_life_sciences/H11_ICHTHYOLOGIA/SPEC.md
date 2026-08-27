> **Layer 5** · Ichthyology & Fish · `H11-20`

## Purpose
The Ichthyologia Agent models marine and freshwater fish populations, fluid dynamic swimming efficiency, oceanic migration, and fisheries management scenarios. It evaluates the impact of ocean acidification and temperature shifts on aquatic biodiversity.

## Technical Deep-Dive
Integrates Navier-Stokes approximations for fish propulsion hydrodynamics, bioenergetics modeling for growth over the life-cycle, and age-structured population models (like the Leslie matrix) to determine maximum sustainable yield (MSY) in fisheries.

## Architecture (Input Contract, Output Contract, State Schema)
- **Input**: Oceanographic telemetry (temperature, salinity, currents), catch data, species life history parameters.
- **Output**: Biomass projections, MSY quotas, hydrodynamic drag coefficients.
- **State**: Age-structured population vectors, spatial density grids in 3D (including depth).

## Dependencies
- numpy, scipy
- xarray for multidimensional ocean data
- sympy for analytical hydrodynamic approximations

## Failure Modes
- Ignoring depth stratification can lead to erroneous spatial overlaps between predator and prey.
- Overestimating recruitment due to hidden variables like microplastic disruption on larval stages.

## Performance Characteristics
3D spatial movement tracking requires octree structures `O(N log N)`. Matrix multiplication for age structures is highly efficient `O(A^3)` where A is max age.

## Research References
- Helfman, G., Collette, B. B., Facey, D. E., & Bowen, B. W. (2009). The Diversity of Fishes.
- Quinn, T. J., & Deriso, R. B. (1999). Quantitative Fish Dynamics.

## Implementation Notes
Deep integration with physical oceanography layers needed for accurate migratory drift and metabolic rate scaling.
