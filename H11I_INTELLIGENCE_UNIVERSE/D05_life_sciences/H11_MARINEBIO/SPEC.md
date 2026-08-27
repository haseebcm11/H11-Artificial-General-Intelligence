> **Layer 5** · Marine biology & ocean life · `H11-MARINEBIO`

## Purpose
The H11-MARINEBIO agent models marine ecosystems, oceanographic interactions with marine life, coral reef ecology, and pelagic food webs. It focuses on the physiological adaptations of organisms in aquatic environments.

## Technical Deep-Dive
Integrates physical oceanography parameters (salinity, temperature, pressure, currents) with biological models. Uses coupled differential equations for phytoplankton-zooplankton-nekton food webs. Models coral bleaching events based on Degree Heating Weeks (DHW).

## Architecture (Input Contract, Output Contract, State Schema)
- **Input**: Oceanographic telemetry, species counts, SST (Sea Surface Temp) anomalies.
- **Output**: Trophic energy transfer rates, bleaching risk assessments, migration routes.
- **State Schema**: 3D spatial grids mapping marine habitats, temperature profiles, species distributions.

## Dependencies
- NumPy, SciPy (multidimensional grid processing, PDE solvers)
- Matplotlib/Seaborn (generating profile plots implicitly for downstream)
- Pandas (timeseries ocean data)

## Failure Modes
- Sparse deep-sea data causing high uncertainty in mesopelagic models.
- Rigid trophic layers failing to capture complex omnivory or ontogenetic diet shifts.

## Performance Characteristics
- 3D spatial grid operations scale O(X*Y*Z) but optimized via vectorized NumPy.
- Trophic cascades computed in near real-time.

## Research References
- Nybakken, J. W., & Bertness, M. D. (2005). Marine Biology: An Ecological Approach.
- Hoegh-Guldberg, O. (1999). Climate change, coral bleaching and the future of the world's coral reefs.

## Implementation Notes
Employs Eulerian grids for ocean physics and Lagrangian particle tracking for larvae/plankton dispersion.
